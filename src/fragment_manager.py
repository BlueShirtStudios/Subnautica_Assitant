import sqlite3
import time
from typing import List, Optional
from fragments import Fragment

fragment = Fragment()

""" MODULE DESCRIPTION
This module will manage all things related to the fragment class. Any queries, filtering, etc. will be handled here.
On request from fragment lookup menu, any needed data will be extracted from the database to the Fragment object and then 
will be returned as specified.
"""

class Fragment_Manager:
    """
    db_name (str) : Name of Database
    """
    def __init__(self, DB_Name : str):
        self.db_name = DB_Name
        
    def _connect(self):
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except sqlite3.Error as e:
            print(f"Could not connect to database: {e}")
            
    def _create_fragment_table(self):
        with self._connect() as conn:
            if conn:
                cursor = conn.cursor()
                cursor.execute('''
                        CREATE TABLE IF NOT EXISTS fragment_details (
                        fragment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        total_fragments_needed INT,
                        locations TEXT,
                        depth_level TEXT,
                        dangers TEXT,
                        needed_tools TEXT
                    )
                ''')
                conn.commit()
                print("Table was created successfully.")
            else:
                print("Could not create the Table.")
        cursor.close()
        conn.close()
        
    def delete_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS fragment_details")

        conn.commit()
        conn.close()
        print("Table Deleted.")
                
    def _add_fragment_details(self, name : str, total_fragment : int, locations : str, depth_level : str,
                              dangers : str, needed_tools : str):
        with self._connect() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('''
                                   INSERT INTO fragment_details (name, total_fragments_needed, locations, depth_level, dangers, needed_tools)
                                   VALUES (?, ?, ?, ?, ?, ?)
                                   ''', (name, total_fragment, locations, depth_level, dangers, needed_tools))
                    conn.commit()
                    print(f"Fragment: {name} was succesfully added")
                except sqlite3.IntegrityError:
                    print(f" Fragment: {name} already added.")
                except sqlite3.Error as e:
                    print(f"Error with adding fragment: {e}")
        cursor.close()
        conn.close()
        
    def _populate_intital_data(self):
        self._add_fragment_details("Seaglide", 2, "Safe Shallows, Kelp Forest", "0-100m", "Stalkers in the Kelp Forest", "None, but a Rebreather is helpful for longer dives")
        self._add_fragment_details("Mobile Vehicle Bay", 3, "Kelp Forest, Safe Shallows wrecks", "0-100m", "Stalkers in the Kelp Forest", "None")
        self._add_fragment_details("Seamoth", 3, "Grassy Plateaus, Aurora wreckage", "50-150m", "Stalkers and Sandsharks in the Grassy Plateaus, and Reapers around the Aurora", "None for fragments in the Grassy Plateaus, but a Propulsion Cannon is required for debris in the Aurora")
        self._add_fragment_details("Laser Cutter", 3, "Grassy Plateaus, wrecks in various biomes", "50-200m", "Sandsharks and Stalkers", "None to find the fragments, but it's needed to open sealed doors in many wrecks")
        self._add_fragment_details("Modification Station", 3, "Sparse Reef, Mushroom Forest, Jellyshroom Cave, Crag Field", "100-300m", "Bonesharks in the Mushroom Forest, Crabsnakes in the Jellyshroom Caves", "Seamoth with a depth module is highly recommended")
        self._add_fragment_details("Moonpool", 2, "Degasi Seabases, Mushroom Forest, Grand Reef", "200-500m", "Bonesharks, Warpers, and potentially Ghost Leviathans depending on the exact location", "Seamoth with a depth module (MK1 and above)")
        self._add_fragment_details("Power Cell Charger", 2, "Sparse Reef, wrecks, Degasi Seabases", "100-300m", "Bonesharks in the Sparse Reef", "Seamoth with a depth module is helpful")
        self._add_fragment_details("Nuclear Reactor", 4, "Mountains, Grand Reef Degasi Seabase", "400-800m", "Reaper Leviathans and Bonesharks in the Mountains, Warpers and Ghost Leviathans in the Grand Reef", "PRAWN Suit with a drill arm and depth module is essential")
        self._add_fragment_details("Cyclops Bridge", 3, "Mushroom Forest, Crash Zone, Sea Treader's Path", "150-400m", "Bonesharks and Crab Squids in the Mushroom Forest, Reaper Leviathans in the Crash Zone, and Sea Treader Leviathans on their path", "Seamoth with a depth module")
        self._add_fragment_details("Cyclops Hull", 3, "Mushroom Forest, Sea Treader's Path", "150-400m", "Bonesharks and Crab Squids in the Mushroom Forest, Sea Treader Leviathans on their path", "Seamoth with a depth module")
        self._add_fragment_details("Cyclops Engine", 3, "Crag Field, Mountains, Crash Zone, Aurora wreckage", "200-600m", "Bonesharks in the Crag Field, Reaper Leviathans in the Mountains and Crash Zone", "Seamoth with a depth module (MK1 and above). To access the Aurora, a Laser Cutter, Propulsion Cannon, and a Radiation Suit are also needed")
        self._add_fragment_details("PRAWN Suit", 4, "PRAWN Suit Bay in the Aurora wreckage", "0m (inside the Aurora)", "Radiation from the Aurora (requires a Radiation Suit) and a hungry Reaper Leviathan patrolling the area", "Radiation Suit, Laser Cutter, Propulsion Cannon, and a Seaglide to get around the wreckage")
        self._add_fragment_details("PRAWN Suit Drill Arm", 2, "Grand Reef, Blood Kelp Trench, Dunes, Mountains wrecks", "400m+", "Ghost Leviathans, Warpers, and Reaper Leviathans", "PRAWN Suit with a depth module")
        self._add_fragment_details("PRAWN Suit Grappling Arm", 2, "Wrecks in the Underwater Islands, Grand Reef, Blood Kelp Trench, Dunes, Mountains", "400m+", "Bonesharks, Ghost Leviathans, Warpers, and Reaper Leviathans", "PRAWN Suit with a depth module")
        self._add_fragment_details("Bioreactor", 2, "Grassy Plateaus", "50-150m", "Sandsharks, Stalkers", "None")
        self._add_fragment_details("Stasis Rifle", 2, "Large wrecks in various biomes", "100m+", "Varies by wreck location", "Laser Cutter and Seamoth depth module are helpful")
        self._add_fragment_details("Propulsion Cannon", 2, "Underwater Islands wreck, Aurora, Crash Zone", "200m+", "Bonesharks in Underwater Islands, Reaper Leviathans in Crash Zone", "Seamoth with depth module (MK1 and above)")
        self._add_fragment_details("Power Transmitter", 1, "Mushroom Forest", "150-250m", "Bonesharks, Crab Squids", "Seamoth with depth module")
        self._add_fragment_details("Scanner Room", 2, "Grassy Plateaus, Sea Treader's Path, Crag Field", "50-300m", "Sandsharks, Bonesharks, Sea Treader Leviathans", "Seamoth with depth module is helpful")
        self._add_fragment_details("Vehicle Upgrade Console", 2, "Grassy Plateaus wrecks, Grand Reef Degasi Seabase", "50-500m", "Sandsharks, Warpers, Ghost Leviathans", "Seamoth with depth module")
        self._add_fragment_details("Stillsuit", 2, "Wrecks in various biomes", "50m+", "Varies by wreck location", "None")
        self._add_fragment_details("Reinforced Dive Suit", 2, "Degasi Seabase in the Jellyshroom Cave", "200-300m", "Crabsnakes", "Seamoth with depth module")
        self._add_fragment_details("Alien Containment", 2, "Degasi Seabase in the Jellyshroom Cave", "200-300m", "Crabsnakes", "Seamoth with depth module")
        self._add_fragment_details("Water Filtration Machine", 2, "Wrecks in various biomes", "50m+", "Varies by wreck location", "None")
        self._add_fragment_details("Prawn Suit Propulsion Arm", 2, "Wrecks", "50m+", "Varies by wreck location", "None, but a Laser Cutter may be needed to access wrecks")
        self._add_fragment_details("Prawn Suit Torpedo Arm", 2, "Wrecks", "50m+", "Varies by wreck location", "None, but a Laser Cutter may be needed to access wrecks")
        self._add_fragment_details("Thermal Plant", 2, "Wrecks", "50m+", "Varies by wreck location", "None")
        self._add_fragment_details("Battery Charger", 2, "Wrecks in the Grassy Plateaus, Safe Shallows", "50-100m", "Sandsharks, Stalkers", "None")
        self._add_fragment_details("Solar Panel", 2, "Grassy Plateaus, Safe Shallows", "50-100m", "Sandsharks, Stalkers", "None")
        self._add_fragment_details("Spotlight", 2, "Wrecks in the Kelp Forest", "100-150m", "Stalkers", "None")
        self._add_fragment_details("Multipurpose Room", 2, "Wrecks in various biomes", "50m+", "Varies by wreck location", "None, but a Laser Cutter may be needed")
        self._add_fragment_details("Light Stick", 1, "Wrecks, Kelp Forest", "0-150m", "Stalkers", "None")
        self._add_fragment_details("Grav-trap", 1, "Wrecks", "50m+", "Varies by wreck location", "None")
        self._add_fragment_details("Repulsion Cannon", 2, "Wrecks, Aurora", "50-200m", "Sandsharks, Stalkers", "Propulsion Cannon needed for Aurora fragments")

    def check_fragment_table(self):
        #Connect to Database
        with self._connect() as conn:
            if not conn:
                print("Could not connect to database.")
                return

        #Check is the table exists
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='fragment_details'")
        if cursor.fetchone() is None: 
            self._create_fragment_table()
        
        cursor.execute("SELECT COUNT(*) FROM fragment_details")
        result = cursor.fetchone()
        if result and result[0] == 0:
            self._populate_intital_data()
            
        cursor.close()
        conn.close()
        
    def _check_connection(self):
        with self._connect() as conn:
            if not conn:
                print("Could not connect to database.")
                return
        return conn
        
    def get_fragment_by_name(self, name):
       #Check Connection
       conn = self._check_connection()
       
       #Assemble Query
       cursor = conn.cursor()
       sql_query = "SELECT * FROM fragment_details WHERE name LIKE ?"
       cursor.execute(sql_query, (f"%{name}%", ))
       
       tuple_all_records = cursor.fetchall()
       if tuple_all_records:
            print(f"Retrieving information for fragment with name: {name}...")
            print("--------------------------------------------------")
            for tuple_db_record in tuple_all_records:
                fragment.set_fragmentID(tuple_db_record[0])
                fragment.set_name(tuple_db_record[1])
                fragment.set_total_fragments_needed(tuple_db_record[2])
                fragment.set_locations(tuple_db_record[3])
                fragment.set_depth_level(tuple_db_record[4])
                fragment.set_dangers(tuple_db_record[5])
                fragment.set_needed_tools(tuple_db_record[6])
                
                #Display result
                fragment.get_all_details()
                print("-----------------------------------------------------------------")
                time.sleep(2)