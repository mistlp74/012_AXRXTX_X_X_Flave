from flask import Flask, jsonify, render_template, request, redirect, url_for
from models import db, User
from data_manager import user_verify_password, user_create, user_existence

app = Flask(__name__)



@app.route("/", methods=['POST', 'GET'])


def starter_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not user_existence(username):
            print("~ ~ ~ User does not exist ~ ~ ~")
            return render_template("starter_page.html", error="User does not exist")

        if (user_verify_password(username, password)):
            print("~ ~ ~ Login successful ~ ~ ~")
            return redirect("/main")
        
        return render_template("starter_page.html", error="Invalid username or password")
        
    return render_template("starter_page.html")




@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if user_existence(username):
            print("~ ~ ~ User already exists ~ ~ ~")
            return render_template("register.html", error="User already exists")

        user_create(username, password)
        print("~ ~ ~ User created successfully ~ ~ ~")
        return redirect(url_for('starter_page'))

    return render_template("register.html")



@app.route("/main")
def main():
    return render_template("main.html")



@app.route("/users")
def show_users():
    users = User.query.all()
    return "<br>".join([f"ID: {u.id} | Public ID: {u.public_id} |  Username: {u.username} | Password: {u.password} | Salt: {u.salt}" for u in users])



with app.test_request_context():
    print(url_for('starter_page'))
    print(url_for('register'))
    print(url_for('main'))





# Database configuration

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)

with app.app_context():
    db.create_all()





if __name__ == "__main__":
    app.run(debug=True)
