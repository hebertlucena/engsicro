import requests
import pandas as pd
import json
from pathlib import Path

from datetime import datetime, timedelta

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"
from_time = (datetime.now() + timedelta(-1)).strftime(TIMESTAMP_FORMAT)

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

df = pd.DataFrame.from_dict(response['results'])


path = Path("temp/education.csv")

if path.is_file() == False:
    df.to_csv("temp/education.csv")
else:
    df_old = pd.read_csv("temp/education.csv")
    df_new = pd.concat([df_old, df])
        
    df_main_drop_duplicadas = df_new.drop_duplicates(subset = 'id', keep = 'first')
        
    df_main_drop_duplicadas.to_csv("temp/education.csv")
