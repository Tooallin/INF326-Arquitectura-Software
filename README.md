# INF326-Arquitectura-Software Servicio de Búsqueda

Integrantes:
- Jan Jorquera.
- Jose Astudillo.
- Alessandro Cintolesi.

Repositorio asociado al servicio de búsqueda cuyas tareas son: 
Indexa eventos de mensajes, hilos y archivos.
Expone búsquedas por canal, hilo o palabra clave.

## [Enlace video](https://usmcl-my.sharepoint.com/:v:/g/personal/jan_jorquera_usm_cl/ERjWPO-v5AdAivVsWNW5TWcBoSLpJe8-DF9RSoOXLnRZ1A?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=rAz1cH)
## [Enlace video pruebas de servicio](https://usmcl-my.sharepoint.com/:v:/g/personal/jan_jorquera_usm_cl/IQAnlUWod82JTah4fMXek5RQAYRR_n18sT_CaoKCfhplEkU?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=XLkt7r)
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

6.- Para levantar el contenedor para testear el microservicio: 
`docker compose -f docker-compose-test.yaml up --build --attach test_runner --abort-on-container-exit --exit-code-from test_runner`