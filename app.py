from myproject import app, mongo_db
from myproject.firstmeal import generatemeal, gender, cuisine, onClickGenerateMeal, feedbacklst
from flask import render_template, redirect, request, url_for, flash, abort, session, send_from_directory, jsonify
from datetime import datetime
from myproject.models import User
import os
from pymongo.errors import DuplicateKeyError

from flask_login import login_user, login_required, logout_user
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm, FeedbackForm
from werkzeug.security import generate_password_hash, check_password_hash

meals = []
breakfastlstarg = []
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'templates', 'images', 'icons'), 'favicon.ico')

@app.route('/chat', methods=['GET','POST'])
def chat():
    answer = None
    if request.method == 'POST':
        prompt = (request.form.get('prompt') or '').lower()
        
        # Health and nutrition queries
        if 'weight' in prompt and 'loss' in prompt:
            answer = 'Focus on high-protein, high-fiber meals, 500 kcal daily deficit, and 8k-10k steps. Consider strength training 2-3 times per week.'
        elif 'diabetes' in prompt:
            answer = 'Monitor carbohydrate intake, focus on low glycemic foods, and exercise regularly. Try 30 minutes of moderate cardio 5 times a week.'
        elif 'heart' in prompt:
            answer = 'Focus on heart-healthy foods, limit sodium, and include omega-3 rich foods. Start with walking 30 minutes daily and gradually increase intensity.'
        elif 'protein' in prompt:
            answer = 'Aim for 1.2–1.6 g protein per kg body weight daily, spaced across meals. Good sources include lean meats, fish, eggs, and legumes.'
        elif 'exercise' in prompt:
            answer = 'Start with 150 minutes of moderate exercise weekly. Include both cardio and strength training. Always warm up and cool down properly.'
        elif 'diet' in prompt:
            answer = 'Focus on whole foods, plenty of vegetables, lean proteins, and whole grains. Stay hydrated and maintain portion control.'
        else:
            answer = 'Try balanced plates: 50% vegetables, 25% lean protein, 25% whole grains. Hydrate well and stay active with regular exercise.'
    return render_template('chat.html', answer=answer)

@app.route('/recipes')
def recipes():
    sample_breakfast = list(mongo_db['breakfast'].find({}, {"_id": 0}).limit(5))
    sample_lunchdinner = list(mongo_db['lunchdinner'].find({}, {"_id": 0}).limit(5))
    return render_template('recipes.html', breakfast=sample_breakfast, lunchdinner=sample_lunchdinner)

@app.route('/recipe/<recipe_id>/review', methods=['POST'])
@login_required
def add_review(recipe_id):
    uid = session.get('userid')
    if not uid:
        return jsonify({'error': 'Please login first'}), 401
    
    user = User.find_by_id(uid)
    rating = int(request.form.get('rating'))
    comment = request.form.get('comment')
    
    user.add_recipe_review(recipe_id, rating, comment)
    return jsonify({'success': True})

@app.route('/workout-plans', methods=['GET', 'POST'])
@login_required
def workout_plans():
    uid = session.get('userid')
    if not uid:
        flash('Please login to access workout plans.')
        return redirect(url_for('login'))
    
    user = User.find_by_id(uid)
    
    if request.method == 'POST':
        name = request.form.get('name')
        exercises = request.form.getlist('exercises[]')
        if name and exercises:
            user.create_workout_plan(name, exercises)
            flash('Workout plan created successfully!')
    
    plans = user.get_workout_plans()
    return render_template('workout_plans.html', plans=plans)

@app.route('/workout-plan/<plan_id>/complete', methods=['POST'])
@login_required
def complete_workout(plan_id):
    uid = session.get('userid')
    if not uid:
        return jsonify({'error': 'Please login first'}), 401
    
    user = User.find_by_id(uid)
    user.complete_workout(plan_id)
    return jsonify({'success': True})

@app.route('/weight-tracker', methods=['GET', 'POST'])
@login_required
def weight_tracker():
    uid = session.get('userid')
    if not uid:
        flash('Please login to track your weight.')
        return redirect(url_for('login'))
    
    user = User.find_by_id(uid)
    if not user:
        flash('User not found. Please login again.')
        return redirect(url_for('logout'))

    if request.method == 'POST':
        weight = request.form.get('weight')
        if weight:
            try:
                user.add_weight_entry(float(weight))
                flash('Weight entry added successfully!')
            except ValueError:
                flash('Please enter a valid weight.')
        
    weight_history = user.get_weight_history()
    return render_template('weight_tracker.html', 
                         weight_history=weight_history,
                         current_weight=user.weight)

@app.route('/exercise')
@login_required
def exercise():
    uid = session.get('userid')
    if not uid:
        flash('Please login to view personalized exercise recommendations.')
        return redirect(url_for('login'))
    
    user = User.find_by_id(uid)
    if not user:
        flash('User not found. Please login again.')
        return redirect(url_for('logout'))
    
    # Personalize exercise recommendations based on health condition
    exercises = {
        'general': [
            {'name': 'Walking', 'duration': '30 minutes', 'frequency': '5 times per week', 'intensity': 'Moderate'},
            {'name': 'Swimming', 'duration': '30 minutes', 'frequency': '3 times per week', 'intensity': 'Moderate'},
            {'name': 'Strength Training', 'duration': '45 minutes', 'frequency': '2-3 times per week', 'intensity': 'Moderate'}
        ],
        'diabetes': [
            {'name': 'Brisk Walking', 'duration': '30 minutes', 'frequency': '5 times per week', 'intensity': 'Moderate'},
            {'name': 'Resistance Training', 'duration': '20-30 minutes', 'frequency': '2-3 times per week', 'intensity': 'Light to Moderate'},
            {'name': 'Stationary Cycling', 'duration': '20-30 minutes', 'frequency': '3 times per week', 'intensity': 'Moderate'}
        ],
        'heart_disease': [
            {'name': 'Light Walking', 'duration': '15-20 minutes', 'frequency': 'Daily', 'intensity': 'Light'},
            {'name': 'Swimming', 'duration': '20 minutes', 'frequency': '2-3 times per week', 'intensity': 'Light'},
            {'name': 'Seated Exercises', 'duration': '15 minutes', 'frequency': 'Daily', 'intensity': 'Very Light'}
        ],
        'high_cholesterol': [
            {'name': 'Brisk Walking', 'duration': '30 minutes', 'frequency': '5 times per week', 'intensity': 'Moderate'},
            {'name': 'Cycling', 'duration': '30 minutes', 'frequency': '3 times per week', 'intensity': 'Moderate'},
            {'name': 'Yoga', 'duration': '30 minutes', 'frequency': '2-3 times per week', 'intensity': 'Light'}
        ]
    }
    
    # Get recommended exercises based on health condition
    health_condition = user.health_issues if user.health_issues else 'general'
    recommended_exercises = exercises.get(health_condition, exercises['general'])
    
    return render_template('exercise.html', 
                         exercises=recommended_exercises, 
                         health_condition=health_condition,
                         user=user)

@app.route('/menu')
@login_required
def menu():
    uid = session.get('userid')
    if not uid:
        flash('Please login to view your menu.')
        return redirect(url_for('login'))
    user = User.find_by_id(uid)
    if not user:
        flash('User not found. Please login again.')
        return redirect(url_for('logout'))
    age = int(user.age)
    height = int(user.height)
    weight = int(user.weight)
    exercise = float(user.exercise)
    usergender = gender()
    usercuisine = cuisine()
    hasCancer = 'N'
    hasDiabetes = 'N'
    if user.health_issues == 'diabetes':
        hasDiabetes = 'Y'
    if user.health_issues in ['heart_disease', 'high_cholesterol']:
        hasCancer = 'Y'

    meals, breakfastlst = onClickGenerateMeal(uid,age,height,weight,usergender,exercise,hasCancer,hasDiabetes,usercuisine, breakfastlstarg)
    session['meals'] = meals
    session['breakfastlst'] = breakfastlst
    return render_template('menu.html', meals=meals)

@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'GET':
        form = FeedbackForm()
        meals = session.get('meals', [])
        return render_template('feedback.html', meals=meals, form=form)
    
    uid = session.get('userid')
    if not uid:
        flash('Please login to submit feedback.')
        return redirect(url_for('login'))
    user = User.find_by_id(uid)
    age = int(user.age)
    height = int(user.height)
    weight = int(user.weight)
    exercise = float(user.exercise)
    usergender = gender()
    usercuisine = cuisine()
    hasCancer = 'N'
    hasDiabetes = 'N'
    if user.health_issues == 'diabetes':
        hasDiabetes = 'Y'
    if user.health_issues in ['heart_disease', 'high_cholesterol']:
        hasCancer = 'Y'
    # meals, breakfastlst = generatemeal(21,176,69,1.2,'M','Y','Y','gujarat')
    # session['meals'] = meals
    # session['breakfastlst'] = breakfastlst
    # return render_template('menu.html', meals=meals)
    breakfastlstargs = session['breakfastlst']
    meals, breakfastlst = feedbacklst(uid,age,height,weight,usergender,exercise,hasCancer,hasDiabetes,usercuisine, breakfastlstargs)
    session['meals'] = meals
    session['breakfastlst'] = breakfastlst
    return redirect(url_for('menu'))


@app.route('/logout')
@login_required
def logout():
    session.pop('breakfastlst',None)
    session.pop('meals',None)

    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our MongoDB collection
        user = User.find_by_email(form.email.data)
        
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if  user is not None and user.check_password(form.password.data):
            #Log in the user
            session['userid'] = str(user._id)
            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('home')

            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    height=form.height.data,
                    age=form.age.data,
                    weight=form.weight.data,
                    blood=form.blood.data,
                    health_issues=form.health_issues.data,
                    exercise=form.exercise.data,
                    plan_period=form.plan_period.data,
                    food_type=form.food_type.data,
                    diet_pref=form.diet_pref.data,
                    password=form.password.data)
        try:
            user.save()
        except DuplicateKeyError:
            flash('Email or username already exists. Please use a different one.')
            return render_template('register.html', form=form)
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)