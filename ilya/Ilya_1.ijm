outputDir = "/home/hajaalin/Data/Ilya/Output/";

title = getTitle();
blue = title + " (blue)";
green = title + " (green)";
red = title + " (red)";

run("Split Channels");
selectWindow(red);
close();

// scale intensities in blue image
blueMultiplier = 0.3;
run("Multiply...", "value=" + blueMultiplier);

// subtract scaled blue signal from green
imageCalculator("Subtract create", green,blue);
selectWindow("Result of " + green);
greenTmp = "greenTmp";
rename(greenTmp)
selectWindow(greenTmp);

// threshold the image
radius = 100;
run("Auto Local Threshold", "method=Bernsen radius=" + radius + " parameter_1=0 parameter_2=0 white");
selectWindow(greenTmp);
run("Fill Holes");
run("Watershed");

// define and run measurements
minSize = 0;
run("Set Measurements...", "area mean perimeter shape feret's integrated skewness kurtosis redirect=None decimal=2");
run("Analyze Particles...", "size=" + minSize + "-Infinity circularity=0.00-1.00 show=[Overlay Outlines] display exclude clear add");
roiManager("Show All with labels");
roiManager("Show All");

// save results
outputFile = outputDir + title + "_nucleoli.txt";
saveAs("Results", outputFile);


// count the cells
selectWindow(blue);
run("Auto Threshold", "method=Default white");
run("Fill Holes");
run("Despeckle");
run("Set Measurements...", "area redirect=None decimal=2");
run("Analyze Particles...", "size=0-Infinity circularity=0.00-1.00 show=[Overlay Outlines] display clear add");
outputFile = outputDir + title + "_nuclei.txt";
saveAs("Results", outputFile);


