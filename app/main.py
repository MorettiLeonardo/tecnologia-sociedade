from app.config import INPUT_FILE, OUTPUT_FILE
from app.services.analysis_service import (
    generate_analysis_tables,
    highest_cost_equipment,
    top_failure_types,
)
from app.services.cleaning_service import clean_data
from app.services.excel_service import read_excel, validate_columns
from app.services.pdf_service import write_results_pdf


def _print_top(title: str, df, cols: list[str], top_n: int = 5) -> None:
    print(f"\n{title}")
    if df.empty:
        print("Sem dados.")
        return
    print(df.loc[:, cols].head(top_n).to_string(index=False))


def run() -> None:
    raw_df = read_excel(INPUT_FILE)
    validate_columns(raw_df)

    cleaned_df, cleaning_summary_df = clean_data(raw_df)
    analysis_tables = generate_analysis_tables(cleaned_df)

    output_tables = {
        "dados_limpos": cleaned_df,
        "limpeza_resumo": cleaning_summary_df,
        **analysis_tables,
    }
    write_results_pdf(OUTPUT_FILE, output_tables)

    print(f"Total lido: {len(raw_df)}")
    print(f"Total após limpeza: {len(cleaned_df)}")

    _print_top(
        "Top 5 falhas por equipamento:",
        analysis_tables["falhas_por_equipamento"],
        ["equipamento", "total_falhas"],
    )
    _print_top(
        "Top 5 tipos de falha:",
        top_failure_types(cleaned_df, top_n=5),
        ["tipo_falha", "total_falhas"],
    )
    _print_top(
        "Top 5 equipamentos por custo:",
        highest_cost_equipment(cleaned_df),
        ["equipamento", "custo_total_manutencao"],
    )
