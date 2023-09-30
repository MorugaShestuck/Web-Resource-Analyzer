from fastapi import FastAPI

app = FastAPI()

@app.get('/ping')
def ping():
    return {"message": "pong"}

@app.get("/check_domain")
def check_domain(domain: str):
    return {"message": domain}