from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
import json

app = FastAPI()

@app.get("/scrape")
async def scrape(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", {"id": "__NEXT_DATA__", "type": "application/json"})

        if script_tag:
            return json.loads(script_tag.string)  # Send JSON directly
        else:
            raise HTTPException(status_code=404, detail="Script tag not found")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
