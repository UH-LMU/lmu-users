from ij import IJ, ImagePlus, ImageStack, WindowManager
from ij.process import ImageProcessor, ByteProcessor
from java.lang import Double

from fiji.scripting import Weaver
def thresholdStackW(imp, low, high):
    i = 1
    stack = imp.getStack()
    depth = imp.getNSlices()
    print "thresholdStackW: depth", depth
    width = stack.getProcessor(i).getWidth()
    height = stack.getProcessor(i).getHeight()
    winput = [None]
    w = Weaver.inline(
            """
            byte[] input = (byte[]) winput.get(0);
            byte[] output = new byte[input.length];
            for (int i=0; i<input.length; i++) {
                if (input[i] < low || input[i] > high){
                    output[i] = (byte)0;
                } else {
                    output[i] = (byte)255;
                }
            }
            return output;
            """,
            {"winput":winput, "low":low, "high":high})
    stackout = ImageStack(width, height)
    for k in range(1, depth+1):
        ip = stack.getProcessor(k)
        winput[0] = ip.getPixels()
        pixels = w.call()
        ipout = ByteProcessor(width, height)
        ipout.setPixels(pixels)
        stackout.addSlice(ipout)
        imp.setStack(stackout)

THR_METHOD = "Otsu"
THR_MAX = Double.POSITIVE_INFINITY
THR_ADJUST = 2.5

# find out the threshold given by the autothreshold algorithm
imp = WindowManager.getCurrentImage()
print imp.getTitle()
tmp = imp.duplicate()
ip = tmp.getProcessor()
ip.setAutoThreshold(THR_METHOD, True, ip.NO_LUT_UPDATE)
thr = ip.getMinThreshold()
print "min threshold: " + str(thr)
thr = int(round(THR_ADJUST * thr))
print "new threshold: " + str(thr)
tmp.close()

# apply the threshold
thresholdStackW(imp, thr, THR_MAX)

