# Обновляет поля (содержание, номера страниц) в .docx через Microsoft Word и сохраняет копию в PDF.
# Запуск:  powershell -ExecutionPolicy Bypass -File tools\word_finalize.ps1 -Path "<путь к .docx>" [-NoPdf]
param(
    [Parameter(Mandatory = $true)][string]$Path,
    [switch]$NoPdf
)
$full = (Resolve-Path -LiteralPath $Path).Path
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($full, $false, $false)
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    $doc.Fields.Update() | Out-Null
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    $doc.Save()
    $pages = $doc.ComputeStatistics(2)
    if (-not $NoPdf) {
        $pdf = [System.IO.Path]::ChangeExtension($full, '.pdf')
        $doc.ExportAsFixedFormat($pdf, 17)
        Write-Output "PDF: $pdf"
    }
    Write-Output "Pages: $pages"
    $doc.Close($false)
} finally {
    $word.Quit()
}
