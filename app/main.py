from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.api.v1.routes import router as v1_router
from db.database import init_db, get_db, TokenUsage
from sqlalchemy.orm import Session
from sqlalchemy import func
import os

app = FastAPI(title="Prompt Optimizer Proxy")

# Initialize DB on Startup
@app.on_event("startup")
def on_startup():
    if not os.path.exists("./db"):
        os.makedirs("./db")
    init_db()

# Include API Routes
app.include_router(v1_router, prefix="/v1")

templates = Jinja2Templates(directory="app/templates")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    # Aggregate stats
    stats = db.query(
        func.sum(TokenUsage.original_tokens).label("total_original"),
        func.sum(TokenUsage.compressed_tokens).label("total_compressed"),
        func.sum(TokenUsage.savings_tokens).label("total_savings")
    ).first()
    
    logs = db.query(TokenUsage).order_by(TokenUsage.timestamp.desc()).limit(10).all()
    
    avg_savings = 0
    if stats and stats.total_original and stats.total_original > 0:
        avg_savings = round((stats.total_savings / stats.total_original) * 100, 2)

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "stats": stats,
        "avg_savings": avg_savings,
        "logs": logs
    })

@app.get("/")
async def root():
    return {"message": "Prompt Optimizer Proxy is running. Use /v1 for API and /dashboard for monitoring."}
