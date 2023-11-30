from estufa_model import EstufaModel
from exception_model import EqualIdExceptionModel, NotFoundExceptionModel
from atualizar_estufa_model import AtualizarEstufaModel
import sys
from pymongo import MongoClient

# Informações de conexão
host = ''
porta = ''
usuario = ''
senha = ''
banco_de_dados = ''

# Criando a string de conexão
string_conexao = "mongodb://:@:/"



try:

    # Conectando ao MongoDB
    cliente = MongoClient(string_conexao)

    # Selecionando o banco de dados
    db = cliente[banco_de_dados]
    estufas = db['estufas']
except Exception as e:
    print(e)
    sys.exit(1)

def criarNovaEstufa(novaEstufa: EstufaModel):
    try:
        print(db.list_collection_names())
        exists = estufas.find_one({'id': novaEstufa.id})
        if(exists == None):
           estufas.insert_one(novaEstufa.dict())
        else:
            raise EqualIdExceptionModel
    except Exception as e:
        raise EqualIdExceptionModel

def updateStove(stove: AtualizarEstufaModel):
    try:
        exists = estufas.find_one({'id': stove.id})
        print(exists)
        if(exists != None):
            update = {}
            if(stove.nome):
                update['nome'] = stove.nome
            if(stove.humidadeDoAr):
                update['humidadeDoAr'] = stove.humidadeDoAr
            if(stove.humidadeDoSolo):
                update['humidadeDoSolo'] = stove.humidadeDoSolo
            if(stove.qtdDeMudas):
                update['qtdDeMudas'] = stove.qtdDeMudas
            if(stove.luminosidade):
                update['luminosidade'] = stove.luminosidade

            estufas.update_one({'id': stove.id}, {'$set': update})
        else:
            raise NotFoundExceptionModel

    except Exception as e:
        print(e)
        raise NotFoundExceptionModel
    


def search_list(id: None | int):
    result = {}
    if id is None:
        result = estufas.find()
    else:
        result = estufas.find({'id': id})
    list = []
    for res in result:
        
        list.append(EstufaModel(humidadeDoAr=res['humidadeDoAr'], humidadeDoSolo=res['humidadeDoSolo'],
                    id=res['id'], luminosidade=res['luminosidade'], nome=res['nome'], qtdDeMudas=res['qtdDeMudas']))
    if (len(list) == 0):
        raise NotFoundExceptionModel
    return list


def delete_estufa(estufa_id: int):

    try:
        result = estufas.find_one({'id': estufa_id})
        print(result)
        if result == None:
            raise NotFoundExceptionModel
        estufas.delete_one({'id': estufa_id})
        return estufa_id
    except:
        raise NotFoundExceptionModel
