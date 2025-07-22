import subnautica_db
import subnautica_ai

#My function collection
def loadMainMenu():
    print("==========================")
    print("SUBNAUTICA ASSISSTANT")
    print("==========================")
    print("What would you like to do do?")
    print("[0] Exit")
    print("[1] Search Blueprint")
    print("[2] View creature encyclopedia")
    print("[3] Personal Logbook")
    print("[4] AI Assitant")
    
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

def creatureEncyclopedia_Setup():
    print("--------------------------------------------------------------------------------------")
    print("What would you want to do?\n[0] Back to Main Menu \n[1] Search for a creature\n[2] Find creatures from specific biome\n[3] Find creatures by Depth")
    creature_option = int(input("Please enter the number of the action you want to take. "))
    return creature_option
    
#Start of main program - Start the main while loop
bMain_Continue = True

#If option is valid, proceed with determining what to do
while bMain_Continue: 
    mainOption = mainMenu_Setup()
    match mainOption:
        case 0:
            #Exit program
            bContinue = False
            print("Exiting the program...")
            exit()
            
        case 1:
            #View blue prints
            print(f"Option {mainOption} selected")
            
        case 2: 
            #View Creatures
            subnautica_db.creatures_DB_Setup()
            bCreature_Encyclopedia = True
            while bCreature_Encyclopedia:
                creature_Option = creatureEncyclopedia_Setup()
                if creature_Option == 0:
                    print("Returning to main menu...")
                    bCreature_Encyclopedia = False
                    continue
                
                elif creature_Option == 1:
                    creature = input("What creature are you looking for: ")
                    subnautica_db.search_CreatureByName(creature)
                    continue
                    
                elif creature_Option == 2:
                    biome = input("What is the biome your looking to explore: ")
                    subnautica_db.search_CreatureByBiome(biome)
                    continue
                    
                elif creature_Option == 3:
                    depth = input("Enter the depth desired to explore, and I will enlighten you of the fauna.")
                    print("Not enough will power for this yet...")
                    #Figure out how to do this
                    continue
        case 3:
            #User recored finds
            print("")
        case 4:
            #AI assisant help
            subnautica_ai.start_AI()