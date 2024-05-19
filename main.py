from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


# Inicializar o navegador
driver = webdriver.Chrome()

# URL da página de login
login_url = 'https://pacocondominios.superlogica.net/clients/areadocondomino/unidades/id/18195'
driver.get(login_url)

# Aguarde o campo de email aparecer e preencha-o
email_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "email"))
)
email_field.send_keys("tapparo.flavio@gmail.com")

# Clique no botão "Entrar Agora"
entrar_agora_button = driver.find_element(By.ID, "salvar")
entrar_agora_button.click()

# Aguarde o campo de senha aparecer e preencha-o
senha_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "senha"))
)
senha_field.send_keys("Fet@250287")

# Clique no botão "Entrar"
entrar_button = driver.find_element(By.XPATH, "//input[@value='Entrar']")
entrar_button.click()

# Aguarde o carregamento da página de destino
time.sleep(5)

# Encontrar os elementos <li> com a classe apropriada
list_items = driver.find_elements(By.CSS_SELECTOR, 'li.bloco')

# Lista para armazenar os dados extraídos
data = []

# Iterar sobre os elementos <li> e extrair os dados
for item in list_items:
    dados = item.get_attribute('dados')
    if dados:
        dados_dict = json.loads(dados.replace('&quot;', '"'))
        data.append(dados_dict)

# Salvar os dados em um arquivo JSON
with open('dados_moradores.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print('Dados extraídos e salvos em dados_moradores.json')

# Fechar o navegador
driver.quit()
