//
// Generate a hexagonal patch-wise analysis of intensity changes in a cell. 
//	See description in Figure 4 in Kim, H. Y. and Davidson, L. A. (2011) 
//	'Punctuated actin contractions during convergent extension and their permissive regulation by the 
//	non-canonical Wnt-signaling pathway', J Cell Sci 124(4): 635-646.
//	(please cite this paper if this macro has been useful in your research)
//
// 1. Identify a cell of interest within a timelapse sequence.
// 2. Use automated or manual methods to outline a region of interest in the cell. 
// 3. Launch "DrillwithinROIforAster"
//
// A. Generates a ROI list from ROI manager. The first ROI is the cell cortex ROI; all subsequent ROI are hexagonal patch //	ROIs. Note these ROIs are associated with the first frame of the timelapse stack. 
//	This list can be used later to generate maps to draw different intensity values within small hexagons.
// B. F-actin intensities in each patch are stored in the log-file. Intensities are only recorded if above the threshold. 
//    	Each row is a specific ROI, each column is the intensity in each slice.
//	The log-file can be saved and processed with additional code (R, matlab, python, perl, excel, etc) to assign
//	categories to each hexagon at each timepoint. Edit the macro to include intensities irrespective of the threshold.
// C. The stack "Actin Contractions" is generated with the same size of the original raw data stack. Each hexagon
//	containing an actin-contraction is indicated with a value of 255, all other areas are zeros.
//	This stack can be subject to additional processing with automated "track-particle" analysis.
//
// For questions contact Lance Davidson (lad43@pitt.edu)
// (Jan 24, 2020)

var cellx = newArray(9000);
var celly = newArray(9000);
var ncells;
var rawstack, actstack;

function MakeHexROI(x,y,r)
{
	var delx, dely1, dely2, x1,x2,x3,x4,x5,x6, y1,y2,y3,y4,y5,y6;
	
	delx = r*(sqrt(3)/2);
	dely1 = r/2;
	dely2 = r;
	
	x1 = x;
	y1 = y-dely2;
	
	x2 = x + delx;
	y2 = y-dely1;
	
	x3 = x + delx;
	y3 = y + dely1;
	
	x4 = x;
	y4 = y + dely2;
	
	x5 = x - delx;
	y5 = y + dely1;
	
	x6 = x - delx;
	y6 = y - dely1;
	
	makePolygon(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6);
}

function HexROIFill(rhex, offsetx, offsety, frwidth, frheight)
{

	var nwidth, nheight, offx, offy, i, j, icell;
	
	var t, theight, highx;

//	rhex=getNumber("Radius of hexagons to pack into frame", 10);

	
//	find out how many hexagons pack in height
	

	// the max number of short sides
	
	theight = frheight/(rhex+(rhex*sqrt(3))/2);
	
	highx = 0;
	lastx = 0;
	t = 0;
	
	highx = 2*rhex;
	
	while (highx < frheight)
	{
		lastx = highx;

		t++;
		highx = highx + rhex + rhex*sqrt(3)/2;
	}
	
	highx = lastx;
	
	nwidth = floor( frwidth / (rhex*sqrt(3)));
	nheight = 1+ floor( (frheight - 2*rhex)/(rhex + rhex/2));
	
	highx = 2*rhex + (nheight-1)*(rhex + rhex/2);

// offset of first hexagon in upper left

	
	offx = offsetx + 0.5*(frwidth - nwidth*rhex*sqrt(3));
	
	offy = offsety + 0.5*(frheight - highx);

	offsetx = offsety = 0;

	icell = 1;
	
	for (j=1;j<=nheight; j++)
	{	
		offsety = offsety + rhex;

		if (2*floor(j/2) == j)
		{
		// even rows offset centers
			offsetx = rhex*sqrt(3);
			for (i=1;i<nwidth; i++)
			{
				cellx[icell] = offx + offsetx + (i-1)*(rhex*sqrt(3));
				celly[icell] = offy + offsety + (j-1)*(rhex/2);
			//	DrawOval(cellx[icell], celly[icell], rhex/10);
				MakeHexROI(cellx[icell], celly[icell],rhex);
				roiManager("Add");				
				icell++;
			}
		}
		else
		{
		// odd rows no offset
			offsetx = rhex*sqrt(3)/2;
			for (i=1;i<=nwidth; i++)
			{
				cellx[icell] = offx + offsetx + (i-1)*(rhex*sqrt(3));
				celly[icell] = offy + offsety + (j-1)*(rhex/2);
			//	 DrawOval(cellx[icell], celly[icell], rhex/10);
				MakeHexROI(cellx[icell], celly[icell],rhex);
				roiManager("Add");
				icell++;
			}
		}	
	}
	ncells = icell-1;
}

function EliminateOutsiders()
{
//
// compare ROIs to eliminate ROIs that lie outside ROI-zero
// each time an ROI is eliminated the list is updated...
//
	stackID = getImageID();
	
	nrois = roiManager("Count");
	roiManager("Select", 0);
	getStatistics(area1);

	i = 1;
	nrois = roiManager("Count");
	while (i < nrois)
	{
		setKeyDown("none");
		selectImage(stackID);
		roiManager("Select", 0);
		setKeyDown("shift");
		roiManager("Select", i);
		setKeyDown("none");
		getStatistics(areaboth);
		//
		//	check for overlapping selections
		//
		if (areaboth == area1) // ROI i is completely contained within ROI-zero
		{
			// do nothing
			i++;
		}
		else	// the areas are completely different or they partially overlap
		{
			roiManager("Select",i);
			roiManager("Delete");
		}
		nrois = roiManager("Count");
	}
}

function AllHexStackAveIntensity()
{
//
//
// calculate the average intensity for the entire set of hex ROIs in all the slices.
//
//

//
// first create a super-hex ROI that includes all the hex ROIs.
//
	nrois = roiManager("Count");
	
	//
	// ROI 0 is the large "cell-enclosing" ROI
	// ROI 1...nrois are the smaller hex ROIs
	//
	
	roiManager("Select", 1);
	for (i=2;i<nrois; i++)
	{
		setKeyDown("shift");   // -shift select- adds the ROI to the existing ROI
		roiManager("Select", i);
	}
	
//
// then advance through the stack adding the mean intensity of each slice.
//	and calculate the average intenstiy (all hexROI - all slices)
//
	stackintens = 0;
	for (n=1; n<=nSlices; n++) 
	{	
		setSlice(n);
		run("Measure");
		hexslice = getResult("Mean");
		stackintens = stackintens + hexslice;
	}
	stackintens = stackintens/nSlices;
	return stackintens;
}



macro "DrillwithinROIforAster"
{

//
//	Set the patch size for hexagons.
//
	var hexradius = 8;
	
//
//	Set the threshold to categorize patch as an F-actin contraction.
//
	var actinthresh = 1.2;
	
	rawstack = getTitle();	
	getSelectionBounds(xbox, ybox, rwidth, rheight);
	if (rwidth == 0)
	{
		ShowMessage("Requires an ROI drawn within a cell");
		exit;
	}
	roiManager("Add");
	

	var bigstring = "";
	HexROIFill(hexradius, xbox, ybox, rwidth, rheight);
	EliminateOutsiders();
	nrois = roiManager("Count");

	run("Set Measurements...", "  mean slice redirect=None decimal=6");
	
	stackintens = AllHexStackAveIntensity();
	
//
//
//
	selectWindow(rawstack);
	getDimensions(rwidth, rheight, rchannels, rslices, rframes);

	newImage("Actin Contraction Stack", "8-bit black", rwidth, rheight, rslices);
	actstack = getTitle();
	
	selectWindow(rawstack);
//
//
//	
	setColor(255);
	
	setBatchMode(true);
	for (i=1;i<nrois; i++)
	{
		bigstring = toString(i) + fromCharCode(9);
		roiManager("Select",i);
		for (n=1; n<=nSlices; n++) 
		{	
			selectWindow(rawstack);

			
			roiManager("Select",i);
			setSlice(n);
			
			run("Measure");
			hexintens = getResult("Mean");
			
			if ( hexintens > stackintens*actinthresh)
			{	
				
				selectWindow(actstack);
				roiManager("Select",i);
				setSlice(n);
				setColor(255);
				fill();

			}
			
			else
			{
				hexintens=0;
				
				//
				// Comment out the line above to store "non-contraction" intensities in the log file.
				//
			 }

			bigstring = bigstring + toString(hexintens) + fromCharCode(9);
		}
				
		
		print (bigstring);
		bigstring = "";
	}

	setBatchMode("exit and display");
}
//
// 	For an interesting representation of this analysis displayed on your original
//	try the following process manually...
//
//	imageCalculator("Multiply create 32-bit stack", rawstack, actstack); 	// Image - Image Calculator
//	run("Divide...", "value=255.000000 stack"); 				// Image - Math
//	setMinAndMax(0, 255); 							// Image - Adjust brightness contrast
//	run("8-bit"); 								// Image - Type
//	tempstack = getTitle();	
//	run("Merge Channels...", "c4="+rawstack+" c7="+tempstack);} 		// Image - Color - Merge Channels


