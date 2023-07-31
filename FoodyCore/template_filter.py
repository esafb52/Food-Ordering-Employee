import datetime
import khayyam

import FoodyOrder.model
from FoodyAuth.model import Section
from FoodyCore import app
from FoodyCore.utils import TimeStamp
from FoodyOrder.model import FoodList, Day
from FoodyAuth.model import User





@app.template_filter("Convert2Persian")
def Convert2Persian(dt: datetime.datetime) -> khayyam.JalaliDatetime:
    t = TimeStamp()
    t = t.convert_grg2_jalali_dt(dt)
    return f"{t.time()} - {t.year}/{t.month}/{t.day}"


@app.template_filter("SectionName")
def SectionName(SectionID: int) -> str:
    """This Filter Get a Section id and Return SectionName"""
    return Section.query.get(SectionID).Name or "NULL"


@app.template_filter("GetDayName")
def GetDayName(day : Day.id) -> str:
    """
    this Filter Take a Day_ID and return Day.Name
    """
    return Day.query.filter(Day.id == day).first().NameFa or "NULL"


@app.template_filter("GetFoodName")
def GetFoodName(food_id: int) -> str:
    """
    Get a Food_id and return food Name for db
    """
    return FoodList.query.filter(FoodList.id == food_id).first().Name  or "NULL"



@app.template_filter("GetPersianDate")
def GetPersianDate(date: str) -> str:
    """
    convert an georgian time to jalali time
    """
    t = TimeStamp()
    d = t.convert_grg2_jalali_d(date)
    x = f" {str(d.isoformat())} - {d.strftime('%A') }"
    return x


@app.template_filter("GetUserName")
def GetUserName(userID: int) -> str:
    """
        get user id in db and return user's firstname + last name
    """
    name = User.query.filter(User.id == userID).first()
    if not name:
        return "NULL"
    return f"{name.FirstName} {name.LastName}"



@app.template_filter("GetSectionNameByUserID")
def GetSectionNameByUserID(userID: int) -> str:
    """
        return section name that user work via user id
    """
    user = User.query.filter(User.id == userID).first()
    if not user:
        return "NULL"
    return Section.query.filter(Section.id == user.SectionID).first().Name or "NULL"



print("[OK] All Template Filter Readed By Flask App <FoodyCore>".title())