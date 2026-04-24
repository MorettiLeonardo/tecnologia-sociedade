import pandas as pd
import pytest

from app.services.excel_service import read_excel, validate_columns


def test_validate_columns_fails_when_missing_column():
    df = pd.DataFrame(
        {
            "equipamento": ["Bomba A"],
            "tipo_falha": ["Vazamento"],
            "data_falha": ["21/04/2026"],
            "data_manutencao": ["22/04/2026"],
            "tempo_parada_horas": ["2,5"],
            "custo_manutencao": ["100,0"],
            "status": ["Aberta"],
            "descricao": ["Teste"],
        }
    )

    with pytest.raises(ValueError):
        validate_columns(df)


def test_read_excel_integration(tmp_path):
    file_path = tmp_path / "sample.xlsx"
    expected = pd.DataFrame(
        {
            "equipamento": ["Bomba A"],
            "tipo_falha": ["Vazamento"],
            "data_falha": ["21/04/2026"],
            "data_manutencao": ["22/04/2026"],
            "tempo_parada_horas": ["2,5"],
            "custo_manutencao": ["100,0"],
            "status": ["aberta"],
            "prioridade": ["alta"],
            "descricao": ["Teste"],
        }
    )
    expected.to_excel(file_path, index=False, engine="openpyxl")

    read_df = read_excel(file_path)
    validate_columns(read_df)

    assert len(read_df) == 1
    assert set(read_df.columns) == set(expected.columns)


def test_validate_columns_accepts_optional_id_column():
    df = pd.DataFrame(
        {
            "id": [1],
            "equipamento": ["Bomba A"],
            "tipo_falha": ["Vazamento"],
            "data_falha": ["21/04/2026"],
            "data_manutencao": ["22/04/2026"],
            "tempo_parada_horas": ["2,5"],
            "custo_manutencao": ["100,0"],
            "status": ["Aberta"],
            "prioridade": ["Alta"],
            "descricao": ["Teste"],
        }
    )

    validate_columns(df)
