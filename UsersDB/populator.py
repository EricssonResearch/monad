#!/usr/bin/python
import sys
import uuid
import random
import MySQLdb

''' Populator for our DB

A simple populator that takes a NUMBER_OF_USERS and creates a number of
random dummy entries for our USER_PROFILE table. To run for your localhost
execute:

python populator.py <connection_password> <number_of_users>
'''

# Select a random number of entries. Default is 1000
NUMBER_OF_USERS = int(sys.argv[2])

#DATABASE CREDENTIALS
HOST = "localhost"
USER = "root"
# Change the password to connect to your database
PASSWORD = str(sys.argv[1])
DB = "MONAD"

# Open database connection

db = MySQLdb.connect(HOST,USER,PASSWORD,DB)

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Random names list
firstnames = ['Ciera', 'Mariah', 'Jaimie','Ricky', 'Roselle','Summer',
    'Gail', 'Madge', 'Jennell', 'Emilio', 'Ranae', 'Dora', 'Virginia', 'Ursula',
    'Timika', 'Rheba', 'Karon', 'Ute', 'Elisabeth', 'Jolyn', 'Shirleen',
    'Shirly',     'Lenny', 'Willena', 'Latrisha', 'Edison', 'Claudio', 'Felisa',
    'Domenica', 'Cherri', 'Nina', 'Norah', 'Velma', 'Benito', 'Lorene',
    'Sharan', 'Donna', 'Lizeth',     'Sona', 'Latrina', 'Frank', 'Rudolph',
    'Angeline', 'Sanora', 'Anna', 'Madeline', 'Margarete', 'Zina', 'Kassie',
    'Dewey', 'Zana', 'Sharee', 'Rayford', 'Ashlie',     'Brittanie', 'Calvin',
    'Joselyn', 'Valeria', 'Kamilah', 'Jenelle', 'Paula', 'Azalee', 'Hayden',
    'Madlyn', 'Asa', 'Natasha', 'Sheron', 'Josef', 'Gisele', 'Lauretta',
    'Millie', 'Edra', 'Nathanial', 'Camelia', 'Burt', 'Grady', 'Augustus',
    'Cathleen',     'Lani', 'Elliot', 'Nona', 'Lilliana', 'Perry', 'Waltraud',
    'Felicidad', 'Hershel',     'Margaretta', 'Lemuel', 'Jamila', 'Jae',
    'Faith', 'Marleen', 'Mabel', 'Virgina', 'Arvilla', 'Sena', 'Marlen',
    'Brynn', 'Mark', 'Milagro'
]

# Random emails provider and name list
domains = [ "hotmail.com", "gmail.com", "aol.com", "mail.com" , "mail.kz",
            "yahoo.com"]
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']

# Function for generating random email addresses
def random_email():
    name = ( ''.join(letters[random.randint(0, len(letters)-1)] for i in
             range (7)))
    name += "@"
    name += domains[random.randint(0, len(domains)-1)]
    return name

# Function for generating random unique usernames, phones, names and passwords
# and populating our table with all the credentials by calling the SIGNUP
# function
def populate_users(number):
    phone = 1000000000
    for i in range(number):
        sql = (("SELECT SIGNUP('%s','%s','%s','%s','%s','%s')"
                %(uuid.uuid4(),
                  firstnames[random.randint(0,len(firstnames)-1)],
                  firstnames[random.randint(0,len(firstnames)-1)],
                  random_email(),
                  phone,
                  uuid.uuid4())))
        #print sql
        cursor.execute(sql)
        phone += 1

# The actual call of the function
sql = "SET autocommit = 0;"
cursor.execute(sql)
sql = "SET unique_checks=0;"
cursor.execute(sql)

populate_users(NUMBER_OF_USERS)

sql = "SET unique_checks=1;"
cursor.execute(sql)
sql = "COMMIT;"
cursor.execute(sql)

# disconnect from server

db.close()
