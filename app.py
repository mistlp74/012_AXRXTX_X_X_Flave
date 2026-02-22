from flask import Flask, jsonify, render_template, request, redirect, url_for, session, jsonify
from models import Contacts, Requests, db, User
from data_manager import add_contact_request, get_id_by_public_id, user_verify_password, user_create, user_existence, user_id_existence, dm_add_contact

app = Flask(__name__)

app.secret_key = "b'\x00$X\xac\xf3N@e\x8d,\x89r\x0c\xf3\xc6\xc0\xc9\xf3l\x1b\xdd\x9b?\xa8\xb9\xf3\x7f\xdf\xa1\x859\xe6\x84\x0738\xc5\xbd\xf1R>\xa1U\x99\x93\xf8\x13N\x02\xb0\xc1\x1d\xdekB\x8b\xec\xdeR\xb79\x7f\xf8\x85'"

@app.route("/", methods=['POST', 'GET'])
def starter_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not user_existence(username):
            print("~ ~ ~ User does not exist ~ ~ ~")
            return render_template("starter_page.html", error="User does not exist")

        if (user_verify_password(username, password)):
            session['username'] = username
            session['public_id'] = User.query.filter_by(username=username).first().public_id
            print("~ ~ ~ Login successful ~ ~ ~")
            return redirect(url_for('main', username=username))
        
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



@app.route("/add_contact", methods=['POST', 'GET'])
def add_contact():
    if request.method == 'POST':
        contact_name = request.form['contact_name']

        contact_public_id = request.form['contact_public_id']
        contact_id = get_id_by_public_id(contact_public_id)

        user_public_id = session['public_id']
        user_id = get_id_by_public_id(user_public_id)
        username = session['username']

        if not user_id_existence(contact_public_id):
            print("~ ~ ~ User does not exist ~ ~ ~")
            return render_template("main.html", error="User does not exist")
        
        add_contact_request(user_id, username, contact_name, contact_id)
        print("~ ~ ~ Add contact request successful ~ ~ ~")
        return jsonify({"message": "Contact request sent"})
    

@app.route("/main/<string:username>")
def main(username):
    return render_template("main.html")


@app.route("/api/requests")
def get_requests():
    user_id = get_id_by_public_id(session['public_id'])
    requests_list = Requests.query.filter_by(user2_id=user_id).all()
    
    data = [
        {
            "id": r.id,
            "user_id": r.user_id,
            "username": r.username,
        }
        for r in requests_list
    ]
    
    return jsonify(data)


@app.route("/api/accept_request/<int:request_id>", methods=["POST"])
def api_accept_request(request_id):
    r = Requests.query.get(request_id)

    dm_add_contact(r.user2_id, r.user_id, r.username)
    dm_add_contact(r.user_id, r.user2_id, r.user2_phantom_name)

    db.session.delete(r)
    db.session.commit()

    return jsonify({"message": "Request accepted"}), 200


@app.route("/api/decline_request/<int:request_id>", methods=["POST"])
def api_decline_request(request_id):
    r = Requests.query.get(request_id)

    db.session.delete(r)
    db.session.commit()

    return jsonify({"message": "Request declined"}), 200





# Temporary route for testing database connection and user creation

@app.route("/users")
def show_users():
    users = User.query.all()
    return "<br>".join([f"ID: {u.id} | Public ID: {u.public_id} |  Username: {u.username} | Password: {u.password} | Salt: {u.salt}" for u in users])

@app.route("/requests")
def show_contacts():
    requests = Requests.query.all()
    return "<br>".join([f"ID: {r.id} | User ID: {r.user_id} | Username: {r.username} | Contact ID: {r.user2_id} | Contact Phantom Name: {r.user2_phantom_name}" for r in requests])



with app.test_request_context():
    print(url_for('starter_page'))
    print(url_for('register'))
    print(url_for('main', username='example_user'))
    print(url_for('add_contact'))





# Database configuration

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)

with app.app_context():
    db.create_all()



if __name__ == "__main__":
    app.run(debug=True)
