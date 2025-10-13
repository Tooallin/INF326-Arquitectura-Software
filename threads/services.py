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
    response = client.search(index=index_name, body=body)
    results = [hit["_source"] for hit in response["hits"]["hits"]]
    return results        
    
def get_by_category(category):
    client = get_client()
    body = {
        "query": {
            "term": {
                "category": category
            }
        }
    }
    response = client.search(index=index_name, body=body)
    results = [hit["_source"] for hit in response["hits"]["hits"]]
    return results

def get_by_author(author_id):
    client = get_client()
    body = {
        "query": {
            "term": {
                "author_id": author_id
            }
        }
    }
    response = client.search(index=index_name, body=body)
    results = [hit["_source"] for hit in response["hits"]["hits"]]
    return results

def get_by_date_range(start_date, end_date):
    client = get_client()
    body = {
        "query": {
            "range": {
                "creation_date": {
                    "gte": start_date,
                    "lt": end_date
                }
            }
        }
    }
    response = client.search(index=index_name, body=body)
    results = [hit["_source"] for hit in response["hits"]["hits"]]
    return results

def get_by_tag(tag):
    client = get_client()
    body = {
        "query": {
            "term": {
                "tags": tag
            }
        }
    }
    response = client.search(index=index_name, body=body)
    results = [hit["_source"] for hit in response["hits"]["hits"]]
    return results

def get_by_keyword(keyword):
    client = get_client()
    body = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["title", "content", "tags", "category"]
            }
        }
    }
    response = client.search(index=index_name, body=body)
    results = [hit["_source"] for hit in response["hits"]["hits"]]
    return results