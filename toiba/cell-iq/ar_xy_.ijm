
var MIN_AREA = "300";

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
	run("Analyze Particles...", "size=" + MIN_AREA + "-Infinity pixel display exclude clear add");
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

function process_well(output_well) {
	output_seg = output_well + "/segmentation";
	output_ar = output_well + "/ar";
	output_xy = output_well + "/xy";
	//output_ar = replace(output_seg, "segmentation", "ar");
	//output_xy = replace(output_seg, "segmentation", "xy");
	print(output_ar);
	print(output_xy);
	File.makeDirectory(output_ar);
	File.makeDirectory(output_xy);

	wdone = false;
	list = getFileList(output_seg);
	for (i=0; i<list.length && !wdone; i++){
		if (endsWith(list[i],'.tif')) {
			//print(list[i]);
			ar_xy(output_seg, list[i], output_ar, output_xy);
		}
		if(i==0) {
			// uncomment for testing with fewer images
			//print("finished test images " + i);
			//wdone = true;
		}
	}
}

function process_plate(output_plate) {
	pdone = false;
	wells = getFileList(output_plate);
	for (w=0; w<wells.length && !pdone; w++){
		if (startsWith(wells[w],'Well')) {
			well = wells[w];
			output_well = output_plate + "/" + well;
			process_well(output_well);
		}
		if(w==10) {
			// uncomment for testing with fewer wells
			//print("finished test wells " + w);
			//pdone = true;
		}
	}
}

setBatchMode(true);

//output = getDirectory("Select plate output directory, e.g. Plate1/output");

output = '/work/data/mushtaq/test_well_output';
process_well(output);

//output = '/work/data/mushtaq/test_plate_output';
//process_plate(output);


