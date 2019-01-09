'''
update species_category table in postgis
by D. Bailey
'''

# Import os and pandas
import os
import pandas as pd
import psycopg2

# Ubuntu path: /usr/share/wildlife_project/tabular_data/
# iMac path: /Users/davidbailey/Desktop/Data/GIS_Data/tabular_data/
# Macbook path: /Users/DavidBailey/Desktop/Data/GIS_Data/tabular_data

species_list_excel = os.path.join("/Users/davidbailey/Desktop/Data/GIS_Data/tabular_data/", "Species_status.xlsx")

# Load spreadsheet
xl = pd.ExcelFile(species_list_excel)

# Load a sheet into a DataFrame by name: df1
df1 = xl.parse('Sheet1')

#df1.rename(index=str, columns={"SCI_NAME": "sci_name", "STATUS": "status"})\

df1.columns = ['sci_name', 'common_names', 'species_category', 'status']

df1['common_names'] = df1['common_names'].str.replace(r"\(.*\)","")

df1['common_names'] = df1['common_names'].replace('\s+', ' ', regex=True)


#result = re.findall(regex, com_name)

print df1['common_names']

print df1

# connection variables for wildlife_db
db = "dbname='wildlife_db'"
user = "user='wildlife_db'"
host = "host"
passw = "password"

# connect to postgis
connection = psycopg2.connect(db + user + host + passw)
cursor = connection.cursor()

# load processed pandas data frame into postgres using sqlalechemy
print "Pushing Pandas Data Frame to PostGres"

from sqlalchemy import create_engine
engine = create_engine('postgresql://wildlife_db:ggEc2ad!jqSfdawd!#$@138.68.62.194:5432/wildlife_db', pool_pre_ping=True)
df1.to_sql('species_status', engine, schema='prod_data', if_exists='append')
