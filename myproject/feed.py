import pandas as pd
import numpy as np
import scipy.stats
from myproject import mongo_db

# Helper to fetch feedback-related data from MongoDB
def get_breakfast_df():
    return pd.DataFrame(list(mongo_db['breakfast'].find({}, {"_id": 0})))

def get_lunchdinner_df():
    return pd.DataFrame(list(mongo_db['lunchdinner'].find({}, {"_id": 0})))

def feedbackmeal(breakfastlst):
    # Load data from MongoDB collections
    dfb = pd.DataFrame(list(mongo_db['breakfast'].find({}, {"_id": 0})))
    dfl = pd.DataFrame(list(mongo_db['lunchdinner'].find({}, {"_id": 0})))
    
    # Remove unnecessary columns
    dfb.drop(columns=['Keywords', 'soup'], inplace=True)
    dfl.drop(columns=['Keywords', 'soup'], inplace=True)
    
    # Create dataframe with selected meals
    dfm = dfb.loc[dfb['ID'] == breakfastlst[0]]
    
    for i in range(1, len(breakfastlst)):
        if i == 1:  # First item after breakfast is lunch
            dfm = dfm.append(dfl.loc[dfl['ID'] == breakfastlst[i]])
        else:  # Rest are dinner items
            dfm = dfm.append(dfl.loc[dfl['ID'] == breakfastlst[i]])
    
    lstDoc = dfm.to_dict('records')
    return lstDoc