from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired
class SignupFormdemo(Form):
    email = StringField('email',validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired()])
    submit = SubmitField("Sign In")