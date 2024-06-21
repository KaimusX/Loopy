# Will be used to manage access and checks against the SQL that stores user information.
import pandas as pd
import PySimpleGUI as sg
import pygame
import os

class UserAccount:

    def createDataframe():
        df = pd.DataFrame({'Username': [], 'Displayname': [], 'Name': [], 'Email': [], 'Role': [], 'Password': []})
        df.to_csv('Database.csv', index=False)

    def createUserRow():
        # Loading the dataframe
        df = pd.read_csv('Database.csv')

        # Temporary inputs until we have a front end to submit information through
        Username = 'invalid'
        while Username == 'invalid':
            Username = input("Username: ")
            for x in ['&','?']:
                if x in Username:
                    Username = 'invalid'
        DisplayName = input("Display name: ")
        Name = input("Full name: ")
        Email = input("Email address: ")
        Role = input("Role: ")
        Pass = input("Password: ")

        # Temproary hash skip, until hashing is implemented
        HashedPass = Pass

        # Complete row of data
        newRow = {'Username':Username, 'Displayname': DisplayName, 'Name': Name, 'Email': Email, 'Role': Role, 'Password': HashedPass}

        # Row added to the file.
        df = df._append(newRow, ignore_index=True)
        df.to_csv('Database.csv', index=False)

    def checkUser():
        Username = input("Enter username: ")
        Password = input("Enter password: ")

def main():
    UserAccount.createDataframe()
    UserAccount.createUserRow()

if __name__ == "__main__":
    main()