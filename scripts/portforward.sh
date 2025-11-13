#!/bin/bash

# ================================
# CONFIGURA TUS SERVICIOS AQUÍ
# Formato:
#   port-forward LOCAL_PORT:CLUSTER_PORT service_name
# ================================

services=(
  "8081:80 users-service default"
  "8082:8000 channel-api-service default"
  "8083:80 threads-service default"
  "8084:80 messages-service default"
  "8085:80 presence-service default"
  "8086:8000 moderation-service default"
  "8087:80 file-service-api file-service"
  "8088:8000 search-service default"
  #"8089:6379 redis-academico default"
  #"8090:"
  "8091:8000 api calculadora"
  "8092:9001 wikipedia-chatbot-service default"
  "8093:80 chatbot-programming-service default"
)


# ================================


echo "Iniciando port-forwards"
echo

for entry in "${services[@]}"; do
  local_port=$(echo "$entry" | awk '{print $1}' | cut -d':' -f1)
  cluster_port=$(echo "$entry" | awk '{print $1}' | cut -d':' -f2)
  svc=$(echo "$entry" | awk '{print $2}')
  namespace=$(echo "$entry" | awk '{print $3}')

  echo "→ svc/$svc  (ns: $namespace)"
  echo "    localhost:$local_port  →  $svc:$cluster_port"
  echo

  kubectl port-forward -n "$namespace" svc/"$svc" "$local_port":"$cluster_port" &
done

echo "✓ Port-forwards activos. CTRL+C para detenerlos."
echo

wait