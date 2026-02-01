# 修复UTF-8编码问题的PowerShell脚本

# 定义要处理的目录
$targetDirectory = "content/publications"

# 获取所有index.md文件
$files = Get-ChildItem -Path $targetDirectory -Recurse -Filter "index.md"

# 定义要替换的错误字符和正确的替换
$replacements = @{
    'â' = '-'
    'â' = '-'
    'â' = '-'
    'â¢' = '-'
    'â¦' = '...'
    'â' = '"'
    'â' = '"'
    'â' = "'"
    'â' = "'"
}

# 处理每个文件
foreach ($file in $files) {
    Write-Host "Processing $($file.FullName)..."
    
    try {
        # 读取文件内容
        $content = Get-Content -Path $file.FullName -Encoding UTF8 -Raw
        
        # 定义要替换的错误字符模式
        $patterns = @(
            'â\u0088\u0092',  # 错误的减号
            'â\u0080\u0094',  # 错误的破折号
            'â\u0080\u0093',  # 错误的短破折号
            'â\u0080\u0099',  # 错误的单引号
            'â\u0080\u0098',  # 错误的单引号
            'â\u0080\u009d',  # 错误的双引号
            'â\u0080\u009c',  # 错误的双引号
            'â\u0080\u00a6',  # 错误的省略号
            'â\u0080\u00a2'   # 错误的项目符号
        )
        
        # 检查是否包含错误字符
        $hasErrors = $false
        foreach ($pattern in $patterns) {
            if ($content -match $pattern) {
                $hasErrors = $true
                break
            }
        }
        
        if ($hasErrors) {
            # 替换错误字符
            $newContent = $content
            $newContent = $newContent -replace 'â\u0088\u0092', '-'
            $newContent = $newContent -replace 'â\u0080\u0094', '-'
            $newContent = $newContent -replace 'â\u0080\u0093', '-'
            $newContent = $newContent -replace 'â\u0080\u0099', "'"
            $newContent = $newContent -replace 'â\u0080\u0098', "'"
            $newContent = $newContent -replace 'â\u0080\u009d', '"'
            $newContent = $newContent -replace 'â\u0080\u009c', '"'
            $newContent = $newContent -replace 'â\u0080\u00a6', '...'
            $newContent = $newContent -replace 'â\u0080\u00a2', '-'
            
            # 写入修复后的内容
            Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
            Write-Host "  Fixed encoding issues in $($file.FullName)"
        } else {
            Write-Host "  No encoding issues found in $($file.FullName)"
        }
    } catch {
        Write-Host "  Error processing $($file.FullName): $($_.Exception.Message)"
    }
}

Write-Host "Processing complete!"
