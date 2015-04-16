from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo, ValidationError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from flask.ext.scrypt import check_password_hash, enbase64, debase64
from .models import User, Test


# CREATE ALL FORM OBJECTS HERE (FLASK-WTF)


class LoginForm(Form):
    email = StringField(validators=[
        InputRequired(),
        Email()
    ])
    password = PasswordField(validators=[
        InputRequired()
    ])

    # WTForms supports "inline" validators
    # which are methods of our `Form` subclass
    # with names in the form `validate_[fieldname]`.
    # This validator will run after all the
    # other validators have passed.
    def validate_password(form, field):
        try:
            user = User.query.filter(User.email == form.email.data).one()
        except (MultipleResultsFound, NoResultFound):
            raise ValidationError("We couldn't find your email.")
        if user is None:
            raise ValidationError("We couldn't find your email.")

        # check the password hash!
        if not(check_password_hash(form.password.data, user.password_hash, user.salt)):
            raise ValidationError("Wrong password.")

        # Make the current user available
        # to calling code (view).
        form.user = user


class RegistrationForm(Form):
    first_name = StringField(validators=[
        Length(min=2, max=25),
        InputRequired()
    ])
    last_name = StringField(validators=[
        Length(min=2, max=25),
        InputRequired()
    ])
    email = StringField(validators=[
        Length(min=4, max=25),
        InputRequired(),
        Email()
    ])
    password = PasswordField(validators=[
        InputRequired(),
        EqualTo('confirm', message="Your passwords don't match.")
    ])
    confirm = PasswordField()


    def validate_email(form, field):
        user = User.query.filter(User.email == field.data).first()
        if user is not None:
            raise ValidationError("A user with that email already exists!")


class TestDataForm(Form):

    test_string = TextAreaField('test', validators=[DataRequired()])

class ButtonForm(Form):

    button = BooleanField()


