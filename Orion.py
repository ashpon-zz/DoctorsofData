
# coding: utf-8

# In[77]:

import pandas as pd
import matplotlib.pyplot as plot
import requests as req
from census import Census
from us import states
import os

# Census API Key
c = Census("5e99f22848e97d5bcc53f03a358b973493473cd9")
cKey = "5e99f22848e97d5bcc53f03a358b973493473cd9"


# In[78]:

# Read Main CSV
msgPpl = pd.read_csv("NCMEC_final.csv")
msgPpl.head()


# In[126]:

census_data = c.acs5.get(("NAME", "B19013_001E", "B01003_001E", "B01002_001E",
                          "B19301_001E",
                          "B17001_002E"), {'for': 'zip code tabulation area:*'})


# In[ ]:




# In[125]:

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
df_state_pop.loc[df_state_pop['Missing_Ratio'] > 20]


# In[120]:

dfbottom3State = df_state_pop.sort_values(["POP"], ascending = True).head(3)
dfbottom3State


# In[121]:

dfTop3State = df_state_pop.sort_values(["POP"], ascending=False).head(3)
dfTop3State


# In[ ]:



