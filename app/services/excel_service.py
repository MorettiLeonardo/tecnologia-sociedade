from pathlib import Path

import pandas as pd

from app.config import DEFAULT_SHEET_NAME, EXPECTED_COLUMNS, OPTIONAL_INPUT_COLUMNS, REQUIRED_COLUMNS


def read_excel(path: str | Path, sheet_name: str | int = DEFAULT_SHEET_NAME) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name=sheet_name, engine="openpyxl")


def validate_columns(df: pd.DataFrame) -> None:
    current_cols = list(df.columns)
    expected = set(EXPECTED_COLUMNS)
    optional = set(OPTIONAL_INPUT_COLUMNS)
    current = set(current_cols)

    missing = [col for col in REQUIRED_COLUMNS if col not in current]
    unexpected = [col for col in current_cols if col not in expected and col not in optional]

    if missing or unexpected:
        parts = []
        if missing:
            parts.append(f"Colunas faltando: {missing}")
        if unexpected:
            parts.append(f"Colunas inesperadas: {unexpected}")
        raise ValueError("Estrutura inválida do Excel. " + " | ".join(parts))


def write_results(path: str | Path, tables: dict[str, pd.DataFrame]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, table in tables.items():
            safe_name = str(sheet_name)[:31]
            table.to_excel(writer, index=False, sheet_name=safe_name)
