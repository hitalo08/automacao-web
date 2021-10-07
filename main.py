#--------------AUTOMAÇÃO WEB E BUSCA DE INFORMAÇÕES COM PYTHON----------------
#Selenium é a ferramenta mais utilizada para automação web.
#para utilizar o selenium é necessário baixar o web driver e selenium.
#baixar o webdriver e colocar na pasta do seu código
#google chrome - chromedriver
#firefox - geckodriver
import time
from selenium import webdriver #<- Importando somente o webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import openpyxl

navegador = webdriver.Chrome('chromedriver.exe') #< abrindo navegador
#passo 1 - Pegar cotação dolar
#entrar no site google
navegador.get('https://www.google.com') #<- navegar no endereço estagnado.
#pesquisar "cotação dolar"
navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('Cotação dolar')
navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
#pegar cotação da pagina do google
cotacao_dolar = navegador.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value') #Pegando o atributo do elemento
print('A cotação do dolar é: {}'.format(cotacao_dolar))
#utilizamos aspas simples pois em alguns xpath possuem aspas duplas.
#passo 2 - Pegar cotação euro
navegador.get('https://www.google.com')
navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('Cotação euro')
navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
cotacao_euro = navegador.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value') #Pegando o atributo do elemento
print('A cotação do euro é: {}'.format(cotacao_euro))
#passo 3 - Pegar cotação ouro
navegador.get('https://www.melhorcambio.com/ouro-hoje')
cotacao_ouro = navegador.find_element_by_xpath('//*[@id="comercial"]').get_attribute('value')
print('A cotação do ouro é: {}'.format(cotacao_ouro))
cotacao_ouro = cotacao_ouro.replace(',','.')
print('')
print('-'*10)
print('BASE DE DADOS')
print('-'*10)
#passo 4 - Importar base de dados
table = pd.read_excel('Produtos.xlsx')
#Sempre que for importar base de dados no python, utilizaremos o pandas
#passo 5 - Atualizar cotação, o preço de compra e o preço de vendas
#Sempre que quisermos atualizar uma linha de uma tabela utilizamos o .loc ex: table.loc
table.loc[table['Moeda'] == 'Dólar','Cotação'] = float(cotacao_dolar) #Tabela na linha moeda compare com dolar e aplique a cotação do valor atual float dolar
table.loc[table['Moeda'] == 'Euro','Cotação'] = float(cotacao_euro)
table.loc[table['Moeda'] == 'Ouro','Cotação'] = float(cotacao_ouro)
#preço de compra = cotação * preço original
table['Preço Base Reais'] = table['Preço Base Original'] * table['Cotação']
#preço de vendas = preço de compra * margem de lucro
table['Preço Final'] = table['Preço Base Reais'] * table['Margem']
table['Preço Final'] = table['Preço Final'].map('R${:.2f}'.format) #formatando o valor
table['Cotação'] = table['Cotação'].map('R${:.2f}'.format)
table['Preço Base Reais'] = table['Preço Base Reais'].map('R${:.2f}'.format)
print(table)
#passo 6 - exportar relatório atualizado
table.to_excel('Produtos Novo.xlsx')
print('!!!!!!!!!!!!!!!!!VOCÊ EXPORTOU A BASE DE DADOS COM SUCESSO!!!!!!!!!!!!!!!!')
time.sleep(2)
navegador.quit()


