def get_user_selection() -> int:
    #Display an UI that looks like a app calling for help
    print("---- Emergency System Failover ----")
    print("Ï understand the current circumstances are unwanted, but please provide us with nessary information to boot the emergency system.")
    print("[1] Create New Alterra Account")
    print("[2] I already have an Alterra Account")
    print("[0] Exit")

    #Get the selected option from the user
    try:  
        user_option = int(input("Press the number of the wanted action: "))
        return user_option
    
    except TypeError as e:
        print(f"Please enter ONLY a number from the selected list.")
    
    except Exception as e:
        print(f"An unknown error has occurred: {e}")

def enter_username() -> str:
    try:
        while True:
            username = input("Enter a username: ").strip()

            if not username:
                print("Please enter a username. Empty spaces not allowed.")
                continue

            #Corrected error message length hint
            elif len(username) > 50:
                print("Username is too long. It must be shorter than 50 characters.")
                continue

            return username
        
    except TypeError as e:
        print(f"Please enter ONLY a letters.")
    
    except Exception as e:
        print(f"An unknown error has occurred: {e}")


def enter_password() -> str:
    try:
        while True:
            first_pass = input("Enter password: ")
            
            #Check for empty string before proceeding
            if not first_pass:
                print("Empty spaces are not allowed. Please enter a password.")
                continue

            second_pass = input("Enter the same password again: ")

            if not second_pass:
                print("Empty spaces are not allowed. Please re-enter the password.")
                continue

            if first_pass == second_pass:
                #Check length after match to avoid repeating input on mismatch
                if len(second_pass) > 256:
                    print("Password exceeds character cap (256 characters), please make the password shorter.")
                    continue

                return second_pass

            else:
                print("Passwords do not match. Please re-enter when asked.")
                
    except TypeError as e:
        print(f"Please enter reasnoble characters for a password.")
    
    except Exception as e:
        print(f"An unknown error has occurred: {e}")

def enter_name_and_surname() -> str:
    try:
        while True:
            name = input("Enter your name: ").strip()

            if not name:
                print("Please enter your name. Empty input not allowed.")
                continue

            elif len(name) > 50:
                print("Name exceeds the maximum amount of characters allowed (50).")
                continue

            surname = input("Enter your surname: ").strip()

            if not surname:
                print("Please enter your surname. Empty input not allowed.")
                continue

            elif len(surname) > 50:
                print("Surname exceeds the maximum amount of characters allowed (50).")
                continue

            combined = f"{name} {surname}"
            return combined
        
    except TypeError as e:
        print(f"Please enter ONLY a letters.")
    
    except Exception as e:
        print(f"An unknown error has occurred: {e}")

def enter_email() -> str:
    try:
        while True:
            email = input("Enter your email: ").strip()

            if not email:
                print("Please enter an email. Empty spaces not allowed.")
                continue

            elif len(email) > 100:
                print("Email is too long. It must be shorter than 100 characters.")
                continue

            return email
        
    except TypeError as e:
        print(f"Please enter characters for an email.")
    
    except Exception as e:
        print(f"An unknown error has occurred: {e}")


def add_new_user() -> tuple:
    #Use a list to build the details
    new_user_details = []
    new_user_details.append(enter_username())
    new_user_details.append(enter_password())
    new_user_details.append(enter_name_and_surname())
    new_user_details.append(enter_email())

    #Convert the list to a tuple for return
    return tuple(new_user_details)

def attempt_login() -> tuple:
    #Use a list to get the deatails
    user_details = []
    user_details.append(enter_username())
    user_details.append(enter_password())
    
    #Convert to tuple for return
    return tuple(user_details)
    