from estufa_model import EstufaModel
from possue_id_igual import possueIdIgual
from exception_model import EqualIdExceptionModel
db = []

def criarNovaEstufa(novaEstufa: EstufaModel):
    if(possueIdIgual(db, novaEstufa)):
        raise EqualIdExceptionModel
    db.append(novaEstufa)



