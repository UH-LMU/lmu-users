import csv
import os
import sys

# file names
FILE_CELLS = "MyExpt_CellsGFP.csv"
FILE_CELLS_MINUS_SPOTS = "MyExpt_CellsGFPMinusSpots.csv"
FILE_SPOTS = "MyExpt_SpotsInCellsGFP.csv"

# csv headers
#H_OBJECT_NUMBER = "Number_Object_Number"
H_OBJECT_NUMBER = "ObjectNumber"
H_PARENT_NUMBER = "Parent_CellsGFP"
H_SPOT_COUNT = "Children_SpotsInCellsGFP_Count"
H_SPOT_AREA = "Mean_SpotsInCellsGFP_AreaShape_Area"
H_LC3 = "Intensity_IntegratedIntensity_LC3"
H_IMAGE = "ImageT"

def processSubfolder(folder,subfolder,cellList):
    cells = None
    cellsMinusSpots = None
    spots = None
    f1 = open(os.path.join(folder,subfolder,FILE_CELLS))
    cells = csv.DictReader(f1)
    f2 = open(os.path.join(folder,subfolder,FILE_CELLS_MINUS_SPOTS))
    #cellsMinusSpots = csv.DictReader(f2)
    cellsMinusSpots = []
    for row in csv.DictReader(f2):
        cellsMinusSpots.append(row)
    f3 = open(os.path.join(folder,subfolder,FILE_SPOTS))
    #spots = csv.DictReader(f3)
    spots = []
    for row in csv.DictReader(f3):
        spots.append(row)

    for c in cells:
        #print subfolder
        #print c[H_OBJECT_NUMBER]
        #print c[H_SPOT_COUNT]
        #print c[H_SPOT_AREA]
        #print

        # check if cell is accepted
        if not "%s,%s"%(subfolder,c[H_OBJECT_NUMBER]) in cellList:
            print "%s,%s,not accepted"%(subfolder,c[H_OBJECT_NUMBER])
            continue

        lc3cell = 0
        for cms in cellsMinusSpots:
            #print cms
            #if cms[H_PARENT_NUMBER] == c[H_OBJECT_NUMBER]:
            if cms[H_OBJECT_NUMBER] == c[H_OBJECT_NUMBER]:
                lc3cell = cms[H_LC3]
        # print

        lc3spots = 0
        for s in spots:
            if s[H_PARENT_NUMBER] == c[H_OBJECT_NUMBER]:
                lc3spots = lc3spots + float(s[H_LC3])
        # print lc3spots
        # print

        print "%s,%s,%s,%s,%s,%.3f" % (subfolder,c[H_OBJECT_NUMBER],c[H_SPOT_COUNT],c[H_SPOT_AREA],lc3cell,lc3spots)
    f1.close()
    f2.close()
    f3.close()

# first command line argument is the folder with the data to process
folder = sys.argv[1]
#print folder
subfolders = []
for entry in os.listdir(folder):
	#print entry
	if os.path.isdir(os.path.join(folder, entry)):
		subfolders.append(entry)

# second command line argument is the file with the accepted cells listed
#print sys.argv[2]
cellListFile = open(sys.argv[2])
cellList = cellListFile.readlines()
cellListFile.close()
for i in range(0,len(cellList)):
    cellList[i] = cellList[i].rstrip()

#for c in cellList:
#    print c

print "%s,%s,%s,%s,%s,%s" % (H_IMAGE,H_OBJECT_NUMBER,H_SPOT_COUNT,H_SPOT_AREA,H_LC3 + "_Cell",H_LC3 + "_Spots")
for s in subfolders:
    processSubfolder(folder,s,cellList)
