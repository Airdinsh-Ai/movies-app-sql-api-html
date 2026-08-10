from sqlalchemy import create_engine, text

# define the database URL
DB_URL = "sqlite:///data/movies.db"

# create the engine
engine = create_engine(DB_URL, echo=True)

# Create the users and movies tables if they do not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """))
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT,
            imdb_id TEXT,
            country TEXT,
            note TEXT,
            UNIQUE (user_id, title),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """))
    connection.commit()


def list_users():
    """Returns a dict of {user_id: user_name} for every existing user."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id, name FROM users ORDER BY id"))
        users = result.fetchall()

    return {row[0]: row[1] for row in users}


def create_user(name):
    """Creates a new user and returns their id."""
    with engine.connect() as connection:
        connection.execute(text("INSERT INTO users (name) VALUES (:name)"), {"name": name})
        connection.commit()
        result = connection.execute(
            text("SELECT id FROM users WHERE name = :name"), {"name": name}
        )
        return result.fetchone()[0]


def list_movies(user_id):
    """Retrieve all movies belonging to the given user from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text(
                "SELECT title, year, rating, poster_url, imdb_id, country, note "
                "FROM movies WHERE user_id = :user_id"
            ),
            {"user_id": user_id},
        )
        movies = result.fetchall()

    return {
        row[0]: {
            "year": row[1],
            "rating": row[2],
            "poster_url": row[3],
            "imdb_id": row[4],
            "country": row[5],
            "note": row[6],
        }
        for row in movies
    }


def add_movie(user_id, title, year, rating, poster_url=None, imdb_id=None, country=None):
    """Add a new movie for the given user to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    "INSERT INTO movies (user_id, title, year, rating, poster_url, imdb_id, country) "
                    "VALUES (:user_id, :title, :year, :rating, :poster_url, :imdb_id, :country)"
                ),
                {
                    "user_id": user_id,
                    "title": title,
                    "year": year,
                    "rating": rating,
                    "poster_url": poster_url,
                    "imdb_id": imdb_id,
                    "country": country,
                },
            )
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(user_id, title):
    """Delete a movie belonging to the given user from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("DELETE FROM movies WHERE user_id = :user_id AND title = :title"),
                {"user_id": user_id, "title": title},
            )
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(user_id, title, note):
    """Update a movie's note in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    "UPDATE movies SET note = :note "
                    "WHERE user_id = :user_id AND title = :title"
                ),
                {"user_id": user_id, "title": title, "note": note},
            )
            connection.commit()
            print(f"Movie '{title}' successfully updated")
        except Exception as e:
            print(f"Error: {e}")
