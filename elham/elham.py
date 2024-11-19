from ij import IJ,ImagePlus
from ij.plugin import ImageCalculator
from ij.plugin.filter import Analyzer
from loci.plugins.in import ImagePlusReader,ImporterOptions,ImportProcess
from trainableSegmentation import WekaSegmentation
import os.path
import re
import sys

def measureImage(imp):
    #print(type(imp))
    nz = imp.getStackSize()
    print("nc: " + str(imp.getNChannels()))
    print("nz: " + str(nz))

    imp.setTitle("tmp")
    imp.show()
    IJ.run(imp, "Split Channels", "")

    # 1 is the fluorescence channel,
    # 2 is the transmitted light channel

    # close channel 2 image
    IJ.selectWindow("C2-tmp")
    IJ.getImage().close()

    # get this threshold by imaging a sample without any dye injected?
    THRESHOLD = 600
    
    orig = IJ.getImage()
    orig.setTitle("orig")
    mask = orig.duplicate()
    mask.setTitle('mask')
    #IJ.setRawThreshold(imp, THRESHOLD, 65535)
    IJ.setThreshold(mask, THRESHOLD, 65535)
    IJ.run(mask, "Make Binary", "background=Light")
    IJ.run(mask, "Divide...", "value=255 stack");
    IJ.run(mask, "16-bit", "")
    mask.show()

    masked = ImageCalculator.run(mask, orig, "Multiply create stack 32-bit")
    masked.setTitle("masked")
    masked.show()

    IJ.selectWindow(masked.getTitle())
    IJ.run("Z Project...", "projection=[Sum Slices]")

    IJ.selectWindow("SUM_" + masked.getTitle())
    IJ.run("Set Measurements...", "mean min integrated median redirect=None decimal=0")
    IJ.run("Measure")

    # uncomment to see intermediate images
    #return
    IJ.getImage().close()
    orig.close()
    mask.changes = False
    mask.close()
    masked.close()
    

def save_tl_edf(imp, filename_tl):
    imp.setTitle("tmp")
    imp.show()

    IJ.run(imp, "Split Channels", "")

    # 1 is the fluorescence channel,
    # 2 is the transmitted light channel

    # close channel 1 image
    #IJ.selectWindow("C1-tmp")
    #c1 = IJ.getImage()
    #c1.close()

    IJ.selectWindow("C2-tmp")
    #c2 = IJ.getImage()

    IJ.run("Stack Focuser ", "enter=11");
    IJ.selectWindow("Focused_C2-tmp")
    f2 = IJ.getImage()
    IJ.saveAsTiff(f2, filename_tl)

    #c2.close()
    #f2.close()


    
def measureBF(filepath):
    """
    List all series in a LIF file.
    Arguments:
    filename: LIF filename
    """

    opts = ImporterOptions()
    opts.setId(filepath)
    opts.setUngroupFiles(True)

    # set up import process
    process = ImportProcess(opts)
    process.execute()
    nseries = process.getSeriesCount()

    # reader belonging to the import process
    reader = process.getReader()

    # select only one series (magnification)
    MAG = 3

    # define where to save metadata file
    dirname = os.path.dirname(filepath)
    basename = os.path.basename(filepath)
    filename,ext = os.path.splitext(basename)
    filename_out = os.path.join(dirname, filename + '_s%d.csv' % (MAG))
    filename_selmag = os.path.join(dirname, filename + '_s%d.tif' % (MAG))
    filename_tl = os.path.join(dirname, filename + '_s%d_tl.tif' % (MAG))
    
    # reader external to the import process
    impReader = ImagePlusReader(process)

    print "measureBF: %s" % (filename)

    # activate all series (same as checkbox in GUI)
    #opts.setOpenAllSeries(True)

    opts.setSeriesOn(MAG,True)
    reader.setSeries(MAG)

    # read and process image
    imps = impReader.openImagePlus()
    #print(type(imps))
    print("nimages: " + str(len(imps)))

    imp = imps[0]
    #IJ.saveAsTiff(imp, filename_selmag)

    
    # clear results table
    rt = Analyzer.getResultsTable()
    rt.reset()

    ## The actual processing happens here
    #measureImage(imp)
    save_tl_edf(imp, filename_tl)
    
    # save results table
    rt.save(filename_out)

    #imp.close()
    IJ.run("Close All")
        

inputdir = '/home/user/data/elham/'
# On Windows you have to use \\ instead of /, so something like
# inputdir = 'L:\\lmu_active1\users\h ...'

import os
import fnmatch

def find_bf_files(root_folder, ext='*.czi'):
    bf_files = []
    for root, dirs, files in os.walk(root_folder):
        for filename in files:
            if fnmatch.fnmatch(filename, ext):
                bf_files.append(os.path.join(root, filename))
    return bf_files

bf_files = find_bf_files(inputdir)

# Now bf_files will contain a list of paths to all .czi files in the specified folder and its subdirectories
print(bf_files)

for f in bf_files:
    measureBF(f)

    # uncomment to test with only the first file
    #break
