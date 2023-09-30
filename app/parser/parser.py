from SeleniumParser import SeleniumParser
from ClassicParser import ClassicParser
from bs4 import BeautifulSoup
import requests


def parse(url, depth=1):
    if len(BeautifulSoup(requests.get(url).text, "html.parser").find_all('a', href=True)) <= 3:
        p = SeleniumParser()
        p.crawl(url, depth)
        return p
    else:
        p = ClassicParser()
        p.crawl(url, depth)
        return p


if __name__ == "__main__":
    p = parse("https://sbermegamarket.ru/catalog/audiosistemy-dlya-lodok-i-katerov/")
    print(p.type + " " + str(p.length()))

    p = parse("https://pet-mir.ru/")
    print(p.type + " " + str(p.length()))