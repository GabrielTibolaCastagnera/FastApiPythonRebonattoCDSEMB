from fastapi import FastAPI

app = FastAPI()

@app.get("/semtipo/")
async def semtipo(arg1):
    return {"resultado": "Veio " + arg1}

@app.get("/soma/")
async def soma(valor1: int, valor2: int):
    return {"resultado": valor1+valor2}

@app.get("/somadefault/")
async def somadef(valor1: int = 0, valor2: int = 10):
    return {"resultado": valor1+valor2} 