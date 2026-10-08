from fastapi import FastAPI

from webhook.router import router as webhook_router

app = FastAPI()
app.include_router(webhook_router)

@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.get('/health')
def health():
    return {'status': 'ok'}