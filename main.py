import wx.adv
import wx
import os
import subprocess
from pynput import keyboard
from pyautogui import screenshot
import sys
from lang import l_ptbr, l_russian, validos
import threading
import time

sys.path.insert(0, './config/')
from pref import language, fix, clipboard

def lconfig():
    try:
        os.environ['TESSDATA_PREFIX'] = './lang-tess/'
    except:
        print("Erro!")
        exit()

# Linguagens-tess
lconfig()

# AppIcon
TRAY_TOOLTIP = 'Name' 
TRAY_ICON = 'alien.png' 

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        self.listener_thread = threading.Thread(target=self.start_listener)
        self.listener_thread.start()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Converter agora', self.on_start)
        menu.AppendSeparator()
        create_menu_item(menu, 'Idiomas', self.on_config)
        menu.AppendSeparator()
        create_menu_item(menu, 'Sair', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        pass

    def on_start(self, event):
        screenshot("select.png")
        if os.name != "nt":
            subprocess.run("python3 capture.py", shell=True)
        else:
            subprocess.run("python capture.py", shell=True)

    def on_config(self, event):
        os.system("clear")
        while True:
             print("Escolha um idioma:")
             print("1. Português")
             print("2. Russo")

             escolha_idioma = input("Digite o número do idioma desejado: ")

             if escolha_idioma == '1':
                 print("Você escolheu Português")
                 l_ptbr()
                 os.system("clear")
                 break  # Sai do loop e retorna ao menu principal
             elif escolha_idioma == '2':
                 print("Você escolheu Russo")
                 l_russian()
                 os.system("clear")
                 break  # Sai do loop e retorna ao menu principal
             else:
                 time.sleep(2)
                 print("Opção inválida. Por favor, escolha novamente.")
                 os.system("clear")


    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

    def on_press(self, key):
        try:
            if key.char == 'z':
                self.on_start(None)
        except AttributeError:
            pass

    def start_listener(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

class App(wx.App):
    def OnInit(self):
        frame = wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

def main():
    app = App(False)
    app.MainLoop()

if __name__ == '__main__':
    main()
