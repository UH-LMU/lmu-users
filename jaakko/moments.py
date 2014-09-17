#!/usr/bin/env python 
import re

class Moments:
    # central moments
    m00 = None
    m01 = None
    m02 = None
    m10 = None
    m11 = None
    m12 = None
    m20 = None
    m21 = None
    m22 = None

def printMoments(inputFile):
    from ij import IJ
    imp = IJ.openImage(inputFile)
    IJ.run(imp,"Image Moments", "order=3")


def readMoments(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()

    m = Moments()
    for l in lines:
        l = l.rstrip()
        if re.search(".tif", l) or l == "":
            continue

        #param, value, unit = l.split()
        param, value, unit = re.split(r'\t+', l)
        print "%s # %s # %s" % (param, value, unit)

        if param == "m[0][0]": 
            m.m00 = float(value)
            print m.m00
        elif param == "m[0][1]":
            m.m01 = float(value)
        elif param == "m[0][2]":
            m.m02 = float(value)
        elif param == "m[1][0]":
            m.m10 = float(value)
        elif param == "m[1][1]":
            m.m11 = float(value)
        elif param == "m[1][2]":
            m.m12 = float(value)
        elif param == "m[2][0]":
            m.m20 = float(value)
        elif param == "m[2][1]":
            m.m21 = float(value)
        elif param == "m[2][2]":
            m.m22 = float(value)
                  
    return m

import math
def orientation(m):
    up20 = m.m20 / m.m00
    up02 = m.m02 / m.m00
    up11 = m.m11 / m.m00

    theta = math.atan(2*up11 / (up20 - up02))
    return 360 * theta / math.pi


from optparse import OptionParser
if __name__=='__main__':
    usage ="""%prog [options] input_file
    Convert MatrixScreener data to stacks, one multicolor stack per field.
    Run '%prog -h' for options.
    """
    parser = OptionParser(usage=usage)
    parser.add_option('-r', '--read', action="store_true", default=False, help="")
    options, args = parser.parse_args()

    inputFile = args[0]
    if options.read:
        m = readMoments(inputFile)
        print orientation(m)

    else:
        printMoments(inputFile)


