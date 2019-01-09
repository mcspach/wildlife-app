'''
load basemap shapefiles into postgis
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
#cursor.execute("DELETE FROM basemap_data.state") DONE
#cursor.execute("DELETE FROM basemap_data.city") DONE
#cursor.execute("DELETE FROM basemap_data.county") DONE
#cursor.execute("DELETE FROM basemap_data.ecoregions") DONE
#cursor.execute("DELETE FROM basemap_data.national_forest") DONE
#cursor.execute("DELETE FROM basemap_data.national_park") DONE

cursor.execute("DELETE FROM basemap_data.state_park")
cursor.execute("DELETE FROM basemap_data.country")


# get shapefiles
#ecoregion_file = os.path.join("/Users/DavidBailey/Desktop/Bitbucket/wildlife_app/basemap_shp/", "FWS_Ecoregions.shp")
#ecoregion_shp = osgeo.ogr.Open(ecoregion_file)
#national_forest_file = os.path.join("/Users/DavidBailey/Desktop/Bitbucket/wildlife_app/basemap_shp/", "S_USA.AdministrativeForest.shp")
#national_forest_shp = osgeo.ogr.Open(national_forest_file)
#national_park_file = os.path.join("/Users/DavidBailey/Desktop/Bitbucket/wildlife_app/basemap_shp/", "ne_10m_parks_and_protected_lands_area.shp")
#national_park_shp = osgeo.ogr.Open(national_park_file)
state_park_file = os.path.join("/Users/DavidBailey/Desktop/Bitbucket/wildlife_app/basemap_shp/", "caStateParkBdysMapLinks201603e.shp")
state_park_shp = osgeo.ogr.Open(state_park_file)
countries_file = os.path.join("/Users/DavidBailey/Desktop/Bitbucket/wildlife_app/basemap_shp/", "TM_WORLD_BORDERS_SIMPL-0.3.shp")
countries_shp = osgeo.ogr.Open(countries_file)

'''
state_file = os.path.join("/Users/DavidBailey/Desktop/Bitbucket/wildlife_app/basemap_shp/", "cb_2017_us_state_5m.shp")
state_shp = osgeo.ogr.Open(state_file)
co_file = os.path.join("/Users/DavidBailey/Desktop/Bitbucket/wildlife_app/basemap_shp/", "cb_2017_us_county_5m.shp")
co_shp = osgeo.ogr.Open(co_file)
ci_file = os.path.join("/Users/DavidBailey/Desktop/Bitbucket/wildlife_app/basemap_shp/", "cb_2017_us_ua10_500k.shp")
ci_shp = osgeo.ogr.Open(ci_file)
'''

# get COUNTRY name field and geometry
layer1 = countries_shp.GetLayer(0)
for s in layer1:
    geom = s.GetGeometryRef()
    name = s.name.decode('latin1')
    print name
    # feature = layer1.GetFeature(1)
    print geom

    try:

        # force a polygon to multipolygon
        if geom.GetGeometryType() == osgeo.ogr.wkbPolygon:
            # if polygon then force to multipolygon then export geometry to WKT
            geom = osgeo.ogr.ForceToMultiPolygon(geom)
            wkt = geom.ExportToWkt()
            print "POLY"
            cursor.execute(
                "INSERT INTO basemap_data.country (name,polygon) " + "VALUES (%s, ST_GeometryFromText(%s, " + "4326))",
                (name.decode('utf8'), wkt))
        else:
            # if multipolygon then export geometry to WKT
            print "MULTI"
            wkt = geom.ExportToWkt()
            cursor.execute(
                "INSERT INTO basemap_data.country (name,polygon) " + "VALUES (%s, ST_GeometryFromText(%s, " + "4326))",
                (name.decode('utf8'), wkt))

    except:

        print "ERROR"

        # force a polygon to multipolygon
        if geom.GetGeometryType() == osgeo.ogr.wkbPolygon:
            # if polygon then force to multipolygon then export geometry to WKT
            geom = osgeo.ogr.ForceToMultiPolygon(geom)
            wkt = geom.ExportToWkt()
            print "POLY"
            cursor.execute(
                "INSERT INTO basemap_data.country (name,polygon) " + "VALUES (%s, ST_GeometryFromText(%s, " + "4326))",
                (name, wkt))
        else:
            # if multipolygon then export geometry to WKT
            print "MULTI"
            wkt = geom.ExportToWkt()
            cursor.execute(
                "INSERT INTO basemap_data.country (name,polygon) " + "VALUES (%s, ST_GeometryFromText(%s, " + "4326))",
                (name, wkt))
'''
# get NATIONAL PARK name field and geometry
layer1 = state_park_shp.GetLayer(0)
for s in layer1:
    geom = s.GetGeometryRef()
    unitname = s.unitname.decode('latin1')
    print unitname
    # feature = layer1.GetFeature(1)
    print geom


    # force a polygon to multipolygon
    if geom.GetGeometryType() == osgeo.ogr.wkbPolygon:
        # if polygon then force to multipolygon then export geometry to WKT
        geom = osgeo.ogr.ForceToMultiPolygon(geom)
        wkt = geom.ExportToWkt()
        print "POLY"
        cursor.execute(
            "INSERT INTO basemap_data.state_park (name,polygon) " + "VALUES (%s, ST_GeometryFromText(%s, " + "4326))",
            (unitname.decode('utf8'), wkt))
    else:
        # if multipolygon then export geometry to WKT
        print "MULTI"
        wkt = geom.ExportToWkt()
        cursor.execute(
            "INSERT INTO basemap_data.state_park (name,polygon) " + "VALUES (%s, ST_GeometryFromText(%s, " + "4326))",
            (unitname.decode('utf8'), wkt))

        #Latin-1
'''
# commit to Database
connection.commit()
