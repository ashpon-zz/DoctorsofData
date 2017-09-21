import json
import requests
import pandas as pd

session = requests.Session()
df = pd.DataFrame(columns = ['name','age','sex','ethnicity','height','weight','eye_color','hair_color','NCMEC_case#','case_type','missing_date','missing_city','missing_county','missing_state',])

state = input("Which State to gather data from?(Abbreviations only) ")
query_url_temp = "http://www.missingkids.com/missingkids/servlet/JSONDataServlet?action=publicSearch&searchLang=en_US&search=new&subjToSearch=child&missState=" + state + "&missCountry=US"
try:
    response_temp = session.get(query_url_temp)
    response_temp_json = json.loads(response_temp.text)
except:
    print("api timeout T.T")
    quit()

for i in range(int(response_temp_json['totalPages'])):
    query_url_loop = "http://www.missingkids.com/missingkids/servlet/JSONDataServlet?action=publicSearch&searchLang=en_US&goToPage={}".format(i+1)
    response_loop = session.get(query_url_loop)
    response_loop_json = json.loads(response_loop.text)
    
    for ii in range(len(response_loop_json['persons'])):
        # detailed response
        try:
            detailed_response = session.get("http://www.missingkids.com/missingkids/servlet/JSONDataServlet?action=childDetail&caseNum={}&orgPrefix={}".format(response_loop_json['persons'][ii]["caseNumber"], response_loop_json['persons'][ii]["orgPrefix"]))
            detailed_response_json = json.loads(detailed_response.text)
            person_info = detailed_response_json['childBean']
        except:
            print("api timeout T.T")
            quit()
        
        # first + middle + last name
        person_name = person_info['firstName'] + " " + person_info['lastName']
        if person_info['middleName'] != "":
            person_name.replace("", " {} ".format(person_info['middleName']))
        
        # index number of df
        index_num = (len(response_temp_json['persons']) * i) + ii
        try:
            df.set_value(index_num,'name',person_name)
            df.set_value(index_num,'age',person_info['age'])
            df.set_value(index_num,'sex',person_info['sex'])
            df.set_value(index_num,'ethnicity',peson_info['race'])
            df.set_value(index_num,'height',person_info['height'])
            df.set_value(index_num,'weight',person_info['weight'])
            df.set_value(index_num,'eye_color',person_info['eyeColor'])
            df.set_value(index_num,'hair_color',person_info['hairColor'])
            df.set_value(index_num,'NCMEC_case#',person_info['caseNumber'])
            df.set_value(index_num,'case_type',person_info['caseType'])
            df.set_value(index_num,'missing_date',person_info['missingDate'])
            df.set_value(index_num,'missing_city',person_info['missingCity'])
            df.set_value(index_num,'missing_county',person_info['missingCounty'])
            df.set_value(index_num,'missing_state',person_info['missingState'])
        except:
            print('error T.T - person {}, page {}'.format(i+1,ii+1))
            continue
        print("person {}, page {} complete".format(i+1,ii+1))
            
df.to_csv("NCMEC_{}.csv".format(state), encoding="utf-8", index=False)