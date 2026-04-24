from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class MaintenanceRecord:
    equipamento: str
    tipo_falha: str
    data_falha: datetime
    data_manutencao: datetime
    tempo_parada_horas: float
    custo_manutencao: float
    status: str
    prioridade: str
    descricao: str | None = None
