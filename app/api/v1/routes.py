from fastapi import APIRouter, Request, Depends
from app.services.compressor import compressor_service
from app.services.forwarder import forwarder_service
from db.database import get_db, TokenUsage
from sqlalchemy.orm import Session
from app.core.config import settings
import json

router = APIRouter()

@router.post("/models/{model}:generateContent")
async def generate_content(model: str, request: Request, db: Session = Depends(get_db)):
    # 1. Get request body
    body = await request.json()
    headers = dict(request.headers)
    
    # 2. Extract contents for compression
    contents = body.get("contents", [])
    origin_tokens = 0
    compressed_tokens = 0
    
    if contents:
        # Extract text from the structured Gemini payload
        extracted_texts = []
        for turn in contents:
            if "parts" in turn:
                for part in turn["parts"]:
                    if "text" in part:
                        extracted_texts.append(part["text"])
        
        combined_prompt = "\n".join(extracted_texts) if extracted_texts else json.dumps(contents)
        
        compression_result = compressor_service.compress(combined_prompt)
        compressed_text = compression_result["compressed_prompt"]
        origin_tokens = compression_result["origin_tokens"]
        compressed_tokens = compression_result["compressed_tokens"]
        
        # Replace contents with a single user turn containing compressed text
        body["contents"] = [
            {
                "role": "user",
                "parts": [{"text": compressed_text}]
            }
        ]
    else:
        origin_tokens = 0
        compressed_tokens = 0
    
    # 3. Forward to Gemini API
    # Path format: models/{model}:generateContent
    path = f"models/{model}:generateContent"
    response_data, status_code = await forwarder_service.forward_request(
        path, 
        request.method, 
        body, 
        headers
    )
    
    # 4. Log savings to DB
    savings = origin_tokens - compressed_tokens
    
    # Model-specific pricing calculation
    price_per_1m = settings.GEMINI_MODEL_PRICING.get(model)
    if not price_per_1m:
        for key in settings.GEMINI_MODEL_PRICING:
            if key in model:
                price_per_1m = settings.GEMINI_MODEL_PRICING[key]
                break
    
    price_per_1m = price_per_1m or settings.GEMINI_MODEL_PRICING["default"]
    savings_usd = (max(0, savings) / 1000000) * price_per_1m

    usage = TokenUsage(
        original_tokens=origin_tokens,
        compressed_tokens=compressed_tokens,
        savings_tokens=max(0, savings),
        savings_percent=(max(0, savings) / origin_tokens * 100) if origin_tokens > 0 else 0,
        model=model,
        savings_usd=savings_usd
    )
    db.add(usage)
    db.commit()
    
    return response_data
