
function process_site(plate, site, output_sequence, output_aligned, output_cropped) {
	 // replace spaces with underscore in output filenames
	 filename_site = replace(site, " ", "_");
	 filename_site = replace(filename_site, "/", "");

	 input_site = plate + "/" + site;
	 File.openSequence(input_site);
	 seq = getTitle();
	 saveAs("tif", output_sequence + "/" + filename_site + "_sequence.tif");

	 run("Linear Stack Alignment with SIFT", "initial_gaussian_blur=1.60 steps_per_scale_octave=3 minimum_image_size=64 maximum_image_size=1024 feature_descriptor_size=4 feature_descriptor_orientation_bins=8 closest/next_closest_ratio=0.92 maximal_alignment_error=25 inlier_ratio=0.05 expected_transformation=Translation interpolate");
	 aligned = getTitle();
	 saveAs("tif", output_aligned + "/" + filename_site + "_aligned.tif");

	 // https://github.com/agclark12/autocrop_black_edges/blob/master/Autocrop_Black_Edges.py
//	 runMacro("/home/hajaalin/Downloads/Autocrop_Black_Edges.py");
	 runMacro("L:\\lmu_active2\\users\\m\\mushtaq\\CellIQ 10x PIV IMAGING\\Macros\\Autocrop_Black_Edges.py");
	 saveAs("tif", output_cropped + "/" + filename_site + "_cropped.tif");

	 run("Close All");
}

function process_plate(plate, output_sequence, output_aligned, output_cropped) {
        pdone = false;
        sites = getFileList(plate);
        for (i=0; i<sites.length && !pdone; i++) {
                if (startsWith(sites[i],'Well')) {
                        site = sites[i];
                        process_site(plate, site, output_sequence, output_aligned, output_cropped);
                }
                if(i==1) {
                        // uncomment for testing with fewer sites
                        print("finished test sites " + i);
                        pdone = true;
                }
        }
}

setBatchMode(true);


//input = "/mnt/lmu_active2/users/m/mushtaq/CellIQ 10x PIV IMAGING/HARRI/raw data/";
//input = "/mnt/lmu_active2/users/m/mushtaq/CellIQ 10x PIV IMAGING/HARRI/test1/";
input = "L:\\lmu_active2\\users\\m\\mushtaq\\CellIQ 10x PIV IMAGING\\HARRI\\test1\\";
//output = "/mnt/lmu_active2/users/m/mushtaq/CellIQ 10x PIV IMAGING/HARRI/output/PlateN";
output = "L:\\lmu_active2\\users\\m\\mushtaq\\CellIQ 10x PIV IMAGING\\HARRI\\output\\PlateN";

output_sequence = output + "/sequence";
output_aligned = output + "/aligned";
output_cropped = output + "/cropped";
File.makeDirectory(output_sequence);
File.makeDirectory(output_aligned);
File.makeDirectory(output_cropped);

process_plate(input, output_sequence, output_aligned, output_cropped);
