from fastapi import FastAPI, HTTPException
from helper import helper_functions
app = FastAPI()

@app.get("/")
def root():
    return {"result":"hello world"}

@app.post("/market_sentiment")
def market_sentiment_endpoint(keywords_list: list[str]):
    try:
        ans = helper_functions.market_sentiment(keywords_list)
        return {"result": ans}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/important_conversations")
def important_conversations_endpoint(keywords_list: list[str]):
    try:
        ans = helper_functions.important_conversations(keywords_list)
        return {"result": ans}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/latest_conversations")
def latest_conversations_endpoint(keywords_list: list[str]):
    try:
        ans = helper_functions.latest_conversations(keywords_list)
        return {"result": ans}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/correlated_keywords")
def correlated_keywords_endpoint(keywords: list[str]):
    try:
        ans = helper_functions.correlated_keywords(keywords)
        return {"result": ans}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
