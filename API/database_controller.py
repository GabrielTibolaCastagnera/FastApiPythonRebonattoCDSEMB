from multiprocessing import get_all_start_methods
from pkgutil import get_data
from estufa_model import EstufaModel
from possue_id_igual import possueIdIgual
from exception_model import EqualIdExceptionModel, NotFoundExceptionModel
from atualizar_estufa_model import AtualizarEstufaModel
from indexOf import indexOf
import mariadb
import sys

cur: mariadb.Cursor

try:
    conn = mariadb.connect(
        user="183929",
        password="183929",
        host="177.67.253.69",
        port=53306,
        database="183929"
    )
    cur = conn.cursor()
except mariadb.Error as e:
    print(f"Error conecting to MariaDB Platform: {e}")
    sys.exit(1)


def criarNovaEstufa(novaEstufa: EstufaModel):
    try:
        cur.execute(
            f"INSERT INTO `ESTUFAS`(`id`, `nome`, `humidadeDoAr`, `humidadeDoSolo`, `qtdDeMudas`, `luminosidade`) VALUES ({str(novaEstufa.id)}, '{str(novaEstufa.nome)}', {str(novaEstufa.humidadeDoAr)}, {str(novaEstufa.humidadeDoSolo)}, {str(novaEstufa.qtdDeMudas)}, {str(novaEstufa.luminosidade)})")
        conn.commit()
    except mariadb.Error as e:
        print(e)
        raise EqualIdExceptionModel

def updateStove(stove: AtualizarEstufaModel):
    try:
        cur.execute("SELECT id FROM ESTUFAS WHERE id = " + str(stove.id))
        count = 0
        for (id) in cur:
            count += 1
        if count == 0:
            raise NotFoundExceptionModel
        hasUpdate = False
        update = "UPDATE ESTUFAS SET "
        if not (stove.humidadeDoAr is None):
            hasUpdate = True
            update += "humidadeDoAr = " + str(stove.humidadeDoAr) + ", "
        if not (stove.humidadeDoSolo is None):
            hasUpdate = True
            update += "humidadeDoSolo = " + str(stove.humidadeDoSolo) + ", "
        if not (stove.luminosidade is None):
            hasUpdate = True
            update += "luminosidade = " + str(stove.luminosidade) + ", "
        if not (stove.nome is None):
            hasUpdate = True
            update += "nome = '" + stove.nome + "', "
        if not (stove.qtdDeMudas is None):
            hasUpdate = True
            update += "qtdDeMudas = " + str(stove.qtdDeMudas) + ", "
        if (hasUpdate):
            update = update[:-1]
            update = update[:-1]
            update += " WHERE id = " + str(stove.id)
            print(update)
            cur.execute(update)
        else:
            raise NotFoundExceptionModel

    except mariadb.Error as e:
        print(e)
        raise NotFoundExceptionModel
    


def search_list(id: None | int):
    if id is None:
        cur.execute("SELECT * FROM ESTUFAS")
    else:
        cur.execute("SELECT * FROM ESTUFAS WHERE id = " + str(id))
    list = []
    for (id, nome, hum, humS, mudas, lum) in cur:
        list.append(EstufaModel(humidadeDoAr=hum, humidadeDoSolo=humS,
                    id=id, luminosidade=lum, nome=nome, qtdDeMudas=mudas))
    if (len(list) == 0):
        raise NotFoundExceptionModel
    return list


def delete_estufa(estufa_id: int):

    try:
        cur.execute("SELECT id FROM ESTUFAS WHERE id = " + str(estufa_id))
        count = 0
        for (id) in cur:
            count += 1
        if count == 0:
            raise NotFoundExceptionModel
        cur.execute("DELETE FROM ESTUFAS WHERE id = " + str(estufa_id))
        return estufa_id
    except:
        raise NotFoundExceptionModel
