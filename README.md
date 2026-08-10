# Movies App

A command-line movie database application. Movies are stored in a SQLite
database and can be enriched automatically with year, rating and poster
image by fetching data from the OMDb API. The app can also generate a
static HTML website listing your movie collection.

## Features

- Add, delete, update and list movies
- Movie details (year, rating, poster) are fetched automatically from the
  OMDb API when adding a movie
- Statistics (average/median rating, best/worst movie)
- Fuzzy movie search, sorting and filtering
- Rating histogram (matplotlib)
- Static website generation from the movie collection

## Installation

Clone the repository and install the dependencies:

```
pip install -r requirements.txt
```

Create a `.env` file in the project root with your own OMDb API key
(get one for free at https://www.omdbapi.com/apikey.aspx):

```
OMDB_API_KEY=your_key_here
```

## Usage

```
python main.py
```

Follow the on-screen menu to manage your movie collection. Choose
"Generate website" to create `index.html` from your current collection.
