from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
from uuid import uuid4
import json
import requests


class Item(BaseModel):
    id: str
    value: str


class Message(BaseModel):
    status: int
    message: str


error404 = JSONResponse(status_code=404, content={"status": 404, "message": "Item não encontrado"})

sucessoDelete = JSONResponse(status_code=200, content={"status": 200, "message": "O cliente foi removido com sucesso!"})

sucessoCadastro = JSONResponse(status_code=200, content={"status": 200, "message": "O cliente foi cadastrado com sucesso!"})

cepErro = JSONResponse(status_code=404, content={"status": 404, "message": "Cep Invalido"})

compradorNaoCadastrado = JSONResponse(status_code=404, content={"status": 404, "message": "cpf não cadastrado"})

quantidadeDeProdutosInvalida = JSONResponse(status_code=404, content={"status": 404, "message": "Você não pode adicionar 0 produtos"})

vendedorNaoCadastrado = JSONResponse(status_code=404, content={"status": 404, "message": "Vendedor não localizado"})

produtoNaoLocalizado = JSONResponse(status_code=404, content={"status": 404, "message": "Produto não localizado"})

sucessoVenda = JSONResponse(status_code=200, content={"status": 200, "message": "A venda foi realizada com sucesso!"})




 