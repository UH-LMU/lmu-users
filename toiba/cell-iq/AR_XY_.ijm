
function ar_xy(input_dir, filename, output_ar, output_xy) {
	AR = "AR";
	XY = "XY";
	newImage(AR, "8-bit black", 1392, 1040, 1);
	newImage(XY, "8-bit black", 1392, 1040, 1);

	print(input_dir + "/" + filename);
	open(input_dir + "/" + filename);
	Stack.setXUnit("px");
	run("Properties...", "channels=1 slices=1 frames=1 pixel_width=1 pixel_height=1 voxel_depth=1.0000");
	run("Set Measurements...", "area centroid center fit shape redirect=None decimal=3");
	run("Analyze Particles...", "display exclude clear add");
	//print(nResults);
	
	//xcoord = newArray(0);
	//ycoord = newArray(0);
	xcoord = newArray(nResults);
	ycoord = newArray(nResults);
	selectWindow(AR);
	for (i=0;i<nResults; i++) {
		//print(i);
		roiManager("Select",i);
		value = getResult("AR",i) * 10;
		setColor(value);
		fill();

		//xcoord.append(getResult("X",i));
		//ycoord.append(getResult("Y",i));
		xcoord[i] = getResult("X",i);
		ycoord[i] = getResult("Y",i);
	}

	print(xcoord[nResults-1]);
	print(ycoord[nResults-1]);
	output_file = replace(filename,'.tif','_ar.tif');
	saveAs("tif", output_ar + "/" + output_file);
	
	selectWindow(XY);
	setColor(value);
	makeSelection("point dot small", xcoord, ycoord);
	run("Draw", "slice");	
	output_file = replace(filename,'.tif','_xy.tif');
	saveAs("tif", output_xy + "/" + output_file);

	run("Close All");
}

input = '/work/data/mushtaq/cellIQ 30.06.2020 20ulseeding a2WT a3TRI b2Afa b3Magi c2Occ c3LSR/Well A2 WT _01_segmentation';
output_ar = replace(input, "_segmentation", "_ar");
output_xy = replace(input, "_segmentation", "_xy");
File.makeDirectory(output_ar);
File.makeDirectory(output_xy);

setBatchMode(true);

list = getFileList(input);
var done = false;
for (i=0; i<list.length && !done; i++){
	if (endsWith(list[i],'.tif')) {
		//print(list[i]);
		ar_xy(input, list[i], output_ar, output_xy);
	}

	if(i==5) done = true;
}
