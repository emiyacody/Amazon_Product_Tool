import sys
import json
import asyncio
from app.scraper import AmazonScraper

async def main():
    # Ensure URL argument is provided
    if len(sys.argv) < 2:
        print("Usage: python verify_scraper.py <Amazon_Product_URL>")
        sys.exit(1)
        
    url = sys.argv[1]
    print(f"Starting scraper test for URL: {url}")
    
    scraper = AmazonScraper()
    result = await scraper.scrape_url(url)
    
    if "error" in result:
        print(f"Scraping failed: {result['error']}")
        sys.exit(1)
        
    # Print summary of extracted info
    print("\n--- Extracted Product Summary ---")
    print(f"Title: {result.get('title', 'N/A')}")
    print(f"Price: {result.get('price', 'N/A')}")
    print(f"Category: {result.get('category', 'N/A')}")
    print(f"Number of Bullet Features: {len(result.get('bullets', []))}")
    print(f"Description Length: {len(result.get('description', ''))} characters")
    print(f"Number of Technical Specs: {len(result.get('specs', {}))}")
    print("---------------------------------")
    
    # Save output to a local JSON file for the analyzer test to use offline
    output_file = "mock_product.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    print(f"\nSaved scraped details to '{output_file}' for subsequent AI verification.")
    
    # Basic validation checks
    if not result.get("title"):
        print("Warning: Title is empty. Scraping might have been blocked or page layout has changed.")
    else:
        print("Scraper verification completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
