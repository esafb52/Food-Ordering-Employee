from flask import render_template, flash, redirect, request, url_for
from FoodyAdmin import admin
from FoodyAdmin.views import admin_login_required
from FoodyCore.extension import ServerCaptchaV2, db
from FoodyAuth.model import User, Section

from FoodyConfig.config import SMS_IR_TEMPLATES
import FoodyAdmin.Apps.ManageUsers.utils as ManageUsersUtils
import FoodyAdmin.Apps.ManageUsers.form as ManageUsersForm

from FoodyCore.extension import smsIR


BASE_URL = "manage/users/"
TEMPLATE_FOLDER = "admin/ManageUsers"



@admin.route(f"/{BASE_URL}/", methods=["GET"])
@admin_login_required
def add_new_users():
    """This view return template for adding new user"""
    ctx = {
        "manage_users": "show",
        "add_new_user":"item-active"
    }
    form = ManageUsersForm.AddNewUserForm()
    form.Active.data = "inactive"
    return render_template(f'{TEMPLATE_FOLDER}/add_new_user.html', ctx=ctx, form=form)


@admin.route(f"/{BASE_URL}/", methods=["POST"])
@admin_login_required
def add_new_users_post():
    """
    this view take a post request and add new user to app
    """
    ctx = {
        "manage_users": "show",
        "add_new_user":"item-active"
    }
    form = ManageUsersForm.AddNewUserForm()
    captcha = ServerCaptchaV2.is_verify()

    if not captcha:
        flash("ارزیابی کپچا نادرست است", "danger")
        return render_template(f'{TEMPLATE_FOLDER}/add_new_user.html', ctx=ctx, form=form)

    if not form.validate():
        flash("برخی مقادیر مقدار دهی اولیه نشده اند", "danger")
        return render_template(f'{TEMPLATE_FOLDER}/add_new_user.html', ctx=ctx, form=form)


    if User.query.filter_by(Username=form.Username.data).first():
        flash("نام کاربری ، توسط کاربر دیگری انتخاب شده است/ لطفا نام کاربری دیگری انتخاب کنید", "danger")
        return render_template(f'{TEMPLATE_FOLDER}/add_new_user.html', ctx=ctx, form=form)

    if User.query.filter_by(PhoneNumber=form.PhoneNumber.data).first():
        flash("شماره تماس توسط کاربری دیگری انتخاب شده است / لطفا شماره تلفن دیگری وارد کنید", "danger")
        return render_template(f'{TEMPLATE_FOLDER}/add_new_user.html', ctx=ctx, form=form)

    if User.query.filter_by(NationalCode=form.NationalCode.data).first():
        flash("کد ملی توسط کاربر دیگری انتخاب شده است / لطفا کد ملی دیگری انتخاب کنید", "danger")
        return render_template(f'{TEMPLATE_FOLDER}/add_new_user.html', ctx=ctx, form=form)

    if User.query.filter_by(EmployeeCode=form.EmployeeCode.data).first():
        flash("کد کارمندی کاربر تکراری می باشد / لطفا کد کارمندی جدیدی وارد کنید", "danger")
        return render_template(f'{TEMPLATE_FOLDER}/add_new_user.html', ctx=ctx, form=form)

    # check SectionID is valid
    if not (sectionDB := Section.query.filter_by(PublicKey=form.SectionID.data).first()):
        flash ("موفعیت شعلی کارمند به درستی وارد نشده است","danger")
        return render_template(f'{TEMPLATE_FOLDER}/add_new_user.html', ctx=ctx, form=form)


    NewUser = User()

    if not NewUser.SetUsername(form.Username.data):
        flash("خطایی هنگام تنظیم نام کاربری کاربر رخ داد / احتمالا نام کاربری توسط کاربر دیگری انتخاب شده است", "danger")
        return render_template(f'{TEMPLATE_FOLDER}/add_new_user.html', ctx=ctx, form=form)

    if form.Email.data:
        print("Here")
        if not NewUser.SetEmailAddress(form.Email.data):
            print("Here 123")
            flash("آدرس ایمیل کاربر تکراری می باشد\nلطفا آدرس ایمیل یکتایی برای کاربر وارد کنید", "danger")
            return render_template(f'{TEMPLATE_FOLDER}/add_new_user.html', ctx=ctx, form=form)


    NewUser.SetPublicKey()
    NewUser.SetPassword(form.Password.data)
    NewUser.NationalCode = form.NationalCode.data
    NewUser.Active = True if form.Active.data == "active" else False
    NewUser.EmployeeCode = form.EmployeeCode.data
    NewUser.SectionID = sectionDB.id
    NewUser.PhoneNumber = form.PhoneNumber.data
    NewUser.FirstName = form.FirstName.data
    NewUser.LastName = form.LastName.data


    if form.Email.data:
        NewUser.Email = form.Email.data

    try:
        db.session.add(NewUser)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        flash("خطایی رخ داد / بعدا امتحان کنید", "danger")
        return render_template(f'{TEMPLATE_FOLDER}/add_new_user.html', ctx=ctx, form=form)
    else:
        smsResponse = smsIR.send_verify_code(
            number=NewUser.PhoneNumber ,# value: string of a mobile
            template_id=SMS_IR_TEMPLATES["ADD-NEW-USER"]["ID"] ,##  value 150740
            parameters=[
                {
                    "name":"EMPLOYEE_NAME",
                    "value":NewUser.FirstName + " " + NewUser.LastName # value: string,

                }
            ]
        )
        try:
            smsMessage = smsResponse.json()["message"]
        except KeyError:
            smsMessage = "NULL"


        msg = 'کاربر با موفقیت به سامانه اضافه گردید / '
        msg += "پیامک با موفقیت ارسال "
        msg += "گردید" if smsResponse.status_code == 200 else "نگردید"
        msg += "\n پیغام دریافتی از سرور ارسال پیامک: "
        msg += smsMessage
        flash(msg, "success")

        return redirect(request.referrer)


    flash("عملیاتی انجام نشد", "warning")
    return redirect(request.referrer)


@admin.route(f"{BASE_URL}/all/", methods=["GET"])
@admin_login_required
def manage_users_all():
    """This View Show All Users In app"""
    ctx = {
        "manage_users": "show",
        "manage_users_all": "item-active"
    }
    page = request.args.get(key="page", type=int, default=1)
    ctx["users"] = User.query.order_by(User.id).paginate(page=page, per_page=15)
    ctx["current_page"] = page
    return render_template(f"{TEMPLATE_FOLDER}/all_users.html", ctx=ctx)


@admin.route(f"{BASE_URL}/search/", methods=["GET"])
@admin_login_required
def search_in_users():

    ctx = {
        "manage_users": "show",
        "search_in_users": "item-active"
    }
    form = ManageUsersForm.SearchInUsers()
    return render_template(f"{TEMPLATE_FOLDER}/search_in_users.html", ctx=ctx, form=form)



@admin.route(f"{BASE_URL}/search/", methods=["POST"])
@admin_login_required
def search_in_users_post():
    ctx = {
        "manage_users": "show",
        "search_in_users": "item-active"
    }
    form = ManageUsersForm.SearchInUsers()
    if not form.validate():
        flash("برخی موارد مقدار دهی نشده اند", "danger")
        return render_template(f"{TEMPLATE_FOLDER}/search_in_users.html", ctx=ctx, form=form)
    else:
        searchOption, searchBox = form.SearchOption.data, form.SearchBox.data

        SearchResult = ManageUsersUtils.Search_In_Users(option=searchOption, data=searchBox)
        if not SearchResult:
            flash("نتیجه ای با موارد وارد شده یافت نشد", "danger")
            return redirect(request.referrer)
        else:
            ctx["result"] = SearchResult
            return render_template(f"{TEMPLATE_FOLDER}/search_in_users_result.html", ctx=ctx)



@admin.route(f"{BASE_URL}/edit/<uuid:userKey>/", methods=["GET"])
@admin_login_required
def edit_user(userKey):
    """
        This view take a user PublicKey and find user in db and return a template for editing user
    :param userKey: uuid
    :return: template
    """
    ctx = {
        "manage_users": "show",
        "manage_users_all": "item-active"
    }
    userKey = str(userKey)
    user_db = User.query.filter(User.PublicKey == userKey).first()
    if not user_db:
        flash("کاربر با مشخصات وارده یافت نشد", "danger")
        return redirect(url_for('admin.manage_users_all'))

    form = ManageUsersForm.AddNewUserForm()

    form.FirstName.data = user_db.FirstName
    form.LastName.data = user_db.LastName
    form.Username.data = user_db.Username
    form.Password.data = user_db.Password
    form.Password.type = "password"
    form.Password.errors = ["به علت رمزنگاری گذرواژه ها امکان مشاهده وجود ندارد", "صورتی که میخواهید گذرواژه را تغییر دهید صرفا این فیلد را پر کنید"]
    form.NationalCode.data = user_db.NationalCode
    form.PhoneNumber.data = user_db.PhoneNumber
    form.SectionID.data = Section.query.filter(Section.id == user_db.SectionID).first().PublicKey
    form.Active = ""
    # form.Active.data = "active" if user_db.Active else "inactive"
    form.EmployeeCode.data = user_db.EmployeeCode
    form.Email.data = user_db.Email



    form.username = user_db.FirstName + " " + user_db.LastName
    form.user = user_db
    return render_template(f"{TEMPLATE_FOLDER}/edit_user.html", ctx=ctx,form=form)




@admin.route(f"{BASE_URL}/edit/<uuid:userKey>/", methods=["POST"])
@admin_login_required
def edit_user_post(userKey):
    """
    This view take a post request for edit a user info in db
    :param userKey:
    :return:
    """
    ctx = {
        "manage_users": "show",
        "manage_users_all": "item-active"
    }
    userKey = str(userKey)
    user_db = User.query.filter(User.PublicKey == userKey).first()
    if not user_db:
        flash("کاربر با مشخصات وارده یافت نشد", "danger")
        return redirect(url_for('admin.manage_users_all'))

    form = ManageUsersForm.AddNewUserForm()
    form.Active.validators = []
    form.Active.validate_choice = False

    if not form.validate():
        print(form.errors)
        flash("خطایی رخ داد \n  بعدا امتحان کنید", "danger")
        return redirect(request.referrer)
    else:

        if form.Username.data != user_db.Username:
            if not user_db.SetUsername(form.Username.data):
                flash("نام کاربری توسط کاربر دیگری انتخاب شده است", "danger")
                return render_template(f"{TEMPLATE_FOLDER}/edit_user.html", ctx=ctx, form=form)

        if form.NationalCode.data != user_db.NationalCode:
            if not user_db.SetNationalCode(form.NationalCode.data):
                flash("کد ملی توسط کاربر دیگری انتخاب شده است", "danger")
                return render_template(f"{TEMPLATE_FOLDER}/edit_user.html", ctx=ctx, form=form)

        if form.PhoneNumber.data != user_db.PhoneNumber:
            if not user_db.SetPhoneNumber(form.PhoneNumber.data):
                flash("شماره تماس توسط کاربر دیگری انتخاب شده است", "danger")
                return render_template(f"{TEMPLATE_FOLDER}/edit_user.html", ctx=ctx, form=form)

        if form.EmployeeCode.data != user_db.EmployeeCode:
            if not user_db.SetEmploeeCode(form.EmployeeCode.data):
                flash("کد کارمندی توسط کاربر دیگری انتخاب شده است", "danger")
                return render_template(f"{TEMPLATE_FOLDER}/edit_user.html", ctx=ctx, form=form)


        if not (section_DB := Section.query.filter(Section.PublicKey == form.SectionID.data).first()):
            flash("موقعیت شغلی انتخاب شده نامعتبر است", "danger")
            return render_template(f"{TEMPLATE_FOLDER}/edit_user.html", ctx=ctx, form=form)

        user_db.FirstName = form.FirstName.data
        user_db.LastName = form.LastName.data
        user_db.SectionID = section_DB.id
        user_db.Email = form.Email.data
        # user_db.Active = True if form.Active.data == "active" else False
        if form.Password.data != user_db.Password:
            user_db.SetPassword(form.Password.data)

        try:
            db.session.add(user_db)
            db.session.commit()
        except:
            db.session.rollback()
            flash("خطایی رخ داد\n دوباره سسعی کنید","danger")
        else:
            flash("عملیات با موفقیت انجام شد \n حساب کاربر با موفقیت بروزرسانی شد","success")

        return redirect(request.referrer)