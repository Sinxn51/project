"""
Test script to verify authentication system
"""
from myproject import app, users_collection
from myproject.models import User
from werkzeug.security import check_password_hash

def test_user_creation():
    """Test creating a user and verifying password"""
    print("=" * 50)
    print("Testing User Creation and Authentication")
    print("=" * 50)
    
    # Test data
    test_email = "test@example.com"
    test_password = "testpass123"
    
    # Clean up any existing test user
    users_collection.delete_many({"email": test_email})
    print(f"\n✓ Cleaned up existing test user")
    
    # Create a new user
    print(f"\n1. Creating user with email: {test_email}")
    user = User(
        email=test_email,
        username="testuser",
        age="25",
        height="175",
        weight="70",
        blood="O",
        health_issues="none",
        exercise="1.55",
        diet_pref="balanced",
        plan_period="daily",
        food_type="vegetarian",
        gender="male",
        password=test_password
    )
    
    # Save user
    user.save()
    print(f"✓ User created with ID: {user._id}")
    print(f"✓ Password hash: {user.password_hash[:50]}...")
    
    # Verify user in database
    print(f"\n2. Verifying user in database")
    db_user = users_collection.find_one({"email": test_email})
    if db_user:
        print(f"✓ User found in database")
        print(f"  - Email: {db_user['email']}")
        print(f"  - Username: {db_user['username']}")
        print(f"  - Has password_hash: {bool(db_user.get('password_hash'))}")
    else:
        print(f"✗ User NOT found in database")
        return False
    
    # Test password verification
    print(f"\n3. Testing password verification")
    
    # Load user from database
    loaded_user = User.find_by_email(test_email)
    if not loaded_user:
        print(f"✗ Could not load user from database")
        return False
    
    print(f"✓ User loaded from database")
    
    # Test correct password
    if loaded_user.check_password(test_password):
        print(f"✓ Correct password verified successfully")
    else:
        print(f"✗ Correct password verification FAILED")
        return False
    
    # Test wrong password
    if not loaded_user.check_password("wrongpassword"):
        print(f"✓ Wrong password correctly rejected")
    else:
        print(f"✗ Wrong password was incorrectly accepted")
        return False
    
    # Clean up
    users_collection.delete_many({"email": test_email})
    print(f"\n✓ Test user cleaned up")
    
    print(f"\n{'=' * 50}")
    print(f"✓ ALL TESTS PASSED!")
    print(f"{'=' * 50}")
    return True

if __name__ == "__main__":
    with app.app_context():
        test_user_creation()
