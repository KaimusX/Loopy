import PySimpleGUI as sg
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

def account_manager_ui():
    manager = AccountManager()
    
    layout = [
        [sg.Text('Username'), sg.Input(key='-USERNAME-')],
        [sg.Text('Password'), sg.Input(key='-PASSWORD-', password_char='*')],
        [sg.Button('Login'), sg.Button('Create Account')]
    ]

    window = sg.Window('Account Management System', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Login':
            username = values['-USERNAME-']
            password = values['-PASSWORD-']

            user = manager.get_user_by_username(username)
            if user and user.check_password(password):
                sg.popup('Success', 'Login successful!')
            else:
                sg.popup('Error', 'Invalid username or password.')
        elif event == 'Create Account':
            create_account_dialog(manager)

    window.close()

def create_account_dialog(manager):
    layout = [
        [sg.Text('Full Name'), sg.Input(key='-NAME-')],
        [sg.Text('Username'), sg.Input(key='-USERNAME-')],
        [sg.Text('Email'), sg.Input(key='-EMAIL-')],
        [sg.Text('Password'), sg.Input(key='-PASSWORD-', password_char='*')],
        [sg.Button('Create'), sg.Button('Cancel')]
    ]

    window = sg.Window('Create Account', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break
        elif event == 'Create':
            try:
                manager.validate_input(
                    name=values['-NAME-'], 
                    username=values['-USERNAME-'], 
                    email=values['-EMAIL-'], 
                    password=values['-PASSWORD-']
                )
                user = User(
                    name=values['-NAME-'], 
                    username=values['-USERNAME-'], 
                    email=values['-EMAIL-'], 
                    password=values['-PASSWORD-']
                )
                manager.add_account(user)
                sg.popup('Success', 'Account created successfully!')
                break
            except ValueError as e:
                sg.popup('Error', str(e))

    window.close()

def file_manager_ui():
    file_manager = FileManager()

    layout = [
        [sg.Text('File Name'), sg.Input(key='-FILENAME-')],
        [sg.Text('Entries (comma-separated)'), sg.Input(key='-ENTRIES-')],
        [sg.Button('Create File'), sg.Button('Delete File')]
    ]

    window = sg.Window('File Management System', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Create File':
            filename = values['-FILENAME-']
            entries = values['-ENTRIES-'].split(',')
            entries = [entry.strip() for entry in entries if entry.strip()]

            if not filename:
                sg.popup('Error', 'Please enter a filename.')
                continue

            if len(entries) > 10:
                sg.popup('Error', 'Maximum 10 entries allowed.')
                continue

            file_manager.create_file(filename, entries)
            sg.popup('Success', f"File '{filename}' created successfully!")
        elif event == 'Delete File':
            filename = values['-FILENAME-']

            if not filename:
                sg.popup('Error', 'Please enter a filename.')
                continue

            file_manager.delete_file(filename)
            sg.popup('Success', f"File '{filename}' deleted successfully!")

    window.close()

def main():
    layout = [
        [sg.Button('Account Management')],
        [sg.Button('File Management')],
        [sg.Button('Exit')]
    ]

    window = sg.Window('Main Menu', layout)

    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Account Management':
            account_manager_ui()
        elif event == 'File Management':
            file_manager_ui()

    window.close()

if __name__ == "__main__":
    main()
