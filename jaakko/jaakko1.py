from ij import IJ
from ij.gui import Roi, ShapeRoi, PointRoi
from ij.measure import Measurements, ResultsTable
from ij.plugin.filter import ParticleAnalyzer as PA
from ij.plugin.filter import ThresholdToSelection
from ij.plugin.frame import RoiManager
from ij.gui import WaitForUserDialog as Wait

import glob
import sys

from java.lang import Double

inputDir = "/input/LMU-active2/Harri/Data/Jaakko/sample 0001.tif_Files/"

tmp = glob.glob(inputDir + "fibrone*")
fibronectin = tmp[0]
tmp = glob.glob(inputDir + "nucleus*")
nucleus = tmp[0]
tmp = glob.glob(inputDir + "actin*")
actin = tmp[0]

imp_fn = IJ.openImage(fibronectin)

IJ.run(imp_fn,"Set Scale...", "distance=1 known=1 pixel=1 unit=pixels")
IJ.run(imp_fn,"Gaussian Blur...","sigma=5")
IJ.run(imp_fn,"Make Binary","")
#IJ.run(imp_fn,"Invert","")
imp_fn.show()

# Create a table to store the results
rt = ResultsTable()
paOpts = PA.SHOW_OUTLINES \
        + PA.INCLUDE_HOLES \
        + PA.EXCLUDE_EDGE_PARTICLES
measurements = PA.CENTROID + PA.AREA
MINSIZE = 0
MAXSIZE = Double.POSITIVE_INFINITY
pa = PA(paOpts,measurements, rt, MINSIZE, MAXSIZE)
pa.setHideOutputImage(True)
 
if pa.analyze(imp_fn):
    print "All ok"
else:
    print "There was a problem in analyzing", imp_fn

# The measured centroids are listed in the first column of the results table, as a float array:
centroids_x = rt.getColumn(rt.X_CENTROID)
centroids_y = rt.getColumn(rt.Y_CENTROID)

cx = int(round(centroids_x[0]))
cy = int(round(centroids_y[0]))

fn_centroid_roi = PointRoi(cx,cy)
fn_centroid_roi.setDefaultMarkerSize("Large")

IJ.run(imp_fn,"Skeletonize","")
#imp_fn.getProcessor().drawRoi(fn_centroid_roi)
imp_fn.repaintWindow()
#wait = Wait("msg!")
#wait.show()


