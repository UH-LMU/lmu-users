from ij import IJ,ImagePlus
from loci.plugins.in import ImagePlusReader,ImporterOptions,ImportProcess
import os.path
import re
import sys


def listLif(filepath):
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

    # define where to save metadata file
    dirname = os.path.dirname(filepath)
    basename = os.path.basename(filepath)
    filename,ext = os.path.splitext(basename)
    filename_out = os.path.join(dirname, filename + '.csv')

    # pattern to find metadata in the series name
    # short explanation:
    # - the values are inside ()
    # - / is a special character, so it has to be marked as \/
    # - so the first value is anything between / /
    # - the second value is any number of digits before :
    pattern = re.compile("\/(.*)\/.*([0-9]+):")

    with open(filename_out, 'w') as csv:
        csv.write("MetadataSeries,MetadataRegion,MetadataRepetition\n")
    
        # reader external to the import process
        impReader = ImagePlusReader(process)

        # note that series index starts from 0, even though Fiji shows it starting from 1
        for i in range(0, nseries):
            label = process.getSeriesLabel(i)
            print "listLif: %d/%d %s" % (i, nseries, label)

            result = re.search(pattern, label)
            if result:
                region = result.groups()[0]
                repetition = result.groups()[1]

                csv.write("%s,%s,%s\n" % (i,region,repetition))
            else:
                print "Warning: metadata not found for series %s: %s" % (i, label)
        

inputdir = '/home/hajaalin/data/homa/'
# On Windows you have to use \\ instead of /, so something like
# inputdir = 'L:\\lmu_active1\users\h ...'

import os
import fnmatch

def find_lif_files(root_folder):
    lif_files = []
    for root, dirs, files in os.walk(root_folder):
        for filename in files:
            if fnmatch.fnmatch(filename, '*.lif'):
                lif_files.append(os.path.join(root, filename))
    return lif_files

lif_files = find_lif_files(inputdir)

# Now lif_files will contain a list of paths to all .lif files in the specified folder and its subdirectories
print(lif_files)

for lif in lif_files:
    listLif(lif)
