import main_config
import input_handler as iph
from data_access import UserDataAccessor
from ai_assitant import Gemini_AI_Agent

#Intialize Instances for run
UDA = UserDataAccessor()

#This is where the implentation of the agent lies  
def boot_emergency_systems():
    ALT = Gemini_AI_Agent(main_config.AI_CONFIGS)

    run = True

    #Run ALT
    while (run):
        user_question = input("What is you question? ").strip()
        if (user_question[0] == "/"):
            ALT.assit_commands.run_command(user_question)
        
        else:
            response = ALT.send_message(user_question)
            print(response)

#Display an UI that looks like a app calling for help
print("---- Emergency System Failover ----")
print("Ï understand the current circumstances are unwanted, but please provide us with nessary information to boot the emergency system.")
print("[1] Create New Alterra Account")
print("[2] I already have an Alterra Account")
print("[0] Exit")

#Get the selected option from the user
user_option = int(input("Press the number of the wanted action: "))
match user_option:
    case 0:
        print("Exiting Emergency System Failover...")
        exit()
    
    case 1:
        #Creates the new user
        tuple_new_user = iph.add_new_user()
        combined = tuple_new_user[2].split()
        name = combined[0]
        surname = combined[1]
        UDA.add_new_user(tuple_new_user[0], tuple_new_user[1], name, surname, tuple_new_user[3])
 
    case 2: 
        #Provides user with login attempt
        log_attempt = 0
        while log_attempt <= 3:
           tuple_entered_user = iph.attempt_login()
           
           #Checks if a user with those credentials exists
           userID = UDA.login_user(tuple_entered_user[0], tuple_entered_user[1])
           if not userID:
            print("Username or password does not match. Please try again.")
            log_attempt += 1
            print(f"Remaining login attempt: {3 - log_attempt}")
            
           else:
               print("Successfully logged in. Booting emergency systems...")
               boot_emergency_systems()
         
    case _:
        print("Invalid case option occured.")