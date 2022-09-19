from ij import IJ,ImagePlus
from loci.plugins.in import ImagePlusReader,ImporterOptions,ImportProcess
import os
import os.path
import sys




def iterateLif(filename,impProcessor):
    """
    Iterate over all series in a LIF file and process them.
    Arguments:
    filename: LIF filename
    impProcessor: processor object, implements method process(ImagePlus).
    """

    opts = ImporterOptions()
    opts.setId(filename)
    opts.setUngroupFiles(True)

    # set up import process
    process = ImportProcess(opts)
    process.execute()
    nseries = process.getSeriesCount()

    # reader belonging to the import process
    reader = process.getReader()

    # reader external to the import process
    impReader = ImagePlusReader(process)
    for i in range(0, nseries):
        print "iterateLif: %d/%d %s" % (i+1, nseries, process.getSeriesLabel(i))

        # activate series (same as checkbox in GUI)
        opts.setSeriesOn(i,True)

        # point import process reader to this series
        reader.setSeries(i)

        # read and process all images in series
        imps = impReader.openImagePlus()
        for imp in imps:
            imp.setTitle("%s_%d_%d" % (imp.getTitle(),i+1,nseries))
            print "iterateLif: " + imp.getTitle()
            try:
                impProcessor.process(imp)
            finally:
                imp.close()

        # deactivate series (otherwise next iteration will have +1 active series)
        opts.setSeriesOn(i, False)

from ij.plugin import ChannelSplitter
from ij.plugin import ZProjector
from ij.process import LUT
from java.awt import Color

class SamuLifProcessor:
    """
    <imagej> process_lifs.py <inputDirectory> <outputDirectory>
    Fiji.app/ImageJ-linux64 process_lifs.py ./input/ ./output/
    """

    def __init__(self,outputDir):
        self.outputDir = outputDir

    # Thanks to:
    # https://wiki.cmci.info/documents/120206pyip_cooking/python_imagej_cookbook#channel_splitter
        
    def maxZprojection(self, stackimp):
	zp = ZProjector(stackimp)
	zp.setMethod(ZProjector.MAX_METHOD)
	zp.doProjection()
	zpimp = zp.getProjection()
	return zpimp

    
    def process(self,imp):
        imps = ChannelSplitter.split(imp)
        c1 = imps[1]
        c2 = imps[2]

        c1.setTitle(imp.getTitle() + "_c1")
        c2.setTitle(imp.getTitle() + "_c2")

        z1 = self.maxZprojection(c1)
        z2 = self.maxZprojection(c2)

        z1.getProcessor().setLut(LUT.createLutFromColor(Color.MAGENTA))
        z2.getProcessor().setLut(LUT.createLutFromColor(Color.GREEN))
        #z1.setColor(Color.MAGENTA)
        #z2.setColor(Color.GREEN)

        IJ.saveAsTiff(z1, os.path.join(self.outputDir, z1.getTitle()))
        IJ.saveAsTiff(z2, os.path.join(self.outputDir, z2.getTitle()))

        print z1.getTitle()


def main():
    inputDir = sys.argv[1]
    outputDir = sys.argv[2]

    processor = SamuLifProcessor(outputDir)

    for filename in os.listdir(inputDir):
        if filename.endswith(".lif"):
            iterateLif(os.path.join(inputDir,filename), processor)

if __name__ == "__main__":
    main()
