from elastic_search.connection import get_client
from elasticsearch.dsl import Search, query, aggs
from threads.mapping import index_name

def get_by_id(thread_id):
    client=get_client()
    s = Search(using=client, index=index_name).query(query.Term("id",thread_id))
    
    response = s.execute()
    
    results = [hit.to_dict() for hit in response]

    return results        
    
def get_by_category(category):
    client=get_client()
    s = Search(using=client, index=index_name) \
        .query(query.Term("category", category))
    
    response = s.execute()

    results = [hit.to_dict() for hit in response]
    
    return results

def get_by_author(author_id):
    client=get_client()
    s= Search(using=client, index=index_name) \
        .query(query.Term("author_id", author_id))
    
    response = s.execute()

    results = [hit.to_dict() for hit in response]
    
    return results

def get_by_date_range(start_date, end_date):
    client=get_client()
    s= Search(using=client, index=index_name) \
        .query(query.Range(
            creation_date={"gte": start_date, "lt":end_date}
        ))    
    response = s.execute()

    results = [hit.to_dict() for hit in response]
    
    return results

def get_by_tag(tag):
    client=get_client()
    s = Search(using=client, index=index_name) \
        .query(query.Term("tags", tag))
    
    response = s.execute()

    results = [hit.to_dict() for hit in response]
    
    return results

def get_by_keyword(keyword):
    client=get_client()
    s = Search(using=client, index=index_name) \
        .query(
            query.MultiMatch(
            query=keyword,
            fields=["title", "content", "tags", "category"],
            )
        )
    
    response = s.execute()

    results = [hit.to_dict() for hit in response]
    return results