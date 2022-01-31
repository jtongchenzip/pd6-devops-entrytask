import os

from dotenv import dotenv_values


env_values = {
    **dotenv_values(".env"),
    **os.environ,  # Override with OS
}


class DBConfig:
    vendor = env_values.get('DB_VENDOR')
    host = env_values.get('DB_HOST')
    port = int(env_values.get('DB_PORT'))
    username = env_values.get('DB_USERNAME')
    password = env_values.get('DB_PASSWORD')
    db_name = env_values.get('DB_DBNAME')


# default config objects
db_config = DBConfig()
