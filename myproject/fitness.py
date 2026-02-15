from myproject import mongo_db
from flask import session
import pandas as pd
import numpy as np
from datetime import datetime
import random
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import joblib
import os
import pickle
from bson import ObjectId

# Collections
users_collection = mongo_db['users']
meal_preferences = mongo_db['meal_preferences']
fitness_goals = mongo_db['fitness_goals']
workout_logs = mongo_db['workout_logs']
meal_feedback = mongo_db['meal_feedback']

class AIRecommendationEngine:
    """AI-powered meal recommendation engine using collaborative filtering and content-based filtering"""
    
    def __init__(self):
        self.breakfast_data = self._load_meal_data('breakfast')
        self.lunch_dinner_data = self._load_meal_data('lunchdinner')
        self.user_preferences = {}
        self.seasonal_ingredients = self._get_seasonal_ingredients()
        
    def _load_meal_data(self, collection_name):
        """Load meal data from MongoDB collection"""
        try:
            data = list(mongo_db[collection_name].find({}))
            return data
        except Exception as e:
            print(f"Error loading meal data: {e}")
            return []
    
    def _get_seasonal_ingredients(self):
        """Get seasonal ingredients based on current month"""
        current_month = datetime.now().month
        
        seasonal_map = {
            # Winter (Dec-Feb)
            12: ['kale', 'brussels sprouts', 'sweet potatoes', 'winter squash', 'citrus'],
            1: ['kale', 'brussels sprouts', 'sweet potatoes', 'winter squash', 'citrus'],
            2: ['kale', 'brussels sprouts', 'sweet potatoes', 'winter squash', 'citrus'],
            
            # Spring (Mar-May)
            3: ['asparagus', 'peas', 'artichokes', 'spinach', 'strawberries'],
            4: ['asparagus', 'peas', 'artichokes', 'spinach', 'strawberries'],
            5: ['asparagus', 'peas', 'artichokes', 'spinach', 'strawberries'],
            
            # Summer (Jun-Aug)
            6: ['tomatoes', 'corn', 'zucchini', 'berries', 'watermelon'],
            7: ['tomatoes', 'corn', 'zucchini', 'berries', 'watermelon'],
            8: ['tomatoes', 'corn', 'zucchini', 'berries', 'watermelon'],
            
            # Fall (Sep-Nov)
            9: ['apples', 'pumpkin', 'butternut squash', 'brussels sprouts', 'pears'],
            10: ['apples', 'pumpkin', 'butternut squash', 'brussels sprouts', 'pears'],
            11: ['apples', 'pumpkin', 'butternut squash', 'brussels sprouts', 'pears']
        }
        
        return seasonal_map.get(current_month, ['vegetables', 'fruits', 'whole grains'])
    
    def _calculate_user_nutrition_needs(self, user):
        """Calculate user's nutritional needs based on profile"""
        # Basic BMR calculation using Harris-Benedict equation
        if user.get('gender', 'male').lower() == 'male':
            bmr = 88.362 + (13.397 * float(user['weight'])) + (4.799 * float(user['height'])) - (5.677 * float(user['age']))
        else:
            bmr = 447.593 + (9.247 * float(user['weight'])) + (3.098 * float(user['height'])) - (4.330 * float(user['age']))
        
        # Activity factor
        activity_factors = {
            '1.2': 1.2,  # Sedentary
            '1.375': 1.375,  # Light activity
            '1.55': 1.55,  # Moderate activity
            '1.725': 1.725,  # Very active
            '1.9': 1.9  # Extra active
        }
        
        activity_level = user.get('exercise', '1.2')
        tdee = bmr * activity_factors.get(activity_level, 1.2)
        
        # Adjust for health conditions
        if user.get('health_issues') == 'diabetes':
            carb_ratio = 0.4  # Lower carbs for diabetes
        elif user.get('health_issues') in ['heart_disease', 'high_cholesterol']:
            fat_ratio = 0.25  # Lower fat for heart issues
        else:
            carb_ratio = 0.5
            fat_ratio = 0.3
        
        protein_ratio = 0.2
        
        # Calculate macros
        daily_calories = tdee
        daily_carbs = (daily_calories * carb_ratio) / 4  # 4 calories per gram of carbs
        daily_protein = (daily_calories * protein_ratio) / 4  # 4 calories per gram of protein
        daily_fat = (daily_calories * fat_ratio) / 9  # 9 calories per gram of fat
        
        return {
            'daily_calories': daily_calories,
            'daily_carbs': daily_carbs,
            'daily_protein': daily_protein,
            'daily_fat': daily_fat
        }
    
    def _filter_meals_by_preferences(self, meals, user):
        """Filter meals based on user preferences"""
        filtered_meals = []
        
        diet_pref = user.get('diet_pref', 'none').lower()
        food_type = user.get('food_type', 'all').lower()
        
        for meal in meals:
            # Skip meals that don't match dietary preferences
            if diet_pref == 'vegetarian' and meal.get('vegetarian', 'N') != 'Y':
                continue
            if diet_pref == 'vegan' and meal.get('vegan', 'N') != 'Y':
                continue
            
            # Skip meals that don't match food type preferences
            if food_type == 'low_carb' and meal.get('carbs', 0) > 30:
                continue
            if food_type == 'high_protein' and meal.get('protein', 0) < 20:
                continue
            
            # Skip meals that don't match health conditions
            if user.get('health_issues') == 'diabetes' and meal.get('diabetes_friendly', 'N') != 'Y':
                continue
            if user.get('health_issues') in ['heart_disease', 'high_cholesterol'] and meal.get('heart_healthy', 'N') != 'Y':
                continue
            
            filtered_meals.append(meal)
        
        return filtered_meals if filtered_meals else meals  # Return original if all filtered out
    
    def _get_user_meal_history(self, user_id):
        """Get user's meal history and ratings"""
        try:
            history = list(meal_feedback.find({'user_id': ObjectId(user_id)}))
            return history
        except Exception as e:
            print(f"Error getting meal history: {e}")
            return []
    
    def _calculate_meal_similarity(self, meals):
        """Calculate similarity between meals based on nutritional content"""
        if not meals:
            return np.array([])
        
        # Extract nutritional features
        features = []
        for meal in meals:
            feature = [
                meal.get('calories', 0),
                meal.get('protein', 0),
                meal.get('carbs', 0),
                meal.get('fat', 0)
            ]
            features.append(feature)
        
        # Standardize features
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        # Calculate similarity
        similarity_matrix = cosine_similarity(features_scaled)
        return similarity_matrix
    
    def _add_seasonal_ingredients(self, meal):
        """Add seasonal ingredient recommendations to meal"""
        seasonal = random.sample(self.seasonal_ingredients, min(2, len(self.seasonal_ingredients)))
        meal['seasonal_ingredients'] = seasonal
        return meal
    
    def _add_substitution_options(self, meal):
        """Add substitution options for meal ingredients"""
        substitutions = {
            'rice': ['quinoa', 'cauliflower rice', 'brown rice'],
            'pasta': ['zucchini noodles', 'whole grain pasta', 'chickpea pasta'],
            'beef': ['turkey', 'plant-based meat', 'mushrooms'],
            'chicken': ['tofu', 'tempeh', 'chickpeas'],
            'cheese': ['nutritional yeast', 'vegan cheese', 'avocado'],
            'milk': ['almond milk', 'oat milk', 'coconut milk'],
            'sugar': ['honey', 'maple syrup', 'stevia'],
            'flour': ['almond flour', 'coconut flour', 'whole wheat flour']
        }
        
        meal_substitutions = {}
        for ingredient in meal.get('ingredients', '').lower().split(','):
            ingredient = ingredient.strip()
            for key in substitutions:
                if key in ingredient:
                    meal_substitutions[ingredient] = random.sample(substitutions[key], 1)[0]
        
        meal['substitution_options'] = meal_substitutions
        return meal
    
    def generate_meal_recommendations(self, user_id):
        """Generate personalized meal recommendations for a user"""
        try:
            # Get user data
            user_data = users_collection.find_one({"_id": ObjectId(user_id)})
            if not user_data:
                return []
            
            # Calculate nutritional needs
            nutrition_needs = self._calculate_user_nutrition_needs(user_data)
            
            # Filter meals by preferences
            breakfast_options = self._filter_meals_by_preferences(self.breakfast_data, user_data)
            lunch_dinner_options = self._filter_meals_by_preferences(self.lunch_dinner_data, user_data)
            
            # Get user meal history and preferences
            meal_history = self._get_user_meal_history(user_id)
            
            # Calculate meal similarity
            breakfast_similarity = self._calculate_meal_similarity(breakfast_options)
            lunch_dinner_similarity = self._calculate_meal_similarity(lunch_dinner_options)
            
            # Select meals based on user preferences and nutritional needs
            recommended_meals = []
            
            # Breakfast
            if breakfast_options:
                breakfast = random.choice(breakfast_options)
                breakfast = self._add_seasonal_ingredients(breakfast)
                breakfast = self._add_substitution_options(breakfast)
                breakfast['meal_type'] = 'breakfast'
                recommended_meals.append(breakfast)
            
            # Lunch
            if lunch_dinner_options:
                lunch = random.choice(lunch_dinner_options)
                lunch = self._add_seasonal_ingredients(lunch)
                lunch = self._add_substitution_options(lunch)
                lunch['meal_type'] = 'lunch'
                recommended_meals.append(lunch)
            
            # Dinner
            if lunch_dinner_options:
                # Ensure dinner is different from lunch
                dinner_options = [meal for meal in lunch_dinner_options if meal.get('name') != recommended_meals[-1].get('name')]
                if not dinner_options:
                    dinner_options = lunch_dinner_options
                
                dinner = random.choice(dinner_options)
                dinner = self._add_seasonal_ingredients(dinner)
                dinner = self._add_substitution_options(dinner)
                dinner['meal_type'] = 'dinner'
                recommended_meals.append(dinner)
            
            # Store recommendations in session for persistence
            session['meal_recommendations'] = recommended_meals
            
            return recommended_meals
            
        except Exception as e:
            print(f"Error generating meal recommendations: {e}")
            return []
    
    def update_preferences_from_feedback(self, user_id, meal_id, rating, feedback_text):
        """Update user preferences based on meal feedback"""
        try:
            feedback_data = {
                'user_id': ObjectId(user_id),
                'meal_id': meal_id,
                'rating': rating,
                'feedback': feedback_text,
                'date': datetime.utcnow()
            }
            
            meal_feedback.insert_one(feedback_data)
            return True
        except Exception as e:
            print(f"Error updating preferences: {e}")
            return False


class FitnessTracker:
    """Comprehensive fitness tracking with analytics and goal setting"""
    
    def __init__(self):
        self.exercise_data = self._load_exercise_data()
        self.calorie_burn_rates = self._load_calorie_burn_rates()
    
    def _load_exercise_data(self):
        """Load exercise data with muscle groups and difficulty levels"""
        exercises = {
            'cardio': [
                {'name': 'Running', 'difficulty': 'medium', 'muscle_groups': ['legs', 'cardiovascular']},
                {'name': 'Cycling', 'difficulty': 'medium', 'muscle_groups': ['legs', 'cardiovascular']},
                {'name': 'Swimming', 'difficulty': 'medium', 'muscle_groups': ['full body', 'cardiovascular']},
                {'name': 'Jump Rope', 'difficulty': 'medium', 'muscle_groups': ['legs', 'cardiovascular']},
                {'name': 'Elliptical', 'difficulty': 'easy', 'muscle_groups': ['legs', 'cardiovascular']}
            ],
            'strength': [
                {'name': 'Push-ups', 'difficulty': 'medium', 'muscle_groups': ['chest', 'triceps', 'shoulders']},
                {'name': 'Pull-ups', 'difficulty': 'hard', 'muscle_groups': ['back', 'biceps']},
                {'name': 'Squats', 'difficulty': 'medium', 'muscle_groups': ['legs', 'glutes']},
                {'name': 'Lunges', 'difficulty': 'medium', 'muscle_groups': ['legs', 'glutes']},
                {'name': 'Planks', 'difficulty': 'medium', 'muscle_groups': ['core']}
            ],
            'flexibility': [
                {'name': 'Yoga', 'difficulty': 'varies', 'muscle_groups': ['full body', 'flexibility']},
                {'name': 'Stretching', 'difficulty': 'easy', 'muscle_groups': ['full body', 'flexibility']},
                {'name': 'Pilates', 'difficulty': 'medium', 'muscle_groups': ['core', 'flexibility']}
            ]
        }
        return exercises
    
    def _load_calorie_burn_rates(self):
        """Load estimated calorie burn rates for different exercises"""
        # Calories burned per minute for a 70kg person
        calorie_burn = {
            'Running': 11.4,
            'Cycling': 8.5,
            'Swimming': 10.0,
            'Jump Rope': 12.0,
            'Elliptical': 8.0,
            'Push-ups': 7.0,
            'Pull-ups': 8.0,
            'Squats': 8.0,
            'Lunges': 6.0,
            'Planks': 5.0,
            'Yoga': 4.0,
            'Stretching': 2.5,
            'Pilates': 5.0
        }
        return calorie_burn
    
    def calculate_calories_burned(self, exercise_name, duration_minutes, user_weight):
        """Calculate calories burned for a specific exercise"""
        base_burn_rate = self.calorie_burn_rates.get(exercise_name, 5.0)
        weight_factor = user_weight / 70.0  # Adjust for user weight (baseline is 70kg)
        return base_burn_rate * duration_minutes * weight_factor
    
    def log_workout(self, user_id, exercise_name, duration_minutes, intensity, notes=None):
        """Log a workout for a user"""
        try:
            # Get user data for calorie calculation
            user_data = users_collection.find_one({"_id": ObjectId(user_id)})
            if not user_data:
                return False
            
            user_weight = float(user_data.get('weight', 70))
            
            # Calculate calories burned
            calories_burned = self.calculate_calories_burned(exercise_name, duration_minutes, user_weight)
            
            # Create workout log entry
            workout_data = {
                'user_id': ObjectId(user_id),
                'exercise': exercise_name,
                'duration': duration_minutes,
                'intensity': intensity,
                'calories_burned': calories_burned,
                'notes': notes,
                'date': datetime.utcnow()
            }
            
            # Insert into database
            workout_logs.insert_one(workout_data)
            
            # Check if any fitness goals have been achieved
            self._check_goal_achievements(user_id)
            
            return True
        except Exception as e:
            print(f"Error logging workout: {e}")
            return False
    
    def get_workout_history(self, user_id, days=30):
        """Get workout history for a user"""
        try:
            # Calculate date range
            end_date = datetime.utcnow()
            start_date = end_date - pd.Timedelta(days=days)
            
            # Query database
            history = list(workout_logs.find({
                'user_id': ObjectId(user_id),
                'date': {'$gte': start_date, '$lte': end_date}
            }).sort('date', -1))
            
            return history
        except Exception as e:
            print(f"Error getting workout history: {e}")
            return []
    
    def get_workout_analytics(self, user_id, days=30):
        """Get workout analytics for a user"""
        try:
            # Get workout history
            history = self.get_workout_history(user_id, days)
            
            if not history:
                return {
                    'total_workouts': 0,
                    'total_duration': 0,
                    'total_calories': 0,
                    'exercise_breakdown': {},
                    'streak': 0
                }
            
            # Calculate analytics
            total_workouts = len(history)
            total_duration = sum(workout.get('duration', 0) for workout in history)
            total_calories = sum(workout.get('calories_burned', 0) for workout in history)
            
            # Exercise breakdown
            exercise_breakdown = {}
            for workout in history:
                exercise = workout.get('exercise')
                if exercise in exercise_breakdown:
                    exercise_breakdown[exercise] += 1
                else:
                    exercise_breakdown[exercise] = 1
            
            # Calculate streak
            streak = self._calculate_workout_streak(history)
            
            return {
                'total_workouts': total_workouts,
                'total_duration': total_duration,
                'total_calories': total_calories,
                'exercise_breakdown': exercise_breakdown,
                'streak': streak
            }
        except Exception as e:
            print(f"Error getting workout analytics: {e}")
            return {}
    
    def _calculate_workout_streak(self, workout_history):
        """Calculate current workout streak in days"""
        if not workout_history:
            return 0
        
        # Convert workout dates to days only
        workout_dates = [workout.get('date').date() for workout in workout_history]
        unique_dates = sorted(set(workout_dates), reverse=True)
        
        if not unique_dates:
            return 0
        
        # Calculate streak
        streak = 1
        today = datetime.utcnow().date()
        
        # Check if worked out today
        if unique_dates[0] != today:
            # Check if worked out yesterday
            yesterday = today - pd.Timedelta(days=1)
            if unique_dates[0] != yesterday:
                return 0  # Streak broken
        
        # Count consecutive days
        for i in range(len(unique_dates) - 1):
            current_date = unique_dates[i]
            next_date = unique_dates[i + 1]
            
            if (current_date - next_date).days == 1:
                streak += 1
            else:
                break
        
        return streak
    
    def set_fitness_goal(self, user_id, goal_type, target_value, deadline=None):
        """Set a fitness goal for a user"""
        try:
            if deadline:
                deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
            else:
                # Default to 30 days from now
                deadline_date = datetime.utcnow() + pd.Timedelta(days=30)
            
            goal_data = {
                'user_id': ObjectId(user_id),
                'goal_type': goal_type,  # e.g., 'weight_loss', 'workout_frequency', 'calories_burned'
                'target_value': float(target_value),
                'start_date': datetime.utcnow(),
                'deadline': deadline_date,
                'completed': False,
                'progress': 0.0
            }
            
            # Insert into database
            fitness_goals.insert_one(goal_data)
            return True
        except Exception as e:
            print(f"Error setting fitness goal: {e}")
            return False
    
    def get_fitness_goals(self, user_id):
        """Get fitness goals for a user"""
        try:
            goals = list(fitness_goals.find({
                'user_id': ObjectId(user_id)
            }).sort('deadline', 1))
            
            # Update progress for each goal
            for goal in goals:
                goal['progress'] = self._calculate_goal_progress(goal)
            
            return goals
        except Exception as e:
            print(f"Error getting fitness goals: {e}")
            return []
    
    def _calculate_goal_progress(self, goal):
        """Calculate progress towards a fitness goal"""
        try:
            goal_type = goal.get('goal_type')
            target_value = goal.get('target_value')
            user_id = goal.get('user_id')
            start_date = goal.get('start_date')
            
            if goal_type == 'weight_loss':
                # Get starting weight and current weight
                user_data = users_collection.find_one({"_id": user_id})
                if not user_data:
                    return 0.0
                
                current_weight = float(user_data.get('weight', 0))
                
                # Get weight at start date
                start_weight_record = weight_history.find_one({
                    'user_id': user_id,
                    'date': {'$lte': start_date}
                }, sort=[('date', -1)])
                
                if not start_weight_record:
                    return 0.0
                
                start_weight = float(start_weight_record.get('weight', current_weight))
                weight_to_lose = start_weight - target_value
                
                if weight_to_lose <= 0:
                    return 0.0
                
                weight_lost = start_weight - current_weight
                progress = min(100, (weight_lost / weight_to_lose) * 100)
                return progress
            
            elif goal_type == 'workout_frequency':
                # Count workouts since start date
                workout_count = workout_logs.count_documents({
                    'user_id': user_id,
                    'date': {'$gte': start_date}
                })
                
                progress = min(100, (workout_count / target_value) * 100)
                return progress
            
            elif goal_type == 'calories_burned':
                # Sum calories burned since start date
                workouts = workout_logs.find({
                    'user_id': user_id,
                    'date': {'$gte': start_date}
                })
                
                total_calories = sum(workout.get('calories_burned', 0) for workout in workouts)
                progress = min(100, (total_calories / target_value) * 100)
                return progress
            
            return 0.0
        except Exception as e:
            print(f"Error calculating goal progress: {e}")
            return 0.0
    
    def _check_goal_achievements(self, user_id):
        """Check if any fitness goals have been achieved"""
        try:
            goals = fitness_goals.find({
                'user_id': ObjectId(user_id),
                'completed': False
            })
            
            for goal in goals:
                progress = self._calculate_goal_progress(goal)
                
                # Update progress in database
                fitness_goals.update_one(
                    {'_id': goal.get('_id')},
                    {'$set': {'progress': progress}}
                )
                
                # Check if goal is completed
                if progress >= 100:
                    fitness_goals.update_one(
                        {'_id': goal.get('_id')},
                        {'$set': {'completed': True, 'completion_date': datetime.utcnow()}}
                    )
        except Exception as e:
            print(f"Error checking goal achievements: {e}")
    
    def generate_workout_plan(self, user_id, fitness_level='beginner', focus_areas=None, days_per_week=3):
        """Generate a personalized workout plan based on user profile"""
        try:
            # Get user data
            user_data = users_collection.find_one({"_id": ObjectId(user_id)})
            if not user_data:
                return []
            
            # Default focus areas if none provided
            if not focus_areas:
                focus_areas = ['full body']
            
            # Adjust difficulty based on fitness level
            difficulty_map = {
                'beginner': ['easy'],
                'intermediate': ['easy', 'medium'],
                'advanced': ['medium', 'hard']
            }
            
            allowed_difficulties = difficulty_map.get(fitness_level, ['easy', 'medium'])
            
            # Filter exercises by difficulty and focus areas
            suitable_exercises = []
            for category, exercises in self.exercise_data.items():
                for exercise in exercises:
                    if exercise.get('difficulty') in allowed_difficulties or exercise.get('difficulty') == 'varies':
                        # Check if exercise targets any of the focus areas
                        if any(area in exercise.get('muscle_groups', []) for area in focus_areas) or 'full body' in exercise.get('muscle_groups', []):
                            suitable_exercises.append({**exercise, 'category': category})
            
            if not suitable_exercises:
                return []
            
            # Create workout plan
            workout_plan = []
            
            # Create workouts for each day
            for day in range(1, days_per_week + 1):
                # Mix of cardio and strength for each workout
                day_exercises = []
                
                # Add 1-2 cardio exercises
                cardio_options = [ex for ex in suitable_exercises if ex.get('category') == 'cardio']
                if cardio_options:
                    day_exercises.append(random.choice(cardio_options))
                
                # Add 2-3 strength exercises
                strength_options = [ex for ex in suitable_exercises if ex.get('category') == 'strength']
                if strength_options:
                    day_exercises.extend(random.sample(strength_options, min(3, len(strength_options))))
                
                # Add 1 flexibility exercise
                flexibility_options = [ex for ex in suitable_exercises if ex.get('category') == 'flexibility']
                if flexibility_options:
                    day_exercises.append(random.choice(flexibility_options))
                
                # Create workout for this day
                workout = {
                    'day': day,
                    'exercises': day_exercises,
                    'duration': 30 if fitness_level == 'beginner' else (45 if fitness_level == 'intermediate' else 60)
                }
                
                workout_plan.append(workout)
            
            return workout_plan
        except Exception as e:
            print(f"Error generating workout plan: {e}")
            return []


# Initialize the recommendation engine and fitness tracker
recommendation_engine = AIRecommendationEngine()
fitness_tracker = FitnessTracker()

# Functions to be used in routes
def get_meal_recommendations(user_id):
    """Get meal recommendations for a user"""
    # Check if recommendations exist in session
    if 'meal_recommendations' in session:
        return session['meal_recommendations']
    
    # Generate new recommendations
    return recommendation_engine.generate_meal_recommendations(user_id)

def submit_meal_feedback(user_id, meal_id, rating, feedback_text):
    """Submit feedback for a meal"""
    return recommendation_engine.update_preferences_from_feedback(user_id, meal_id, rating, feedback_text)

def log_user_workout(user_id, exercise_name, duration_minutes, intensity, notes=None):
    """Log a workout for a user"""
    return fitness_tracker.log_workout(user_id, exercise_name, duration_minutes, intensity, notes)

def get_user_workout_analytics(user_id, days=30):
    """Get workout analytics for a user"""
    return fitness_tracker.get_workout_analytics(user_id, days)

def set_user_fitness_goal(user_id, goal_type, target_value, deadline=None):
    """Set a fitness goal for a user"""
    return fitness_tracker.set_fitness_goal(user_id, goal_type, target_value, deadline)

def get_user_fitness_goals(user_id):
    """Get fitness goals for a user"""
    return fitness_tracker.get_fitness_goals(user_id)

def generate_user_workout_plan(user_id, fitness_level='beginner', focus_areas=None, days_per_week=3):
    """Generate a workout plan for a user"""
    return fitness_tracker.generate_workout_plan(user_id, fitness_level, focus_areas, days_per_week)