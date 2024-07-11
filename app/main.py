from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import string
import random

app = FastAPI()

# configure MongoDB
client = MongoClient('mongodb://mongo:27017/')
db = client.url_shortener
collection = db.urls

class URL(BaseModel):
    long_url: str

# generate short url from user input
def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(length))
    return short_url

@app.post("/shorten")
async def shorten_url(url: URL):
    short_url = generate_short_url()
    collection.insert_one({'short_url': short_url, 'long_url': url.long_url})
    return {"short_url": short_url}

@app.get("/{short_url}")
async def redirect_url(short_url: str):
    url_data = collection.find_one({'short_url': short_url})
    if url_data:
        return {"long_url": url_data['long_url']}
    raise HTTPException(status_code=404, detail="URL not found")