# 修复UTF-8编码问题的简单PowerShell脚本

# 定义要处理的目录
$targetDirectory = "content/publications"

# 获取所有index.md文件
$files = Get-ChildItem -Path $targetDirectory -Recurse -Filter "index.md"

# 处理每个文件
foreach ($file in $files) {
    Write-Host "Processing $($file.FullName)..."
    
    try {
        # 读取文件内容
        $content = Get-Content -Path $file.FullName -Encoding UTF8 -Raw
        
        # 检查是否包含错误字符
        if ($content -match 'â') {
            # 替换常见的错误字符
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
