from flask import Flask, request, session
from FoodyCore.extension import ServerCsrf, ServerMigrate, ServerCaptchaV2, ServerSession, db, ServerCaptchaV2
from FoodyConfig.config import AutoCinfig
import FoodyAuth.utils as AuthUtils

def create_app():
    """Factory Function for crreate flask app"""
    app = Flask(__name__)
    app.config.from_object(AutoCinfig())

    db.init_app(app=app)
    ServerCsrf.init_app(app=app)
    ServerMigrate.init_app(app=app, db=db)
    ServerSession.init_app(app=app)
    ServerCaptchaV2.init_app(app)

    print(ServerCaptchaV2.ENABLED)

    from FoodyOrder import order
    app.register_blueprint(order, url_prefix="/order")

    from FoodyWeb import web
    app.register_blueprint(web, url_prefix="/")


    from FoodyAuth import auth
    app.register_blueprint(auth, url_prefix="/auth")

    from FoodyUser import user
    app.register_blueprint(user, url_prefix="/user")

    from FoodyAdmin import admin
    app.register_blueprint(admin, url_prefix="/admin")

    return app



app = create_app()




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


import FoodyCore.template_filter
import FoodyCore.http_errors
