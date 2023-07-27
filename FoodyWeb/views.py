from FoodyWeb import web
from flask import redirect, url_for, send_from_directory


# init user and sections
from FoodyAuth.model import User
from FoodyCore.extension import db
from FoodyAuth.model import Section
from FoodyConfig.StaticConfig.Sections import SECTIONS
from FoodyConfig.config import ALL_DAYS
from FoodyAdmin.model import Admin
from FoodyOrder.model import Day
from FoodyConfig.config import Media




@web.route("/asdasdasd/<path:path>")
def aimd(path):
    return send_from_directory(Media / "Foods", path)



@web.route("/")
def index_view():

    # add a user
    new_user = User()
    new_user.SetPassword("123654")
    new_user.SetUsername("alisharify")
    new_user.EmployeeCode = 111
    new_user.SetPublicKey()
    new_user.NationalCode = "12312321"
    new_user.Email = "helloworld@gmail.com"
    new_user.PhoneNumber = "12333333333"
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

    # add section
    for each in SECTIONS:
        s = Section()
        s.SetPublicKey()
        s.Name = each["name"]
        s.Description = each["description"]
        try:
            db.session.add(s)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()


    a = Admin()
    a.Active = 1
    a.TryNumber = 0
    a.SetPublicKey()
    a.SetUsername("alisharify")
    a.SetPassword("123654")
    a.PhoneNumber = "12333333333"
    try:
        db.session.add(a)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)

    for each in ALL_DAYS:
        d = Day()
        d.SetPublicKey()
        d.NameFa = each[0]
        d.NameEn = each[1]
        try:
            db.session.add(d)
            db.session.commit()
        except :
            db.session.rollback()


    return redirect(url_for('auth.login'))