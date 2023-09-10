import sqlite3
with open('D:\Download\Github仓库\Python-examples\Exercise\exercise 2\stephen_king_adaptations.txt', 'r') as file:
    list = file.readlines()
    stephen_king_adaptations_list = []
    for i in list:
        stephen_king_adaptations_list.append(i.strip())
    print(stephen_king_adaptations_list)

    conn = sqlite3.connect('stephen_king_adaptations.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table
             (movieID INT PRIMARY KEY NOT NULL,
             movieName TEXT NOT NULL,
             movieYear INT NOT NULL,
             imdbRating REAL NOT NULL);''')
    

    for i, movie in enumerate(stephen_king_adaptations_list):
        movie_details = movie.split(',')
        print(movie_details[0])
        c.execute("INSERT INTO stephen_king_adaptations_table (movieID, movieName, movieYear, imdbRating) VALUES (?,?,?,?)", (i+1, movie_details[1], int(movie_details[2]), float(movie_details[3])))

    while True:
        print("\nPlease select an option:")
        print("1. Search for a movie by name")
        print("2. Search for a movie by year")
        print("3. Search for a movie by rating")
        print("4. Quit\n")
        option = input()
   
        if option == '1':
            movie_name = input("\nPlease enter the name of the movie: ")
            c.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName=?", (movie_name,))
            movie_details = c.fetchone()
            if movie_details:
                print("Movie ID:", movie_details[0])
                print("Movie Name:", movie_details[1])
                print("Movie Year:", movie_details[2])
                print("IMDB Rating:", movie_details[3])
                print("\n")
            else:
                print("No such movie exists in our database.\n")

        elif option == '2':
            year = input("\nPlease enter the year: ")
            c.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (year,))
            movies = c.fetchall()
            if movies:
                for movie in movies:
                    print("Movie ID:", movie[0])
                    print("Movie Name:", movie[1])
                    print("Movie Year:", movie[2])
                    print("IMDB Rating:", movie[3])
                    print("\n")
            else:
                print("No movies were found.\n")

        elif option == '3':
            rating = input("\nPlease enter the rating: ")
            c.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating>=?", (rating,))
            movies = c.fetchall()
            if movies:
                for movie in movies:
                    print("Movie ID:", movie[0])
                    print("Movie Name:", movie[1])
                    print("Movie Year:", movie[2])
                    print("IMDB Rating:", movie[3])
                    print("\n")
            else:
                print("There is no such movie have the same rating or higher.\n")
    
        elif option == '4':
            break

        print("Do you want to query other message?(Yes or No)")
        option1 = input()

        if option1 == 'No':
            break
        
conn.close()
