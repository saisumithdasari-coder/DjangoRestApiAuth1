from flask import Flask, render_template, request, session

from utils import register_request, login_request, revoke_request, hello_world_request, refresh_request

app = Flask(__name__)

app.url_map.strict_slashes = False


@app.route("/hello_world/")
def hello_world():
    response = hello_world_request(session.get('jwt_header', ''))
    return render_template("index.html", msg=response)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username'].lower()
        password = request.form['password']
        response = register_request(username, password)
        if response.get('access_token', None) is not None:
            session['logged_in'] = True
            session["refresh_token"] = response['refresh_token']
            session["jwt_header"] = response['access_token']
            return render_template("index.html", msg="You have been registered...")
        return render_template("index.html", msg="Register failed...")
    return render_template("login.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username'].lower()
        password = request.form['password']
        response = login_request(username, password)
        if response.get('access_token', None) is not None:
            session['logged_in'] = True
            session["refresh_token"] = response['refresh_token']
            session["jwt_header"] = response['access_token']
        return render_template("index.html", msg=f"You have been logged in...\n{response}")
    return render_template("login.html")


@app.route("/token/")
def token():
    return render_template("index.html", msg={'message': session.get("jwt_header", 'no token stored')})


@app.route("/logout/")
def logout():
    response = revoke_request(session.get('jwt_header', ''))
    session.clear()
    return render_template("index.html", msg=response)


@app.route("/refresh/")
def refresh():
    response = refresh_request(session.get('refresh_token', ''))
    session["refresh_token"] = response['refresh_token']
    session["jwt_header"] = response['access_token']
    return render_template("index.html", msg=response)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True, host='0.0.0.0')

