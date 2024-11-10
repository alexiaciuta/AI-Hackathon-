from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random secret key

# Initilizes/Creates the database if not already there

# Configure the SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
database_file = 'sqlite:///' + os.path.join(basedir, 'app.db')

app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Optional: specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    points = db.Column(db.Integer, default=0)
    age = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    interests = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'

    def __repr__(self):
        return f'<User {self.name}>'

# Creates the signup function for the page

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
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
            points = 50,
            location=location,
            email=email,
            interests=interests_str,
        )

         # Set the user's password
        new_user.set_password(password)

        # Add to database session and commit
        db.session.add(new_user)
        db.session.commit()

        # Log the user in
        login_user(new_user)

        return redirect(url_for('home'))

    interests_options = ['Football', 'Sailing', 'Rugby', 'Tennis', 'Pilates', 'Swimming', 'Hiking', 'Sports', 'Cycling', 'Running', 'Nature', 'Gardening', 'Crafts', 
                         'Reading', 'Cooking', 'Video Game', 'Board Game', 'Chess', 'Card Game', 'Music', 'Dance', 'Art', 'Theatre & film', 
                         'Museums', 'Travelling']
    return render_template('signup.html', interests_options=interests_options)

# Creates a voucher class for rewards
class Voucher(db.Model):
    __tablename__ = 'vouchers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    voucher_type = db.Column(db.String(50), nullable=False)
    redeemed_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('vouchers', lazy=True))

    def __repr__(self):
        return f'<Voucher {self.voucher_type} redeemed by User {self.user_id}>'

# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Where to redirect for @login_required

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Creates the login function for the page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        password = request.form.get('password')

        # Look up the user in the database
        user = User.query.filter_by(name=name).first()

        # Check if user exists and password is correct
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Creates the logout function for the page

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Creates a page to view all users in the database

@app.route('/users')
@login_required
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

# Creates the home page

@app.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user)

# Opens the appropiate start page

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
    
# Creates the matching page
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

# Creates the rewards page
@app.route('/rewards', methods=['GET', 'POST'])
@login_required
def rewards():
    # Available rewards
    reward_options = [
        {'name': '£10 Book Voucher', 'points': 100},
        {'name': 'Free Coffee Voucher', 'points': 50},
        {'name': 'Free Meal Voucher', 'points': 200},
    ]

    if request.method == 'POST':
        selected_reward = request.form.get('reward')
        
        # Find the selected reward
        reward = next((item for item in reward_options if item['name'] == selected_reward), None)
        if reward:
            if current_user.points >= reward['points']:
                # Deduct points
                current_user.points -= reward['points']

                # Create a new voucher
                new_voucher = Voucher(
                    user_id=current_user.id,
                    voucher_type=reward['name']
                )
                db.session.add(new_voucher)
                db.session.commit()

                message = f"You have successfully redeemed a {reward['name']}!"
            else:
                message = "You do not have enough points to redeem this reward."
        else:
            message = "Invalid reward selection."

        return render_template('rewards.html', user=current_user, reward_options=reward_options, message=message)

    return render_template('rewards.html', user=current_user, reward_options=reward_options)

# Creates the events page
@app.route('/events')
@login_required
def events():
    return "<h1>Events Page - Coming Soon</h1>"

if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080)
