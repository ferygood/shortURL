# ShortURL

This is a server for generating short URL. Users first provide their original long URL and this API generate a shorter one for users. Later on, users can use this URL to visit their origin website.

## Key techniques used
- **Framework**: FastAPI
- **Database**: MongoDB
- **Container**: Docker
- **Unit test**: pytest

## Features
- Enter long URL and generate short URL
- Use short URL to redirect to long URL
- Copy the generated short URL

## Installation
1. Clone this repository
   ```bash
   git clone https://github.com/ferygood/shortURL.git
   cd shortURL
   ```
2. Create a virtual environment and install dependencies
   ```python
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## How to use
Run the app
```bash
uvicorn main:app --reload
```

After running the app, you can use tools such as cURL to interact with the api
For example:
```bash
curl -X POST "http://localhost:8000/shorten" -H "Content-Type: application/json" -d '{"long_url": "https://www.google.com"}'

```
use the shorten url. Let says you receive a short URL: abcd123,
```bash
curl -X GET "http://localhost:8000/abcd123"
```
