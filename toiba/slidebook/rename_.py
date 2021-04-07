from ij.io import DirectoryChooser,OpenDialog
from java.io import File
import os
import os.path
import re

DEBUG = False
reg = re.compile("(.*)_before([0-9]*)_after([0-9]*).* Snap image - ([0-9]*)_.*")
def new_name(name):

    result = reg.match(name)
    if not result:
        raise ValueError("filename does not match: " + name)

    sample = result.groups()[0]
    before = int(result.groups()[1])
    after = int(result.groups()[2])
    snap = int(result.groups()[3])

    if DEBUG:
        print sample
        print before
        print after
        print snap

    channel = "c00"
    if snap % 2 == 0:
        channel = "c01"

    timepoint = "t00"
    if snap >= after:
        timepoint = "t99"

    site = snap - (1 - snap%2)
    if snap >= after:
        site = site - before

    return sample + "_s" + str(site).zfill(2) + "_" + channel + "_" + timepoint

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
    Download rename_.py. Then in Fiji:
    File -> New -> Script...
    Script Editor -> File -> Open... rename_.py
    Script Editor -> Run
    """
    print "directorychooser1"
    input_dir = DirectoryChooser("Choose input directory").getDirectory()
    #filename = OpenDialog("Choose LIF/SLD").getPath()
    if not input_dir:
        # user canceled dialog
        return

    file_types = "tif"
    filters = "before"
    do_recursive = True
    
    image_paths = batch_open_images(input_dir,
                                    split_string(file_types),
                                    split_string(filters),
                                    do_recursive)

    for ip in sorted(image_paths):
        parent = os.path.dirname(ip)
        print ip
        base,ext = os.path.splitext(os.path.basename(ip))
        base = new_name(base)
        renamed = os.path.join(parent, base) + ext
        print renamed

print __name__

if __name__ in ("__main__", "__builtin__"):
    print "main"
    main()

