import fastapi


app = fastapi.FastAPI()


@app.get('/')
async def index():
    return "I'm alive! <a href=/docs>/docs</a>"


@app.get('/insert')
async def insert():
    import random
    num = random.randint(1, 1000000)

    import database
    await database.execute(f"INSERT INTO my_table (num) VALUES ({num})")

    return f"{num} is inserted!"


@app.get('/read')
async def read():
    import database

    row = await database.execute("SELECT count(*), min(num), max(num) FROM my_table")
    print(row)
    count, min_num, max_num = row

    return f"There are {count} rows in table, maximum is {max_num}, minimum is {min_num}"
