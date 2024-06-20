import tkinter as tk
from tkinter import messagebox
import json
import bcrypt

class AccountManager:
    def __init__(self, storage_file='users.json'):
        self.storage_file = storage_file
        self.load_accounts()

    def load_accounts(self):
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                self.accounts = [User(**user_data) for user_data in data]
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is empty, initialize with an empty list
            self.accounts = []

    def save_accounts(self):
        with open(self.storage_file, 'w') as f:
            json.dump([vars(user) for user in self.accounts], f, indent=4)

    def add_account(self, user):
        self.accounts.append(user)
        self.save_accounts()

    def delete_account(self, username):
        for user in self.accounts:
            if user.username == username:
                self.accounts.remove(user)
                self.save_accounts()
                return True
        return False

    def modify_account_status(self, username, new_status):
        for user in self.accounts:
            if user.username == username:
                user.status = new_status
                self.save_accounts()
                return True
        return False

    def log_activity(self, username, activity):
        for user in self.accounts:
            if user.username == username:
                if activity == 'login':
                    user.log_login()
                elif activity == 'logout':
                    user.log_logout()
                self.save_accounts()
                return True
        return False

    def get_user_by_username(self, username):
        for user in self.accounts:
            if user.username == username:
                return user
        return None

    def validate_input(self, **kwargs):
        # Basic input validation to ensure required fields are not empty
        required_fields = ['name', 'username', 'email', 'password']
        for field in required_fields:
            if not kwargs.get(field):
                raise ValueError(f"Missing required field: {field}")

class User:
    def __init__(self, name, username, email, password, status='active'):
        self.name = name
        self.username = username
        self.email = email
        self.set_password(password)
        self.status = status
        self.last_login = None
        self.last_logout = None

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password.encode('utf-8'), bcrypt.gestalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def is_active(self):
        return self.status == 'active'

    def log_login(self):
        self.last_login = datetime.datetime.now()

    def log_logout(self):
        self.last_logout = datetime.datetime.now()

class FileManager:
    def __init__(self, storage_file='files.json'):
        self.storage_file = storage_file
        self.load_files()

    def load_files(self):
        try:
            with open(self.storage_file, 'r') as f:
                self.files = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.files = {}

    def save_files(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.files, f, indent=4)

    def create_file(self, filename, entries):
        self.files[filename] = entries
        self.save_files()

    def delete_file(self, filename):
        if filename in self.files:
            del self.files[filename]
            self.save_files()

    def get_file_entries(self, filename):
        return self.files.get(filename, [])

class AccountManagerUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Account Management System")
        self.manager = AccountManager()

        self.username_label = tk.Label(master, text="Username:")
        self.username_label.grid(row=0, column=0, sticky="e")
        self.username_entry = tk.Entry(master)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(master, text="Password:")
        self.password_label.grid(row=1, column=0, sticky="e")
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.create_account_button = tk.Button(master, text="Create Account", command=self.create_account)
        self.create_account_button.grid(row=3, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.manager.get_user_by_username(username)
        if user and user.check_password(password):
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def create_account(self):
        name = tkinter.SimpleDialog.askstring("Create Account", "Enter your full name:")
        if not name:
            return

        username = SimpleDialog.askstring("Create Account", "Enter a username:")
        if not username:
            return

        email = SimpleDialog.askstring("Create Account", "Enter your email:")
        if not email:
            return

        password = SimpleDialog.askstring("Create Account", "Enter a password:")
        if not password:
            return

        try:
            self.manager.validate_input(name=name, username=username, email=email, password=password)
            user = User(name, username, email, password)
            self.manager.add_account(user)
            messagebox.showinfo("Success", "Account created successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

class FileManagerUI:
    def __init__(self, master):
        self.master = master
        self.master.title("File Management System")
        self.file_manager = FileManager()

        self.filename_label = tk.Label(master, text="File Name:")
        self.filename_label.grid(row=0, column=0, sticky="e")
        self.filename_entry = tk.Entry(master)
        self.filename_entry.grid(row=0, column=1)

        self.entries_label = tk.Label(master, text="Entries (comma-separated):")
        self.entries_label.grid(row=1, column=0, sticky="e")
        self.entries_entry = tk.Entry(master)
        self.entries_entry.grid(row=1, column=1)

        self.create_file_button = tk.Button(master, text="Create File", command=self.create_file)
        self.create_file_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.delete_file_button = tk.Button(master, text="Delete File", command=self.delete_file)
        self.delete_file_button.grid(row=3, column=0, columnspan=2)

    def create_file(self):
        filename = self.filename_entry.get()
        entries = self.entries_entry.get().split(',')
        entries = [entry.strip() for entry in entries if entry.strip()]

        if not filename:
            messagebox.showerror("Error", "Please enter a filename.")
            return

        if len(entries) > 10:
            messagebox.showerror("Error", "Maximum 10 entries allowed.")
            return

        self.file_manager.create_file(filename, entries)
        messagebox.showinfo("Success", f"File '{filename}' created successfully!")

    def delete_file(self):
        filename = self.filename_entry.get()

        if not filename:
            messagebox.showerror("Error", "Please enter a filename.")
            return

        self.file_manager.delete_file(filename)
        messagebox.showinfo("Success", f"File '{filename}' deleted successfully!")

def main():
    root = tk.Tk()

    account_manager_ui = AccountManagerUI(root)
    file_manager_ui = FileManagerUI(root)

    root.mainloop()

if __name__ == "__main__":
    main()
