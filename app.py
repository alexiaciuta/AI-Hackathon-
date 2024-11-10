from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        location = request.form.get('location')
        interests = request.form.getlist('interests')
        connection_type = request.form.get('connection_type')
        # For now, we'll just display a thank you message with the user's name
        return f"Thank you for signing up, {name}!"

    interests_options = ['Football', 'Sailing', 'Rugby', 'Tennis', 'Pilates', 'Swimming', 'Hiking', 'Sports', 'Cycling', 'Running', 'Nature', 'Gardening', 'Crafts', 
                         'Reading', 'Cooking/Baking', 'Video Games', 'Board games', 'Chess', 'Card Games', 'Music', 'Dance', 'Art', 'Theatre & film', 
                         'Visiting museums', 'Travelling']
    return render_template('signup.html', interests_options=interests_options)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)