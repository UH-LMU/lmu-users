import os
import numpy as np
from skimage import io, measure, morphology

# Input and output directories
input_dir = "output"
output_dir = "largest_label"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Process each label image
for file in os.listdir(input_dir):
    if file.endswith(".tif"):
        # Load the label image
        label_image = io.imread(os.path.join(input_dir, file))
        
        # Measure region properties
        properties = measure.regionprops(label_image)
        if properties:
            # Find the largest label by area
            largest_label = max(properties, key=lambda x: x.area).label
            
            # Create a new label image with only the largest label
            largest_label_image = np.where(label_image == largest_label, label_image, 0)
            
            # Save the new label image
            io.imsave(os.path.join(output_dir, file), largest_label_image.astype(np.uint16))
