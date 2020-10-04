# NASA Space Apps Challenge Hackathon

Team _Pablo and the [Aikmen](https://www.cellarbar.co.uk/)_.

_Terra Tinder_ aims to match users with datasets that are suited to their preferences. The user will use our web app to find the best dataset in an efficient and accessible format.

## Architecture

### Backend

The backend is responsible for computing recommendation based on the positive and negative feedback the user gave on previous datasets (i.e. swiping right or left).

First, metadata on all ~30,000 NASA Earth Science Datasets was gathered via the associated API and saved in `data/data.csv`.
Each dataset was mapped to a point in a 15-dimensional embedding space by using the means of the word2vec embeddings for the dataset summaries.
This data was saved in CSV file in `data/embeddings.csv`

The backend server runs on Python.
Upon startup, an adjacency matrix is calculated based on the cosine similarity between all dataset embeddings.
This adjacency matrix contains roughly 900,000,000 entries and would be too large to commit to version control.
Instead it is calculated once upon startup of the server and stored in memory.

The server provides an API for the frontend for recommending datasets.
Dataset recommendation is achieved using an algorithm that takes into account the previously liked and disliked datasets (which are supplied as part of the API request), and associated similarity scores to other datasets.

Furthermore, the backend extracts keywords from the recommended dataset's title using NLP techniques in order to conduct a Bing image search to obtain a relevant image to display in the web app.

### Frontend

The frontend is written in JavaScript using React.
It establishes a connection to the backend server and uses the backend API to serve information.
See the screenshot below.

<img src="images/screenshot.png" alt="screenshot" style="width:300px;"/>

## Installing and running

### Backend

For the backend, install Python 3 and the `poetry` package manager.
Then, run (from the `server` folder):

```bash
poetry install
```

To run the server, execute

```bash
poetry run uvicorn server:app
```

### Frontend

To install the dependencies for the frontend, first install `node` and `npm` and then run (in the `app` directory):

```bash
npm install
```

Finally, to start the web app, run

```bash
npm start
```

Navigate to [http://localhost:3000](http://localhost:3000) to view the app.
