from sqlite3 import Date, IntegrityError
from config import get_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL
from sqlalchemy import Column, String, Integer, Boolean, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL
from sqlalchemy import Column, String, Integer, Boolean, Float, DateTime, ForeignKey, join, select, insert, update
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

#datawharehousing Tables
Base = declarative_base()
Session = sessionmaker(bind=get_engine())
session = Session()


#Tabelas Dimensão

class Dim_Tempo(Base):
    __tablename__ = "Dim_Tempo"
    Id_Tempo = Column(Integer, primary_key=True)
    Cod_Dia = Column(String)
    DatadIA = Column(Date)
    Cod_Semana = Column(Integer)
    Nome_Dia_Semana = Column(String)
    Codigo_Mes = Column(Integer)
    Nome_Mes = Column(String)
    Cod_Mes_Ano = Column(String)
    Nome_Mes_Ano = Column(String)
    Cod_Trimestre = Column(Integer)
    Nome_Trimestre = Column(String)
    Cod_Trimestre_Ano = Column(String)
    Nome_Trimeste_Ano = Column(String)
    Cod_Semestre = Column(Integer)
    Nome_Semestre = Column(String)
    Cod_Semestre_Ano = Column(String)
    Nome_Semestre_Ano = Column(String)
    Ano = Column(String)
    BitSemana = Column(Boolean)
 


class Dim_Marca(Base):
    __tablename__ = "Dim_Tempo"
    Id_Marca = Column(Integer, primary_key=True)
    Cod_Marca = Column(Integer)
    Desc_Marca = Column(String)
    Marca = Column(String)
    PrazoMarca = Column(Integer)
    BitAtivo = Column(Boolean)


class Dim_Produto(Base):
    __tablename__ = "Dim_Produto"
    Id_produto = Column(Integer, primary_key=True)
    Cod_Produto = Column(String)
    Cod_Marca = Column(String)
	NomeProduto = Column(String)
	Marca = Column(String)


class Dim_Categoria(Base):
    __tablename__ = "Dim_Categoria"
    Id_Categoria = Column(Integer, primary_key=True)
    Cod_Categoria = Column(Integer)
    Nome_Categoria = Column(String)
	

class Dim_Cliente(Base):
    __tablename__ = "Dim_Cliente"
    Id_Cliente = Column(Integer, primary_key=True)
	cod_cliente = Column(Integer)
    Desc_Cliente = Column(String)
    Cod_Cidade = Column(Integer),
    Desc_Cidade = Column(String)
    Cod_Estado = Column(Integer),
    Cod_Regiao = Column(Integer),
    Desc_Regiao = Column(String)
    Cod_Segmento = Column(Integer),
    Desc_Segmento = Column(String)
    BitAtivo = Column(Boolean)
    

class Dim_Fabrica(Base):
    __tablename__ = "Dim_Fabrica"
    Id_Fabrica = Column(Integer, primary_key=True)
    Desc_Fabrica = Column(String)
    Marca = Column(String)
    BitAtivo = Column(Boolean)
  

class Dim_Frete(Base):
    __tablename__ = "Dim_Frete"
    Id_Frete = Column(Integer, primary_key=True)
    CodFrete = Column(Integer)
    uf = Column(String)
    estado = Column(String)
    cidade = Column(String)
    valor = Column(Float)
    peso = Column(Float)
    data_frete = Column(Date)
    hora_frete = Column(String)
    cep = Column(String)
    transportadora = Column(String)



class Dim_Estoque(Base):
    __tablename__ = "Dim_Estoque"
    Id_Estoque = Column(Integer, primary_key = True)
    Cod_Estoque = Column(Integer)
    Desc_Estoque = Column(String)
    Quantidade = Column(Float)
    Data_Alteracao = Column(Date),
    Cod_Produto = Column(Integer)


class Dim_Cidade(Base):
    __tablename__ = "Dim_Cidade"
    Id_Cidade   = Column(Integer, primary_key = True)
    Cod_Cidade = Column(Integer)
    Desc_Cidade = Column(String)
    Uf_Cidade = Column(String)

class Dim_Loja(Base):
    __tablename__ = "Dim_Loja"
    Id_Loja = Column(Integer, primary_key = True)
    Cod_Loja = Column(Integer)
    Desc_Loja = Column(String)





#Tabelas Fato

class Fato_Pedido(Base):
    __tablename__ = "Fato_Pedido"
	Id_FatoPedido = Column(Integer, primary_key = True)
	Cod_CodCliente = Column(Integer)
	Cod_Marca = Column(Integer)
	Cod_produto = Column(Integer)
	SKU = Column(String)
	Cod_Barras = Column(String)
	dataVenda = Column(Date)
	horaVenda = Column(String)
	EstoqueProdutVenda = Column(Float)
	NomeProduto = Column(String)
	Marca = Column(String)
	Preco = Column(Float)
	Custo = Column(Float)
	Frete = Column(Float)
	Margem = Column(Float)
	Pagamento = Column(String)
	Loja = Column(String)
	Prazo = Column(Float)
	Quantidade = Column(Float)
    Id_Frete = Column(Integer, ForeignKey("Dim_Frete.Id_Frete"))
    Id_Marca = Column(Integer, ForeignKey("Dim_Marca.Id_Marca"))
    Id_Loja = Column(Integer, ForeignKey("Dim_Loja.Id_Loja"))
    Id_Cliente = Column(Integer, ForeignKey("Dim_Cliente.Id_Cliente"))
    Id_produto = Column(Integer, ForeignKey("Dim_Produto.Id_produto"))
    Id_Fabrica = Column(Integer, ForeignKey("Dim_Fabrica.Id_Fabrica"))
    Id_Categoria = Column(Integer, ForeignKey("Dim_Categoria.Id_Categoria"))
    Id_Estoque = Column(Integer, ForeignKey("Dim_Estoque.Id_Estoque"))
    Id_Cidade = Column(Integer, ForeignKey("Dim_Cidade.Id_Cidade"))
    Id_Tempo = Column(Integer, ForeignKey("Dim_Tempo.Id_Tempo"))


class Fato_Frete(Base):
    __tablename__ = "Fato_Frete"
    Id_FatoFrete = Column(Integer, primary_key=True)
    Frete = Column(Float)
	Quantidade = Column(Float)
	Peso = Column(Float)
	Destino = Column(String)
	UF = Column(String)
    Cod_Dia = Column(String)
    Id_Cliente =  Column(Integer, ForeignKey("Dim_Cliente.Id_Cliente"))
    Id_produto = Column(Integer, ForeignKey("Dim_Produto.Id_produto"))
    Id_Org = Column(Integer, ForeignKey("Dim_Organizacional.Id_Org"))
    Id_Tempo = Column(Integer, ForeignKey("Dim_Tempo.Id_Tempo"))
    Id_Frete = Column(Integer, ForeignKey("Dim_Frete.Id_Frete"))


class Fato_Faturamento(Base):
    __tablename__ = "Fato_Faturamento"
    IdFaturamento = Column(Integer, primary_key = True)
    Faturamento = Column(Float)
    Imposto = Column(Float)
    Custo_Variavel = Column(Float)
    Quantidade_Vendida = Column(Float)
    Unidades_Vendidas = Column(Float)
    Id_Tempo = Column(Integer, ForeignKey("Dim_Tempo.Id_Tempo"))
    Id_Fabrica = Column(Integer, ForeignKey("Dim_Fabrica.Id_Fabrica"))
    Id_produto = Column(Integer, ForeignKey("Dim_Produto.Id_produto"))
    Id_Cliente = Column(Integer, ForeignKey("Dim_Cliente.Id_Cliente"))



class Fato_Custos(Base):
    __tablename__ = "Dim_Estoque"
    Id_FatoCustos = Column(Integer, primary_key = True)
    CustoFornecedor = Column(Float)
	CustoFrete  = Column(Float)
    Id_FatoCustos = Column(Integer, ForeignKey("Dim_Produto.Id_FatoCustos"))
    Id_Fabrica = Column(Integer, ForeignKey("Dim_Fabrica.Id_Fabrica"))
    Id_Tempo = Column(Integer, ForeignKey("Dim_Tempo.Id_Tempo"))
    Id_Cliente = Column(Integer, ForeignKey("Dim_Cliente.Id_Cliente"))
    