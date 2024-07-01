from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SubmitField, FloatField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField

class AddProduct(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    price = StringField("Product Price", validators=[DataRequired()])
    image_url = StringField("Product Image")
    image = FileField("Product Image")
    text = StringField("Product Description")
    category_id = IntegerField("Product Category Id")

    submit = SubmitField("Submit")

class AddOffer(FlaskForm):
    name = StringField("Offer Name", validators=[DataRequired()])
    price = StringField("Offer Price", validators=[DataRequired()])
    image_url = StringField("Offer Image")
    image = FileField("Offer Image")
    text = StringField("Offer Description")

    submit = SubmitField("Submit")

class LogIn(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    submit =  SubmitField("Log in")

class Register(FlaskForm):
    email = EmailField("Email", validators=[Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])

    submit = SubmitField("Sign Up")

