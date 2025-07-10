#$model = "D:\HJ20250217\vizcaino\Plate1\models\AVC202502211558"
$plate = "L:\lmu_active2\users\m\margauxh\test\Plate1"
$model_out = "mh20250710a_confluent"

$diam = 50

# --pretrained_model $model
cellpose --use_gpu --train --diam_mean $diam --dir $plate --look_one_level_down --model_name_out $model_out --mask_filter _seg.npy --verbose