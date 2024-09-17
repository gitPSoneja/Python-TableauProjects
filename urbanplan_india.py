# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 14:27:46 2024

@author: psson
"""

import pandas as pd

data = pd.read_excel("AllUrE_India2011_FNv2.xlsx",sheet_name=2)

#Renaming column names
data.rename(columns = {'IND_fof11':'industrial_fossilFuel',
                       'IND_ele11':'industrial_electricity',
                       'RES_fof11':'residential_fossilFuel',
                       'RES_ele11':'residential_electricity',
                       'RES_fwd11':'residential_firewood',
                       'TRA_fof11':'transportation_fossilFuel',
                       'TRA_ele11':'transportation_electricity',
                       'OTH_fof11':'commercial_fossilFuel',
                       'OTH_ele11':'commercial_electricity',
                       'No_HH':'totalHouseholds',
                       'TOT_P':'totalPopulation',
                       'TOT_M':'malePopulation',
                       'TOT_F':'femalePopulation',
                       'MAIN_CL_P':'mainWorkers_cultivators',
                       'MAIN_AL_P':'mainWorkers_agriculturalLabourers',
                       'MAIN_HH_P':'mainWorkers_household',
                       'MAIN_OT_P':'mainWorkers_otherSectors',
                       'MARG_CL_P':'marginalWorkers_cultivators',
                       'MARG_AL_P':'marginalWorkers_agriculturalLabourers',
                       'MARG_HH_P':'marginalWorkers_household',
                       'MARG_OT_P':'marginalWorkers_otherSectors',
                       'NON_WORK_P':'nonworkingPersons',
                       'MAIN_IND_WRK':'mainWorkers_industrial',
                       'MARG_IND_WRK':'marginalWorkers_industrial',
                       'MAIN_COM_WRK':'mainWorkers_commercial',
                       'MARG_COM_WRK':'marginalWorkers_commercial',
                       'HH_nonint':'totalHouseholds_noninstitutional',
                       'nock_per':'nocook_per',
                       'othck_per':'otherenergycook_per',
                       'biogck_per':'biogascook_per',
                       'eleck_per':'electricitycook_per',
                       'LPGck_per':'LPGcook_per',
                       'kerock_per':'kerosenecook_per',
                       'coalck_per':'coalcook_per',
                       'dungck_per':'dungcakecook_per',
                       'cropck_per':'cropresiduecook_per',
                       'frwdck_per':'firewoodcook_per',
                       'latr_access':'sanitationaccess_per',
                       'ele_access':'electricityaccess_per',
                       'h2otrtd_per':'wateraccess_per',
                       'popden':'personsperarea' }
                       , inplace = True)

#fetch state names from the State Code file

statecode = pd.read_excel('State Code.xlsx')

data = pd.merge(data , statecode , on = 'ST_ID' )


#Calculating first KPI - Electricity consumption per capita

industrial_electricity = round(data['industrial_electricity'].sum(),2)
residential_electricity = round(data['residential_electricity'].sum(),2)
transportation_electricity = round(data['transportation_electricity'].sum(),2)
commercial_electricity = round(data['commercial_electricity'].sum(),2)

totalPopulation = round(data['totalPopulation'].sum(),2)

electricity_per_capita = ((industrial_electricity + residential_electricity + transportation_electricity + commercial_electricity ) / totalPopulation) * 100


#Calculating second measure - population of each state


statepopulation = data.groupby(['State Name'])['totalPopulation'].sum()
statepopulation.name = 'statepopulation'
data = data.join(statepopulation, on = 'State Name')

#classifying each state by rural, semi-rural, urban, semi-urban


classi_list = []
length = len(data['statepopulation'])
for x in range(0,length):
    try:
        if(data['statepopulation'][x] < 10000):
            classi = 'Rural'
        elif(data['statepopulation'][x] >= 10000 and data['statepopulation'][x] < 100000):
            classi = 'Semi - Urban'
        elif(data['statepopulation'][x] >= 100000 and data['statepopulation'][x] <= 1000000):
            classi = 'Urban'
        elif(data['statepopulation'][x] >= 1000000):
            classi = 'Metropolitan'
        else:
            classi = 'Unkown'
    except:
        classi = 'Unkown'
    classi_list.append(classi)
    
#classifying each district by rural, semi-rural, urban and semi-urban
    
    
data.loc[data['totalPopulation'] < 10000 , 'Classification'] = 'Rural'
data.loc[((data['totalPopulation'] >= 10000) & (data['totalPopulation'] < 100000)), 'Classification'] = 'Semi-Urban'
data.loc[((data['totalPopulation'] >= 100000) & (data['totalPopulation'] < 1000000)), 'Classification'] = 'Urban'
data.loc[data['totalPopulation'] >=1000000 , 'Classification'] = 'Metropolitan'

data.to_excel("UrbanPlanning_cleaned.xlsx" , sheet_name = "UrbanPlanning" , index = False)





    

              

        
    
        
        


