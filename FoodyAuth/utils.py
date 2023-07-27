import uuid
from flask import session
from FoodyAuth.model import User
from FoodyCore.extension import ServerRedis


def generate_change_password_token(User_PublicKey:uuid) -> str:
    """ This function generate and set a change password token for user """
    while True:
        token = str(uuid.uuid4())
        if ServerRedis.get(name=token):
            continue
        else:
            return token


def login(user_session: session, user_db:User):
    """This function take a user session and authenticate user for login """
    user_id, user_password = user_db.id, user_db.Password
    session["account-id"] = user_id
    session["account-password"] = user_password
    session["login"] = True


def LoadUserObject(user_id : int) -> User:
    """ Load User via user primary key """
    return User.query.get(user_id) or None


def LoadUserObjectPublickKey(public_key : uuid) -> User:
    """ Load User via user Public key """
    return User.query.filter_by(PublicKey = public_key).first() or None

