from pydantic import BaseModel, Field
from typing import List

class ProductAnalysisSchema(BaseModel):
    """
    Pydantic schema defining the structured output from Gemini for the English / US market.
    All fields for analysis and script generation must be returned in clear, engaging English.
    """
    product_name: str = Field(description="Name of the product in concise English.")
    category: str = Field(description="Product category or classification in English.")
    price: str = Field(description="Price of the product with currency symbol (e.g., '$29.99'), or 'N/A' if not available.")
    core_features: List[str] = Field(description="List of key technical features or specifications in English.")
    
    target_users: List[str] = Field(description="Target audience groups or customer personas in English.")
    usage_scenarios: List[str] = Field(description="Typical usage scenarios or contexts for the product in English.")
    user_pain_points: List[str] = Field(description="Core problems or frustrations that the product addresses for users in English.")
    core_selling_points: List[str] = Field(description="Key unique selling propositions (USPs) and differentiators in English.")
    
    video_hook: str = Field(description="An attention-grabbing hook for the first 5 seconds of the video in English.")
    video_body: str = Field(description="The main body of the voiceover script highlighting features and benefits in English.")
    video_cta: str = Field(description="A short call to action (CTA) at the end of the script in English.")
    full_script: str = Field(description="The complete unified voiceover script combining hook, body, and CTA in English. MUST be 150 words or less in total.")
