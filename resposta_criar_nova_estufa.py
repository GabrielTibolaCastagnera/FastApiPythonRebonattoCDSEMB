from pydantic import BaseModel
from pydantic import Field

class RespostaCriarNovaEstufa(BaseModel):
    mensagem: str = Field(description='Mensagem de Sucesso')
    codigo: str = Field(description='Código de Sucesso')