import sys
from flask import Flask, abort, make_response, redirect, render_template, render_template_string, request
import base64
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.get("/logout")
def logout():
    response = redirect("/login")
    response.set_cookie("login_cookie", "")
    return response

@app.get("/login")
def login():
    login_cookie = request.cookies.get('login_cookie')
    
    if (login_cookie is None):
        return render_template("login.html")
    
    try:
        name, role = decode_cookie(login_cookie)
    except:
        return render_template("login.html", logged_in = False)
    
    return render_template("login.html", logged_in = True, username = name, role = role)

@app.post("/login")
def post_login():
    username = request.form.get('username')
    if username is None: abort(400)
    password = request.form.get('password')
    if password is None: abort(400)

    login_cookie = base64.b64encode(bytes(f"{username};regular_user", 'utf-8')).decode('utf8')
    response = redirect("/login")
    response.set_cookie("login_cookie", login_cookie)
    
    return response

@app.get("/admin")
def admin():
    login_cookie = request.cookies.get('login_cookie')

    if (login_cookie is None):
        return render_template("admin.html", is_admin = False)
        
    try:
        name, role = decode_cookie(login_cookie)
    except:
        return render_template("admin.html", is_admin = False)
    
    is_admin = role == "admin"

    f = open(f'{sys.argv[0]}/../templates/admin.html')
    admin_template = f.read().replace('admin_name', name)

    return render_template_string(admin_template, is_admin = is_admin)

def decode_cookie(login_cookie):
    decoded_cookie = base64.b64decode(login_cookie).decode('utf8')
    name, role = decoded_cookie.split(";")
    return name, role 

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)