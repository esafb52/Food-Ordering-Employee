from flask import Flask
from FoodyCore.extension import ServerCsrf, ServerMigrate, ServerCaptchaV2, ServerSession, db, ServerCaptchaV2
from FoodyConfig.config import AutoCinfig


def create_app():
    """Factory Function for crreate flask app"""
    app = Flask(__name__)
    app.config.from_object(AutoCinfig())

    db.init_app(app=app)
    ServerCsrf.init_app(app=app)
    ServerMigrate.init_app(app=app, db=db)
    ServerSession.init_app(app=app)
    ServerCaptchaV2.init_app(app)

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



import FoodyCore.template_filter
import FoodyCore.http_errors
import FoodyCore.baseView