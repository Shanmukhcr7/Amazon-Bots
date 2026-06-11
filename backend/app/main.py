from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import api_router

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router.router, prefix="/api")

@app.on_event("startup")
def on_startup():
    from app.core.init_db import init_db
    init_db()
    
    from apscheduler.schedulers.background import BackgroundScheduler
    from app.tasks.scraper import scrape_amazon_dummy
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_amazon_dummy, 'interval', minutes=60)
    scheduler.start()
    
    # Run once at startup
    scrape_amazon_dummy()

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
