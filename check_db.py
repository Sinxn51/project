"""
Check if MongoDB has the required data
"""
from myproject import mongo_db

print("=" * 50)
print("Checking MongoDB Collections")
print("=" * 50)

# Check breakfast collection
breakfast_count = mongo_db['breakfast'].count_documents({})
print(f"\nBreakfast collection: {breakfast_count} documents")

if breakfast_count > 0:
    sample = mongo_db['breakfast'].find_one()
    print(f"Sample breakfast item:")
    print(f"  - ID: {sample.get('ID')}")
    print(f"  - Name: {sample.get('Name')}")
    print(f"  - Calories: {sample.get('Calories')}")
    print(f"  - Has 'soup' field: {bool(sample.get('soup'))}")

# Check lunchdinner collection
lunchdinner_count = mongo_db['lunchdinner'].count_documents({})
print(f"\nLunchDinner collection: {lunchdinner_count} documents")

if lunchdinner_count > 0:
    sample = mongo_db['lunchdinner'].find_one()
    print(f"Sample lunch/dinner item:")
    print(f"  - ID: {sample.get('ID')}")
    print(f"  - Name: {sample.get('Name')}")
    print(f"  - Calories: {sample.get('Calories')}")
    print(f"  - Has 'soup' field: {bool(sample.get('soup'))}")

# Check users collection
users_count = mongo_db['users'].count_documents({})
print(f"\nUsers collection: {users_count} documents")

print("\n" + "=" * 50)

if breakfast_count == 0 or lunchdinner_count == 0:
    print("\n⚠️  WARNING: Collections are empty!")
    print("You need to import data from CSV files.")
    print("\nRun this command to import data:")
    print("  python scripts/import_data.py")
else:
    print("\n✓ All collections have data!")
