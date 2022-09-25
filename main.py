import os
import uvicorn
import meilisearch
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector as mariadb

# Model
import pandas as pd
from scipy import spatial
from sklearn.feature_extraction.text import TfidfVectorizer


def create_model():
    # Load data
    data = pd.read_csv(
        './dataset/switch-games-clean-reviews.csv',
        delimiter=','
    )

    # My model will be a simple tf-idf over all reviews
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data['clean_review'])
    X.shape

    # Tree to do a fast search over distances
    tree = spatial.KDTree(X.toarray())
    return X, tree, data

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = meilisearch.Client(
    'https://api.egiovanni.com:7700',
    api_key=os.environ.get('PROJECTS_PERSONAL_KEY')
)

connection = mariadb.connect(
    user='root',
    password=os.environ.get('PROJECTS_PERSONAL_KEY'),
    host='35.232.158.64',
    database='games'
)

X, tree, data = create_model()


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


@app.get('/model/')
async def model_prediction(id: str = Query(min_length = 8)):
    print('-------', data)
    print('-------', data.index[data['id'] == id][0])

    index = data.index[data['id'] == id][0]
    game_array = X[index].toarray()[0]
    games_closest = tree.query(game_array, k=21)[1][1:]
    return [data.iloc[index]['id'] for index in games_closest]


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=80)