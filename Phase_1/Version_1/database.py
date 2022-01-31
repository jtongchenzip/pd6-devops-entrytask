from config import db_config


async def execute(sql):

    if db_config.vendor.lower() == 'mysql':
        import asyncio
        import aiomysql
        connection: aiomysql.Connection = await aiomysql.connect(
            host=db_config.host,
            port=db_config.port,
            user=db_config.username,
            password=db_config.password,
            db=db_config.db_name,
            loop=asyncio.get_running_loop(),
            autocommit=True,
        )
        cursor: aiomysql.cursors.Cursor = await connection.cursor()
        try:
            await cursor.execute(sql)
            return await cursor.fetchone()
        finally:
            await cursor.close()
            await connection.ensure_closed()

    elif db_config.vendor.lower() == 'postgresql':
        import asyncpg
        connection: asyncpg.Connection = await asyncpg.connect(
            host=db_config.host,
            port=db_config.port,
            user=db_config.username,
            password=db_config.password,
            database=db_config.db_name,
        )
        try:
            return await connection.fetchrow(sql)
        finally:
            await connection.close()

    else:
        raise ValueError
