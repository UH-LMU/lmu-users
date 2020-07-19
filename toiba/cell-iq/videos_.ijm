var FIRST_FRAME = "1";

function create_overlay_video(input_dir, tif, ntif, output_video) {
	run("Image Sequence...", "open=[" + input_dir + "/" + tif +"] starting=" + FIRST_FRAME + " file=.tif sort use");
	getDimensions(width, height, channels, slices, frames);
	print(slices);
	print(frames);
	ntif = ntif - parseInt(FIRST_FRAME) + 1 ;
	print(ntif);
	run("Stack to Hyperstack...", "order=xyczt(default) channels=3 slices=1 frames="+ntif+" display=Composite");
	run("AVI... ", "compression=JPEG frame=7 save=["+output_video+"/overlay.avi]");
	run("Close All");
}

function create_ar_video(input_dir, tif, ntif, output_video) {
	run("Image Sequence...", "open=[" + input_dir + "/" + tif +"] starting=" + FIRST_FRAME + " file=.tif sort");
	//run("Enhance Contrast", "saturated=0.35 all use");
	setMinAndMax(1,40);
	run("Fire");
	run("Apply LUT", "stack");
	run("AVI... ", "compression=JPEG frame=7 save=["+output_video+"/ar.avi]");
	run("Close All");
}

function process_well(output_well) {
	output_ar = output_well + "ar";
	output_overlay = output_well + "overlay";
	output_video = output_well + "video";
	print(output_video);
	File.makeDirectory(output_video);

	// overlay video
	list = getFileList(output_overlay);
	tif = "";
	ntif = 0;
	for (i=0; i<list.length; i++){
		if (endsWith(list[i],'.tif')) {
			tif = list[i];
			ntif = ntif + 1;
		}
	}
	create_overlay_video(output_overlay, tif, ntif, output_video);

	// ar video
	list = getFileList(output_ar);
	tif = "";
	ntif = 0;
	for (i=0; i<list.length; i++){
		if (endsWith(list[i],'.tif')) {
			tif = list[i];
			ntif = ntif + 1;
		}
	}
	create_ar_video(output_ar, tif, ntif, output_video);
}

function process_plate(output_plate) {
	print(output_plate);

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

output = '/work/data/mushtaq/test_well_output/';
process_well(output);

//output = '/work/data/mushtaq/test_plate_output/';
//process_plate(output);


