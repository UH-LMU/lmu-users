// https://forum.image.sc/t/16bit-lut-for-label-masks/10425/19

import ij.IJ
import ij.ImagePlus
import ij.gui.ImageRoi
import ij.gui.Overlay
import ij.process.ShortProcessor

import java.awt.image.BufferedImage
import java.awt.image.IndexColorModel

impRaw = IJ.openImage("/work/data/jilehtim/HARRI/C1-250919_Lifeact-mKate2_NMIIA-GFP_pax-iRFP670_10s_interval_001_D3D_ALX.tif");
impLabel = IJ.openImage("/work/data/jilehtim/HARRI/timetubes2_long.ome.tiff");

// Create a random 16-bit LUT
int n = Math.pow(2, 16)-1 as int
def r = new byte[n]
def g = new byte[n]
def b = new byte[n]
def a = new byte[n]
def rand = new Random(100L)
rand.nextBytes(r)
rand.nextBytes(g)
rand.nextBytes(b)
Arrays.fill(a, (byte)255)
a[0] = 0
def model = new IndexColorModel(16, n, r, g, b, a)

// Create a colored overlay
int width = impLabel.getWidth()
int height = impLabel.getHeight()
def overlay = new Overlay()
for (int s = 1; s <= impLabel.getStack().getSize(); s++) {
    def pixels = impLabel.getStack().getPixels(s) as short[]
    def raster = model.createCompatibleWritableRaster(width, height)
    def buffer = raster.getDataBuffer()
    System.arraycopy(pixels, 0, buffer.getData(), 0, buffer.getData().length);
    def img = new BufferedImage(model, raster, false, null)
    def roi = new ImageRoi(0, 0, img)
    roi.setOpacity(0.75)
    roi.setPosition(s)
    overlay.add(roi)
}

impRaw.setOverlay( overlay )
impRaw.show()
