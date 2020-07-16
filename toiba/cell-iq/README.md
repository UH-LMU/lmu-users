# Scripts for Cell-IQ

Run the scripts in this order:

- segment_folder_.ijm (segments original phase contrast images)
- ar_xy_.ijm (run and save measurements)
- overlays_.ijm (overlay originals with cell segmentation and centers)

After this, the overlays can be imported for tracking:
- Import -> Image sequence
- Image -> Hyperstacks -> Stack to hyperstack (channels=3, slices=1, timepoints=..., displaymode=composite)
- Image -> Properties (pixel width and height = 6.45 um, voxel depth = 1 -, frame interval = ...

Trackmate settings:
- Segment in channel 2 (cell center markers)
- Estimated blob diameter = 6 um (markers are one pixel)
- Threshold = 200 (marker intensity is 255)
- No median filter
- No sub-pixel localization


