'''
load species distribution shapefiles in postgis
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
cursor.execute("DELETE FROM basemap_data.species_distribution")

# Ubuntu path: /usr/share/wildlife_project/basemap_shp/
# iMac path: /Users/davidbailey/Desktop/Data/GIS_Data/basemap_shp/
# Macbook path: /Users/DavidBailey/Desktop/Data/GIS_Data/basemap_shp/

# get shapefiles from Ubuntu server
AMPHIBIANS_file = os.path.join("/Users/davidbailey/Desktop/Data/GIS_Data/basemap_shp/", "AMPHIBIANS.shp")
AMPHIBIANS_shp = osgeo.ogr.Open(AMPHIBIANS_file)
REPTILES_file = os.path.join("/Users/davidbailey/Desktop/Data/GIS_Data/basemap_shp/", "REPTILES.shp")
REPTILES_shp = osgeo.ogr.Open(REPTILES_file)
MAMMALS_file = os.path.join("/Users/davidbailey/Desktop/Data/GIS_Data/basemap_shp/", "MAMMALS.shp")
MAMMALS_shp = osgeo.ogr.Open(MAMMALS_file)
#FISH1_file = os.path.join("/Users/DavidBailey/Desktop/Bitbucket/wildlife_app/basemap_shp/", "MAMMALS.shp")
#FISH1_shp = osgeo.ogr.Open(FISH1_file)

# get AMPHIBIANS_shp binomial field, species category and geometry
layer1 = AMPHIBIANS_shp.GetLayer(0)
for s in layer1:

    geom = s.GetGeometryRef()
    binomial = s.binomial.decode('latin1')
    print binomial
    #feature = layer1.GetFeature(1)
    print geom

    category = "AMPHIBIANS"

    # force a polygon to multipolygon
    if geom.GetGeometryType() == osgeo.ogr.wkbPolygon:
        # if polygon then force to multipolygon then export geometry to WKT
        geom = osgeo.ogr.ForceToMultiPolygon(geom)
        wkt = geom.ExportToWkt()
        print "POLY"
        #cursor.execute("INSERT INTO basemap_data.species_distribution (sci_name,species_category,polygon) " + "VALUES (%s, %s, ST_GeometryFromText(%s, " + "4326))",(binomial.decode('utf8'), category, wkt))
    else:
    # if multipolygon then export geometry to WKT
        print "MULTI"
        wkt = geom.ExportToWkt()
        #cursor.execute("INSERT INTO basemap_data.species_distribution (sci_name,species_category,polygon) " + "VALUES (%s, %s, ST_GeometryFromText(%s, " + "4326))",(binomial.decode('utf8'), category, wkt))

# get REPTILES_shp binomial field, species category and geometry
layer1 = REPTILES_shp.GetLayer(0)
for s in layer1:

    geom = s.GetGeometryRef()
    binomial = s.binomial.decode('latin1')
    print binomial
    #feature = layer1.GetFeature(1)
    print geom

    category = "REPTILES"

    # force a polygon to multipolygon
    if geom.GetGeometryType() == osgeo.ogr.wkbPolygon:
        # if polygon then force to multipolygon then export geometry to WKT
        geom = osgeo.ogr.ForceToMultiPolygon(geom)
        wkt = geom.ExportToWkt()
        print "POLY"
        cursor.execute("INSERT INTO basemap_data.species_distribution (sci_name,species_category,polygon) " + "VALUES (%s, %s, ST_GeometryFromText(%s, " + "4326))",(binomial.decode('utf8'), category, wkt))
    else:
    # if multipolygon then export geometry to WKT
        print "MULTI"
        wkt = geom.ExportToWkt()
        cursor.execute("INSERT INTO basemap_data.species_distribution (sci_name,species_category,polygon) " + "VALUES (%s, %s, ST_GeometryFromText(%s, " + "4326))",(binomial.decode('utf8'), category, wkt))

# get MAMMALS_shp binomial field, species category and geometry
layer1 = MAMMALS_shp.GetLayer(0)
for s in layer1:

    geom = s.GetGeometryRef()
    binomial = s.binomial.decode('latin1')
    print binomial
    #feature = layer1.GetFeature(1)
    print geom

    category = "MAMMALS"

    # force a polygon to multipolygon
    if geom.GetGeometryType() == osgeo.ogr.wkbPolygon:
        # if polygon then force to multipolygon then export geometry to WKT
        geom = osgeo.ogr.ForceToMultiPolygon(geom)
        wkt = geom.ExportToWkt()
        print "POLY"
        cursor.execute("INSERT INTO basemap_data.species_distribution (sci_name,species_category,polygon) " + "VALUES (%s, %s, ST_GeometryFromText(%s, " + "4326))",(binomial.decode('utf8'), category, wkt))
    else:
    # if multipolygon then export geometry to WKT
        print "MULTI"
        wkt = geom.ExportToWkt()
        cursor.execute("INSERT INTO basemap_data.species_distribution (sci_name,species_category,polygon) " + "VALUES (%s, %s, ST_GeometryFromText(%s, " + "4326))",(binomial.decode('utf8'), category, wkt))

# commit to Database
connection.commit()
