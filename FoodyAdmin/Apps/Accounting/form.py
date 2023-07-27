from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired


class SearchBySectionsForm(FlaskForm):
    """ Base Flask Form For Searching in Sections """


    Sections = SelectField(
        choices=[],
        validators=[
            DataRequired(),
            InputRequired()
        ],
        render_kw={
            "class":"form-control",
            "placeholder":"بخش مورد نظر"
        }
    )

    StartDate = StringField(
        validators=[
            DataRequired(),
            InputRequired()
        ],
        render_kw={
            "class":"form-control",
            "placeholder":"تاریخ شروع"
        }
    )

    EndDate = StringField(
        validators=[
            DataRequired(),
            InputRequired()
        ],
        render_kw={
            "class":"form-control",
            "placeholder":"تاریخ پایان"
        }
    )

    Submit = SubmitField()