import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import tkinter as tk
from tkinter import ttk, messagebox
from tkinterweb import HtmlFrame

# URL de juegos gratis en Steam
URL = 'https://store.steampowered.com/search/?maxprice=free&specials=1'

# Función para obtener los juegos
def obtener_juegos_gratis():
    response = requests.get(URL)
    if response.status_code != 200:
        print('Error al acceder a Steam')
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    juegos = []
    
    for juego in soup.find_all('a', class_='search_result_row'): 
        try:
            titulo = juego.find('span', class_='title').text
            enlace = juego['href']
            fecha = juego.find('div', class_='search_released').text.strip()
            precio = juego.find('div', class_='discount_final_price').text if juego.find('div', 'discount_final_price') else 'Gratis'
            reseñas = juego.find('span', class_='search_review_summary')
            if reseñas:
                reseñas = reseñas['data-tooltip-html'] if 'data-tooltip-html' in reseñas.attrs else 'Sin reseñas'
            else:
                reseñas = 'Sin reseñas'
            juegos.append({'titulo': titulo, 'enlace': enlace, 'fecha': fecha, 'precio': precio, 'reseñas': reseñas})
        except AttributeError:
            continue
    
    return juegos

# Función para agregar juegos a la cuenta con Selenium 
def agregar_juegos_a_cuenta(juegos, usuario, contraseña):
    driver = webdriver.Chrome()
    driver.get('https://store.steampowered.com/login/')
    
    time.sleep(2)
    driver.find_element(By.XPATH, '(//input[@type="text"])[1]').send_keys(usuario)
    driver.find_element(By.XPATH, '(//input[@type="password"])[1]').send_keys(contraseña)
    driver.find_element(By.XPATH,'//button[@class="DjSvCZoKKfoNSmarsEcTS"]').click()
    
    messagebox.showinfo("Autenticación", 'Completa cualquier paso adicional de autenticación.')
    
    for juego in juegos:
        driver.get(juego['enlace'])
        try:
            driver.find_element(By.CLASS_NAME, 'btn_addtocart').click()
            messagebox.showinfo("Atencion", "Por favor, siga las instrucciones en el navegador para abrir la aplicación de steam. Cuando haya terminado, pulse Aceptar.")
            messagebox.showinfo("", f"Juego añadido: {juego['titulo']}")
        except Exception:
            messagebox.showinfo("", f"No se pudo añadir: {juego['titulo']}")
    print('El navegador permanecerá abierto hasta que el usuario lo cierre manualmente.')

# GUI principal
root = tk.Tk()
root.title('Bot Steam Mejorado')
root.geometry('800x600')

# Widgets de usuario y contraseña
label_usuario = tk.Label(root, text="Usuario de Steam:")
label_usuario.pack(pady=5)
entry_usuario = tk.Entry(root, width=40)
entry_usuario.pack(pady=5)

label_contraseña = tk.Label(root, text="Contraseña de Steam:")
label_contraseña.pack(pady=5)
entry_contraseña = tk.Entry(root, show="*", width=40)
entry_contraseña.pack(pady=5)

# Filtro de reseñas
label_filtro = tk.Label(root, text="Filtrar por reseñas:")
label_filtro.pack(pady=5)
combo_reseñas = ttk.Combobox(root, values=["Todas", "Mayormente Positivas", "Mixtas", "Negativas"])
combo_reseñas.set("Todas")
combo_reseñas.pack(pady=5)

# Tabla para mostrar los juegos
tree = ttk.Treeview(root, columns=("Titulo", "Fecha", "Precio", "Reseñas"), show='headings')
tree.heading('Titulo', text='Título')
tree.heading('Fecha', text='Fecha de Lanzamiento')
tree.heading('Precio', text='Precio')
tree.heading('Reseñas', text='Reseñas')
tree.pack(pady=10, fill='both', expand=True)

# Barra de progreso
progress_bar = ttk.Progressbar(root, length=400, mode='determinate')
progress_bar.pack(pady=10)

# Botones
button_obtener = tk.Button(root, text="Ver lista de juegos gratis", command=lambda: mostrar_juegos())
button_obtener.pack(pady=5)

button_agregar = tk.Button(root, text="Agregar Juegos a la cuenta", command=lambda: ejecutar_agregar())
button_agregar.pack(pady=5)

# Función para mostrar juegos en la tabla
def mostrar_juegos():
    tree.delete(*tree.get_children())
    juegos = obtener_juegos_gratis()
    filtro = combo_reseñas.get()
    for juego in juegos:
        if filtro == 'Todas' or filtro in juego['reseñas']:
            tree.insert('', 'end', values=(juego['titulo'], juego['fecha'], juego['precio'], juego['reseñas']))

# Función para ejecutar el proceso completo
def ejecutar_agregar():
    juegos = obtener_juegos_gratis()
    if not juegos:
        messagebox.showerror("Error", "No se pudieron obtener juegos gratuitos.")
        return
    
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    if not usuario or not contraseña:
        messagebox.showerror("Error", "Por favor ingresa tu usuario y contraseña de Steam.")
        return
    
    agregar_juegos_a_cuenta(juegos, usuario, contraseña)

# Iniciar GUI
root.mainloop()
