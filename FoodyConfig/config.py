import os
import datetime
import secrets
import khayyam


from pathlib import Path
from dotenv import load_dotenv
from redis import Redis
from FoodyConfig.StaticConfig.SMS_IR_Config import SMS_IR_TEMPLATES


load_dotenv()
BASE_DIR = Path(__file__).parent.parent


STATUS = os.environ.get("APP_DEBUG", False)
ADMIN_LOGIN_TOKEN = os.environ.get("ADMIN_LOGIN_TOKEN", "123654")


# DB INFO <for localhost>
USERNAME_DB = os.environ.get('DATABASE_USERNAME')
PASSWORD_DB = os.environ.get('DATABASE_PASSWORD')
HOST_DB = os.environ.get('DATABASE_HOST')
PORT_DB = os.environ.get('DATABASE_PORT')
NAME_DB = os.environ.get('DATABASE_NAME')
DATABASE_TABLE_PREFIX = os.environ.get("DATABASE_TABLE_PREFIX", "FOODY_")


MAX_ORDER_TIMEOUT_DAY = 7
# this is the default for showing ordering food that means user only can order for only a week ahead


# this variables hold some special location for saving or serving static files
Media = BASE_DIR.joinpath("Media")
FoodDir = Media.joinpath("Foods")
Web_Static = BASE_DIR.joinpath("FoodyWeb/static")
Auth_Static = BASE_DIR.joinpath("FoodyAuth/private_static")
User_Static = BASE_DIR.joinpath("FoodyUser/private_static")
Admin_Static = BASE_DIR.joinpath("FoodyAdmin/private_static")


if STATUS:
    REDIS_URI = os.environ.get('REDIS_LOCAL_HOST')
else:
    REDIS_URI = os.environ.get("REDIS_URI")


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(64))
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # session configuration
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=16)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_NAME = '_session_cookie_'

    SESSION_REDIS = Redis().from_url(REDIS_URI)

    # google recaptcha v2
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_ENABLED = True if os.environ.get('RECAPTCHA_ENABLED', '') == 'True' else False


class Development(BaseConfig):
    DEBUG = True
    FLASK_DEBUG = True


class Production(BaseConfig):
    DEBUG = False
    FLASK_DEBUG = False


def AutoCinfig():
    """
    This Method choise the Best config for app base on azma-debug <local environment>
    """
    return Production if not STATUS else Development


if STATUS:
    SMS_API = None
    SMS_LINE = None
else:
    SMS_API = os.environ.get("SMS_API_KEY")
    SMS_LINE = os.environ.get("SMS_LINE_NUMBER")



# ----------------------------------------------- Days config ---------------------------------------------
# dont change or touch _variables
_ALL_VALID_DAYS_ENGLISH = [
    "Shanbeh",
    "Yekshanbeh",
    "Doshanbeh",
    "Seshanbeh",
    "Chaharshanbeh",
    "Panjshanbeh",
    "Jomeh"
]
_DATE_PERSIAN_FARSI = list()
for i in range(0, 7):
    # 1402, 4, 24 this day is shanbe => to jomeh
    d = khayyam.JalaliDatetime(1402, 4, 24) + datetime.timedelta(days=i)
    _DATE_PERSIAN_FARSI.append(d.strftime("%A"))

_ALL_VALID_DAYS_PERSIAN = list(_DATE_PERSIAN_FARSI)

# this list hold all days => [ (persian-Name, english-Name), ...]
ALL_DAYS = list(zip(_ALL_VALID_DAYS_PERSIAN, _ALL_VALID_DAYS_ENGLISH))

_english_to_persian_dict = dict()
for index, each in enumerate(_ALL_VALID_DAYS_ENGLISH):
    _english_to_persian_dict[str(each)] = _ALL_VALID_DAYS_PERSIAN[index]

_persian_to_english_dict = dict()
for index, each in enumerate(_ALL_VALID_DAYS_PERSIAN):
    _persian_to_english_dict[str(each)] = _ALL_VALID_DAYS_ENGLISH[index]

# with this dict you can search immediately in days
SEARCH_ABLES_DAYS = {
    "english_to_persian": _english_to_persian_dict,
    "persian_to_english": _persian_to_english_dict
}

# this variable keep all valid days that users can order
VALID_DAYS = ALL_DAYS[:-1]  # for adding or deleting day for ordering only change this list
VALID_DAYS_PERSIAN = [each[0] for each in VALID_DAYS]


# --------------------------------- Enf of the days config ---------------------------------


# valid images extensions for uploading for a food
VALID_IMAGE_EXTENSIONS = [
    '.png',
    '.jpg',
    '.jpeg'
]