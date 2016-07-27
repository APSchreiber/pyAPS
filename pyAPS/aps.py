# APS python library

# Horner and Shifrin
# Author: Andrew Schreiber
# Created: 3/18/16
# Modified: 

#####################################




#####################################

import arcpy, sys, traceback, os, zipfile, PIL, Image, csv, winsound

### GENERAL ###

# Test if module is loaded
def testload():
    print "APS module successfully loaded."

# Extract/unzip files/folders in a directory
def extract_all(directory):
    files_list = os.listdir(directory)
    for the_file in files_list:
        if the_file[-3:].lower() == "zip":
            file_path = directory + os.sep + the_file
            file_ref = zipfile.ZipFile(file_path, "r")
            zip_to_directory = file_path[:-4]
            #print "\nextracting " + the_file + " to directory '" + zip_to_directory + "'."
            file_ref.extractall(zip_to_directory)
            file_ref.close()


### BASEMAP TOOLS ###


### LAYER TOOLS ###

# Make feature layers from a list of features
def make_feature_layers(features, workspace):
    """
    Make feature layers from a list  of layer names
    """
    if workspace:
        
        arcpy.MakeFeatureLayer_management(in_features, out_layer, {where_clause}, {workspace}, {field_info})


### CATALOG TOOLS ###

# Batch define projections in a given workspace
def batch_define_projection(wkid, workspace):
    """
    Batch define projections in a given workspace.
    """
    if workspace:
        arcpy.env.workspace = workspace
    arcpy.env.addOutputsToMap = False
    sr = arcpy.SpatialReference(wkid)
    fcs = arcpy.ListFeatureClasses()
    for fc in fcs:
        current_sr = arcpy.Describe(fc).spatialReference
        if current_sr != sr:
            arcpy.DefineProjection_management(fc, sr)

### PROJECTION, TRANSFORMATION, AND SCALING TOOLS ###

def ground_to_grid(workspace, fc, factor, where_clause='1=1'):
        arcpy.env.workspace = workspace
	arcpy.MakeFeatureLayer_management (fc, 'fl', where_clause)
	with arcpy.da.Editor(workspace) as edit:
		field_names = ('SHAPE@X', 'SHAPE@Y')
		cursor = arcpy.da.UpdateCursor('fl', field_names)
		for row in cursor:
			row[0] = (row[0] * factor)
			row[1] = (row[1] * factor)
			cursor.updateRow(row)
			del row
		del cursor
						
### DATA TRANSFER TOOLS ###
def copy_attributes_spatial(workspace, source_fc, target_fc, source_fields, target_fields):
    arcpy.env.workspace = workspace
    arcpy.env.addOutputsToMap = False
    arcpy.MakeFeatureLayer_management(source_fc, "source_fl")
    arcpy.MakeFeatureLayer_management(target_fc, "target_fl")
    sc = arcpy.SearchCursor(source_fc)
    with arcpy.da.Editor(workspace) as edit:
        for row in sc:
            arcpy.SelectLayerByAttribute_management("source_fl", "NEW_SELECTION", "OBJECTID = " + str(row.OBJECTID))
            arcpy.SelectLayerByLocation_management("target_fl", "", "source_fl", "", "NEW_SELECTION")
            uc = arcpy.UpdateCursor("target_fl")
            for urow in uc:
                for sf in source_fields:
                    ind = source_fields.index(sf)
                    setattr(urow, target_fields[ind], getattr(row, sf))
                uc.updateRow(urow)
                del urow
            del uc
            del row
    del sc

#def copy_attributes_id(workspace, source_fc, target_fc, source_id_field, source_fields, target_id_field, target_fields):
def copy_attributes_id(workspace, source_fc=1, target_fc=1, source_id_field=1, source_fields=1, target_id_field=1, target_fields=1):

    # Test case
    if workspace == 'test':
        #workspace = r"C:\Scratch\ILAWC\ILAWC_Test.gdb"
        workspace = r"\\ARCSERVE1\MapData\ILAWCConn_SDE.sde"
        source_fc = "WaterMainsCorrected"
        target_fc = "WaterMains"
        source_id_field = "WMnNo"
        source_fields = ("GNSS_Height", "Vert_Prec", "Horz_Prec")
        target_id_field = "WMnNo"
        target_fields = ("GNSS_Height", "Vert_Prec", "Horz_Prec")
    
    arcpy.env.workspace = workspace
    arcpy.env.addOutputsToMap = False
    arcpy.MakeFeatureLayer_management(source_fc, "source_fl")
    arcpy.MakeFeatureLayer_management(target_fc, "target_fl")
    #sc = arcpy.da.SearchCursor(source_fc, ("SHAPE@X", "SHAPE@Y", source_id_field))
    sc = arcpy.da.SearchCursor(source_fc, ("SHAPE@X", "SHAPE@Y", source_id_field) + source_fields)
    with arcpy.da.Editor(workspace) as edit:
        #d = 800
        for row in sc:
            source_feature_id = row[2]
            #target_field_type = (x for x in arcpy.ListFields(target_fc) if x == target_id_field)[0].type
            #if target_field_type == 'String':
            where_clause = str(target_id_field) + " = '" + str(source_feature_id) + "'"
            print "AHHH"
            #winsound.Beep(d, 100)
            #d += 5
            #uc = arcpy.da.UpdateCursor(target_fc, ("SHAPE@X", "SHAPE@Y"), where_clause)
            uc = arcpy.da.UpdateCursor(target_fc, ("SHAPE@X", "SHAPE@Y") + target_fields, where_clause)
            for urow in uc:
                try:
                    print row[0], row[1]

                    urow[0] = row[0]
                    urow[1] = row[1]

                    urow[2] = row[3]
                    urow[3] = row[4]
                    urow[4] = row[5]

                    uc.updateRow(urow)
                except:
                    pass
                
                del urow
            del uc
            del row
    del sc

def find_duplicates(dataset, id_field_list=('CasNo', 'FldTapNum', 'FitNo', 'FldTapNo', 'SMnNo', 'HydNo', 'WMnNo', 'WMtrNo', 'WMtrPitNo', 'WVlvNo')):
    arcpy.env.workspace = dataset
    fcs = arcpy.ListFeatureClasses()
    for fc in fcs:
        print
        print fc
        fields = arcpy.ListFields(fc)
        for field in fields:
            if field.name in id_field_list:
                ids = []
                dupes = []
                sc = arcpy.SearchCursor(fc)
                for row in sc:
                    if (getattr(row, field.name)).lower() not in ids:
                        ids.append((getattr(row, field.name)).lower())
                    else:
                        dupes.append(getattr(row, field.name))
                    del row
                del sc
                for dupe in dupes:
                    print dupe

def find_counts(dataset):
    arcpy.env.workspace = dataset
    fcs = arcpy.ListFeatureClasses()
    for fc in fcs:
        print
        print fc
        sc = arcpy.SearchCursor(fc)
        count = 0
        for row in sc:
            count += 1
            del row
        del sc
        print "Features: " + str(count)

### IMAGE TOOLS ###

# Turn an ArcGIS Attachment into an Image file
def attachment_to_file(out_dir, featureid, data, attachment_name):
    # attach_fields = ('REL_GLOBALID', 'DATA', 'ATTACHMENTID', 'ATT_NAME')
    output_image_file = out_dir + os.sep + featureid + "_" + attachment_name
    open(output_image_file, 'wb').write(data)

# Convert an image to a different format
def convert_image_format(working_dir, image, ext):
    img = Image.open(working_dir + os.sep + image)
    img.save(image[:-3] + ext)
    

### ERROR HANDLING ###

# Handle exceptions
def handle_exception():
    """
    Handle exceptions
    """
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
    msgs = arcpy.GetMessages(2)
    arcpy.SetParameterAsText(5, msgs)


