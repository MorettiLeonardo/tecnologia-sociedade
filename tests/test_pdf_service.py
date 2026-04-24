import pandas as pd

from app.services.pdf_service import write_results_pdf


def test_write_results_pdf_creates_file(tmp_path):
    output = tmp_path / "resultado.pdf"
    tables = {
        "dados_limpos": pd.DataFrame({"equipamento": ["Bomba A"], "total": [1]}),
        "limpeza_resumo": pd.DataFrame({"motivo": ["teste"], "linhas_removidas": [0]}),
    }

    write_results_pdf(output, tables)

    assert output.exists()
    assert output.stat().st_size > 0
