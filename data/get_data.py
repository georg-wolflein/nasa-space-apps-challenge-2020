import requests
import json
import itertools
import pandas as pd
import numpy as np

url = "https://cmr.earthdata.nasa.gov/search/collections.json?page_size=100&scroll=true"


def _get_data(response):
    for dataset in response.json()["feed"]["entry"]:
        id = dataset["id"]
        title = dataset["title"]
        summary = dataset["summary"]
        if "links" in dataset:
            link = dataset["links"][0]["href"]
        else:
            link = "http://google.com/search?q=" + "+".join(title.split(" "))
        yield id, title, summary, link


def get_data(*args, **kwargs):
    return list(_get_data(*args, **kwargs))


response = requests.get(url)
scroll_id = response.headers["CMR-Scroll-Id"]
data_pages = [get_data(response)]

for i in itertools.count():
    print(i)
    response = requests.get(url, headers={"CMR-Scroll-Id": scroll_id})
    data = get_data(response)
    if len(data) == 0:
        break
    data_pages.append(data)

data = np.array(list(itertools.chain.from_iterable(data_pages)))
df = pd.DataFrame(data)
df.columns = ["id", "title", "summary", "url"]
df.to_csv("data.csv")
