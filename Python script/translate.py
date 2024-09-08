import requests

def translate_text(text, target_lang):
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": f"en|{target_lang}"
    }
    response = requests.get(url, params=params)
    return response.json()["responseData"]["translatedText"]

userInput = input("Translate: ")

translated = translate_text(userInput, 'ja')
print(translated)
