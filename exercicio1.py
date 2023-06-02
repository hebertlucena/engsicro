import requests
import pandas as pd
import json
from pathlib import Path

from datetime import datetime, timedelta

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"
from_time = (datetime.now() + timedelta(-1000)).strftime(TIMESTAMP_FORMAT)

args = {
    'section' : 'education',
    'from-date' : from_time,
    'order-by' : 'newest', 
    'api-key' : '5eb7e673-9bad-41f1-84d3-6d8c5c1cb12c',
}

url_principal = 'http://content.guardianapis.com/search'
url_principal = '{}?{}'.format(
    url_principal, 
    '&'.join(["{}={}".format(kk, vv) for kk, vv in args.items()])
)
req = requests.get(url_principal)

src = req.text


response = json.loads(src)['response']

assert response['status'] == 'ok'

json.loads(src)['response']['status']

sections = json.loads(src)['response']

education_main = pd.DataFrame.from_dict(response['results'])


df_current = pd.read_csv('education_current.csv')
path = Path("education_main.csv")

if path.is_file() == False:
  # if false, save initial main file  
  df_current.to_csv("education_main.csv", index = False)
else:
  # if the file already exists, save it to a dataframe and then append to a new one    
  df_main_old = pd.read_csv("education_main.csv")
  df_main_new = pd.concat([df_main_old,df_current])

  # deduplicate based on unique id
  df_main_new_drop_dupes = df_main_new.drop_duplicates(subset = "id", keep = "first")

  # save to dataframe and overwrite the old usgs_main file
  df_main_new_drop_dupes.to_csv("education_main.csv", index = False)

#df.to_csv("education.csv")
