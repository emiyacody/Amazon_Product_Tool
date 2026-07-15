import os
import hashlib
import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import edge_tts

# Load environment variables at startup
load_dotenv()

from app.scraper import AmazonScraper
from app.analyzer import ProductAnalyzer

app = FastAPI(title="Amazon Product Analyzer API")

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up local cache directory
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

class AnalyzeRequest(BaseModel):
    url: Optional[str] = None
    raw_text: Optional[str] = None
    style: Optional[str] = "enthusiastic"

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "zh-CN-XiaoxiaoNeural"

def get_cache_path(key: str) -> str:
    return os.path.join(CACHE_DIR, f"{key}.json")

def get_md5(data: str) -> str:
    return hashlib.md5(data.encode("utf-8")).hexdigest()

@app.post("/api/analyze")
async def analyze_endpoint(req: AnalyzeRequest):
    """
    Analyzes Amazon product info.
    Supports dual-input: scraping by URL or direct parsing of pasted raw HTML text.
    """
    if not req.url and not req.raw_text:
        raise HTTPException(status_code=400, detail="Either 'url' or 'raw_text' must be provided.")
        
    # Generate content cache key based on URL or content hash
    content_key = get_md5(req.url) if req.url else get_md5(req.raw_text)
    style_name = req.style or "enthusiastic"
    
    # 1. Check final analysis cache
    analysis_key = f"analysis_{content_key}_{style_name}"
    analysis_cache_path = os.path.join(CACHE_DIR, f"{analysis_key}.json")
    
    if os.path.exists(analysis_cache_path):
        print(f"Analysis Cache HIT for key: {analysis_key}")
        try:
            with open(analysis_cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to read analysis cache file: {e}")
            
    # 2. Check scraped data cache to avoid fetching Amazon page again
    scraped_key = f"scraped_{content_key}"
    scraped_cache_path = os.path.join(CACHE_DIR, f"{scraped_key}.json")
    
    scraped_data = {}
    if os.path.exists(scraped_cache_path):
        print(f"Scraped Data Cache HIT for key: {scraped_key}")
        try:
            with open(scraped_cache_path, "r", encoding="utf-8") as f:
                scraped_data = json.load(f)
        except Exception as e:
            print(f"Failed to read scraped cache file: {e}")
            
    # 3. If scraped data is not cached, fetch it
    if not scraped_data:
        if req.url:
            print(f"Scraped Data Cache MISS. Scraping URL: {req.url}")
            scraper = AmazonScraper()
            scraped_data = await scraper.scrape_url(req.url)
            if "error" in scraped_data:
                raise HTTPException(status_code=500, detail=f"Scraping failed: {scraped_data['error']}")
        else:
            print("Scraped Data Cache MISS. Parsing raw HTML text input.")
            scraper = AmazonScraper()
            scraped_data = scraper.parse_html(req.raw_text)
            
        # Validate parsed data quality: requires at least a title or some features
        if not scraped_data.get("title") and not scraped_data.get("bullets"):
            raise HTTPException(
                status_code=422, 
                detail="Failed to extract product details. Please verify the URL or pasted content."
            )
            
        # Save scraped data in cache
        try:
            with open(scraped_cache_path, "w", encoding="utf-8") as f:
                json.dump(scraped_data, f, indent=4, ensure_ascii=False)
            print(f"Scraped data cache saved at: {scraped_cache_path}")
        except Exception as e:
            print(f"Failed to save scraped cache file: {e}")
            
    # 4. Invoke Gemini analyzer with requested style
    print(f"Invoking Gemini analyzer with style: {style_name}...")
    analyzer = ProductAnalyzer()
    analysis_result = analyzer.analyze(scraped_data, style=style_name)
    
    if "error" in analysis_result:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {analysis_result['error']}")
        
    # 5. Save the analysis result in local cache
    try:
        with open(analysis_cache_path, "w", encoding="utf-8") as f:
            json.dump(analysis_result, f, indent=4, ensure_ascii=False)
        print(f"Analysis result cache saved at: {analysis_cache_path}")
    except Exception as e:
        print(f"Failed to save analysis cache file: {e}")
        
    return analysis_result

@app.post("/api/tts")
async def tts_endpoint(req: TTSRequest):
    """
    Generates text-to-speech audio stream using Microsoft Edge Neural TTS.
    """
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")
    
    try:
        communicate = edge_tts.Communicate(req.text, req.voice)
        
        async def audio_generator():
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    yield chunk["data"]
                    
        return StreamingResponse(audio_generator(), media_type="audio/mpeg")
    except Exception as e:
        print(f"TTS generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")

# Serve static frontend UI (if 'static' folder exists)
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")
elif os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
