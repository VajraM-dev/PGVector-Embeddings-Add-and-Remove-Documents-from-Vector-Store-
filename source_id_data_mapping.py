import sqlite3
import json
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(".env.dev"))

DB_NAME = os.environ.get("SQLITE_DB_NAME")
# Database initialization function
def initialize_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS source_id_mappings (
            source TEXT PRIMARY KEY,
            ids TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# Function to insert or update a source with associated IDs
def insert_source_ids(source: str, associated_ids: list):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO source_id_mappings (source, ids) 
        VALUES (?, ?) 
        ON CONFLICT(source) 
        DO UPDATE SET ids=excluded.ids
    """, (source, json.dumps(associated_ids)))
    
    conn.commit()
    conn.close()

# Function to delete IDs based on the source
def delete_source(source: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM source_id_mappings WHERE source = ?", (source,))
    
    conn.commit()
    conn.close()

# Function to retrieve IDs based on the source
def get_ids_by_source(source: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT ids FROM source_id_mappings WHERE source = ?", (source,))
    result = cursor.fetchone()
    
    conn.close()
    
    return json.loads(result[0]) if result else None

# Initialize the database
initialize_database()
