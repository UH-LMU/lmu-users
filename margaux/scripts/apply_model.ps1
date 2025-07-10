## Step 3: Apply a model to data in subfolders. Save e.g. as step3_apply_model.ps1

# History or examples as comments
#$model = "E:\LocalData\vizcaino\2025-02-11_B16_wt_G8_C2_E1_A1_H3\Plate1\models\avc20250309"
#$plate = "E:\LocalData\vizcaino\2025-02-11_B16_wt_G8_C2_E1_A1_H3\Plate1"
#$plate_out = "E:\LocalData\vizcaino\2025-02-11_B16_wt_G8_C2_E1_A1_H3\Plate1_output_avc20250309"

$model = "L:\lmu_active2\users\m\margauxh\test\Plate1\models\mh20250710a_confluent"
$plate = "L:\lmu_active2\users\m\margauxh\test\Plate1"
$plate_out = "L:\lmu_active2\users\m\margauxh\test\Plate1_output_mh20250710a_confluent"

C:\hyapp\cellpose_celliq.ps1 $model 50 $plate $plate_out