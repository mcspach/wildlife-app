'''
load csv's into wildlife_list postgis
by D. Bailey
'''

# Import os and pandas and numpy
import os
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 2000)
pd.set_option('display.max_rows', 9000)
import psycopg2
import io


'''
# convert excel to csv - Mammals
species_list_excel2 = os.path.join("/Users/DavidBailey/Desktop/Bitbucket/wildlife_app/tabular_data/","2018_EDGE_Lists_for_website.xlsx")
output_mammals2 =  os.path.join("/Users/DavidBailey/Desktop/Bitbucket/wildlife_app/tabular_data/", 'mammals_list.csv')
wb2 = xlrd.open_workbook(species_list_excel2)
sh2 = wb2.sheet_by_name('EDGE Mammals')
mammals_csv_file2 = open(output_mammals2, 'wb2')
wr2 = csv.writer(mammals_csv_file2, quoting=csv.QUOTE_ALL)

for rownum2 in xrange(sh2.nrows):
    print rownum2
    wr2.writerow(sh2.row_values(rownum2))

mammals_csv_file2.close()
'''

### pre-process csv data ###

# Ubuntu path: /usr/share/wildlife_project/tabular_data/
# iMac path: /Users/davidbailey/Desktop/Data/GIS_Data/tabular_data/
# Macbook path: /Users/DavidBailey/Desktop/Data/GIS_Data/tabular_data

# csv paths
csv_amphibians = os.path.join("/Users/DavidBailey/Desktop/Data/GIS_Data/tabular_data","complete_amphibians_list.csv")
csv_reptiles = os.path.join("/Users/DavidBailey/Desktop/Data/GIS_Data/tabular_data","complete_reptiles_list.csv")
csv_mammals = os.path.join("/Users/DavidBailey/Desktop/Data/GIS_Data/tabular_data","complete_mammals_list.csv")

## process amphibians data using pandas ##

# create data frame
df_amphibians = pd.read_csv(csv_amphibians)[["order", "family", "genus", "species", "common_names"]] # original data frame

# merge genus and species into one column
df_amphibians["species"] = df_amphibians.genus + " " + df_amphibians.species

# remove unwanted species by splitting at multiple delimiters, change NaN to sci name
df_amphibians['common_names'] = df_amphibians['common_names'].str.split(',').str[0]
df_amphibians['common_names'] = df_amphibians['common_names'].str.split(';').str[0]
df_amphibians['common_names'] = df_amphibians['common_names'].str.split('<').str[0]
df_amphibians['common_names'] = df_amphibians['common_names'].str.split('(').str[0]
df_amphibians['common_names'] = df_amphibians['common_names'].str.split('|').str[0]
df_amphibians['common_names'] = df_amphibians['common_names'].replace(np.nan, df_amphibians['species'], regex=True)
df_amphibians['species_category'] = 'AMPHIBIANS'

# populate generic name in data frame based on common_names value
search_toad = ["Toad", "toad", "Toads", "toads"]
search_toad2 =["Bufonidae", "Scaphiopodidae", "Rhinophrynidae", "Pelobatidae", "Bombinatoridae"]
search_frog = ["Frog", "frog", "Frogs", "frogs"]
search_frog2 = ["Anura", "anura"]
search_salamander = ["Salamander", "salamander", "Salamanders", "salamanders"]
search_salamander2 = ["Caudata"]
search_newts = ["Newt", "newt", "Newts", "newts"]
Gymnophiona = ["Gymnophiona"]
amphibians_all = search_toad + search_frog + search_salamander + search_newts + search_frog2 + search_toad2 + search_salamander + Gymnophiona
df_amphibians.loc[~df_amphibians.common_names.str.contains("|".join(amphibians_all)), 'gen_name'] = "Other"
df_amphibians.loc[df_amphibians.order.str.contains("|".join(search_frog2)), 'gen_name'] = "Frog"
df_amphibians.loc[df_amphibians.family.str.contains("|".join(search_toad2)), 'gen_name'] = "Toad"
df_amphibians.loc[df_amphibians.order.str.contains("|".join(search_salamander2)), 'gen_name'] = "Salamander"
df_amphibians.loc[df_amphibians.order.str.contains("|".join(Gymnophiona)), 'gen_name'] = "Caecilian"
df_amphibians.loc[df_amphibians.common_names.str.contains("|".join(search_toad)), 'gen_name'] = "Toad"
df_amphibians.loc[df_amphibians.common_names.str.contains("|".join(search_frog)), 'gen_name'] = "Frog"
df_amphibians.loc[df_amphibians.common_names.str.contains("|".join(search_salamander)), 'gen_name'] = "Salamander"
df_amphibians.loc[df_amphibians.common_names.str.contains("|".join(search_newts)), 'gen_name'] = "Newt"

# drop excess columns
df_amphibians.drop(['order', 'family', 'genus'], axis=1, inplace=True)

#print df_amphibians

## process mammals data using pandas ##

# create data frame
df_mammals = pd.read_csv(csv_mammals)[["Genus", "species", "common_names"]]

# merge genus and species into one column
df_mammals["species"] = df_mammals.Genus + " " + df_mammals.species

# remove unwanted species by splitting at multiple delimiters, change NaN to sci name
df_mammals['common_names'] = df_mammals['common_names'].str.split(',').str[0]
df_mammals['common_names'] = df_mammals['common_names'].str.split(';').str[0]
df_mammals['common_names'] = df_mammals['common_names'].str.split('<').str[0]
df_mammals['common_names'] = df_mammals['common_names'].str.split('(').str[0]
df_mammals['common_names'] = df_mammals['common_names'].str.split('|').str[0]
df_mammals['common_names'] = df_mammals['common_names'].replace(np.nan, df_mammals['species'], regex=True)
df_mammals['common_names'] = df_mammals['common_names'].replace(np.nan, "Unknown", regex=True)
df_mammals['species_category'] = 'MAMMALS'
#print df_mammals

# populate generic name in data frame based on common_name value
search_bear = ["Bear", "bear", "Bear", "bears", "Grizzly", "grizzly"]
search_deer = ["Deer", "deer", "Deers", "Deers"]
search_lion = ["Lion", "lion", "Lions", "lions"]
search_cougar = ["Cougar", "cougar", "Cougars", "cougars", "Wildcat", "wildcat", "Mountain Lion", "Mountain lion"]
search_beaver = ["Beaver", "beaver", "Beavers", "beavers"]
search_marmot = ["Marmot", "marmot", "Marmots", "marmots"]
search_squirrel = ["Squirrel", "squirrel", "Squirrels", "squirrels"]
search_raccoon = ["Raccoon", "raccoon", "Raccoons", "raccoons"]
search_rabbit = ["Rabbit", "rabbit", "Rabbits", "rabbits", "Cottontail", "cottontail", "Hare", "hare"]
search_buffalo = ["Buffalo", "buffalo", "Newts", "buffalos", "Bison", "bison"]
search_bobcat = ["Bobcat", "bobcat", "Bobcats", "bobcats"]
search_wolverine = ["Wolverine", "wolverine", "Wolverines", "wolverines", "wolverene", "Wolverene"]
search_goat = ["Goat", "goat", "Goats", "goats", "Mountain Goat", "Mountain goat"]
search_cow = ["Cow", "cow", "Cows", "cow"]
search_sheep = ["Sheep", "sheep", "Sheeps", "sheeps"]
search_moose = ["Moose", "moose"]
search_bat = ["Bat", "bat", "Bats", "bats"]
search_fox = ["Fox", "fox", "Foxes", "foxes"]
search_caribou = ["Caribou", "caribou", "Caribous", "caribous", "reindeer", "Reindeer"]
search_tiger = ["Tiger", "tiger", "Tigers", "tigers"]
search_cheetah = ["Cheetah", "Cheetahs", "cheetah", "cheetahs"]
search_chipmunk = ["Chipmunk", "Chipmunks", "chipmunk", "chipmunks"]
search_coyote = ["Coyote", "coyote", "Coyotes", "coyotes"]
search_monkey = ["Monkey", "monkey", "Monkeys", "monkeys"]
search_wolf = ["Wolf", "wolf", "Wolves", "wolves"]
search_groundhog = ["Groundhog", "groundhog", "Groundhogs", "groundhogs"]
search_river_otter = ["River Otter", "river otter", "River Otters", "river otters", "River otter", "River otters"]
search_sea_otter = ["Sea Otter", "sea otter", "Sea Otters", "sea otters", "Sea otter", "Sea otters"]
search_whale = ["Whale", "whale", "Whales", "whales"]
search_dolphin = ["Dolphin", "dolphin", "Dolphins", "dolphins"]
search_pig = ["Pigs", "pig", "Pigs", "pigs", "Hog", "hog", "Boar", "boar"]
search_platypus = ["Platypus", "platypus"]
search_prairie_dog = ["Prairie Dog", "prairie dog", "Prairie Dogs", "prairie dog", "prairie dog", "prairie dogs"]
search_horse = ["Horse", "horse", "Horses", "horses"]
search_skunk = ["Skunk", "skunk", "Skunks", "skunks"]
search_zebra = ["Zebra", "zebra", "Zebras", "zebras"]
search_elk = ["Elk", "elk"]
search_pika = ["Pika", "pika", "Pikas", "pikas"]
search_fisher = ["Fisher", "Fishers", "fisher", "fishers"]
search_rat = ["Rat", "rat", "Rats", "rats"]
search_mouse = ["Mouse", "mice", "mouse", "mice"]
search_vole = ["Vole", "voles", "vole", "Voles"]
search_mule = ["Mule", "mule", "Mules", "mules"]
search_weasel = ["Weasel", "weasel", "Weasels", "weasels"]
search_badger = ["Badger", "badger", "Badgers", "badgers"]
search_echidna = ["Echidna"]

mammals_all = search_bear + search_deer + search_badger + search_dolphin + search_weasel + search_cougar +\
              search_beaver + search_marmot + search_squirrel + search_rabbit + search_buffalo + search_bobcat\
              + search_wolverine + search_goat + search_cow + search_sheep + search_moose + search_bat + search_fox\
              + search_caribou + search_tiger + search_cheetah + search_chipmunk + search_coyote + search_monkey +\
              search_wolf + search_groundhog + search_river_otter + search_sea_otter + search_whale + search_pig +\
              search_platypus + search_prairie_dog + search_horse + search_skunk + search_zebra + search_elk +\
              search_pika + search_fisher + search_rat + search_mouse + search_vole + search_mule + search_echidna

df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_bear)), 'gen_name'] = "Bear"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_deer)), 'gen_name'] = "Deer"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_cougar)), 'gen_name'] = "Cougar"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_beaver)), 'gen_name'] = "Beaver"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_marmot)), 'gen_name'] = "Marmot"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_squirrel)), 'gen_name'] = "Squirrel"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_rabbit)), 'gen_name'] = "Rabbit"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_buffalo)), 'gen_name'] = "Buffalo"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_bobcat)), 'gen_name'] = "Bobcat"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_wolverine)), 'gen_name'] = "Wolverine"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_goat)), 'gen_name'] = "Goat"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_sheep)), 'gen_name'] = "Sheep"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_moose)), 'gen_name'] = "Moose"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_bat)), 'gen_name'] = "Bat"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_fox)), 'gen_name'] = "Fox"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_caribou)), 'gen_name'] = "Caribou"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_tiger)), 'gen_name'] = "Tiger"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_cheetah)), 'gen_name'] = "Cheetah"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_chipmunk)), 'gen_name'] = "Chipmunk"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_coyote)), 'gen_name'] = "Coyote"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_monkey)), 'gen_name'] = "Monkey"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_wolf)), 'gen_name'] = "Wolf"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_groundhog)), 'gen_name'] = "Groundhog"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_river_otter)), 'gen_name'] = "River Otter"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_sea_otter)), 'gen_name'] = "Sea Otter"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_whale)), 'gen_name'] = "Whale"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_pig)), 'gen_name'] = "Pig"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_platypus)), 'gen_name'] = "Platypus"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_prairie_dog)), 'gen_name'] = "Prairie Dog"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_horse)), 'gen_name'] = "Horse"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_skunk)), 'gen_name'] = "Skunk"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_zebra)), 'gen_name'] = "Zebra"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_elk)), 'gen_name'] = "Elk"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_pika)), 'gen_name'] = "Pika"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_fisher)), 'gen_name'] = "Fisher"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_rat)), 'gen_name'] = "Rat"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_vole)), 'gen_name'] = "Vole"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_mule)), 'gen_name'] = "Mule"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_dolphin)), 'gen_name'] = "Dolphin"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_weasel)), 'gen_name'] = "Weasel"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_badger)), 'gen_name'] = "Badger"
df_mammals.loc[df_mammals.common_names.str.contains("|".join(search_echidna)), 'gen_name'] = "Echidna"
df_mammals.loc[~df_mammals.common_names.str.contains("|".join(mammals_all)), 'gen_name'] = "Other"

# drop excess columns
df_mammals.drop(['Genus'], axis=1, inplace=True)

#print df_mammals
## process reptile data using pandas ##

# create data frame
df_reptiles = pd.read_csv(csv_reptiles)[["species", "common_names"]]

# remove unwanted species by splitting at multiple delimiters, change NaN to sci name
df_reptiles['common_names'] = df_reptiles['common_names'].str.split(',').str[0]
df_reptiles['common_names'] = df_reptiles['common_names'].str.split(';').str[0]
df_reptiles['common_names'] = df_reptiles['common_names'].str.split('<').str[0]
df_reptiles['common_names'] = df_reptiles['common_names'].str.split('(').str[0]
df_reptiles['common_names'] = df_reptiles['common_names'].str.split('|').str[0]
df_reptiles['common_names'] = df_reptiles['common_names'].str.split('\nG:').str[0]
df_reptiles['common_names'] = df_reptiles['common_names'].str.split('\n').str[0]
df_reptiles['common_names'] = df_reptiles['common_names'].str.split('.').str[0]
df_reptiles['common_names'] = df_reptiles['common_names'].str.split(': ').str[-1]
df_reptiles['common_names'] = df_reptiles['common_names'].replace(np.nan, df_reptiles['species'], regex=True)
df_reptiles['species_category'] = 'REPTILES'

# populate generic name in data frame based on common_name value
search_snake = ["Snake", "snake", "SNAKE", "snakes", "Copperhead", "Viper", "viper", "Moccasin", "Sidewinder", "Blackhead", "Rattlesnake", "rattlesnake", "Boa", "Python", "python", "boa"]
search_lizard =["Lizard", "lizard", "LIZARD", "lizards", "Anole", "anole", "Whiptail"]
search_turtle = ["Turtle", "turtle", "Frogs", "frogs"]
search_skink = ["Skink", "skink"]
search_gecko = ["Gecko", "gecko", "geckos", "Geckos"]
search_croc = ["Crocodile", "crocodile", "Alligator", "alligator"]
search_chameleon = ["Chameleon", "chameleon", "Chameleons", "chameleons"]

reptiles_all = search_snake + search_lizard + search_turtle + search_skink + search_gecko + search_croc + search_chameleon
df_reptiles.loc[df_reptiles.common_names.str.contains("|".join(search_snake)), 'gen_name'] = "Snake"
df_reptiles.loc[df_reptiles.common_names.str.contains("|".join(search_lizard)), 'gen_name'] = "Lizard"
df_reptiles.loc[df_reptiles.common_names.str.contains("|".join(search_turtle)), 'gen_name'] = "Turtle"
df_reptiles.loc[df_reptiles.common_names.str.contains("|".join(search_skink)), 'gen_name'] = "Skink"
df_reptiles.loc[df_reptiles.common_names.str.contains("|".join(search_gecko)), 'gen_name'] = "Gecko"
df_reptiles.loc[df_reptiles.common_names.str.contains("|".join(search_croc)), 'gen_name'] = "Crocodile"
df_reptiles.loc[df_reptiles.common_names.str.contains("|".join(search_chameleon)), 'gen_name'] = "Chameleon"
df_reptiles.loc[~df_reptiles.common_names.str.contains("|".join(reptiles_all)), 'gen_name'] = "Other"
#print df_reptiles


### connect to postgres ###

# connection variables for wildlife_db
db = "dbname='wildlife_db'"
user = "user='wildlife_db'"
host = "host='138.68.62.194'"
passw = "password=ggEc2ad!jqSfdawd!#$"

# connect to postgis
connection = psycopg2.connect(db + user + host + passw)
cursor = connection.cursor()

'''
# input for password ASddsD$jw!!8fd0Fggsd&4
enter_pass = raw_input("Enter Password for wildlife_db: ")
# connection variables
db = "dbname='wildlife_db'"
user = "user='wildlife_db'"
host = "host='138.68.62.194'"
passw = "password=" + enter_pass

# make connection to postgres
connection = psycopg2.connect(db + user + host + passw)
cursor = connection.cursor()

'''
# delete existing data in table
#cursor.execute("DROP TABLE prod_data.wildlife_list;")

# load processed pandas data frame into postgres using sqlalechemy
print "Pushing Pandas Data Frame to PostGres"

from sqlalchemy import create_engine
engine = create_engine('postgresql://wildlife_db:ggEc2ad!jqSfdawd!#$@138.68.62.194:5432/wildlife_db', pool_pre_ping=True)
#df_amphibians.to_sql('wildlife_list', engine, schema='prod_data', if_exists='append')
#df_reptiles.to_sql('wildlife_list', engine, schema='prod_data', if_exists='append')
df_mammals.to_sql('wildlife_list', engine, schema='prod_data', if_exists='append')


'''
from sqlalchemy import create_engine
engine = create_engine('postgresql://wildlife_db:ggEc2ad!jqSfdawd!#$@138.68.62.194:5432/wildlife_db')
conn = engine.raw_connection()
cur = conn.cursor()
output = io.StringIO()
df_amphibians.to_csv(output, sep='\t', header=False, index=False)
output.seek(0)
contents = output.getvalue()
cur.copy_from(output, 'table_name', null="") # null values become ''
conn.commit()

print "success"
'''
# commit to Database
connection.commit()
