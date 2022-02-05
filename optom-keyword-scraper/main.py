import time

from bs4 import BeautifulSoup
import requests
from rich import print


URL = "https://www.allaboutvision.com/resources/"
PAGES = ["glossary.htm", "glossary-1a.htm", "glossary-1b.htm", "glossary-2.htm",  "glossary-2a.htm",  "glossary-2b.htm",  "glossary-3.htm"]

def get_words(URL, PAGES):
    """
    Get words from page
    """

    words = []
    for page in PAGES:
        time.sleep(0.5)
        print(f"parsing: {page}")
        response = requests.get(URL + page)
        soup = BeautifulSoup(response.content, 'html.parser')
        p_tags = soup.find('div', {'class':'article__content'}).findAll("p", recursive=False)

        for line in p_tags:
            soup_p = BeautifulSoup(str(line), 'html.parser')
            strong = soup_p.find('strong')
            if strong is not None:
                words.append(strong.text)

    return words


def parse_words(words):
    """
    parse word
    5 letters per word
    make sure words are all alpha
    make sure words are lower cased
    """
    parsed_words = []
    print(f"words to parse: {len(words)}")

    for word in words:
        _word = word.replace("'", "")
        if len(_word) > 4:
            first_5 = _word[0:5]
            if first_5.isalpha():
                parsed_words.append((first_5.lower(), word))

    return parsed_words


def save_word_list(words):
    """
    save word list
    """
    count = 0

    with open("wordlist.ts", "w") as file:
        file.write("export const WORDS = [\n")
        for word  in words:
            file.write(f"'{word[0]}', // {word[1]}\n")
            count += 1
        file.write("]")
    print(f'words saved: {count}')


def main():
    words = get_words(URL, PAGES)
   # words = [
   #         'ANSI Z87.1-2003 Standard', 
   #         'anterior chamber', 
   #         'antibody', 
   #         "h'h'h'h'h",
   #         'ANTII',
   #         'antioxidant', 
   #         'anti-reflective coating',
   #         'lol',
   #         ]
    parsed_words = parse_words(words)
    save_word_list(parsed_words)


if __name__ == "__main__":
    main()
