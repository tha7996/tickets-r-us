# Import the sqlite3 library
import  sqlite3


# Database for project
DATABASE = 'ticketsrus.db'

# Connect to database
connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()

# Foregin key functoinality disabled by default. This turns them on
connection.execute("PRAGMA foreign_keys = ON")


# Create tables for tickets r us database

# Movies table
cursor.execute("""CREATE TABLE IF NOT EXISTS movies(
                        movie_id INTEGER PRIMARY KEY,
                        movie_name TEXT UNIQUE NOT NULL
                        )""")

# Theatres table                     
cursor.execute("""CREATE TABLE IF NOT EXISTS theatres(
                        theatre_id INTEGER PRIMARY KEY,
                        theatre_name TEXT UNIQUE NOT NULL,
                        theatre_capacity INTEGER NOT NULL
                        )""")

# Showtimes joining table
cursor.execute("""CREATE TABLE IF NOT EXISTS showtimes(
                        showtime_id INTEGER PRIMARY KEY,
                        showtime_showtime DATETIME NOT NULL,
                        showtime_price INTEGER NOT NULL,
                        movie_id INTEGER NOT NULL,
                        theatre_id INTEGER NOT NULL,
                            FOREIGN KEY(movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
                            FOREIGN KEY(theatre_id) REFERENCES theatres(theatre_id) ON DELETE CASCADE
                        )""")

# Set up theatres
cursor.execute("""INSERT INTO theatres (theatre_name, theatre_capacity) VALUES 
                        ('Mann Theatre', 80), 
                        ('The Academy', 120), 
                        ('Green Fern Theatre', 100)""")
connection.commit()
                        



