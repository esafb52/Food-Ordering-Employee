import datetime
import os.path

from flask import request, render_template, flash, send_from_directory
from FoodyAdmin import admin
from FoodyAuth.AccessControl.decorators import admin_login_required
from FoodyConfig.config import Admin_Static
from FoodyOrder.model import Order
from FoodyAuth.model import User


@admin.route("/AdminPrivateStatic/<path:filename>/")
@admin_login_required
def AdminStatic(filename):
    """Serve Static Files only To Admin accounts"""
    if os.path.exists(Admin_Static / filename):
        return send_from_directory(Admin_Static, filename)
    else:
        return "File Not Found!", 404



@admin.route("/asdasd/<path:filename>/")
@admin_login_required
def TemPServe(filename):
    return send_from_directory(Admin_Static.parent.parent / "Media/Foods", filename)


@admin.route("/")
@admin_login_required
def index():
    ctx = {
        "all_orders": Order.query.count(),
        "today_orders": Order.query.filter(Order.OrderDate == datetime.date.today()).count(),
        "all_users": User.query.count(),
        "active_users": User.query.filter(User.Active == True).count(),
    }


    # from random import randint, choice
    # from FoodyAuth.model import Section
    # from FoodyCore.extension import db
    # all_sections = Section.query.all()
    #
    # for i in range(314,999):
    #     new_user = User()
    #     new_user.SetPublicKey()
    #     new_user.Active = True if randint(1,3) == 2 else False
    #     new_user.FirstName = "User_"+str(i)
    #     new_user.LastName = "User_"+str(i)
    #     new_user.EmployeeCode = i+5
    #     new_user.PhoneNumber = str(randint(111111111,99999999999+1))
    #     new_user.SectionID = choice(all_sections).id
    #     new_user.NationalCode = str(randint(111111111,99999999999+1))
    #     new_user.Username = str("User_"+str(i))
    #     new_user.SetPassword(str(i))
    #     try:
    #         db.session.add(new_user)
    #         db.session.commit()
    #     except Exception as e:
    #         db.session.rollback()
    #         pass



    return render_template("admin/index.html", ctx=ctx)


