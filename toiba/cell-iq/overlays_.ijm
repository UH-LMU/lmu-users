
function create_overlay(input_orig, filename, output_seg, output_xy, output_overlay) {
	open(input_orig + "/" + filename);
	orig = getTitle();

	filename_seg = replace(filename,'.tif','_segmentation.tif');
	open(output_seg + "/" + filename_seg);
	run("Invert");
	seg = getTitle();

	filename_xy = replace(filename,'.tif','_segmentation_xy.tif');
	open(output_xy + "/" + filename_xy);
	xy = getTitle();

	run("Merge Channels...", "c1="+seg +" c2="+xy + " c4="+orig + " create");
	
	output_file = replace(filename,'.tif','_overlay.tif');
	saveAs("tif", output_overlay + "/" + output_file);

	run("Close All");
}

setBatchMode(true);

//plate = '/work/data/mushtaq/cellIQ 30.06.2020 20ulseeding a2WT a3TRI b2Afa b3Magi c2Occ c3LSR/';
plate = getDirectory("Select plate directory, e.g. Plate1");
output_plate = plate + "/output";
print(output_plate);

pdone = false;
wells = getFileList(plate);
for (w=0; w<wells.length && !pdone; w++){
	if (startsWith(wells[w],'Well')) {
		well = wells[w];
		input_well = plate + "/" + well;
		output_seg= output_plate + "/" + well + "segmentation";
		output_ar= output_plate + "/" + well + "ar";
		output_xy= output_plate + "/" + well + "xy";
		output_overlay= output_plate + "/" + well + "overlay";
		print(output_overlay);
		File.makeDirectory(output_overlay);

		wdone = false;
		list = getFileList(input_well);
		for (i=0; i<list.length && !wdone; i++){
			if (endsWith(list[i],'.tif')) {
				//print(list[i]);
				create_overlay(input_well, list[i], output_seg, output_xy, output_overlay);
			}
			if(i==2) {
				// uncomment for testing with fewer images
				//print("finished test images " + i);
				//wdone = true;
			}
		}
	}
	if(w==10) {
		// uncomment for testing with fewer wells
		//print("finished test wells " + w);
		//pdone = true;
	}
}
