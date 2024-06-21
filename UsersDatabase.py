# Will be used to manage access and checks against the SQL that stores user information.
import pandas as pd
import PySimpleGUI as sg
import pygame
import os

class UserAccount:

    def createDataframe():
        df = pd.DataFrame({'Username': [], 'Displayname': [], 'Name': [], 'Email': [], 'Role': [], 'Password': []})
        df.to_csv('Database.csv', index=False)

    def createUserDatabase():
        # Loading the dataframe
        df = pd.read_csc('Database.csv')

        # Temporary inputs until we have a front end to submit information through
        Username = input()
        DisplayName = input()
        Name = input()
        Email = input()
        Role = input()
        Pass = input()

        # Temproary hash skip, until hashing is implemented
        HashedPass = Pass

        # Complete row of data
        newRow = {'Username':Username, 'Displayname': DisplayName, 'Name': Name, 'Email': Email, 'Role': Role, 'Password': HashedPass}

        # Row added to the file.
        df = df._append(newRow, ignore_index=True)
        df.to_csv('Database.csv', index=False)

def main():
    UserAccount.createDataframe()
    UserAccount.createUserDatabase()