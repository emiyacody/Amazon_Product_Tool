import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

def main():
    # Load environment variables from .env
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    if not api_key:
        print("Error: GEMINI_API_KEY is not set in the environment or .env file.")
        sys.exit(1)
        
    print(f"Initializing Gemini API with model: {model_name}")
    
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    
    try:
        # Create the model instance
        model = genai.GenerativeModel(model_name)
        
        # Send a simple test prompt to verify connectivity
        print("Sending test request to Gemini API...")
        response = model.generate_content("Say 'Hello, Gemini API connection verified successfully!' in English.")
        
        print("\n--- Response ---")
        print(response.text.strip())
        print("----------------")
        print("\nGemini API connection test passed.")
        
    except Exception as e:
        print(f"\nError: Failed to connect to Gemini API. Details: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
