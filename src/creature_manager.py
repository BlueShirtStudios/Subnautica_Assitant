import sqlite3
from typing import List, Optional
import time
import json
import os

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
    
    """
    Table creatures setup/add
    """
    def _create_tblcreatures(self):
        conn = self._connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS creatures (
                        creature_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT NOT NULL,
                        behavior TEXT NOT NULL,
                        min_depth INTEGER,
                        max_depth INTEGER,
                        pda_entry TEXT,
                        img_url TEXT
                    )
                        ''')
            conn.commit()
            print("Table 'creatures' successfully created. ")
        else:
            print("Table 'creatures could not be created.")
            
        cursor.close()
        conn.close()
    
    def _add_creature(self, name : str, category : str, behavior : str, min_depth : int, 
                      max_depth : int, pda_entry : str, img_url : str):  
        conn = self._connect()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                               INSERT INTO creatures (name, category, behavior, min_depth, max_depth, pda_entry, img_url)
                               VALUES (?, ?, ?, ?, ?, ?, ?)
                               ''', (name, category, behavior, min_depth, max_depth, pda_entry, img_url),)
                conn.commit()
            except sqlite3.IntegrityError:
                print(f"Error: Creature : {name} already added.")
            except sqlite3.Error as e:
                print(f"Erorr with adding creature: {e}")
        cursor.close()
        conn.close()
        
        
    """
    Table biomes Create and Add
    """
    def _create_tblbiomes(self):
        conn = self._connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS biomes (
                               biome_id INTEGER PRIMARY KEY AUTOINCREMENT,
                               name TEXT NOT NULL
                           )
                           ''')
            conn.commit()
            print("Table 'biomes' created successfully.")
        else:
            print("Could not create table 'biomes'.")
            
        cursor.close()
        conn.close()
    
    def _add_biome(self, name : str):  
        conn = self._connect()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                               INSERT INTO biomes (name)
                               VALUES (?)
                               ''', (name, ))
                conn.commit()
            except sqlite3.IntegrityError:
                print(f"Error: Biome : {name} already added.")
            except sqlite3.Error as e:
                print(f"Erorr with adding biome: {e}")
        cursor.close()
        conn.close()   
        
    """
    Table creature_biome create/add   
    """
    def _create_tblcreature_biome(self):
        conn = self._connect()
        if conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS creature_biomes (
                               creature_id INTEGER NOT NULL,
                               biome_id INTEGER NOT NULL,
                               PRIMARY KEY (creature_id, biome_id),
                               FOREIGN KEY (creature_id) REFERENCES creatures(creaure_id) ON DELETE CASCADE,
                               FOREIGN KEY (biome_id) REFERENCES biomes(biome_id) ON DELETE CASCADE
                           )
                           ''')
            conn.commit()
            print("Table 'creature_biomes' created successfully.")
        else:
            print("Could not create table 'creatuer_biomes'.")
            
        cursor.close()
        conn.close()
        
    def _add_creature_biome(self, creature_id : int, biome_id : int):
        conn = self._connect()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                               INSERT INTO creature_biomes (creature_id, biome_id)
                               VALUES (?, ?)
                               ''', (creature_id, biome_id))
                conn.commit()
            except sqlite3.IntegrityError:
                print(f"Error: Comination Key : {creature_id} and {biome_id} already added.")
            except sqlite3.Error as e:
                print(f"Erorr with adding combination key: {e}")
        cursor.close()
        conn.close() 
        
    def _get_creature_id(self, name : str):
        conn = self._connect()
        if conn:
            cursor = conn.cursor()
            query = "SELECT creature_id FROM creatures WHERE name = ?"
            cursor.execute(query, (name, ))
            creature_id = cursor.fetchone()
            cursor.close()
            conn.close()
            if creature_id:
                return creature_id[0]
            else:
                print("No creature_id to return")
        else:
            print('Could not connect to database.')
            return None
            
    def _get_biome_id(self, name : str):
        conn = self._connect()
        if conn:
            cursor = conn.cursor()
            query = "SELECT biome_id FROM biomes WHERE name = ?"
            cursor.execute(query, (name, ))
            biome_id = cursor.fetchone()
            cursor.close()
            conn.close()
            if biome_id:
                return biome_id[0]
            else:
                print("No biome_id to return")
        else:
            print('Could not connect to database.')
            return None
        
    def delete_tables(self): #ONLY USE WHEN CAUSING POPULATION ISSUES
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS creature_biomes")   
        cursor.execute("DROP TABLE IF EXISTS creatures")
        cursor.execute("DROP TABLE IF EXISTS biomes")
        conn.commit()
        conn.close()
        print("Table Deleted.")
        
        
    def _populate_intial_creature_data(self):
        #Open creature details json
        print("Opening creature_data.json...")
        creature_data_file = os.path.join("src",  "initial_data", "creature_data.json" )
        with open (creature_data_file, "r", encoding="utf-8") as creature_file:
            #Add each creature to the database
            creatures = json.load(creature_file)
            for creature_record in creatures:
                self._add_creature(creature_record['name'],
                                    creature_record['category'],
                                    creature_record['behavior'],
                                    creature_record['min_depth'],
                                    creature_record['max_depth'],
                                    creature_record['pda_entry'],
                                    creature_record['img_url'])
        print("Creatures added to database.")
        
        #Open biome details json
        print("Opening biome_data.json...")
        biome_data_file = os.path.join("src", "initial_data", "biome_data.json" )
        with open (biome_data_file, "r", encoding="utf-8") as biome_file: 
            #Add biomes to table
            biomes = json.load(biome_file) 
            for biome_record in biomes: 
                self._add_biome(biome_record['name'])
                
        print("Biomes added to database.")
        
        #Open creature_biomes details json
        creature_biome_data_file = os.path.join("src", "initial_data", "creature_biomes.json" )
        with open (creature_biome_data_file, "r", encoding="utf-8") as file:
            creature_biomes = json.load(file)
            
            #Loop for all records in file
            for creature_biomes_record in creature_biomes:
                creature_name = creature_biomes_record['creature_name']
                list_biomes = creature_biomes_record['biomes']
                
                print(f"Creature : {creature_name}")
                print(f"Biome list: {list_biomes}")
                
                #if creature name not empty
                if creature_name:
                    creature_id = self._get_creature_id(creature_name)
                    print("Attempting to Add......")
                    print(f"Creature: {creature_name} Creature ID: {creature_id}")
                    
                    #if list not empty
                    if list_biomes:
                        for biome in list_biomes:
                            biome_id = self._get_biome_id(biome)
                            
                            try:
                                print(f"Attempting to add: Biome: {biome} Biome ID: {biome_id}")
                                self._add_creature_biome(creature_id, biome_id)
        
                            except KeyError as e:
                                print(f"There was an issue: {e}")
                    print("SUCCESSFULL\n--------------------------------------------------------------------------")
                            
                time.sleep(2)
                    
    def check_db_creature_details(self):
        #Connect to DB
        with self._connect() as conn:
            if not conn:
                print("Could not connect to database.")
                return

        #Check if all tables exists and count its records
        cursor = conn.cursor()
        
        #Creature Table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='creatures'")
        if cursor.fetchone() is None:
            self._create_tblcreatures()
            
        #Count Records
        cursor.execute("SELECT COUNT(*) FROM creatures")
        creature_tot_record = cursor.fetchone()
            
        #Biome Table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='biomes'")
        if cursor.fetchone() is None:
            self._create_tblbiomes()
            
        #Count Records
        cursor.execute("SELECT COUNT(*) FROM biomes")
        biome_tot_record = cursor.fetchone()
            
        #Creature_biome table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='creature_biomes'")
        if cursor.fetchone() is None:
            self._create_tblcreature_biome()
            
        #Count Records
        cursor.execute("SELECT COUNT(*) FROM creature_biomes")
        creature_biome_tot_record = cursor.fetchone()
            
        #Check if population is needed
        if creature_tot_record[0] == 0 and biome_tot_record[0] == 0 and creature_biome_tot_record[0] == 0:
            self._populate_intial_creature_data()
    
        cursor.close()
        conn.close()
        
        return True
    
    def get_creature_by_name(self, creature_name : str):
        #Connect to DB
        conn = self._connect()
        
        #Setup Query
        cursor = conn.cursor()
        sql_query = "SELECT * FROM creatures WHERE name LIKE ?"
        cursor.execute(sql_query, (f"%{creature_name}%", ))   
        
        #Add the record to the creature object 
        tuple_all_records = cursor.fetchall()
        if tuple_all_records:
            #Intailize
            index_number = 0
            list_names = []
            
            #Loop to get all biomes of the creature
            print("Retreiving information on all creatures with similer name...")
            for tuple_db_record in tuple_all_records:
                #Assign Values to creature object
                creature.set_creature_id(tuple_db_record[0])
                creature.set_name(tuple_db_record[1])
                creature.set_category(tuple_db_record[2])
                creature.set_behavior(tuple_db_record[3])
                creature.set_min_depth(tuple_db_record[4])
                creature.set_max_depth(tuple_db_record[5])
                creature.set_pda_entry(tuple_db_record[6])
                creature.set_img_url(tuple_db_record[7])
                
                #Add creature to list 
                list_names.append(creature.get_name())
                possible_creature_name = list_names[index_number]
                index_number += 1
                
                #Re-intialize
                list_biome_id = []
                list_biomes = []
                
                #Get the creature id
                creature.set_creature_id(tuple_db_record[0])
                creature_id = creature.get_creature_id()
                
                #Get all biome IDs of that creature ID
                sql_query = "SELECT biome_id FROM creature_biomes WHERE creature_id = ?"
                cursor.execute(sql_query, (creature_id, ) )
                tuple_rows = cursor.fetchall()
                for row in tuple_rows:
                    list_biome_id.append(row[0])
                
                #Construct new query to get the biome names
                sql_query = "SELECT name FROM biomes WHERE biome_id = ?"
                for biome_id in list_biome_id:
                    cursor.execute(sql_query, (biome_id, ))
                    tuple_biome_name = cursor.fetchall()
                    list_biomes.append(tuple_biome_name[0])

                #Assign biomes to creature
                creature.set_biomes(list_biomes)
                
                #Display the results
                print("------------------------------------------------------------")
                creature.display_creature_info()   
                time.sleep(2)    
        else:
            print("No creature found with such name. Please make sure that the creature does exist.")
            
        if len(list_names) > 1:
                possible_name_string = ', '.join(list_names)
        elif len(list_names) == 1:
                possible_name_string = list_names[0]
        else:
            possible_name_string = ''
        print("")       
        print(f"Retrieved all informarion on : {possible_name_string}. Were these the results you were looking for?")
            
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
        sql_query = "SELECT biome_id FROM biomes WHERE name LIKE ?"
        cursor.execute(sql_query, (f"%{search_biome}%", ))    
        
        #Retreive the results
        tuple_all_records = cursor.fetchall()
        if tuple_all_records:
            index_main = 0
            print(f"Searching for creatures in {search_biome}...")
            print("------------------------------------------------------------")
            
            #Get which biome it is
            sql_query = "SELECT creature_id FROM creature_biomes WHERE biome_id = ?"
            for biome_id in tuple_all_records:
                cursor.execute(sql_query, (biome_id[0], ))
                
                #Get creatrures that live in that biome
                creature_ids = cursor.fetchall()
                for creature_id in creature_ids:
                    
                    creature.set_creature_id(creature_id[0])
                    
                    #Search for the creature details an return results
                    sql_query = "SELECT * FROM creatures WHERE creature_id = ?"
                    cursor.execute(sql_query, (creature.get_creature_id(), ) )
                    tuple_creature_record = cursor.fetchall()
                    
                    #Assign to Creature
                    creature.set_name(tuple_creature_record[0][1])
                    creature.set_category(tuple_creature_record[0][2])
                    creature.set_behavior(tuple_creature_record[0][3])
                    
                            
                    #Get Results
                    result = f"Name: {creature.get_name()}\nCategory: {creature.get_category()}\nBehavior: {creature.get_behavior()}"
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
                creature.set_creature_id(tuple_db_record[0])
                creature.set_name(tuple_db_record[1])
                creature.set_behavior(tuple_db_record[3])
                creature.set_min_depth(tuple_db_record[4])
                creature.set_max_depth(tuple_db_record[5])
                creature.set_pda_entry(tuple_db_record[6])
                
                #Re-intialize
                list_biome_id = []
                list_biomes = []
                list_clean_biomes = []
            
                creature_id = creature.get_creature_id()
                
                #Get all biome IDs of that creature ID
                sql_query = "SELECT biome_id FROM creature_biomes WHERE creature_id = ?"
                cursor.execute(sql_query, (creature_id, ) )
                tuple_rows = cursor.fetchall()
                for row in tuple_rows:
                    list_biome_id.append(row[0])
                
                #Construct new query to get the biome names
                sql_query = "SELECT name FROM biomes WHERE biome_id = ?"
                for biome_id in list_biome_id:
                    cursor.execute(sql_query, (biome_id, ))
                    tuple_biome_name = cursor.fetchall()
                    list_biomes.append(tuple_biome_name[0])

                #Assign biomes to creature
                for biomes in  list_biomes:
                    list_clean_biomes.append(biomes[0])
                creature.set_biomes(list_biomes)
                
                #Print Results
                result = f"Name: {creature.get_name()}\nBiomes: {creature.get_biomes()}\nDepth-Level: {creature.get_min_depth()}-{creature.get_max_depth()}m \nPDA Entry: {creature.get_pda_entry()}\n"
                print(result)
                print("------------------------------------------------------------")
                time.sleep(2)
                
        cursor.close()
        conn.close()