import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from parsel import Selector
from bs4 import BeautifulSoup
import pandas as pd
import datetime

filename = sys.argv[1]

#file = open("input.txt","r")
#file = open(filename,"r")

title_check = []
correcciones = []
categorias = []

#for product in file.readlines():
#	product = product.replace("\n","")
#	title_check.append(product)

#file.close()
df = pd.read_csv("input.csv")
title_check = df['producto'].values.tolist()
correcciones = df['correccion'].values.tolist()
categorias = df['categoria'].values.tolist()
#print(title_check)
#print(correcciones)
#print(categorias)


titles = []
prices = []
corrections = []
categories = []

urlbase = "https://www.tiendainglesa.com.uy/busqueda?0,0," #sys.argv[2]

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome("../chromedriver")

for t in title_check:

    i = title_check.index(t)
    #print(i)
    url = urlbase + t
    driver.get(url)
    driver.refresh()
    sleep(15)

    #print(driver.page_source)

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    for element in soup.findAll('div', attrs={'class': 'SearchResultsWithoutCart'}):
        title = element.find('span', attrs={'class': 'card-product-name'})
        #print(title)
        price = element.find('span', attrs={'class': 'ProductPrice'})
        precio = price.text[2:]
        if (title.text in title_check) and (not title.text in titles) :
            print(title.text)
            titles.append(title.text)
            prices.append(precio)
            corrections.append(correcciones[i])
            categories.append(categorias[i])

print(titles)
print(prices)
print(corrections)
print(categories)

df = pd.DataFrame({'Producto': titles, 'Precio': prices, 'Correcion':corrections, 'Categoria':categories})

today = datetime.datetime.today()
fileNameOutput = 'tienda_inglesa' + str(today.year) + str(today.month) + str(today.day) + '.csv'
df.to_csv(fileNameOutput, index=False, encoding='utf-8')

driver.quit()
