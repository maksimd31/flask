from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello')
def hello():
    name = request.cookies.get('name')
    return render_template('hello.html', name=name)


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    resp = make_response(redirect('/hello'))
    resp.set_cookie('name', name)
    return resp


@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('name')
    return resp


if __name__ == '__main__':
    app.run()
