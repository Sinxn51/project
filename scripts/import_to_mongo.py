import os
import pandas as pd
from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'myproject', 'data')

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'diet_planner')

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]


def import_csv(collection_name: str, csv_path: str) -> None:
    df = pd.read_csv(csv_path)
    if 'ID' in df.columns:
        df['ID'] = df['ID'].astype(int)
    records = df.where(pd.notnull(df), None).to_dict('records')
    db[collection_name].delete_many({})
    if records:
        db[collection_name].insert_many(records)
    print(f"Imported {len(records)} records into '{collection_name}'.")


def main() -> None:
    breakfast_csv = os.path.join(DATA_DIR, 'Breakfast.csv')
    lunch_csv = os.path.join(DATA_DIR, 'LunchDinner.csv')

    import_csv('breakfast', breakfast_csv)
    import_csv('lunchdinner', lunch_csv)


if __name__ == '__main__':
    main()


