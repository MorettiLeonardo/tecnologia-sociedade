import pandas as pd

from app.config import TOP_FAILURE_TYPES_N


def failures_by_equipment(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("equipamento", dropna=False)
        .size()
        .reset_index(name="total_falhas")
        .sort_values("total_falhas", ascending=False)
        .reset_index(drop=True)
    )
    return result


def avg_downtime_by_equipment(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("equipamento", dropna=False)["tempo_parada_horas"]
        .mean()
        .reset_index(name="tempo_medio_parada_horas")
        .sort_values("tempo_medio_parada_horas", ascending=False)
        .reset_index(drop=True)
    )
    return result


def top_failure_types(df: pd.DataFrame, top_n: int = TOP_FAILURE_TYPES_N) -> pd.DataFrame:
    result = (
        df.groupby("tipo_falha", dropna=False)
        .size()
        .reset_index(name="total_falhas")
        .sort_values("total_falhas", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    return result


def highest_cost_equipment(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("equipamento", dropna=False)["custo_manutencao"]
        .sum()
        .reset_index(name="custo_total_manutencao")
        .sort_values("custo_total_manutencao", ascending=False)
        .reset_index(drop=True)
    )
    return result


def failure_type_downtime_relation(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("tipo_falha", dropna=False)["tempo_parada_horas"]
        .agg(["mean", "median", "count"])
        .reset_index()
        .rename(
            columns={
                "mean": "tempo_medio_parada_horas",
                "median": "tempo_mediano_parada_horas",
                "count": "quantidade_ocorrencias",
            }
        )
        .sort_values("quantidade_ocorrencias", ascending=False)
        .reset_index(drop=True)
    )
    return result


def generate_analysis_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {
        "falhas_por_equipamento": failures_by_equipment(df),
        "tempo_medio_por_equipamento": avg_downtime_by_equipment(df),
        "falhas_por_tipo_top": top_failure_types(df),
        "equipamentos_maior_custo": highest_cost_equipment(df),
        "tipo_falha_x_tempo": failure_type_downtime_relation(df),
    }
