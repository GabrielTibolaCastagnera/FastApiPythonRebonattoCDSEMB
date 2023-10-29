from pydantic import BaseModel
from pydantic import Field
from atualizar_estufa_model import AtualizarEstufaModel
class EstufaModel(BaseModel):
    id: int = Field(description= "Código da Estufa")
    nome: str = Field(description= "Nome da Estufa")
    humidadeDoAr: float = Field(description= "Umidade do Ar (%)")
    humidadeDoSolo: float = Field(description= "Umidade do Solo (%)")
    qtdDeMudas: int = Field(description="Quantidade de Mudas")
    luminosidade: int = Field(description= "Luminosidade(lm/m2)")
    def copyWith(self, estufa: AtualizarEstufaModel):
        return EstufaModel(
            id= self.id,
            humidadeDoAr= estufa.humidadeDoAr or self.humidadeDoAr,
            humidadeDoSolo= estufa.humidadeDoSolo or self.humidadeDoSolo,
            luminosidade= estufa.luminosidade or self.luminosidade,
            nome= estufa.nome or self.nome,
            qtdDeMudas= estufa.qtdDeMudas or self.qtdDeMudas,
            )
