import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from getpass import getpass
from selenium.webdriver.common.action_chains import ActionChains

# URL de juegos gratis en Steam
URL = 'https://store.steampowered.com/search/?maxprice=free&specials=1'

# Función para obtener juegos gratis
def obtener_juegos_gratis():
    response = requests.get(URL)
    if response.status_code != 200:
        print('Error al acceder a Steam')
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    juegos = []
    
    for juego in soup.find_all('a', class_='search_result_row'): 
        titulo = juego.find('span', class_='title').text
        enlace = juego['href']
        juegos.append({'titulo': titulo, 'enlace': enlace})
    
    return juegos

# Función para iniciar sesión y agregar juegos
def agregar_juegos_a_cuenta(juegos, usuario, contraseña):
    driver = webdriver.Chrome()
    driver.get('https://store.steampowered.com/login/')
    
    time.sleep(2)
    driver.find_element(By.XPATH, '(//input[@type="text"])[1]').send_keys(usuario)  # Primer campo de texto (usuario)
    driver.find_element(By.XPATH, '(//input[@type="password"])[1]').send_keys(contraseña)  # Primer campo de contraseña
    driver.find_element(By.XPATH,'//button[@class="DjSvCZoKKfoNSmarsEcTS"]').click()
    
    print('Por favor, completa cualquier paso adicional de autenticación (Steam Guard) si es necesario.')
    input('Presiona Enter después de completar la autenticación y asegurarte de estar en la página principal de tu cuenta...')
    
    for juego in juegos:
        driver.get(juego['enlace'])
        try:
            driver.find_element(By.CLASS_NAME, 'btn_addtocart').click()
            print(f"Juego añadido: {juego['titulo']}")
        except Exception:
            print(f"No se pudo añadir: {juego['titulo']}")
    
    print('Proceso completado, cerrando el navegador')
    driver.quit()

# Ejecución del bot
if __name__ == '__main__':
    juegos = obtener_juegos_gratis()
    print(f'Se encontraron {len(juegos)} juegos gratuitos.')
    
    for i, juego in enumerate(juegos, 1):
        print(f"{i}. {juego['titulo']} - {juego['enlace']}")
    
    opcion = input('¿Deseas agregar estos juegos a tu cuenta de Steam? (s/n): ').strip().lower()
    if opcion == 's':
        usuario = input('Introduce tu usuario de Steam: ')
        contraseña = getpass('Introduce tu contraseña: ')
        agregar_juegos_a_cuenta(juegos, usuario, contraseña)
    else:
        print('Operación cancelada.')
