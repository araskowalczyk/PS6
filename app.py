from flask import Flask, render_template, request, redirect, url_for, session
from auth import register_user, login_user
from leave import submit_leave_request
from database import init_db

app = Flask(__name__)
app.secret_key = 'tajny_klucz'

# Inicjalizacja bazy danych na starcie
init_db()

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', username=session['user'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = login_user(username, password)
        if user:
            session['user'] = user.username
            session['user_id'] = user.user_id
            return redirect(url_for('index'))
        return render_template('login.html', error='Błędne dane logowania')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/leave-request', methods=['GET', 'POST'])
def leave_request():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        reason = request.form['reason']
        success = submit_leave_request(session['user_id'], start_date, end_date, reason)
        return render_template('leave_request.html', success=success)
    return render_template('leave_request.html')

@app.route('/my-requests')
def my_requests():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT start_date, end_date, reason, status FROM leave_requests WHERE user_id = ?", (session['user_id'],))
    requests = c.fetchall()
    conn.close()

    return render_template('my_requests.html', requests=requests)

if __name__ == '__main__':
    app.run(debug=True)



