from flask import Flask, redirect, url_for, render_template, session, request, flash
from datetime import timedelta
from database.User import User

app = Flask(__name__)

app.secret_key = 'mykey'
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['nm']
        password = request.form['pass']

        if User.find_user(user, password):
            session['user'] = user
            session['password'] = password
            return redirect(url_for('home'))
        else:
            flash('Không tìm thấy tài khoản hoặc mật khẩu trùng')
            return render_template('login.html')
    else:
        if 'user' in session and 'password' in session:
            return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/home')
def home():
    if 'user' in session and 'password' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('password', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9999', debug=True)
