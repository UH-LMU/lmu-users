var FIRST_FRAME = "100";

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

setBatchMode(true);

//plate = '/work/data/mushtaq/cellIQ 30.06.2020 20ulseeding a2WT a3TRI b2Afa b3Magi c2Occ c3LSR/output';
plate = getDirectory("Select plate output directory, e.g. Plate1/output");
output_plate = plate;
print(output_plate);

pdone = false;
wells = getFileList(plate);
for (w=0; w<wells.length && !pdone; w++){
	if (startsWith(wells[w],'Well')) {
		well = wells[w];
		output_ar = output_plate + "/" + well + "ar";
		output_overlay = output_plate + "/" + well + "overlay";
		output_video = output_plate + "/" + well + "video";
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
	if(w==10) {
		// uncomment for testing with fewer wells
		//print("finished test wells " + w);
		//pdone = true;
	}
}
