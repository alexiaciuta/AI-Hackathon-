import database
import sqlite3
from typing import List, Set, Tuple, Optional
import random

# Initialize the database
initialize_database('main.db')

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
    add_person(name, person_interests, 'main.db')