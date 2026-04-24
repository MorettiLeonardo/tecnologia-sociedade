import re
import unicodedata

import pandas as pd

from app.config import (
    NUMERIC_MIN_RULES,
    PRIORIDADE_ALLOWED,
    PRIORIDADE_NORMALIZATION_MAP,
    REQUIRED_COLUMNS,
    STATUS_ALLOWED,
    STATUS_NORMALIZATION_MAP,
)


def _normalize_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _normalize_key(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return _normalize_spaces(ascii_text).lower()


def _to_number(value: object) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None

    text = str(value).strip()
    if not text:
        return None

    text = text.replace(" ", "")
    if "," in text and "." in text and text.rfind(",") > text.rfind("."):
        text = text.replace(".", "").replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")

    try:
        return float(text)
    except ValueError:
        return None


def standardize_text(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    text_columns = ["equipamento", "tipo_falha", "status", "prioridade", "descricao"]

    for col in text_columns:
        if col not in result.columns:
            continue
        result[col] = result[col].apply(
            lambda val: _normalize_spaces(str(val)) if pd.notna(val) else val
        )

    for col in ("equipamento", "tipo_falha"):
        if col in result.columns:
            result[col] = result[col].apply(lambda val: val.title() if pd.notna(val) else val)

    return result


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    for col in ("data_falha", "data_manutencao"):
        if col in result.columns:
            result[col] = pd.to_datetime(result[col], dayfirst=True, errors="coerce")
    return result


def parse_numbers(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    for col in ("tempo_parada_horas", "custo_manutencao"):
        if col in result.columns:
            result[col] = result[col].apply(_to_number)
            result[col] = pd.to_numeric(result[col], errors="coerce")
    return result


def normalize_enums(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    if "status" in result.columns:
        result["status"] = result["status"].apply(
            lambda v: STATUS_NORMALIZATION_MAP.get(_normalize_key(str(v)))
            if pd.notna(v)
            else pd.NA
        )
    if "prioridade" in result.columns:
        result["prioridade"] = result["prioridade"].apply(
            lambda v: PRIORIDADE_NORMALIZATION_MAP.get(_normalize_key(str(v)))
            if pd.notna(v)
            else pd.NA
        )

    return result


def validate_business_rules(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    current = df.copy()
    summary: list[dict[str, object]] = []

    invalid_dates_mask = current["data_falha"].isna() | current["data_manutencao"].isna()
    removed = int(invalid_dates_mask.sum())
    summary.append({"motivo": "datas_invalidas", "linhas_removidas": removed})
    current = current.loc[~invalid_dates_mask].copy()

    invalid_negative_mask = pd.Series(False, index=current.index)
    for col, min_value in NUMERIC_MIN_RULES.items():
        if col in current.columns:
            invalid_negative_mask = invalid_negative_mask | (current[col] < min_value)
    removed = int(invalid_negative_mask.sum())
    summary.append({"motivo": "valores_numericos_negativos", "linhas_removidas": removed})
    current = current.loc[~invalid_negative_mask].copy()

    invalid_enum_mask = (~current["status"].isin(STATUS_ALLOWED)) | (
        ~current["prioridade"].isin(PRIORIDADE_ALLOWED)
    )
    removed = int(invalid_enum_mask.sum())
    summary.append({"motivo": "status_ou_prioridade_invalidos", "linhas_removidas": removed})
    current = current.loc[~invalid_enum_mask].copy()

    null_required_mask = current[REQUIRED_COLUMNS].isna().any(axis=1)
    removed = int(null_required_mask.sum())
    summary.append({"motivo": "nulos_em_campos_obrigatorios", "linhas_removidas": removed})
    current = current.loc[~null_required_mask].copy()

    return current.reset_index(drop=True), pd.DataFrame(summary)


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    processed = standardize_text(df)
    processed = parse_dates(processed)
    processed = parse_numbers(processed)
    processed = normalize_enums(processed)
    return validate_business_rules(processed)
