from fastapi import FastAPI

from app.analyzer.analyzer import Analyzer
from app.parser import parser

app = FastAPI()


@app.get('/ping')
def ping():
    return {"message": "pong"}

@app.get('/get_pages')
def ping(url):
    p = parser.parse_urls(url)
    return {"links": p.site_links}

@app.get("/check_url")
def check_domain(domain: str):
    a = Analyzer()
    return {"message": domain}