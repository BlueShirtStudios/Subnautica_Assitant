import sqlite3
import time
import os
import json
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
    
    """
    Table Setup and Creation from here
    """
    def __init__(self, DB_Name : str):
        self.db_name = DB_Name
        
    def _connect(self):
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except sqlite3.Error as e:
            print(f"Could not connect to database: {e}")
            
    def _create_table_fragment(self):
        with self._connect() as conn:
            if conn:
                cursor = conn.cursor()
                cursor.execute('''
                        CREATE TABLE IF NOT EXISTS fragments (
                        fragment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        total_fragments_needed INT,
                        min_depth INTEGER,
                        max_depth INTEGER
                    )
                ''')
                conn.commit()
                print("Table fragment details was created successfully.")
            else:
                print("Could not create fragment_details the Table.")
        cursor.close()
        conn.close()
        
    def delete_tables(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS fragment_details")

        conn.commit()
        conn.close()
        print("Table Deleted.")
                
    def _add_fragment_details(self, name : str, total_fragment : int, min_depth : int, max_depth : int):
        with self._connect() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('''
                                   INSERT INTO fragments (name, total_fragments_needed, min_depth, max_depth)
                                   VALUES (?, ?, ?, ?)
                                   ''', (name, total_fragment, min_depth, max_depth))
                    conn.commit()
                    print(f"Fragment: {name} was succesfully added")
                except sqlite3.IntegrityError:
                    print(f" Fragment: {name} already added.")
                except sqlite3.Error as e:
                    print(f"Error with adding fragment: {e}")
        cursor.close()
        conn.close()
        
    def _create_table_equipment(self):
        with self._connect() as conn:
            if conn:
                cursor = conn.cursor()
                cursor.execute('''
                        CREATE TABLE IF NOT EXISTS equipment (
                        equipement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL
                    )
                ''')
                conn.commit()
                print("Table 'equipment' was created successfully.")
            else:
                print("Could not create the Table.")
        cursor.close()
        conn.close()    
        
    def _add_equipment(self, name : str):
        with self._connect() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('''
                                   INSERT INTO equipment (name)
                                   VALUES (?)
                                   ''', (name))
                    conn.commit()
                    print(f"Equipment: {name} was succesfully added")
                except sqlite3.IntegrityError:
                    print(f"Equipment : {name} already added.")
                except sqlite3.Error as e:
                    print(f"Error with adding fragment: {e}")
        cursor.close()
        conn.close()

    def _create_table_fragment_dangers(self):
        with self._connect() as conn:
            if conn:
                cursor = conn.cursor()
                cursor.execute('''
                            CREATE TABLE IF NOT EXISTS fragment_dangers (
                                fragment_id INTEGER NOT NULL,
                                creature_id INTEGER NOT NULL,
                                PRIMARY KEY (fragment_id, creature_id),
                                FOREIGN KEY (fragment_id) REFERENCES fragments(fragment_id) ON DELETE CASCADE,
                                FOREIGN KEY (creature_id) REFERENCES creatures(creature_id) ON DELETE CASCADE
                            )
                ''')
                conn.commit()
                print("Table 'fragment_dangers' was created successfully.")
            else:
                print("Could not create the table 'fragment_dangers'.")
        cursor.close()
        conn.close()    
        
    def _add_fragment_dangers(self, fragament_id : int, creature_id):
        with self._connect() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('''
                                   INSERT INTO fragment_dangers (fragment_id, creature_id)
                                   VALUES (?, ?)
                                   ''', (fragament_id, creature_id))
                    conn.commit()
                    print(f"Combination: {fragament_id} and {creature_id} was succesfully added")
                except sqlite3.IntegrityError:
                    print(f"Combination: {fragament_id} and {creature_id}already added.")
                except sqlite3.Error as e:
                    print(f"Error with adding combination: {e}")
        cursor.close()
        conn.close()

    def _create_table_fragment_biomes(self):
        with self._connect() as conn:
            if conn:
                cursor = conn.cursor()
                cursor.execute('''
                        CREATE TABLE IF NOT EXISTS fragment_biomes (
                            fragment_id INTEGER NOT NULL,
                            biome_id INTEGER NOT NULL,
                            PRIMARY KEY (fragment_id, biome_id),
                            FOREIGN KEY (fragment_id) REFERENCES fragments(fragment_id) ON DELETE CASCADE,
                            FOREIGN KEY (biome_id) REFERENCES biomes(biome_id) ON DELETE CASCADE
                    )
                ''')
                conn.commit()
                print("Table 'fragment_biomes' was created successfully.")
            else:
                print("Could not create the table 'fragment_biomes'.")
        cursor.close()
        conn.close()    
        
    def _add_fragment_biomes(self, frgament_id : int, biome_id):
        with self._connect() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('''
                                   INSERT INTO fragment_biomes (fragment_id, biome_id)
                                   VALUES (?, ?)
                                   ''', (frgament_id, biome_id))
                    conn.commit()
                    print(f"Combination: {frgament_id} and {biome_id} was succesfully added")
                except sqlite3.IntegrityError:
                    print(f"Combination: {frgament_id} and {biome_id}already added.")
                except sqlite3.Error as e:
                    print(f"Error with adding combination: {e}")
        cursor.close()
        conn.close()
        
    def _create_table_fragment_equipment(self):
        with self._connect() as conn:
            if conn:
                cursor = conn.cursor()
                cursor.execute('''
                        CREATE TABLE IF NOT EXISTS fragment_equipment (
                            fragment_id INTEGER NOT NULL,
                            equipment_id INTEGER NOT NULL,
                            PRIMARY KEY (fragment_id, equipment_id),
                            FOREIGN KEY (fragment_id) REFERENCES fragments(fragment_id) ON DELETE CASCADE,
                            FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id) ON DELETE CASCADE
                    )
                ''')
                conn.commit()
                print("Table 'fragment_biomes' was created successfully.")
            else:
                print("Could not create the table 'fragment_biomes'.")
        cursor.close()
        conn.close()    
        
    def _add_fragment_biomes(self, frgament_id : int, equipment_id : int):
        with self._connect() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('''
                                   INSERT INTO fragment_biomes (fragment_id, equipement_id)
                                   VALUES (?, ?)
                                   ''', (frgament_id, equipment_id))
                    conn.commit()
                    print(f"Combination: {frgament_id} and {equipment_id} was succesfully added")
                except sqlite3.IntegrityError:
                    print(f"Combination: {frgament_id} and {equipment_id}already added.")
                except sqlite3.Error as e:
                    print(f"Error with adding combination: {e}")
        cursor.close()
        conn.close()
        
    def _populate_initial_data(self):
        print("Opening fragment_data.json...")
        fragment_file_path = os.path.join("src", "initial_data", "fragment_details", "fragments_data.json")
        with open(fragment_file_path, "r", encoding="utf-8") as file:
            #Needed details to fragment database
            fragment_list = json.load(file)
            for category in fragment_list.values():
                
                for entry in category:
                    name = entry["name"]
                    print(name)
            
        
    def check_tables(self):
        with self._connect() as conn:
            if not conn:
                print("There was a connection issue")
                return

            cursor = conn.cursor()
            
            #Check if all tables exists
            list_tbl_name = ["fragments", "equipment", "fragment_dangers", "fragment_biomes", "fragment_equipment"   ]
            tables_created = 0
            for tbl in list_tbl_name:
                sql_query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
                cursor.execute(sql_query, (tbl, ))
                if cursor.fetchone() is None:
                    if tbl == "fragments":
                        self._create_table_fragment()
                        tables_created += 1
                    elif tbl == "equipment":
                        self._create_table_equipment()
                        tables_created += 1
                    elif tbl == "fragment_biomes":
                        self._create_table_fragment_dangers()
                        tables_created += 1
                    elif tbl == "fragment_location":
                        self._create_table_fragment_biomes()
                        tables_created += 1
                    elif tbl == "fragment_equipment":
                        self._create_table_fragment_equipment()
                        tables_created += 1
                        
            #Determine if population is needed
            tables_created = 5
            if tables_created == 5:
                self._populate_initial_data()