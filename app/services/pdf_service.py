from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def _format_value(value: object) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, pd.Timestamp):
        return value.strftime("%d/%m/%Y %H:%M:%S") if value.time() else value.strftime("%d/%m/%Y")
    return str(value)


def _table_from_dataframe(df: pd.DataFrame) -> Table:
    header = [str(col) for col in df.columns]
    rows = [[_format_value(value) for value in row] for row in df.itertuples(index=False, name=None)]
    data = [header] + rows if header else rows

    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    return table


def write_results_pdf(path: str | Path, tables: dict[str, pd.DataFrame]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(output_path), pagesize=landscape(A4))
    elements = [Paragraph("Relatório de Manutenção Industrial", styles["Title"]), Spacer(1, 12)]

    items = list(tables.items())
    for index, (name, table_df) in enumerate(items):
        title = name.replace("_", " ").title()
        elements.append(Paragraph(title, styles["Heading2"]))
        elements.append(Spacer(1, 6))

        if table_df.empty:
            elements.append(Paragraph("Sem dados.", styles["Normal"]))
        else:
            elements.append(_table_from_dataframe(table_df))

        if index < len(items) - 1:
            elements.append(PageBreak())

    doc.build(elements)
