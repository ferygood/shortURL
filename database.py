from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.short_url_db
collection = db.urls
