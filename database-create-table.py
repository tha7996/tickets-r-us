# Import the sqlite3 library
import  sqlite3


# Database for project
DATABASE = 'ticketsrus.db'
NUMBER_MAIN_MENU_OPTIONS = 3

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
#cursor.execute("""INSERT INTO theatres (theatre_name, theatre_capacity) VALUES 
                        #('Mann Theatre', 80), 
                        #('The Academy', 120), 
                        #('Green Fern Theatre', 100)""")
#connection.commit()

#cursor.execute("""INSERT INTO movies (movie_name) VALUES 
                        #('Kill Bill'), 
                        #('Cars'), 
                        #('Wolf of Wall Street')""")
#connection.commit()

#cursor.execute("""INSERT INTO showtimes (movie_id, theatre_id, showtime_showtime, showtime_price, showtime_seats_left) VALUES 
                        #(1, 1, '2021-11-01 10:00:00',10, 80), 
                        #(1, 2, '2021-11-01 12:00:00', 20,120), 
                        #(3, 2, '2021-11-02 17:30:00', 15,100)""")
#connection.commit()



def get_valid_option(message, option_max_value):
    '''Get a valid option from an option selection i.e. get an integer in the range of options'''
    
    #loops until an option is valid (i.e. an integer within range of options), and then returns
    option_invalid = True
    while option_invalid:
        #tries to get a valid input (i.e. an integer)
        try:
            option_selected = int(input(message))
            
            #checks if input is within range of valid options, and returns input if it is
            if option_selected in range(1, option_max_value + 1):
                return option_selected
            else:
                print("ERROR: Input invalid.")
        #if input        
        except:
            print("ERROR: Input invalid.")




def make_booking():
    '''make a booking'''
    
    print("\nMake a booking. Please select a movie: ")
    
    # ---
    # Get movie
    # --- 
    
    movies = cursor.execute("SELECT movie_id, movie_name FROM movies")
    # Used to keep track of number of movies, and refer to id by index in below list
    i=1
    movie_ids=[]
    # Print movies
    for movie in movies:
        print("   {0}) {1}".format(i,movie[1]))
        movie_ids.append(movie[0])
        i+=1
        
    # First, get placement of movie in list
    movie_number = get_valid_option("Enter movie (number): ", i)
    # Get movie id from this
    movie_id = movie_ids[movie_number-1]
    
    # ---
    # Get theatre
    # ---
    
    print("Movie selected. Please select a theatre showing this movie: ")
    
    #get theatres that show this movie
    theatres = cursor.execute("""SELECT theatres.theatre_id, theatres.theatre_name 
                                 FROM theatres JOIN showtimes 
                                 ON theatres.theatre_id = showtimes.theatre_id 
                                 WHERE showtimes.movie_id = {}""".format(movie_id))
    # Used to keep track of number of theatres, and refer to id by index in below list
    i=1
    theatre_ids=[]
    # Print theatres
    for theatre in theatres:
        print("   {0}) {1}".format(i,theatre[1]))
        theatre_ids.append(theatre[0])
        i+=1
        
    # First, get placement of movie in list
    theatre_number = get_valid_option("Enter theatre (number): ", i)
    # Get theatre id from this
    theatre_id = theatre_ids[theatre_number-1]    
    
    # ---
    # Get showtime
    # ---
    
    print("Theatre selected. Please select a showtime for this movie: ")
    
    #get showtimes based on theatre and movie
    showtimes = cursor.execute("""SELECT showtimes.showtime_id, showtimes.showtime_showtime, showtimes.showtime_price, showtimes.showtime_seats_left
                                 FROM showtimes 
                                 WHERE showtimes.theatre_id={0} AND showtimes.movie_id = {1}""".format(theatre_id, movie_id))
    # Used to keep track of showtimes
    i=1
    showtime_ids=[]
    # Print showtimes
    for showtime in showtimes:
        print("   {0}) Time: {1} | Price: ${2} | Seats left: {3}".format(i,showtime[1],showtime[2],showtime[3]))
        showtime_ids.append(showtime[0])
        i+=1
        
    # First, get placement of movie in list
    showtime_number = get_valid_option("Enter showtime (number): ", i)
    
    # --- 
    # Get number of seats
    # ---
    
    print("Please select number of seats required (number): ")
    number_seats_invalid=True
    while number_seats_invalid:
            
        #tries to get a valid input (i.e. an integer)
        try:
            number_seats = int(input("Number of seats: "))
            if number_seats>showtime[3]:
                print("Sorry! There are not that many seats left")
            elif number_seats<=0:
                print("ERROR: Input invalid")
            else:
                new_seats_left = showtime[3]-number_seats
                cursor.execute("UPDATE showtimes SET showtime_seats_left={0} WHERE showtime_id={1}".format(new_seats_left,showtime[0]))
                connection.commit()
                number_seats_invalid=False       
        except:
            print("ERROR: Input invalid.")  
            
    
    
    print("Confirm booking for: \n   Movie: "+movie_name
                               "\n   Theatre: {}" +
                               "\n   Showtime: {}" +
                               "\n   Number of seats: {}" +
                               "\n   Total Price: {}

    print("Type YES to confirm, NO to cancel")

    
    
    
    
    
    

def admin():
    pass

program_running = True
while program_running:
    
    print("Options: \n   1) Make Booking" +
                   "\n   2) Admin Area" +
                   "\n   3) Quit program")
    
    #Get inputted option
    option_selected = get_valid_option("Enter option (number): ", NUMBER_MAIN_MENU_OPTIONS)
    
    #Calls appropiate function based on input
    if option_selected == 1:
        make_booking()
    elif option_selected == 2:
        admin()
        
    #End program by breaking while loop
    else:
        print("Program Ended.")
        program_running = False
    
                        



