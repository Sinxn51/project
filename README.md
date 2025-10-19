Personalised diet planner to recommend meals on daily or weekly basis based on user's body requirements, health conditions and dietary preferences using content filtering and collaborative filtering.

See `report.pdf` for the detailed write-up.

Getting Started

1) Prerequisites
- Python 3.11+ (tested with 3.13)
- MongoDB running locally or Atlas (use MongoDB Compass to manage data)

2) Setup
- Create and activate a virtual environment, then install deps:
  - Windows PowerShell:
    - `py -3 -m venv .venv`
    - `.\.venv\Scripts\python -m pip install --upgrade pip`
    - `.\.venv\Scripts\pip install -r requirements.txt`

3) Configure environment
- Create a `.env` file (see `.env.example`):
  - `MONGO_URI=mongodb://localhost:27017`
  - `MONGO_DB_NAME=diet_planner`
  - Optional: `SECRET_KEY=change-me`

4) Seed data
- Import the CSVs into MongoDB:
  - `.\.venv\Scripts\python scripts\import_to_mongo.py`
  - Collections created: `breakfast`, `lunchdinner`

5) Run
- `.\.venv\Scripts\python app.py`
- Open `http://127.0.0.1:5000`

Notes
- All data (meals and user accounts) is stored in MongoDB.
- To use MongoDB Compass, connect with your `MONGO_URI`, then browse `diet_planner.breakfast`, `diet_planner.lunchdinner`, and `diet_planner.users`.
