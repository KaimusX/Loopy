import tkinter as tk
from tkinter import messagebox
import UsersDatabase
import os
import InputValidation
import TwoFactor
from PIL import Image, ImageTk
import Home_Page
import playlist as pl

counter = 0
last_usr = ''
class SimpleAccountManagerUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Account Management System")
        self.screen_stack = []  # Stack to keep track of the screens
        self.create_widgets()

    def create_widgets(self):
        self.clear_frame()
        self.screen_stack.append(self.create_widgets)  # Push the current screen function to the stack

        self.login_button = tk.Button(self.main_frame, text="Login", command=self.show_login_screen)
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self.main_frame, text="Register", command=self.show_register_screen)
        self.register_button.pack(pady=10)

    def show_login_screen(self):
        self.clear_frame()
        self.screen_stack.append(self.show_login_screen)  # Push the current screen function to the stack

        tk.Label(self.main_frame, text="Username").pack()
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack()

        tk.Label(self.main_frame, text="Password").pack()
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack()

        tk.Button(self.main_frame, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.go_back).pack(pady=10)

    def login(self):
        global counter
        global last_usr
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not InputValidation.validate_username(username):         
            messagebox.showerror("Login", "Invalid username.")

        if last_usr != self.username_entry.get():
            counter = 0

        last_usr = username

        if counter == 3:
            messagebox.showerror("Login", "Too many attempts. Try again later.")
        elif UsersDatabase.UserAccount.checkUser(username, password) == "Success":
            self.master.destroy()
            Home_Page.Home(username)
        elif UsersDatabase.UserAccount.checkUser(username, password) == "Invalid":
            counter += 1
            messagebox.showerror("Login", "Incorrect password.")
        else:
            messagebox.showerror("Login", "Username not found.")

    def show_register_screen(self):
        self.clear_frame()
        self.screen_stack.append(self.show_register_screen)  # Push the current screen function to the stack

        tk.Label(self.main_frame, text="Name").pack()
        self.name_entry = tk.Entry(self.main_frame)
        self.name_entry.pack()

        tk.Label(self.main_frame, text="Email").pack()
        self.email_entry = tk.Entry(self.main_frame)
        self.email_entry.pack()

        tk.Label(self.main_frame, text="Username").pack()
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack()

        tk.Label(self.main_frame, text="Username must be alphanumeric and between 5 to 20 characters.").pack()

        tk.Label(self.main_frame, text="Password").pack()
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack()

        tk.Label(self.main_frame, text="Password length should contain 8-20 characters, have at least one number, \nhave at least one uppercase letter, have at least one lowercase letter, and have at least one of the symbols: $, @, #, %.").pack()

        tk.Button(self.main_frame, text="Register", command=self.register).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.go_back).pack(pady=10)

    def register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not InputValidation.validate_username(username):                     
            messagebox.showerror("Registration", "Invalid username.")           
        elif not InputValidation.is_valid_email(email):                         
            messagebox.showerror("Registration", "Invalid email.")              
        elif not InputValidation.password_check(password):                      
            messagebox.showerror("Registration", "Invalid Password.")           
        else:
            try:
                UsersDatabase.UserAccount.createUserRow(username, name, email, password)
                messagebox.showinfo("Register", "Registration successful!")
                self.create_widgets()
            except ValueError as e:
                messagebox.showerror("Register", str(e))

    def show_account_screen(self, user_info):
        self.clear_frame()
        self.screen_stack.append(lambda: self.show_account_screen(user_info))  # Push the current screen function to the stack

        tk.Label(self.main_frame, text=f"Name: {user_info['name']}").pack()
        tk.Label(self.main_frame, text=f"Email: {user_info['email']}").pack()
        tk.Label(self.main_frame, text=f"Username: {user_info['username']}").pack()

        tk.Button(self.main_frame, text="Logout", command=self.create_widgets).pack(pady=10)

    def go_back(self):
        if self.screen_stack:
            self.screen_stack.pop()  # Remove the current screen function
            if self.screen_stack:
                previous_screen = self.screen_stack.pop()  # Get the previous screen function
                previous_screen()  # Show the previous screen

    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack()

def main():
    if not os.path.isfile('Database.csv'):
        UsersDatabase.UserAccount.createDataframe()
    if not os.path.isfile('playlists.csv'):
        pl.Playlist.create_dataframe()
    root = tk.Tk()
    root.minsize(1000, 500)
    app = SimpleAccountManagerUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()