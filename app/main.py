from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.get("/health", response_class=PlainTextResponse)
def health() -> str:
    return "ok"


@app.get("/hello", response_class=PlainTextResponse)
def hello() -> str:
    return "hello"
