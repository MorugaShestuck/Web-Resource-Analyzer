import logging
from typing import Dict, List

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
async def get_pages(url, depth: int = 1):
    try:
        p = parser.parse_urls(url, depth)
        links = p.site_links[:depth]
        return {"code": 200, "data": {"links": links}}
    except Exception as e:
        print(e)
        return {"error": str(e)}


@app.get("/check_url")
async def check_url(url: str, depth: int = 1):
    try:
        cache.load_cache()
        cached_data = cache.get_data(url)
        if cached_data:
            categories_resp, themes_resp = cached_data
            categories_resp = categories_resp[:depth]
            themes_resp = themes_resp[:depth]
        else:
            analyzer = Analyzer(keywords=keywords)
            p = ContentParser.ContentParser(url=url)
            p.fetch_content()
            p.parse_content()
            analyzer.analyze_content(p.content)
            categories_resp = [categories.get(key) for key in list(analyzer.get_score(depth=depth).keys())]
            themes_resp = list(analyzer.get_score(depth=depth).keys())
            cache.set_data(url, [[categories.get(key) for key in list(analyzer.get_score().keys())], list(analyzer.get_score(depth=depth).keys())])
            cache.save_cache()
        return {"code": 200, "data": {"categories": categories_resp, "themes": themes_resp}}
    except Exception as e:
        print(e)
        return {"error": str(e)}


@app.post("/check_urls")
async def check_urls(request_data: Dict[str, List[str]], depth: int = 1):
    urls = request_data.get("urls", [])
    print(depth)
    results = []

    for url in urls:
        try:
            cache.load_cache()
            cached_data = cache.get_data(url)
            if cached_data:
                categories_resp, themes_resp = cached_data
                categories_resp = categories_resp[:depth]
                themes_resp = themes_resp[:depth]
            else:
                analyzer = Analyzer(keywords=keywords)
                p = ContentParser.ContentParser(url=url)
                p.fetch_content()
                p.parse_content()
                analyzer.analyze_content(p.content)
                categories_resp = [categories.get(key) for key in list(analyzer.get_score(depth=depth).keys())]
                themes_resp = list(analyzer.get_score(depth=depth).keys())
                cache.set_data(url, [[categories.get(key) for key in list(analyzer.get_score().keys())],
                                     list(analyzer.get_score(depth=depth).keys())])
                cache.save_cache()

            result = {"url": url, "categories": categories_resp, "themes": themes_resp}
            results.append(result)

        except Exception as e:
            print(e)
            result = {"url": url, "error": str(e)}
            results.append(result)

    return {"code": 200, "data": results}

@app.get('/check_domain')
async def check_domain(url: str, depth: int = 1):
    try:
        results = {"categories": [], "themes": []}
        p = parser.parse_urls(url, depth)
        links = p.site_links[:depth]
        for link in links:
            result = await check_url(link, depth=depth)
            results = {
                "categories": [category for category in result["data"]["categories"]],
                "themes": [theme for theme in result["data"]["themes"]]
            }
        return {"code": 200, "data": results}
    except Exception as e:
        print(e)
        return {"error": str(e)}