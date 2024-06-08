## PyEnglish (Dictionary and Translator inside of the terminal)

from bs4 import BeautifulSoup
import requests

class PyEnglish:
    def __init__(self):
        self.url_wordreference = "https://www.wordreference.com/es/translation.asp"
        self.url_libretranslate = "https://libretranslate.de/translate"
        self.use_amount_dict = 0
        self.run = True
        self.use_amount_trans = 0
        self.select_apps()

        if self.use_amount_dict > 0:
            for i in range(5):
                self.search_word()

        elif self.use_amount_trans > 0:
            for i in range(5):
                self.translate_word_or_phrase()

    def select_apps(self):
        if self.run:
            print("Hi, welcome to PyEnglish!")
            print("\n1. WordReference (Dictionary)\n2. LibreTranslate (Translator)")
            option = int(input("\nType the option that you want to select: "))

            if option == 1:
                self.search_word()
            elif option == 2:
                self.translate_word_or_phrase()

    ## If the user selects the first option (WordReference), he/she searchs words with the following function
    def search_word(self):
        word_toSearch = input("\nType the word that you want to search: ")
        parameters = {"tranword": word_toSearch}

        response = requests.get(self.url_wordreference, params=parameters)

        if response.status_code != 200:
            print(f"Error with the HTTP request: {response.status_code}")
            return
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            translations = soup.find_all('td', class_='ToWrd')

            if translations:
                print(f"\nTranslations for the word {word_toSearch}")
                self.use_amount_dict += 1
                for translation in translations:
                    print(translation.text.strip())
            else:
                print(f"Couldn't be found translations for the word: {word_toSearch}")

    ## Translator function with DeepL
    def translate_word_or_phrase(self, target_lang="en", source_lang="es"):
        word_toTranslate = input("\nType a word or phrase that you want to translate: ").strip()

        headers = {
        "Content-Type": "application/x-www-form-urlencoded"
        }

        params = {
            "q": word_toTranslate,
            "source": source_lang,
            "target": target_lang,
            "format": "text"
        }

        response = requests.post(self.url_libretranslate, data=params, headers=headers)

        if response.status_code != 200:
            print(f"Error with the HTTP request: {response.status_code}, {response.text}")
            return
        else:
            result = response.json()
            translation = result["translatedText"]

            print(f"\nTranslation: {translation}")
            self.use_amount_trans += 1

if __name__ == "__main__":
    pyenglish = PyEnglish()