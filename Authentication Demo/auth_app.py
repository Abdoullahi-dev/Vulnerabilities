from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'


accounts = {
    "admin": {
        "password": "admin123",
        "security_questions": {
            "What is your pet's name?": "fluffy",
            "What is your mother's maiden name?": "smith",
            "What is your favourite color": "yellow"
        }
    },
    "John": {
        "password": "bigJohn",
        "security_questions": {
            "What is your pet's name?": "Stinky",
            "What is your mother's maiden name?": "johnson",
            "What is your favourite color": "blue"
        }
    },
    "user2": {
        "password": "password2",
        "security_questions": {
            "What is your pet's name?": "cat",
            "What is your mother's maiden name?": "williams",
            "What is your favourite color": "yellow"
        }
    }
}

@app.route('/')
def login():
    return render_template('authLogin.html', invalid=False)

@app.route('/', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    if username in accounts and accounts[username]['password'] == password:
        return redirect(url_for('home', username=username))
    else:
        return render_template('authLogin.html', invalid=True)

@app.route('/home/<username>')
def home(username):
    return render_template('authHome.html', username=username)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    password = None  
    if request.method == 'POST':
        username = request.form['username']
        question = request.form['question']
        answer = request.form['answer']

        if username in accounts:
            user = accounts[username]
            #User validation
            if question in user["security_questions"] and user["security_questions"][question].lower() == answer.lower():
                password = user['password']  
            else:
                flash("Incorrect answer or question. Try again.", 'danger')
        else:
            flash("User not found.", 'danger')

    # Send the user data to the forgot.html page
    questions = [(q, q) for q in next(iter(accounts.values()))['security_questions'].keys()]  # List of questions
    return render_template('authForgot.html', questions=questions, password=password)

if __name__ == '__main__':
    app.run(debug=True)
