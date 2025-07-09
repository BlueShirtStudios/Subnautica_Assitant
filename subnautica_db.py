import sqlite3

DB_NAME = "subnautica.db"

def connect():
    """Establish connection to database"""
    try:    
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Error with conecting to database: {e}")
        return None
    
def createCreatureTable():
    with connect() as conn:
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
            
def addCreature(name, category, biomes, behavior, danger_level, depth_range, pda_entry, image_url):
    with connect() as conn:
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                               INSERT INTO creatures (name, category, biomes, behavior, danger_level, depth_range, pda_entry, image_url)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                               ''', (name, category, biomes, danger_level, depth_range, pda_entry, image_url))
                conn.commit
                print("Succesfully Addad to databank.")
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                print(f"Error: Creature: {name} already exists.")
            except sqlite3.Error as e:
                print(f"Error with adding creature: {e}")
                
def get_allCreatures():
    with connect() as conn:
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM creatures")
            rows = cursor.fetchall
            if rows:
                for row in rows:
                    print(row)