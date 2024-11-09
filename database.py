import sqlite3
from typing import List, Set, Tuple, Optional
import random

def initialize_database(db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interest TEXT UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people_interests (
            person_id INTEGER,
            interest_id INTEGER,
            FOREIGN KEY(person_id) REFERENCES people(id),
            FOREIGN KEY(interest_id) REFERENCES interests(id),
            UNIQUE(person_id, interest_id)
        )
    ''')

    conn.commit()
    conn.close()

def add_person(name: str, interests: Set[str], db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Add person
    cursor.execute('INSERT OR IGNORE INTO people (name) VALUES (?)', (name,))
    conn.commit()

    # Get person's ID
    cursor.execute('SELECT id FROM people WHERE name = ?', (name,))
    person_id = cursor.fetchone()[0]

    for interest in interests:
        # Add interest
        cursor.execute('INSERT OR IGNORE INTO interests (interest) VALUES (?)', (interest,))
        conn.commit()

        # Get interest's ID
        cursor.execute('SELECT id FROM interests WHERE interest = ?', (interest,))
        interest_id = cursor.fetchone()[0]

        # Link person and interest
        cursor.execute('''
            INSERT OR IGNORE INTO people_interests (person_id, interest_id)
            VALUES (?, ?)
        ''', (person_id, interest_id))
        conn.commit()

    conn.close()

def remove_person(name: str, db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Get person's ID
    cursor.execute('SELECT id FROM people WHERE name = ?', (name,))
    result = cursor.fetchone()
    if result:
        person_id = result[0]

        # Delete from people_interests
        cursor.execute('DELETE FROM people_interests WHERE person_id = ?', (person_id,))
        conn.commit()

        # Delete from people
        cursor.execute('DELETE FROM people WHERE id = ?', (person_id,))
        conn.commit()

    conn.close()