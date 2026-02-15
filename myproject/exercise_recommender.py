"""
Personalized Exercise Recommendation System
Based on health conditions, weight, gender, and fitness level
"""

def calculate_bmi(weight, height):
    """Calculate BMI from weight (kg) and height (cm)"""
    height_m = float(height) / 100
    return float(weight) / (height_m ** 2)

def get_bmi_category(bmi):
    """Get BMI category"""
    if bmi < 18.5:
        return 'underweight'
    elif bmi < 25:
        return 'normal'
    elif bmi < 30:
        return 'overweight'
    else:
        return 'obese'

def get_personalized_exercises(user):
    """
    Get personalized exercise recommendations based on user profile
    """
    # Calculate BMI
    bmi = calculate_bmi(user.weight, user.height)
    bmi_category = get_bmi_category(bmi)
    
    # Get fitness level from exercise multiplier
    exercise_level = float(user.exercise)
    if exercise_level <= 1.2:
        fitness_level = 'beginner'
    elif exercise_level <= 1.55:
        fitness_level = 'intermediate'
    else:
        fitness_level = 'advanced'
    
    # Base recommendations
    recommendations = {
        'summary': {
            'bmi': round(bmi, 1),
            'bmi_category': bmi_category,
            'fitness_level': fitness_level,
            'health_condition': user.health_issues
        },
        'cardio': [],
        'strength': [],
        'flexibility': [],
        'precautions': []
    }
    
    # Health condition specific recommendations
    if user.health_issues == 'diabetes':
        recommendations['cardio'] = [
            {
                'name': 'Brisk Walking',
                'duration': '30 minutes',
                'frequency': '5 times per week',
                'intensity': 'Moderate',
                'benefits': 'Helps control blood sugar, improves insulin sensitivity',
                'tips': 'Check blood sugar before and after exercise'
            },
            {
                'name': 'Stationary Cycling',
                'duration': '20-30 minutes',
                'frequency': '3-4 times per week',
                'intensity': 'Moderate',
                'benefits': 'Low-impact cardio, good for joint health',
                'tips': 'Maintain steady pace, avoid high intensity initially'
            },
            {
                'name': 'Swimming',
                'duration': '30 minutes',
                'frequency': '2-3 times per week',
                'intensity': 'Light to Moderate',
                'benefits': 'Full body workout, easy on joints',
                'tips': 'Great for overall fitness without stress on feet'
            }
        ]
        recommendations['strength'] = [
            {
                'name': 'Resistance Band Training',
                'duration': '20-30 minutes',
                'frequency': '2-3 times per week',
                'intensity': 'Light to Moderate',
                'benefits': 'Builds muscle, improves glucose uptake',
                'tips': 'Focus on major muscle groups, 2-3 sets of 10-15 reps'
            },
            {
                'name': 'Bodyweight Exercises',
                'duration': '15-20 minutes',
                'frequency': '2-3 times per week',
                'intensity': 'Moderate',
                'benefits': 'Increases muscle mass, boosts metabolism',
                'tips': 'Include squats, push-ups, lunges - modified as needed'
            }
        ]
        recommendations['precautions'] = [
            'Monitor blood sugar before, during, and after exercise',
            'Carry fast-acting carbs (glucose tablets, juice)',
            'Stay well hydrated',
            'Wear proper footwear to prevent foot injuries',
            'Start slowly and gradually increase intensity'
        ]
    
    elif user.health_issues in ['heart_disease', 'hypertension']:
        recommendations['cardio'] = [
            {
                'name': 'Gentle Walking',
                'duration': '15-20 minutes',
                'frequency': 'Daily',
                'intensity': 'Light',
                'benefits': 'Improves cardiovascular health, lowers blood pressure',
                'tips': 'Start slow, gradually increase duration'
            },
            {
                'name': 'Water Aerobics',
                'duration': '20-30 minutes',
                'frequency': '2-3 times per week',
                'intensity': 'Light',
                'benefits': 'Low-impact, reduces stress on heart',
                'tips': 'Water provides natural resistance without strain'
            },
            {
                'name': 'Tai Chi',
                'duration': '30 minutes',
                'frequency': '3 times per week',
                'intensity': 'Very Light',
                'benefits': 'Reduces stress, improves balance and flexibility',
                'tips': 'Gentle movements, focus on breathing'
            }
        ]
        recommendations['strength'] = [
            {
                'name': 'Light Dumbbell Exercises',
                'duration': '15-20 minutes',
                'frequency': '2 times per week',
                'intensity': 'Light',
                'benefits': 'Maintains muscle mass, supports heart health',
                'tips': 'Use light weights (2-5 lbs), avoid straining'
            }
        ]
        recommendations['precautions'] = [
            'Get medical clearance before starting',
            'Avoid holding breath during exercises',
            'Stop if you feel chest pain, dizziness, or shortness of breath',
            'Keep intensity low to moderate',
            'Monitor heart rate - stay within safe zone'
        ]
    
    elif user.health_issues == 'high_cholesterol':
        recommendations['cardio'] = [
            {
                'name': 'Brisk Walking',
                'duration': '30-45 minutes',
                'frequency': '5 times per week',
                'intensity': 'Moderate',
                'benefits': 'Raises HDL (good cholesterol), lowers LDL',
                'tips': 'Aim for 10,000 steps daily'
            },
            {
                'name': 'Cycling',
                'duration': '30 minutes',
                'frequency': '3-4 times per week',
                'intensity': 'Moderate',
                'benefits': 'Improves cardiovascular fitness',
                'tips': 'Outdoor or stationary bike both work well'
            },
            {
                'name': 'Swimming',
                'duration': '30 minutes',
                'frequency': '3 times per week',
                'intensity': 'Moderate',
                'benefits': 'Full body cardio, joint-friendly',
                'tips': 'Mix different strokes for variety'
            }
        ]
        recommendations['strength'] = [
            {
                'name': 'Circuit Training',
                'duration': '30 minutes',
                'frequency': '2-3 times per week',
                'intensity': 'Moderate',
                'benefits': 'Builds muscle, improves metabolism',
                'tips': 'Combine cardio and strength in circuits'
            }
        ]
        recommendations['flexibility'] = [
            {
                'name': 'Yoga',
                'duration': '30 minutes',
                'frequency': '2-3 times per week',
                'intensity': 'Light',
                'benefits': 'Reduces stress, improves flexibility',
                'tips': 'Focus on gentle, flowing movements'
            }
        ]
        recommendations['precautions'] = [
            'Combine with heart-healthy diet',
            'Stay consistent with exercise routine',
            'Gradually increase intensity over time'
        ]
    
    elif user.health_issues in ['obesity', 'overweight'] or bmi_category in ['overweight', 'obese']:
        recommendations['cardio'] = [
            {
                'name': 'Walking',
                'duration': '30-45 minutes',
                'frequency': '5-6 times per week',
                'intensity': 'Moderate',
                'benefits': 'Burns calories, low-impact on joints',
                'tips': 'Start with 15 minutes, gradually increase'
            },
            {
                'name': 'Swimming',
                'duration': '30 minutes',
                'frequency': '3 times per week',
                'intensity': 'Moderate',
                'benefits': 'Full body workout, easy on joints',
                'tips': 'Water supports body weight, reduces injury risk'
            },
            {
                'name': 'Elliptical Trainer',
                'duration': '20-30 minutes',
                'frequency': '3-4 times per week',
                'intensity': 'Moderate',
                'benefits': 'Low-impact cardio, burns calories',
                'tips': 'Easier on knees than running'
            }
        ]
        recommendations['strength'] = [
            {
                'name': 'Bodyweight Exercises',
                'duration': '20 minutes',
                'frequency': '3 times per week',
                'intensity': 'Moderate',
                'benefits': 'Builds muscle, boosts metabolism',
                'tips': 'Modified push-ups, squats, planks'
            },
            {
                'name': 'Resistance Training',
                'duration': '30 minutes',
                'frequency': '2-3 times per week',
                'intensity': 'Moderate',
                'benefits': 'Increases lean muscle mass',
                'tips': 'Focus on compound movements'
            }
        ]
        recommendations['precautions'] = [
            'Choose low-impact exercises to protect joints',
            'Focus on consistency over intensity',
            'Combine with calorie-controlled diet',
            'Stay hydrated',
            'Listen to your body, rest when needed'
        ]
    
    elif user.health_issues == 'underweight' or bmi_category == 'underweight':
        recommendations['strength'] = [
            {
                'name': 'Weight Training',
                'duration': '45 minutes',
                'frequency': '4 times per week',
                'intensity': 'Moderate to High',
                'benefits': 'Builds muscle mass, increases strength',
                'tips': 'Focus on compound lifts: squats, deadlifts, bench press'
            },
            {
                'name': 'Bodyweight Strength',
                'duration': '30 minutes',
                'frequency': '3 times per week',
                'intensity': 'Moderate',
                'benefits': 'Builds functional strength',
                'tips': 'Push-ups, pull-ups, dips, squats'
            }
        ]
        recommendations['cardio'] = [
            {
                'name': 'Light Cardio',
                'duration': '20 minutes',
                'frequency': '2-3 times per week',
                'intensity': 'Light',
                'benefits': 'Maintains cardiovascular health',
                'tips': 'Keep cardio minimal to preserve calories for muscle building'
            }
        ]
        recommendations['precautions'] = [
            'Focus on strength training over cardio',
            'Eat calorie surplus with high protein',
            'Get adequate rest between workouts',
            'Consider working with a trainer'
        ]
    
    else:  # No specific health issues or normal weight
        if fitness_level == 'beginner':
            recommendations['cardio'] = [
                {
                    'name': 'Walking',
                    'duration': '30 minutes',
                    'frequency': '5 times per week',
                    'intensity': 'Moderate',
                    'benefits': 'Builds cardiovascular endurance',
                    'tips': 'Start your fitness journey with consistency'
                },
                {
                    'name': 'Cycling',
                    'duration': '20-30 minutes',
                    'frequency': '3 times per week',
                    'intensity': 'Light to Moderate',
                    'benefits': 'Low-impact cardio',
                    'tips': 'Great alternative to walking'
                }
            ]
            recommendations['strength'] = [
                {
                    'name': 'Bodyweight Exercises',
                    'duration': '20 minutes',
                    'frequency': '2-3 times per week',
                    'intensity': 'Light',
                    'benefits': 'Builds foundational strength',
                    'tips': 'Start with modified versions, focus on form'
                }
            ]
            recommendations['flexibility'] = [
                {
                    'name': 'Stretching',
                    'duration': '10-15 minutes',
                    'frequency': 'Daily',
                    'intensity': 'Light',
                    'benefits': 'Improves flexibility, prevents injury',
                    'tips': 'Hold each stretch for 20-30 seconds'
                }
            ]
        
        elif fitness_level == 'intermediate':
            recommendations['cardio'] = [
                {
                    'name': 'Running',
                    'duration': '30-40 minutes',
                    'frequency': '3-4 times per week',
                    'intensity': 'Moderate to High',
                    'benefits': 'Improves cardiovascular fitness, burns calories',
                    'tips': 'Mix steady-state and interval training'
                },
                {
                    'name': 'Swimming',
                    'duration': '30 minutes',
                    'frequency': '2-3 times per week',
                    'intensity': 'Moderate',
                    'benefits': 'Full body workout',
                    'tips': 'Vary strokes for complete workout'
                }
            ]
            recommendations['strength'] = [
                {
                    'name': 'Weight Training',
                    'duration': '45 minutes',
                    'frequency': '3-4 times per week',
                    'intensity': 'Moderate',
                    'benefits': 'Builds muscle, increases strength',
                    'tips': 'Follow a structured program, progressive overload'
                },
                {
                    'name': 'HIIT',
                    'duration': '20-30 minutes',
                    'frequency': '2 times per week',
                    'intensity': 'High',
                    'benefits': 'Burns fat, improves conditioning',
                    'tips': 'Short bursts of intense exercise with rest periods'
                }
            ]
            recommendations['flexibility'] = [
                {
                    'name': 'Yoga',
                    'duration': '30-45 minutes',
                    'frequency': '2-3 times per week',
                    'intensity': 'Light to Moderate',
                    'benefits': 'Flexibility, balance, stress relief',
                    'tips': 'Try different styles: Vinyasa, Hatha, Yin'
                }
            ]
        
        else:  # Advanced
            recommendations['cardio'] = [
                {
                    'name': 'Running/Sprints',
                    'duration': '45-60 minutes',
                    'frequency': '4-5 times per week',
                    'intensity': 'High',
                    'benefits': 'Peak cardiovascular fitness',
                    'tips': 'Include tempo runs, intervals, long runs'
                },
                {
                    'name': 'Cycling',
                    'duration': '60+ minutes',
                    'frequency': '3-4 times per week',
                    'intensity': 'High',
                    'benefits': 'Endurance, leg strength',
                    'tips': 'Hill climbs, intervals, long rides'
                }
            ]
            recommendations['strength'] = [
                {
                    'name': 'Advanced Weight Training',
                    'duration': '60 minutes',
                    'frequency': '4-5 times per week',
                    'intensity': 'High',
                    'benefits': 'Maximum strength and muscle gains',
                    'tips': 'Periodized training, focus on progressive overload'
                },
                {
                    'name': 'CrossFit/Functional Training',
                    'duration': '45-60 minutes',
                    'frequency': '3-4 times per week',
                    'intensity': 'Very High',
                    'benefits': 'Overall fitness, functional strength',
                    'tips': 'Varied workouts, high intensity'
                }
            ]
            recommendations['flexibility'] = [
                {
                    'name': 'Yoga/Mobility Work',
                    'duration': '30 minutes',
                    'frequency': '3-4 times per week',
                    'intensity': 'Moderate',
                    'benefits': 'Recovery, injury prevention',
                    'tips': 'Essential for recovery and performance'
                }
            ]
    
    # Gender-specific considerations
    if user.gender == 'female':
        recommendations['precautions'].extend([
            'Consider bone health - include weight-bearing exercises',
            'Adjust intensity during menstrual cycle if needed',
            'Focus on pelvic floor exercises'
        ])
    
    # General precautions
    if not recommendations['precautions']:
        recommendations['precautions'] = [
            'Always warm up before exercise (5-10 minutes)',
            'Cool down and stretch after workouts',
            'Stay hydrated throughout the day',
            'Listen to your body and rest when needed',
            'Gradually increase intensity over time'
        ]
    
    return recommendations
