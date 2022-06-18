from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional, Union
from pydantic import BaseModel
from uuid import uuid4
from erros import Item, Message, error404, sucessoDelete, sucessoCadastro, cepErro, compradorNaoCadastrado, quantidadeDeProdutosInvalida, vendedorNaoCadastrado, produtoNaoLocalizado, sucessoVenda
import json
import requests

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
    id: Optional[str];
    nome: str
    cep: str
    logradouro: Optional[str] = "GERADO AUTOMATICAMENTE"
    bairro: Optional[str] = "GERADO AUTOMATICAMENTE"
    cidade: Optional[str] = "GERADO AUTOMATICAMENTE"
    email: str
    idade: str
    cpf: str


armazenamento: list[Cadastro] = []

class Venda(BaseModel):
    id: Optional[str] = "Gerado Automaticamente"
    nomeComprador: Optional[str] = "Gerado pelo CPF"
    cpfComprador: str
    idVendedor: str
    vendedor: Optional[str] = "Gerado pelo ID"
    idProduto: str
    produto: Optional[str] = "Gerado pelo ID"
    quantidade: int
    precoUnidade: Optional[str] = "Gerado pelo ID"
    precoTotal: Optional[str] = "Gerado Automaticamente"


armazenamentoVendas: list[Venda] = []


@app.get('/clientes', response_model=list)
def listar_clientes():
    return armazenamento


@app.get('/clientes/{cliente_id}', response_model=Cadastro, responses={404: {"model": Message}})
def obter_cliente(cliente_id: str):
    for cliente in armazenamento:
        if cliente.id == cliente_id:
            return cliente
    else:
       return error404


@app.delete('/clientes/{cliente_id}', response_model=Message, responses={404: {"model": Message}})
def deletar_cliente(cliente_id: str):
    posicao = -1
    for index, cliente in enumerate(armazenamento):
        if cliente.id == cliente_id:
            posicao = index
            break

    if posicao != -1:
        armazenamento.pop(posicao)
        return sucessoDelete
    return error404


@app.post('/cadastrar')
def cadastrar_cliente(cliente: Cadastro):
    cliente.id = str(uuid4())

    pegandoCep = requests.get("https://viacep.com.br/ws/{}/json/".format(cliente.cep))
    pegandoCep = pegandoCep.json()

    if "erro" in pegandoCep:
        return cepErro

    cliente.logradouro = format(pegandoCep['logradouro'])
    cliente.bairro = format(pegandoCep['bairro'])
    cliente.cidade = format(pegandoCep['localidade'])

    armazenamento.append(cliente)
    return sucessoCadastro


@app.get('/venda')
def listar_vendas():
    return armazenamentoVendas


@app.post('/venda', responses={404: {"model": Message}})
def adicionar_venda(dadosVenda: Venda):

    if (dadosVenda.quantidade == 0): # VERIFICA SE A QUANTIDADE É IGUAL A 0
        return quantidadeDeProdutosInvalida # RETORNA ERROR 404 INFORMANDO

    #VERIFICA SE O USUARIO ESTA CADASTRADO
    for cliente in armazenamento:
        if cliente.cpf == dadosVenda.cpfComprador:
           dadosVenda.nomeComprador = format(cliente.nome) # CASO EXISTA PEGA O NOME DO COMPRADOR
           break
    else:
        return compradorNaoCadastrado # RETORNA ERROR 404 FALANDO Q COMPRADO NÃO ESTA CADASTRADO


    # CONSUMINDO A API DE VENDORES
    pegandoVendedor = requests.get("https://afternoon-fortress-37984.herokuapp.com/api/vendedores/{}".format(dadosVenda.idVendedor))
    # VERIFICA SE O VENDEDOR ESTA CADASTRADO    
    verificarVendor = pegandoVendedor.json()
    verificarVendor = format(verificarVendor["data"])
    if str(verificarVendor) == "None":
        return vendedorNaoCadastrado # RETORNA ERROR 404 VENDOR NÃO LOCALIZADO
    
    pegandoVendedor = pegandoVendedor.json()
    dadosVenda.vendedor = format(pegandoVendedor["data"]["attributes"]["nome"])



    pegarProduto = requests.get("https://afternoon-fortress-37984.herokuapp.com/api/produtos/{}".format(dadosVenda.idProduto))
    pegarProduto = pegarProduto.json()
    produtoValidador = format(pegarProduto["data"])
    if str(produtoValidador) == "None":
        return produtoNaoLocalizado # RETORNA ERROR 404 VENDOR NÃO LOCALIZADO
    dadosVenda.produto = format(pegarProduto["data"]["attributes"]["produto"])
    dadosVenda.precoUnidade = format(pegarProduto["data"]["attributes"]["preco"])
    dadosVenda.precoTotal = format(int(pegarProduto["data"]["attributes"]["preco"]) * int(dadosVenda.quantidade))




    dadosVenda.id = str(uuid4())
    armazenamentoVendas.append(dadosVenda)
    return sucessoVenda
