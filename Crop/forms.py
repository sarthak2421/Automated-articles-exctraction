from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, equal_to, Email, DataRequired, ValidationError
from Crop.models import Userdb


class RegisterForm(FlaskForm):
    def validate_uname(self, uname_to_check):
        un = Userdb.query.filter_by(uname=uname_to_check.data).first()
        if un:
            raise ValidationError("Username Already Exists! Try a Different Username")

    def validate_email(self, email_to_check):
        em = Userdb.query.filter_by(email=email_to_check.data).first()
        if em:
            raise ValidationError("Email Already Exists!")

    uname = StringField(label='User Name', validators=[Length(min=2, max=20), DataRequired()])
    email = StringField(label='E-mail', validators=[Email()])
    pass1 = PasswordField(label='Enter Password', validators=[Length(min=6), DataRequired()])
    pass2 = PasswordField(label='Confirm Password', validators=[equal_to('pass1'), DataRequired()])
    submit = SubmitField(label='Register Yourself')


class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='LogIn')


class PurchaseItem(FlaskForm):
    submit = SubmitField(label='Purchase Item')


class SellItem(FlaskForm):
    submit = SubmitField(label='Sell Item')
