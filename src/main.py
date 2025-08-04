from creature_manger import CreatureManager
from ai_assitant import AI_Assitant
from menu import Menu

DB_NAME = "subnautica.db"

""" MODULE DESCRIPTION   
Generate the staring point for the command-line interface. This section contains code to build the main menu,
which will display the options for the user that can be done. The user's input will then determine which action
will be done.
"""
#Create an instance of the MainMenu Class
obj_main_menu = Menu()
    
continue_program = True

while continue_program == True:
    #Create the interface + Asks input from user + Vaildate until correct
    obj_main_menu.intailize_MainMenu()
    main_Option = obj_main_menu.get_User_Option()
    while obj_main_menu.validate_main_option(main_Option) == False:
        main_Option = obj_main_menu.get_User_Option()

    #Depending on user option, will carry out certain operation
    match main_Option:
        case 0: #Exit Program
            continue_program = False
            obj_main_menu.exit_program()
        
        case 1: #Blue Print Lookup
            print("Insert code here...")
        
        case 2: #Creature Enclycopedia        
            continue_encyclopedia = True
            
            #Create Creature Manager and Encyclopedia object instance
            creature_manager = CreatureManager(DB_NAME)
            creature_manager.check_creaturesDB()
            encyclopedia_menu = Menu()
            
            while continue_encyclopedia == True:
                #Create Menu for Encyclopedia + Get option and Validate
                encyclopedia_menu.load_encyclopedia_menu()
                encyclopedia_option = encyclopedia_menu.get_User_Option()
                while encyclopedia_menu.validate_encyclopedia_option(encyclopedia_option) != True:
                    encyclopedia_option = encyclopedia_menu.get_User_Option()
                
                #Depend on option what action will be taken    
                match encyclopedia_option:
                    case 0:
                        continue_encyclopedia = False
                        continue
                    
                    case 1:
                        search_creature = input("What creature are you looking for? ")
                        if search_creature == 0:
                            continue
                        else:
                            creature_manager.get_creature_by_name(search_creature)
                            continue
                        
                    case 2:
                        search_biome = input("What biome are you searching for? ")
                        creature_manager.get_creatures_in_biome(search_biome)
                        continue
                        
                    case 3: 
                        search_category = input("For what category are you searching for? ")
                        creature_manager.get_creature_by_category(search_category)
                        continue
                    
        case 1: #IDK this part is under discussion
            print("Insert code here...")
        
        case 4:
            #Create Assitant Instace
            subnautica_assitant = AI_Assitant()
            
            #Start Chatting
            subnautica_assitant.start_chatting()
            continue