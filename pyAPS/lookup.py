# HS Lookup Library

# Horner and Shifrin
# Author: Andrew Schreiber
# Created: 3/18/16
# Modified: 3/18/16

#####################################

#####################################

import arcpy, sys, traceback, os, glob

# Clients lookup
class Client:
    AltonMO = 'AltonMO'
    ArbyrdMO = 'ArbyrdMO'
    BirchTree = 'BirchTree'
    Butler = 'Butler'

# WKID Lookup
class WKID:
    SPMOe = 102696
    SPMOw = 102698
    SPILe = 3435
    SPILw = 3436
    WGS84 = 4326
    WebMecAux = 3857
    UTM15N = 26915

# Get database connection file
def get_db_conn(client):
    map_data_dir = r"\\arcserve1\MapData"
    os.chdir(map_data_dir)
    for conn in glob.glob("*.sde"):
        if conn.find(client) and conn.find('TEST') == -1:
            return map_data_dir + os.sep + conn
    return "No production connection file found."
    
try:

    pass

except:

    print "exception"

    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n     " + str(sys.exc_info()[1])
  
    msgs = "ARCPY ERRORS:\n" + arcpy.GetMessages(2) + "\n"
  
    arcpy.AddError(msgs)
    arcpy.AddError(pymsg)
  
    print msgs
    print pymsg
      
    arcpy.AddMessage(arcpy.GetMessages(1))
    print arcpy.GetMessages(1)

#####

    msgs = arcpy.GetMessages(2)

    #print msgs

    arcpy.SetParameterAsText(5, msgs)
