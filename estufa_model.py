from pydantic import BaseModel
from pydantic import Field

class EstufaModel(BaseModel):
    id: int = Field(description= "Código da Estufa")
    nome: str = Field(description= "Nome da Estufa")
    humidadeDoAr: float = Field(description= "Umidade do Ar (%)")
    humidadeDoSolo: float = Field(description= "Umidade do Solo (%)")
    qtdDeMudas: int = Field(description="Quantidade de Mudas")
    luminosidade: int = Field(description= "Luminosidade(lm/m2)")
