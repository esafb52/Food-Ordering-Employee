import datetime

from flask import request, jsonify
from FoodyAdmin import admin
from FoodyAuth.AccessControl.decorators import admin_login_required
from FoodyOrder.model import Order
from FoodyCore.extension import db
from FoodyAuth.model import Section, User



@admin.route("/api/AllOrders/", methods=["GET"])
@admin_login_required
def All_Orders_API():
    """
        this api view take 2 get arguments
            from: a date for starting time
            to: a date for ending time

        and return all Orders from date to end date
    """
    Ftime = request.args.get("from", type=str, default=None)
    Etime = request.args.get("end", type=str, default=None)

    if not Ftime or not Etime:
        return jsonify({}), 400

    try:
        f = datetime.datetime.strptime(Ftime,"%Y-%m-%dT%H:%M:%S.%fZ")
        e = datetime.datetime.strptime(Etime,"%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return jsonify({"status":"failed", "error": "invalid date format"}), 400
    except Exception as e:
        print(e)
        return jsonify({"status":"failed", "error": "invalid date format"}), 400

    f = f.date()
    e = e.date()

    data = []
    for each in range(0, (f-e).days):
        time = f + datetime.timedelta(days=each)
        temp = {}
        query = Order.query.filter(Order.OrderDate == time).count()
        temp[str(time)] = query
        data.append(temp)

    return jsonify({"status":"success", "data": data}), 200


@admin.route("/api/AllOrders/Sections/", methods=["GET"])
@admin_login_required
def All_Orders_Sections_API():
    """
    this view take two ISO format date and return all Orders(filtered by SectionsName) that
    are between these two dates
    """
    Ftime = request.args.get("from", type=str, default=None)
    Etime = request.args.get("end", type=str, default=None)

    if not Ftime or not Etime:
        return jsonify({}), 400

    try:
        f = datetime.datetime.strptime(Ftime,"%Y-%m-%dT%H:%M:%S.%fZ")
        e = datetime.datetime.strptime(Etime,"%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return jsonify({"status":"failed", "error": "invalid date format"}), 400
    except Exception as e:
        print(e)
        return jsonify({"status":"failed", "error": "invalid date format"}), 400

    f = f.date()
    e = e.date()

    AllSections = [section for section in db.session.query(Section.id, Section.Name).distinct().all()]

    data = []
    for sectionID, sectionName in AllSections:
        all_section_orders = Order.query.join(User, Order.UserID == User.id).filter(User.SectionID == sectionID)\
            .filter(Order.OrderDate >= f).filter(Order.OrderDate <= e)\
            .count()

        temp = {}
        temp["section_name"] = str(sectionName)
        temp["orders_count"] = all_section_orders
        data.append(temp)

    return jsonify({"status":"success", "data": data}), 200



@admin.route("/api/All/Users/", methods=["GET"])
@admin_login_required
def All_Users_Info():
    """
    this view return an info about all user and how many user each section have
    """

    AllSections = db.session.query(Section.id, Section.Name).distinct().all()

    