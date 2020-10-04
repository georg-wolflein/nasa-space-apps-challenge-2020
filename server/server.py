import typing
import numpy as np
import pandas as pd
import sklearn.metrics

from fastapi import FastAPI

app = FastAPI()

# # Calculate adjacency matrix once on startup
# df = (pd.read_csv("../data/embeddings.csv")
#       .drop(columns="Unnamed: 0")
#       .set_index("V1")
#       .dropna())
# adjacency_matrix = sklearn.metrics.pairwise.cosine_similarity(df, df)
# adjacency_matrix = pd.DataFrame(adjacency_matrix)
# adjacency_matrix.index = df.index
# adjacency_matrix.index.name = "id"
# adjacency_matrix.columns = df.index

# # Read metadata CSV file
# df = pd.read_csv("../data/data_about_nasa_datasets.csv")


@app.post("/recommend")
def get_recommendation(liked: typing.List[str], disliked: typing.List[str]):
    return {
        "id": "abc",
        "title": "dataset title",
        "summary": "summ",
        "url": "http://google.com"
    }
