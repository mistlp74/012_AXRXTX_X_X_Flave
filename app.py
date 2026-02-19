from flask import Flask, jsonify, render_template, request, redirect, url_for
from User_verify import user_login

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def starter_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if (user_login(username, password)):
            return redirect("/main")
        
        return render_template("starter_page.html", error="Invalid username or password")
        
    return render_template("starter_page.html")



@app.route("/Register")
def register():
    return render_template("register.html")


@app.route("/main")
def main():
    return render_template("main.html")


with app.test_request_context():
    print(url_for('starter_page'))
    print(url_for('register'))
    print(url_for('main'))



if __name__ == "__main__":
    app.run(debug=True)
