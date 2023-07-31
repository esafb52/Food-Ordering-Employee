import datetime


from flask import render_template, flash, redirect, request
from FoodyAdmin import admin
from FoodyAdmin.views import admin_login_required
from FoodyCore.extension import db
from FoodyOrder.model import Order
from FoodyAuth.model import Section, User

import FoodyAdmin.Apps.Accounting.form as AccountingForms
import FoodyAdmin.Apps.Accounting.utils as AccountingUtils


BASE_URL = "manage/Accounting"
TEMPLATE_FOLDER = "admin/Accounting"



@admin.route(f"{BASE_URL}/Report/", methods=["GET"])
@admin_login_required
def report_today_get():
    ctx={
        "report_today": "item-active",
        "accounting": "show",
        "today_orders": Order.query.filter(Order.OrderDate == datetime.date.today()).all()
    }

    ctx["total_orders"] = len(ctx["today_orders"])

    return render_template(f"{TEMPLATE_FOLDER}/report_today.html", ctx=ctx)


@admin.route(f"{BASE_URL}/Report/Section/", methods=["GET"])
@admin_login_required
def report_section_get():
    """
    render query by sections in orders
    """
    form = AccountingForms.SearchBySectionsForm()
    form.Sections.choices = AccountingUtils.get_all_unique_sections_wtf_select()

    ctx={
        "accounting": "show",
        "report_section": "item-active",
        "all_sections": db.session.query(Section.Name).distinct().all(),
    }

    return render_template(f"{TEMPLATE_FOLDER}/report_section.html", ctx=ctx, form=form)

@admin.route(f"{BASE_URL}/Report/Section/", methods=["POST"])
@admin_login_required
def report_section_post():
    """
    take a post request and query in db (with section)
    """

    ctx={
        "accounting": "show",
        "report_section": "item-active",
    }

    form = AccountingForms.SearchBySectionsForm()
    form.Sections.choices = AccountingUtils.get_all_unique_sections_wtf_select()

    if not form.validate():
        return redirect(request.referrer)

    if form.Sections.data != "all":
        SectionDb = Section.query.filter_by(PublicKey=form.Sections.data).first()
        if not SectionDb:
            flash("بخش مورد نظر به درستی وارد نشده است", "danger")
            return redirect(request.referrer)

    if not form.validate_dates():
        flash("تاریخ به درستی وارد نشده است", "danger")
        return redirect(request.referrer)

    startDate, endDate = form.GetGeorgianDates()

    if startDate > endDate:
        flash("تاریخ شروع نمی تواند از تاریخ انتهایی بزرگتر باشد", "danger")
        return redirect(request.referrer)

    Orders = Order.query.join(User, Order.UserID == User.id).filter(User.SectionID == SectionDb.id).filter(Order.OrderDate >= startDate)\
        .filter(Order.OrderDate <= endDate).all()

    ctx["orders"] = Orders
    ctx["section"] = SectionDb.Name
    ctx["total_orders"] = len(Orders)

    return render_template(f"{TEMPLATE_FOLDER}/report_section_result.html", ctx=ctx, form=form)