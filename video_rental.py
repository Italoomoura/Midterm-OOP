class Movie:
    """Represents a movie in the store."""

    def __init__(self, title, genre, release_year):
        self.title = title
        self.genre = genre
        self.release_year = release_year
        self.is_rented = False

    def __str__(self):
        status = "Rented" if self.is_rented else "Available"
        return f"{self.title} ({self.release_year}) - {self.genre} [{status}]"


class Customer:
    """Represents a customer and keeps track of the movies they rented."""

    def __init__(self, name):
        self.name = name
        self.rented_movies = []

    def __str__(self):
        titles = ", ".join(m.title for m in self.rented_movies) or "No movies rented"
        return f"{self.name}: {titles}"


class VideoStore:
    """Manages the catalog of movies and the list of customers."""

    def __init__(self):
        self.movies = {}        # title   -> Movie
        self.customers = {}     # name    -> Customer

    # creation
    def add_movie(self, title, genre, release_year):
        if title in self.movies:
            raise ValueError(f"Movie '{title}' already exists.")
        self.movies[title] = Movie(title, genre, release_year)

    def add_customer(self, name):
        if name in self.customers:
            raise ValueError(f"Customer '{name}' already exists.")
        self.customers[name] = Customer(name)

    # rental logic
    def rent_movie(self, title, customer_name):
        movie = self._get_movie(title)
        customer = self._get_customer(customer_name)

        if movie.is_rented:
            raise ValueError(f"'{title}' is already rented.")

        movie.is_rented = True
        customer.rented_movies.append(movie)

    def return_movie(self, title, customer_name):
        movie = self._get_movie(title)
        customer = self._get_customer(customer_name)

        if movie not in customer.rented_movies:
            raise ValueError(f"{customer_name} did not rent '{title}'.")

        movie.is_rented = False
        customer.rented_movies.remove(movie)

    # display
    def display_movies(self):
        print("All movies:")
        for movie in self.movies.values():
            print(f"  {movie}")

    def display_rented_movies(self):
        print("Rented movies:")
        rented = [m for m in self.movies.values() if m.is_rented]
        if not rented:
            print("  None")
        for movie in rented:
            print(f"  {movie}")

    def display_customer_rentals(self, customer_name):  # BONUS
        customer = self._get_customer(customer_name)
        print(f"Movies rented by {customer.name}:")
        if not customer.rented_movies:
            print("  None")
        for movie in customer.rented_movies:
            print(f"  {movie}")

    # helpers
    def _get_movie(self, title):
        if title not in self.movies:
            raise KeyError(f"Movie '{title}' not found.")
        return self.movies[title]

    def _get_customer(self, name):
        if name not in self.customers:
            raise KeyError(f"Customer '{name}' not found.")
        return self.customers[name]


if __name__ == "__main__":
    store = VideoStore()

    # 1995 catalog
    store.add_movie("Toy Story", "Animation", 1995)
    store.add_movie("Pulp Fiction", "Crime", 1994)
    store.add_movie("The Lion King", "Animation", 1994)
    store.add_movie("Forrest Gump", "Drama", 1994)

    store.add_customer("Alice")
    store.add_customer("Bob")

    store.display_movies()

    print("\nRentals")
    store.rent_movie("Toy Story", "Alice")
    store.rent_movie("Pulp Fiction", "Alice")
    store.rent_movie("Forrest Gump", "Bob")

    store.display_rented_movies()
    store.display_customer_rentals("Alice")

    print("\nError handling")
    try:
        store.rent_movie("Toy Story", "Bob")    # already rented
    except ValueError as e:
        print("Error:", e)

    try:
        store.rent_movie("Titanic", "Bob")      # does not exist
    except KeyError as e:
        print("Error:", e)

    print("\nReturn")
    store.return_movie("Toy Story", "Alice")
    store.display_rented_movies()