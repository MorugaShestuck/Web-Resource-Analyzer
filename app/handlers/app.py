from fastapi import FastAPI
from app.parser import parser

app = FastAPI()


@app.get('/ping')
def ping():
    return {"message": "pong"}

@app.get('/get_pages')
def ping(url):
    p = parser.parse_urls(url)
    return {"links": p.site_links}

@app.get("/check_domain")
def check_domain(domain: str):
    return {"message": domain}