import tkinter as tk
from PIL import Image, ImageTk
import os
import pytesseract
import pyautogui

pyautogui.screenshot("teste.png")

WIDTH, HEIGHT = 900, 900
topx, topy, botx, boty = 0, 0, 0, 0
rect_id = None
original_path = "./teste.png"
cropped_path = "./imagem_recortada.png"

def get_mouse_posn(event):
    global topy, topx
    topx, topy = event.x, event.y

def update_sel_rect(event):
    global rect_id, topy, topx, botx, boty
    botx, boty = event.x, event.y
    canvas.coords(rect_id, topx, topy, botx, boty)

def crop_and_extract_text():
    global topx, topy, botx, boty, original_path, cropped_path

    # Cria uma imagem PIL a partir do caminho da imagem original
    original_image = Image.open(original_path)

    # Recorta a região selecionada da imagem original
    cropped_image = original_image.crop((topx, topy, botx, boty))

    # Salva a imagem recortada em um novo arquivo
    cropped_image.save(cropped_path)

    print(f"Imagem recortada salva em {cropped_path}")

    # Extrai texto da imagem recortada
    extracted_text = pytesseract.image_to_string(cropped_image, lang="por")
    
    print("Texto extraído:")
    print(extracted_text)

# Criação da janela e configurações
window = tk.Tk()
window.title("Select Area")
window.configure(background='green')

img = ImageTk.PhotoImage(Image.open(original_path))
canvas = tk.Canvas(window, width=img.width(), height=img.height(),
                   borderwidth=0, highlightthickness=0)
canvas.pack(expand=True)
canvas.img = img
canvas.create_image(0, 0, image=img, anchor=tk.NW)

# Define as coordenadas do retângulo de seleção para cobrir toda a tela
rect_id = canvas.create_rectangle(topx, topy, WIDTH, HEIGHT,
                                  dash=(2,2), fill='', outline='blue')
canvas.bind('<Button-1>', get_mouse_posn)
canvas.bind('<B1-Motion>', update_sel_rect)
canvas.bind('<ButtonRelease-1>', lambda event: crop_and_extract_text())

# Obtém as dimensões da tela diretamente
screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()

# Atualiza a geometria da janela
window.geometry('%sx%s' % (screen_width, screen_height))

window.mainloop()
