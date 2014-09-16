from ij import IJ
from ij.measure import ResultsTable

import sys

inputFile = "/input/LMU-active2/Harri/Data/Jaakko/sample 0001.tif_Files/fibronect 0001_c0.tif"
inputFile = sys.argv[1]
print inputFile

imp = IJ.openImage(inputFile)
IJ.run(imp,"Set Scale...", "distance=1 known=1 pixel=1 unit=pixels")
IJ.run(imp,"Gaussian Blur...","sigma=5")
IJ.run(imp,"Make Binary","")

IJ.run(imp,"Image Moments", "order=3")
#rt = ResultsTable.getResultsTable()
#print rt.getColumnHeadings()


