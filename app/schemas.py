from pydantic import BaseModel, Field
from typing import List, Dict

class ProductAnalysisSchema(BaseModel):
    """
    Pydantic schema defining the structured output from Gemini.
    Fields for analysis and script generation are requested in Chinese.
    """
    product_name: str = Field(description="Name of the product, translated to Chinese if appropriate.")
    category: str = Field(description="Product category or classification (in Chinese).")
    price: str = Field(description="Price of the product, or 'N/A' if not available.")
    core_features: List[str] = Field(description="List of key technical features or specs extracted from the product info.")
    
    target_users: List[str] = Field(description="Target audience groups or customer personas (in Chinese).")
    usage_scenarios: List[str] = Field(description="Typical usage scenarios or contexts for the product (in Chinese).")
    user_pain_points: List[str] = Field(description="Core problems or frustrations that the product addresses for users (in Chinese).")
    core_selling_points: List[str] = Field(description="Key selling propositions and differentiators (in Chinese).")
    
    video_hook: str = Field(description="An attention-grabbing hook for the first 5 seconds of the video (in Chinese).")
    video_body: str = Field(description="The main body of the oral script discussing features and benefits (in Chinese).")
    video_cta: str = Field(description="A short call to action at the end of the script (in Chinese).")
    full_script: str = Field(description="The complete unified oral script combining hook, body, and CTA. MUST be 150 Chinese characters or less in total.")
