from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from myproject.models import User

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField("Log in")

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message="Passwords not matching!")])
    pass_confirm=PasswordField('Confirm Password',validators=[DataRequired()])
    height=StringField('Height (cm)',validators=[DataRequired()])
    age=StringField('Age',validators=[DataRequired()])
    weight=StringField('Weight',validators=[DataRequired()])
    blood=SelectField('Blood Type',[DataRequired()], choices=[('A', 'A'),('B', 'B'),('O', 'O'),('AB', 'AB')])
    health_issues=SelectField('Health Conditions',[DataRequired()], choices=[('none', 'No Health Issues'),('diabetes', 'Diabetes'),('hypertension', 'High Blood Pressure'),('heart_disease', 'Heart Disease'),('high_cholesterol', 'High Cholesterol'),('obesity', 'Obesity'),('underweight', 'Underweight'),('digestive_issues', 'Digestive Issues'),('food_allergies', 'Food Allergies'),('other', 'Other')])
    plan_period=SelectField('Plan Period',[DataRequired()], choices=[('daily', 'Daily'),('weekly', 'Weekly')])
    exercise=SelectField('Exercise',[DataRequired()], choices=[('1.2', 'Little or no exercise'),('1.375', 'Lightly active'),('1.55', 'Moderately active'),('1.725', 'Very active'),('1.9', 'Extra active')])
    food_type=SelectField('Type of food',[DataRequired()], choices=[('vegan', 'Vegan'),('vegetarian', 'Vegerarian'),('non-vegetarian', 'Non-Vegerarian'),('eggitarian', 'eggitarian')])
    diet_pref=SelectField('Diet preference',[DataRequired()], choices=[('balanced', 'Balanced'),('low carbohydrates', 'low carbohydrates'),('low fats', 'low fats')])
    submit=SubmitField('Register!')

    def validate_email(self, field):
        if User.find_by_email(field.data):
            raise ValidationError('Email already exists')

    def validate_username(self, field):
        from myproject import users_collection
        if users_collection.find_one({"username": field.data}):
            raise ValidationError('Username already exists')

class FeedbackForm(FlaskForm):
    Breakfast = RadioField('Breakfast', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Lunch = RadioField('Lunch', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Dinner = RadioField('Dinner', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    submit = SubmitField('Feedback')
