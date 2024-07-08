import tkinter as tk
from tkinter import messagebox
import bcrypt
import UsersDatabase

class SimpleAccountManager:
    def __init__(self):
        self.accounts = {}

    def add_account(self, username, password, name, email):
        if username in self.accounts:
            raise ValueError("Username already exists.")
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.accounts[username] = {
            'name': name,
            'email': email,
            'password_hash': password_hash
        }

    def check_credentials(self, username, password):
        if username in self.accounts:
            stored_hash = self.accounts[username]['password_hash']
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        return False

    def get_user_info(self, username):
        if username in self.accounts:
            return self.accounts[username]
        return None

class SimpleAccountManagerUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Account Management System")
        self.manager = SimpleAccountManager()
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
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.manager.check_credentials(username, password):
            messagebox.showinfo("Login", f"Login successful!\nWelcome {username}!")
            user_info = self.manager.get_user_info(username)
            self.show_account_screen(user_info)
        else:
            messagebox.showerror("Login", "Invalid username or password.")

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

        tk.Label(self.main_frame, text="Password").pack()
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack()

        tk.Button(self.main_frame, text="Register", command=self.register).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.go_back).pack(pady=10)

    def register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            #UsersDatabase.UserAccount.createUserRow(username, name, email, password)
            self.manager.add_account(username, password, name, email)
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
    root = tk.Tk()
    app = SimpleAccountManagerUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()