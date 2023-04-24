import db
import sys
import argparse
import os
import time

login_successful = False
current_user_id = -1    

def create_arg_parser():
    parser = argparse.ArgumentParser(description="FinApp at your fingertips")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    subparsers = parser.add_subparsers(title='Commands', dest='command')
    setup_command = subparsers.add_parser('setup')

    login_command = subparsers.add_parser('login')
    login_command.add_argument('-u', '--username', type=str, help='Enter username')
    login_command.add_argument('-p', '--password', type=str, help='Enter password')

    add_user_command = subparsers.add_parser('add-user')
    add_user_command.add_argument('arg2')

    check_balance_command = subparsers.add_parser('check-balance')

    update_balance_command = subparsers.add_parser('update-balance')
    update_balance_command.add_argument('-t', '--transaction', type=float, help="Enter transaction amount")
    return parser

def login(username, password):
    """
    Validate the user's login credentials and save the login state.

    Parameters:
        username (str): The user's username.
        password (str): The user's password.

    If the provided username and password are valid, the user is logged in and the
    login state is saved. If the login is successful, a welcome message is printed
    to the console. If the login fails, an error message is printed.

    The login state consists of the login status (bool), the login time (float),
    and the current user ID (int), and is saved to a file named 'login.txt'.
    """
    result = db.validate_login(username, password)
    if result < 0:
        login_successful = False
        current_user_id = -1         
        print(f"""Login failed for {username}""")
    else:
        login_successful = True
        login_time = time.time()
        current_user_id = result
        print(f"""Welcome back, {username.title()}!""")
    # Save the login state for subsequent actions
    save_session_state(login_successful, login_time, current_user_id)

def save_session_state(login_successful, login_time, current_user_id):
    """
    Save the login session state to a file.

    Parameters:
        login_successful (bool): Whether the user is currently logged in.
        login_time (float): The time when the user logged in, in seconds since the epoch.
        current_user_id (int): The ID of the current user.

    The login session state is saved to a file named 'login.txt', with the format
    'login_successful,login_time,current_user_id'.
    """
    with open('login.txt', 'w') as f:
        f.write(f'{login_successful},{login_time},{current_user_id}')

def read_session_state():
    """
    Read the login session state from a file.

    Returns:
        tuple: A tuple containing the login session state, consisting of the
               login status (bool), the login time (float), and the current user ID (int).

    If the login session state file exists, the login status, login time, and current
    user ID are read from the file and returned as a tuple. Otherwise, default values
    are returned.
    """
    if os.path.isfile('login.txt'):
        with open('login.txt', 'r') as f:
            login_successful, login_time, current_user_id = f.read().split(',')
            login_successful = bool(login_successful)
            login_time = float(login_time)
            current_user_id =  int(current_user_id)
    else:
        login_successful = False
        login_time = None
        current_user_id = -1
    return login_successful, login_time, current_user_id 

def is_session_valid(login_successful, login_time):
    """
    Check whether a login session is still valid.

    Parameters:
        login_successful (bool): Whether the user is currently logged in.
        login_time (float): The time when the user logged in, in seconds since the epoch.

    Returns:
        bool: Whether the login session is still valid.

    If the user is logged in and the session has been active for more than 2 minutes, the
    login status is set to False and a message is printed indicating that the session
    has expired. Otherwise, the login status is left unchanged.
    """

    if login_successful:
        if time.time() - login_time > 120:
            login_successful = False
            print('Login session expired')
            return False
        else:
            return True

if __name__ == '__main__':
    
    parser = create_arg_parser()
    args = parser.parse_args()
    
    # Read user session state
    login_successful, login_time, current_user_id = read_session_state()
    
    # Process action commands 
    if args.command == "setup":
        # db.create_table()
        db.seed_db()
    elif args.command == "login":
        username = args.username 
        password = args.password
        login(username, password)
    elif args.command == "check-balance":
        if is_session_valid(login_successful, login_time):
            balance = db.check_account_balance(current_user_id)
            print(f"""The current balance is ${balance}""")
    elif args.command == "update-balance":
        if is_session_valid(login_successful, login_time):
            transaction_amount = args.transaction
            balance = db.update_account_balance(current_user_id, transaction_amount)
            print(f"""The updated balance is ${balance}""")
