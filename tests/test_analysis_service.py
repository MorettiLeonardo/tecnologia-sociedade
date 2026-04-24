import pandas as pd

from app.services.analysis_service import (
    failure_type_downtime_relation,
    failures_by_equipment,
    highest_cost_equipment,
)


def _analysis_df():
    return pd.DataFrame(
        {
            "equipamento": ["Bomba A", "Bomba A", "Motor X"],
            "tipo_falha": ["Vazamento", "Vazamento", "Superaquecimento"],
            "tempo_parada_horas": [2.0, 4.0, 3.0],
            "custo_manutencao": [100.0, 200.0, 500.0],
        }
    )


def test_failures_by_equipment_output():
    df = _analysis_df()
    result = failures_by_equipment(df)
    assert list(result.columns) == ["equipamento", "total_falhas"]
    assert result.loc[0, "equipamento"] == "Bomba A"
    assert result.loc[0, "total_falhas"] == 2


def test_highest_cost_equipment_output():
    df = _analysis_df()
    result = highest_cost_equipment(df)
    assert list(result.columns) == ["equipamento", "custo_total_manutencao"]
    assert result.loc[0, "equipamento"] == "Motor X"
    assert result.loc[0, "custo_total_manutencao"] == 500.0


def test_failure_type_downtime_relation_output():
    df = _analysis_df()
    result = failure_type_downtime_relation(df)
    expected_cols = [
        "tipo_falha",
        "tempo_medio_parada_horas",
        "tempo_mediano_parada_horas",
        "quantidade_ocorrencias",
    ]
    assert list(result.columns) == expected_cols
    row = result.loc[result["tipo_falha"] == "Vazamento"].iloc[0]
    assert row["tempo_medio_parada_horas"] == 3.0
    assert row["tempo_mediano_parada_horas"] == 3.0
    assert row["quantidade_ocorrencias"] == 2
