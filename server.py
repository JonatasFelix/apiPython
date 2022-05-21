from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5500",
    "http://127.0.0.1:5500",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Cadastro(BaseModel):
    id: Optional[str]
    nome: str
    sobrenome: str
    email: str
    fone: int
    estado: str
    cidade: str


armazenamento: list[Cadastro] = []


@app.get('/clientes')
def listar_clientes():
    return armazenamento


@app.get('/clientes/{cliente_id}')
def obter_cliente(cliente_id: str):
    for cliente in armazenamento:
        if cliente.id == cliente_id:
            return cliente
    else:
        return {'status': '404', 'error': 'Cliente_id não localizado'}


@app.delete('/clientes/{cliente_id}')
def deletar_cliente(cliente_id: str):
    posicao = -1
    for index, cliente in enumerate(armazenamento):
        if cliente.id == cliente_id:
            posicao = index
            break

    if posicao != -1:
        armazenamento.pop(posicao)
        return {'mensagem': 'O cliente foi removido com sucesso!'}
    else:
        return {'error': 'Cliente_id não localizado!'}


@app.post('/cadastrar')
def cadastrar_cliente(cliente: Cadastro):
    cliente.id = str(uuid4())
    armazenamento.append(cliente)
    return {'mensagem': f'Olá {cliente.nome}, seu cadastro foi efetuado com sucesso!'}
