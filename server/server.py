import string
import typing
import numpy as np
import pandas as pd
import sklearn.metrics
import random
import json
import requests
from gensim.summarization import keywords
import nltk
import re

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
    image = get_bing_image_url_from_title(title)

    return {
        "id": id,
        "title": title,
        "summary": summary,
        "url": url,
        "image": image
    }


def get_bing_image_url_from_title(title):
    headers = {'Ocp-Apim-Subscription-Key': '9958354b605a4c2b937ff6e9b3e4592e'}
    title = title.translate(str.maketrans('', '', string.punctuation))
    title = re.sub(r'[0-9]+', '', title)

    tokens = nltk.word_tokenize(title)
    tagged = nltk.pos_tag(tokens)

    occurrences = tagged.count("NNP")

    if(occurrences > 2):
        for j in tagged:
            if(j[1] != 'NNP'):
                tagged.remove(j)

    for j in tagged:
        if(j[1] != 'NNP'):
            tagged.remove(j)
        if(len(j[1]) < 2):
            tagged.remove(j)

    tagged_1 = np.array(tagged)
    title2 = tagged_1[:, 0]

    new_sentence = (' '.join(title2))

    key_num = keywords(new_sentence, words=6, scores=False, lemmatize=True)

    payload = {'q': key_num, 'count': 1, 'offset': 0, 'safeSearch': "moderate"}
    r = requests.get('https://api.cognitive.microsoft.com/bing/v7.0/images/search?',
                     params=payload, headers=headers)
    rJson = json.loads(r.text)
    return rJson["value"][0]['contentUrl']
