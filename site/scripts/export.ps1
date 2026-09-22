$ErrorActionPreference = 'Stop'
$siteDirectory = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Write-ProjectArchive {
    param([string]$Name, [object[]]$Files, [string]$BaseDirectory)
    $archivePath = Join-Path $siteDirectory $Name
    $stream = [System.IO.File]::Open($archivePath, [System.IO.FileMode]::Create)
    $archive = [System.IO.Compression.ZipArchive]::new($stream, [System.IO.Compression.ZipArchiveMode]::Create)
    try {
        foreach ($file in ($Files | Sort-Object FullName -Unique)) {
            $entryName = [System.IO.Path]::GetRelativePath($BaseDirectory, $file.FullName).Replace('\', '/')
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $file.FullName, $entryName, [System.IO.Compression.CompressionLevel]::Optimal) | Out-Null
        }
    } finally {
        $archive.Dispose()
        $stream.Dispose()
    }
    Get-Item -LiteralPath $archivePath | Select-Object Name, Length
}

$sourcePaths = @('src','public','scripts','package.json','package-lock.json','vite.config.js','index.html','render-lab.html','README.md','DESIGN_NOTES.md','CHANGE_LIST.md','SITE_BRIEF.md','.gitignore','qa/font-source.css','qa/font-originals','qa/assembly/source-register.md','qa/assembly/blind-review.md')
$sourceFiles = foreach ($relativePath in $sourcePaths) { Get-ChildItem -LiteralPath (Join-Path $siteDirectory $relativePath) -File -Recurse -Force }
$sourceFiles += Get-ChildItem -LiteralPath (Join-Path $siteDirectory 'revisions/first-build') -Filter '*.md' -File
$sourceFiles += Get-ChildItem -LiteralPath (Join-Path $siteDirectory 'revisions/scroll-edition') -Filter '*.md' -File
Write-ProjectArchive -Name 'bingbong-source.zip' -Files $sourceFiles -BaseDirectory $siteDirectory

$distDirectory = Join-Path $siteDirectory 'dist'
Write-ProjectArchive -Name 'bingbong-static.zip' -Files (Get-ChildItem -LiteralPath $distDirectory -File -Recurse) -BaseDirectory $distDirectory

$reviewFiles = Get-ChildItem -LiteralPath (Join-Path $siteDirectory 'qa') -File -Recurse | Where-Object { $_.FullName -notmatch '-frames[\\/]' -and $_.FullName -notmatch 'font-originals[\\/]' }
$reviewFiles += Get-Item -LiteralPath (Join-Path $siteDirectory 'DESIGN_NOTES.md'), (Join-Path $siteDirectory 'CHANGE_LIST.md')
Write-ProjectArchive -Name 'bingbong-review.zip' -Files $reviewFiles -BaseDirectory $siteDirectory
