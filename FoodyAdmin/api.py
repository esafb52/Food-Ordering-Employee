import datetime

from flask import request, jsonify
from FoodyAdmin import admin

from FoodyCore.utils import TimeStamp
from FoodyAuth.AccessControl.decorators import admin_login_required

from FoodyOrder.model import Order

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
        temp[str(time)] = str(time)
        temp["data"] = query
        data.append(temp)


    return jsonify({"status":"success", "data": data}), 200