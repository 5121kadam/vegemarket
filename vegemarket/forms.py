
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField
from wtforms.validators import InputRequired, email

# Form Use for submit detail of User
class CheckoutForm(FlaskForm):
    firstName = StringField("Your First Name", validators=[InputRequired()])
    lastName = StringField("Your Last Name", validators=[InputRequired()])
    email = StringField("Your Email", validators=[InputRequired(), email()])
    phone = StringField("Your Phone Number", validators=[InputRequired()])
    submit = SubmitField("Submit")