# Engenharia de Computação - UPF
# Gabriel Tibola Castagnera 

from fastapi import FastAPI
from database_controller import criarNovaEstufa, search_list, updateStove, delete_estufa
from estufa_model import EstufaModel
from resposta_criar_nova_estufa import RespostaSucessoEstufa
from fastapi.responses import JSONResponse
from exception_model import EqualIdExceptionModel, ExceptionModel, NotFoundExceptionModel
from atualizar_estufa_model import AtualizarEstufaModel
app = FastAPI()


@app.post("/criarNovaEstufa")
async def criarNovaEstufaDef(novaEstufa: EstufaModel):
    try:
        criarNovaEstufa(novaEstufa=novaEstufa)
        return RespostaSucessoEstufa(codigo='criado', mensagem='Sua estufa ' + novaEstufa.nome + ' foi criada')
    except EqualIdExceptionModel:
        erro = JSONResponse(status_code=400, content=ExceptionModel(
            codigo='equalStoveId', menssagem='Id Existente').to_dict())
        return erro


@app.get("/consultarEstufa")
async def get_estufa(id: int = None):
    try:
        return {'result': search_list(id)}
    except NotFoundExceptionModel:
        return JSONResponse(status_code=404, content=ExceptionModel(codigo='estufaNaoEncontrada', menssagem='Estufa não encontrada.').to_dict())


@app.put("/atualizarEstufa")
async def update_estufa(atualizarEstufa: AtualizarEstufaModel):
    try:
        updateStove(atualizarEstufa)
        return RespostaSucessoEstufa(codigo='atualizado', mensagem='Sua estufa com ID ' + str(atualizarEstufa.id) + ' foi atualizada')

    except NotFoundExceptionModel:
        return JSONResponse(status_code=404, content=ExceptionModel(codigo='estufaNaoEncontrada', menssagem='Estufa não encontrada.').to_dict())


@app.patch("/excluirEstufa")
@app.delete("/excluirEstufa")
async def deleteEstufa(estufa_id: int):
    try:
        deletedEstufa = delete_estufa(estufa_id)
        return {"message": f"Estufa com ID {deletedEstufa} excluída com sucesso"}
    except NotFoundExceptionModel:
        return JSONResponse(status_code=404, content=ExceptionModel(codigo='estufaNaoEncontrada', menssagem='Estufa não encontrada.').to_dict())