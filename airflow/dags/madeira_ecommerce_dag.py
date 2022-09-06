import lxml.html as parser
import requests
import csv
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow import models
from airflow.models.baseoperator import chain
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options



def scroll():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

def madeira():
    driver = webdriver.Chrome(ChromeDriverManager().install())

    urls_produto = []
    dict_produtos = {}
    items = []
    lista_dicts = []


    data = pd.read_excel("urlmadeira.xlsx")
    for i, row in data.iterrows():
        driver.get(row[0])
        time.sleep(1)

        dict_produtos = {}
        scroll()
            
        dict_produtos['PaginaProduto'] = row[0]
        dict_produtos['Loja'] = 'MadeiraMadeira'
        dict_produtos['Marca'] = 'Tarkett'
        dict_produtos['EAN'] = 'naoinformado'

        try:
            nome_produto = driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div[2]/div/div[2]/h1')[0].text
            dict_produtos['NomeProduto'] = nome_produto
            
        except:
            print("Nome nao encontrado")

        try:
            categorias = driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[1]/div/a')
            categoriasurl = driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[1]/div/a')
            cont = 0
            for categoria in categorias:
                dict_produtos[categoria.text] = categoriasurl[cont].get_attribute('href')
                cont+=1
                    
        except:
            print("error categoria")
            
        try:
            seller_vendendo = driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div[2]/div/div[2]/p/a')[0].text
            dict_produtos['SellerVendendo'] = seller_vendendo
        except:
            print("erro Seller")
            
        try:
            preco = driver.find_elements_by_xpath(
                    '//*[@id="__next"]/div/main/div[2]/div[2]/div[2]/div/div[2]/div[4]/div/div[2]/span')[0].text
            dict_produtos['PRECO'] = preco
        except:
            print("Error")

        try:
            opcoes_cores = driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div[2]/div/div[2]/div[3]/div/div[2]/div/span')
            cont = 0
            for opcoes in opcoes_cores:
                dict_produtos["cores"+str(cont)] = opcoes.text
                cont+=1
        except:
            print("erro cores")

        try:
            metro = driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div[2]/div/div[2]/div[6]/div/div/div/div[1]/input')[0]
            metro = metro.get_attribute('value')
            dict_produtos['MetroProduto'] = metro
        except:
            print("error metro")

        try:
            observacoes = driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div[1]/div[2]/div/div/p[1]')
            for obs in observacoes:
                dict_produtos['Observacoes'] = obs.text
        except:
            print("error")

        try:
            imagens = driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div[1]/div[1]/div/div[1]/div[2]/ul/li/a/div/img')
            imagcont = 0
            for imagem in imagens:
                dict_produtos['IMAGEM'+str(imagcont)] = imagem.get_attribute("src").replace("width=256","width=600")
                imagcont+=1
        except:
            print("error imagem")

        try:
            descricao = driver.find_elements_by_xpath('//*[@id="radix-id-0-158-content-product_information"]/div/div/div[1]/div[3]/div')
            for descri in descricao:
                dict_produtos['DescricaoProduto'] = descri.text
        except:
            print('error')

        lista_referencia = []
        lista_valor = []
        referencia_atributo = driver.find_elements_by_xpath(
                    '//*[@id="radix-id-0-158-content-product_information"]/div/div/div/div/div/table/tbody/tr/td[1]')
        for valor in referencia_atributo:
            lista_referencia.append(valor.get_attribute('textContent'))

        valor_atributo = driver.find_elements_by_xpath(
                    '//*[@id="radix-id-0-158-content-product_information"]/div/div/div/div/div/table/tbody/tr/td[2]')

        for valor in valor_atributo:

            lista_valor.append(valor.get_attribute('textContent'))

        for keys, values in zip_longest(lista_referencia, lista_valor):
            dict_produtos[keys] = values

        print(dict_produtos)
        lista_dicts.append(dict_produtos)

    datamadeira = pd.DataFrame(lista_dicts)
    datamadeira.to_excel("infosmadeira.xlsx")



default_args = {
  'start_date': datetime(2022,8,31),
  'sla': timedelta(minutes=50)
}
    
with DAG('madeira_prices',  default_args=default_args,
   catchup=False) as dag:

    madeira = PythonOperator(
        task_id = 'madeira',
        python_callable = madeira
    )

madeira


