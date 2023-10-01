import logging
from typing import Dict, List

from fastapi import FastAPI
from pydantic import BaseModel

from app.analyzer.analyzer import Analyzer
from app.parser import parser, ContentParser
from app.utils.Cache import Cache
from app.utils.hash_table import HashTable

app = FastAPI()

keywords, categories = HashTable(), HashTable()
keywords.load("app/data/data.json")
categories.load("app/data/categories.json")
cache = Cache(cache_file="app/data/cache.json")
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class GetPagesRequest(BaseModel):
    url: str
    depth: int = 1


class GetPagesResponse(BaseModel):
    code: int
    data: Dict[str, List[str]]


@app.get('/ping')
async def ping():
    """
    Ping endpoint to check if the server is running.
    """
    return {"message": "pong"}


@app.get('/get_pages', response_model=GetPagesResponse)
async def get_pages(request_data: GetPagesRequest):
    """
    Retrieve web pages starting from a given URL and a specified depth.

    Args:
        url (str): The starting URL.
        depth (int): The depth to crawl (default is 1).

    Returns:
        Dict: A dictionary containing the links retrieved.
        :param request_data:
    """
    try:
        url = request_data.url
        depth = request_data.depth
        p = parser.parse_urls(url, depth)
        links = p.site_links[:depth]
        return {"code": 200, "data": {"links": links}}
    except Exception as e:
        error_message = f"Error: {str(e)}"
        logging.error(error_message)
        return {"code": 500, "data": {"error": error_message}}


@app.get("/check_url")
async def check_url(url: str, depth: int = 1):
    """
    Check a single URL for categories and themes.

    Args:
        url (str): The URL to check.
        depth (int): The depth for analysis (default is 1).

    Returns:
        Dict: A dictionary containing the categories and themes found.
    """
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
        if depth == 1:
            return {"category": categories_resp[0], "theme": themes_resp[0]}
        return {"code": 200, "data": {"categories": categories_resp, "themes": themes_resp}}
    except Exception as e:
        error_message = f"Error: {str(e)}"
        logging.error(error_message)
        return {"code": 500, "data": {"error": error_message}}


@app.post("/check_urls")
async def check_urls(request_data: Dict[str, List[str]], depth: int = 1):
    """
    Check multiple URLs for categories and themes.

    Args:
        request_data (Dict[str, List[str]]): JSON data with a list of URLs.
        depth (int): The depth for analysis (default is 1).

    Returns:
        Dict: A dictionary containing the results for each URL.
    """
    try:
        urls = request_data.get("urls", [])
        results = []

        for url in urls:
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

            if depth == 1:
                result = {"url": url, "category": categories_resp[0], "theme": themes_resp[0]}
            else:
                result = {"url": url, "categories": categories_resp, "themes": themes_resp}
            results.append(result)

        return {"code": 200, "data": results}
    except Exception as e:
        error_message = f"Error: {str(e)}"
        logging.error(error_message)
        return {"code": 500, "data": {"error": error_message}}


@app.get('/check_domain')
async def check_domain(url: str, depth: int = 1):
    """
    Check a domain for categories and themes based on its linked pages.

    Args:
        url (str): The URL of the domain.
        depth (int): The depth for analysis (default is 1).

    Returns:
        Dict: A dictionary containing the categories and themes found in the domain.
    """
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
        error_message = f"Error: {str(e)}"
        logging.error(error_message)
        return {"code": 500, "data": {"error": error_message}}
