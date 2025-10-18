from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from threads.services import *

router = APIRouter()

class Thread(BaseModel):
    id: str
    title: str
    content: str
    author_id: str
    channel_id: str
    creation_date: datetime
    tags: Optional[list[str]] = None
    category: Optional[str] = None


@router.get("/id/{thread_id}")
def read_id(thread_id: str):
    return get_by_id(thread_id)

@router.get("/category/{thread_category}")
def read_category(thread_category: str):
    return get_by_category(thread_category)

@router.get("/author/{thread_author}")
def read_author(thread_author: str):
    return get_by_author(thread_author)

@router.get("/daterange")
def read_date_range(start_date: datetime, end_date: datetime):
    return get_by_date_range(start_date, end_date)

@router.get("/tag/{thread_tag}")
def read_tag(thread_tag: str):
    return get_by_tag(thread_tag)

@router.get("/keyword/{thread_keyword}")
def read_keyword(thread_keyword: str):
    return get_by_keyword(thread_keyword)
