from ij import IJ,ImagePlus
from ij.io import DirectoryChooser,OpenDialog
from java.io import File
from loci.plugins.in import ImagePlusReader,ImporterOptions,ImportProcess
import os
import os.path
import sys


#
# This part goes through the LIF, SLD etc. file containing many images.
#
def iterate(filename,impProcessor):
    """
    Iterate over all series in a LIF or SLD file and process them.
    Arguments:
    filename: .lif, .sld, ...
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
            print "iterate: " + imp.getTitle()
            try:
                impProcessor.process(imp)
            finally:
                imp.close()

        # deactivate series (otherwise next iteration will have +1 active series)
        opts.setSeriesOn(i, False)


#
# This part does the actual conversion to 8-bit.
#
class Processor:

    def __init__(self,exportDir):
        self.exportDir = exportDir
    
    def process(self,imp):
        # save as tiff
        #IJ.saveAsTiff(imp, os.path.join(self.exportDir,imp.getTitle()))

        scale_conversions = True
        
        # save individual channels as tif
        for c in range(1,imp.getNChannels()+1):
            imp.setPosition(c,1,1)
            
            # convert to 8-bit
            ip = imp.getProcessor().convertToByte(scale_conversions)
            
            impc = ImagePlus(imp.getTitle() + "_c" + str(c) + "_8bit", ip)
            print impc.getTitle()
            IJ.saveAsTiff(impc, os.path.join(self.exportDir,impc.getTitle()))
            impc.close()


#
# Steal some code to process all images in a folder:
# https://imagej.net/Jython_Scripting.html#A_batch_opener_using_os.walk.28.29
#
def batch_open_images(path, file_type=None, name_filter=None, recursive=False):
    '''Open all files in the given folder.
    :param path: The path from were to open the images. String and java.io.File are allowed.
    :param file_type: Only accept files with the given extension (default: None).
    :param name_filter: Only accept files that contain the given string (default: None).
    :param recursive: Process directories recursively (default: False).
    '''
    # Converting a File object to a string.
    if isinstance(path, File):
        path = path.getAbsolutePath()
 
    def check_type(string):
        '''This function is used to check the file type.
        It is possible to use a single string or a list/tuple of strings as filter.
        This function can access the variables of the surrounding function.
        :param string: The filename to perform the check on.
        '''
        if file_type:
            # The first branch is used if file_type is a list or a tuple.
            if isinstance(file_type, (list, tuple)):
                for file_type_ in file_type:
                    if string.endswith(file_type_):
                        # Exit the function with True.
                        return True
                    else:
                        # Next iteration of the for loop.
                        continue
            # The second branch is used if file_type is a string.
            elif isinstance(file_type, string):
                if string.endswith(file_type):
                    return True
                else:
                    return False
            return False
        # Accept all files if file_type is None.
        else:
            return True
 
    def check_filter(string):
        '''This function is used to check for a given filter.
        It is possible to use a single string or a list/tuple of strings as filter.
        This function can access the variables of the surrounding function.
        :param string: The filename to perform the filtering on.
        '''
        if name_filter:
            # The first branch is used if name_filter is a list or a tuple.
            if isinstance(name_filter, (list, tuple)):
                for name_filter_ in name_filter:
                    if name_filter_ in string:
                        # Exit the function with True.
                        return True
                    else:
                        # Next iteration of the for loop.
                        continue
            # The second branch is used if name_filter is a string.
            elif isinstance(name_filter, string):
                if name_filter in string:
                    return True
                else:
                    return False
            return False
        else:
        # Accept all files if name_filter is None.
            return True
 
    # We collect all files to open in a list.
    path_to_images = []
    # Replacing some abbreviations (e.g. $HOME on Linux).
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    # If we don't want a recursive search, we can use os.listdir().
    if not recursive:
        for file_name in os.listdir(path):
            full_path = os.path.join(path, file_name)
            if os.path.isfile(full_path):
                if check_type(file_name):
                    if check_filter(file_name):
                        path_to_images.append(full_path)
    # For a recursive search os.walk() is used.
    else:
        # os.walk() is iterable.
        # Each iteration of the for loop processes a different directory.
        # the first return value represents the current directory.
        # The second return value is a list of included directories.
        # The third return value is a list of included files.
        for directory, dir_names, file_names in os.walk(path):
            # We are only interested in files.
            for file_name in file_names:
                # The list contains only the file names.
                # The full path needs to be reconstructed.
                full_path = os.path.join(directory, file_name)
                # Both checks are performed to filter the files.
                if check_type(file_name):
                    if check_filter(file_name):
                        # Add the file to the list of images to open.
                        path_to_images.append(full_path)
    # Create the list that will be returned by this function.
    #images = []
    #for img_path in path_to_images:
    return path_to_images


def split_string(input_string):
    '''Split a string to a list and strip it
    :param input_string: A string that contains semicolons as separators.
    '''
    string_splitted = input_string.split(';')
    # Remove whitespace at the beginning and end of each string
    strings_striped = [string.strip() for string in string_splitted]
    return strings_striped


def main():
    """
    Download export_sld.py. Then in Fiji:
    File -> New -> Script...
    Script Editor -> File -> Open... export_lif_gui.py
    Script Editor -> Run
    """
    print "directorychooser1"
    input_dir = DirectoryChooser("Choose input directory").getDirectory()
    #filename = OpenDialog("Choose LIF/SLD").getPath()
    if not input_dir:
        # user canceled dialog
        return
    print "directorychooser2"
    output_root = DirectoryChooser("Choose output directory").getDirectory()
    if not output_root:
        # user canceled dialog
        return

    file_types = "sld"
    filters = ""
    do_recursive = False
    
    image_paths = batch_open_images(input_dir,
                                    split_string(file_types),
                                    split_string(filters),
                                    do_recursive)

    for ip in image_paths:
        basename,ext = os.path.splitext(os.path.basename(ip))
        output_dir = os.path.join(output_root,basename)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        
        processor = Processor(output_dir)
        iterate(ip, processor)

print __name__

if __name__ in ("__main__", "__builtin__"):
    print "main"
    main()

