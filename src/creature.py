class Creature:
    def __init__(self,
                 creature_id : int = None,
                 name : str = None,
                 category : str = None,
                 biomes : list[str] = None,
                 behavior : str = None,
                 danger_level : str = None,
                 depth_level : str = None, 
                 pda_entry : str = None,
                 img_url : str =  None
                ):
        
        self.creature_id = creature_id
        self.name = name
        self.category = category
        self.biomes = biomes if biomes is not None else []
        self.behavior = behavior
        self.danger_level = danger_level
        self.depth_level = depth_level
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

    def get_danger_level(self):
        return self.danger_level

    def get_depth_level(self):
        return self.depth_level

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

    def set_danger_level(self, new_danger_level: str):
        self.danger_level = new_danger_level

    def set_depth_level(self, new_depth_level: str):
        self.depth_level = new_depth_level

    def set_pda_entry(self, new_pda_entry: str):
        self.pda_entry = new_pda_entry

    def set_img_url(self, new_img_url: str):
        self.img_url = new_img_url
    
    def display_creature_info(self):
        print(f"Name: {self.name}")
        print(f"Category: {self.category}")
        print(f"Biomes: {self.biomes}")
        print(f"Behavior: {self.behavior}")
        print(f"Danger_Level: {self.danger_level}")
        print(f"Depth-Level: {self.depth_level}")
        print(f"PDA Entry: {self.pda_entry}")
