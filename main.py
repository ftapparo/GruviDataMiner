from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Inicializar o navegador
driver = webdriver.Chrome()

# URL da página de login
login_url = 'https://pacocondominios.superlogica.net/clients/areadocondomino'
unidades_url = 'https://pacocondominios.superlogica.net/clients/areadocondomino/unidades'

# Função para fazer login
def login(driver):

    # URL da página de login
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


# Função para carregar mais itens até que todos sejam carregados
def carregar_todos_itens(driver):
    driver.get(unidades_url)

    # Aguarde o carregamento da página de unidades
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "lista"))
    )

    # Obter o total de unidades
    total_unidades = int(driver.find_element(By.CSS_SELECTOR, "div.lista").get_attribute("totalunidades"))

    # Carregar mais itens até que todos sejam carregados
    while True:
        try:
            # Verificar se o botão "Mais itens" está presente e clicável
            botao_mais_itens = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "botaoMaisItens-unidade"))
            )
            botao_mais_itens.click()
            time.sleep(2)  # Aguarde um pouco para os itens serem carregados
        except:
            break

    # Verificar a quantidade de unidades carregadas
    unidade_links = driver.find_elements(By.CSS_SELECTOR, "a.bloco")
    unidades_carregadas = len(unidade_links)

    return unidade_links, total_unidades, unidades_carregadas


# Função para extrair IDs, números e nomes das unidades
def extrair_unidades(driver, unidade_links):
    unidades = []
    for link in unidade_links:
        unidade_url = link.get_attribute('href')
        unidade_id = unidade_url.split('/id/')[1].split('?')[0]
        numero_unidade = link.find_element(By.CSS_SELECTOR, "div.numero").text.strip()
        nome_residente = link.find_element(By.CSS_SELECTOR, "div.nome").text.strip()

        unidade_info = {
            "id": unidade_id,
            "numero": numero_unidade,
            "nome": nome_residente
        }
        unidades.append(unidade_info)

    return unidades


# Função principal
def main():
    # Inicializar o navegador e fazer login
    driver = webdriver.Chrome()
    login(driver)

    # Carregar todos os itens e obter a quantidade total de unidades
    unidade_links, total_unidades, unidades_carregadas = carregar_todos_itens(driver)

    # Extrair informações das unidades
    unidades = extrair_unidades(driver, unidade_links)

    # Dados de resumo
    resumo = {
        "total_unidades": total_unidades,
        "unidades_carregadas": unidades_carregadas,
        "unidades": unidades
    }

    # Salvar as informações das unidades em um arquivo JSON
    with open('unidades.json', 'w', encoding='utf-8') as json_file:
        json.dump(resumo, json_file, ensure_ascii=False, indent=4)

    print('Informações das unidades extraídas e salvas em unidades.json')

    # Fechar o navegador
    driver.quit()

if __name__ == "__main__":
    main()
