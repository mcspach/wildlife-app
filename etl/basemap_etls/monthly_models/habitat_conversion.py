'''
update critical_habitat table in postgis
by D. Bailey
'''

import os.path
import psycopg2
import osgeo.ogr

# run as dbailey on Ubuntu server

# input for password
enter_pass = raw_input("Enter Password for basemap_user: ")

# connection variables
db = "dbname='wildlife_db'"
user = "user='basemap_user'"
host = "host='138.68.62.194'"
passw = "password=" + enter_pass

# connect to postgis
connection = psycopg2.connect(db + user + host + passw)
cursor = connection.cursor()

# drop tables first
#cursor.execute("DELETE FROM basemap_data.wetlands")
cursor.execute("DELETE FROM basemap_data.fws_critical_habitat")

# Ubuntu path: /usr/share/wildlife_project/basemap_shp/
# iMac path: /Users/davidbailey/Desktop/Data/GIS_Data/basemap_shp/
# Macbook path: /Users/DavidBailey/Desktop/Data/GIS_Data/basemap_shp/

# get shapefiles - https://www.fws.gov/gis/data/national/
critical_habitat_file = os.path.join("/Users/davidbailey/Desktop/Data/GIS_Data/basemap_shp/", "CRITHAB_POLY.shp")
critical_habitat_shp = osgeo.ogr.Open(critical_habitat_file)

# get CRITICAL HABITAT com_name, sci_name, status, habitat_type field and geometry
layer1 = critical_habitat_shp.GetLayer(0)
for s in layer1:
    geom = s.GetGeometryRef()
    comname = s.comname.decode('latin1')
    sciname = s.sciname.decode('latin1')
    listing_st = s.listing_st.decode('latin1')
    print comname
    #feature = layer1.GetFeature(1)
    print geom


    # force a polygon to multipolygon
    if geom.GetGeometryType() == osgeo.ogr.wkbPolygon:
        # if polygon then force to multipolygon then export geometry to WKT
        geom = osgeo.ogr.ForceToMultiPolygon(geom)
        wkt = geom.ExportToWkt()
        print "POLY"
        cursor.execute("INSERT INTO basemap_data.fws_critical_habitat (com_name,sci_name,status,polygon) " + "VALUES (%s, %s, %s, ST_GeometryFromText(%s, " + "4326))",(comname.decode('utf8'), sciname.decode('utf8'), listing_st, wkt))
    else:
    # if multipolygon then export geometry to WKT
        print "MULTI"
        wkt = geom.ExportToWkt()
        cursor.execute("INSERT INTO basemap_data.fws_critical_habitat (com_name,sci_name,status,polygon) " + "VALUES (%s, %s, %s, ST_GeometryFromText(%s, " + "4326))",(comname.decode('utf8'), sciname.decode('utf8'), listing_st, wkt))

# commit to Database
connection.commit()
