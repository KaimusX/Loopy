import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import bcrypt
import datetime

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
            self.accounts = []

    def save_accounts(self):
        with open(self.storage_file, 'w') as f:
            json.dump([vars(user) for user in self.accounts], f, indent=4)

    def add_account(self, user):
        self.accounts.append(user)
        self.save_accounts()

    def get_user_by_username(self, username):
        for user in self.accounts:
            if user.username == username:
                return user
        return None

    def validate_input(self, **kwargs):
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
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class AccountManagerUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Account Management System")
        self.manager = AccountManager()
        self.current_frame = None

        self.show_login_screen()

    def switch_frame(self, new_frame_class):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = new_frame_class(self.master, self)
        self.current_frame.pack()

    def show_login_screen(self):
        self.switch_frame(LoginScreen)

    def show_register_screen(self):
        self.switch_frame(RegisterScreen)

    def show_forgot_password_screen(self):
        self.switch_frame(ForgotPasswordScreen)

    def show_otp_screen(self):
        self.switch_frame(OTPScreen)

    def show_create_password_screen(self):
        self.switch_frame(CreatePasswordScreen)

class LoginScreen(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Email:").grid(row=0, column=0, sticky="e")
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=0, column=1)

        tk.Label(self, text="Password:").grid(row=1, column=0, sticky="e")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Checkbutton(self, text="Remember Me").grid(row=2, columnspan=2)

        tk.Button(self, text="Login", command=self.login).grid(row=3, columnspan=2, pady=10)
        tk.Button(self, text="Register", command=self.app.show_register_screen).grid(row=4, columnspan=2)
        tk.Button(self, text="Forgot Password?", command=self.app.show_forgot_password_screen).grid(row=5, columnspan=2)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        user = self.app.manager.get_user_by_username(email)
        if user and user.check_password(password):
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid email or password.")

class RegisterScreen(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Name:").grid(row=0, column=0, sticky="e")
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self, text="Username:").grid(row=1, column=0, sticky="e")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1)

        tk.Label(self, text="Email:").grid(row=2, column=0, sticky="e")
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=2, column=1)

        tk.Label(self, text="Password:").grid(row=3, column=0, sticky="e")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=3, column=1)

        tk.Checkbutton(self, text="Remember Me").grid(row=4, columnspan=2)

        tk.Button(self, text="Register", command=self.register).grid(row=5, columnspan=2, pady=10)
        tk.Button(self, text="Login", command=self.app.show_login_screen).grid(row=6, columnspan=2)

    def register(self):
        name = self.name_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        try:
            self.app.manager.validate_input(name=name, username=username, email=email, password=password)
            user = User(name, username, email, password)
            self.app.manager.add_account(user)
            messagebox.showinfo("Success", "Account created successfully!")
            self.app.show_login_screen()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

class ForgotPasswordScreen(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Enter your registered email to receive password reset instructions:").grid(row=0, columnspan=2)
        tk.Label(self, text="Email:").grid(row=1, column=0, sticky="e")
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=1, column=1)

        tk.Button(self, text="Continue", command=self.continue_reset).grid(row=2, columnspan=2, pady=10)

    def continue_reset(self):
        email = self.email_entry.get()
        user = self.app.manager.get_user_by_username(email)
        if user:
            self.app.show_otp_screen()
        else:
            messagebox.showerror("Error", "Email not found.")

class OTPScreen(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Enter the verification code sent to your email:").grid(row=0, columnspan=2)
        self.otp_entry = tk.Entry(self)
        self.otp_entry.grid(row=1, columnspan=2)

        tk.Button(self, text="Verify", command=self.verify_code).grid(row=2, columnspan=2, pady=10)

    def verify_code(self):
        # Placeholder for OTP verification logic
        self.app.show_create_password_screen()

class CreatePasswordScreen(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Create New Password:").grid(row=0, columnspan=2)

        tk.Label(self, text="Password:").grid(row=1, column=0, sticky="e")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Label(self, text="Confirm Password:").grid(row=2, column=0, sticky="e")
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.grid(row=2, column=1)

        tk.Button(self, text="Reset Password", command=self.reset_password).grid(row=3, columnspan=2, pady=10)

    def reset_password(self):
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        if password == confirm_password:
            # Placeholder for password reset logic
            messagebox.showinfo("Success", "Password reset successful!")
            self.app.show_login_screen()
        else:
            messagebox.showerror("Error", "Passwords do not match.")

def main():
    root = tk.Tk()
    app = AccountManagerUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
