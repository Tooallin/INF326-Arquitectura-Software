import json
import logging
from files.mapping import index_name
from elastic_search.connection import get_client
from elasticsearch import helpers

def svc_getall():
	es = get_client()
	if not es.indices.exists(index=index_name):
		logging.warning(f"[files] índice no existe: {index_name}")
		return []  # devolver lista vacía es más útil que string vacío

	# Si se acaba de indexar, asegura visibilidad
	es.indices.refresh(index=index_name)

	# Conteo para diagnosticar
	total = es.count(index=index_name).get("count", 0)
	logging.info(f"[files] total docs en '{index_name}': {total}")

	if total == 0:
		return []

	res_files = []
	try:
		for hit in helpers.scan(
			client=es,
			index=index_name,
			query={"query": {"match_all": {}}},
			_source=True,
			scroll="2m",
			size=1000,
			preserve_order=True,
		):
			src = hit.get("_source") or {}
			if src:
				res_files.append(src)
	except Exception as e:
		logging.error(f"[files] error en scan: {e}")
		return []

	return res_files 

def svc_searchfiles(q=None, thread_id=None, message_id=None, pages_min=None, pages_max=None, limit=10, offset=0):
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
				"fields": ["name^3", "content"],
				"type": "best_fields",
				"operator": "and",  # AND entre términos, OR entre campos
			}
		})
		# 2) Booster por prefijo/frase (autocomplete y coincidencias de frase)
		should.append({
			"multi_match": {
				"query": q,
				"fields": ["name^4", "content"],
				"type": "phrase_prefix"
			}
		})

	# Filtros exactos
	if thread_id is not None:
		filter_.append({"term": {"thread_id": thread_id}})
	if message_id is not None:
		filter_.append({"term": {"message_id": message_id}})
	if pages_min is not None or pages_max is not None:
		rg = {}
		if pages_min is not None: rg["gte"] = pages_min
		if pages_max is not None: rg["lte"] = pages_max
		filter_.append({"range": {"pages": rg}})

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

	resp = es.search(
		index=index,
		query=query,
		from_=offset,
		size=limit,
		track_total_hits=True
	)

	results = [h["_source"] for h in resp["hits"]["hits"]]
	return {
		"total": resp["hits"]["total"]["value"] if "hits" in resp else 0,
		"results": results
	}