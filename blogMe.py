# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 19:32:18 2024

@author: psson
"""

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#read excel file

data = pd.read_excel('articles.xlsx')

#summary of the data
data.describe()

#summary of the columns
data.info()

#count number of articles per source

data.groupby(['source_id'])['article_id'].count()

#number of reactions per publisher

data.groupby(['source_id'])['engagement_reaction_count'].sum()

#dropping a column

data = data.drop('engagement_comment_plugin_count' , axis = 1)


#defining a function
def thisFunction():
    print('This is my first function')
    
thisFunction()
 

#creating a keyword flag

keyword = 'crash'

#using for loop to isolate each row

# length = len(data['title'])
# keyword_flag = []
# for x in range (0,length):
#     heading = data['title'][x]
#     if keyword in heading:
#         flag = 1
#     else:
#         flag = 0
#     keyword_flag.append(flag)
        
#creating the function

def keywordFlag(keyword):
    length = len(data)
    keyword_flag = []
    for x in range (0,length):
        heading = data['title'][x]
        try:
            if keyword in heading:
                flag = 1
                print(data['title'][x])
            else:
                flag = 0
        except:
            flag = 0
        keyword_flag.append(flag)
    return keyword_flag
    
keywordFlag = keywordFlag('murder')
            
data['keyword_flag'] = pd.Series(keywordFlag)


#Sentinent Analyzer

sent_int = SentimentIntensityAnalyzer()
text = data['title'][16]
sent = sent_int.polarity_scores(text)


#adding sentiment to each title using for loop

title_pos_sentiment = []
title_neg_sentiment = []
title_neu_sentiment = []

length = len(data)

for x in range(0,length):
    try:
        text = data['title'][x]
        sent_int = SentimentIntensityAnalyzer()
        sent = sent_int.polarity_scores(text)
        neg = sent['neg']
        pos = sent['pos']
        neu = sent['neu']
    except:
        neg = 0
        pos = 0
        neu = 0
    title_neg_sentiment.append(neg)
    title_pos_sentiment.append(pos)
    title_neu_sentiment.append(neu)
    
    
title_neg_sentiment = pd.Series(title_neg_sentiment)
title_pos_sentiment = pd.Series(title_pos_sentiment)
title_neu_sentiment = pd.Series(title_neu_sentiment)


data['title_neg_sentiment'] = title_neg_sentiment
data['title_pos_sentiment'] = title_pos_sentiment
data['title_neu_sentiment'] = title_neu_sentiment


#writing the data to excel

data.to_excel('blogme_clean.xlsx', sheet_name = 'blogmedata', index = False)