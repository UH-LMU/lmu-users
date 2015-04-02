import csv
from ij import IJ
from ij.gui import PointRoi
from ConfigParser import SafeConfigParser
from java.awt import Color
import os
import string, sys

config = SafeConfigParser()
config.read("config.ini")

OUTPUTROOT = config.get('main','outputdir')

classes = {}
for i in config.items("classes"):
    classes[i[1]] = i[0]
print classes

colors = {}
for i in config.items("colors"):
    colors[i[0]] = i[1]
print colors

colormap = {}
colormap["red"] = Color.red
colormap["green"] = Color.green
colormap["blue"] = Color.blue

def draw_classes(inputfile,data):

    pathname,filename = os.path.split(inputfile)

    # last subdir is for well
    ## TODO ## support multiple plates, read plate and well from csv
    well = os.path.basename(pathname)

    # create output directory
    outputdir = os.path.join(OUTPUTROOT,well)
    if not os.path.isdir(outputdir):
        os.makedirs(outputdir)

    # create output filename
    head,tail = os.path.splitext(filename)
    outputfilename = head + "_classes" + tail
    outputfilename = os.path.join(outputdir,outputfilename)
    print outputfilename

    imp = IJ.openImage(inputfile).duplicate()
    IJ.run(imp,"RGB Color","")

    for d in data:
        x = int(float(d[0]))
        y = int(float(d[1]))
        c = int(float(d[2]))

        classname = classes[str(c)]
        colorname = colors[classname]
        color = colormap[colorname]
        #print colorname

        roi = PointRoi(x,y)
        roi.setDefaultMarkerSize("Large")
        roi.setStrokeColor(colormap[colorname])
        
        imp.getProcessor().drawRoi(roi)

    IJ.saveAs(imp,"png",outputfilename)
    #IJ.saveAsTiff(imp,outputfilename)


# store images and objects
inputs = {}

f = open(sys.argv[1], 'rb') 
try:
    reader = csv.reader(f,quotechar="'")

    # skip header row
    # reader.next()

    for data in reader:
        pathname = data[1]
        filename = data[2]
        x = int(float(data[3]))
        y = int(float(data[4]))
        c = int(float(data[5]))

        # fix pathname for Linux
        pathname = string.replace(pathname,"Y:\\\\","/input/")
        pathname = string.replace(pathname,"\\","/")

        # read input image
        inputfile = os.path.join(pathname,filename)
        #print inputfile

        if not inputs.has_key(inputfile):
            #print "new inputfile"
            inputs[inputfile] = []
        inputs[inputfile].append((x,y,c))

        #draw_class(row)
        #sys.exit()
finally:
    f.close()

#print sorted(inputs.keys())

#sys.exit()

for i in sorted(inputs.keys()):
    draw_classes(i,inputs[i])

