import os
import json
import sys
from dotenv import load_dotenv
from app.analyzer import ProductAnalyzer

def main():
    # Reconfigure stdout to use UTF-8 to avoid encoding errors on Windows terminal
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        
    # Load environment variables
    load_dotenv()
    
    # Check if mock product file exists
    mock_file = "mock_product.json"
    if not os.path.exists(mock_file):
        print(f"Error: '{mock_file}' not found. Please run verify_scraper.py first to generate it.")
        sys.exit(1)
        
    print(f"Loading cached product details from: {mock_file}")
    with open(mock_file, "r", encoding="utf-8") as f:
        product_data = json.load(f)
        
    print("Initializing ProductAnalyzer...")
    try:
        analyzer = ProductAnalyzer()
    except Exception as e:
        print(f"Initialization failed: {e}")
        sys.exit(1)
        
    print("Calling Gemini API for analysis and script generation...")
    result = analyzer.analyze(product_data)
    
    if "error" in result:
        print(f"Analysis failed: {result['error']}")
        sys.exit(1)
        
    # Display the results
    print("\n================ AI Analysis Results ================")
    print(f"Product Name: {result.get('product_name')}")
    print(f"Category:     {result.get('category')}")
    print(f"Price:        {result.get('price')}")
    print(f"Core Features: {', '.join(result.get('core_features', []))}")
    print("\n--- Target Audience & Positioning ---")
    print(f"Target Users:      {', '.join(result.get('target_users', []))}")
    print(f"Usage Scenarios:   {', '.join(result.get('usage_scenarios', []))}")
    print(f"User Pain Points:  {', '.join(result.get('user_pain_points', []))}")
    print(f"Selling Points:    {', '.join(result.get('core_selling_points', []))}")
    print("\n--- Video Script Generation ---")
    print(f"Hook (First 5s):   {result.get('video_hook')}")
    print(f"Body:              {result.get('video_body')}")
    print(f"CTA:               {result.get('video_cta')}")
    print(f"\n[Full Oral Script]:\n{result.get('full_script')}")
    print("=====================================================")
    
    # Run Automated AI Quality Checks
    print("\n--- Running AI Quality Checks ---")
    
    # 1. Schema validation
    required_keys = [
        "product_name", "category", "price", "core_features", "target_users", 
        "usage_scenarios", "user_pain_points", "core_selling_points", 
        "video_hook", "video_body", "video_cta", "full_script"
    ]
    missing_keys = [k for k in required_keys if k not in result]
    if missing_keys:
        print(f"FAIL: Missing keys in JSON output: {missing_keys}")
        sys.exit(1)
    else:
        print("PASS: Schema check passed. All required fields are present.")
        
    # 2. Word count check (English words limit: 150)
    full_script = (result.get("full_script") or "").strip()
    word_count = len(full_script.split()) if full_script else 0
    print(f"Full Script Word Count: {word_count} words (limit: 150)")
    if word_count > 150:
        print(f"FAIL: Voiceover script exceeds the 150-word limit.")
        sys.exit(1)
    else:
        print("PASS: Voiceover script word count is within the 150-word limit.")
        
    # 3. Hook existence check
    hook = result.get("video_hook", "")
    if len(hook.strip()) == 0:
        print("FAIL: The video hook is empty.")
        sys.exit(1)
    else:
        print(f"PASS: Video hook is present and populated.")
        
    print("\nAI Analyzer quality verification completed successfully!")

if __name__ == "__main__":
    main()
