
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
var pdone = false;
var wdone = false;

plate = '/work/data/mushtaq/cellIQ 30.06.2020 20ulseeding a2WT a3TRI b2Afa b3Magi c2Occ c3LSR';
output_plate = plate + "/output";
print(output_plate);

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

		list = getFileList(input_well);
		var done = false;
		for (i=0; i<list.length && !wdone; i++){
			if (endsWith(list[i],'.tif')) {
				//print(list[i]);
				create_overlay(input_well, list[i], output_seg, output_xy, output_overlay);
			}
			// uncomment to test with fewer images
			//if(i==5) wdone = true;
		}
	}
	// uncomment to test with fewer wells
	//if(w==5) pdone = true;
}
