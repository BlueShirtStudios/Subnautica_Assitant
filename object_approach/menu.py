class MainMenu:
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
    
    def _set_User_Option(self, newOption):
        self.option = newOption
    
    def validate_Option(self, option):
        #Set the new option to the attribute
        self._set_User_Option(option)
        
        #Determine if option is valid
        if (self.option >= 0) and (self.option <= 4):
            return True
        else:
            print("Invalid Option.")
            return False
        
    def exit_program(self):
        print("Safe Travels. Exiting the Assitant...")
        exit()
