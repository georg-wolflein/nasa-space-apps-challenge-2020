import typing
import numpy as np
import pandas as pd
import sklearn.metrics
import random

from fastapi import FastAPI

app = FastAPI()

# Calculate adjacency matrix once on startup
df = (pd.read_csv("../data/embeddings.csv")
      .drop(columns="Unnamed: 0")
      .set_index("V1")
      .dropna())
adjacency_matrix = sklearn.metrics.pairwise.cosine_similarity(df, df)
adjacency_matrix = pd.DataFrame(adjacency_matrix)
adjacency_matrix.index = df.index
adjacency_matrix.index.name = "id"
adjacency_matrix.columns = df.index

# Read metadata CSV file
df = pd.read_csv("../data/data.csv")
df = df.set_index("id")


@app.post("/recommend")
def get_recommendation(liked: typing.List[str], disliked: typing.List[str]):
    liked = list(set(liked))
    disliked = list(set(disliked))
    seen = list(set(liked + disliked))
    if len(liked) == 0:
        id = df.index[random.randint(0, 30000)]
    else:
        def get_top_n(n=10):
            for liked_id in liked:
                yield adjacency_matrix[liked_id].nlargest(n + len(seen)).drop(index=seen, errors="ignore")
        id = random.choice(pd.concat(list(get_top_n())).nlargest(10).index)
    info = df.loc[id]
    print(info)
    title = info["title"]
    summary = info["summary"]
    url = info["url"]

    return {
        "id": id,
        "title": title,
        "summary": summary,
        "url": url,
        "image": "https://scontent.xx.fbcdn.net/v/t1.15752-0/p280x280/120844566_370002721029530_5021203831255866936_n.jpg?_nc_cat=100&_nc_sid=ae9488&_nc_ohc=3iyUnuzPWlkAX-0NKw4&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&tp=6&oh=ccb0f0b641bdb8d3ab6aa8131b78919b&oe=5F9D87CA"
    }
