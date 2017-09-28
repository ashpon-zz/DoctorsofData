
# coding: utf-8

# In[134]:

import pandas as pd
import matplotlib.pyplot as plot
import requests as req
from census import Census
from us import states
import os

# Census API Key
c = Census("5e99f22848e97d5bcc53f03a358b973493473cd9")
cKey = "5e99f22848e97d5bcc53f03a358b973493473cd9"


# In[135]:

# Read Main CSV
msgPpl = pd.read_csv("NCMEC_final.csv")
msgPpl.head()


# In[136]:

# census_data = c.acs5.get(("NAME", "B19013_001E", "B01003_001E", "B01002_001E",
#                           "B19301_001E",
#                           "B17001_002E"), {'for': 'zip code tabulation area:*'})


# In[137]:

#Create census for states
url = "https://api.census.gov/data/2014/pep/natstprc?get=STNAME,POP&for=state:*&DATE=7"
reqUrl = url + "&key="+ cKey
getData = req.get(reqUrl).json()
df_state_pop = pd.DataFrame(getData,columns=getData[0])
df_state_pop = df_state_pop.drop(df_state_pop.index[0])
df_state_pop['POP'] =  list(map(int,df_state_pop['POP']))
df_state_pop = df_state_pop[df_state_pop.STNAME != 'District of Columbia']
df_state_pop = df_state_pop[df_state_pop.STNAME != 'Puerto Rico Commonwealth']
df_state_pop = df_state_pop.reset_index(drop = True)
msgState = msgPpl.groupby("missing_state").count()["name"]
df_state_pop['Missing_Population'] = list(msgState)
df_state_pop['Missing_Ratio'] = round(df_state_pop['Missing_Population']/df_state_pop['POP'] * 1000000,2)
# df_state_pop.loc[df_state_pop['Missing_Ratio'] > 20]
df_state_pop


# In[138]:

dfbottom3State = df_state_pop.sort_values(["POP"], ascending = True).head(3)
dfbottom3State


# In[139]:

dfTop3State = df_state_pop.sort_values(["POP"], ascending=False).head(3)
dfTop3State


# In[147]:

# Create an income list by state
# https://api.census.gov/data/2015/acs1?get=NAME,B19013_001E&for=state:*%20&key=5e99f22848e97d5bcc53f03a358b973493473cd9
url = "https://api.census.gov/data/2015/acs1?get=NAME,B19013_001E,B02001_002E,B02001_003E,B02001_004E,B02001_005E,B02001_006E,B02001_007E,B02001_008E,B02001_009E,B02001_010E&for=state:*"
incUrl = url + "&key="+ cKey
getIncData = req.get(incUrl).json()
getIncData = pd.DataFrame(getIncData, columns=getIncData[0])
getIncData = getIncData.drop(getIncData.index[0])
# getIncData["Total Ethnic"] =  int (getIncData["B02001_002E"]) + int (getIncData["B02001_003E"]) +int (getIncData["B02001_004E"]) + int (getIncData["B02001_005E"]) + int (getIncData["B02001_006E"]) + int (getIncData["B02001_007E"]) + int (getIncData["B02001_008E"]) + int (getIncData["B02001_009E"]) + int (getIncData["B02001_010E"])
getIncData = getIncData.rename(columns={"B19013_001E": "Household Income", 
                                      "B02001_002E": "Whites", 
                                      "B02001_003E": "African Americans",
                                      "B02001_004E": "American Indians",
                                      "B02001_005E": "Asians",
                                      "B02001_006E": "Pacific Islanders",
                                      "B02001_007E": "Others",
                                      "B02001_008E": "Two or More Races",
                                      "B02001_009E": "Two or More Inc Others",
                                      "B02001_010E": "Two or More Excl Others",
                                      "NAME": "STNAME" })
getIncData


# In[148]:

getIncData = getIncData[getIncData.STNAME != 'District of Columbia']
getIncData = getIncData[getIncData.STNAME != 'Puerto Rico Commonwealth']
getIncData = getIncData.reset_index(drop = True)
getIncData


# In[151]:

allDataDf = df_state_pop.merge(getIncData)


# In[153]:

allDataDf["STNAME"]


# In[ ]:



