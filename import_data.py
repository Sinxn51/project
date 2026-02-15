"""
Import CSV data into MongoDB
"""
import pandas as pd
from myproject import mongo_db

print("=" * 50)
print("Importing Data to MongoDB")
print("=" * 50)

# Import Breakfast data
print("\n1. Importing Breakfast data...")
try:
    df_breakfast = pd.read_csv('Breakfastsql.csv')
    print(f"   Found {len(df_breakfast)} breakfast items in CSV")
    
    # Convert to dict and insert
    breakfast_data = df_breakfast.to_dict('records')
    
    # Clear existing data
    mongo_db['breakfast'].delete_many({})
    
    # Insert new data
    result = mongo_db['breakfast'].insert_many(breakfast_data)
    print(f"   ✓ Inserted {len(result.inserted_ids)} breakfast items")
except FileNotFoundError:
    print("   ✗ Breakfastsql.csv not found!")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Import Lunch/Dinner data
print("\n2. Importing Lunch/Dinner data...")
try:
    df_lunchdinner = pd.read_csv('LunchDinnersql.csv')
    print(f"   Found {len(df_lunchdinner)} lunch/dinner items in CSV")
    
    # Convert to dict and insert
    lunchdinner_data = df_lunchdinner.to_dict('records')
    
    # Clear existing data
    mongo_db['lunchdinner'].delete_many({})
    
    # Insert new data
    result = mongo_db['lunchdinner'].insert_many(lunchdinner_data)
    print(f"   ✓ Inserted {len(result.inserted_ids)} lunch/dinner items")
except FileNotFoundError:
    print("   ✗ LunchDinnersql.csv not found!")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Verify import
print("\n" + "=" * 50)
print("Verification:")
print("=" * 50)
breakfast_count = mongo_db['breakfast'].count_documents({})
lunchdinner_count = mongo_db['lunchdinner'].count_documents({})
print(f"Breakfast collection: {breakfast_count} documents")
print(f"LunchDinner collection: {lunchdinner_count} documents")

if breakfast_count > 0 and lunchdinner_count > 0:
    print("\n✓ Data import successful!")
else:
    print("\n✗ Data import incomplete!")
