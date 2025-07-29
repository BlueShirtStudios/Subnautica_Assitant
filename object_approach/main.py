from creature_manger import CreatureManager
from menu import Menu

DB_NAME = "subnautica.db"

"""
Generate the staring point for the command-line interface. This section contains code to build the main menu,
which will display the options for the user that can be done. The user's input will then determine which action
will be done.
"""
#Create an instance of the MainMenu Class
obj_main_menu = Menu()

#Create the interface + Asks input from user + Vaildate until correct
obj_main_menu.intailize_MainMenu()
main_Option = obj_main_menu.get_User_Option()
obj_main_menu.validate_Option(main_Option)

#Depending on user option, will carry out certain operation
while obj_main_menu.validate_main_option(main_Option) != True:
    main_Option = obj_main_menu.get_User_Option()
    
match main_Option:
    case 0: #Exit Program
        obj_main_menu.exit_program()
        
    case 1: #Blue Print Lookup
        print("Insert code here...")
        
    case 2: #Creature Enclycopedia
        #Create Creature Manager object intance
        creature_manager = CreatureManager(DB_NAME)
        creature_manager.check_creaturesDB()
        
        #Create Menu for Encyclopedia + Get option and Validate
        encyclopedia_menu = Menu()
        encyclopedia_menu.load_encyclopedia_menu()
        encyclopedia_option = encyclopedia_menu.get_User_Option()
        while encyclopedia_menu.validate_encyclopedia_option(encyclopedia_option) != True:
            encyclopedia_option = encyclopedia_menu.get_User_Option()
        
        creature_manager.get_Creature_byName("Reaper")
        
