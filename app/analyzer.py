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
        
        # Mapping copywriting styles to specific prompt guidance
        style_prompts = {
            "enthusiastic": "激情带货风：用极具煽动性和热情的口吻，强调核心痛点、震撼效果和立即行动的号召（多使用感叹号，如“家人们冲它！”“买它就对了！”）。",
            "professional": "专业客观风：用冷静、客观、理性的测评人语气，侧重于技术参数、材质工艺、真实使用感受，通过逻辑和对比说服观众。",
            "storytelling": "生活种草风：用亲近、平实、闺蜜/老友日常分享的口吻，从具体生活痛点场景切入，像讲故事一样自然带出产品的使用体验。",
            "humorous": "幽默搞笑风：用风趣、吐槽、自嘲的幽默口吻，放大日常使用中的尴尬或烦恼场景，将产品作为搞笑反转后的“救星”引出。"
        }
        style_instruction = style_prompts.get(style, style_prompts["enthusiastic"])
        
        # Prepare the prompt detailing constraints and instructions
        prompt = f"""
        You are a seasoned product marketing expert and viral short video copywriter.
        Analyze the following Amazon product data and output a structured analysis.
        
        --- Scraped Product Data ---
        Product Title: {product_data.get('title', '')}
        Price: {product_data.get('price', '')}
        Category: {product_data.get('category', '')}
        Bullet Features: {json.dumps(product_data.get('bullets', []), ensure_ascii=False)}
        Description: {product_data.get('description', '')}
        Technical Specifications: {json.dumps(product_data.get('specs', {}), ensure_ascii=False)}
        ----------------------------
        
        Instructions:
        1. Extract the product name, category, price, and core features.
        2. Deduce target users, realistic usage scenarios, core user pain points, and key selling points.
        3. Write a short video oral script in Chinese:
           - The complete script ('full_script') MUST be 150 Chinese characters or less in total.
           - Write the script in the following specific style: {style_instruction}
           - The script MUST begin with a powerful hook in the first 5 seconds ('video_hook') to grab the user's attention.
           - Keep the tone colloquial, energetic, and natural, matching the style of popular short-form videos.
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
