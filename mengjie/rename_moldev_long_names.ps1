param (
    [string]$InputFolder
)

# Check if the input folder exists
if (-Not (Test-Path $InputFolder)) {
    Write-Host "The specified folder does not exist."
    exit
}

# Get all .tif files in the specified input folder
Get-ChildItem -Path $InputFolder -Filter "*.tif" | ForEach-Object {
    $newName = $_.Name -replace '(_w\d).*', '$1.tif'
    Rename-Item $_.FullName -NewName (Join-Path -Path $InputFolder -ChildPath $newName)
}

Write-Host "Renaming completed."