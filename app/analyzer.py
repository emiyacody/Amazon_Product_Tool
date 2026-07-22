import os
import json
import google.generativeai as genai
from app.schemas import ProductAnalysisSchema

class ProductAnalyzer:
    """
    Handles AI analysis and copywriting generation for products using the Gemini API.
    Consolidates extraction, analysis, and script writing into a single API request
    to minimize costs and token usage.
    """
    
    def __init__(self):
        # Configure Gemini API using environment variables
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")
            
        genai.configure(api_key=self.api_key)
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

    def analyze(self, product_data: dict, style: str = "enthusiastic") -> dict:
        """
        Sends product data to Gemini API and returns structured JSON analysis.
        """
        model = genai.GenerativeModel(self.model_name)
        
        # Mapping copywriting styles to specific prompt guidance in English for US market
        style_prompts = {
            "enthusiastic": "High-Energy Hype / TikTok Viral Tone: Energetic, enthusiastic, and persuasive. Uses engaging phrases like 'You guys need to see this!', 'Stop scrolling!', and strong calls to action.",
            "professional": "Tech & Product Reviewer Tone: Calm, articulate, and objective. Focuses on specs, build quality, real-world performance, and logical comparisons.",
            "storytelling": "Relatable Lifestyle / UGC Vlog Tone: Warm, personal, and conversational. Feels like a friend sharing an honest recommendation from an everyday struggle or routine.",
            "humorous": "Witty & Satirical Tone: Humorous, self-deprecating, and funny. Highlights everyday annoyances before revealing the product as the ultimate unexpected hero."
        }
        style_instruction = style_prompts.get(style, style_prompts["enthusiastic"])
        
        # Prepare the prompt detailing constraints and instructions
        prompt = f"""
        You are an expert US e-commerce product marketer and viral short-form video copywriter (TikTok, Instagram Reels, YouTube Shorts).
        Analyze the following Amazon product data and output a structured analysis tailored for the US market.
        
        --- Scraped Product Data ---
        Product Title: {product_data.get('title', '')}
        Price: {product_data.get('price', '')}
        Category: {product_data.get('category', '')}
        Bullet Features: {json.dumps(product_data.get('bullets', []), ensure_ascii=False)}
        Description: {product_data.get('description', '')}
        Technical Specifications: {json.dumps(product_data.get('specs', {}), ensure_ascii=False)}
        ----------------------------
        
        Instructions:
        1. Extract the product name, category, price, and core features in concise English.
        2. Identify target users, realistic usage scenarios, core user pain points, and key unique selling points for US consumers.
        3. Write a high-converting short video voiceover script in natural American English:
           - The complete script ('full_script') MUST be 150 words or less in total (approx. 45-60 seconds when spoken).
           - Write the script in the following specific style: {style_instruction}
           - The script MUST begin with a powerful hook in the first 5 seconds ('video_hook') to immediately stop the scroll.
           - Keep the language natural, punchy, conversational, and trendy for US social media audiences.
           - Provide the hook, body, and CTA separately, as well as combined in 'full_script'.
        """
        
        try:
            # Query Gemini API with JSON schema enforcement
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=ProductAnalysisSchema,
                    temperature=0.7
                )
            )
            
            # Parse the JSON string from the response
            analysis_result = json.loads(response.text)
            return analysis_result
            
        except Exception as e:
            print(f"Error during Gemini API call: {e}")
            return {"error": str(e)}
