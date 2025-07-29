class Menu:
    def __init__(self, option : int = None):
        self.option = option
    
    def intailize_MainMenu(self):
        print("==========================")
        print("SUBNAUTICA ASSISSTANT")
        print("==========================")
        print("What would you like to do do?")
        print("[0] Exit")
        print("[1] Search Blueprint")
        print("[2] View creature encyclopedia")
        print("[3] Personal Logbook")
        print("[4] AI Assitant")
    
    def get_User_Option(self):
        while True:
            try: 
                option = int(input("Please enter the option you want to proceed with: "))
                return option
            except ValueError:
                print("Invalid Input. Please enter a value intger ")
    
    def _set_user_option(self, newOption):
        self.option = newOption
    
    def validate_main_option(self, option):
        #Set the new option to the attribute
        self._set_user_option(option)
        
        #Determine if option is valid
        if (self.option >= 0) and (self.option <= 4):
            return True
        else:
            print("Invalid Option.")
            return False
        
    def exit_program(self):
        print("Safe Travels. Exiting the Assitant...")
        exit()
        
    def load_encyclopedia_menu(self):
        print("===========================\nENCYCLOPEDIA\n===============================")
        print("What would you like to do?")
        print("[0] Return to main menu")
        print("[1] Search a creature by name")
        print("[2] Search for creatures in a certain biome")
        print("[3] Search for creatures in a certain category")
        
    def validate_encyclopedia_option(self, option : int):
        self._set_user_option
        if (option >= 0) and (option <= 3):
            return True
        else:
            print("Invalid Option. Please select an integer option in the given range.")
            return False
        
        
