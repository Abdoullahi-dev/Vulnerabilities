from flask import Flask, request, render_template, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

accounts = [
    {"id": 0, "username": "admin", "password": "admin", "note": "I am a professional kazoo player."},
    {"id": 1, "username": "user1", "password": "pass1", "note": "I sleep with a night light."},
    {"id": 2, "username": "user2", "password": "pass2", "note": "I hoard electronics."},
    {"id": 3, "username": "user3", "password": "pass3", "note": "I hate milk."},
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for account in accounts:
            if account['username'] == username and account['password'] == password:
                session['user_id'] = account['id']  # Store user ID in session
                flash('Login successful!', 'success')
                return redirect(url_for('notes', user_id=account['id']))

        flash('Invalid credentials', 'danger')

    return render_template('login.html')

@app.route('/user/<int:user_id>')
def notes(user_id):
    if 'user_id' not in session:
        flash('You need to log in first!', 'warning')
        return redirect(url_for('login'))

    for user in accounts:
        if user['id'] == user_id:
            return render_template('notes.html', user=user)

    flash('User not found', 'danger')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logout successful!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
