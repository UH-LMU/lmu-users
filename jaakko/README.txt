Here's how to do with the Cytoo images:

1. run CellProfiler project to produce a SQLite database with image measurements

2. run readdb.py with the SQLite file as argument to parse results into a .csv file
./readdb.py /input/LMU-active2/Harri/Data/Jaakko/cellprofiler/output/DefaultDB.db |sed 's#Y.*images#/output/images_all#'> /output/overlays_and_centers_3.csv

3. run "ImageJ draw_centers.py" to draw nucleus centers and anchor centers and orientations.

