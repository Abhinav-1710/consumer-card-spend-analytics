from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any
import uuid
from datetime import datetime, timezone
import pandas as pd
import json

# Import analytics modules
from analytics_engine import CreditCardAnalytics
from sql_queries import get_all_queries

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Load data
TRANSACTIONS_PATH = ROOT_DIR / 'data' / 'transactions.csv'
CUSTOMERS_PATH = ROOT_DIR / 'data' / 'customers.csv'

# Initialize analytics engine
transactions_df = None
customers_df = None
analytics = None

def load_analytics_data():
    global transactions_df, customers_df, analytics
    try:
        transactions_df = pd.read_csv(TRANSACTIONS_PATH)
        customers_df = pd.read_csv(CUSTOMERS_PATH)
        analytics = CreditCardAnalytics(transactions_df, customers_df)
        logging.info(f"Loaded {len(transactions_df)} transactions and {len(customers_df)} customers")
    except Exception as e:
        logging.error(f"Error loading data: {e}")

# Create the main app without a prefix
app = FastAPI(title="Credit Card Analytics API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# Original routes
@api_router.get("/")
async def root():
    return {"message": "Credit Card Analytics API - Ready"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    return status_checks

# Analytics Routes
@api_router.get("/analytics/overview")
async def get_overview():
    """Get overview metrics including campaign ROI"""
    if analytics is None:
        raise HTTPException(status_code=500, detail="Analytics data not loaded")
    
    try:
        metrics = analytics.get_overview_metrics()
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analytics/spend-by-category")
async def get_spend_by_category():
    """Get spend analysis by category"""
    if analytics is None:
        raise HTTPException(status_code=500, detail="Analytics data not loaded")
    
    try:
        data = analytics.get_spend_by_category()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analytics/spend-by-region")
async def get_spend_by_region():
    """Get spend analysis by geographic region"""
    if analytics is None:
        raise HTTPException(status_code=500, detail="Analytics data not loaded")
    
    try:
        data = analytics.get_spend_by_region()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analytics/monthly-trends")
async def get_monthly_trends():
    """Get monthly spend trends"""
    if analytics is None:
        raise HTTPException(status_code=500, detail="Analytics data not loaded")
    
    try:
        data = analytics.get_monthly_trends()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analytics/campaign-effectiveness")
async def get_campaign_effectiveness():
    """Get campaign effectiveness analysis (Pre vs During vs Post)"""
    if analytics is None:
        raise HTTPException(status_code=500, detail="Analytics data not loaded")
    
    try:
        data = analytics.get_campaign_effectiveness()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analytics/customer-segmentation")
async def get_customer_segmentation():
    """Get customer segmentation analysis"""
    if analytics is None:
        raise HTTPException(status_code=500, detail="Analytics data not loaded")
    
    try:
        data = analytics.get_customer_segmentation()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analytics/recommendations")
async def get_recommendations():
    """Get recommended customer segments for future campaigns"""
    if analytics is None:
        raise HTTPException(status_code=500, detail="Analytics data not loaded")
    
    try:
        data = analytics.get_recommended_segments()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analytics/statistical-summary")
async def get_statistical_summary():
    """Get statistical summary of transactions"""
    if analytics is None:
        raise HTTPException(status_code=500, detail="Analytics data not loaded")
    
    try:
        data = analytics.get_statistical_summary()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analytics/sql-queries")
async def get_sql_queries():
    """Get all SQL queries used in the analysis"""
    try:
        queries = get_all_queries()
        return {"queries": queries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analytics/download-data")
async def download_transactions():
    """Download transactions CSV"""
    if not TRANSACTIONS_PATH.exists():
        raise HTTPException(status_code=404, detail="Data file not found")
    
    return FileResponse(
        path=str(TRANSACTIONS_PATH),
        filename="credit_card_transactions.csv",
        media_type="text/csv"
    )

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Load analytics data on startup"""
    load_analytics_data()
    logger.info("Analytics data loaded successfully")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()