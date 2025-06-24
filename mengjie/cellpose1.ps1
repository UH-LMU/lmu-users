$folder = 'data folder here'

ls $folder

$filter = 'mCherry'
$diameter = 190
$output = 'output folder here'

cellpose --use_gpu --dir $folder --img_filter $filter --diameter $diameter --save_png --no_npy --save_rois --savedir $output --verbose
