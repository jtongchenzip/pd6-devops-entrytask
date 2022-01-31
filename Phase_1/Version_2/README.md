# DevOps Entry Task Phase 1-1 version 2

## Phase 1-1 

### Requirements:
Use docker to initialize two services:
1. Python `fastapi` API service
2. MySQL Database service

Note that:
- Both services should live in their own container.
- For convenience, the database schema is included in the backend project. (Which typically should not)

### Instructions:
1. Git clone or download Backend Example at `https://nas.pdogs.ntu.im:30443/pdogs/pdogs-6/pd6-devops/backend-example.git`
2. create `docker-compose.yaml`, and write the followings:
```shell
version: "3.8"

services:
    mysql:
        container_name: mysql_v2
        image: mysql:8
        command: --default-authentication-plugin=mysql_native_password
        restart: always        
        volumes:
            - ./schema:/docker-entrypoint-initdb.d
        environment:
            MYSQL_ROOT_PASSWORD: root
            MYSQL_DATABASE: test
            MYSQL_USER: test
            MYSQL_PASSWORD: test
        ports:
            - "3306:3306"
        env_file: 
            - .env

    app:
        container_name: app_v2
        image: python:3.9
        links: 
            - "mysql:mysql"
        restart: always
        command: sh -c "cd /code && pip install -r requirements.txt && pip install uvicorn && uvicorn app:app --host 0.0.0.0 --port 8000"
        ports:
            - "8000:8000"
        volumes:
            - .:/code       
        env_file: 
            - .env
```
3. Delete .env.example
4. Create .env, and write the followings:
```shell
DB_VENDOR=mysql
DB_HOST=mysql
DB_PORT=3306
DB_USERNAME=root
DB_PASSWORD=root
DB_DBNAME=test
```
5. In your terminal, go to the path where you put the project
6. Run the following command
```shell
docker-compose up -d --build
```
7. After the container is built, run
```shell
docker-compose up
```
  and you should see 
```shell
app_v2   | INFO:     Started server process [1]
app_v2   | INFO:     Waiting for application startup.
app_v2   | INFO:     Application startup complete.
app_v2   | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
mysql_v2 | 2021-07-03T08:46:24.187820Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.25'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
```
8. Go to `http://localhost:8000`, the service should be running there

### Notes
1. In version 2, we pull an python image directly instead of using a dockerfile.
2. `command: --default-authentication-plugin=mysql_native_password` is required for mysql version 8.
3. In `docker-compose.yaml -> service:app:links:` should match with `"DB_VENDOR:DB_HOST"`.
4. In `docker-compose.yaml -> service:mysql:environment:`, it is required to set `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE`.
5. Writing `env_file: -.env` in `docker-compose.yaml` isn't necessary.