from pydantic import BaseModel
from pydantic import Field

class AtualizarEstufaModel(BaseModel):
    id: int = Field(description= "Código da Estufa")
    nome: str | None = None
    humidadeDoAr: float | None= None
    humidadeDoSolo: float | None = None
    qtdDeMudas: int | None = None
    luminosidade: float | None= None

   
