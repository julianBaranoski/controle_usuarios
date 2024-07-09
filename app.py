from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load users and permissions from JSON files
with open('users.json') as f:
    users = json.load(f)

with open('permissions.json') as f:
    permissions = json.load(f)

def get_user(username):
    for user in users:
        if user['username'] == username:
            return user
    return None

@app.route('/')
def index():
    if 'username' in session:
        user = get_user(session['username'])
        user_permissions = permissions[user['role']]
        return render_template('index.html', user=user, permissions=user_permissions)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/menu')
def menu():
    if 'username' in session:
        user = get_user(session['username'])
        if 'view_menu' in permissions[user['role']]:
            return render_template('menu.html')
        return 'Access Denied'
    return redirect(url_for('login'))

@app.route('/report')
def report():
    if 'username' in session:
        user = get_user(session['username'])
        if 'view_report' in permissions[user['role']]:
            return render_template('report.html')
        return 'Access Denied'
    return redirect(url_for('login'))

@app.route('/manage_users')
def manage_users():
    if 'username' in session:
        user = get_user(session['username'])
        if 'manage_users' in permissions[user['role']]:
            return render_template('manage_users.html', users=users)
        return 'Access Denied'
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
