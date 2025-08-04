import sqlite3
from typing import List, Optional
import time

from creature import Creature

creature = Creature()

""" MODULE DESCRIPTION
This module will manage all things related to the creature class. Any queries, filtering, etc. will be handled here.
On request from encyclopedia menu, any needed data will be extracted from the database to the Creature object and then 
will be returned as specified.
"""

class CreatureManager:
    """Manager of the creature class. Handles any database queries that might find its way here.

       Attributes:
       db_name (str) : Name of SQLite3 database
    """
    
    def __init__(self, DB_Name : str):
        self.db_name = DB_Name
        
    def _connect(self):
        """Establish connection to database"""
        try:    
            conn = sqlite3.connect(self.db_name)
            return conn
        except sqlite3.Error as e:
            print(f"Error with conecting to database: {e}")
        return None
    
    def _create_CreatureTable(self):
        with self._connect() as conn:
            if conn:
                cursor = conn.cursor()
                cursor.execute('''
                        CREATE TABLE IF NOT EXISTS creatures (
                        creature_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT,
                        biomes TEXT,
                        behavior TEXT,
                        danger_level TEXT,
                        depth_range TEXT,
                        pda_entry TEXT,
                        image_url TEXT
                    )
                ''')
                conn.commit()
                print("Table creatures checked successfully")
            else:
                print("Could not connect/create the table")
                
        cursor.close()
        conn.close()
                
    def _add_Creature(self, name, category, biomes, behavior, danger_level, depth_range, pda_entry, image_url):
        with self._connect() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('''
                                   INSERT INTO creatures (name, category, biomes, behavior, danger_level, depth_range, pda_entry, image_url)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                   ''', (name, category, biomes, behavior, danger_level, depth_range, pda_entry, image_url))
                    conn.commit()
                except sqlite3.IntegrityError:
                    print(f"Error: Creature: {name} already exists.")
                except sqlite3.Error as e:
                    print(f"Error with adding creature: {e}")
                    
        cursor.close()
        conn.close()                
    def _populate_initial_data(self):
        """
        This will populate the creature table in the database in the first run of the program
        """
        
        self._add_Creature("Peeper", "Fish", "Safe Shallows, Kelp Forest, Grassy Plateaus, Mushroom Forest, Sparse Reef", "Passive, Scavenger", "Low", "0-250m", "A small, common herbivore. Its large eye is a curious adaptation to low light conditions.", "https://static.wikia.nocookie.net/subnautica/images/a/ae/Peeper.png")
        self._add_Creature("Garryfish", "Fish", "Safe Shallows", "Passive, Flighty", "Very Low", "0-50m", "A small, fast-moving fish often found in shallow waters. Known for its quick bursts of speed.", "https://static.wikia.nocookie.net/subnautica/images/e/ef/Garryfish.png")
        self._add_Creature("Bladderfish", "Fish", "Safe Shallows, Kelp Forest", "Passive", "Very Low", "0-100m", "Contains internal air sacs that allow it to generate drinkable water when cooked, or breathable oxygen when alive.", "https://static.wikia.nocookie.net/subnautica/images/2/23/Bladderfish.png")
        self._add_Creature("Spinefish", "Fish", "Grassy Plateaus, Safe Shallows", "Passive, Defensive (spines)", "Low", "0-100m", "A small, bony fish with defensive spines. Offers little nutritional value.", "https://static.wikia.nocookie.net/subnautica/images/8/87/Spinefish.png")
        self._add_Creature("Holefish", "Fish", "Safe Shallows", "Passive", "Very Low", "0-50m", "A small fish with a distinctive hole through its body. Edible.", "https://static.wikia.nocookie.net/subnautica/images/c/c2/Holefish.png")
        self._add_Creature("Boomerang", "Fish", "Safe Shallows, Kelp Forest", "Passive", "Very Low", "0-100m", "Named for its distinctive shape, this fish is a common sight in shallow waters.", "https://static.wikia.nocookie.net/subnautica/images/7/7b/Boomerang.png")
        self._add_Creature("Eyeye", "Fish", "Kelp Forest, Safe Shallows, Grassy Plateaus", "Passive", "Low", "0-200m", "A small fish with a large, bioluminescent eye. Primarily found near kelp forests.", "https://static.wikia.nocookie.net/subnautica/images/0/05/Eyeye.png")
        self._add_Creature("Hoverfish", "Fish", "Safe Shallows, Grassy Plateaus", "Passive, Docile", "Very Low", "0-100m", "A curious, docile fish that hovers in the water, making it easy to catch.", "https://static.wikia.nocookie.net/subnautica/images/4/4c/Hoverfish.png")
        self._add_Creature("Gasopod", "Herbivore", "Safe Shallows, Grassy Plateaus, Mushroom Forest", "Defensive (releases gas)", "Medium", "0-100m", "A passive herbivore that releases poisonous gas pods when threatened.", "https://static.wikia.nocookie.net/subnautica/images/3/36/Gasopod.png")
        self._add_Creature("Reefback Leviathan", "Leviathan, Herbivore", "Safe Shallows, Grassy Plateaus, Grand Reef, Sea Treader's Tunnel, Bulb Zone", "Passive, Migratory", "Low", "0-500m", "A docile, enormous leviathan-class herbivore. Its shell supports a complex ecosystem.", "https://static.wikia.nocookie.net/subnautica/images/6/60/Reefback_Leviathan_Scan.png")
        self._add_Creature("Rabbit Ray", "Fish", "Safe Shallows, Grassy Plateaus", "Passive, Curious", "Very Low", "0-100m", "A docile herbivore, easily startled, but known to approach divers out of curiosity.", "https://static.wikia.nocookie.net/subnautica/images/7/7b/Rabbit_Ray.png")
        self._add_Creature("Cuddlefish", "Companion", "Lost River (Egg), Deep Grand Reef (Egg), Dunes (Egg), Mushroom Forest (Egg)", "Passive, Playful, Companion", "None", "0-1700m", "An ancient, highly intelligent, and docile species with complex emotional responses. Can be befriended.", "https://static.wikia.nocookie.net/subnautica/images/8/87/Cuddlefish.png")
        self._add_Creature("Jellyray", "Filter Feeder", "Grand Reef, Bulb Zone", "Passive, Filter Feeder", "Low", "100-800m", "A large, graceful filter feeder with bioluminescent fins. Gentle and majestic.", "https://static.wikia.nocookie.net/subnautica/images/6/60/Jellyray.png")
        self._add_Creature("Shuttlebug", "Filter Feeder", "Blood Kelp Zone", "Passive, Filter Feeder", "Very Low", "300-800m", "A small, resilient filter feeder that can survive in harsh environments.", "https://static.wikia.nocookie.net/subnautica/images/c/c3/Shuttlebug.png")
        self._add_Creature("Skyray", "Filter Feeder", "Floating Island, Mountain Island (surface/shallow water)", "Passive, Filter Feeder", "Very Low", "0-10m", "An aerial filter feeder that glides above the water, occasionally dipping down to feed.", "https://static.wikia.nocookie.net/subnautica/images/4/4c/Skyray.png")
        self._add_Creature("Floater (Small)", "Detritivore", "Safe Shallows, Kelp Forest, Grassy Plateaus (attaches to objects/creatures)", "Passive, Attaches to objects", "Very Low", "0-500m", "A symbiotic organism that attaches to objects, causing them to float. Non-aggressive.", "https://static.wikia.nocookie.net/subnautica/images/a/ae/Floater.png")
        self._add_Creature("Floater (Large)", "Detritivore", "Floating Island", "Passive, Attaches to objects", "Very Low", "0-50m", "A larger variant of the floater, responsible for the buoyancy of the Floating Island.", "https://static.wikia.nocookie.net/subnautica/images/a/ae/Floater.png")
        self._add_Creature("Sea Treader Leviathan", "Leviathan, Herbivore", "Sea Treader's Path", "Passive, Migratory", "Medium", "100-300m", "A massive, docile leviathan that 'treads' the seafloor, uncovering valuable resources.", "https://static.wikia.nocookie.net/subnautica/images/5/5e/Sea_Treader_Leviathan.png")
        self._add_Creature("Biter", "Fish", "Kelp Forest, Safe Shallows (rare), Blood Kelp Zone, Grassy Plateaus", "Aggressive", "Low", "0-400m", "A small, aggressive carnivore that attacks on sight.", "https://static.wikia.nocookie.net/subnautica/images/4/47/Biter.png")
        self._add_Creature("Bleeder", "Parasite", "Aurora, Blood Kelp Zone, Sparse Reef, Sea Treader's Path", "Aggressive, Parasitic", "Low", "0-500m", "A parasitic creature that attaches to organisms and drains blood. Dangerous in groups.", "https://static.wikia.nocookie.net/subnautica/images/4/42/Bleeder.png")
        self._add_Creature("Stalker", "Carnivore", "Kelp Forest, Grassy Plateaus", "Territorial, Curious (steals metal)", "Medium", "0-200m", "An aggressive predator known for collecting metal salvage, possibly for its den.", "https://static.wikia.nocookie.net/subnautica/images/d/d4/Stalker_Scan.png")
        self._add_Creature("Crabsnake", "Fauna", "Jellyshroom Cave", "Aggressive, Ambush Predator", "High", "100-300m", "A highly aggressive creature that hides within Jellyshrooms, striking out at passing vehicles and divers.", "https://static.wikia.nocookie.net/subnautica/images/a/a2/Crabsnake_Scan.png")
        self._add_Creature("Bone Shark", "Carnivore", "Grand Reef, Bulb Zone, Blood Kelp Zone, Mountains", "Aggressive, Territorial", "High", "100-800m", "A heavily armored predator capable of significant damage. Attacks vehicles relentlessly.", "https://static.wikia.nocookie.net/subnautica/images/2/22/Bone_Shark.png")
        self._add_Creature("Crashfish", "Carnivore, Explosive", "Safe Shallows, Kelp Forest, Grassy Plateaus (found in Sulfur Plants)", "Aggressive, Suicidal (explodes)", "High", "0-100m", "A highly aggressive, territorial creature that charges intruders and explodes upon contact.", "https://static.wikia.nocookie.net/subnautica/images/d/d4/Crashfish.png")
        self._add_Creature("Cave Crawler", "Carnivore", "Safe Shallows (Caves), Kelp Forest (Caves), Grassy Plateaus (Caves), Aurora", "Aggressive, Swarming", "Low", "0-300m", "A small, scuttling arthropod that swarms perceived threats. Primarily found in caves and wreckages.", "https://static.wikia.nocookie.net/subnautica/images/2/22/Cave_Crawler.png")
        self._add_Creature("Ampeel", "Leviathan", "Blood Kelp Zone, Grand Reef", "Aggressive, Electric", "High", "100-800m", "A large, serpentine predator that uses electrical discharges to incapacitate prey.", "https://static.wikia.nocookie.net/subnautica/images/6/6f/Ampeel_Scan.png")
        self._add_Creature("Crab Squid", "Carnivore", "Grand Reef, Blood Kelp Zone (South)", "Aggressive, EMP pulse", "High", "200-800m", "An amphibious predator that uses EMP pulses to disable electronics before attacking.", "https://static.wikia.nocookie.net/subnautica/images/6/6b/Crab_Squid.png")
        self._add_Creature("Lava Larva", "Parasite, Energy Drainer", "Inactive Lava Zone, Active Lava Zone, Lost River", "Aggressive, Parasitic (drains power)", "Medium", "700-1700m", "A parasitic creature that attaches to vehicles and drains their power cells.", "https://static.wikia.nocookie.net/subnautica/images/4/4c/Lava_Larva.png")
        self._add_Creature("Lava Lizard", "Carnivore", "Inactive Lava Zone, Active Lava Zone, Lava Castle", "Aggressive, Fire-resistant", "Medium", "800-1700m", "A heat-resistant carnivore that can launch volcanic projectiles. Found exclusively in lava zones.", "https://static.wikia.nocookie.net/subnautica/images/d/d4/Lava_Lizard.png")
        self._add_Creature("Mesmer", "Carnivore", "Blood Kelp Zone, Grand Reef, Sea Treader's Path", "Aggressive, Hypnotic", "High", "100-600m", "A master of hypnotic camouflage, luring prey with visual and auditory deception before attacking.", "https://static.wikia.nocookie.net/subnautica/images/6/6b/Mesmer.png")
        self._add_Creature("River Prowler", "Carnivore", "Lost River", "Aggressive, Territorial", "High", "400-900m", "An agile, territorial predator found in the Lost River. Possesses powerful jaws.", "https://static.wikia.nocookie.net/subnautica/images/2/22/River_Prowler.png")
        self._add_Creature("Warper", "Aggressive, Alien", "Lost River, Inactive Lava Zone, Blood Kelp Zone, Alien Bases", "Aggressive, Teleportation, Infection hunter", "Extreme", "200-1700m", "An alien construct designed to contain the Kharaa bacterium. Capable of teleporting targets.", "https://static.wikia.nocookie.net/subnautica/images/4/47/Warper.png")
        self._add_Creature("Reaper Leviathan", "Leviathan", "Crash Zone, Mountains, Dunes", "Aggressive, Territorial, Apex Predator", "Extreme", "50-1000m", "Apex predator. Displays extreme territoriality and will attack any perceived threat on sight. Avoid at all costs.", "https://static.wikia.nocookie.net/subnautica/images/2/22/Reaper_Leviathan_Scan.png")
        self._add_Creature("Sea Dragon Leviathan", "Leviathan", "Inactive Lava Zone, Active Lava Zone", "Aggressive, Fire-breather", "Extreme", "900-1700m", "Massive leviathan, capable of spitting molten rock and superheated plasma.", "https://static.wikia.nocookie.net/subnautica/images/6/6b/Sea_Dragon_Leviathan_Scan.png")
        self._add_Creature("Ghost Leviathan", "Leviathan", "Lost River, Grand Reef (Juvenile), Void (Adult)", "Aggressive, Highly Territorial", "Extreme", "400-3000m", "Large, translucent leviathan. Juveniles are territorial, adults patrol the ecological dead zone.", "https://static.wikia.nocookie.net/subnautica/images/c/c3/Ghost_Leviathan_Juvenile_Scan.png")
       
        
    def check_creaturesDB(self):
        #Connect to DB
        with self._connect() as conn:
            if not conn:
                print("Could not connect to database.")
                return

        #Check if table exists
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='creatures'")
        if cursor.fetchone() is None:
            self._create_CreatureTable()

        #Check if table is empty
        cursor.execute("SELECT COUNT(*) FROM creatures")
        result = cursor.fetchone()
        if result and result[0] == 0:
            self._populate_initial_data()

        cursor.close()
        conn.close()
        
    def get_creature_by_name(self, creature_name : str):
        #Connect to DB
        with self._connect() as conn:
            if not conn:
                print("Could not connect to database.")
                return
        
        #Setup Query
        cursor = conn.cursor()
        sql_query = "SELECT * FROM creatures WHERE name LIKE ?"
        cursor.execute(sql_query, (f"%{creature_name}%", ))    
        
        #Add the record to the creature object 
        tuple_all_records = cursor.fetchall()
        if tuple_all_records:
            print("Retreiving information on all creatures with similer name...")
            print("------------------------------------------------------------")
            for tuple_db_record in tuple_all_records: 
                creature.set_creature_id(tuple_db_record[0])
                creature.set_name(tuple_db_record[1])
                creature.set_category(tuple_db_record[2])
                creature.set_biomes(tuple_db_record[3].split(',') if tuple_db_record[3] else [])
                creature.set_behavior(tuple_db_record[4])
                creature.set_danger_level(tuple_db_record[5])
                creature.set_depth_level(tuple_db_record[6])
                creature.set_pda_entry(tuple_db_record[7])
                creature.set_img_url(tuple_db_record[8])
                
                #Print the results
                creature.display_creature_info()  
                print("------------------------------------------------------------")
                time.sleep(5)
                 
        else:
            print("No creature found with such name. Please make sure that the creature does exist.")
            
        cursor.close()
        conn.close()
    
    def get_creatures_in_biome(self, search_biome: str):
        #Connect to DB
        with self._connect() as conn:
            if not conn:
                print("Could not connect to database.")
                return
            
        #Create Query
        cursor = conn.cursor()
        sql_query = "SELECT * FROM creatures WHERE biomes LIKE ?"
        cursor.execute(sql_query, (f"%{search_biome}%", ))    
        
        #Add the record to the creature object 
        tuple_all_records = cursor.fetchall()
        if tuple_all_records:
            print(f"Searching for creatures in {search_biome}...")
            print("------------------------------------------------------------")
            for tuple_db_record in tuple_all_records:
                creature.set_name(tuple_db_record[1])
                creature.set_category(tuple_db_record[2])
                creature.set_behavior(tuple_db_record[4])
                creature.set_danger_level(tuple_db_record[5])
                        
                #Get Results
                result = f"Name: {creature.get_name()}\nCategory: {creature.get_category()}\nBehavior: {creature.get_behavior()}\nDanger-level: {creature.get_danger_level()}\n" 
                print(result) 
                print("------------------------------------------------------------")
                time.sleep(2)           
        else:
            print("Creatures in biome not found. Please make sure your searched biome exists.")
    
    def get_creature_by_category(self, search_category : str):
        #Connect to DB
        with self._connect() as conn:
            if not conn:
                print("Could not connect to database.")
                return
            
        #Create Query
        cursor = conn.cursor()
        sql_query = "SELECT * FROM creatures WHERE category LIKE ?"
        cursor.execute(sql_query, (f"%{search_category}%", ))  
        
        #Add the record to the creature object 
        tuple_all_records = cursor.fetchall()
        if tuple_all_records:
            print(f"Searching for creatures in {search_category}...\n")
            print("------------------------------------------------------------")
            for tuple_db_record in tuple_all_records:
                creature.set_name(tuple_db_record[1])
                creature.set_biomes(tuple_db_record[3].split(',') if tuple_db_record[3] else [])
                creature.set_danger_level(tuple_db_record[5])
                creature.set_depth_level(tuple_db_record[6])
                creature.set_pda_entry(tuple_db_record[7])
                
                #Print Results
                result = f"Name: {creature.get_name()}\nBiomes: {creature.get_biomes()}\nDanger-level: {creature.get_danger_level()}\nDepth-Level: {creature.get_depth_level()}\nPDA Entry: {creature.get_pda_entry()}\n"
                print(result)
                print("------------------------------------------------------------")
                time.sleep(2)
                
        cursor.close()
        conn.close()