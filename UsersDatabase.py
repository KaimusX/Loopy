# Will be used to manage access and checks against the SQL that stores user information.
import pandas as pd
import PySimpleGUI as sg
import pygame
import os
import hashlib


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