import json
import logging
from files.mapping import index_name
from elastic_search.connection import get_client
from elasticsearch import helpers

def svc_searchfiles(q=None, file_id=None, thread_id=None, message_id=None, limit=10, offset=0):
	es = get_client()
	index = index_name  # "files"

	# Asegura visibilidad si acabas de indexar
	try:
		es.indices.refresh(index=index)
	except Exception:
		pass

	must = []
	filter_ = []
	should = []

	# Texto
	if q:
		# 1) Búsqueda principal (mejor campos, exige que todos los términos estén presentes pero en AL MENOS un campo)
		should.append({
			"multi_match": {
				"query": q,
				"fields": ["filename^3"],
				"type": "best_fields",
				"operator": "and",  # AND entre términos, OR entre campos
			}
		})
		# 2) Booster por prefijo/frase (autocomplete y coincidencias de frase)
		should.append({
			"multi_match": {
				"query": q,
				"fields": ["filename^4"],
				"type": "phrase_prefix"
			}
		})

	# Filtros exactos
	if file_id is not None:
		filter_.append({"term": {"file_id": file_id}})
	if thread_id is not None:
		filter_.append({"term": {"thread_id": thread_id}})
	if message_id is not None:
		filter_.append({"term": {"message_id": message_id}})
	# if pages_min is not None or pages_max is not None:
	# 	rg = {}
	# 	if pages_min is not None: rg["gte"] = pages_min
	# 	if pages_max is not None: rg["lte"] = pages_max
	# 	filter_.append({"range": {"pages": rg}})

	# Query final: si no hay texto ni filtros => match_all
	if not q and not filter_:
		query = {"match_all": {}}
	else:
		query = {
			"bool": {
				# Claves: usamos SOLO should para el texto (OR entre campos) y exigimos al menos 1
				"should": should,
				"minimum_should_match": 1 if should else 0,
				"filter": filter_,
			}
		}

	result = es.search(
		index=index,
		query=query,
		from_=offset,
		size=limit,
		track_total_hits=True
	)

	hits = [
		{
			"id": hit["_id"],
			"filename": hit["_source"]["filename"],
			"mime_type": hit["_source"]["mime_type"],
			"size": hit["_source"]["size"],
			"bucket": hit["_source"]["bucket"],
			"object_key": hit["_source"]["object_key"],
			"message_id": hit["_source"].get("message_id"),
			"thread_id": hit["_source"].get("thread_id"),
			"checksum_sha256": hit["_source"].get("checksum_sha256"),
			"created_at": hit["_source"]["created_at"],
			"deleted_at": hit["_source"].get("deleted_at"),
		}
		for hit in result["hits"]["hits"]
	]

	return hits