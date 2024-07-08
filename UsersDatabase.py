# Will be used to manage access and checks against the SQL that stores user information.
import pandas as pd
import PySimpleGUI as sg
import pygame
import os
import hashlib
import re
import csv

DEBUG = True


# Pasword hashing function
def createPwdHash(password):
    # Generate SHA-256 hash
    hash_object = hashlib.sha256(password.encode())
    hash_hex = hash_object.hexdigest()

    # Output the hash
    return hash_hex


class UserAccount:

    # Dataframe (csv/database) creation
    def createDataframe():
        df = pd.DataFrame({'Username': [], 'Displayname': [], 'Name': [], 'Email': [], 'Role': [], 'Password': []})
        df.to_csv('Database.csv', index=False)

    # Account creation
    def createUserRow():
        # Loading the dataframe
        df = pd.read_csv('Database.csv')

        # Temporary inputs until we have a front end to submit information through
        Username = 'invalid'
        while Username == 'invalid':
            Username = input("Username: ")
            for x in ['&','?','/','\'','\\','|','[',']','{','}','%',' ']:
                if x in Username:
                    Username = 'invalid'
        DisplayName = input("Display name: ")
        Name = input("Full name: ")
        Email = input("Email address: ")
        Role = input("Role: ")
        Pass = input("Password: ")

        # Hash the password so we don't transfer it in plain text
        HashedPass = createPwdHash(Pass)

        # Complete row of data
        newRow = {'Username':Username, 'Displayname': DisplayName, 'Name': Name, 'Email': Email, 'Role': Role, 'Password': HashedPass}

        # Row added to the file.
        df = df._append(newRow, ignore_index=True)
        df.to_csv('Database.csv', index=False)
            
        #security_questions = [
        #        "What was your childhood nickname?",
        #        "In what city did you meet your spouse/significant other?",
        #        "What is the name of your favorite childhood friend?",
        #        "What street did you live on in third grade?",
        #        "What is your oldest sibling's birthday month and year?",
        #        "What is the middle name of your youngest child?",
        #        "What is your oldest sibling's middle name?",
        #        "What school did you attend for sixth grade?",
        #        "What was your childhood phone number including area code?",
        #        "What is your oldest cousin's first and last name?",
        #        "What was the name of your first stuffed animal?",
        #        "In what city or town did your mother and father meet?"
        #    ]

        #print("Please choose 3 security questions from the following list:")
        #for i, question in enumerate(security_questions):
        #    print(f"{i+1}. {question}")

        #chosen_questions = []
        #while len(chosen_questions) < 3:
        #    choice = int(input("Enter the number of the question you want to choose: "))
        #    if 1 <= choice <= 12 and choice not in chosen_questions:
        #        chosen_questions.append(choice)
        #    else:
        #        print("Invalid choice or question already selected. Please try again.")

        #chosen_questions_text = [security_questions[i-1] for i in chosen_questions]
        #security_answers = []
        #for question in chosen_questions_text:
        #    answer = input(f"Answer for '{question}': ")
        #    security_answers.append(answer)


        #newRow = {
        #        'Username': Username,
        #        'Displayname': DisplayName,
        #        'Name': Name,
        #        'Email': Email,
        #        'Role': Role,
        #        'Password': HashedPass,
        #        'SecurityQuestions': "|".join(chosen_questions_text),
        #        'SecurityAnswers': "|".join(security_answers)
        #    }

            # Row added to the file.
        #    df = df._append(newRow, ignore_index=True)
        #    df.to_csv('Database.csv', index=False)

        #if (len(password) >= 8 and re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'[0-9]', password) and re.search(r'[^A-Za-z0-9]', password)):


    # Sudo log in function
    def checkUser():
        # Get dataframe first
        cwd = os.getcwd()
        users_file = os.path.join(cwd, 'Database.csv')
        users = []
        users_3d = []

        # Read the users CSV and convert the CSV database into a 3D array with proper columns and rows,
        # excluding the header.
        try:
            with open(users_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header
                users = [row for row in reader]
                users_3d = [[row] for row in users]
        except FileNotFoundError:
            print(f"Error: {users_file} not found.")
        except Exception as e:
            print(f"An error occurred while reading {users_file}: {e}")

        # Input log-in info
        username = input("Enter username: ")
        password = input("Enter password: ")
        hashedPass = createPwdHash(password)

        foundUser = False
        for user_row in users_3d:
            if user_row[0][0] == username:
                if DEBUG:
                    print("Username Valid")
                foundUser = True
                if user_row[0][5] == hashedPass:
                    if DEBUG:
                        print("Password Correct")
                else:
                    if DEBUG:
                        print("Password Incorrect")
                break
        if foundUser == False:
            print("invalid Username")

    def changePass():
        pass


# Main code, uncomment as needed for testing.
def main():
    if not os.path.isfile('Database.csv'):
        UserAccount.createDataframe()
    UserAccount.createUserRow()
    UserAccount.checkUser()
    pass

if __name__ == "__main__":
    main()