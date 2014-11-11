from ij import IJ
from ij.process import StackStatistics
from mosaic.plugins import ParticleTracker_ as PT
import sys

imp = IJ.openImage(sys.argv[1])
pt = PT()

pt.frames_number = 1
pt.stack = imp.getStack()
stack_stats = StackStatistics(imp)
pt.global_max = stack_stats.max
pt.global_min = stack_stats.min

pt.percentile = 0.8 / 100
pt.cutoff = 3.0
pt.radius = 2
pt.makeKernel(pt.radius)
pt.generateMask(pt.radius)

pt.setup("only_detect", imp)
print pt.only_detect

pt.processFrames()
frame = pt.frames[0]
print
print frame.toString()



