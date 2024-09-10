# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 19:53:17 2024

@author: psson
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#method to read json file

json_file = open('loan_data_json.json')
data = json.load(json_file)

#method2 to read json file

with open('loan_data_json.json') as json_file:
    data = json.load(json_file)
    
#convering json file to dataframe

loandata = pd.DataFrame(data)

#finding unique values for the purpose column

loandata['purpose'].unique()

#describe the data

loandata.describe()

#describe the data for a specific column

loandata['int.rate'].describe()
loandata['fico'].describe()
loandata['dti'].describe()

#using exp() to get annual income

income = np.exp(loandata['log.annual.inc'])
loandata['annualincome'] = income

#working with arrays

arr = np.array([1,2,3,4])

#0D array

arr2 = np.array(50)

#2D array

arr3 = np.array([[1,2,3],[4,5,6]])

#using if statement on the fico
# 300 - 400: Very Poor
# - 401 - 600: Poor
# - 601 - 660: Fair
# - 661 - 700: Good
# - 701 - 850: Excellent

fico = 700

if fico >= 300 and fico < 400:
    ficocat = 'Very Poor'
elif fico >= 400 and fico < 600:
    ficocat = 'Poor'
elif fico >= 601 and fico < 660:
    ficocat = 'Fair'
elif fico >= 661 and fico < 700:
    ficocat = 'Good'
elif fico >= 700: 
    ficocat = 'Excellent'
else:
    ficocat = 'Unknown'
    
print(ficocat)


#applying for loop to loandata

length = len(loandata)
ficocat = []
for x in range(0,length):
    category = loandata['fico'][x]
    
    try:
        if category >= 300 and category < 400:
            cat = 'Very Poor'
        elif category >= 400 and category < 600:
            cat = 'Poor'
        elif category >= 601 and category < 660:
            cat = 'Fair'
        elif category >= 661 and category < 700:
            cat = 'Good'
        elif category >= 700:
            cat = 'Excellent'
        else:
            category = 'Unkown'
    except:
        categry = 'Error  - Unknown'
        
    ficocat.append(cat)

ficocat = pd.Series(ficocat)
    
loandata['fico.category'] = ficocat

#using df.loc to create a new column in the dataframe
#Syntax - df.loc[dataframe[columnname] condition, new column name] = value if the condition is met

loandata.loc[loandata['int.rate'] > 0.12, 'int.rate.type'] = 'High'
loandata.loc[loandata['int.rate'] <= 0.12, 'int.rate.type'] = 'Low'


#number of loans / rows by fico category

catplot = loandata.groupby(['fico.category']).size()
catplot.plot.bar(color = 'green' , width = 0.1)
plt.show()

purposecount = loandata.groupby(['purpose']).size()
purposecount.plot.bar(color = 'yellow' , width = 0.3)
plt.show()


#scatter plot

ypoint = loandata['annualincome']
xpoint = loandata['dti']
plt.scatter(xpoint,ypoint, color = 'red')
plt.show()

#writing to csv
loandata.to_csv('loan_cleaned.csv' , index = True)




