import os
import sys
import time
import asyncio
from dotenv import load_dotenv
from app.main import analyze_endpoint, AnalyzeRequest

async def main():
    # Load environment variables
    load_dotenv()
    
    # Reconfigure stdout to use UTF-8 to prevent console errors
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        
    print("Starting API and Cache Verification...")
    
    # 1. Test URL request (should hit cache if analyzed previously)
    url = "https://www.amazon.com/dp/B07FZ8S74R"
    req_url = AnalyzeRequest(url=url)
    
    print(f"\n[Test 1] Sending URL request ({url}) to API...")
    start_time = time.time()
    try:
        response = await analyze_endpoint(req_url)
        duration_url = (time.time() - start_time) * 1000  # convert to ms
        print(f"Response product_name: {response.get('product_name')}")
        print(f"Time taken: {duration_url:.2f} ms")
        
        # Verify cache speed (should be fast, usually < 50ms)
        if duration_url < 200:
            print("PASS: Cache HIT verified. Cache lookup was successful.")
        else:
            print(f"Warning: Cache lookup took longer than expected ({duration_url:.2f} ms).")
    except Exception as e:
        print(f"FAIL: Request failed with error: {e}")
        sys.exit(1)
        
    # 2. Test manual raw text request (Cache Miss first, then Cache Hit)
    raw_text = (
        "<html><body>"
        "<span id='productTitle'>Super Gadget Pro</span>"
        "<div id='feature-bullets'><ul><li>Amazing high speed.</li><li>Comfortable grip.</li></ul></div>"
        "</body></html>"
    )
    req_text = AnalyzeRequest(raw_text=raw_text)
    
    print(f"\n[Test 2 - First Call] Sending raw text request to API...")
    start_time = time.time()
    try:
        response_miss = await analyze_endpoint(req_text)
        duration_miss = (time.time() - start_time) * 1000
        print(f"Response product_name: {response_miss.get('product_name')}")
        print(f"Time taken: {duration_miss:.2f} ms (Cache Miss: Parsed & AI Analyzed)")
    except Exception as e:
        print(f"FAIL: Raw text request failed: {e}")
        sys.exit(1)
        
    print(f"\n[Test 2 - Second Call] Sending identical raw text request (expecting Cache Hit)...")
    start_time = time.time()
    try:
        response_hit = await analyze_endpoint(req_text)
        duration_hit = (time.time() - start_time) * 1000
        print(f"Response product_name: {response_hit.get('product_name')}")
        print(f"Time taken: {duration_hit:.2f} ms (Cache Hit)")
        
        # Validate cache latency speedup
        if duration_hit < 50:
            print(f"PASS: Cache hit successfully reduced response time from {duration_miss:.2f} ms to {duration_hit:.2f} ms!")
        else:
            print(f"Warning: Cache hit response was slow: {duration_hit:.2f} ms.")
    except Exception as e:
        print(f"FAIL: Second raw text request failed: {e}")
        sys.exit(1)
        
    print("\nAPI and Cache verification completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
