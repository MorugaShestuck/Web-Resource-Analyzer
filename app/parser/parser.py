from app.parser.SeleniumLinkParser import SeleniumParser
from app.parser.ClassicLinkParser import ClassicParser
from bs4 import BeautifulSoup
import requests


def parse_urls(url, depth=1):
    if len(BeautifulSoup(requests.get(url).text, "html.parser").find_all('a', href=True)) <= 3:
        p = SeleniumParser()
        p.crawl(url, depth)
        return p
    else:
        p = ClassicParser()
        p.crawl(url, depth)
        return p


if __name__ == "__main__":
    p = parse_urls("https://lenta.ru/news/2022/10/06/rules/")
    print(p.type + " " + str(p.length()))

    p = parse_urls("https://pet-mir.ru/")
    print(p.type + " " + str(p.length()))