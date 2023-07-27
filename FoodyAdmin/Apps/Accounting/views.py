import datetime
import os.path
import pathlib
import uuid

from flask import render_template, flash, redirect, request
from FoodyAdmin import admin
from FoodyAdmin.views import admin_login_required
from FoodyCore.extension import db
from FoodyOrder.model import Order
from FoodyAuth.model import Section

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
    """
    form = AccountingForms.SearchBySectionsForm()
    form.Sections.choices = AccountingUtils.get_all_unique_sections_wtf_select()

    ctx={
        "accounting": "show",
        "report_section": "item-active",
        "all_sections": db.session.query(Section.Name).distinct().all(),
    }

    return render_template(f"{TEMPLATE_FOLDER}/report_section.html", ctx=ctx, form=form)