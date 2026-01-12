# 定义目标目录
$targetDir = 'F:\work\prime-quartz_unzipped\prime-quartz-main\content\publications'

# 从177到1遍历文件夹
for ($i = 177; $i -ge 1; $i--) {
    # 构建文件夹路径
    $folderName = "paper_block_$i"
    $folderPath = Join-Path -Path $targetDir -ChildPath $folderName
    $filePath = Join-Path -Path $folderPath -ChildPath "index.md"
    
    # 检查文件是否存在
    if (Test-Path -Path $filePath) {
        # 读取文件内容
        $content = Get-Content -Path $filePath -Raw
        
        # 提取date字段值
        $dateMatch = [regex]::Match($content, 'date:\s*"([0-9]{4}-[0-9]{2}-[0-9]{2})"')
        if ($dateMatch.Success) {
            $currentDateStr = $dateMatch.Groups[1].Value
            $currentDate = Get-Date -Date $currentDateStr
            
            # 如果不是第一个文件，检查是否需要修改日期
            if ($i -ne 177) {
                if ($currentDate -eq $previousDate) {
                    # 日期相同，日数+1
                    $newDate = $currentDate.AddDays(1)
                    $newDateStr = $newDate.ToString("yyyy-MM-dd")
                    
                    # 更新文件内容 - 使用单引号和字符串连接
                    $newDateLine = 'date: "' + $newDateStr + '"'
                    $content = $content -replace 'date:\s*"[0-9]{4}-[0-9]{2}-[0-9]{2}"', $newDateLine
                    Set-Content -Path $filePath -Value $content
                    
                    # 输出结果 - 使用字符串连接避免转义问题
                    Write-Host ('Updated ' + $folderName + ': ' + $currentDateStr + ' -> ' + $newDateStr)
                    
                    # 更新previousDate为新日期
                    $previousDate = $newDate
                } else {
                    # 日期不同，直接更新previousDate
                    $previousDate = $currentDate
                    Write-Host ('Kept ' + $folderName + ': ' + $currentDateStr)
                }
            } else {
                # 第一个文件，初始化previousDate
                $previousDate = $currentDate
                Write-Host ('Initial ' + $folderName + ': ' + $currentDateStr)
            }
        } else {
            Write-Host ('No date found in ' + $folderName)
        }
    } else {
        Write-Host ('File not found: ' + $filePath)
    }
}