# Will be used to manage access and checks against the SQL that stores user information.
import pandas as pd
import PySimpleGUI as sg
import pygame
import os
import hashlib
import re


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

        while not UserAccount.is_valid_password(Password):
            print("Password must be at least 8 characters long and include an uppercase letter, a lowercase letter, a number, and a special character.")
            Password = input("Password: ")

        # Temproary hash skip, until hashing is implemented
        HashedPass = createPwdHash(Pass)

        # Complete row of data
        newRow = {'Username':Username, 'Displayname': DisplayName, 'Name': Name, 'Email': Email, 'Role': Role, 'Password': HashedPass}

        # Row added to the file.
        df = df._append(newRow, ignore_index=True)
        df.to_csv('Database.csv', index=False)

    # Sudo log in function
    def checkUser():
        # Get dataframe first
        df = pd.read_csv('Database.csv')

        # Input lo in info
        username = input("Enter username: ")
        password = input("Enter password: ")
        hashedPass = createPwdHash(password)
        

    def is_valid_password(password):
        if (len(password) >= 8 and re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'[0-9]', password) and re.search(r'[^A-Za-z0-9]', password)):

    security_questions = [
            "What was your childhood nickname?",
            "In what city did you meet your spouse/significant other?",
            "What is the name of your favorite childhood friend?",
            "What street did you live on in third grade?",
            "What is your oldest sibling's birthday month and year?",
            "What is the middle name of your youngest child?",
            "What is your oldest sibling's middle name?",
            "What school did you attend for sixth grade?",
            "What was your childhood phone number including area code?",
            "What is your oldest cousin's first and last name?",
            "What was the name of your first stuffed animal?",
            "In what city or town did your mother and father meet?"
        ]

    print("Please choose 3 security questions from the following list:")
    for i, question in enumerate(security_questions):
        print(f"{i+1}. {question}")

    chosen_questions = []
    while len(chosen_questions) < 3:
        choice = int(input("Enter the number of the question you want to choose: "))
        if 1 <= choice <= 12 and choice not in chosen_questions:
            chosen_questions.append(choice)
        else:
            print("Invalid choice or question already selected. Please try again.")

    chosen_questions_text = [security_questions[i-1] for i in chosen_questions]
        security_answers = []
        for question in chosen_questions_text:
            answer = input(f"Answer for '{question}': ")
            security_answers.append(answer)


    newRow = {
            'Username': Username,
            'Displayname': DisplayName,
            'Name': Name,
            'Email': Email,
            'Role': Role,
            'Password': HashedPass,
            'SecurityQuestions': "|".join(chosen_questions_text),
            'SecurityAnswers': "|".join(security_answers)
        }

        # Row added to the file.
        df = df._append(newRow, ignore_index=True)
        df.to_csv('Database.csv', index=False)



        # Check if username is valid
        if username not in df['Database.csv'].values:
            print('Invalid Username.')
            return
        
        # If it is, grab the row it relates too
        userRow = df.loc[df['Username'] == username]
        
        # Check if password has matches
        if df.loc[df['Username'] == username,'Password'] == hashedPass:
            pass
            # Log in



# Main code, uncomment as needed.
def main():
    #UserAccount.createDataframe()
    #UserAccount.createUserRow()
    #UserAccount.checkUser()
    pass

if __name__ == "__main__":
    main()