from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
INPUT_FILE = DATA_DIR / "input.xlsx"
OUTPUT_FILE = OUTPUT_DIR / "resultado.pdf"

DEFAULT_SHEET_NAME: str | int = 0

EXPECTED_COLUMNS = [
    "equipamento",
    "tipo_falha",
    "data_falha",
    "data_manutencao",
    "tempo_parada_horas",
    "custo_manutencao",
    "status",
    "prioridade",
    "descricao",
]

OPTIONAL_INPUT_COLUMNS = [
    "id",
]

REQUIRED_COLUMNS = [
    "equipamento",
    "tipo_falha",
    "data_falha",
    "data_manutencao",
    "tempo_parada_horas",
    "custo_manutencao",
    "status",
    "prioridade",
]

STATUS_ALLOWED = {"Aberta", "Em andamento", "Concluída"}
PRIORIDADE_ALLOWED = {"Baixa", "Média", "Alta"}

STATUS_NORMALIZATION_MAP = {
    "aberta": "Aberta",
    "aberto": "Aberta",
    "em andamento": "Em andamento",
    "andamento": "Em andamento",
    "em_andamento": "Em andamento",
    "concluida": "Concluída",
    "concluída": "Concluída",
    "concluido": "Concluída",
    "concluído": "Concluída",
}

PRIORIDADE_NORMALIZATION_MAP = {
    "baixa": "Baixa",
    "media": "Média",
    "média": "Média",
    "alta": "Alta",
}

NUMERIC_MIN_RULES = {
    "tempo_parada_horas": 0.0,
    "custo_manutencao": 0.0,
}

TOP_FAILURE_TYPES_N = 10
