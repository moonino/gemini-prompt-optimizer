from fastapi import APIRouter, Request, Depends
from app.services.compressor import compressor_service
from app.services.forwarder import forwarder_service
from db.database import get_db, TokenUsage
from sqlalchemy.orm import Session
import json

router = APIRouter()

@router.post("/chat/completions")
async def chat_completions(request: Request, db: Session = Depends(get_db)):
    # 1. Get request body
    body = await request.json()
    headers = dict(request.headers)
    
    # 2. Extract Last message for compression (Common pattern)
    messages = body.get("messages", [])
    original_tokens_estimate = len(json.dumps(messages)) // 4 # Rough estimate
    
    if messages:
        # For simplicity, we compress the whole message history if it's long, 
        # or just the latest system/user prompt.
        # Here we compress the entire prompt block for maximum savings.
        combined_prompt = json.dumps(messages)
        compressed_prompt_json = compressor_service.compress(combined_prompt)
        
        # Reconstruct messages from compressed JSON or use as a single string 
        # LLMLingua often outputs a string. We'll wrap it back into the messages list.
        body["messages"] = [{"role": "user", "content": compressed_prompt_json}]
    
    compressed_tokens_estimate = len(json.dumps(body["messages"])) // 4
    
    # 3. Forward to OpenAI
    response_data, status_code = await forwarder_service.forward_request(
        "chat/completions", 
        request.method, 
        body, 
        headers
    )
    
    # 4. Log savings to DB (Background-friendly)
    savings = original_tokens_estimate - compressed_tokens_estimate
    usage = TokenUsage(
        original_tokens=original_tokens_estimate,
        compressed_tokens=compressed_tokens_estimate,
        savings_tokens=savings,
        savings_percent=(savings / original_tokens_estimate * 100) if original_tokens_estimate > 0 else 0,
        model=body.get("model", "unknown")
    )
    db.add(usage)
    db.commit()
    
    return response_data
