import sqlite3
from typing import List, Set, Tuple, Optional
import random

def initialize_database(db_name: str = 'people_interests.db'):
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

def add_person(name: str, interests: Set[str], db_name: str = 'people_interests.db'):
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

def remove_person(name: str, db_name: str = 'people_interests.db'):
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

def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """
    Calculate the Jaccard Similarity between two sets.
    """
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    if not union:
        return 0.0
    return len(intersection) / len(union)

def get_all_people(db_name: str = 'people_interests.db') -> List[Tuple[str, Set[str]]]:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT id, name FROM people')
    people = cursor.fetchall()

    people_list = []

    for person_id, name in people:
        cursor.execute('''
            SELECT interest
            FROM interests
            JOIN people_interests ON interests.id = people_interests.interest_id
            WHERE people_interests.person_id = ?
        ''', (person_id,))
        interests = set([row[0] for row in cursor.fetchall()])
        people_list.append((name, interests))

    conn.close()
    return people_list

def find_closest_match(target_interests: Set[str], db_name: str = 'people_interests.db') -> Optional[Tuple[str, float]]:
    people = get_all_people(db_name)
    max_similarity = 0.0
    closest_person = None

    for name, interests in people:
        similarity = jaccard_similarity(target_interests, interests)
        if similarity > max_similarity:
            max_similarity = similarity
            closest_person = name

    if closest_person:
        return closest_person, max_similarity
    else:
        return None

# Initialize the database
initialize_database()

# List of interests
interests_list = [
    'Football',
    'Sailing',
    'Rugby',
    'Tennis',
    'Pilates',
    'Swimming',
    'Hiking',
    'Cycling',
    'Running',
    'Nature',
    'Gardening',
    'Crafts',
    'Reading',
    'Cooking/Baking',
    'Video Games',
    'Board Games',
    'Chess',
    'Card Games',
    'Music',
    'Dance',
    'Art',
    'Theatre & Film',
    'Visiting Museums',
    'Travelling'
]

# Sample database of people
names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry', 'Irene', 'Jack']

# Add people to the database
for name in names:
    num_interests = random.randint(3, 6)  # Each person has 3 to 6 interests
    person_interests = set(random.sample(interests_list, num_interests))
    add_person(name, person_interests)

# Add a new person
new_person_name = 'Sophia'
new_person_interests = {'Reading', 'Gardening', 'Travelling', 'Cooking/Baking', 'Art'}

#add_person(new_person_name, new_person_interests)

# Remove a person (optional)
remove_person('Sophia')

# Find the closest match for Sophia
target_person_interests = new_person_interests

result = find_closest_match(target_person_interests)

if result:
    closest_person, similarity_score = result
    print(f"The closest match is {closest_person} with a similarity score of {similarity_score:.2f}")
else:
    print("No match found.")

# Display all people and their interests
people = get_all_people()
print("\nPeople in the database and their interests:\n")
for name, interests in people:
    print(f"{name}: {interests}\n")
