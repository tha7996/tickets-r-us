
# Import the sqlite3 library
import sqlite3
# Used to validate datetimes when inserting
import datetime
#hashing
import hashlib



# Database for project
DATABASE = 'ticketsrus.db'
NUMBER_MAIN_MENU_OPTIONS = 3
NUMBER_ADMIN_MENU_OPTIONS = 5

# Connect to database
connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

# Foregin key functoinality disabled by default. This turns them on
connection.execute("PRAGMA foreign_keys = ON")


# Create tables for tickets r us database


cursor.execute("""CREATE TABLE IF NOT EXISTS admin_password(hashed_password TEXT NOT NULL)""")
connection.commit()
#password=bcrypt.hashpw('1234', bcrypt.gensalt())
#cursor.execute("""INSERT INTO admin_password(hashed_password) VALUES ({})""".format(password))
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

    cursor = connection.execute("SELECT movie_id, movie_name FROM movies")
    movies = cursor.fetchall()
    # Used to keep track of number of movies, and refer to id by index in below list
    i=1
    # Print movies
    for movie in movies:
        print("   {0}) {1}".format(i,movie[1]))
        i+=1
    print("   {}) CANCEL BOOKING".format(i))

    # First, get placement of movie in list
    movie_number = get_valid_option("Enter movie (number): ", i)
    # Get movie id from this
    if movie_number == i:
        print("Booking cancelled.\n")
        return
    else:
        movie_id = movies[movie_number-1][0]

    # ---
    # Get theatre
    # ---

    print("Movie selected. Please select a theatre showing this movie: ")

    #get theatres that show this movie
    cursor = connection.execute("""SELECT theatres.theatre_id, theatres.theatre_name 
                                   FROM theatres JOIN showtimes 
                                   ON theatres.theatre_id = showtimes.theatre_id 
                                   WHERE showtimes.movie_id = {}""".format(movie_id))
    theatres = cursor.fetchall()

    i=1
    # Print theatres
    for theatre in theatres:
        print("   {0}) {1}".format(i,theatre[1]))
        i+=1
        
    if i==1:
        print("Sorry! This movie is not showing at any theatres. Booking automatically cancelled.\n")
        return
    
    print("   {}) CANCEL BOOKING".format(i))

    # First, get placement of movie in list
    theatre_number = get_valid_option("Enter theatre (number): ", i)
    # Get theatre id from this
    if theatre_number == i:
        print("Booking cancelled.\n")
        return  
    else:
        theatre_id = theatres[theatre_number-1][0]

    # ---
    # Get showtime
    # ---

    print("Theatre selected. Please select a showtime for this movie: ")

    #get showtimes based on theatre and movie
    cursor = connection.execute("""SELECT showtimes.showtime_id, showtimes.showtime_showtime, showtimes.showtime_price, showtimes.showtime_seats_left
                                   FROM showtimes 
                                   WHERE showtimes.theatre_id={0} AND showtimes.movie_id = {1}""".format(theatre_id, movie_id))
    showtimes = cursor.fetchall()
    
    i=1
    # Print showtimes
    for showtime in showtimes:
        print("   {0}) Time: {1} | Price: ${2} | Seats left: {3}".format(i,showtime[1],showtime[2],showtime[3]))
        i+=1
    print("   {}) CANCEL BOOKING".format(i))

    # First, get placement of movie in list
    showtime_number = get_valid_option("Enter showtime (number): ", i)
    
    if showtime_number == i:
        print("Booking cancelled.\n")
        return     

    # --- 
    # Get number of seats
    # ---

    print("Please select number of seats required (e.g. '4') OR enter '0' to cancel: ")
    number_seats_invalid=True
    while number_seats_invalid:

        #tries to get a valid input (i.e. an integer)
        try:
            number_seats = int(input("Number of seats: "))
            if number_seats>showtime[3]:
                print("Sorry! There are not that many seats left")
            elif number_seats==0:
                print("Booking cancelled.\n")
                return
            elif number_seats<0:
                print("ERROR: Input invalid")
            else:
                new_seats_left = showtime[3]-number_seats
                
                number_seats_invalid=False       
        except:
            print("ERROR: Input invalid.")  



    print("Confirm booking for: \n   Movie: " + movies[movie_number-1][1] +
                               "\n   Theatre: " + theatres[theatre_number-1][1] +
                               "\n   Showtime: " + showtimes[showtime_number-1][1] +
                               "\n   Number of seats: " + str(number_seats) +
                               "\n   Total Price: $" + str(number_seats*showtimes[showtime_number-1][2]))

    confirmation = get_valid_option("Confirm sale (1=YES, 2=NO): ", 2)
    if confirmation==1:
        cursor.execute("UPDATE showtimes SET showtime_seats_left={0} WHERE showtime_id={1}".format(new_seats_left,showtime[0]))
        connection.commit()
        print("Booking confirmed.\n")
    else:
        print("Booking cancelled.\n")
        

def add_movie():
    '''Add movie to database'''
    
    print("\nAdd movie.")
    movie_name_invalid = True
    
    while movie_name_invalid:
        movie_name = input("Please enter movie name: ")
        # Make sure user entered valid input
        if movie_name!='':
            # SQL will fail if name already exists. Thus, use try/except to catch this
            try:
                cursor.execute("INSERT INTO movies (movie_name) VALUES ('{}')".format(movie_name))
                movie_name_invalid = False
            except:
                print("ERROR: Movie with this name already exists")
        else:
            print("ERROR: Please enter a valid movie name")
            
    connection.commit()
    print("Movie successfully added")
                
    
def add_showtime():
    '''Add a showtime for movie'''
    
    
    print("\nAdd showtime. Please select movie for this showtime:")

    # ---
    # Get movie
    # --- 

    cursor = connection.execute("SELECT movie_id, movie_name FROM movies")
    movies = cursor.fetchall()

    i=1
    # Print movies
    for movie in movies:
        print("   {0}) {1}".format(i,movie[1]))
        i+=1

    # First, get placement of movie in list
    movie_number = get_valid_option("Enter movie (number): ", i-1)
    # Get movie id from this
    movie_id = movies[movie_number-1][0]

    # ---
    # Get theatre
    # ---

    print("Movie selected. Please select a theatre for this showtime: ")

    #get theatres that show this movie
    cursor = connection.execute("SELECT theatres.theatre_id, theatres.theatre_name FROM theatres")
    theatres = cursor.fetchall()

    i=1
    # Print theatres
    for theatre in theatres:
        print("   {0}) {1}".format(i,theatre[1]))
        i+=1

    # First, get placement of theatre in list
    theatre_number = get_valid_option("Enter theatre (number): ", i-1)
    # Get theatre id from this
    theatre_id = theatres[theatre_number-1][0] 
    
    # ---
    # Get Price
    # ---
    
    price_invalid = True
    while price_invalid:
        try:
            price = int(input("Please enter price for this showtime: "))
    
            #checks if input is within range of valid options, and returns input if it is
            if price > 0:
                price_invalid = False
            else:
                print("ERROR: Input invalid.")
        #if number not inserted
        except:
            print("ERROR: Input invalid.")
            
    # ---
    # Get time
    # ---
    
    showtime_invalid = True
    while showtime_invalid:
        showtime = input("Please enter showtime in YYYY-MM-DD HH:MM format: ")
        try:
            # Check that date inputted in correct format
            if showtime != datetime.datetime.strptime(showtime, "%Y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M'):
                print("ERROR: Invalid input.")
            else:
                # Check that showtime is after current time
                if datetime.datetime.strptime(showtime, "%Y-%m-%d %H:%M") > datetime.datetime.now():
                    showtime_invalid = False
                else:
                    print("ERROR: Invalid input.")
        except ValueError:
            print("ERROR: Invalid input.")        
    
    
    print("Confirm addition of showtime for: \n   Movie: " + movies[movie_number-1][1] +
                                            "\n   Theatre: " + theatres[theatre_number-1][1] +
                                            "\n   Price: $" + str(price) +
                                            "\n   Showtime: " + showtime)   
    
    confirmation = get_valid_option("Confirm addition of showtime (1=YES, 2=NO): ", 2)
    if confirmation==1:
        
        # Get number of seats by theatre
        cursor = connection.execute("SELECT theatres.theatre_capacity FROM theatres WHERE theatres.theatre_id={}".format(theatres[theatre_number-1][0]))
        seats = cursor.fetchall()[0][0]
        
        # Insert showtime into database
        cursor.execute("""INSERT INTO showtimes (movie_id, theatre_id, showtime_showtime, showtime_price, showtime_seats_left)
                          VALUES ({0}, {1}, '{2}', {3}, {4})""".format(movies[movie_number-1][0], theatres[theatre_number-1][0], showtime, price, seats))

    else:
        print("Showtime addition cancelled.\n")  
        return
            
    connection.commit()
    print("Showtime successfully added") 


def delete_movie():
    '''Delete movie from database'''
    
    print("\nDelete movie. Please select a movie to delete: ")
    
    # Get movie to delete
    
    cursor = connection.execute("SELECT movie_id, movie_name FROM movies")
    movies = cursor.fetchall()
    i=1
    for movie in movies:
        print("   {0}) {1}".format(i,movie[1]))
        i+=1
    movie_number = get_valid_option("Enter movie (number): ", i-1)
    movie_id = movies[movie_number-1][0]
    movie_name = movies[movie_number-1][1]
    
    # Get number of showtimes that will also be deleted.
    cursor = connection.execute("SELECT showtime_id FROM showtimes WHERE movie_id={}".format(movie_id))
    number_showtimes_affected = len(cursor.fetchall())
    
    confirmation = get_valid_option("Confirm deletion of {}. This will also remove {} showtimes. (1=YES, 2=NO): ".format(movie_name, number_showtimes_affected), 2)
    if confirmation==1:
        
        # Delete movie
        connection.execute("DELETE FROM movies WHERE movie_id={}".format(movie_id))
        
    else:
        print("Movie deletion cancelled.\n")  
        return    
    
    print("{} deleted. {} showtime(s) has also been removed".format(movie_name, number_showtimes_affected))
    connection.commit()

    
def delete_showtime():
    '''Delete showtime from database'''
    
    print("\nDelete showtime. Please select showtime to delete:")
    
    # Display showtimes
    
    # Get all showtimes, wiht movie and theatre names from foreign ids
    cursor = connection.execute("""SELECT showtimes.showtime_id, movies.movie_name, theatres.theatre_name, showtimes.showtime_showtime, showtimes.showtime_price, showtimes.showtime_seats_left 
                                   FROM showtimes 
                                      JOIN movies ON showtimes.movie_id=movies.movie_id
                                      JOIN theatres ON showtimes.theatre_id=theatres.theatre_id""")
    showtimes = cursor.fetchall()
    i=1
    for showtime in showtimes:
        print("   {0}) Movie: {1} | Theatre: {2} | Time: {3} | Price: ${4} | Seats left: {5}".format(i,showtime[1],showtime[2],showtime[3],showtime[4],showtime[5]))
        i+=1

    # First, get placement of movie in list
    showtime_number = get_valid_option("Enter showtime (number): ", i-1)
    showtime_id = showtimes[showtime_number-1][0]
    
    connection.execute("DELETE FROM showtimes WHERE showtime_id={}".format(showtime_id))
    connection.commit()
    
    print("Showtime deleted.")
    


def admin():
    
    print("\nAccessing admin section. ")
    
    loggedOut=True
    
    hashed_pass = connection.execute("SELECT hashed_password FROM admin_password")
    hashed_pass = hashed_pass.fetchall()[1][0]    
    
    while loggedOut:
        password = input("Please enter password: ")
        
        hashed_user_pass = hashlib.sha256(password.encode())
        if( hashed_user_pass.hexdigest()==hashed_pass):
            loggedOut = False
        else:
            print("Incorrect password. Please try again.")
            
            
    admin=True
    
    while(admin):
    
        print("\nAdmin section accessed.")
        print("Options: \n   1) Add movie" +
                       "\n   2) Add showtime" +
                       "\n   3) Delete movie" +
                       "\n   4) Delete showtime" +
                       "\n   5) Exit admin")
        option_selected = get_valid_option("Enter option (number): ", NUMBER_ADMIN_MENU_OPTIONS)
        
        if option_selected == 1:
            add_movie()
        elif option_selected == 2:
            add_showtime()
        elif option_selected == 3:
            delete_movie()
        elif option_selected == 4:
            delete_showtime()
        else:
            admin=False
    
    

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


