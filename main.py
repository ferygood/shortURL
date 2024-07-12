from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pymongo.errors import ServerSelectionTimeoutError
from models import URL, ShortURL
from database import collection
from utils import generate_short_url

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_db_client():
    try:
        collection.database.client.admin.command('ismaster')
        print("MongoDB connected")
    except ServerSelectionTimeoutError as e:
        print(f"MongoDB connection error: {e}")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    urls = list(collection.find({}, {"_id": 0}))
    return templates.TemplateResponse("index.html", {"request": request, "urls": urls})

@app.post("/shorten", response_class=HTMLResponse)
async def shorten_url(request: Request, long_url: str = Form(...)):
    short_url = "https://surl/" + generate_short_url()
    url_data = {
        "short_url": short_url,
        "long_url": long_url
    }
    collection.insert_one(url_data)
    urls = list(collection.find({}, {"_id": 0}))
    return templates.TemplateResponse("index.html", {"request": request, "urls": urls, "short_url": short_url, "long_url": long_url})

@app.post("/api/shorten", response_model=ShortURL)
async def api_shorten_url(url: URL):
    short_url = "https://surl/" + generate_short_url()
    url_data = {
        "short_url": short_url,
        "long_url": url.long_url
    }
    collection.insert_one(url_data)
    return url_data

@app.get("/{short_url}", response_model=URL)
async def redirect_url(short_url: str):
    url_data = collection.find_one({"short_url": "https://surl/" + short_url})
    if url_data is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return URL(long_url=url_data["long_url"])

@app.get("/urls", response_class=JSONResponse)
async def get_all_urls():
    urls = list(collection.find({}, {"_id": 0}))
    return JSONResponse(content=urls)
