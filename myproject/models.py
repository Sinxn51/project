from myproject import login_manager, users_collection, mongo_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from bson import ObjectId
from datetime import datetime

# Collections
weight_history = mongo_db['weight_history']
recipe_reviews = mongo_db['recipe_reviews']
workout_plans = mongo_db['workout_plans']

# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()

# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User.from_dict(user_data)
    return None

class User(UserMixin):
    def __init__(self, email, username, age, height, weight, blood, health_issues, exercise, diet_pref, plan_period, food_type, password):
        self.email = email
        self.username = username
        self.age = age
        self.height = height
        self.weight = weight
        self.blood = blood
        self.health_issues = health_issues
        self.exercise = exercise
        self.diet_pref = diet_pref
        self.plan_period = plan_period
        self.food_type = food_type
        self.password_hash = generate_password_hash(password)
        self.created_at = datetime.utcnow()

    def get_id(self):
        return str(self._id)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_weight_entry(self, weight, date=None):
        if date is None:
            date = datetime.utcnow()
        weight_entry = {
            'user_id': ObjectId(self.get_id()),
            'weight': float(weight),
            'date': date
        }
        weight_history.insert_one(weight_entry)
        self.weight = float(weight)  # Update current weight
        self.save()

    def get_weight_history(self):
        history = weight_history.find(
            {'user_id': ObjectId(self.get_id())},
            {'weight': 1, 'date': 1, '_id': 0}
        ).sort('date', -1)
        return list(history)

    # Recipe Rating and Reviews
    def add_recipe_review(self, recipe_id, rating, comment):
        review = {
            'user_id': ObjectId(self.get_id()),
            'recipe_id': recipe_id,
            'rating': rating,
            'comment': comment,
            'helpful_votes': 0,
            'date': datetime.utcnow()
        }
        recipe_reviews.insert_one(review)
        self._check_review_achievements()

    def get_recipe_reviews(self, recipe_id=None):
        query = {'user_id': ObjectId(self.get_id())}
        if recipe_id:
            query['recipe_id'] = recipe_id
        return list(recipe_reviews.find(query))

    # Workout Plans
    def create_workout_plan(self, name, exercises):
        plan = {
            'user_id': ObjectId(self.get_id()),
            'name': name,
            'exercises': exercises,
            'created_at': datetime.utcnow(),
            'completed_workouts': 0
        }
        workout_plans.insert_one(plan)

    def complete_workout(self, plan_id):
        workout_plans.update_one(
            {'_id': ObjectId(plan_id)},
            {'$inc': {'completed_workouts': 1}}
        )
        self._check_workout_achievements()

    def get_workout_plans(self):
        return list(workout_plans.find({'user_id': ObjectId(self.get_id())}))

    def save(self):
        user_dict = {
            'email': self.email,
            'username': self.username,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'blood': self.blood,
            'health_issues': self.health_issues,
            'exercise': self.exercise,
            'diet_pref': self.diet_pref,
            'plan_period': self.plan_period,
            'food_type': self.food_type,
            'password_hash': self.password_hash,
            'created_at': self.created_at
        }
        result = users_collection.insert_one(user_dict)
        self._id = result.inserted_id
        return self

    @classmethod
    def from_dict(cls, data):
        user = cls.__new__(cls)
        user._id = data['_id']
        user.email = data['email']
        user.username = data['username']
        user.age = data['age']
        user.height = data['height']
        user.weight = data['weight']
        user.blood = data['blood']
        user.health_issues = data.get('health_issues', 'none')
        user.exercise = data['exercise']
        user.diet_pref = data['diet_pref']
        user.plan_period = data['plan_period']
        user.food_type = data['food_type']
        user.password_hash = data['password_hash']
        user.created_at = data.get('created_at', datetime.utcnow())
        return user

    @classmethod
    def find_by_email(cls, email):
        user_data = users_collection.find_one({"email": email})
        if user_data:
            return cls.from_dict(user_data)
        return None

    @classmethod
    def find_by_id(cls, user_id):
        user_data = users_collection.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return cls.from_dict(user_data)
        return None
