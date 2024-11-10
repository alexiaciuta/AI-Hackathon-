from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from typing import List, Set, Tuple, Optional
import sqlite3

app = Flask(__name__)

# Configure the SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
database_file = 'sqlite:///' + os.path.join(basedir, 'app.db')

app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'users'  # Optional: specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    location = db.Column(db.String(100))
    email = db.Column(db.String(100))
    interests = db.Column(db.String(200))

    def __repr__(self):
        return f'<User {self.name}>'

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        location = request.form.get('location')
        email = request.form.get('email')
        interests = request.form.getlist('interests')

        # Convert interests list to a comma-separated string
        interests_str = ', '.join(interests)

        # Create a new User instance
        new_user = User(
            name=name,
            age=age,
            location=location,
            email=email,
            interests=interests_str,
        )

        # Add to database session and commit
        db.session.add(new_user)
        db.session.commit()

        # Retrieve all users from the database
        all_users = User.query.all()

        # Render the users template with all user data
        return render_template('users.html', users=all_users)
    
    interests_options = ['Football', 'Sailing', 'Rugby', 'Tennis', 'Pilates', 'Swimming', 'Hiking', 'Sports', 'Cycling', 'Running', 'Nature', 'Gardening', 'Crafts', 
                         'Reading', 'Cooking', 'Video Game', 'Board Game', 'Chess', 'Card Game', 'Music', 'Dance', 'Art', 'Theatre & film', 
                         'Museums', 'Travelling']
    return render_template('signup.html', interests_options=interests_options)

@app.route('/find-a-local-friend')
def get_all_people(db_name: str) -> List[Tuple[str, Set[str]]]:

    all_users = User.query.all()
    print(type(all_users))
    people_list = []
    interests = set([user.interests.split(',') for user in all_users])
    print(interests)
    print(all_users)
    people_list.append((User.name, interests))

    return people_list

def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """
    Calculate the Jaccard Similarity between two sets.
    """
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    if not union:
        return 0.0
    return len(intersection) / len(union)

def find_closest_match(target_interests: Set[str], db_name: str) -> Optional[Tuple[str, float]]:
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
    
    
    
if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080)
