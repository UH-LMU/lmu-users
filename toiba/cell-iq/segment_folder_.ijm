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

function process_well(input_well, output_well) {
	output_seg= output_well + "/segmentation";
	print(output_well);
	print(output_seg);
	File.makeDirectory(output_well);
	File.makeDirectory(output_seg);

	wdone = false;
	list = getFileList(input_well);
	for (i=0; i<list.length && !wdone; i++) {
		if (endsWith(list[i],'.tif')) {
			print(list[i]);
			segment(input_well, list[i], output_seg);
		}
		if(i==2) {
				// uncomment for testing with fewer images
				print("finished test images " + i);
				wdone = true;
		}
	}
}

function process_plate(plate, output_plate) {
	File.makeDirectory(output_plate);

	pdone = false;
	wells = getFileList(plate);
	for (w=0; w<wells.length && !pdone; w++){
		//print(wells[w]);
		if (startsWith(wells[w],'Well')) {
			well = wells[w];
			input_well = plate + well;
			print(input_well);
			output_well = output_plate + "/" + well;
			process_well(input_well, output_well);
		}
		if(w==10) {
			// uncomment for testing with fewer wells
			//print("finished test wells " + w);
			//pdone = true;
		}
	}
}

setBatchMode(true);

//input = getDirectory("Select input directory, e.g. Plate1");
//output = getDirectory("Select output directory");


input = "/work/data/mushtaq/cellIQ 30.06.2020 20ulseeding a2WT a3TRI b2Afa b3Magi c2Occ c3LSR/Well A2 WT _01/";
output = "/work/data/mushtaq/test_well_output/";
process_well(input, output);


/*
input = "/work/data/mushtaq/cellIQ 30.06.2020 20ulseeding a2WT a3TRI b2Afa b3Magi c2Occ c3LSR/";
output = "/work/data/mushtaq/test_plate_output/";
process_plate(input, output);
*/
