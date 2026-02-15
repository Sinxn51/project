"""
AI Agent Module for Diet Planner
This module handles personalized recommendations based on user gender and food preferences
"""
import random
from datetime import datetime

# Sample dataset structure - in production, this would be a larger dataset or database
FOOD_DATASET = {
    'male': {
        'vegetarian': [
            {'name': 'Protein-packed Lentil Bowl', 'calories': 450, 'protein': 25, 'carbs': 40, 'fat': 15},
            {'name': 'Quinoa Power Salad', 'calories': 380, 'protein': 18, 'carbs': 35, 'fat': 12},
            {'name': 'Chickpea and Vegetable Stir-fry', 'calories': 420, 'protein': 20, 'carbs': 38, 'fat': 14}
        ],
        'non-vegetarian': [
            {'name': 'Grilled Chicken with Vegetables', 'calories': 520, 'protein': 40, 'carbs': 25, 'fat': 18},
            {'name': 'Salmon with Quinoa', 'calories': 550, 'protein': 38, 'carbs': 30, 'fat': 22},
            {'name': 'Turkey and Vegetable Stir-fry', 'calories': 480, 'protein': 35, 'carbs': 28, 'fat': 16}
        ],
        'vegan': [
            {'name': 'Tofu and Vegetable Stir-fry', 'calories': 380, 'protein': 20, 'carbs': 35, 'fat': 12},
            {'name': 'Lentil and Spinach Curry', 'calories': 420, 'protein': 18, 'carbs': 40, 'fat': 14},
            {'name': 'Chickpea Buddha Bowl', 'calories': 400, 'protein': 16, 'carbs': 42, 'fat': 13}
        ]
    },
    'female': {
        'vegetarian': [
            {'name': 'Mediterranean Quinoa Bowl', 'calories': 380, 'protein': 18, 'carbs': 35, 'fat': 12},
            {'name': 'Spinach and Feta Wrap', 'calories': 350, 'protein': 15, 'carbs': 30, 'fat': 10},
            {'name': 'Greek Yogurt Parfait', 'calories': 320, 'protein': 20, 'carbs': 25, 'fat': 8}
        ],
        'non-vegetarian': [
            {'name': 'Baked Salmon with Asparagus', 'calories': 450, 'protein': 35, 'carbs': 20, 'fat': 18},
            {'name': 'Grilled Chicken Salad', 'calories': 420, 'protein': 30, 'carbs': 25, 'fat': 15},
            {'name': 'Turkey and Avocado Wrap', 'calories': 400, 'protein': 28, 'carbs': 30, 'fat': 14}
        ],
        'vegan': [
            {'name': 'Avocado and Chickpea Salad', 'calories': 350, 'protein': 15, 'carbs': 30, 'fat': 12},
            {'name': 'Quinoa and Roasted Vegetable Bowl', 'calories': 380, 'protein': 14, 'carbs': 35, 'fat': 13},
            {'name': 'Spinach and Berry Smoothie Bowl', 'calories': 320, 'protein': 12, 'carbs': 40, 'fat': 8}
        ]
    },
    'other': {
        'vegetarian': [
            {'name': 'Balanced Protein Bowl', 'calories': 420, 'protein': 22, 'carbs': 38, 'fat': 14},
            {'name': 'Mixed Grain Salad', 'calories': 380, 'protein': 18, 'carbs': 35, 'fat': 12},
            {'name': 'Vegetable and Hummus Wrap', 'calories': 400, 'protein': 16, 'carbs': 36, 'fat': 13}
        ],
        'non-vegetarian': [
            {'name': 'Balanced Protein Plate', 'calories': 480, 'protein': 35, 'carbs': 28, 'fat': 16},
            {'name': 'Mixed Seafood Bowl', 'calories': 450, 'protein': 32, 'carbs': 30, 'fat': 15},
            {'name': 'Lean Meat and Vegetable Stir-fry', 'calories': 420, 'protein': 30, 'carbs': 32, 'fat': 14}
        ],
        'vegan': [
            {'name': 'Complete Plant Protein Bowl', 'calories': 400, 'protein': 18, 'carbs': 38, 'fat': 13},
            {'name': 'Mixed Bean and Grain Salad', 'calories': 380, 'protein': 16, 'carbs': 40, 'fat': 12},
            {'name': 'Nutrient-Dense Smoothie Bowl', 'calories': 350, 'protein': 14, 'carbs': 42, 'fat': 10}
        ]
    }
}

def get_personalized_recommendations(gender, food_preference, health_issues=None):
    """
    Generate personalized food recommendations based on gender and food preference
    
    Args:
        gender (str): User's gender ('male', 'female', or 'other')
        food_preference (str): User's food preference ('vegetarian', 'non-vegetarian', or 'vegan')
        health_issues (list, optional): List of user's health issues for further personalization
        
    Returns:
        dict: Personalized meal recommendations
    """
    # Default values if input is not in our dataset
    if gender not in FOOD_DATASET:
        gender = 'other'
    
    if food_preference not in FOOD_DATASET[gender]:
        food_preference = 'vegetarian'
    
    # Get recommendations based on gender and food preference
    recommendations = FOOD_DATASET[gender][food_preference]
    
    # Further personalize based on health issues (simplified example)
    if health_issues:
        # In a real system, this would be more sophisticated
        if 'diabetes' in health_issues:
            # Adjust recommendations for diabetic users (lower carbs)
            for meal in recommendations:
                meal['carbs'] = max(15, meal['carbs'] - 10)
                meal['name'] = f"Low-Carb {meal['name']}"
        
        if 'hypertension' in health_issues:
            # Adjust recommendations for users with hypertension (lower sodium)
            for meal in recommendations:
                meal['name'] = f"Low-Sodium {meal['name']}"
    
    # Create a structured response
    breakfast = random.choice(recommendations)
    lunch = random.choice(recommendations)
    dinner = random.choice(recommendations)
    
    return {
        'breakfast': breakfast,
        'lunch': lunch,
        'dinner': dinner,
        'personalization_factors': {
            'gender': gender,
            'food_preference': food_preference,
            'health_issues': health_issues or []
        },
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def register_user_with_otp(email, gender, food_preference):
    """
    Register a new user with OTP verification
    
    Args:
        email (str): User's email for OTP delivery
        gender (str): User's gender
        food_preference (str): User's food preference
        
    Returns:
        bool: True if OTP was sent successfully, False otherwise
    """
    # Store user preferences in session or temporary storage
    # This would be implemented in the actual application
    
    # Previously this sent an OTP for verification. OTP was removed per project requirements.
    # For now, simply return True to indicate the registration step succeeded.
    # If you want to persist preferences, integrate with the application's user model here.
    return True

def validate_user_input(gender, food_preference):
    """
    Validate user input for gender and food preference
    
    Args:
        gender (str): User's gender input
        food_preference (str): User's food preference input
        
    Returns:
        tuple: (is_valid, error_message)
    """
    valid_genders = ['male', 'female', 'other']
    valid_preferences = ['vegetarian', 'non-vegetarian', 'vegan']
    
    if gender.lower() not in valid_genders:
        return False, f"Invalid gender. Please choose from: {', '.join(valid_genders)}"
    
    if food_preference.lower() not in valid_preferences:
        return False, f"Invalid food preference. Please choose from: {', '.join(valid_preferences)}"
    
    return True, "Input validated successfully"