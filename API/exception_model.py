from pydantic import BaseModel
from pydantic import Field

class EqualIdExceptionModel(Exception):
    'Erro ao criar a estufa: id existente'
    pass

class NotFoundExceptionModel(Exception):
    'Não encontrado'
    pass
class ExceptionModel(BaseModel):
    codigo: str = Field('Código de Erro')
    menssagem: str = Field('Mensagem de Erro')
    def to_dict(self):
        return {
            'codigo': self.codigo,
            'menssagem': self.menssagem
        }