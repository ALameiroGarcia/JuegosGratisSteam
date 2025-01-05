import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import tkinter as tk
from tkinter import messagebox
from tkinterweb import HtmlFrame  # Importa el HtmlFrame de tkinterweb

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

# Función para abrir la página web de Steam dentro de la aplicación
def abrir_pagina_web():
    # Crea una ventana secundaria que contendrá el visor web
    ventana_web = tk.Toplevel(root)
    ventana_web.title("Steam - Juegos Gratis")
    ventana_web.geometry("800x600")
    
    # Crear un frame para mostrar la página web
    frame = HtmlFrame(ventana_web, width=800, height=600)
    frame.load_url(URL)  # Carga la URL de Steam dentro del frame
    frame.pack()

# Función para iniciar sesión y agregar juegos
def agregar_juegos_a_cuenta(juegos, usuario, contraseña):
    driver = webdriver.Chrome()
    driver.get('https://store.steampowered.com/login/')
    
    time.sleep(2)
    driver.find_element(By.XPATH, '(//input[@type="text"])[1]').send_keys(usuario)  # Primer campo de texto (usuario)
    driver.find_element(By.XPATH, '(//input[@type="password"])[1]').send_keys(contraseña)  # Primer campo de contraseña
    driver.find_element(By.XPATH,'//button[@class="DjSvCZoKKfoNSmarsEcTS"]').click()
    
    messagebox.showinfo("Autenticación", 'Por favor, completa cualquier paso adicional de autenticación (Steam Guard) si es necesario.')
    messagebox.showinfo("Autenticación", 'Presiona Enter después de completar la autenticación y asegurarte de estar en la página principal de tu cuenta...')
    
    for juego in juegos:
        driver.get(juego['enlace'])
        try:
            driver.find_element(By.CLASS_NAME, 'btn_addtocart').click()
            print(f"Juego añadido: {juego['titulo']}")
        except Exception:
            print(f"No se pudo añadir: {juego['titulo']}")
    
    print('Proceso completado, cerrando el navegador')
    driver.quit()

# Función que maneja la ejecución del programa
def ejecutar_programa():
    juegos = obtener_juegos_gratis()
    if not juegos:
        messagebox.showerror("Error", "No se pudieron obtener juegos gratuitos.")
        return
    
    lista_juegos = '\n'.join([f"{i+1}. {juego['titulo']}" for i, juego in enumerate(juegos)])
    
    juego_seleccionado = messagebox.askquestion("Juegos gratuitos", f"Se encontraron los siguientes juegos gratuitos:\n\n{lista_juegos}\n\n¿Deseas agregarlos a tu cuenta?")
    if juego_seleccionado == 'yes':
        usuario = entry_usuario.get()
        contraseña = entry_contraseña.get()
        
        if not usuario or not contraseña:
            messagebox.showerror("Error", "Por favor ingresa tu usuario y contraseña de Steam.")
            return
        
        agregar_juegos_a_cuenta(juegos, usuario, contraseña)
        messagebox.showinfo("Éxito", "Los juegos han sido añadidos a tu cuenta de Steam.")
    else:
        messagebox.showinfo("Operación cancelada", "No se han agregado juegos a tu cuenta.")

# Crear la ventana principal
root = tk.Tk()
root.title('Bot Steam: Juegos Gratis')

# Configurar la ventana
root.geometry('400x300')

# Etiqueta y campo de texto para el usuario
label_usuario = tk.Label(root, text="Usuario de Steam:")
label_usuario.pack(pady=5)
entry_usuario = tk.Entry(root, width=30)
entry_usuario.pack(pady=5)

# Etiqueta y campo de texto para la contraseña
label_contraseña = tk.Label(root, text="Contraseña de Steam:")
label_contraseña.pack(pady=5)
entry_contraseña = tk.Entry(root, show="*", width=30)
entry_contraseña.pack(pady=5)

# Botón para ejecutar el programa
button_ejecutar = tk.Button(root, text="Obtener y agregar juegos", command=ejecutar_programa)
button_ejecutar.pack(pady=20)

# Botón para abrir la página web de Steam dentro de la app
button_abrir_pagina = tk.Button(root, text="Ver Juegos Gratis en Steam", command=abrir_pagina_web)
button_abrir_pagina.pack(pady=10)

# Ejecutar la ventana
root.mainloop()
