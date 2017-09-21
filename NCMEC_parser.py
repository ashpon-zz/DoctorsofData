
# coding: utf-8

# In[36]:

import json
import requests
import pandas as pd

session = requests.Session()

df = pd.DataFrame(columns = ['name','age','missing_date','missing_city','missing_county','missing_state',])


# In[37]:

state = input("Which State to gather data from?(Abbreviations only) ")
query_url_temp = "http://www.missingkids.com/missingkids/servlet/JSONDataServlet?action=publicSearch&searchLang=en_US&search=new&subjToSearch=child&missState=" + state + "&missCountry=US"
response_temp = session.get(query_url_temp)
#print("{} {}".format(response.status_code, response.reason))


# In[39]:

response_temp_json = json.loads(response_temp.text)
#print(json.dumps(response_temp_json, sort_keys=True, indent=4, separators=(',', ': ')))


# In[43]:

for i in range(int(response_temp_json['totalPages'])):
    query_url_loop = "http://www.missingkids.com/missingkids/servlet/JSONDataServlet?action=publicSearch&searchLang=en_US&goToPage={}".format(i+1)
    response_loop = session.get(query_url_loop)
    response_loop_json = json.loads(response_loop.text)
    #print("starting loop " + str(i+1))
    #print(query_url_loop)
    for ii in range(len(response_loop_json['persons'])):
        person_name = response_loop_json['persons'][ii]['firstName'] + " " + response_loop_json['persons'][ii]['lastName']
        if response_loop_json['persons'][ii]['middleName'] != "":
            person_name.replace("", " {} ".format(response_loop_json['persons'][ii]['middleName']))
        
        index_num = (len(response_loop_json['persons']) * i) + ii
        try:
            df.set_value(index_num,'name',person_name)
            df.set_value(index_num,'age',response_loop_json['persons'][ii]['age'])
            df.set_value(index_num,'missing_date',response_loop_json['persons'][ii]['missingDate'])
            df.set_value(index_num,'missing_city',response_loop_json['persons'][ii]['missingCity'])
            df.set_value(index_num,'missing_county',response_loop_json['persons'][ii]['missingCounty'])
            df.set_value(index_num,'missing_state',response_loop_json['persons'][ii]['missingState'])
        except:
            print('error T.T')
            continue
        #print(person_name)
            
df.to_csv("NCMEC_{}.csv".format(state), encoding="utf-8", index=False)


# In[ ]:



