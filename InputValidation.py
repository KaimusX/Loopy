import re

def validate_username(username):
     #Username must be alphanumeric and between 5 to 20 characters
    if re.fullmatch(r'^[a-zA-Z0-9]{5,20}$', username):
        return True
    else:
        return False

def is_valid_email(email: str) -> bool:
    # Regular expression pattern for validating an email
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Using re.match to check if the email matches the pattern
    if re.match(email_pattern, email):
        return True
    else:
        return False

# Function to validate the password
def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = True
    
    if len(passwd) < 8:
        #print('length should be at least 8')
        val = False
        
    if len(passwd) > 20:
        #print('length should be not be greater than 20')
        val = False
        
    if not any(char.isdigit() for char in passwd):
        #print('Password should have at least one numeral')
        val = False
        
    if not any(char.isupper() for char in passwd):
        #print('Password should have at least one uppercase letter')
        val = False
        
    if not any(char.islower() for char in passwd):
        #print('Password should have at least one lowercase letter')
        val = False
        
    if not any(char in SpecialSym for char in passwd):
        #print('Password should have at least one of the symbols $@#%')
        val = False
    return val