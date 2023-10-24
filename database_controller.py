from multiprocessing import get_all_start_methods
from pkgutil import get_data
from estufa_model import EstufaModel
from possue_id_igual import possueIdIgual
from exception_model import EqualIdExceptionModel
db = []

def criarNovaEstufa(novaEstufa: EstufaModel):
    if(possueIdIgual(db, novaEstufa)):
        raise EqualIdExceptionModel
    db.append(novaEstufa)

def get_list(id=None):

  if id is not None:
    try:
      return [get_data(id)]
    except KeyError:
      raise ValueError("ID não encontrado.")
  else:
    return [get_data(id) for id in get_all_start_methods()]


