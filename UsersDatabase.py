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
        df = pd.DataFrame({'Username': [], 'Displayname': [], 'Name': [], 'Email': [], 'Password': []})
        df.to_csv('Database.csv', index=False)

    # Account creation
    def createUserRow(): #usr,disp,nm,em,psw
        # Loading the dataframe
        df = pd.read_csv('Database.csv')

        # Temporary inputs until we have a front end to submit information through
        Username = input("Username: ") #usr
        DisplayName = input("Display Name: ") #disp
        Name = input("Full Name: ") #nm
        Email = input("Email: ") #em
        Pass = input("Password: ") #psw

        # Hash the password so we don't transfer it in plain text
        HashedPass = createPwdHash(Pass)

        # Complete row of data
        newRow = {'Username':Username, 'Displayname': DisplayName, 'Name': Name, 'Email': Email, 'Password': HashedPass}

        # Row added to the file.
        df = df._append(newRow, ignore_index=True)
        df.to_csv('Database.csv', index=False)


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

        # Condition to track if Username was found
        foundUser = False
        
        # Set up 3D array to search through
        for user_row in users_3d:
            # Username found scenario
            if user_row[0][0] == username:
                if DEBUG:
                    print("Username Valid")
                foundUser = True # Set to true so we dont' trigger an 'invalid user' condition
                if user_row[0][4] == hashedPass:
                    # Correct pass scenario
                    if DEBUG:
                        print("Password Correct")
                else:
                    # Incorrect pass scenario
                    if DEBUG:
                        print("Password Incorrect")
                break
        # If still false at the end, the user wasn't found.
        if foundUser == False:
            print("invalid Username")


    # Function to alter passwords (or any information, eventually)
    def changePass():
        email = input("Enter email: ")
        df = pd.read_csv('Database.csv')
        
        # Find the row where the email matches
        row_index = df.index[df['Email'] == email].tolist()
        
        if not row_index:
            print(f"No user found with email '{email}'")
            return
        
        # Row index
        row_index = row_index[0]
        
        oldPass = input("Enter old password: ")
        newPass = input("Enter new password: ")
        
        # Check if the old password matches
        if createPwdHash(oldPass) != df.at[row_index, 'Password']:
            print("Incorrect old password. Password change failed.")
            return
        
        if createPwdHash(newPass) == df.at[row_index, 'Password']:
            print("This password is alreay in use. Password change failed.")
            return
        
        # Update the password for the found row
        df.at[row_index, 'Password'] = createPwdHash(newPass)
        
        # Write back to the CSV file
        df.to_csv('Database.csv', index=False)
        
        print("Password updated successfully.")

# Main code, uncomment as needed for testing.
def main():
    if not os.path.isfile('Database.csv'):
        UserAccount.createDataframe()
    #UserAccount.createUserRow()
    UserAccount.checkUser()
    UserAccount.changePass()
    UserAccount.checkUser()


if __name__ == "__main__":
    main()