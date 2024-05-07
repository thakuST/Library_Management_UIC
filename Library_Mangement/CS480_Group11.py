# WE HAVE USED DATABASE.SQL as our database for Postgres
# CS 480, Project - Group 11, Spring 2024
# Authors: Sneha Thakur, Justin Thalackan, Shahriar Namvar

import psycopg2
import os
import sys
import datetime

# Connection parameters
hostname = "localhost"  
database = "Library"
username = "postgres"
pwd = "password"
port_id = 5432


#Establishing Connection:
conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id )

#Creating a cursor object using the cursor() method
cur = conn.cursor()

##########################################################################################
# ADDITIONAL FUNCTIONS
##########################################################################################
def getaID():
  cur.execute("SELECT MAX(AddressID) FROM Address")
  num_address = cur.fetchone()[0]
  if num_address == 0 or num_address is None:
    return 0
  else:
    return num_address
##############################################

def getdID(): 
  cur.execute("SELECT MAX(DocID) FROM Document")
  num_doc = cur.fetchone()[0]
  if num_doc == 0 or num_doc is None:
    return 0
  else:
    return num_doc
##############################################

def getpID():
  cur.execute("SELECT MAX(PublisherID) FROM Publisher")
  num_pub = cur.fetchone()[0]
  if num_pub == 0 or num_pub is None:
    return 0
  else:
    return num_pub
##############################################

def getauID():
  cur.execute("SELECT MAX(AuthorID) FROM Author")
  num_auth = cur.fetchone()[0]
  if num_auth == 0 or num_auth is None:
    return 0
  else:
    return num_auth
##############################################

def getcID():
  cur.execute("SELECT MAX(CopyID) FROM Copy")
  num_copy = cur.fetchone()[0]
  if num_copy == 0 or num_copy is None:
    return 0
  else:
    return num_copy
##############################################

def geteID():
  cur.execute("SELECT MAX(CopyID) FROM ElectronicCopy")
  num_ecopy = cur.fetchone()[0]
  if num_ecopy == 0 or num_ecopy is None:
    return 0
  else:
    return num_ecopy
##########################################################################################
##########################################################################################






##########################################################################################
# Librarian Functions
##########################################################################################
def check_librarian(email,pwd):
  cur.execute("SELECT COUNT(*) FROM Librarian WHERE Email = %s AND Password = %s",(email,pwd))
  count = cur.fetchone()[0]
  if count is None or count == 0:
    return False
  else:
    return True
##########################################################################################

def update_doc(DocID):
    cur.execute("SELECT Type FROM Document WHERE DocID = %s", (DocID,))
    type = cur.fetchone()[0]

    action = input("Do you want to update or delete this document? (update/delete): ")

    if action.lower() == 'update':
        if type == 'book':
            doc_title = input("Enter the title of the book: ")
            doc_ISBN = input("Enter the ISBN of the book: ")
            doc_edition = input("Enter the edition of the book: ")
            doc_Num = input("Enter the number of pages of the book: ")
            doc_year = input("Enter the year of publication of the book: ")
            cur.execute("UPDATE Book SET Title = %s, ISBN = %s, Edition = %s, Num_of_Pages = %s WHERE DocID = %s", (doc_title, doc_ISBN, doc_edition, doc_Num, DocID))
            conn.commit()
        elif type == 'magazine':
            doc_title = input("Enter the title of the magazine: ")
            doc_ISBN = input("Enter the ISBN of the magazine: ")
            doc_month = input("Enter the month of the magazine: ")
            doc_name = input("Enter the name of the magazine: ")
            doc_year = input("Enter the year of publication of the magazine: ")
            cur.execute("UPDATE Magazine SET Title = %s, ISBN = %s, Month = %s, Magazine_Name = %s WHERE DocID = %s", (doc_title, doc_ISBN, doc_month, doc_name, DocID))
            conn.commit()
        elif type == 'journal':
            doc_year = input("Enter the year of publication of the Journal Article: ")
            doc_issue = input("Enter the Issue of the Journal Article: ")
            doc_title = input("Enter the Article Title of the Journal Article: ")
            doc_name = input("Enter the Journal Name of the Journal Article: ")
            doc_num = input("Enter the Issue Number of the Journal Article: ")
            cur.execute("UPDATE Journal_Article SET Issue = %s, Article_Title = %s, Journal_Name = %s, Issue_Num = %s WHERE DocID = %s", (doc_issue, doc_title, doc_name, doc_num, DocID))
            conn.commit()
        doc_year = input("Enter the year of publication of the document: ")
        cur.execute("UPDATE Document SET Year = %s WHERE DocID = %s", (doc_year, DocID))
        conn.commit()

    elif action.lower() == 'delete':
        cur.execute("UPDATE Document SET Num_Copies = 0 WHERE DocID = %s", (DocID,))
        conn.commit()
        print("Document deleted successfully.")

    else:
        print("Invalid action. Please choose either 'update' or 'delete'.")
##########################################################################################

def insert_doc(type):
  DocID = getdID()
  DocID +=1
  num_copies = 1
  if type == "b":
    doc_type = "book"
    doc_title = input("Enter the title of the book: ")
    doc_ISBN = input("Enter the ISBN of the book: ")
    doc_edition = input("Enter the edition of the book: ")
    doc_Num = input("Enter the number of pages of the book: ")
    doc_author = input("Enter the author of the book: ")
    doc_publisher = input("Enter the publisher of the book: ")
    doc_year = input("Enter the year of publication of the book: ")
    cur.execute("SELECT COUNT (*) FROM Author WHERE Name = %s ",(doc_author,))
    count = cur.fetchone()[0]
    cur.execute("SELECT COUNT (*) FROM Publisher WHERE Name = %s ",(doc_publisher,))
    count2 = cur.fetchone()[0]
    
    if(count2 == 0 or count is None):
      publisherID = getpID()
      publisherID +=1
      cur.execute("INSERT INTO Publisher (Name,PublisherID) VALUES (%s,%s)",(doc_publisher,publisherID))
      conn.commit()
      cur.execute("INSERT INTO Document (DocID,Year,Type,Num_Copies,PublisherID) VALUES (%s,%s,%s,%s,%s)",(DocID,doc_year,doc_type,num_copies,publisherID))
      conn.commit()
    else:
      cur.execute("SELECT PublisherID FROM Publisher WHERE Name = %s",(doc_publisher,))
      pID = cur.fetchone()[0]
      cur.execute("INSERT INTO Document (DocID,Year,Type,Num_Copies,PublisherID) VALUES (%s,%s,%s,%s,%s)",(DocID,doc_year,doc_type,num_copies,pID))
      conn.commit()
      
      if(count == 0 or count is None):
        authorID = getauID()
        authorID+=1
        cur.execute("INSERT INTO Author (Name,AuthorID,DocID) VALUES (%s,%s,%s)",(doc_author,authorID,DocID))
        conn.commit()
      else:
        authorID = getauID()
        authorID +=1
        cur.execute("INSERT INTO Author (Name,AuthorID,DocID) VALUES (%s,%s,%s)",(doc_author,authorID,DocID))
        conn.commit()     
    cur.execute("INSERT INTO Book (Title,ISBN,Edition,Num_of_Pages,DocID) VALUES (%s,%s,%s,%s,%s)", (doc_title,doc_ISBN,doc_edition,doc_Num,DocID))
    conn.commit()
  elif type == 'm':
    doc_type = "magazine"
    doc_title = input("Enter the title of the magazine: ")
    doc_ISBN = input("Enter the ISBN of the magazine: ")
    doc_month = input("Enter the month of the magazine: ")
    doc_name = input("Enter the name of the magazine: ")
    doc_author = input("Enter the author of the book: ")
    doc_publisher = input("Enter the publisher of the book: ")
    doc_year = input("Enter the year of publication of the book: ")
    cur.execute("SELECT COUNT (*) FROM Author WHERE Name = %s ",(doc_author,))
    count = cur.fetchone()[0]
    cur.execute("SELECT COUNT (*) FROM Publisher WHERE Name = %s ",(doc_publisher,))
    count2 = cur.fetchone()[0]
    
    if(count2 == 0 or count is None):
      publisherID = getpID()
      publisherID +=1
      cur.execute("INSERT INTO Publisher (Name,PublisherID) VALUES (%s,%s)",(doc_publisher,publisherID))
      conn.commit()
      cur.execute("INSERT INTO Document (DocID,Year,Type,Num_Copies,PublisherID) VALUES (%s,%s,%s,%s,%s)",(DocID,doc_year,doc_type,num_copies,publisherID))
      conn.commit()
    else:
      cur.execute("SELECT PublisherID FROM Publisher WHERE Name = %s",(doc_publisher,))
      pID = cur.fetchone()[0]
      cur.execute("INSERT INTO Document (DocID,Year,Type,Num_Copies,PublisherID) VALUES (%s,%s,%s,%s,%s)",(DocID,doc_year,doc_type,num_copies,pID))
      conn.commit()
      
    if(count == 0 or count is None):
      authorID = getauID()
      authorID+=1
      cur.execute("INSERT INTO Author (Name,AuthorID,DocID) VALUES (%s,%s,%s)",(doc_author,authorID,DocID))
      conn.commit()
    else:
      authorID = getauID()
      authorID+=1
      cur.execute("INSERT INTO Author (Name,AuthorID,DocID) VALUES (%s,%s,%s)",(doc_author,authorID,DocID))
      conn.commit()
    cur.execute("INSERT INTO Magazine (Title,ISBN,Month,Magazine_Name_,DocID) VALUES (%s,%s,%s,%s,%s)",(doc_title,doc_ISBN,doc_month,doc_name,DocID))
    conn.commit()
    
  elif type == 'j':
    doc_type = "journal"
    doc_author = input("Enter the author of the Journal Article: ")
    doc_publisher = input("Enter the publisher of the Journal Article: ")
    doc_year = input("Enter the year of publication of the Journal Article: ")
    doc_issue = input("Enter the Issue of the Journal Article: ")
    doc_title = input("Enter the Article Title of the Journal Article: ")
    doc_name = input("Enter the Journal Name of the Journal Article: ")
    doc_num = input("Enter the Issue Number of the Journal Article: ")
    cur.execute("SELECT COUNT (*) FROM Author WHERE Name = %s ",(doc_author,))
    count = cur.fetchone()[0]
    cur.execute("SELECT COUNT (*) FROM Publisher WHERE Name = %s ",(doc_publisher,))
    count2 = cur.fetchone()[0]
    
    if(count2 == 0 or count is None):
      publisherID = getpID()
      publisherID +=1
      cur.execute("INSERT INTO Publisher (Name,PublisherID) VALUES (%s,%s)",(doc_publisher,publisherID))
      conn.commit()
      cur.execute("INSERT INTO Document (DocID,Year,Type,Num_Copies,PublisherID) VALUES (%s,%s,%s,%s,%s)",(DocID,doc_year,doc_type,num_copies,publisherID))
      conn.commit()
    else:
      cur.execute("SELECT PublisherID FROM Publisher WHERE Name = %s",(doc_publisher,))
      pID = cur.fetchone()[0]
      cur.execute("INSERT INTO Document (DocID,Year,Type,Num_Copies,PublisherID) VALUES (%s,%s,%s,%s,%s)",(DocID,doc_year,doc_type,num_copies,pID))
      conn.commit()
      
    if(count == 0 or count is None):
      authorID = getauID()
      authorID +=1
      cur.execute("INSERT INTO Author (Name,AuthorID,DocID) VALUES (%s,%s,%s)",(doc_author,authorID,DocID))
      conn.commit()
    else:
      authorID = getauID()
      authorID +=1
      cur.execute("INSERT INTO Author (Name,AuthorID,DocID) VALUES (%s,%s,%s)",(doc_author,authorID,DocID))
      conn.commit()
    cur.execute("INSERT INTO Journal_Article (Issue,Article_Title,Journal_Name,Issue_Num,DocID) VALUES (%s,%s,%s,%s,%s)",(doc_issue,doc_title,doc_name,doc_num,DocID))
    conn.commit()
##########################################################################################
##########################################################################################






##########################################################################################
# Client Functions
##########################################################################################
def check_client(email,pwd):
  cur.execute("SELECT COUNT(*) FROM Client WHERE Email = %s AND Password = %s",(email,pwd))
  count = cur.fetchone()[0]
  if count is None or count == 0:
    return False
  else:
    return True
##########################################################################################  

def search_documents():
    print("Search Documents: ")
    print("Enter search criteria:")
    attribute = input("Enter attribute to search by (eg: Title, Author, Publisher, ISBN): ")
    value = input("Value to search for: ")
    search_type = input("Search type (Equality, Contains, Search with placeholders)(e/c/s): ").lower()

    if search_type == "e":
        sql_query = f"SELECT * FROM Document WHERE {attribute} = %s"
    elif search_type == "c":
        sql_query = f"SELECT * FROM Document WHERE {attribute} LIKE %s"
        value = f"%{value}%"  
    elif search_type == "s":
        sql_query = f"SELECT * FROM Document WHERE {attribute} LIKE %s"
        value = value.replace("_", "\_")  
        value = value.replace("%", "\%")  
        value = f"%{value}%"  
    else:
        print("Invalid search type.")
        return

    cur.execute(sql_query, (value,))
    results = cur.fetchall()

    if results:
        print("Search Results:")
        for result in results:
            doc_id = result[0]
            num_copies = result[3]
            print(f"Document ID: {doc_id}, Number of Copies: {num_copies}")
    else:
        print("No documents found matching the search criteria.")
##########################################################################################

def return_doc(email,DocID,type):
  if type == "p":
    try:
      cur.execute("SELECT CopyID FROM Copy WHERE Email = %s AND DocID = %s", (email, DocID))
      CopyID = cur.fetchone()[0]
      cur.execute("SELECT LendDate FROM Copy WHERE Email = %s AND DocID = %s", (email, DocID))
      lendDate = cur.fetchone()[0]

      date_input = input("Enter the return date (YYYY-MM-DD)")
      today = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
      borrow_period = today - lendDate
      weeks_overdue = borrow_period.days // 7 - 4  

      late_fee = max(0, weeks_overdue) * 5  
      cur.execute("DELETE FROM Copy WHERE CopyID = %s", (CopyID,))
      if late_fee > 0:
          cur.execute("UPDATE Client SET Account_Bal = Account_Bal + %s WHERE Email = %s", (late_fee, email))

      conn.commit()
      cur.execute("UPDATE Document SET Num_Copies = Num_Copies + 1 WHERE DocID = %s ",(DocID,))
      conn.commit()
      print(f"Document returned successfully. Late fee: ${late_fee}")

    except (Exception, psycopg2.DatabaseError) as error:
      print(f"Error: {error}")
      conn.rollback()    
  elif type == 'e':
    try:
      cur.execute("SELECT ECopyID FROM ElectronicCopy WHERE Email = %s AND DocID = %s", (email, DocID))
      ECopyID = cur.fetchone()[0]
      cur.execute("SELECT LendDate FROM ElectronicCopy WHERE Email = %s AND DocID = %s", (email, DocID))
      lendDate = cur.fetchone()[0]


      date_input = input("Enter the return date (YYYY-MM-DD)")
      today = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
      borrow_period = today - lendDate
      weeks_overdue = borrow_period.days // 7 - 4  

      late_fee = max(0, weeks_overdue) * 5  
      cur.execute("DELETE FROM ElectronicCopy WHERE ElectronicCopyID = %s", (ECopyID,))
      
      if late_fee > 0:
          cur.execute("UPDATE Client SET Account_Bal = Account_Bal + %s WHERE Email = %s", (late_fee, email))

      conn.commit()
      print(f"Document returned successfully. Late fee: ${late_fee}")

    except (Exception, psycopg2.DatabaseError) as error:
      print(f"Error: {error}")
      conn.rollback()
##########################################################################################

def borrow_doc(DocID,email):
    CopyID = getcID()
    CopyID+=1
    date_input = input("Enter the lend date (YYYY-MM-DD)")
    lendDate = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
    cur.execute("INSERT INTO Copy (CopyID,LendDate,DocID,Email) VALUES (%s,%s,%s,%s)",(CopyID,lendDate,DocID,email))
    conn.commit()
##########################################################################################

def payment_method(client_email):
  user_input = input("Would you like to add, delete or update a payment method? (a/d/u): ")
  if user_input == "a":
      user_card = input("Enter the Credit Card Number you would like to add: ")
      user_street = input("Enter the street address: ")
      user_city = input("Enter the city: ")
      user_zip = input("Enter the zip code: ")
      user_state = input("Enter the state: ")
      addressID = getaID()
      addressID +=1
      cur.execute("INSERT INTO Address (AddressID, City, State, Street, Zip_Code) VALUES (%s, %s, %s, %s, %s)",(addressID,user_city,user_state,user_street,user_zip))
      conn.commit()
      cur.execute("INSERT INTO Credit_Card (Card_Num, AddressID, Email) VALUES (%s, %s, %s)",
                  (user_card,addressID, client_email))
      conn.commit()
      print("Payment method added successfully!")
  elif user_input == "d":
      user_card = input("Enter the Credit Card Number you would like to delete: ")
      cur.execute("SELECT AddressID FROM Credit_Card WHERE Card_Num = %s AND Email = %s",(user_card, client_email))
      address = cur.fetchone()
      cur.execute("DELETE FROM Address WHERE AddressID = %s",(address))
      conn.commit()
      cur.execute("DELETE FROM Credit_Card WHERE Card_Num = %s AND Email = %s", (user_card, client_email))
      conn.commit()
      print("Payment method deleted successfully!")
  elif user_input == "u":
    user_card=input("Enter the Credit Card Number you would like to update: ")
    cur.execute("SELECT AddressID FROM Credit_Card WHERE Card_Num = %s AND Email = %s",(user_card, client_email))
    address = cur.fetchone()
    user_street = input("Enter the updated street address: ")  
    user_city = input("Enter the updated city: ")
    user_zip = input("Enter the updated zip code: ")
    user_state = input("Enter the updated state: ")
    cur.execute("UPDATE Address SET Street = %s, City = %s, Zip_Code = %s, State = %s WHERE AddressID = %s",  
            (user_street, user_city, user_zip, user_state, user_card, address))
    conn.commit()
    print("Payment method updated successfully!")
##########################################################################################
##########################################################################################






##########################################################################################
# CLIENT MENU
##########################################################################################
def client_menu(client_email):
  while True:
    print("\nClient Menu:")
    print("1. Search Documents")
    print("2. Borrow Documents")
    print("3. Return Documents")
    print("4. Pay Fees")
    print("5. Update Payment Method")
    print("6. Exit")

    choice = input("Enter your choice (1-6): ")

    if choice == "1":
      search_documents()
      
    elif choice == "2":
      copy_type = input("Would you be borrowing a Electronic Copy or Physical Copy?(e/p)")
      if copy_type == 'p':
        doc_borrow = input("Enter the DocumentID you want to borrow: ")
        cur.execute("SELECT Num_Copies FROM Document WHERE DocID = %s", (doc_borrow, ))
        available = cur.fetchone()[0]
        
        if available > 0:
          borrow_doc(doc_borrow,client_email)
          print("Borrowed Database Successful.")
        else:
          print("Sorry, the document is not available.")    
          
      elif copy_type == "e":
        doc_borrow = input("Enter the DocumentID you want to borrow: ")
        eCopyID = geteID()
        eCopyID+=1
        date_input = input("Enter the lend date (YYYY-MM-DD)")
        lendDate = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
        cur.execute("INSERT INTO ElectronicCopy (ECopyID,LendDate,DocID,Email) VALUES (%s,%s,%s,%s)",(eCopyID,lendDate,doc_borrow,client_email))
        conn.commit()
      print("Document borrowed successfully.")
          
    elif choice == "3":
      cur.execute("SELECT DocID FROM Copy WHERE Email = %s", (client_email, ))
      doc_id = cur.fetchone()
      print(doc_id)
      cur.execute("SELECT DocID FROM ElectronicCopy WHERE Email = %s", (client_email, ))
      doc_id2 = cur.fetchone()
      print(doc_id2)
      doc_type = input("Electronic or Physical?(e/p)")
      doc_return = input("Which Document would you like to return?(enter the DocID): ")
      return_doc(client_email,doc_return,doc_type)  

    elif choice == "4":
      cur.execute("SELECT COUNT(*) FROM Credit_Card WHERE Email = %s", (client_email, ))
      count = cur.fetchone()[0]
      
      if count == 0:
        print("You have no credit card. Please add one first.")
      else:
        user_card = input("Enter your credit card number: ")
        cur.execute("UPDATE Client SET Account_Bal = 0 WHERE Email = %s", (client_email, ))
        conn.commit()
        cur.execute("SELECT Account_Bal FROM Client WHERE Email = %s",(client_email,))
        balance = cur.fetchone()[0]
        print("Your balance now is $")
        print(balance)
        
    elif choice == "5":
      payment_method(client_email)
      
    elif choice == "6":
      print("**Exiting the Client Menu**")
      break
    
    else:
      print("Invalid choice. Please try again.")
##########################################################################################
##########################################################################################



##########################################################################################
# LIBRARIAN MENU
##########################################################################################
def librarian_menu():
  while True:
    print("\nLibrarian Menu:")
    print("1. Register Clients")
    print("2. Add Documents")
    print("3. Update Documents")
    print("4. Update Number of Copies")
    print("5. Delete Copies")
    print("6. Update Client")
    print("7. Delete Client")
    print("8. Exit")
    choice = input("Enter your choice (1-7): ")

    if choice == "1":
      addressID = getaID()
      addressID +=1
      client_email = input("What is the client's email? ")
      client_name = input ("What is the client's name? ")
      client_city = input("What city does the client live in? ")
      client_state = input("What state does the client live in? ")
      client_zip = input("What is the client's zip code? ")
      client_street = input("What is the client's street address? ")
      client_pwd = input("What is the client's password? ")
      cur.execute("INSERT INTO Address (AddressID, Street, City, State, Zip_Code) VALUES (%s,%s,%s,%s,%s)", (addressID, client_street, client_city, client_state, client_zip))
      conn.commit()
      cur.execute("INSERT INTO Client (Email, Name, Password, Account_Bal, AddressID) VALUES (%s,%s,%s,%s,%s)", (client_email, client_name, client_pwd, 0, addressID))
      conn.commit()
      
    elif choice == "2":
      type = input("Is this a book, magazine, journal article? (entering b/m/j as an answer) ")
      insert_doc(type)
      
    elif choice == "3":
      user_doc = input("What DocID would you like to update? ")
      update_doc(user_doc)
      
    elif choice == "4":
      user_doc = input("Which DocID would you like to update the Copies for? ")
      user_copies = input("How many copies are there for this Document? ")
      cur.execute("UPDATE Document set Num_Copies = %s WHERE DocID = %s",(user_copies,user_doc))
      conn.commit()
      
    elif choice == "5":
      user_doc = input("Which DocID would you like to update the Copies for? ")
      user_copies = input("How many copies are there for this Document? ")
      cur.execute("UPDATE Document set Num_Copies = %s WHERE DocID = %s",(user_copies,user_doc))
      conn.commit()
      
    elif choice == "6":
      client_email = input("What is the client's email? ")
      pwd = input("What is the client's password? ")
      
      if(check_client(client_email,pwd) == False):
        print("Incorrect email or password")
        break
      
      user_i = input("Would you like to change your Address? (y/n)")
      if (user_i == 'y'):
        client_city = input("What city does the client live in? ")
        client_state = input("What state does the client live in? ")
        client_zip = input("What is the client's zip code? ")
        client_street = input("What is the client's street address? ")
        addressID = getaID()
        addressID +=1
        cur.execute("INSERT INTO Address (AddressID,Street,City,State,Zip_Code) VALUES (%s,%s,%s,%s,%s)",(addressID, client_street, client_city, client_state, client_zip))
        cur.execute("Update client set AddressID = %s where Email = %s", (addressID, client_email))
      user_i = input("Would you like to change your name? (y/n) ")
      
      if (user_i == 'y'):
        client_name = input ("What is the client's name? ")
        cur.execute("Update client set Name = %s where Email = %s", ( client_name, client_email))
        
      user_i = input("Would you like to change your payment method? (y/n)")
      
      if user_i == "y":
        payment_method(client_email)  
        
    elif choice == "7":
      client_ID=input("Enter the client ID you would like to delete: ")
      cur.execute("Delete from client where clientID = %s",(client_ID, ))
      
    elif choice == "8":
      print("**Exiting the Librarian Menu**")
      break
    
    else:
      print("Invalid choice. Please try again.")
##########################################################################################
##########################################################################################




##########################################################################################
# Main Program
##########################################################################################
print("**Welcome to the Library Application**")
print()

def main():
  while True:
    user_type = input("Are you a client or a librarian (e to exit)? (c/l): ").lower()

    if user_type == "c":
      user_check = input("What is your email? ")
      user_check2 = input("What is your password? ")
      if (check_client(user_check,user_check2)):
        client_menu(user_check)     
      else:
        print("You are not a client!")

    elif user_type == "l":
      user_check = input("What is your email? ")
      user_check2 = input("What is your password? ")
      if(check_librarian(user_check,user_check2)):
        librarian_menu()
      else:
        print("You are not a librarian!")
    elif user_type == "e":
      print("**Exiting the Library Application**")
      break
    else:
      print("Invalid input. Please enter a valid option.")
    

if __name__ == "__main__":
  main()
  conn.close()
##########################################################################################
##########################################################################################
