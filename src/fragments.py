""" MODULE DISCRIPTION
All the details of the fragments from the database will be loaded in here for use. Any output and
manipulation will be done with data from here
"""

class Fragment:
    """
    fragmentID (int) : Primary Key of fragment in the fragment_details table
    name (str) : Fragment Name
    total_fragments_needed (int) : How many fragments the player must collect before crafting it
    list_locations (list[str]) : Locations where this fragment can be found
    depth_level (str) : Depth Range where fragment spawns are expected
    list_dangers (list[str]) : Possible dangers near fragments
    list_needed_tools (lisr[str]) : Tools/Equipment you will need to get tp the fragment
    """
    def __init__(self, 
                 fragmentID : int = None,
                 name : str = None,
                 total_fragments_needed : int = None,
                 list_locations : list[str] = None, 
                 depth_level : str = None,
                 list_dangers : list[str] = None, 
                 list_needed_tools : list[str] = None):
        self.fragmentID = fragmentID
        self.name = name
        self.total_fragments_needed = total_fragments_needed
        self.locations = list_locations if list_locations is not None else []
        self.depth_level = depth_level
        self.dangers = list_dangers if list_dangers is not None else []
        self.needed_tools = list_needed_tools if list_needed_tools is not None else []

    def get_fragmentID(self):
        return self.fragmentID
    
    def set_fragmentID(self, fragmentID):
        self.fragmentID = fragmentID

    def get_name(self):
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_total_fragments_needed(self):
        return self.total_fragments_needed

    def set_total_fragments_needed(self, total_fragments_needed: int):
        self.total_fragments_needed = total_fragments_needed

    def get_locations(self):
        return self.locations

    def set_locations(self, locations: list[str]):
        self.locations = locations

    def get_depth_level(self):
        return self.depth_level

    def set_depth_level(self, depth_level: str):
        self.depth_level = depth_level

    def get_dangers(self):
        return self.dangers

    def set_dangers(self, dangers: list[str]):
        self.dangers = dangers

    def get_needed_tools(self):
        return self.needed_tools

    def set_needed_tools(self, needed_tools: list[str]):
        self.needed_tools = needed_tools
        
    def get_all_details(self):
        print(f"Fragment Name: {self.name}\nTotal fragments needed to scan: {self.total_fragments_needed}\n")
        print(f"Locations Found: {self.locations}\nDepth Found At: {self.depth_level}\n")
        print(f"Possible Dangers: {self.dangers}\nNeeded Tools/Equipment: {self.needed_tools}")

