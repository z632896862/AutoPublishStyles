"""
gsconfig is a python library for manipulating a GeoServer instance via the GeoServer RESTConfig API.

The project is distributed under a MIT License .
"""

__author__ = "David Winslow"
__copyright__ = "Copyright 2012-2015 Boundless, Copyright 2010-2012 OpenPlans"
__license__ = "MIT"


def shapefile_and_friends(path):
    return {ext: path + "." + ext for ext in ['shx', 'shp', 'dbf', 'prj']}
