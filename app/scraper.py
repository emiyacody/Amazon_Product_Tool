import re
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

class AmazonScraper:
    """
    A specialized scraper for extracting product details from Amazon pages.
    Focuses on specific CSS selectors to retrieve the minimum necessary data,
    saving tokens and costs for subsequent LLM processing.
    """
    
    def __init__(self):
        # Common User-Agents to help bypass basic bot detection
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]

    async def scrape_url(self, url: str) -> dict:
        """
        Scrapes an Amazon product URL using Playwright and returns extracted details.
        """
        async with async_playwright() as p:
            # Launch browser in headless mode
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=self.user_agents[0],
                viewport={"width": 1280, "height": 800}
            )
            page = await context.new_page()
            
            # Set extra headers to simulate a normal browser request
            await page.set_extra_http_headers({
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Referer": "https://www.google.com/"
            })
            
            try:
                print(f"Navigating to URL: {url}")
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                
                # Wait for title element to load
                try:
                    await page.wait_for_selector("#productTitle", timeout=10000)
                except Exception:
                    print("Warning: #productTitle selector not found within timeout. Attempting parsing anyway.")
                
                html_content = await page.content()
                
                # Save debug HTML if scraping fails
                if "productTitle" not in html_content:
                    with open("debug.html", "w", encoding="utf-8") as f:
                        f.write(html_content)
                    print("Saved HTML to debug.html for inspection.")
                    
                await browser.close()
                
                return self.parse_html(html_content)
                
            except Exception as e:
                await browser.close()
                print(f"Error during page navigation/scraping: {e}")
                return {"error": str(e)}

    def parse_html(self, html_content: str) -> dict:
        """
        Parses Amazon HTML and extracts core product fields.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 1. Extract Title
        title_elem = soup.select_one("#productTitle")
        title = title_elem.get_text().strip() if title_elem else ""
        
        # 2. Extract Price
        price = ""
        price_selectors = [
            "#priceInsideBuyBox_feature_div",
            "#corePrice_feature_div .a-offscreen",
            "#priceInsideBuyBox",
            "span.a-price span.a-offscreen",
            "#corePriceDisplay_desktop_feature_div .a-price span.a-offscreen"
        ]
        for selector in price_selectors:
            price_elem = soup.select_one(selector)
            if price_elem:
                text = price_elem.get_text().strip()
                if text:
                    price = text
                    break
        
        # 3. Extract Bullets / Key Features
        bullets = []
        bullets_elem = soup.select_one("#feature-bullets")
        if bullets_elem:
            items = bullets_elem.select("ul li span.a-list-item")
            for item in items:
                text = item.get_text().strip()
                # Skip helper texts like 'Make sure this fits'
                if text and not text.startswith("Make sure this fits"):
                    bullets.append(text)
        
        # Fallback bullets selector
        if not bullets and soup.select_one("#featurebullets_feature_div"):
            items = soup.select("#featurebullets_feature_div ul li")
            for item in items:
                text = item.get_text().strip()
                if text:
                    bullets.append(text)

        # 4. Extract Product Description
        description = ""
        desc_elem = soup.select_one("#productDescription")
        if desc_elem:
            description = desc_elem.get_text().strip()
        else:
            desc_elem = soup.select_one("#productDescription_feature_div")
            if desc_elem:
                description = desc_elem.get_text().strip()
                
        # Clean description whitespace
        description = re.sub(r'\s+', ' ', description)
        
        # 5. Extract Product Specs
        specs = {}
        tech_specs = soup.select("#prodDetails tr")
        for row in tech_specs:
            key_elem = row.select_one("th")
            val_elem = row.select_one("td")
            if key_elem and val_elem:
                key = key_elem.get_text().strip()
                val = val_elem.get_text().strip()
                key = re.sub(r'\s+', ' ', key)
                val = re.sub(r'\s+', ' ', val)
                if key and val:
                    specs[key] = val
                    
        # Fallback specs (bullet format)
        if not specs:
            detail_bullets = soup.select("#detailBullets_feature_div ul li span.a-list-item")
            for item in detail_bullets:
                text = item.get_text().strip()
                parts = text.split(":")
                if len(parts) >= 2:
                    key = parts[0].strip()
                    val = ":".join(parts[1:]).strip()
                    key = re.sub(r'\s+', ' ', key)
                    val = re.sub(r'\s+', ' ', val)
                    # Filter out garbage characters (like visual bullet characters)
                    key = re.sub(r'[^\w\s]', '', key).strip()
                    if key and val:
                        specs[key] = val

        # 6. Extract Category / Breadcrumbs
        category = ""
        breadcrumbs = soup.select("#wayfinding-breadcrumbs_container ul li span.a-list-item a")
        if breadcrumbs:
            cats = [b.get_text().strip() for b in breadcrumbs if b.get_text().strip()]
            category = " > ".join(cats)

        return {
            "title": title,
            "price": price,
            "category": category,
            "bullets": bullets,
            "description": description,
            "specs": specs
        }
