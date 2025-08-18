from creature_manager import CreatureManager
from fragment_manager import Fragment_Manager
from ai_assitant import AI_Assitant
from menu import MainMenu, Encyclopedia, FragmentLookUp

DB_NAME = "subnautica.db"

""" MODULE DESCRIPTION   
Generate the staring point for the command-line interface. This section contains code to build the main menu,
which will display the options for the user that can be done. The user's input will then determine which action
will be done.
"""
#Create an instance of the MainMenu Class
main_menu = MainMenu()
    
continue_program = True

while continue_program == True:
    #Create the interface + Asks input from user + Vaildate until correct
    main_menu.intailize_MainMenu()
    main_Option = main_menu.get_User_Option()
    while main_menu.validate_main_option(main_Option) == False:
        main_Option = main_menu.get_User_Option()

    #Depending on user option, will carry out certain operation
    match main_Option:
        case 0: #Exit Program
            continue_program = False
            main_menu.exit_program()
        
        case 1: #Fragment Look Up
            continue_fragment_lookup = True
            
            #Create Fragment and fragment manager object instance
            fragment_manager = Fragment_Manager(DB_NAME)
            fragment_manager.check_fragment_table()
            fragment_lookup_menu = FragmentLookUp()
            
            while continue_fragment_lookup == True:
                #Create CLI-Menu and Validate Input
                fragment_lookup_menu.load_fragment_lookup_menu()
                fragment_lookup_option = fragment_lookup_menu.get_User_Option()
                while fragment_lookup_menu.validate_fragment_lookup_option(fragment_lookup_option) != True:
                    fragment_lookup_option = fragment_lookup_menu.get_User_Option()
                
                #Depending on option, will carry out action
                match fragment_lookup_option:
                    case 0: #Exit Fragment Lookup
                        continue_fragment_lookup = False
                        continue
                    
                    case 1: #Search for Fragment By Name
                        fragment_name = input("What is the fragment you are looking for? ")
                        fragment_manager.get_fragment_by_name(fragment_name)
                        continue
            
            
            
        
        case 2: #Creature Enclycopedia        
            continue_encyclopedia = True
            
            #Create Creature Manager and Encyclopedia object instance
            creature_manager = CreatureManager(DB_NAME)
            if creature_manager.check_db_creature_details() == False:
                print("Check is unsuccessfull, table creation or table population was problematic")
                main_menu.exit_program()
                
            encyclopedia_menu = Encyclopedia()
            
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
                        if search_creature == " ":
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
                    
        case 3: #IDK this part is under discussion
            print("Insert code here...")
        
        case 4:
            #Create Assitant Instace
            subnautica_assitant = AI_Assitant()
            
            #Start Chatting
            subnautica_assitant.start_chatting()
            continue