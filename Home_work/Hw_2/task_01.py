from flask import Flask, request, render_template, session, redirect, url_for, make_response


app = Flask(__name__)
app.secret_key = '5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('welcome.html', username=username)
    else:
        return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form.get('username') or 'NoName'
        return redirect(url_for('index'))
    return render_template('login_pr.html')


@app.route('/logout/')
def logout():
    session.pop('username', None)
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('username', '', max_age=0)
    return resp


if __name__ == '__main__':
    app.run(debug=True)
