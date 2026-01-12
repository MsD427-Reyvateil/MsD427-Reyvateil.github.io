$indexFile = 'f:\work\prime-quartz_unzipped\prime-quartz-main\content\Members\_index.md'
$membersDir = 'f:\work\prime-quartz_unzipped\prime-quartz-main\content\Members'

# Get all referenced icons from _index.md
$content = Get-Content -Path $indexFile
$icons = @()
foreach ($line in $content) {
    if ($line -match 'icon: (.+\.jpg)') {
        $icon = $matches[1].Trim()
        $icons += $icon
    }
}

Write-Output "Referenced icons in _index.md:"
Write-Output "----------------------------------"
$allExist = $true

foreach ($icon in $icons) {
    $iconPath = Join-Path -Path $membersDir -ChildPath $icon
    $exists = Test-Path -Path $iconPath
    
    if ($exists) {
        Write-Output "✓ $icon"
    } else {
        Write-Output "✗ $icon - Missing!"
        $allExist = $false
    }
}

Write-Output "----------------------------------"
if ($allExist) {
    Write-Output "All icons exist in the Members directory."
} else {
    Write-Output "Some icons are missing. Please check the above list."
}
