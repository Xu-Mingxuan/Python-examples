import sqlite3

conn = sqlite3.connect('library.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Books
                  (BookID TEXT PRIMARY KEY,
                   Title TEXT,
                   Author TEXT,
                   ISBN TEXT,
                   Status TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Users
                  (UserID TEXT PRIMARY KEY,
                   Name TEXT,
                   Email TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Reservations
                  (ReservationID TEXT PRIMARY KEY,
                   BookID TEXT,
                   UserID TEXT,
                   ReservationDate TEXT,
                   FOREIGN KEY(BookID) REFERENCES Books(BookID),
                   FOREIGN KEY(UserID) REFERENCES Users(UserID))''')


def add_book():
    book_id = input("Enter BookID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = input("Enter Status: ")

    c.execute("INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, ?)",
                   (book_id, title, author, isbn, status))
    conn.commit()

def find_book_by_id():
    book_id = input("Enter BookID: ")

    c.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Reservations.ReservationDate,
                      Users.UserID, Users.Name, Users.Email
                      FROM Books LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID
                      WHERE Books.BookID = ?''', (book_id,))
    result = c.fetchone()

    if result:
        book_id, title, author, isbn, reservation_date, user_id, name, email = result
        print("BookID:", book_id)
        print("Title:", title)
        print("Author:", author)
        print("ISBN:", isbn)
        if reservation_date:
            print("Reservation Date:", reservation_date)
            print("Reserved by:")
            print("User ID:", user_id)
            print("Name:", name)
            print("Email:\n", email)
        else:
            print("Not reserved\n")
    else:
        print("Book not found\n")

def find_reservation_status():
    search_text = input("Enter search text: ")

    if search_text.startswith('LB'): 
        book_id = search_text
        c.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
        result = c.fetchone()

        if result:
            book_id, title, author, isbn, status = result
            print("BookID:", book_id)
            print("Title:", title)
            print("Author:", author)
            print("ISBN:", isbn)
            print("Status:\n", status)
        else:
            print("Book not found\n")
    elif search_text.startswith('LU'): 
        user_id = search_text
        c.execute("SELECT * FROM Users WHERE UserID = ?", (user_id,))
        result = c.fetchone()

        if result:
            user_id, name, email = result
            print("User ID:", user_id)
            print("Name:", name)
            print("Email:\n", email)
        else:
            print("User not found\n")
    elif search_text.startswith('LR'):
        reservation_id = search_text
        c.execute("SELECT * FROM Reservations WHERE ReservationID = ?", (reservation_id,))
        result = c.fetchone()

        if result:
            reservation_id, book_id, user_id, reservation_date = result
            print("Reservation ID:", reservation_id)
            print("Book ID:", book_id)
            print("User ID:", user_id)
            print("Reservation Date:\n", reservation_date)
        else:
            print("Reservation not found\n")
    else:
        title = search_text
        c.execute("SELECT * FROM Books WHERE Title = ?", (title,))
        result = c.fetchone()

        if result:
            book_id, title, author, isbn, status = result
            print("BookID:", book_id)
            print("Title:", title)
            print("Author:", author)
            print("ISBN:", isbn)
            print("Status:\n", status)
        else:
            print("Book not found\n")


def find_all_books():
    c.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Reservations.ReservationDate,
                      Users.UserID, Users.Name, Users.Email
                      FROM Books LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID''')
    results = c.fetchall()

    for result in results:
        book_id, title, author, isbn, reservation_date, user_id, name, email = result
        print("BookID:", book_id)
        print("Title:", title)
        print("Author:", author)
        print("ISBN:\n", isbn)
        if reservation_date:
            print("Reservation Date:", reservation_date)
            print("Reserved by:")
            print("User ID:", user_id)
            print("Name:", name)
            print("Email:\n", email)
        else:
            print("Not reserved\n")
        print("---")


def update_book():
    book_id = input("Enter BookID: ")
    new_status = input("Enter new Status: ")

    c.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (new_status, book_id))
    c.execute("UPDATE Reservations SET ReservationDate = NULL WHERE BookID = ?", (book_id,))
    conn.commit()
    print("Book details updated")


def delete_book():
    book_id = input("Enter BookID: ")

    c.execute("SELECT * FROM Reservations WHERE BookID = ?", (book_id,))
    result = c.fetchone()

    if result:
        c.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
    c.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
    conn.commit()
    print("Book deleted\n")


while True:
    print("Library Management System")
    print("1. Add a new book to the database")
    print("2. Find a book's detail based on BookID")
    print("3. Find a book's reservation status based on search text")
    print("4. Find all the books in the database")
    print("5. Modify/update book details based on its BookID")
    print("6. Delete a book based on its BookID")
    print("7. Exit")
    choice = input("Enter your choice (1-7): ")

    if choice == '1':
        add_book()
    elif choice == '2':
        find_book_by_id()
    elif choice == '3':
        find_reservation_status()
    elif choice == '4':
        find_all_books()
    elif choice == '5':
        update_book()
    elif choice == '6':
        delete_book()
    elif choice == '7':
        break
    else:
        print("Invalid choice. Please try again.")


conn.close()