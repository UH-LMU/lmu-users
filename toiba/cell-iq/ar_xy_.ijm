
function ar_xy(input_dir, filename, output_ar, output_xy) {
	AR = "AR";
	XY = "XY";

	// create new images for AR and cell center
	newImage(AR, "8-bit black", 1392, 1040, 1);
	newImage(XY, "8-bit black", 1392, 1040, 1);

	print(input_dir + "/" + filename);
	open(input_dir + "/" + filename);
	Stack.setXUnit("px");
	run("Properties...", "channels=1 slices=1 frames=1 pixel_width=1 pixel_height=1 voxel_depth=1.0000");
	run("Set Measurements...", "area centroid center fit shape redirect=None decimal=3");
	run("Analyze Particles...", "display exclude clear add");
	//print(nResults);

	// arrays for cell center coordinates
	xcoord = newArray(nResults);
	ycoord = newArray(nResults);
	selectWindow(AR);
	for (i=0;i<nResults; i++) {
		//print(i);
		// select one cell at a time
		roiManager("Select",i);
		// read AR from Results
		value = getResult("AR",i) * 10;
		// set the intensity of the cell to AR
		setColor(value);
		fill();

		// read coordinates into arrays
		xcoord[i] = getResult("X",i);
		ycoord[i] = getResult("Y",i);
	}
	// save AR image
	output_file = replace(filename,'.tif','_ar.tif');
	saveAs("tif", output_ar + "/" + output_file);
	
	//print(xcoord[nResults-1]);
	//print(ycoord[nResults-1]);
	
	// paint cell centers in XY image
	selectWindow(XY);
	setColor(255);
	makeSelection("point dot small", xcoord, ycoord);
	run("Draw", "slice");	
	// save XY image
	output_file = replace(filename,'.tif','_xy.tif');
	saveAs("tif", output_xy + "/" + output_file);

	// save measurements
	selectWindow("Results");
	output_file = replace(filename,'.tif','_results.csv');
	saveAs("Results", output_ar + "/" + output_file);

	run("Close All");
}


setBatchMode(true);
var pdone = false;
var wdone = false;

plate = '/work/data/mushtaq/cellIQ 30.06.2020 20ulseeding a2WT a3TRI b2Afa b3Magi c2Occ c3LSR/output';
output_plate = plate;
print(output_plate);

wells = getFileList(plate);
for (w=0; w<wells.length && !pdone; w++){
	if (startsWith(wells[w],'Well')) {
		well = wells[w];
		output_seg= output_plate + "/" + well + "segmentation";
		output_ar= output_plate + "/" + well + "ar";
		output_xy= output_plate + "/" + well + "xy";
		print(output_ar);
		print(output_xy);
		File.makeDirectory(output_ar);
		File.makeDirectory(output_xy);

		list = getFileList(output_seg);
		var done = false;
		for (i=0; i<list.length && !wdone; i++){
			if (endsWith(list[i],'.tif')) {
				//print(list[i]);
				ar_xy(output_seg, list[i], output_ar, output_xy);
			}
			// uncomment to test with fewer images
			//if(i==5) wdone = true;
		}
	}
	// uncomment to test with fewer wells
	//if(w==5) pdone = true;
}
