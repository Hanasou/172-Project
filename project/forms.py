from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

class SignUpForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired(), EqualTo('confirm_password', message = 'Passwords must match')])
    confirm_password = PasswordField("Password", validators = [DataRequired()])
    first_name = StringField("First Name", validators = [DataRequired()])
    last_name = StringField("Last Name", validators = [DataRequired()])
    submit = SubmitField("Register")

    def check_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Username already registered')

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField("Login")
