from sys import exit
import json

validos = {"Russo": "rus",
           "English": "eng",
           "Portuguese": "por"
}

def load_preferences():
    try:
        with open('./config/preferences.json', 'r') as file:
            preferences = json.load(file)
        return preferences
    except FileNotFoundError:
        print("File 'preferences.json' not found.")
        exit()
        return None
    
def save_preferences(preferences):
    try:
        with open('./config/preferences.json', 'w') as file:
            json.dump(preferences, file, indent=4)
        print("Preferências salvas com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar preferências: {e}")

preferencias = load_preferences()
#save_pref = save_preferences(preferencias)



if preferencias is not None:
    if preferencias['language'] in validos.values():
        pass
    else:
        escolha_idioma = input("Escolha o idioma: ")

        escolha_idioma = escolha_idioma.lower()

        preferencias['language'] = escolha_idioma

        save_preferences(preferencias)
else:
    print("Não foi possível carregar as preferências existentes.")

chaves = ["language", "screenFix", "clipboardMode"]

# Leitura do arquivo JSON
try:
    for chave in chaves:
        with open('./config/preferences.json', 'r') as file:
            preferences = json.load(file)

            # Obter preferência da chave "language"
            language_preference = preferences.get(f'{chave}')

            if language_preference is not None:
                #print(f"{chave} preference:", language_preference)
                pass
            else:
                print("Language preference not found in preferences.json.")
except FileNotFoundError:
    print("File 'preferences.json' not found.")
    exit()

# chaves
language = preferences.get('language')
fix = preferences.get('screenFix')
clipboard = preferences.get('clipboardMode')
