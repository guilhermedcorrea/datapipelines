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
import lxml.html as parser
import requests
import csv
import time
import re
import json
from urllib.parse import urlsplit, urljoin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
from random import randint
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import lxml.html as parser
import requests
import csv
import time
import re
import json
from urllib.parse import urlsplit, urljoin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
from random import randint
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


class Google:
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    def __init__(self):
        self.dict = {}
        self.lista_dicts = []

    def scroll(self):

        lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True

    def get_urls(self):
        lista_dicts = []
        data = pd.read_excel("googleshopping.xlsx")
        for i, row in data.iterrows():
            ean = row[0]
            url_google = row[1]
           
            dict_items = {}
            dict_items['EAN'] = ean
            dict_items['URLGOOGLE'] = url_google
            lista_dicts.append(dict_items)
        
        return lista_dicts

    def get_precos(self):
        lista_dicts = []
        dicts = self.get_urls()
        for dict in dicts:
            time.sleep(1)
            
            self.driver.get(dict['URLGOOGLE'])
            self.scroll()
            name_sellers = []
            urls = []
            items = []
            prices_sellers = []
            eanferencia = []
            perfil_url = []
            try:
                names = self.driver.find_elements_by_xpath('//*[@id="sh-osd__online-sellers-cont"]/tr/td[1]/div[1]/a')
                for name in names:
                    nam = name.text.strip()
                    name_sellers.append(nam)
                    urls.append(dict['URLGOOGLE'])
                    eanferencia.append(dict['EAN'])
                   
            except:
                print("Error")
            
            try:
                prices = self.driver.find_elements_by_xpath('//*[@id="sh-osd__online-sellers-cont"]/tr/td[4]/div/div[1]')
                for pric in prices:
                    price = pric.text.replace("R$","").replace(".","").replace(",",".").strip()
                    prices_sellers.append(price)
            except:
                prices_sellers.append(price).append("preçonaoencontrado")

            try:
                perfil_seller = self.driver.find_elements_by_xpath('//*[@id="sh-osd__online-sellers-cont"]/tr/td[5]/div/a')
                for perfil in perfil_seller:
                    perfil = perfil.get_attribute('href')
                    perfil_url.append(perfil)
            except:
                perfil_url.append(dict['URLGOOGLE'])

            name_se = [i for i in name_sellers if i != '']
            

            for i, num in enumerate(name_se):
                desc={}

                try:
                    desc['Sellers']=name_se[i]
                except:
                    desc['Sellers']='valornaoencontrado'
             
                try:
                    desc['Prices']=prices_sellers[i]
                except:
                    desc['Prices']='valornaoencontrado'
                try:
                    desc['Urls']=urls[i]
                except:
                    desc['Urls'] = 'valornaoencontrado'

                try:
                    desc["EanReferencia"] = eanferencia[i]
                except:
                    desc["EanReferencia"] = 'valor'

                try:
                    desc['perfilseller']=perfil_url[i]
                except:
                    desc['perfilseller']='urlnaoencontrada'

                lista_dicts.append(desc)

        datagoogle = pd.DataFrame(lista_dicts)
        datagoogle.to_excel("googlehausz0506.xlsx")
  


def google():
    google = Google()
    google = Google()
    google.get_precos()


default_args = {
  'start_date': datetime(2022,8,31),
  'sla': timedelta(minutes=50)
}
    
with DAG('google_shopping',  default_args=default_args,
   catchup=False) as dag:

    google = PythonOperator(
        task_id = 'google',
        python_callable = google
    )

google
