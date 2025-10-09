# INF326-Arquitectura-Software

## Instrucciones para correr la tarea

1.- Crear la red donde se comunicarán los containers
`docker network create Search_Service`

2.- En el directorio `/message_broker` correr: 
`docker-compose up --build`

3.- En el directorio raíz del proyecto correr: 
`docker-compose up --build`

4.- Finalmente para terminar la ejecución correr en directorio raíz y en `/message_broker` el siguiente comando: 
`docker-compose down`