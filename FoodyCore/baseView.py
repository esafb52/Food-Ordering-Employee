from FoodyCore import app
from flask import session, request

from FoodyConfig.config import ADMIN_CONFIG
from FoodyConfig.SuperUser import create_super_user

import FoodyAuth.utils as AuthUtils

with app.app_context():
    create_super_user(
        username=ADMIN_CONFIG["ADMIN_USERNAME"],
        password=ADMIN_CONFIG["ADMIN_PASSWORD"],
        email=ADMIN_CONFIG["ADMIN_EMAIL"],
        phonenumber=ADMIN_CONFIG["AMDIN_PHONE"]
    )

@app.before_request
def before_request():
    """
    This Middleware like django authentication put some data in request before heads up to actual view
    :return: None


        is_userAuthenticated = True  : if user is authenticated
        is_userAuthenticated = False  : if user is not authenticated


        user_object = Sqlalchemy<User Object>  : if is_userAuthenticated is True
        user_object = None  : if is_userAuthenticated is False

    """
    request.is_userAuthenticated = False
    request.user_object = None

    if (account_id := session.get("account-id")):
        user_db = AuthUtils.LoadUserObject(account_id)
        if user_db:
            request.is_userAuthenticated = True if session.get("login") else False
            request.user_object = user_db
