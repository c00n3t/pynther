import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import pytesseract
import subprocess
import sys
import pyautogui
import time

sys.path.insert(0, './config/')
from pref import language, fix, clipboard

pyautogui.screenshot("select.png")

WIDTH, HEIGHT = 900, 900
topx, topy, botx, boty = 0, 0, 0, 0
original_path = "./select.png"
cropped_path = "./view.png"
rect_id = None

def get_mouse_posn(event):
    global topy, topx
    topx, topy = event.x, event.y

def update_sel_rect(event):
    global topy, topx, botx, boty, original_path, cropped_path, rect_id

    # Atualiza as coordenadas do retângulo de seleção
    botx, boty = event.x, event.y

    # Garante que as coordenadas estão dentro dos limites da imagem
    botx = max(topx, min(botx, img.width()))
    boty = max(topy, min(boty, img.height()))

    # Atualiza as coordenadas do retângulo de seleção
    canvas.coords(rect_id, topx, topy, botx, boty)

    # Desenha o retângulo na tela
    draw_selection_rectangle()

def crop_and_extract_text():
    global topx, topy, botx, boty, original_path, cropped_path

    # Cria uma imagem PIL a partir do caminho da imagem original
    original_image = Image.open(original_path)

    # Recorta a região selecionada da imagem original
    cropped_image = original_image.crop((topx, topy, botx, boty))

    # Salva a imagem recortada em um novo arquivo
    cropped_image.save(cropped_path)

    # Extrai texto da imagem recortada
    extracted_text = pytesseract.image_to_string(cropped_image, lang=f"{language}")
    cleaned_text = ''.join(char for char in extracted_text if char.isprintable())

    window.clipboard_clear()
    window.clipboard_append(extracted_text)
    window.update()

    try:
        subprocess.run("rm view.png && rm select.png", shell=True)
    except:
        pass
    if fix == 0:
        window.after(5, window.destroy)
    else:
        pass

def draw_selection_rectangle():
    # Desenha o retângulo de seleção na imagem
    img = Image.open(original_path)
    draw = ImageDraw.Draw(img)
    draw.rectangle([topx, topy, botx, boty], outline='#00FF00', width=2)

    # Atualiza a exibição na tela
    photo = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    canvas.img = photo

window = tk.Tk()
window.title("Select Area")
window.configure(background='green')

img = ImageTk.PhotoImage(Image.open(original_path))
canvas = tk.Canvas(window, width=img.width(), height=img.height(),
                   borderwidth=0, highlightthickness=0)
canvas.pack(expand=True)
canvas.img = img
canvas.create_image(0, 0, image=img, anchor=tk.NW)

rect_id = canvas.create_rectangle(topx, topy, botx, boty, outline='#00FF00', width=2)  # Adiciona a criação do retângulo

canvas.bind('<Button-1>', get_mouse_posn)
canvas.bind('<B1-Motion>', update_sel_rect)
canvas.bind('<ButtonRelease-1>', lambda event: crop_and_extract_text())

# Obtém as dimensões da tela diretamente
screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()

# Atualiza a geometria da janela
window.geometry('%sx%s' % (screen_width, screen_height))

window.configure(background='white')
window.mainloop()
