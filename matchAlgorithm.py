import database
from typing import List, Set, Tuple, Optional
import random

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





# Add a new person
new_person_name = input("Name: ")
new_person_interests = input("Interests: ")


user = "Sophia"


#add_person(new_person_name, new_person_interests)

# Remove a person (optional)
#remove_person('Sophia')

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