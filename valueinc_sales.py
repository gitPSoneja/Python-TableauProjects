# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 13:29:14 2024

@author: psson
"""

import pandas as pd

data = pd.read_csv("transaction.csv")

data = pd.read_csv("transaction.csv",sep=';')

#summary of the dataset
data.info() 

#Playing around with variables

var = ['apple','pears','mango'] #list
var2 = ('apple','pears','mango') #tuple
var3 = range(10) #range
var4 = {'name':'Pooja Soneja','location':'Delhi','God':'Lord Jesus'} #dict
var5 = {'apple','pears','mango'} #set
var6 = True

#defining variables in value inc project

#Cost Per Transaction column

CostPerItem = data['CostPerItem']
NumberOfItemsPurchased = data['NumberOfItemsPurchased']
CostPerTransaction = CostPerItem * NumberOfItemsPurchased

#adding new column to the dataframe

data['CostPerTransaction'] = CostPerTransaction

#Sales Per Transaction

data['SalesPerTransaction'] = data['SellingPricePerItem'] * data['NumberOfItemsPurchased']

#Profit Calculation = Sales - Cost

data['ProfitPerTransaction'] = data['SalesPerTransaction'] - data['CostPerTransaction']

#Markup Calculation = Sales - Cost / Cost

data['Markup'] = round((data['SalesPerTransaction'] - data['CostPerTransaction'])/ data['CostPerTransaction'] , 2)


#checking data type of a column

print(data['Day'].dtype)

#changing data type of a column

day = data['Day'].astype(str)
year = data['Year'].astype(str)
print(day.dtype)
print(year.dtype)

my_date = day + '-' + day + '-' + year

data['Date'] = my_date

#using iloc 

data.iloc[0] #views first row in the dataframe
data.iloc[0:3] #views first 3 rows in the dataframe
data.iloc[-5:] #views last 5 rows in the dataframe
data.iloc[:,2] #views all rows and first 2 columns
data.iloc[4,2] #views the cell - 4th row and 2nd column

#using head

data.head(5) #displays first 5 rows of the dataframe

#using split to split the column - client keywords

split_col = data['ClientKeywords'].str.split(',', expand = True)

#creatingn new columns in the dataframe from the split column series

data['ClientAge'] = split_col[0]
data['ClientType'] = split_col[1]
data['LengthOfContract'] = split_col[2]

#using replace function to replace a character

data['ClientAge'] = data['ClientAge'].str.replace('[' , '')
data['LengthOfContract'] = data['LengthOfContract'].str.replace(']' , '')

#using lower function to change the case

data['ItemDescription'] = data['ItemDescription'].str.lower()

#bringing in new dataset for the merge

data2 = pd.read_csv("value_inc_seasons.csv", sep = ';')

#merging files --> merge_df = pd.merge(old_df,new_df,on='key')

data = pd.merge(data, data2, on='Month')

#dropping columns

data = data.drop('ClientKeywords', axis = 1)
data = data.drop('Day' , axis = 1)
data = data.drop(['Month','Year'], axis = 1)

#export to csv

data.to_csv("ValueInc_Cleaned.csv", index = False)
