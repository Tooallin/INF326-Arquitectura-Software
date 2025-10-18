# INF326-Arquitectura-Software Tarea 4
Integrantes:
- Jan Jorquera.
- Jose Astudillo.
- Alessandro Cintolesi.

## Instrucciones para correr la tarea

1.- Crear la red donde se comunicarán los containers
`docker network create Search_Service`

2.- En el directorio `/message_broker` correr: 
`docker compose up --build -d`

3.- En el directorio `/publisher` correr: 
`docker compose up --build -d`

4.- En el directorio raíz del proyecto correr: 
`docker compose up --build -d`

5.- Finalmente para terminar la ejecución correr en los directorio correspondientes el siguiente comando: 
`docker compose down`