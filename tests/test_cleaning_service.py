import pandas as pd

from app.services.cleaning_service import clean_data, normalize_enums, parse_dates, parse_numbers


def _base_df():
    return pd.DataFrame(
        {
            "equipamento": ["bomba a", "motor x"],
            "tipo_falha": ["vazamento", "superaquecimento"],
            "data_falha": ["21/04/2026", "22/04/2026"],
            "data_manutencao": ["22/04/2026", "23/04/2026"],
            "tempo_parada_horas": ["2,5", "-1,0"],
            "custo_manutencao": ["100,50", "50,00"],
            "status": ["concluida", "em andamento"],
            "prioridade": ["alta", "media"],
            "descricao": ["desc", "desc 2"],
        }
    )


def test_parse_dates_ptbr():
    df = _base_df()
    parsed = parse_dates(df)
    assert str(parsed.loc[0, "data_falha"].date()) == "2026-04-21"
    assert str(parsed.loc[0, "data_manutencao"].date()) == "2026-04-22"


def test_parse_numbers_decimal_comma():
    df = _base_df()
    parsed = parse_numbers(df)
    assert parsed.loc[0, "tempo_parada_horas"] == 2.5
    assert parsed.loc[0, "custo_manutencao"] == 100.5


def test_normalize_status_and_prioridade():
    df = _base_df()
    normalized = normalize_enums(df)
    assert normalized.loc[0, "status"] == "Concluída"
    assert normalized.loc[1, "prioridade"] == "Média"


def test_negative_tempo_parada_is_removed():
    df = _base_df()
    cleaned, summary = clean_data(df)
    assert len(cleaned) == 1
    negatives = summary.loc[
        summary["motivo"] == "valores_numericos_negativos", "linhas_removidas"
    ].iloc[0]
    assert negatives == 1
