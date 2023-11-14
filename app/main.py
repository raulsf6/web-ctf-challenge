from flask import Flask, render_template, request
import base64
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/admin")
def admin():
    login_cookie = request.cookies.get('login_cookie')

    if (login_cookie is not None):
        decoded_cookie = base64.b64decode(login_cookie)
        name, role = decoded_cookie.split(";")
        is_admin = role == "admin"
    else:
        is_admin = False

    return render_template("admin.html", is_admin = is_admin)

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)