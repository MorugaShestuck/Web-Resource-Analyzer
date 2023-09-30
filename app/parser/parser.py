from app.parser.SeleniumLinkParser import SeleniumLinkParser
from app.parser.ClassicLinkParser import ClassicLinkParser
from bs4 import BeautifulSoup
import requests


def parse_urls(url, depth=1):
    if len(BeautifulSoup(requests.get(url).text, "html.parser").find_all('a', href=True)) <= 3:
        p = SeleniumLinkParser()
        p.crawl(url, depth)
        return p
    else:
        p = ClassicLinkParser()
        p.crawl(url, depth)
        return p


if __name__ == "__main__":
    p = parse_urls("https://lenta.ru/news/2022/10/06/rules/")
    print(p.type + " " + str(p.length()))

    p = parse_urls("https://pet-mir.ru/")
    print(p.type + " " + str(p.length()))