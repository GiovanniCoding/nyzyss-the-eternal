import os
import uvicorn
import meilisearch
from fastapi import FastAPI, Query
import mysql.connector as mariadb


app = FastAPI()
client = meilisearch.Client(
    'http://api.egiovanni.com:7700',
    api_key=os.environ.get('PROJECTS_PERSONAL_KEY')
)

connection = mariadb.connect(
    user='root',
    password=os.environ.get('PROJECTS_PERSONAL_KEY'),
    host='34.136.74.202',
    database='games'
)


@app.get("/")
async def root():
    return {"message": "Wellcome to a Private API"}


@app.get("/meilisearch/")
async def meilisearch_search(collection: str = Query(min_length=3), query: str = Query(min_length=1)):
    return client.index(collection).search(query)


@app.get("/db/")
async def db_search(games: str = Query(min_length=8)):
    games = "','".join(games.split('-'))
    cursor = connection.cursor()
    query = '''
        SELECT *
        FROM switch_games
        WHERE id IN ('{0}')
    '''.format(games)
    cursor.execute(query)
    games_list = cursor.fetchmany(20)
    return games_list


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=80)