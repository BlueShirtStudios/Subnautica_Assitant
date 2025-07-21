import subnautica_db

#My function collection
def loadMainMenu():
    print("==========================")
    print("SUBNAUTICA ASSISSTANT")
    print("==========================")
    print("What would you like to do do?")
    print("[0] Exit")
    print("[1] Search Blueprint")
    print("[2] View creature encyclopedia")
    
def checkOptionValid(option):
    if option < 0 :
      print("Invalid Option Selected. Please enter an option in the given range.")
      return False
    else:
        return True
    
def mainMenu_Setup():
    loadMainMenu()
    mainOption = int(input("Please enter the option you want to proceed with: "))
    
    #Check if option is valid
    while checkOptionValid(mainOption) != True:
        mainOption = int(input("Please enter the option you want to proceed with: "))
    return mainOption
    
    
#Start of main program
mainOption = mainMenu_Setup()

#If option is valid, proceed with determining what to do
match mainOption:
    case 0:
        print("Exiting the program...")
    case 1:
        print(f"Option {mainOption} selected")
    case 2: 
        subnautica_db.creatures_DB_Setup()
        print("--------------------------------------------------------------------------------------")
        print("What would you want to do?\n [0] Back to Main Menu \n[1] Search for a creature\n[2] Find creatures from specific biome\n[3] Find creatures by Depth")
        creature_Option = int(input("Please enter the number of the action you want to take. "))
        if creature_Option == 0:
            print("Returning to main menu.") #--> Somthing with while loop and mainMenu_Setup()
        elif creature_Option == 1:
            creature = input("What creature are you looking for: ")
            subnautica_db.search_CreatureByName(creature)
        