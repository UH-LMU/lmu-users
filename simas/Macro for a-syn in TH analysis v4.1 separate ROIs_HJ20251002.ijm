// Macro from Grok v4.1 (improved to enlarge ROIs individually, with intermediate image saving)

// Function to get base name without extension
function getBaseName(fileName) {
    dotPos = lastIndexOf(fileName, ".");
    if (dotPos > 0) {
        return substring(fileName, 0, dotPos);
    } else {
        return fileName;
    }
}

// Prompt for input directory and verify it exists
//inputDir = getDirectory("/mnt/lmu_active1/users/s/sima/JJ-005-12"); 
inputDir = getDirectory("/home/hajaalin/git/simas/data2"); 
if (inputDir == "") { 
    print("Error: No directory selected. Exiting."); 
    exit(); 
} 
if (!File.isDirectory(inputDir)) { 
    print("Error: Selected path is not a valid directory: " + inputDir); 
    exit(); 
}

// Create output directory
outputDir = inputDir + "Analysis" + File.separator; 
File.makeDirectory(outputDir); 
outputFile = outputDir + "Analysis_Results separate ROIs.csv";

// Create image output directory and subfolders
imageOutputDir = outputDir + "Intermediate_Images" + File.separator; 
File.makeDirectory(imageOutputDir); 
thMasksDir = imageOutputDir + "TH_Masks" + File.separator; 
File.makeDirectory(thMasksDir); 
dapiThreshDir = imageOutputDir + "DAPI_Thresholded" + File.separator; 
File.makeDirectory(dapiThreshDir); 
nucleiMaskDir = imageOutputDir + "Nuclei_Masks" + File.separator; 
File.makeDirectory(nucleiMaskDir); 
asynThreshDir = imageOutputDir + "aSyn_Thresholded" + File.separator; 
File.makeDirectory(asynThreshDir);

// Initialize results file with headers
if (!File.exists(outputFile)) {
    File.append("Well,Site,ROI_ID,TH_DAPI_Count,aSyn_Spot_Count,aSyn_Total_Area,aSyn_Spot_Size", outputFile);
}

// Get list of image files and debug
list = getFileList(inputDir);
print("Selected directory: " + inputDir);
print("Found " + list.length + " files:");
for (i = 0; i < list.length; i++) {
    print(" - " + list[i]);
}
if (list.length == 0) {
    print("Error: No files found in directory: " + inputDir);
    exit();
}

// Define the arrayContains function
function arrayContains(array, value) {
    for (i = 0; i < array.length; i++) {
        if (array[i] == value) return true;
    }
    return false;
}

// Identify unique well-site combinations
wellSites = newArray();
for (i = 0; i < list.length; i++) {
    if (endsWith(list[i], ".tif") || endsWith(list[i], ".tiff")) {
        if (matches(list[i], ".*_([A-H][0-9]{1,2})_s[0-9]+_w[1-4].*")) {
            parts = split(list[i], "_");
            well = "";
            site = "";
            for (j = 0; j < parts.length; j++) {
                if (matches(parts[j], "[A-H][0-9]{1,2}")) well = parts[j];
                if (matches(parts[j], "s[0-9]+")) site = parts[j];
            }
            if (well != "" && site != "") {
                wellSite = well + "_" + site;
                if (!arrayContains(wellSites, wellSite)) {
                    wellSites = Array.concat(wellSites, wellSite);
                }
            }
        }
    }
}
print("Found " + wellSites.length + " unique well-site combinations:");
for (i = 0; i < wellSites.length; i++) {
    print(" - " + wellSites[i]);
}
if (wellSites.length == 0) {
    print("Error: No valid well-site combinations found. Check filename format.");
    exit();
}

// Enable batch mode to process images without displaying windows
setBatchMode(true);

// Close Summary table if open to prevent accumulation
if (isOpen("Summary")) {
    selectWindow("Summary");
    run("Close");
}

// Process each well-site combination
for (ws = 0; ws < wellSites.length; ws++) {
    wellSite = wellSites[ws];
    parts = split(wellSite, "_");
    well = parts[0];
    site = parts[1];
    
    // Load images for the current well and site based on wavelength
    dapiFile = "";
    thFile = "";
    asynFile = "";
    for (i = 0; i < list.length; i++) {
        if (indexOf(list[i], well + "_" + site + "_w1") >= 0) dapiFile = list[i];
        if (indexOf(list[i], well + "_" + site + "_w2") >= 0) thFile = list[i];
        if (indexOf(list[i], well + "_" + site + "_w4") >= 0) asynFile = list[i];
    }
    
    if (dapiFile == "" || thFile == "" || asynFile == "") {
        print("Missing images for " + wellSite + ":");
        print(" - DAPI (w1): " + (dapiFile == "" ? "Not found" : dapiFile));
        print(" - TH (w2): " + (thFile == "" ? "Not found" : thFile));
        print(" - a-syn (w4): " + (asynFile == "" ? "Not found" : asynFile));
        print("Skipping this well-site.");
        continue;
    }
    
    print("Processing well-site: " + wellSite);
    print(" - Loading DAPI: " + dapiFile);
    print(" - Loading TH: " + thFile);
    print(" - Loading a-syn: " + asynFile);

    // Open images
    open(inputDir + dapiFile);
    dapiID = getImageID();
    open(inputDir + thFile);
    thID = getImageID();
    open(inputDir + asynFile);
    asynID = getImageID();
    
    // Create TH mask
    selectImage(thID);
    run("Duplicate...", "title=TH_Mask");
    thMaskID = getImageID();
    setThreshold(380, 65535); // Replaced from this: setAutoThreshold("Otsu dark");
    run("Convert to Mask");
    // Save TH mask
    selectImage(thMaskID);
    thBase = getBaseName(thFile);
    saveAs("Tiff", thMasksDir + thBase + "_th.tif");
    
    // Smooth DAPI image
    selectImage(dapiID);
    run("Duplicate...", "title=DAPI_Smoothed");
    dapiSmoothID = getImageID();
	run("Smooth");

	// Threshold DAPI image
    selectImage(dapiSmoothID);
    run("Duplicate...", "title=DAPI_Thresholded");
    dapiThreshID = getImageID();
    setThreshold(130, 65535); // Replaced from this: setAutoThreshold("Otsu dark");
    run("Convert to Mask");
    // Save DAPI thresholded mask
    selectImage(dapiThreshID);
    dapiBase = getBaseName(dapiFile);
    saveAs("Tiff", dapiThreshDir + dapiBase + "_dapi.tif");
    
    // Apply TH mask to thresholded DAPI image
    imageCalculator("AND create", dapiThreshID, thMaskID);
    dapiMaskedID = getImageID();
    
    // Count DAPI nuclei in masked image
    selectImage(dapiMaskedID);
    run("Watershed");
    run("Analyze Particles...", "size=35-Infinity circularity=0.1-1.0 show=Masks add");
    nucleiMaskID = getImageID();
    selectImage(nucleiMaskID);
    run("Invert LUT");
    dapiBase = getBaseName(dapiFile);
    saveAs("Tiff", nucleiMaskDir + dapiBase + "_nuclei.tif");
    
    thDapiCount = roiManager("count");
    
    // Enlarge each ROI individually to avoid merging
    if (thDapiCount > 0) {
        for (k = 0; k < thDapiCount; k++) {
            roiManager("Select", k);
            run("Enlarge...", "enlarge=7 pixel");
            roiManager("Update");
        }
    } 
    
    // Analyze a-syn spots in expanded ROIs
    selectImage(asynID);
    run("Duplicate...", "title=aSyn_Thresholded");
    asynThreshID = getImageID();
    setThreshold(1430, 65535); // Replaced from this: setAutoThreshold("Otsu dark");
    run("Convert to Mask");
    // Save aSyn thresholded mask
    selectImage(asynThreshID);
    asynBase = getBaseName(asynFile);
    saveAs("Tiff", asynThreshDir + asynBase + "_asyn.tif");
    
    // Measure a-syn spots in each ROI
    for (i = 0; i < thDapiCount; i++) {
        roiManager("Select", i);
        run("Clear Results"); // Clear before analysis to ensure no carryover
        run("Analyze Particles...", "size=5-Infinity show=Nothing display"); // Added "display", removed "summarize"
        spotCount = nResults; // Use nResults for clarity (equivalent to getValue("results.count"))
        if (isNaN(spotCount) || spotCount < 0) {
            spotCount = 0;
        }
        spotSizes = newArray(spotCount);
        totalArea = 0;     
        if (spotCount > 0) {
            for (j = 0; j < spotCount; j++) {
                area = getResult("Area", j);
                if (isNaN(area)) {
                    continue;
                }
                spotSizes[j] = area;
                totalArea += spotSizes[j];
            }
        } 
        // Build spotSizesStr, with "NaN" if no spots
        if (spotCount == 0) {
            spotSizesStr = "0";
        } else {
            spotSizesStr = "";
            for (j = 0; j < spotCount; j++) {
                spotSizesStr += spotSizes[j];
                if (j < spotCount-1) spotSizesStr += ";";
            }
        }
        File.append(well + "," + site + "," + i + "," + thDapiCount + "," + spotCount + "," + totalArea + "," + spotSizesStr, outputFile);
        // Clear Results table
        run("Clear Results");
    }
    
    // Clean up images immediately after use
    if (isOpen(dapiID)) { selectImage(dapiID); close(); }
    if (isOpen(thID)) { selectImage(thID); close(); }
    if (isOpen(asynID)) { selectImage(asynID); close(); }
    if (isOpen(thMaskID)) { selectImage(thMaskID); close(); }
    if (isOpen(dapiSmoothID)) { selectImage(dapiSmoothID); close(); }
    if (isOpen(dapiThreshID)) { selectImage(dapiThreshID); close(); }
    if (isOpen(dapiMaskedID)) { selectImage(dapiMaskedID); close(); }
    if (isOpen(nucleiMaskID)) { selectImage(nucleiMaskID); close(); }
    if (isOpen(asynThreshID)) { selectImage(asynThreshID); close(); }
    roiManager("Reset");
}

// Disable batch mode after processing
setBatchMode(false);

// Notify completion
print("Analysis complete. Results saved to " + outputFile);
print("Intermediate images saved to " + imageOutputDir);