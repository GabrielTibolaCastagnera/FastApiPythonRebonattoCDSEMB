from pydantic import BaseModel
from pydantic import Field

class EqualIdExceptionModel(Exception):
    'Erro ao criar a estufa: id existente'
    pass

class ExceptionModel(BaseModel):
    codigo: str = Field('Código de Erro')
    menssagem: str = Field('Mensagem de Erro')