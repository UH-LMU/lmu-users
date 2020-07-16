function segment(input_dir, filename, output_dir) {
	print(input_dir + "/" + filename);
	open(input_dir + "/" + filename);
	run("Gaussian Blur...", "sigma=2");
	run("Make Binary");
	run("Invert LUT");
	run("Watershed");
	run("Invert LUT");
	run("Find Maxima...", "prominence=50 light output=[Segmented Particles]");
	output_file = getTitle();
	output_file = replace(output_file,'.tif Segmented','_segmentation.tif');
	print(output_dir + "/" + output_file);
	saveAs("tif", output_dir + "/" + output_file);
	run("Close All");
}

setBatchMode(true);
var pdone = false;
var wdone = false;

plate = '/work/data/mushtaq/cellIQ 30.06.2020 20ulseeding a2WT a3TRI b2Afa b3Magi c2Occ c3LSR';
output_plate = plate + "/output";
print(output_plate);
File.makeDirectory(output_plate);

wells = getFileList(plate);
for (w=0; w<wells.length && !pdone; w++){
	if (startsWith(wells[w],'Well')) {
		well = wells[w];
		input_well = plate + "/" + well;
		output_well = output_plate + "/" + well;
		output_seg= output_plate + "/" + well + "segmentation";
		print(output_well);
		print(output_seg);
		File.makeDirectory(output_well);
		File.makeDirectory(output_seg);

		list = getFileList(well);
		var done = false;
		for (i=0; i<list.length && !wdone; i++){
			if (endsWith(list[i],'.tif')) {
				//print(list[i]);
				segment(input_well, list[i], output_seg);
			}
			// uncomment to test with fewer images
			//if(i==5) wdone = true;
		}
	}
	// uncomment to test with fewer wells
	//if(w==2) pdone = true;
}


