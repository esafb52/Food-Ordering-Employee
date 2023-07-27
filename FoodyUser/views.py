import datetime
import os.path

import khayyam

from FoodyUser import user
from flask import render_template, send_from_directory, request


from FoodyAuth.AccessControl.decorators import login_required
from FoodyConfig.config import User_Static
from FoodyOrder.model import FoodList, Order
from FoodyCore.utils import TimeStamp




@user.route("/UserStatic/<path:filename>")
@login_required
def UserStatic(filename):
    """Serve Static files to users that have access"""
    if os.path.exists(User_Static / filename):
        return send_from_directory(User_Static, filename)
    else:
        return "File Not Found!", 404



@user.get("/")
@login_required
def index_view():
    return render_template("user/index.html")


@user.route("/menu/", methods=["GET"])
@login_required
def get_menu():
    """return food menu for user"""
    ctx = {}
    ctx["foods"] = FoodList.query.filter(FoodList.Active == True).all()
    return render_template("user/menu.html", ctx=ctx)


@user.route("/order/", methods=["GET"])
@login_required
def order_get():
    return render_template("user/order.html")


@user.route("/history/", methods=["GET"])
@login_required
def history_get():
    page = request.args.get("page", type=int, default=1)
    ctx = {
        "orders": Order.query.order_by(Order.id.desc()).filter(Order.UserID == request.user_object.id).paginate(per_page=15, page=page),
        "current_page":page

    }
    return render_template("user/history.html", ctx=ctx)


@user.route("/panel/", methods=["GET"])
@login_required
def panel_get():
    """

    """
    Today = khayyam.JalaliDate.today()
    t = TimeStamp()

    startofMonth = t.convert_jlj2_georgian_d(khayyam.JalaliDate(year=Today.year, month=Today.month, day=1))
    endofMonth = t.convert_jlj2_georgian_d(khayyam.JalaliDate(year=Today.year, month=Today.month, day=Today.daysinmonth))

    ctx = {
        "user":request.user_object,
        "this_month_orders": Order.query.filter(Order.UserID == request.user_object.id).filter(Order.OrderDate > startofMonth).filter(Order.OrderDate < endofMonth).count()

    }
    return render_template("user/panel.html", ctx=ctx)


