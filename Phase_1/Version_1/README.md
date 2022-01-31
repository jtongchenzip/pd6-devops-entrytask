# DevOps Entry Task Phase 1-1 version 1

## Phase 1-1 

### Requirements:
Use docker to initialize two services:
1. Python `fastapi` API service
2. MySQL Database service

Note that:
- Both services should live in their own container.
- For convenience, the database schema is included in the backend project. (Which typically should not)

### Instructions:
1. Git clone or download Backend Example at `https://nas.pdogs.ntu.im:30443/pdogs/pdogs-6/pd6-devops/backend-example`
2. Create a `Dockerfile`at the root of the folder, which is used in order to create a python image
```shell
FROM python:3.9

COPY . ./code/
WORKDIR /code
ADD requirements.txt .
RUN pip install -r requirements.txt \ 
    && pip install uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```
3. Create `docker-compose.yaml`at the root of the folder, and write the followings:
```shell
version: "3.8"

services:
    mysql:
        container_name: mysql_v1
        image: mysql:8
        command: --default-authentication-plugin=mysql_native_password
        restart: always        
        volumes:
            - ./schema:/docker-entrypoint-initdb.d
        environment:
            MYSQL_ROOT_PASSWORD: root
            MYSQL_USER: user
            MYSQL_PASSWORD: root
            MYSQL_DATABASE: 1-1
        ports:
            - "3306:3306"
        env_file: 
            - .env

    app:
        container_name: app_v1
        build: .
        ports:
            - "8000:8000"
        volumes:
            - .:/code
        links: 
            - "mysql:mysql"
        env_file: 
            - .env
```
4. Delete .env.example
5. Create .env, and write the followings:
```shell
DB_VENDOR=mysql
DB_HOST=mysql
DB_PORT=3306
DB_USERNAME=root
DB_PASSWORD=root
DB_DBNAME=1-1
```
6. In your terminal, go to the path where you put the project
7. Run the following command
```shell
docker-compose up -d --build
```
8. After the container is built, run
```shell
docker-compose up
```
and you should see 
```shell
app_v1   | INFO:     Started server process [1]
app_v1   | INFO:     Waiting for application startup.
app_v1   | INFO:     Application startup complete.
app_v1   | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
mysql_v1 | 2021-07-03T07:49:38.902343Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.25'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
```
9. Go to `http://localhost:8000`, the service should be running there

### Notes
1. In version 1, instead of directly pull a python image, we use a dockerfile to create a python image.
2. `command: --default-authentication-plugin=mysql_native_password` is required for mysql version 8.
3. In `docker-compose.yaml -> service:app:links:`, the links should match `"DB_VENDOR:DB_HOST"`.
4. In `docker-compose.yaml -> service:mysql:environment:`, it is required to set `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE`.
5. Writing `env_file: -.env` in `docker-compose.yaml` isn't necessary.