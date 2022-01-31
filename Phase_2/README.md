# DevOps Entry Task Phase 1-2

## Phase 1-2

### Requirements:
1. Initialize another PostgreSQL service in another container
2. Migrate the data from existing MySQL to PostgreSQL
3. Run and test the API service, using the new PostgreSQL database instead


### Instructions:
1. Start with the files we had in Phase 1-1
2. edit `docker-compose.yaml` to the following:
```shell
version: "3.8"

services:
    mysql:
        container_name: mysql_1-2
        image: mysql:5.7
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
        container_name: app_1-2
        image: python:3.9
        links: 
            - "postgres:postgres"
        restart: always
        command: sh -c "cd /code && pip install -r requirements.txt && pip install uvicorn && uvicorn app:app --host 0.0.0.0 --port 80"
        ports:
            - "8080:80"
        volumes:
            - .:/code       
        env_file: 
            - .env

    postgres:
        image: postgres:latest
        container_name: postgres_1-2
        ports:
            - 5432:5432
        restart: always
        volumes: 
            - db_data:/var/lib/postgres/db_data
        environment: 
            POSTGRES_PASSWORD: root

volumes: 
    db_data:
```
3. In your terminal, run
```shell
docker-compose up -d --build
```
which should build three containers for mysql, app, and postgres

4. In order to create a new database in postgresql for migration, run
```shell
docker exec -it $postgres_container_name createdb -U postgres $new_database_name
```
  (In this case, `$postgres_container_name` is postgres_1-2, `$new_database_name` is targetdb)

5. In order to use `pgloader` to migrate, run 
```shell
docker run --rm --network host --name pgloader dimitri/pgloader:latest pgloader -v --debug mysql://root:$MYSQL_ROOT_PASSWORD@172.17.0.1:$port_of_mysql/$MYSQL_DATABASE postgresql://postgres:$POSTGRES_PASSWORD@172.17.0.1:$port_of_postgres/$POSTGRES_DATABASE
```
  (In this case, `$MYSQL_ROOT_PASSWORD` is root, `$port_of_mysql` is 3306,  `$MYSQL_DATABASE` is test, `$POSTGRES_PASSWORD` is root, `$port_of_postgres` is 5432, `$POSTGRES_DATABASE` is targetdb)
  (172.17.0.1 represents docker itself or host)

6. Run
```shell
docker-compose up
```
7. The service should be running at `https://localhost:8080`
8. You could turn off the mysql container to test if the fastapi service is running on postgres

### Notes
1. `command: --default-authentication-plugin=mysql_native_password` is required for mysql version 8.
2. In `docker-compose.yaml -> service:app:links:` should match with `"DB_VENDOR:DB_HOST"`.
3. In `docker-compose.yaml -> service:mysql:environment:`, it is required to set `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE`.
4. Writing `env_file: -.env` in `docker-compose.yaml` isn't necessary.