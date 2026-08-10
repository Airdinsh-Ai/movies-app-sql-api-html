import random

import matplotlib.pyplot as plt

import movie_storage_sql as storage
import omdb_api

# Custom ANSI styles using the JBlond Gist reference
STYLE_HEADER = "\033[1;4;93m"  # Bold + Underlined Yellow (Title)
STYLE_MENU = "\033[38;5;208m"  # Orange (256-color palette) for menu text
STYLE_MENU_NUM = "\033[1;38;5;214m"  # Bold Bright Orange (256-color) for menu numbers
STYLE_INPUT_PROMPT = "\033[4m"  # Underlined only for the prompt text
STYLE_SUCCESS_BG = "\033[97;42m"  # White text on Dark Green background
STYLE_ERROR_BG = "\033[97;41m"  # White text on Dark Red background
STYLE_RED = "\033[91m"  # Bright red text (no background) for warnings
STYLE_CYAN = "\033[96m"  # Clean Cyan for regular data output
STYLE_LIGHT_BLUE = "\033[38;5;117m"  # Very bright, light blue for user input
STYLE_DIM = "\033[2m"  # Faint/Dim style for separators
STYLE_RESET = "\033[0m"  # Clears all formatting


def colored_input(prompt_text: str) -> str:
    """Helper to prompt the user and color their typed input in light blue.

    Resets the terminal style immediately after Enter is pressed.
    """
    # We display the styled prompt and open the Light Blue style for the user's input
    user_data = input(
        f"{STYLE_INPUT_PROMPT}{prompt_text}{STYLE_RESET}{STYLE_LIGHT_BLUE}"
    )
    # Reset formatting instantly so the rest of the terminal stays normal
    print(STYLE_RESET, end="")
    return user_data


def get_nonempty_input(prompt_text: str) -> str:
    """Repeatedly prompts until the user enters a non-empty string."""
    while True:
        value = colored_input(prompt_text).strip()
        if value:
            return value
        print(f"\n{STYLE_ERROR_BG} Error: Input cannot be empty! {STYLE_RESET}")


def get_int_input(prompt_text: str) -> int:
    """Repeatedly prompts until the user enters a valid whole number."""
    while True:
        try:
            return int(colored_input(prompt_text))
        except ValueError:
            print(
                f"\n{STYLE_ERROR_BG} Error: Please enter a whole number! {STYLE_RESET}"
            )


def get_rating_input(prompt_text: str) -> float:
    """Repeatedly prompts until the user enters a valid rating between 0 and 10."""
    while True:
        try:
            rating = float(colored_input(prompt_text))
        except ValueError:
            print(f"\n{STYLE_ERROR_BG} Error: Rating must be a number! {STYLE_RESET}")
            continue
        if 0 <= rating <= 10:
            return rating
        print(
            f"\n{STYLE_ERROR_BG} Error: Rating must be between 0 and 10! {STYLE_RESET}"
        )


def get_yes_no_input(prompt_text: str) -> bool:
    """Repeatedly prompts until the user answers Y or N. Returns True for Y."""
    while True:
        answer = colored_input(prompt_text).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print(f"\n{STYLE_ERROR_BG} Error: Please enter Y or N! {STYLE_RESET}")


def get_optional_float_input(prompt_text: str):
    """Prompts for a float; returns None if the user leaves it blank."""
    while True:
        value = colored_input(prompt_text).strip()
        if not value:
            return None
        try:
            return float(value)
        except ValueError:
            print(
                f"\n{STYLE_ERROR_BG} Error: Please enter a number or leave "
                f"blank! {STYLE_RESET}"
            )


def get_optional_int_input(prompt_text: str):
    """Prompts for a whole number; returns None if the user leaves it blank."""
    while True:
        value = colored_input(prompt_text).strip()
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            print(
                f"\n{STYLE_ERROR_BG} Error: Please enter a whole number or "
                f"leave blank! {STYLE_RESET}"
            )


def print_menu():
    """Prints the application menu using a bold yellow title and orange choices."""
    print(f"\n{STYLE_HEADER}********** My Movies Database **********{STYLE_RESET}")
    print(f"\n{STYLE_MENU}Menu Choices:{STYLE_RESET}")
    print(
        f" {STYLE_MENU_NUM}1{STYLE_RESET}{STYLE_DIM}.{STYLE_RESET} {STYLE_MENU}List movies{STYLE_RESET}"
    )
    print(
        f" {STYLE_MENU_NUM}2{STYLE_RESET}{STYLE_DIM}.{STYLE_RESET} {STYLE_MENU}Add movie{STYLE_RESET}"
    )
    print(
        f" {STYLE_MENU_NUM}3{STYLE_RESET}{STYLE_DIM}.{STYLE_RESET} {STYLE_MENU}Delete movie{STYLE_RESET}"
    )
    print(
        f" {STYLE_MENU_NUM}4{STYLE_RESET}{STYLE_DIM}.{STYLE_RESET} {STYLE_MENU}Update movie{STYLE_RESET}"
    )
    print(
        f" {STYLE_MENU_NUM}5{STYLE_RESET}{STYLE_DIM}.{STYLE_RESET} {STYLE_MENU}Stats{STYLE_RESET}"
    )
    print(
        f" {STYLE_MENU_NUM}6{STYLE_RESET}{STYLE_DIM}.{STYLE_RESET} {STYLE_MENU}Random movie{STYLE_RESET}"
    )
    print(
        f" {STYLE_MENU_NUM}7{STYLE_RESET}{STYLE_DIM}.{STYLE_RESET} {STYLE_MENU}Search movie{STYLE_RESET}"
    )
    print(
        f" {STYLE_MENU_NUM}8{STYLE_RESET}{STYLE_DIM}.{STYLE_RESET} {STYLE_MENU}Movies sorted by rating{STYLE_RESET}"
    )
    print(
        f" {STYLE_MENU_NUM}9{STYLE_RESET}{STYLE_DIM}.{STYLE_RESET} {STYLE_MENU}Create rating histogram{STYLE_RESET}"
    )
    print(
        f" {STYLE_MENU_NUM}10{STYLE_RESET}{STYLE_DIM}.{STYLE_RESET} {STYLE_MENU}Movies sorted by year{STYLE_RESET}"
    )
    print(
        f" {STYLE_MENU_NUM}11{STYLE_RESET}{STYLE_DIM}.{STYLE_RESET} {STYLE_MENU}Filter movies{STYLE_RESET}"
    )
    print(
        f" {STYLE_MENU_NUM}12{STYLE_RESET}{STYLE_DIM}.{STYLE_RESET} {STYLE_MENU}Generate website{STYLE_RESET}"
    )
    print(
        f" {STYLE_MENU_NUM}0{STYLE_RESET}{STYLE_DIM}.{STYLE_RESET} {STYLE_MENU}Exit Application{STYLE_RESET}"
    )


def main():
    """Main Application Loop."""
    while True:
        # Reload from the database on every iteration so the menu always
        # reflects the latest state after an add/delete/update.
        movies = storage.list_movies()

        print_menu()
        # Custom helper ensures input typed by user is colored Light Blue
        choice = colored_input("\nEnter choice (0-12): ").strip()

        # Handle choices by calling the appropriate functions
        if choice == "1":
            list_movies(movies)
        elif choice == "2":
            add_movies(movies)
        elif choice == "3":
            delete_movies(movies)
        elif choice == "4":
            update_movies(movies)
        elif choice == "5":
            show_stats(movies)
        elif choice == "6":
            show_random_movie(movies)
        elif choice == "7":
            search_movie(movies)
        elif choice == "8":
            sort_movies(movies)
        elif choice == "9":
            create_rating_histogram(movies)
        elif choice == "10":
            sort_movies_by_year(movies)
        elif choice == "11":
            filter_movies(movies)
        elif choice == "12":
            generate_website(movies)
        elif choice == "0":
            print(
                f"\n{STYLE_SUCCESS_BG} Thank you for using My Movies "
                f"Database. Bye! {STYLE_RESET}"
            )
            break
        else:
            print(
                f"\n{STYLE_ERROR_BG} Invalid choice! Please enter a "
                f"number between 0 and 12. {STYLE_RESET}"
            )


def list_movies(movies):
    """1. List all movies in the database."""
    print(f"\n{STYLE_CYAN}{len(movies)} movies in total:{STYLE_RESET}\n")
    for title, info in movies.items():
        print(
            f"  {STYLE_CYAN}{title:<40}{STYLE_RESET} | "
            f"Year: {info['year']} | Rating: {info['rating']}"
        )


def add_movies(movies):
    """2. Add a new movie by fetching its details from the OMDb API."""
    while True:
        new_title = get_nonempty_input("\nEnter new movie title: ")
        if new_title not in movies:
            break
        print(f"\n{STYLE_ERROR_BG} Error: '{new_title}' already exists! {STYLE_RESET}")

    try:
        movie_data = omdb_api.fetch_movie(new_title)
    except omdb_api.MovieNotFoundError as error:
        print(f"\n{STYLE_ERROR_BG} Error: {error} {STYLE_RESET}")
        return
    except ConnectionError as error:
        print(f"\n{STYLE_ERROR_BG} Error: {error} {STYLE_RESET}")
        return

    storage.add_movie(
        new_title, movie_data["year"], movie_data["rating"], movie_data["poster_url"]
    )


def delete_movies(movies):
    """3. Delete a movie from the database."""
    title_to_delete = get_nonempty_input("\nEnter movie title to delete: ")
    if title_to_delete in movies:
        storage.delete_movie(title_to_delete)
    else:
        print(
            f"\n{STYLE_ERROR_BG} Error: '{title_to_delete}' does not exist! {STYLE_RESET}"
        )


def update_movies(movies):
    """4. Update the rating of an existing movie."""
    title_to_update = get_nonempty_input("\nEnter movie title to update: ")
    if title_to_update in movies:
        new_rating = get_rating_input(f"Enter new rating for '{title_to_update}': ")
        storage.update_movie(title_to_update, new_rating)
    else:
        print(
            f"\n{STYLE_ERROR_BG} Error: '{title_to_update}' does not exist! {STYLE_RESET}"
        )


def show_stats(movies):
    """5. Show database statistics (average, median, best, worst)."""
    if not movies:
        print(f"\n{STYLE_ERROR_BG} Database is empty! {STYLE_RESET}")
        return

    ratings = {title: info["rating"] for title, info in movies.items()}

    # (5.1) Average rating
    average_rating = sum(ratings.values()) / len(ratings)
    print(f"\n{STYLE_CYAN}Average rating:{STYLE_RESET} {average_rating:.1f}")

    # (5.2) Median rating
    sorted_ratings = sorted(ratings.values())
    number_of_movies = len(sorted_ratings)
    middle = number_of_movies // 2

    if number_of_movies % 2 != 0:
        median_rating = sorted_ratings[middle]
    else:
        median_rating = (sorted_ratings[middle - 1] + sorted_ratings[middle]) / 2
    print(f"{STYLE_CYAN}Median rating:{STYLE_RESET}  {median_rating:.1f}")

    # (5.3) Best movie
    highest_rating = sorted_ratings[-1]
    best_movies = [t for t, r in ratings.items() if r == highest_rating]
    print(
        f"{STYLE_CYAN}Highest rated:{STYLE_RESET}  {', '.join(best_movies)} "
        f"({highest_rating:.1f})"
    )

    # (5.4) Worst movie
    lowest_rating = sorted_ratings[0]
    worst_movies = [t for t, r in ratings.items() if r == lowest_rating]
    print(
        f"{STYLE_CYAN}Lowest rated:{STYLE_RESET}   {', '.join(worst_movies)} "
        f"({lowest_rating:.1f})"
    )


def show_random_movie(movies):
    """6. Display a random movie from the database."""
    if not movies:
        print(f"\n{STYLE_ERROR_BG} Database is empty! {STYLE_RESET}")
        return
    movie_titles = list(movies.keys())
    random_title = random.choice(movie_titles)
    print(
        f"\nYour random movie is: {STYLE_CYAN}{random_title}{STYLE_RESET} "
        f"({movies[random_title]['rating']})"
    )


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculates the minimum edit distance between two strings."""
    rows = len(s1) + 1
    cols = len(s2) + 1
    dist = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(1, rows):
        dist[i][0] = i
    for j in range(1, cols):
        dist[0][j] = j

    for col in range(1, cols):
        for row in range(1, rows):
            cost = 0 if s1[row - 1] == s2[col - 1] else 1
            dist[row][col] = min(
                dist[row - 1][col] + 1,
                dist[row][col - 1] + 1,
                dist[row - 1][col - 1] + cost,
            )
    return dist[-1][-1]


def search_movie(movies: dict) -> None:
    """Searches for movies in the database using fuzzy matching."""
    search_query = get_nonempty_input("\nEnter part of movie name: ")

    # Stage 1: Exact match
    for movie in movies:
        if movie.lower() == search_query.lower():
            print(f"Found movie: {STYLE_CYAN}{movie}{STYLE_RESET}")
            return

    # Stage 2: Substring match
    substring_matches = [
        movie for movie in movies if search_query.lower() in movie.lower()
    ]

    if substring_matches:
        for movie in substring_matches:
            print(f"  {STYLE_CYAN}{movie}{STYLE_RESET}")
        return

    # Stage 3: Advanced fuzzy matching
    # Note: Now printed in plain red text without a background block
    print(f'\n{STYLE_RED}Movie "{search_query}" not found. Did you mean:{STYLE_RESET}')

    suggestions = []
    max_error = 3

    for movie in movies:
        movie_lower = movie.lower()
        query_lower = search_query.lower()
        full_dist = levenshtein_distance(query_lower, movie_lower)

        is_partial_fuzzy = False
        query_len = len(query_lower)

        for width in (query_len - 1, query_len, query_len + 1):
            if width < 2:
                continue
            for i in range(len(movie_lower) - width + 1):
                sub_part = movie_lower[i: i + width]
                if levenshtein_distance(query_lower, sub_part) <= 1:
                    is_partial_fuzzy = True
                    break
            if is_partial_fuzzy:
                break

        if full_dist <= max_error or is_partial_fuzzy:
            suggestions.append(movie)

    if suggestions:
        for s in suggestions:
            print(f"  {STYLE_CYAN}{s}{STYLE_RESET}")
    else:
        print(f"  {STYLE_DIM}No similar movies found.{STYLE_RESET}")


def sort_movies(movies):
    """8. Sort movies by rating in descending order."""
    if not movies:
        print(f"\n{STYLE_ERROR_BG} Database is empty! {STYLE_RESET}")
        return

    sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
    print()
    for title, info in sorted_movies:
        print(f"  {STYLE_CYAN}{title:<40}{STYLE_RESET} | Rating: {info['rating']}")


def sort_movies_by_year(movies):
    """10. Sort movies chronologically, newest or oldest first."""
    if not movies:
        print(f"\n{STYLE_ERROR_BG} Database is empty! {STYLE_RESET}")
        return

    newest_first = get_yes_no_input("\nDo you want the latest movies first? (Y/N): ")

    sorted_movies = sorted(
        movies.items(), key=lambda x: x[1]["year"], reverse=newest_first
    )
    print()
    for title, info in sorted_movies:
        print(
            f"  {STYLE_CYAN}{title:<40}{STYLE_RESET} | "
            f"Year: {info['year']} | Rating: {info['rating']}"
        )


def filter_movies(movies):
    """11. Filter movies by minimum rating, start year and/or end year."""
    if not movies:
        print(f"\n{STYLE_ERROR_BG} Database is empty! {STYLE_RESET}")
        return

    min_rating = get_optional_float_input(
        "\nEnter minimum rating (leave blank for no minimum rating): "
    )
    start_year = get_optional_int_input(
        "Enter start year (leave blank for no start year): "
    )
    end_year = get_optional_int_input("Enter end year (leave blank for no end year): ")

    filtered_movies = []
    for title, info in movies.items():
        if min_rating is not None and info["rating"] < min_rating:
            continue
        if start_year is not None and info["year"] < start_year:
            continue
        if end_year is not None and info["year"] > end_year:
            continue
        filtered_movies.append((title, info))

    print(f"\n{STYLE_CYAN}Filtered Movies:{STYLE_RESET}")
    if not filtered_movies:
        print(f"  {STYLE_DIM}No movies match the given criteria.{STYLE_RESET}")
        return
    for title, info in filtered_movies:
        print(f"  {STYLE_CYAN}{title} ({info['year']}):{STYLE_RESET} {info['rating']}")


def create_rating_histogram(movies):
    """9. Create and save a rating histogram using matplotlib."""
    if not movies:
        print(f"\n{STYLE_ERROR_BG} Database is empty! {STYLE_RESET}")
        return

    filename = colored_input("\nEnter a filename (e.g. histogram.png): ").strip()
    if not filename:
        print(f"\n{STYLE_ERROR_BG} Error: Filename cannot be empty! {STYLE_RESET}")
        return

    ratings = [info["rating"] for info in movies.values()]
    custom_bins = [x * 0.5 for x in range(2, 21)]

    plt.hist(
        ratings,
        bins=custom_bins,
        edgecolor="black",
        rwidth=0.8,
        linewidth=1,
        color="lightblue",
    )

    plt.title("Distribution of Movie Ratings")
    plt.xlabel("Ratings")
    plt.ylabel("Number of Movies")
    plt.xticks(range(1, 11))

    try:
        plt.savefig(filename)
        print(
            f"\n{STYLE_SUCCESS_BG} Histogram successfully saved as '{filename}'. {STYLE_RESET}"
        )
    except Exception as error:
        print(f"\n{STYLE_ERROR_BG} An error occurred: {error} {STYLE_RESET}")
    finally:
        plt.close()


def serialize_movie(title, info):
    """Builds one <li> movie-card entry for the website's movie grid."""
    poster_url = info.get("poster_url") or ""
    return (
        '<li>\n'
        '    <div class="movie">\n'
        f'        <img class="movie-poster" src="{poster_url}" title="{title}"/>\n'
        f'        <div class="movie-title">{title}</div>\n'
        f'        <div class="movie-year">{info["year"]}</div>\n'
        '    </div>\n'
        '</li>\n'
    )


def generate_website(movies):
    """12. Generate index.html from the template, listing all movies."""
    with open("index_template.html", "r") as file:
        html_template = file.read()

    movie_grid = ""
    for title, info in movies.items():
        movie_grid += serialize_movie(title, info)

    html_output = html_template.replace("__TEMPLATE_TITLE__", "My Movie App")
    html_output = html_output.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

    with open("index.html", "w") as file:
        file.write(html_output)

    print(f"\n{STYLE_SUCCESS_BG} Website was generated successfully. {STYLE_RESET}")


if __name__ == "__main__":
    main()
