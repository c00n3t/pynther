# lang.py

import os 
import sys
from pathlib import Path
import subprocess
import json

sys.path.insert(0, './config/')
from pref import preferencias, load_preferences, save_preferences


validos = {"Russo": "rus",
           "English": "eng",
           "Portuguese": "por"
}


def l_ptbr():
        escolha_idioma = "por"
        escolha_idioma = escolha_idioma.lower()
        preferencias['language'] = escolha_idioma
        save_preferences(preferencias)


def l_russian():
        escolha_idioma = "rus"
        escolha_idioma = escolha_idioma.lower()
        preferencias['language'] = escolha_idioma
        save_preferences(preferencias)






