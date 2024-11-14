# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 16:14:22 2024

@author: psson
"""

import pandas as pd
import numpy as np
from string import ascii_letters
from string import punctuation
from string import digits
import matplotlib.pyplot as plt


#importing excel files
dataset = pd.read_csv("games_description.csv")
review_data = pd.read_csv("steam_game_reviews.csv" , usecols = ['hours_played', 'recommendation' , 'game_name'])
dataset_ranking = pd.read_csv("games_ranking.csv")

#define functions here
def openingbracket(column):
    return column.str.replace('[','')

def closingbracket(column):
    return column.str.replace(']','')

#removing opening and closing square bracket from the dataFrame columns
dataset['genres'] = openingbracket(dataset['genres'])
dataset['genres'] = closingbracket(dataset['genres'])

dataset['minimum_system_requirement'] = openingbracket(dataset['minimum_system_requirement'])
dataset['minimum_system_requirement'] = closingbracket(dataset['minimum_system_requirement'])

dataset['recommend_system_requirement'] = openingbracket(dataset['recommend_system_requirement'])
dataset['recommend_system_requirement'] = closingbracket(dataset['recommend_system_requirement'])

dataset['developer'] = openingbracket(dataset['developer'])
dataset['developer'] = closingbracket(dataset['developer'])

dataset['publisher'] = openingbracket(dataset['publisher'])
dataset['publisher'] = closingbracket(dataset['publisher'])

#Converting column - number_of_reviews_from_purchased_people negavtive number to positive and removing the values that have round bracket
for i in range(0,len(dataset)):
    if '(' and ')' in dataset['number_of_reviews_from_purchased_people'][i]:
        dataset['number_of_reviews_from_purchased_people'][i] = 0
    else:
        continue

dataset['number_of_reviews_from_purchased_people'] = dataset['number_of_reviews_from_purchased_people'].str.replace(',','')
dataset['number_of_reviews_from_purchased_people'] = dataset['number_of_reviews_from_purchased_people'].str.replace('-','')

dataset['number_of_reviews_from_purchased_people'] = pd.to_numeric(dataset['number_of_reviews_from_purchased_people'] , errors = 'coerce')
dataset['number_of_reviews_from_purchased_people'] = pd.to_numeric(dataset['number_of_reviews_from_purchased_people'] , errors = 'coerce').convert_dtypes()


#deleting column - "link" from the dataframe
dataset = dataset.drop('link' , axis = 1)

#creating new columns of esports, FPS and RPG
is_fps = []
is_esports = []
is_rpg = []

for game in range(0,len(dataset)):
    if 'FPS' in dataset['genres'][game]:
        fps = True
    else:
        fps = False
    is_fps.append(fps)
        
for game in range(0,len(dataset)):
    if 'eSports' in dataset['genres'][game]:
        esports = True
    else:
        esports = False
    is_esports.append(esports)
    
for game in range(0,len(dataset)):
    if 'RPG' in dataset['genres'][game]:
        rpg = True
    else:
        rpg = False
    is_rpg.append(rpg)
    
#convering the lists - is_fps, is_esports, is_rpg to Series and adding them to the dataset
is_fps = pd.Series(is_fps)
is_esports = pd.Series(is_esports)
is_rpg = pd.Series(is_rpg)

dataset['is_fps'] = is_fps
dataset['is_esports'] = is_esports
dataset['is_rpg'] = is_rpg

#Maintaining the integrity of the column - overall_player_rating by having values as  -->
review_comment = ['Overwhelmingly Positive',
'Very Positive',
'Mostly Positive',
'Neutral',
'Mostly Negative',
'Very Negative',
'Overwhelmingly Negative']
dataset['overall_player_rating'] = np.where((dataset.overall_player_rating.isin(review_comment)) , dataset['overall_player_rating'] , 'Neutral' )
        
#Removing foreign characters, copyright, trademark and registered trademark characters from the column - name
allowed = set(ascii_letters + ' ' + punctuation + digits)
for ch in range(len(dataset)):
    dataset['name'][ch] = ''.join(i for i in dataset['name'][ch] if i in allowed)


#Removing foreign characters, copyright, trademark and registered trademark characters from the column - short_description
for ch in range(len(dataset)):
    try:
        dataset['short_description'][ch] = ''.join(i for i in dataset['short_description'][ch] if i in allowed)
    except:
        dataset['short_description'][ch] = ''
        
#deleting column - long_description
dataset = dataset.drop('long_description' , axis = 1)

#Removing single quotation marks from the columns developer and publisher
def removequotationmarks(col):
    return col.str.replace('\'' , '')

dataset['developer'] = removequotationmarks(dataset['developer'])
dataset['publisher'] = removequotationmarks(dataset['publisher'])

##---------------Working on the dataframe dataset_ranking------------------##

#Removing foreign characters, copyright, trademark and registered trademark characters from the column - name
for ch in range(len(dataset_ranking)):
    dataset_ranking['game_name'][ch] = ''.join(i for i in dataset_ranking['game_name'][ch] if i in allowed) 

##----------------Working on the dataframe review_data---------------##

#Removing foreign characters, copyright, trademark and registered trademark characters from the column - name
for ch in range(len(review_data)):
    review_data['game_name'][ch] = ''.join(i for i in review_data['game_name'][ch] if i in allowed)
    

#creating a new column to sum the hours played for each game
review_data['hours_played'] = review_data['hours_played'].str.replace(',' , '')
review_data['hours_played'] = pd.to_numeric(review_data['hours_played'] , errors = 'coerce').convert_dtypes()
hours = review_data.groupby(by = ['game_name'] , sort = False)['hours_played'].sum()

review_data = pd.merge(review_data , hours , left_on = 'game_name' , right_on = 'game_name' , how = 'left')

#Summarizing recommendation on the basis of players' reviews

review_data['recommended'] = review_data.groupby(['game_name','recommendation'])['recommendation'].transform('count')


#deleting column - hours_played_x
review_data = review_data.drop('hours_played_x' , axis = 1)

#removing duplicate rows from the dataframe - review_data
review_data = review_data.drop_duplicates(subset = 'game_name')

#slicing the dataframe review_data to 11 rows
xaxis = review_data['game_name'][:11]
yaxis = review_data['hours_played_y'][:11]

#plotting bar graph for Total Hours Played
plt.xticks(range(len(xaxis)) , xaxis , color = 'orange' , rotation = 90 , fontsize = 10)
plt.bar(xaxis , yaxis)
plt.title("Total Hours Played")

##-----------------------Exporting to new csvs----------------------------##
dataset.to_csv("Steam_Games_Analysis2_cleaned.csv" , index = False)
dataset_ranking.to_csv("dataset_ranking_cleaned.csv" , index = False)




