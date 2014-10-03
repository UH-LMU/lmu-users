from ij import IJ
from ij.gui import PointRoi

from java.awt import Color

import csv
import math
import os
import sys

LINE_DX = 300

def draw_centers(data):
    pathname = data[1]
    filename = data[2]

    nx = int(round(float(data[3])))
    ny = int(round(float(data[4])))
    ax = int(round(float(data[5])))
    ay = int(round(float(data[6])))
    
    orientation = 2*math.pi * float(data[7]) / 360.0
    line_dy = int(round(math.atan(orientation) * LINE_DX))
    ax2 = ax - LINE_DX
    ay2 = ay - line_dy

    imp = IJ.openImage(os.path.join(pathname,filename))

    roi_nucleus = PointRoi(nx,ny)
    roi_nucleus.setDefaultMarkerSize("Large")
    roi_nucleus.setStrokeColor(Color.CYAN)
    roi_anchor = PointRoi(ax,ay)
    roi_anchor.setDefaultMarkerSize("Large")
 
    imp.getProcessor().drawRoi(roi_nucleus)
    imp.getProcessor().drawRoi(roi_anchor)

    imp.setColor(Color.WHITE)
    imp.getProcessor().drawLine(ax,ay,ax2,ay2)

    IJ.saveAsTiff(imp,os.path.join(pathname,filename))

f = open(sys.argv[1], 'rb') 
try:
    reader = csv.reader(f,quotechar="'")
    for row in reader:
        draw_centers(row)
        #sys.exit()
finally:
    f.close()
