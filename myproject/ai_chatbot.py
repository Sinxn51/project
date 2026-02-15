"""
AI Chatbot for nutrition and health queries
"""

def get_chatbot_response(prompt, user=None):
    """
    Get AI response based on user prompt and profile
    """
    prompt_lower = prompt.lower()
    
    # Personalized responses if user is provided
    user_context = ""
    if user:
        user_context = f" (Based on your profile: {user.health_issues}, {user.food_type} diet)"
    
    # Weight loss queries
    if any(word in prompt_lower for word in ['weight loss', 'lose weight', 'fat loss']):
        return f"""To lose weight safely{user_context}:
        
• Create a calorie deficit of 500-750 calories per day for 1-1.5 lbs/week loss
• Focus on high-protein foods (lean meats, fish, eggs, legumes) to preserve muscle
• Include plenty of vegetables and fiber to stay full
• Drink 8-10 glasses of water daily
• Combine with 150+ minutes of moderate exercise weekly
• Get 7-9 hours of quality sleep
• Track your progress weekly, not daily

Remember: Sustainable weight loss is gradual. Avoid crash diets!"""

    # Protein queries
    elif 'protein' in prompt_lower:
        return f"""Protein recommendations{user_context}:

• General adults: 0.8-1.0g per kg body weight
• Active individuals: 1.2-1.6g per kg body weight
• Athletes/bodybuilders: 1.6-2.2g per kg body weight

Best protein sources:
• Animal: Chicken, fish, eggs, lean beef, Greek yogurt
• Plant: Lentils, chickpeas, tofu, quinoa, nuts, seeds

Tip: Spread protein intake across 3-4 meals for optimal muscle synthesis."""

    # Diabetes queries
    elif 'diabetes' in prompt_lower or 'blood sugar' in prompt_lower:
        return f"""Managing diabetes through diet{user_context}:

• Choose low glycemic index (GI) foods
• Include fiber-rich foods (vegetables, whole grains, legumes)
• Limit refined carbs and sugary foods
• Eat regular, balanced meals
• Monitor portion sizes
• Stay hydrated

Good food choices:
• Non-starchy vegetables
• Whole grains (oats, brown rice, quinoa)
• Lean proteins
• Healthy fats (nuts, avocado, olive oil)

Always consult your doctor for personalized advice!"""

    # Heart health queries
    elif any(word in prompt_lower for word in ['heart', 'cholesterol', 'blood pressure']):
        return f"""Heart-healthy eating tips{user_context}:

• Limit saturated fats and trans fats
• Include omega-3 rich foods (salmon, walnuts, flaxseeds)
• Eat plenty of fruits and vegetables (5+ servings daily)
• Choose whole grains over refined grains
• Reduce sodium intake (< 2,300mg daily)
• Limit alcohol consumption

Heart-healthy foods:
• Fatty fish (salmon, mackerel)
• Berries and leafy greens
• Nuts and seeds
• Olive oil
• Oats and beans

Regular exercise and stress management are also crucial!"""

    # Exercise queries
    elif 'exercise' in prompt_lower or 'workout' in prompt_lower:
        return f"""Exercise recommendations{user_context}:

Weekly goals:
• 150 minutes moderate cardio OR 75 minutes vigorous cardio
• 2-3 strength training sessions
• Daily stretching/flexibility work

Types of exercise:
• Cardio: Walking, running, cycling, swimming
• Strength: Weight training, bodyweight exercises
• Flexibility: Yoga, stretching, Pilates

Pre-workout: Light carbs + protein (banana + peanut butter)
Post-workout: Protein + carbs within 30-60 minutes

Start slowly and gradually increase intensity!"""

    # Hydration queries
    elif 'water' in prompt_lower or 'hydration' in prompt_lower:
        return f"""Hydration guidelines{user_context}:

Daily water intake:
• Men: 3.7 liters (15.5 cups)
• Women: 2.7 liters (11.5 cups)
• During exercise: Add 1.5-2.5 cups per hour

Signs of good hydration:
• Light yellow urine
• Regular urination
• Moist lips and mouth
• Good energy levels

Tips:
• Drink water with each meal
• Carry a reusable water bottle
• Eat water-rich foods (cucumbers, watermelon)
• Drink before you feel thirsty"""

    # Vitamins queries
    elif 'vitamin' in prompt_lower or 'supplement' in prompt_lower:
        return f"""Essential vitamins and minerals{user_context}:

Key nutrients:
• Vitamin D: Sunlight, fatty fish, fortified foods
• Vitamin B12: Meat, fish, dairy, fortified cereals
• Iron: Red meat, spinach, lentils, fortified grains
• Calcium: Dairy, leafy greens, fortified plant milk
• Omega-3: Fatty fish, walnuts, flaxseeds

Who needs supplements?
• Vegans (B12, D, omega-3)
• Pregnant women (folate, iron)
• Older adults (D, B12, calcium)
• Those with deficiencies

Best approach: Get nutrients from whole foods first, supplement only if needed after consulting a healthcare provider."""

    # Meal timing queries
    elif 'meal timing' in prompt_lower or 'when to eat' in prompt_lower:
        return f"""Optimal meal timing{user_context}:

General guidelines:
• Breakfast: Within 1-2 hours of waking
• Lunch: 4-5 hours after breakfast
• Dinner: 3-4 hours before bedtime
• Snacks: Between meals if needed

Benefits of regular timing:
• Stable blood sugar levels
• Better metabolism
• Improved digestion
• Consistent energy

Tip: Listen to your hunger cues and maintain consistency!"""

    # Healthy snacks
    elif 'snack' in prompt_lower:
        return f"""Healthy snack ideas{user_context}:

Protein-rich:
• Greek yogurt with berries
• Hard-boiled eggs
• Nuts and seeds (1/4 cup)
• Hummus with veggies

Balanced options:
• Apple with peanut butter
• Whole grain crackers with cheese
• Trail mix (nuts + dried fruit)
• Protein smoothie

Quick energy:
• Fresh fruit
• Vegetable sticks
• Rice cakes with avocado

Keep snacks under 200 calories and include protein or fiber for satiety!"""

    # Portion control
    elif 'portion' in prompt_lower:
        return f"""Portion control strategies{user_context}:

Visual guides:
• Protein: Palm of your hand
• Carbs: Cupped hand
• Fats: Thumb size
• Vegetables: Two cupped hands

Practical tips:
• Use smaller plates (9-10 inches)
• Measure servings initially to learn sizes
• Eat slowly and mindfully
• Stop when 80% full
• Avoid eating from packages

Restaurant tips:
• Share entrees or take half home
• Order appetizer portions
• Ask for dressing/sauce on the side"""

    # Default response
    else:
        return f"""I'm here to help with nutrition and health questions{user_context}!

I can provide information about:
• Weight loss and management
• Protein and nutrient needs
• Managing health conditions (diabetes, heart disease)
• Exercise and fitness nutrition
• Hydration and supplements
• Meal timing and planning
• Healthy snacks and portion control

Please ask me a specific question, and I'll provide detailed guidance!

Note: This is general information. Always consult healthcare professionals for personalized medical advice."""

    return response
