from ij import IJ, ImagePlus
from ij.gui import Roi, ShapeRoi, PointRoi
from ij.measure import Measurements, ResultsTable
from ij.plugin.filter import ParticleAnalyzer as PA
from ij.plugin.filter import ThresholdToSelection
from ij.plugin.frame import RoiManager
from ij.gui import WaitForUserDialog as Wait

from skeleton_analysis import AnalyzeSkeleton_,Graph,Edge,Vertex 

import glob
import math
import sys

from java.lang import Double
from java.awt import Color

inputDir = "/input/LMU-active2/Harri/Data/Jaakko/sample 0001.tif_Files/"

def getParticleCenters(imp):
    # Create a table to store the results
    rt = ResultsTable()
    paOpts = PA.SHOW_OUTLINES \
            + PA.INCLUDE_HOLES \
            + PA.EXCLUDE_EDGE_PARTICLES
    measurements = PA.CENTROID + PA.CENTER_OF_MASS
    MINSIZE = 0
    MAXSIZE = Double.POSITIVE_INFINITY
    pa = PA(paOpts,measurements, rt, MINSIZE, MAXSIZE)
    pa.setHideOutputImage(True)
     
    if not pa.analyze(imp):
        print "There was a problem in analyzing", imp

    # The measured centroids are listed in the first column of the results table, as a float array:
    centroids_x = rt.getColumn(rt.X_CENTROID)
    centroids_y = rt.getColumn(rt.Y_CENTROID)
    coms_x = rt.getColumn(rt.X_CENTER_OF_MASS)
    coms_y = rt.getColumn(rt.Y_CENTER_OF_MASS)

    return (centroids_x,centroids_y, coms_x, coms_y)

def processOneImage(inputDir):
    tmp = glob.glob(inputDir + "fibrone*")
    fibronectin = tmp[0]
    tmp = glob.glob(inputDir + "nucleus*")
    nucleus = tmp[0]
    tmp = glob.glob(inputDir + "actin*")
    actin = tmp[0]

    # original images
    imp_fn_orig = IJ.openImage(fibronectin)
    imp_nuc_orig = IJ.openImage(nucleus)

    # work copies
    imp_fn = imp_fn_orig.duplicate()
    imp_nuc = imp_nuc_orig.duplicate()

    IJ.run(imp_fn,"Set Scale...", "distance=1 known=1 pixel=1 unit=pixels")
    IJ.run(imp_fn,"Gaussian Blur...","sigma=5")
    IJ.run(imp_fn,"Make Binary","")
    IJ.run(imp_nuc,"Set Scale...", "distance=1 known=1 pixel=1 unit=pixels")
    IJ.run(imp_nuc,"Gaussian Blur...","sigma=5")
    IJ.run(imp_nuc,"Make Binary","")

    
    # centroid of fibronectin anchor
    centers = getParticleCenters(imp_fn)
    cxfn = int(round(centers[0][0]))
    cyfn = int(round(centers[1][0]))
    fn_centroid_roi = PointRoi(cxfn,cyfn)
    fn_centroid_roi.setDefaultMarkerSize("Large")
    fn_centroid_roi.setStrokeColor(Color.CYAN)

    # center of mass of nucleus 
    centers = getParticleCenters(imp_nuc)
    cxnuc = int(round(centers[2][0]))
    cynuc = int(round(centers[3][0]))
    nuc_com_roi = PointRoi(cxnuc,cynuc)
    nuc_com_roi.setDefaultMarkerSize("Large")

    # skeletonize fibronectin anchor to find its orientation
    IJ.run(imp_fn,"Skeletonize","")
    skel = AnalyzeSkeleton_()
    skel.setup("",imp_fn)
    skelResult = skel.run(skel.NONE, False, True, None, True, True)
    graph = skelResult.getGraph()
    print len(graph)
    print skelResult.getNumOfTrees()
    graph = graph[0]
    edges = graph.getEdges()
    # find longest edge, the main axis of the anchor
    edges = sorted(edges, key=lambda edge: edge.getLength(), reverse=True)
    #for e in edges:
    #    print e.getLength()
    v1long = edges[0].getV1()
    v2long = edges[0].getV2()
    x1 = v1long.getPoints()[0].x
    y1 = v1long.getPoints()[0].y
    x2 = v2long.getPoints()[0].x
    y2 = v2long.getPoints()[0].y
    anchor_roi = PointRoi(x1,y1)
    anchor_roi = anchor_roi.addPoint(x2,y2)
    # find top and bottom vertices of the graph
    vertices = graph.getVertices()
    vertices = sorted(vertices, key=lambda vertex: vertex.getPoints()[0].y)
    v1short = vertices[len(vertices)-1]
    v2short = vertices[0]
    x3 = v1short.getPoints()[0].x
    y3 = v1short.getPoints()[0].y
    x4 = v2short.getPoints()[0].x
    y4 = v2short.getPoints()[0].y
    anchor_roi = anchor_roi.addPoint(x3,y3)
    anchor_roi = anchor_roi.addPoint(x4,y4)
    # calculate angles
    a1 = math.atan(float(y2-y1)/float(x2-x1))
    a2 = math.atan(float(x4-x3)/float(y3-y4))
    print x1,y1,x2,y2,x3,y3,x4,y4,a1,a2

    # create composite
    print "creating composite"
    comp = ImagePlus("composite",imp_nuc_orig.getProcessor().convertToColorProcessor())
    comp.getProcessor().setChannel(2,imp_fn_orig.getProcessor())
    comp.getProcessor().setChannel(3,imp_fn.getProcessor())
    comp.show()
    comp.getProcessor().drawRoi(fn_centroid_roi)
    comp.getProcessor().drawRoi(nuc_com_roi)
    comp.getProcessor().drawRoi(anchor_roi)
    comp.repaintWindow()
    IJ.saveAsTiff(comp,"/output/" + "comp_jaakko1.tif")

    #IJ.run(imp_fn, "Analyze Skeleton (2D/3D)","show")
    #wait = Wait("msg!")
    #wait.show()


processOneImage(inputDir)
