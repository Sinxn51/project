import pandas as pd
import numpy as np
import scipy.stats
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from myproject.models import User
from myproject import mongo_db
from collections import defaultdict

# MongoDB doesn't need this function - data is already in dict format


def meal(cuisine,meal,calorie,hascancer,hasdiabetes,df2):
    if hascancer=='Y':
        for index,i in df2.iterrows():
            if (i['Fiber']>15) or (('high fiber') in i['soup']):
                continue
            else:
                df2.drop(index,inplace=True)
    if hasdiabetes=='Y':
        for index,i in df2.iterrows():
            if 'diabet' not in i['soup']:
                df2.drop(index,inplace=True)
    
    if hascancer!='Y' and hasdiabetes !='Y':
        for index,i in df2.iterrows():
            if cuisine not in i['soup']:
                df2.drop(index,inplace=True)
    
    for index,i in df2.iterrows():
        if (calorie+50>i['Calories'] and calorie-200<i['Calories']):
            continue
        else:
            df2.drop(index,inplace=True)
    lst=[]
    if meal=='breakfast':
        lst.append(int(df2.sample()['ID']))
        return lst
    else:
        lst.append(int(df2.sample()['ID']))
        temp=int(df2.sample()['ID'])
        while temp==lst[0]:
            temp=int(df2.sample()['ID'])
        lst.append(temp)
        return lst

def generatemeal(age,height,weight,exercise,sex,hascancer,hasdiabetes,cuisine):
    BMR=0
    if sex=='M':
      BMR = 13.397*weight + 4.799*height - 5.677*age + 88.362  
    else:
        BMR = 9.247*weight + 3.0988*height - 4.330*age + 447.593
#     print(BMR)
#  Sedentary (little or no exercise) : Calorie-Calculation = BMR x 1.2
# Lightly active (light exercise/sports 1-3 days/week) : Calorie-Calculation = BMR x 1.375
# Moderately active (moderate exercise/sports 3-5 days/week) : Calorie-Calculation = BMR x 1.55
# Very active (hard exercise/sports 6-7 days a week) : Calorie-Calculation = BMR x 1.725
# If you are extra active (very hard exercise/sports & a physical job) : Calorie-Calculation = BMR x 1.9
    calorie=BMR*exercise
    
    # Data loaded from MongoDB collections
    
    # Load Breakfast from MongoDB collection 'breakfast'
    dfb = pd.DataFrame(list(mongo_db['breakfast'].find({}, {"_id": 0})))
    # dfb=pd.read_csv('Breakfast.csv')  
    dfb2=dfb.copy()
    breakfastlst=meal(cuisine,'breakfast',1/7*calorie,hascancer,hasdiabetes,dfb)
    
    # dfl=pd.read_csv('LunchDinner.csv')
    # Load LunchDinner from MongoDB collection 'lunchdinner'
    dfl = pd.DataFrame(list(mongo_db['lunchdinner'].find({}, {"_id": 0})))
    # dfl=pd.read_csv('LunchDinner.csv')
    dfl2=dfl.copy()

    lunchlst=meal(cuisine,'lunch',2/10*calorie,hascancer,hasdiabetes,dfl)
    breakfastlst.extend(lunchlst)
    
    dfb2.drop(columns=['soup'], inplace=True)
    dfl2.drop(columns=['soup'], inplace=True)
    
    dfm = dfb2.loc[dfb2['ID'] == breakfastlst[0]]
    
    for i in range(1,len(breakfastlst)):
        dfm = pd.concat([dfm, dfl2.loc[dfl2['ID'] == breakfastlst[i]]], ignore_index=True)
    lstDoc = dfm.to_dict('records')
    return lstDoc, breakfastlst
#     return breakfastlst

def get_recommendations(ID, cosine_sim, idx, df):
    # Get the index of the item that matches the title
    indices_from_food_id = pd.Series(df.index, index=df['ID'])
    if idx == -1 and ID != "":
        try:
            idx = indices_from_food_id[ID]
        except KeyError:
            # If ID not found, return a random ID from the dataframe
            return int(df.sample()['ID'])

    # Get the pairwise similarity scores of all dishes with that dish
    try:
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort the dishes based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get the scores of the most similar dishes
        sim_scores = sim_scores[1:25]

        # Get the food indices
        food_indices = [i[0] for i in sim_scores]

        # Return the top most similar dish
        if food_indices:
            return int(df.iloc[food_indices[0]]['ID'])
        else:
            return int(df.sample()['ID'])
    except (IndexError, KeyError):
        # Fallback to random selection if any error occurs
        return int(df.sample()['ID'])

def cosinemat(df):
    count = CountVectorizer(stop_words='english')

    # df1['soup']
    count_matrix = count.fit_transform(df['soup'])

    # Compute the Cosine Similarity matrix based on the count_matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    
    #indices_from_title = pd.Series(df.index, index=df['Name'])
    indices_from_food_id = pd.Series(df.index, index=df['ID'])
    return cosine_sim    

def onClickGenerateMeal(userID,age,height,weight,sex,exercise,hascancer,hasdiabetes,cuisine,lst):
     # Retrieve previously suggested meal from MongoDB 
    if not lst:
        lstDoc, breakfastlst = generatemeal(age,height,weight,exercise,sex,hascancer,hasdiabetes,cuisine)
        return lstDoc, breakfastlst
    else:
        breakfastid=lst[0]
        lunchid=lst[1]
        dinnerid=lst[2]
        
        dfb = pd.DataFrame(list(mongo_db['breakfast'].find({}, {"_id": 0})))
        dfb2 = dfb.copy()
        cosine_sim=cosinemat(dfb)

        newlst = []
        brkid = get_recommendations(breakfastid,cosine_sim,-1,dfb)
        newlst.append(brkid)
        
        dfl = pd.DataFrame(list(mongo_db['lunchdinner'].find({}, {"_id": 0})))
        dfl2 = dfl.copy()

        cosine_sim=cosinemat(dfl)
        lid = get_recommendations(lunchid,cosine_sim,-1,dfl)
        newlst.append(lid)
        did = get_recommendations(dinnerid,cosine_sim,-1,dfl)
        newlst.append(did)
        
        dfb2.drop(columns=['soup'], inplace=True)
        dfl2.drop(columns=['soup'], inplace=True)
        
        dfm = dfb2.loc[dfb2['ID'] == newlst[0]]
        
        for i in range(1,len(newlst)):
            dfm = pd.concat([dfm, dfl2.loc[dfl2['ID'] == newlst[i]]], ignore_index=True)
        lstDoc = dfm.to_dict('records')
        return lstDoc, newlst



def feedbacklst(userID,age,height,weight,sex,exercise,hascancer,hasdiabetes,cuisine,lst):
    
    if not lst:
        lstDoc, breakfastlst = generatemeal(age,height,weight,exercise,sex,hascancer,hasdiabetes,cuisine)
        return lstDoc, breakfastlst
    else:
        breakfastid=lst[0]
        lunchid=lst[1]
        dinnerid=lst[2]
        
        dfb = pd.DataFrame(list(mongo_db['breakfast'].find({}, {"_id": 0})))
        dfb2 = dfb.copy()
        cosine_sim=cosinemat(dfb)

        newlst = []
        brkid = get_recommendations(breakfastid,cosine_sim,-1,dfb)
        newlst.append(brkid)
        
        dfl = pd.DataFrame(list(mongo_db['lunchdinner'].find({}, {"_id": 0})))
        dfl2 = dfl.copy()

        cosine_sim=cosinemat(dfl)
        lid = get_recommendations(lunchid,cosine_sim,-1,dfl)
        newlst.append(lid)
        did = get_recommendations(dinnerid,cosine_sim,-1,dfl)
        newlst.append(did)
        
        dfb2.drop(columns=['soup'], inplace=True)
        dfl2.drop(columns=['soup'], inplace=True)
        
        dfm = dfb2.loc[dfb2['ID'] == newlst[0]]
        
        for i in range(1,len(newlst)):
            dfm = pd.concat([dfm, dfl2.loc[dfl2['ID'] == newlst[i]]], ignore_index=True)
        lstDoc = dfm.to_dict('records')
        return lstDoc, newlst













def gender():
    return 'M'

def cuisine():
    return 'gujarat'