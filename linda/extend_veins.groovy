import qupath.lib.objects.PathDetectionObject
import qupath.lib.objects.classes.PathClass
import qupath.lib.scripting.QP
//import qupath.lib.geom.GeometryTools
import org.locationtech.jts.geom.Geometry
import org.locationtech.jts.operation.buffer.BufferOp
import org.locationtech.jts.geom.util.GeometryCombiner
import qupath.lib.regions.ImagePlane

// Parameters
def veinClass = PathClass.fromString("vein")
def bufferPixels = 300

// Image & scale info
def imageData = QP.getCurrentImageData()
def server = imageData.getServer()
def pixelSize = server.getPixelCalibration().getAveragedPixelSize()
def bufferMicrons = bufferPixels * pixelSize
def plane = ImagePlane.getDefaultPlane()

// Remove previous results
def expandedVeinClass = PathClass.fromString("expandedVein")
def oldExpanded = QP.getDetectionObjects().findAll { it.getPathClass() == expandedVeinClass }
QP.removeObjects(oldExpanded, true)

// Get all vein detections
def veinDetections = QP.getDetectionObjects().findAll { it.getPathClass() == veinClass }
if (veinDetections.isEmpty()) {
    print "No vein detections found."
    return
}

// Step 1: Dilate all vein geometries
def bufferedGeoms = veinDetections.collect { det ->
    BufferOp.bufferOp(det.getROI().getGeometry(), bufferMicrons)
}

// Step 2: Union all buffered geometries
def unioned = GeometryCombiner.combine(bufferedGeoms).union()

// Step 3: Split unioned result into separate geometries
def numGeometries = unioned.getNumGeometries()
def components = (0..<numGeometries).collect { unioned.getGeometryN(it) }

// Step 4: For each component, find intersecting original veins, merge originals
def mergedObjects = components.collect { geom ->
    def roi = GeometryTools.geometryToROI(geom, plane)
    new PathDetectionObject(roi, expandedVeinClass)
}

// Step 5: Add to viewer
QP.addObjects(mergedObjects)
print "Original veins: ${veinDetections.size()}, Expanded merged clusters: ${mergedObjects.size()}"
