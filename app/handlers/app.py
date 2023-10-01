import logging

from fastapi import FastAPI

from app.analyzer.analyzer import Analyzer
from app.parser import parser, ContentParser
from app.utils.Cache import Cache
from app.utils.hash_table import HashTable


app = FastAPI()

keywords, categories = HashTable(), HashTable()
keywords.load("data/data.json")
categories.load("data/categories.json")
cache = Cache(cache_file="data/cache.json")

@app.get('/ping')
async def ping():
    return {"message": "pong"}


@app.get('/get_pages')
async def get_pages(url):
    p = parser.parse_urls(url)
    return {"links": p.site_links}


@app.get("/check_url")
async def check_domain(url: str):
    try:
        cache.load_cache()
        cached_data = cache.get_data(url)
        if cached_data:
            category, theme = cached_data
        else:
            analyzer = Analyzer(keywords=keywords)
            p = ContentParser.ContentParser(url=url)
            p.fetch_content()
            p.parse_content()
            analyzer.analyze_content(p.content)
            theme = list(analyzer.get_score(deep=1))[0]
            category = categories.get(list(analyzer.get_score(deep=1))[0])
            cache.set_data(url, [category, theme])
            cache.save_cache()
        return {"code": 200, "data": {"category": category, "theme": theme}}
    except Exception as e:
        print(e)
        return{"error": e}