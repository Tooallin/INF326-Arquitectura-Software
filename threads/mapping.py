index_name = "threads"

#Definir la estructura
mapping = {
    "properties":{
        "id": { "type": "keyword" },
        "title":{ 
            "type": "text",
            "fields":{
                "keyword": { "type": "keyword", "ignore_above": 256 }
            }
                  } ,
        "content": { "type": "text" }, 
        "author_id": { "type": "keyword" },
        "creation_date": { "type": "date" } ,
        "tags": { "type": "keyword" },
        "category": { "type": "keyword" }
    }
}