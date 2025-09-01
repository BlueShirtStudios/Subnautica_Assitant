""" MODULE DISCRIPTION
This module contains the details of the creatures and will work with it. Any output that needs details from creatures
will be called from here
"""
class Creature:
    """
    creature_id (int) : Primary Key in database for the creature
    name (str) : Name of the creature
    category (str) : Which category does the creature fall in, e.g. carnivore
    biomes (list[str]) : Biome/s where the creature is found
    behavior (str) : Behavior towards player and enviroment
    min_depth (int) : Minimum depth of the creature
    max_depth (int) : Max depth of the creature
    pda_entry (str) : The pda entry of the creature
    img_url (str) : Link for image of creature
    """
    def __init__(self,
                 creature_id : int = None,
                 name : str = None,
                 category : str = None,
                 biomes: list[str] = None,
                 behavior : str = None,
                 min_depth : int = None,
                 max_depth : int = None, 
                 pda_entry : str = None,
                 img_url : str =  None
                ):
        
        self.creature_id = creature_id
        self.name = name
        self.category = category
        self.biomes = biomes if not None else []
        self.behavior = behavior
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.pda_entry = pda_entry
        self.img_url = img_url
        
    def get_creature_id(self):
        return self.creature_id

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def get_biomes(self):
        return self.biomes

    def get_behavior(self):
        return self.behavior

    def get_min_depth(self):
        return self.min_depth

    def get_max_depth(self):
        return self.max_depth

    def get_pda_entry(self):
        return self.pda_entry

    def get_img_url(self):
        return self.img_url

    def set_creature_id(self, new_id: int):
        self.creature_id = new_id

    def set_name(self, new_name: str):
        self.name = new_name

    def set_category(self, new_category: str):
        self.category = new_category

    def set_biomes(self, new_biomes: list[str]):
        self.biomes = new_biomes

    def set_behavior(self, new_behavior: str):
        self.behavior = new_behavior

    def set_min_depth(self, new_min_depth : int):
        self.min_depth = new_min_depth

    def set_max_depth(self, new_max_depth : int):
        self.max_depth = new_max_depth

    def set_pda_entry(self, new_pda_entry: str):
        self.pda_entry = new_pda_entry

    def set_img_url(self, new_img_url: str):
        self.img_url = new_img_url
    
    def display_creature_info(self):
        print(f"Name: {self.name}")
        print(f"Category: {self.category}")
        print(f"Biomes: {self.biomes}")
        print(f"Behavior: {self.behavior}")
        print(f"Depth Range: {self.min_depth} - {self.max_depth}m")
        print(f"PDA Entry: {self.pda_entry}")
