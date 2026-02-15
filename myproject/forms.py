from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Log in")

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    pass_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match!')
    ])
    gender = SelectField('Gender', validators=[DataRequired()], choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
    height = StringField('Height (cm)', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    weight = StringField('Weight (kg)', validators=[DataRequired()])
    blood = SelectField('Blood Type', validators=[DataRequired()], choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('O', 'O'),
        ('AB', 'AB')
    ])
    health_issues = SelectField('Health Conditions', validators=[DataRequired()], choices=[
        ('none', 'No Health Issues'),
        ('diabetes', 'Diabetes'),
        ('hypertension', 'High Blood Pressure'),
        ('heart_disease', 'Heart Disease'),
        ('high_cholesterol', 'High Cholesterol'),
        ('obesity', 'Obesity'),
        ('underweight', 'Underweight'),
        ('digestive_issues', 'Digestive Issues'),
        ('food_allergies', 'Food Allergies'),
        ('other', 'Other')
    ])
    plan_period = SelectField('Plan Period', validators=[DataRequired()], choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly')
    ])
    exercise = SelectField('Exercise Level', validators=[DataRequired()], choices=[
        ('1.2', 'Little or no exercise'),
        ('1.375', 'Lightly active'),
        ('1.55', 'Moderately active'),
        ('1.725', 'Very active'),
        ('1.9', 'Extra active')
    ])
    food_type = SelectField('Type of food', validators=[DataRequired()], choices=[
        ('vegan', 'Vegan'),
        ('vegetarian', 'Vegetarian'),
        ('non-vegetarian', 'Non-Vegetarian'),
        ('eggitarian', 'Eggitarian')
    ])
    diet_pref = SelectField('Diet preference', validators=[DataRequired()], choices=[
        ('balanced', 'Balanced'),
        ('low carbohydrates', 'Low Carbohydrates'),
        ('low fats', 'Low Fats')
    ])
    submit = SubmitField('Register!')

    def validate_email(self, field):
        from myproject import users_collection
        if users_collection.find_one({"email": field.data}):
            raise ValidationError('Email already registered. Please use a different email.')

    def validate_username(self, field):
        from myproject import users_collection
        if users_collection.find_one({"username": field.data}):
            raise ValidationError('Username already taken. Please choose a different username.')

class FeedbackForm(FlaskForm):
    Breakfast = RadioField('Breakfast', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Lunch = RadioField('Lunch', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Dinner = RadioField('Dinner', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    submit = SubmitField('Feedback')
