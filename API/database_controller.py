from multiprocessing import get_all_start_methods
from pkgutil import get_data
from estufa_model import EstufaModel
from possue_id_igual import possueIdIgual
from exception_model import EqualIdExceptionModel, NotFoundExceptionModel
from atualizar_estufa_model import AtualizarEstufaModel
from indexOf import indexOf
import mariadb
import sys
# Print List of Contacts
def print_contacts(cur):
     print("OLA!")
     """Retrieves the list of contacts from the database and prints to stdout"""

     # Initialize Variables
     contacts = []

     # Retrieve Contacts
     cur.execute("SELECT * FROM ESTUFAS")

     # Prepare Contacts
     for (id, nome, hum, humS, mudas, lum) in cur:
        print(f"{nome}: {hum}")

     # List Contacts
     print("\n".join(contacts))
try:
   conn = mariadb.connect(
      user="183929",
      password="183929",
      host="10.0.235.199",
      port=3306,
      database = "183929"
   )
   cur = conn.cursor()
   #print_contacts(cur)
   # Close Connection
   conn.close()
except mariadb.Error as e:
   print(f"Error conecting to MariaDB Platform: {e}")
   sys.exit(1)
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

def updateStove(stove: AtualizarEstufaModel):
   indexOfStove = indexOf(db, stove.id)
   if(indexOfStove is None):
      raise NotFoundExceptionModel
   db[indexOfStove] = db[indexOfStove].copyWith(stove)

def search_list(id: None | int):
  if id is None:
    return db
  for stove in db:
    if(stove.id == id):
        return [stove]
  raise NotFoundExceptionModel

def delete_estufa(estufa_id: int):
    estufa_index = indexOf(db, estufa_id)
    if estufa_index is not None:
        deleteEstufa = db.pop(estufa_index)
        return deleteEstufa
    raise NotFoundExceptionModel
