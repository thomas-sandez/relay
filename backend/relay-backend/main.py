from fastapi import FastAPI

from database import Base, engine
from events import models as events_models  # noqa: F401  (registra el modelo)
from events.router import router as events_router
from webhook import models as webhook_models  # noqa: F401  (registra el modelo)
from webhook.router import router as webhook_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(webhook_router)
app.include_router(events_router)


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/health')
def health():
    return {'status': 'ok'}