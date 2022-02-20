from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class SignUpForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class DataForm(FlaskForm):
    no_ppl = IntegerField('Number of people in household', validators = [DataRequired(), NumberRange(min=1)])
    natural_gas = IntegerField('Natural Gas Consumed (CCF)', validators = [NumberRange(min=0)])
    electricity = IntegerField('Electricity Consumption (kWh)', validators = [NumberRange(min=0)])
    fuel = IntegerField('Fuel Consumed (Gallons)', validators = [NumberRange(min=0)])

    submit = SubmitField('Submit')