from elastic_search.connection import get_client
from threads.mapping import index_name

def get_by_id(thread_id):
    client = get_client()
    body = {
        "query": {
            "term": {
                "id": thread_id
            }
        }
    }
    result = client.search(index=index_name, body=body)
    hits = [
        {
            "id": hit["_id"],
            "channel_id": hit["_source"]["channel_id"],
            "title": hit["_source"]["title"],
            "created_by": hit["_source"]["created_by"],
            "status": hit["_source"].get("status"),
            "meta": hit["_source"].get("meta"),
            "created_at": hit["_source"]["created_at"],
            "updated_at": hit["_source"].get("updated_at"),
            "deleted_at": hit["_source"].get("deleted_at"),
        }
        for hit in result["hits"]["hits"]
    ]
    return hits
    
def get_by_author(author_id):
    client = get_client()
    body = {
        "query": {
            "term": {
                "created_by": author_id
            }
        }
    }
    result = client.search(index=index_name, body=body)
    hits = [
        {
            "id": hit["_id"],
            "channel_id": hit["_source"]["channel_id"],
            "title": hit["_source"]["title"],
            "created_by": hit["_source"]["created_by"],
            "status": hit["_source"].get("status"),
            "meta": hit["_source"].get("meta"),
            "created_at": hit["_source"]["created_at"],
            "updated_at": hit["_source"].get("updated_at"),
            "deleted_at": hit["_source"].get("deleted_at"),
        }
        for hit in result["hits"]["hits"]
    ]
    return hits

def get_by_date_range(start_date, end_date):
    client = get_client()
    body = {
        "query": {
            "range": {
                "created_at": {
                    "gte": start_date,
                    "lt": end_date
                }
            }
        }
    }
    result = client.search(index=index_name, body=body)
    hits = [
        {
            "id": hit["_id"],
            "channel_id": hit["_source"]["channel_id"],
            "title": hit["_source"]["title"],
            "created_by": hit["_source"]["created_by"],
            "status": hit["_source"].get("status"),
            "meta": hit["_source"].get("meta"),
            "created_at": hit["_source"]["created_at"],
            "updated_at": hit["_source"].get("updated_at"),
            "deleted_at": hit["_source"].get("deleted_at"),
        }
        for hit in result["hits"]["hits"]
    ]
    return hits

def get_by_keyword(keyword):
    client = get_client()
    body = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["title"]
            }
        }
    }
    result = client.search(index=index_name, body=body)
    hits = [
        {
            "id": hit["_id"],
            "channel_id": hit["_source"]["channel_id"],
            "title": hit["_source"]["title"],
            "created_by": hit["_source"]["created_by"],
            "status": hit["_source"].get("status"),
            "meta": hit["_source"].get("meta"),
            "created_at": hit["_source"]["created_at"],
            "updated_at": hit["_source"].get("updated_at"),
            "deleted_at": hit["_source"].get("deleted_at"),
        }
        for hit in result["hits"]["hits"]
    ]
    return hits

def get_by_status(status):
    client = get_client()
    body = {
        "query": {
            "term": {
                "status": status
            }
        }
    }

    result = client.search(index=index_name, body=body)
    hits = [
        {
            "id": hit["_id"],
            "channel_id": hit["_source"]["channel_id"],
            "title": hit["_source"]["title"],
            "created_by": hit["_source"]["created_by"],
            "status": hit["_source"].get("status"),
            "meta": hit["_source"].get("meta"),
            "created_at": hit["_source"]["created_at"],
            "updated_at": hit["_source"].get("updated_at"),
            "deleted_at": hit["_source"].get("deleted_at"),
        }
        for hit in result["hits"]["hits"]
    ]
    return hits