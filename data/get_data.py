import requests
import json
import itertools
import pandas as pd
import numpy as np

url = "https://cmr.earthdata.nasa.gov/search/collections.json?page_size=1&scroll=true&include_facets=true&hierarchical_facets=true&echo_compatible=true"


def _get_data(response):
    for dataset in response.json()["feed"]["entry"]:
        id = dataset["id"]
        title = dataset["title"]
        summary = dataset["summary"]

        print(len(response.json()["feed"]["facets"]))
        print(len(response.json()["feed"]["entry"]))
        print("--")

        # let values = []
        # let topic = resp.data.feed.facets[9].category[0].topic;

        # console.log(topic)

        # //THIS SHIT GETS THE LITTLE KEYWORDS AND NOT THE BIG ONES
        # for (i = 0; i < topic.length; i++) {
        #     let terms = topic[i].term
        #     for (j = 0; j < terms.length; j++) {
        #         let subfields = terms[j].subfields
        #         for (x = 0; x < subfields.length; x++) {
        #             let subValues = terms[j][subfields[x]]
        #             for (y = 0; y < subValues.length; y++) {
        #                 values.push(subValues[y].value)
        #                 subfields2 = subValues[y].subfields
        #                 if (typeof subfields2 != "undefined") {
        #                     for (z = 0; z < subfields2.length; z++) {
        #                         let s2 = subfields2[z]
        #                         let subfields3 = subValues[y][s2]
        #                         for (e = 0; e < subfields3.length; e++) {
        #                             values.push(subfields3[e].value)
        #                         }
        #                     }
        #                 }
        #             }
        #         }
        #     }
        # }

        # //THIS SHIT GETS THE BIG KEYWORDS
        # for (i = 0; i < topic.length; i++) {
        #     values.push(topic[i].value)
        # }

        # var valuesCSV = values.join('|')
        # console.log(valuesCSV)
        yield id, title, summary


def get_data(*args, **kwargs):
    return list(_get_data(*args, **kwargs))


response = requests.get(url)
scroll_id = response.headers["CMR-Scroll-Id"]
data_pages = [get_data(response)]

for i in itertools.count():
    print("i", i)
    response = requests.get(url, headers={"CMR-Scroll-Id": scroll_id})
    data = get_data(response)
    if len(data) == 0:
        break
    data_pages.append(data)
    break

data = np.array(list(itertools.chain.from_iterable(data_pages)))
df = pd.DataFrame(data)
df.columns = ["id", "title", "summary"]
df.to_csv("data.csv")
