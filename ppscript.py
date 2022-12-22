import requests
import re
import sys
import json
import time
import math
import pandas as pd
import random
import mariadb

# sleep to allow network services to startup after reboot
#time.sleep(300)

# define the saskpower outage JSON API
url = 'https://outagemap.saskpower.com/Files/GetJsonFile'

# define a funtion to build a semi random request payload to hopefully defeat scraping detection
def make_payload():
    # generate the current unix epoch in expected format and randomize it a bit
    epoch = math.floor(time.time()*1000) + random.randint(10000, 100000) 
    rid = int(epoch / 60000) 
    # build request payload
    payload =   {   'rid': rid, 
                    'callback': 'OutageMap', 
                    '_':epoch, 
                }
    return payload

# define a funtion to return current year
def get_yearnow():
    return time.strftime('%Y', time.gmtime(time.time()))

#parse config settings from config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
        database=config["database"]
    )
    print("Success: connected to MariaDB Platform")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

#get cursor object 
curse = conn.cursor()
conn.autocommit = False

# process json response
resp = requests.get(url, data=make_payload(), verify=True)
trimmed = re.findall('(?:OutageMap\()(.+)(?:\))', resp.text)
raw_json = json.loads(trimmed[0])
outages = raw_json['Outages']

if outages:

    # process dataframe cleanup tasks
    alert_df = pd.json_normalize(outages, record_path=['Alerts'], meta=['OutageId', 'RegionId', 'Region', 'Planned'])
    alert_df['CreateDate'] = get_yearnow() +' '+ alert_df['CreateDate']
    alert_df['CreateDate'] = pd.to_datetime(alert_df['CreateDate'], utc=False)
    alert_df['Planned'] = alert_df['Planned'].replace('Unplanned', 0)
    alert_df['Planned'] = alert_df['Planned'].replace('Planned', 1)

    # iterate over the dataframe and push the rows into the database
    for index, row in alert_df.iterrows():
        values = row.values.astype('str').tolist()
        #print(values)
        try:
            curse.execute("INSERT IGNORE INTO alerts (alert_create_date, alert_message, outage_id, region_id, region_text, planned ) VALUES (?, ?, ?, ?, ?, ?)", (values))
            conn.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")
        continue

else:
    print('No Outages To Report')