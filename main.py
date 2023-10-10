from selenium import webdriver
from selenium.webdriver.common.by import By     #importa o By pra usar nos find_element
from selenium.webdriver.support.ui import WebDriverWait     #importa a função de esperar um elemento aparecer
from selenium.webdriver.support import expected_conditions as EC    #importa EC pra ser usado na função de espera
from datetime import datetime

#inicia webdriver para o Chrome
driver = webdriver.Chrome()

## login no twitter ##

#define username e senha do twitter do bot (escrever manualmente)
usernameTwitter = ''
senhaTwitter = ''

#pega a data de hoje no mesmo formato do site de cc, pra comparar com os posts depois
hoje = datetime.now().strftime("%d-%m-%Y")

#pra testar o bot como um dia que tem notícia, comentar a linha 17 e descomentar a 20
#hoje = "28-06-2023"

#acessar pag de login do twitter
driver.get("https://twitter.com/i/flow/login")

#espera a página carregar até o input de username aparecer 
                            #tempo max de espera em segundos
elem = WebDriverWait(driver, 30).until(
                                                #xpath do input de username
    EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'))
)

#seleciona o input de username pelo xpath
username = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')

#escreve o username definido na variavel
username.send_keys(usernameTwitter)

#seleciona todos os botões da página
botoes = driver.find_elements(By.XPATH, '//div[@role="button"]')

#clica no penúltimo botão, que é o de continuar
botoes[-2].click()

#espera a página carregar até o input de senha aparecer
elem = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'))
)

#seleciona o input de senha pelo xpath
senha = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')

#escreve a senha
senha.send_keys(senhaTwitter)

#encontra o botão de enviar e já clica nele com o .click()
driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div').click()

#fecha popup de 2-factor se aparecer
try:
    #tenta encontrar o botão de fechar pop-up. Se ele não existir, vai dar erro e cair no except
    driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div').click()
except:
    print('não apareceu pop-up')

#guarda a guia do twitter pra voltar pra ela depois
twitter_tab = driver.current_window_handle


## busca os posts no site de cc ##

#abre uma nova guia
driver.switch_to.new_window('tab')

#acessa o site de cc
driver.get("https://cc.uffs.edu.br/")

#guarda a guia dos posts pra voltar do twitter caso tenha mais notícia
posts_tab = driver.current_window_handle

#seleciona todos os posts pela classe 'post-row'
posts = driver.find_elements(By.CLASS_NAME, 'post-row')


## postagem no twitter de cada post de hoje ##

#percorre cada post
for post in posts:

    #pega a data (única tag 'time' dentro do html do post) e vê se é hoje
    if post.find_element(By.TAG_NAME, 'time').text == hoje:

        #pega os dados da noticia (também pela tag)
        link = post.find_element(By.TAG_NAME, 'a').get_attribute("href")
        titulo = post.find_element(By.TAG_NAME, 'h4').text

        #muda pra guia do twitter
        driver.switch_to.window(twitter_tab)

        #espera aparecer a caixa de texto
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div/span'))
        )

        #seleciona a caixa para escrever
        caixaTweet = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div/span')
        
        #escreve o título e o link da notícia
        caixaTweet.send_keys(titulo + ' ' + link)

        #clica no botão de enviar
        driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[3]').click()

        #volta pra guia de posts pro loop poder continuar e selecionar mais notícias
        driver.switch_to.window(posts_tab)

#volta pra guia do twitter
driver.switch_to.window(twitter_tab)

#abre o perfil do bot pra ver o resultado
driver.get("https://twitter.com/"+usernameTwitter)

#input pro navegador não fechar
input()

