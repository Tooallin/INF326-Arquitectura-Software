from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from threads.services import *

router = APIRouter()

class ThreadSchema(BaseModel):
    id: str
    channel_id: str
    title: str
    created_by: str
    status: str
    meta: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

@router.get("/id/{thread_id}", response_model=List[ThreadSchema])
def read_id(thread_id: str):
    return get_by_id(thread_id)

@router.get("/author/{created_by}", response_model=List[ThreadSchema])
def read_author(created_by: str):
    return get_by_author(created_by)

@router.get("/daterange", response_model=List[ThreadSchema])
def read_date_range(start_date: datetime, end_date: datetime):
    return get_by_date_range(start_date, end_date)

@router.get("/keyword/{thread_keyword}", response_model=List[ThreadSchema])
def read_keyword(thread_keyword: str):
    return get_by_keyword(thread_keyword)

@router.get("/status/{status}", response_model=List[ThreadSchema])
def read_keyword(status: str):
    return get_by_status(status)
