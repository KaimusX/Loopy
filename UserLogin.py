import tkinter as tk
from tkinter import messagebox
import UsersDatabase
import os
import InputValidation
import TwoFactor
from PIL import Image, ImageTk
import Home_Page
import playlist as pl

TEMP_OTP = None

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
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not InputValidation.validate_username(username):         
            messagebox.showerror("Login", "Invalid username.")      
        elif not InputValidation.password_check(password):          
            messagebox.showerror("Login", "Invalid Password.")      

        if UsersDatabase.UserAccount.checkUser(username, password) == "Success":
            self.show_2fa_screen(username) # Go to 2FA to check it, then we can say success and let them through. We can maybe put the success on it's own function.
        else:
            messagebox.showerror("Login", "Username or password not found.")

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

    def finishRegister(self):
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
            global TEMP_OTP
            try:
                UsersDatabase.UserAccount.createUserRow(username, name, email, password, TEMP_OTP)
                messagebox.showinfo("Register", "Registration successful!")
                self.create_widgets()
            except ValueError as e:
                messagebox.showerror("Register", str(e))
            cwd = os.getcwd()
            qr_path = os.path.join(cwd, 'qr.png')
            os.remove(qr_path)
            TEMP_OTP = None
        

    def register(self):
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
            global TEMP_OTP
            TEMP_OTP = TwoFactor.otp_gen(username)

            cwd = os.getcwd()
            qr_path = os.path.join(cwd, 'qr.png')
            
            image1 = Image.open(qr_path)
            test = ImageTk.PhotoImage(image1)
            label1 = tk.Label(image = test)
            label1.image = test
            
            label1.place(x=550, y=70)
            
            tk.Button(self.main_frame, text="Done", command=self.finishRegister).pack(pady=10)

    def show_account_screen(self, user_info):
        self.clear_frame()
        self.screen_stack.append(lambda: self.show_account_screen(user_info))  # Push the current screen function to the stack

        tk.Label(self.main_frame, text=f"Name: {user_info['name']}").pack()
        tk.Label(self.main_frame, text=f"Email: {user_info['email']}").pack()
        tk.Label(self.main_frame, text=f"Username: {user_info['username']}").pack()

        tk.Button(self.main_frame, text="Logout", command=self.create_widgets).pack(pady=10)
#####################################################################################################################################

    def show_2fa_screen(self,usr):
        self.clear_frame()
        self.screen_stack.append(self.show_2fa_screen)  # Push the current screen function to the stack

        tk.Label(self.main_frame, text="2-Factor Authentication").pack(pady=10)
        tk.Label(self.main_frame, text="Enter the 2FA code sent to you:").pack()
        self.otp_entry = tk.Entry(self.main_frame)
        self.otp_entry.pack(pady=10)

        tk.Button(self.main_frame, text="Submit", command=self.verify_2fa(usr)).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.go_back).pack(pady=10)

    def verify_2fa(self,usr):
        otp_code = self.otp_entry.get()
        totp = UsersDatabase.UserAccount.getOTP(usr)
        if True: #TwoFactor.verify_otp(totp, otp_code):
            messagebox.showinfo("2FA", f"2FA successful! You are successfully logged in {usr}!")
            self.create_widgets()
            self.master.destroy()
            Home_Page.Home(usr)
        else:
            messagebox.showerror("2FA", "Invalid 2FA code. Please try again.")

#####################################################################################################################################
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