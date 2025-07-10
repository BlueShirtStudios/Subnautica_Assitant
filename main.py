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
    
#The actual program
loadMainMenu()
option = int(input("Please enter the option you want to proceed with: "))

#Check if option is valid
while checkOptionValid(option) != True:
    option = int(input("Please enter the option you want to proceed with: "))
    
#If option is valid, proceed with determining what to do
match option:
    case 0:
        print("Exiting the program...")
    case 1:
        print(f"Option {option} selected")
    case 2: 
        #Set the database up for use
        subnautica_db.create_CreatureTable()
        subnautica_db.check_creaturesDB()
        subnautica_db.get_allCreatures()
        