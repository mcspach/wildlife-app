'''
main etl for wildlife_app - extracts postgis dev_data.wildlife_pt, auto-populate fields and loads into postgis prod_data.wildlife_pt
by D. Bailey
'''

import os.path
import psycopg2
import osgeo.ogr
import pandas as pd

# run as dbailey on Ubuntu server
# only run on 1 record at a time

# input for password
#enter_pass = raw_input("Enter Password for wildlife_db: ")

## Update function for updating tables

# connection variables for wildlife_db
db = "dbname='wildlife_db'"
user = "user='wildlife_db'"
host = "host"
passw = "password"

# connect to postgis
connection = psycopg2.connect(db + user + host + passw)
cursor = connection.cursor()

# check number of records in dev_data.wildlife_pt
cursor.execute("SELECT count(*) AS exact_count FROM dev_data.wildlife_pt")
row_count = cursor.fetchone()
print row_count[0]

if row_count[0] == 1:

    print "Run fetchone()[0]"

    ## get wildlife_pt table from dev_data ##

    ## wildlife_id
    cursor.execute("SELECT wildlife_id FROM dev_data.wildlife_pt")
    wildlife_id = cursor.fetchone()[0]
    print wildlife_id

    ## gen_name
    cursor.execute("SELECT gen_name FROM dev_data.wildlife_pt")
    gen_name = cursor.fetchone()[0]
    # make all names title case
    gen_name = gen_name.title()
    print gen_name

    # UPDATE table
    cursor2 = connection.cursor()
    update_sql = """UPDATE dev_data.wildlife_pt SET gen_name = '{}' WHERE wildlife_id = {}""".format(gen_name, wildlife_id)
    cursor2.execute(update_sql)

    ## com_name
    cursor.execute("SELECT com_name FROM dev_data.wildlife_pt")
    com_name = cursor.fetchone()[0]
    print com_name

    if com_name == 'I dont know':
        pass
        # add comment: not sure if this is a Western Rattlesnake
        # run additional spatial intersect and if there are less than 3 species then randomly select the most common
    elif com_name == "" or com_name is None:
        # UPDATE table
        cursor2 = connection.cursor()
        # run additional spatial intersect and if there are less than 3 species then randomly select the most common
        update_sql = """UPDATE dev_data.wildlife_pt SET com_name = '{}' WHERE wildlife_id = {}""".format("", wildlife_id)
        cursor2.execute(update_sql)
    else:
        pass

    ## associate gen_name to gen_name in prod_data.wildlife_list
    ## and populate com_name with with com_name in prod_data.wildlife_list

    # UPDATE table
    cursor2 = connection.cursor()
    update_sql2 = """UPDATE dev_data.wildlife_pt SET sci_name = prod_data.wildlife_list.species FROM prod_data.wildlife_list WHERE com_name = prod_data.wildlife_list.common_names"""
    cursor2.execute(update_sql2)

    ## sci_name
    cursor.execute("SELECT sci_name FROM dev_data.wildlife_pt")
    sci_name = cursor.fetchone()[0]
    print sci_name

    ## associate gen_name to gen_name in prod_data.wildlife_list
    ## and populate com_name with with com_name in prod_data.wildlife_list

    ## associate com_name to com_name in prod_data.wildlife_list
    ## and populate sci_name with with sci_name in prod_data.wildlife_list

    ## associate com_name to com_name in prod_data.species_status
    ## and populate endangered with with species_status in prod_data.species_status

    # UPDATE table
    cursor2 = connection.cursor()
    update_sql2 = """UPDATE dev_data.wildlife_pt SET endangered = prod_data.species_status.status FROM prod_data.species_status WHERE com_name = prod_data.species_status.common_names"""
    cursor2.execute(update_sql2)

    ## endangered
    cursor.execute("SELECT endangered FROM dev_data.wildlife_pt")
    endangered = cursor.fetchone()[0]
    print endangered
    #remove all spaces
    endangered1 = endangered

    ## username
    cursor.execute("SELECT username FROM dev_data.wildlife_pt")
    username = cursor.fetchone()[0]
    print username

    ## name sure username is in username table

    ## comments
    cursor.execute("SELECT comments FROM dev_data.wildlife_pt")
    comments = cursor.fetchone()[0]
    print comments

    ##lat
    cursor.execute("SELECT lat FROM dev_data.wildlife_pt")
    lat = cursor.fetchone()[0]
    print lat

    ##long
    cursor.execute("SELECT long FROM dev_data.wildlife_pt")
    long = cursor.fetchone()[0]
    print long

    ##point
    cursor.execute("SELECT point FROM dev_data.wildlife_pt")
    point = cursor.fetchone()[0]
    print point

    ##species_category
    cursor2 = connection.cursor()
    update_sql2 = """UPDATE dev_data.wildlife_pt SET species_category = prod_data.wildlife_list.species_category FROM prod_data.wildlife_list WHERE dev_data.wildlife_pt.gen_name = prod_data.wildlife_list.gen_name OR com_name = prod_data.wildlife_list.common_names"""
    cursor2.execute(update_sql2)

    # species category
    cursor.execute("SELECT species_category FROM dev_data.wildlife_pt")
    species_category = cursor.fetchone()[0]

    ## associate com_name to com_name in prod_data.wildlife_list
    ## and populate species_category with with species_category in prod_data.wildlife_list

    ##harmful
    cursor2 = connection.cursor()
    update_sql2 = """UPDATE dev_data.wildlife_pt SET harmful = prod_data.dangerous_animals.danger FROM prod_data.dangerous_animals WHERE dev_data.wildlife_pt.gen_name = prod_data.dangerous_animals.gen_name"""
    cursor2.execute(update_sql2)

    ##harmful
    cursor.execute("SELECT harmful FROM dev_data.wildlife_pt")
    harmful = cursor.fetchone()[0]
    print harmful

    #remove all spaces
    if harmful is None:
        harmful1 = harmful
    else:
        harmful1 = harmful.strip()

    ## photo_s3_url1
    cursor.execute("SELECT photo_s3_url1 FROM dev_data.wildlife_pt")
    photo_s3_url1 = cursor.fetchone()[0]
    print photo_s3_url1

    # <img src="https://static.pexels.com/photos/189349/pexels-photo-189349.jpeg" height="120px" width="120px"/>

    ##photo_s3_url2
    cursor.execute("SELECT photo_s3_url2 FROM dev_data.wildlife_pt")
    photo_s3_url2 = cursor.fetchone()[0]
    print photo_s3_url2

    ##photo_s3_url3
    cursor.execute("SELECT photo_s3_url3 FROM dev_data.wildlife_pt")
    photo_s3_url3 = cursor.fetchone()[0]
    print photo_s3_url3

    ##marker
    marker_rare_mammal = "icons/rare_snake_marker.png"
    marker_normal_mammal = "icons/normal_mammal_marker.png"
    marker_danger_mammal = "icons/danger_mammal_marker.png"
    marker_rare_snake = "icons/rare_snake_marker.png"
    marker_normal_snake = "icons/normal_snake_marker.png"
    marker_danger_snake = "icons/danger_snake_marker.png"
    marker_rare_reptile = "icons/rare_reptile_marker.png"
    marker_normal_reptile = "icons/normal_reptile_marker.png"
    marker_danger_reptile = "icons/danger_reptile_marker.png"
    marker_rare_amp = "icons/rare_amph_marker.png"
    marker_normal_amp = "icons/normal_amph_marker.png"
    marker_danger_amp = "icons/danger_amph_marker.png"
    marker_rare_bear = "icons/rare_bear_marker.png"
    marker_danger_bear = "icons/danger_bear_marker.png"
    marker_rare_frog = "icons/rare_frog_marker.png"
    marker_normal_frog = "icons/normal_frog_marker.png"
    marker_danger_frog = "icons/danger_frog_marker.png"

    # if common_names is bear or snake or else

    print species_category

    print gen_name

    print endangered1

    print harmful1

    if species_category == "MAMMALS":
        print "elan"
        if gen_name == "Bear":
            # danger icon
            if endangered1 == "Endangered" or endangered1 == "Threatened":
                cursor4 = connection.cursor()
                update_MAMMALS = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_rare_bear, wildlife_id)
                cursor4.execute(update_MAMMALS)

            # rare icon
            elif harmful1 == "dangerous" or harmful1 == "venomous" or harmful1 == "poisonous":
                cursor4 = connection.cursor()
                update_MAMMALS = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_danger_bear, wildlife_id)
                cursor4.execute(update_MAMMALS)

            else:
                cursor4 = connection.cursor()
                update_MAMMALS = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_normal_mammal,wildlife_id)
                cursor4.execute(update_MAMMALS)
        else:
            # danger icon
            if endangered1 == "Endangered" or endangered1 == "Threatened":
                cursor4 = connection.cursor()
                update_MAMMALS = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_rare_mammal,wildlife_id)
                cursor4.execute(update_MAMMALS)

            # rare icon
            elif harmful1 == "dangerous" or harmful1 == "venomous" or harmful1 == "poisonous":
                cursor4 = connection.cursor()
                update_MAMMALS =  """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_danger_mammal, wildlife_id)
                cursor4.execute(update_MAMMALS)

            else:
                print "NORM"
                update_MAMMALS = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_normal_mammal, wildlife_id)
                cursor.execute(update_MAMMALS)

    elif species_category == "REPTILES":
        if gen_name == "Snake":
            # danger icon
            if endangered1 == "Endangered" or endangered1 == "Threatened":
                cursor4 = connection.cursor()
                update_REP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_rare_snake, wildlife_id)
                cursor4.execute(update_REP)
            # rare icon
            elif harmful1 == "dangerous" or harmful1 == "venomous" or harmful1 == "poisonous":
                cursor4 = connection.cursor()
                update_REP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_danger_snake, wildlife_id)
                cursor4.execute(update_REP)

            else:
                cursor4 = connection.cursor()
                update_REP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_normal_snake, wildlife_id)
                cursor4.execute(update_REP)

        else:
            # danger icon
            if endangered1 == "Endangered" or endangered1 == "Threatened":
                cursor4 = connection.cursor()
                update_REP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_rare_reptile,  wildlife_id)
                cursor4.execute(update_REP)

            # rare icon
            elif harmful1 == "dangerous" or harmful1 == "venomous" or harmful1 == "poisonous":
                cursor4 = connection.cursor()
                update_REP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_danger_reptile, wildlife_id)
                cursor4.execute(update_REP)

            else:
                cursor4 = connection.cursor()
                update_REP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_normal_reptile, wildlife_id)
                cursor4.execute(update_REP)

    else:

        if gen_name == "Frog":
            # danger icon
            if endangered1 == "Endangered" or endangered1 == "Threatened":
                cursor4 = connection.cursor()
                update_AMP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_rare_frog, wildlife_id)
                cursor4.execute(update_AMP)

            # rare icon
            elif harmful1 == "dangerous" or harmful1 == "venomous" or harmful1 == "poisonous":
                cursor4 = connection.cursor()
                update_AMP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_danger_frog, wildlife_id)
                cursor4.execute(update_AMP)

            else:
                cursor4 = connection.cursor()
                update_AMP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_normal_frog, wildlife_id)
                cursor4.execute(update_AMP)

        else:
            # danger icon
            if endangered1 == "Endangered" or endangered1 == "Threatened":
                cursor4 = connection.cursor()
                update_AMP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_rare_amp, wildlife_id)
                cursor4.execute(update_AMP)

            # rare icon
            elif harmful1 == "dangerous" or harmful1 == "venomous" or harmful1 == "poisonous":
                cursor4 = connection.cursor()
                update_AMP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_danger_amp, wildlife_id)
                cursor4.execute(update_AMP)

            else:
                cursor4 = connection.cursor()
                update_AMP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_normal_amp, wildlife_id)
                cursor4.execute(update_AMP)

    ##marker
    cursor2 = connection.cursor()
    cursor.execute("SELECT marker FROM dev_data.wildlife_pt")
    marker = cursor.fetchone()[0]

    print marker


    ## if com_name in prod_data.dangerous_animals
    ## then create url for harmful icon

    ## if com_name in prod_data.species_status
    ## then create url for rare icon

    ##encountered_date
    cursor.execute("SELECT encountered_date FROM dev_data.wildlife_pt")
    encountered_date = cursor.fetchone()[0]
    print encountered_date

    ##encountered_time
    cursor.execute("SELECT encountered_time FROM dev_data.wildlife_pt")
    encountered_time = cursor.fetchone()[0]
    print encountered_time

    ##ts_time
    cursor.execute("SELECT ts_time FROM dev_data.wildlife_pt")
    ts_time = cursor.fetchone()[0]
    print ts_time

    ##ts_date
    cursor.execute("SELECT ts_date FROM dev_data.wildlife_pt")
    ts_date = cursor.fetchone()[0]
    print ts_date

    ### PostGIS DEV to PostGIS PROD
    cursor10 = connection.cursor()
    cursor10.execute('INSERT INTO prod_data.wildlife_pt (gen_name, com_name, sci_name, endangered, harmful, marker, species_category, username, comments, point, lat, long, encountered_date, encountered_time, ts_time, ts_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',(gen_name, com_name, sci_name, endangered, harmful, marker, species_category, username, comments, point, lat, long, encountered_date, encountered_time, ts_time, ts_date))


    print "pushing to PROD"

    ### Remove DEV record
    cursor11 = connection.cursor()
    cursor11.execute('DELETE FROM dev_data.wildlife_pt WHERE wildlife_id = {}'.format(wildlife_id))

elif row_count[0] == 0:
    print "NO RECORDS"

else:
    print "Run first record and PAUSE"

    cursor.execute("SELECT * FROM dev_data.wildlife_pt")

    records = cursor.fetchall()
    for record in records:

        ## wildlife_id
        wildlife_id = record[0]

        print wildlife_id
        print "wildlife_id"

        ## gen_name
        gen_name = record[1]
        # make all names title case
        gen_name = gen_name.title()

        print gen_name
        print "gen_name"

        # UPDATE table
        cursor2 = connection.cursor()
        update_sql = """UPDATE dev_data.wildlife_pt SET gen_name = '{}' WHERE wildlife_id = {}""".format(gen_name, wildlife_id)
        cursor2.execute(update_sql)

        ## com_name
        com_name = record[2]
        print com_name
        print "com_name"

        if com_name == 'I dont know':
            pass
            # add comment: not sure if this is a Western Rattlesnake
            # run additional spatial intersect and if there are less than 3 species then randomly select the most common
        elif com_name == "" or com_name is None:
            # UPDATE table
            cursor2 = connection.cursor()
            # run additional spatial intersect and if there are less than 3 species then randomly select the most common
            #update_sql = """UPDATE dev_data.wildlife_pt SET com_name = '{}' WHERE wildlife_id = {}""".format("", wildlife_id)
            #cursor2.execute(update_sql)
        else:
            pass

        ## associate gen_name to gen_name in prod_data.wildlife_list
        ## and populate com_name with with com_name in prod_data.wildlife_list

        sci_name = record[3]
        print sci_name
        print "sci_name"

        # UPDATE table
        cursor2 = connection.cursor()
        update_sql2 = """UPDATE dev_data.wildlife_pt SET sci_name = prod_data.wildlife_list.species FROM prod_data.wildlife_list WHERE com_name = prod_data.wildlife_list.common_names AND wildlife_id = {}""".format(wildlife_id)
        cursor2.execute(update_sql2)

        ## sci_name
        cursor.execute("SELECT sci_name FROM dev_data.wildlife_pt WHERE wildlife_id = {}".format(wildlife_id))
        sci_name = cursor.fetchone()[0]

        endangered = record[4]
        print endangered
        print "endangered"

        # UPDATE table
        cursor2 = connection.cursor()
        update_sql2 = """UPDATE dev_data.wildlife_pt SET endangered = prod_data.species_status.status FROM prod_data.species_status WHERE com_name = prod_data.species_status.common_names AND wildlife_id = {}""".format(wildlife_id)
        cursor2.execute(update_sql2)

        ## endangered
        cursor.execute("SELECT endangered FROM dev_data.wildlife_pt WHERE wildlife_id = {}".format(wildlife_id))
        endangered = cursor.fetchone()[0]
        print endangered

        ## username
        username = record[6]
        print username
        print "username"

        ## name sure username is in username table

        ## comments
        comments = record[7]
        print comments
        print "comments"

        ##lat
        lat = record[8]
        print lat
        print "lat"

        ##long
        long = record[9]
        print long
        print "long"

        ##point
        point = record[10]
        print point
        print "point"

        ##species_category
        species_category = record[11]

        cursor2 = connection.cursor()
        update_sql2 = """UPDATE dev_data.wildlife_pt SET species_category = prod_data.wildlife_list.species_category FROM prod_data.wildlife_list WHERE dev_data.wildlife_pt.gen_name = prod_data.wildlife_list.gen_name OR com_name = prod_data.wildlife_list.common_names AND wildlife_id = {}""".format(wildlife_id)
        cursor2.execute(update_sql2)

        ## associate com_name to com_name in prod_data.wildlife_list
        ## and populate species_category with with species_category in prod_data.wildlife_list

        ## species_category
        cursor.execute("SELECT species_category FROM dev_data.wildlife_pt WHERE wildlife_id = {}".format(wildlife_id))
        species_category = cursor.fetchone()[0]
        print species_category
        print "species_category"

        harmful = record[12]
        print "harmful"

        ##harmful
        cursor2 = connection.cursor()
        update_sql2 = """UPDATE dev_data.wildlife_pt SET harmful = prod_data.dangerous_animals.danger FROM prod_data.dangerous_animals WHERE dev_data.wildlife_pt.gen_name = prod_data.dangerous_animals.gen_name AND wildlife_id = {}""".format(wildlife_id)
        cursor2.execute(update_sql2)

        # remove all spaces
        if harmful is None:
            harmful = harmful
        else:
            harmful = harmful.strip()

        ## harmful
        cursor.execute("SELECT harmful FROM dev_data.wildlife_pt WHERE wildlife_id = {}".format(wildlife_id))
        harmful = cursor.fetchone()[0]

        ## photo_s3_url1
        photo_s3_url1 = record[5]
        print photo_s3_url1

        # <img src="https://static.pexels.com/photos/189349/pexels-photo-189349.jpeg" height="120px" width="120px"/>

        # photo_s3_url2
        photo_s3_url2 = record[14]
        print photo_s3_url2

        # photo_s3_url3
        photo_s3_url3 = record[15]
        print photo_s3_url3
        
        ##encountered_date
        encountered_date = record[17]
        print encountered_date
    
        ##encountered_time
        encountered_time = record[18]
        print encountered_time
    
        ##ts_time
        ts_time = record[19]
        print ts_time
    
        ##ts_date
        ts_date = record[20]
        print ts_date

        ##marker
        marker_rare_mammal = "icons/rare_snake_marker.png"
        marker_normal_mammal = "icons/normal_mammal_marker.png"
        marker_danger_mammal = "icons/danger_mammal_marker.png"
        marker_rare_snake = "icons/rare_snake_marker.png"
        marker_normal_snake = "icons/normal_snake_marker.png"
        marker_danger_snake = "icons/danger_snake_marker.png"
        marker_rare_reptile = "icons/rare_reptile_marker.png"
        marker_normal_reptile = "icons/normal_reptile_marker.png"
        marker_danger_reptile = "icons/danger_reptile_marker.png"
        marker_rare_amp = "icons/rare_amph_marker.png"
        marker_normal_amp = "icons/normal_amph_marker.png"
        marker_danger_amp = "icons/danger_amph_marker.png"
        marker_rare_bear = "icons/rare_bear_marker.png"
        marker_danger_bear = "icons/danger_bear_marker.png"
        marker_rare_frog = "icons/rare_frog_marker.png"
        marker_normal_frog = "icons/normal_frog_marker.png"
        marker_danger_frog = "icons/danger_frog_marker.png"
    
        # if common_names is bear or snake or else
    
        if species_category == "MAMMALS":
            print "elan"
            if gen_name == "Bear":
                # danger icon
                if endangered == "Endangered" or endangered == "Threatened":
                    cursor4 = connection.cursor()
                    update_MAMMALS = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_rare_bear, wildlife_id)
                    cursor4.execute(update_MAMMALS)
    
                # rare icon
                elif harmful == "dangerous" or harmful == "venomous" or harmful == "poisonous":
                    cursor4 = connection.cursor()
                    update_MAMMALS = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_danger_bear, wildlife_id)
                    cursor4.execute(update_MAMMALS)
    
                else:
                    cursor4 = connection.cursor()
                    update_MAMMALS = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_normal_mammal,wildlife_id)
                    cursor4.execute(update_MAMMALS)
            else:
                # danger icon
                if endangered == "Endangered" or endangered == "Threatened":
                    cursor4 = connection.cursor()
                    update_MAMMALS = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_rare_mammal,wildlife_id)
                    cursor4.execute(update_MAMMALS)
    
                # rare icon
                elif harmful == "dangerous" or harmful == "venomous" or harmful == "poisonous":
                    cursor4 = connection.cursor()
                    update_MAMMALS =  """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_danger_mammal, wildlife_id)
                    cursor4.execute(update_MAMMALS)
    
                else:
                    print "NORM"
                    update_MAMMALS = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_normal_mammal, wildlife_id)
                    cursor.execute(update_MAMMALS)
    
        elif species_category == "REPTILES":
            if gen_name == "Snake":
                # danger icon
                if endangered == "Endangered" or endangered == "Threatened":
                    cursor4 = connection.cursor()
                    update_REP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_rare_snake, wildlife_id)
                    cursor4.execute(update_REP)
                # rare icon
                elif harmful == "dangerous" or harmful == "venomous" or harmful == "poisonous":
                    cursor4 = connection.cursor()
                    update_REP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_danger_snake, wildlife_id)
                    cursor4.execute(update_REP)
    
                else:
                    cursor4 = connection.cursor()
                    update_REP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_normal_snake, wildlife_id)
                    cursor4.execute(update_REP)
    
            else:
                # danger icon
                if endangered == "Endangered" or endangered == "Threatened":
                    cursor4 = connection.cursor()
                    update_REP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_rare_reptile,  wildlife_id)
                    cursor4.execute(update_REP)
    
                # rare icon
                elif harmful == "dangerous" or harmful == "venomous" or harmful == "poisonous":
                    cursor4 = connection.cursor()
                    update_REP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_danger_reptile, wildlife_id)
                    cursor4.execute(update_REP)
    
                else:
                    cursor4 = connection.cursor()
                    update_REP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_normal_reptile, wildlife_id)
                    cursor4.execute(update_REP)
    
        else:
    
            if gen_name == "Frog":
                # danger icon
                if endangered == "Endangered" or endangered == "Threatened":
                    cursor4 = connection.cursor()
                    update_AMP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_rare_frog, wildlife_id)
                    cursor4.execute(update_AMP)
    
                # rare icon
                elif harmful == "dangerous" or harmful == "venomous" or harmful == "poisonous":
                    cursor4 = connection.cursor()
                    update_AMP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_danger_frog, wildlife_id)
                    cursor4.execute(update_AMP)
    
                else:
                    cursor4 = connection.cursor()
                    update_AMP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_normal_frog, wildlife_id)
                    cursor4.execute(update_AMP)
    
            else:
                # danger icon
                if endangered == "Endangered" or endangered == "Threatened":
                    cursor4 = connection.cursor()
                    update_AMP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_rare_amp, wildlife_id)
                    cursor4.execute(update_AMP)
    
                # rare icon
                elif harmful == "dangerous" or harmful == "venomous" or harmful == "poisonous":
                    cursor4 = connection.cursor()
                    update_AMP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_danger_amp, wildlife_id)
                    cursor4.execute(update_AMP)
    
                else:
                    cursor4 = connection.cursor()
                    update_AMP = """UPDATE dev_data.wildlife_pt SET marker = '{}' WHERE wildlife_id = {}""".format(marker_normal_amp, wildlife_id)
                    cursor4.execute(update_AMP)
    
        ##marker
        cursor.execute("SELECT marker FROM dev_data.wildlife_pt WHERE wildlife_id = {}".format(wildlife_id))
        marker = cursor.fetchone()[0]
        print marker

        ### PostGIS DEV to PostGIS PROD
        cursor10 = connection.cursor()
        #cursor10.execute('INSERT INTO prod_data.wildlife_pt (gen_name, com_name, sci_name, endangered, harmful, marker, species_category, username, comments, point, lat, long, encountered_date, encountered_time, ts_time, ts_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',(gen_name, com_name, sci_name, endangered, harmful, marker, species_category, username, comments, point, lat, long, encountered_date, encountered_time, ts_time, ts_date))
        cursor10.execute('INSERT INTO prod_data.wildlife_pt(gen_name, com_name, sci_name, endangered, harmful, marker, species_category, username, comments, point, lat, long, encountered_date, encountered_time, ts_time, ts_date) (SELECT gen_name, com_name, sci_name, endangered, harmful, marker, species_category, username, comments, point, lat, long, encountered_date, encountered_time, ts_time, ts_date FROM dev_data.wildlife_pt WHERE wildlife_id = {})'.format(wildlife_id))

        print "pushing to PROD"

        ### Remove DEV record
        cursor11 = connection.cursor()
        cursor11.execute('DELETE FROM dev_data.wildlife_pt WHERE wildlife_id = {}'.format(wildlife_id))

# commit to Database
connection.commit()