# Movies App

A command-line movie database application with multiple user profiles.
Movies are stored in a SQLite database and can be enriched automatically
with year, rating, poster image, IMDB link and country of origin by
fetching data from the OMDb API. The app can also generate a static HTML
website for each user, listing their personal movie collection.

## Features

- Multiple user profiles: create new users, switch between them and
  delete a user (including all of their movies)
- Add, delete, update and list movies
- Movie details (year, rating, poster, IMDB link, country) are fetched
  automatically from the OMDb API when adding a movie
- Personal notes can be added to a movie and are shown as a tooltip on
  the generated website
- Statistics (average/median rating, best/worst movie)
- Fuzzy movie search, sorting and filtering
- Rating histogram (matplotlib)
- Static website generation per user (movie posters link to IMDB, movie
  titles are prefixed with the country's flag), with a responsive grid
  layout that also works well for larger collections

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

Select or create a user profile, then follow the on-screen menu to
manage your movie collection. Choose "Generate website" to create an
HTML page (named after the current user) from their movie collection.
