from fastapi import FastAPI
from database_controller import criarNovaEstufa
from estufa_model import EstufaModel
from resposta_criar_nova_estufa import RespostaCriarNovaEstufa
from fastapi.exceptions import HTTPException
from exception_model import EqualIdExceptionModel, ExceptionModel
app = FastAPI()

@app.post("/criarNovaEstufa/")
async def criarNovaEstufaDef(novaEstufa: EstufaModel):
    try:
        criarNovaEstufa(novaEstufa=novaEstufa)
        return RespostaCriarNovaEstufa(codigo='criado', mensagem='Sua estufa ' + novaEstufa.nome + ' criada')
    except EqualIdExceptionModel:
        return HTTPException(status_code=400, detail= ExceptionModel(codigo='equalStoveId', menssagem='Id Existente'))
    
@app.get("/consultarEstufa/")
async def get_estufa(id: int):
    try:
         return get_estufa(id)
    except KeyError:
        raise HTTPException(status_code=404, detail=ExceptionModel(codigo='estufaNaoEncontrada', menssagem='Estufa não encontrada.'))
