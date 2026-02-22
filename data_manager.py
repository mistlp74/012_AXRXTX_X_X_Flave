from models import db, User, Requests, Contacts, Messages
import os
import hashlib

def delete_the_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

def user_existence(username):
    return User.query.filter_by(username=username).first() is not None

def user_id_existence(public_id):
    return User.query.filter_by(public_id=public_id).first() is not None


def user_get(username):
    return User.query.filter_by(username=username).first()


def user_verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    salt = user.salt
    hashed_password = get_hashed_password(password, salt)

    if not user:
        return False
    return user.password == hashed_password


def user_create(username, password):
    if user_existence(username):
        return False
    
    salt, hashed_password = hash_password(password)

    new_user = User(

        public_id="TEMP_PUBLIC_ID",
        username=username,
        password=hashed_password,
        salt=salt
    )

    db.session.add(new_user)
    db.session.commit()

    new_user.public_id = generate_public_id(new_user.id)
    db.session.commit()

    return True


# Password hashing functions

def hash_password(password):
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
    return salt, hashed

def get_hashed_password(password, salt):
    new_hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
    return new_hashed
    
def generate_public_id(user_id):
    prefix = os.urandom(4).hex()
    suffix = os.urandom(3).hex()
    return f"{prefix}#{user_id}_{suffix}"

def get_id_by_public_id(public_id):
    parts = str(public_id).split('#')
    user_id_str = parts[1].split('_')[0]
    return int(user_id_str)


# Users interaction functions

def add_contact_request(user_id, username, contact_name, contact_id):
    new_request = Requests(
        user_id = user_id,
        username = username,
        user2_id = contact_id,
        user2_phantom_name = contact_name
    )

    db.session.add(new_request)
    db.session.commit()

def dm_add_contact(user_id, contact_name, contact_id):
    new_contact = Contacts(
        user_id = user_id,
        user2_id = contact_id,
        user2_phantom_name = contact_name
    )

    db.session.add(new_contact)
    db.session.commit()