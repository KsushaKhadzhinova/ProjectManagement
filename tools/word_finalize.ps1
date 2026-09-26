# Финализация отчёта по СТП 01–2017 в Microsoft Word:
#  - таблицы, переходящие на следующую страницу, разбиваются; перед продолжением ставится
#    «Продолжение таблицы N» (п. 2.6 СТП) и повторяется строка заголовков;
#  - обновляются поля: содержание, номера страниц;
#  - сохраняется копия в PDF.
# Запуск:  powershell -ExecutionPolicy Bypass -File tools\word_finalize.ps1 -Path "<путь к .docx>" [-NoPdf]
param(
    [Parameter(Mandatory = $true)][string]$Path,
    [switch]$NoPdf
)
$ErrorActionPreference = 'Stop'
$full = (Resolve-Path -LiteralPath $Path).Path
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$wdPage = 3

function Get-TableNumber($table) {
    $p = $table.Range.Paragraphs.First.Previous()
    for ($k = 0; $k -lt 3 -and $p -ne $null; $k++) {
        $t = $p.Range.Text
        if ($t -match '^(Таблица|Продолжение таблицы)\s+([А-ЯA-Z]?\.?[\d\.]+)') { return $Matches[2].TrimEnd('.') }
        $p = $p.Previous()
    }
    return $null
}

try {
    $doc = $word.Documents.Open($full, $false, $false)
    $doc.Repaginate()
    $i = 1
    $splits = 0
    while ($i -le $doc.Tables.Count) {
        $t = $doc.Tables.Item($i)
        $num = Get-TableNumber $t
        $n = $t.Rows.Count
        $splitAt = 0
        if ($num -and $n -gt 2) {
            $prev = $t.Rows.Item(2).Range.Information($wdPage)
            for ($r = 3; $r -le $n; $r++) {
                $pg = $t.Rows.Item($r).Range.Information($wdPage)
                if ($pg -ne $prev) { $splitAt = $r; break }
                $prev = $pg
            }
        }
        if ($splitAt -gt 0) {
            $new = $t.Split($splitAt)
            $gap = $new.Range.Paragraphs.First.Previous()
            $gap.Range.InsertBefore("Продолжение таблицы $num")
            $gap.Format.FirstLineIndent = 0
            $gap.Format.LeftIndent = 0
            $gap.Alignment = 0
            $gap.Format.KeepWithNext = $true
            $gap.Range.Font.Bold = $false
            $gap.Range.Font.Size = 14
            $new.Rows.Add($new.Rows.Item(1)) | Out-Null
            $hdr = $t.Rows.Item(1)
            for ($c = 1; $c -le $hdr.Cells.Count; $c++) {
                $src = $hdr.Cells.Item($c).Range
                $src.MoveEnd(1, -1) | Out-Null
                $dst = $new.Rows.Item(1).Cells.Item($c).Range
                $dst.MoveEnd(1, -1) | Out-Null
                $dst.FormattedText = $src.FormattedText
            }
            $new.Rows.Item(1).HeadingFormat = $true
            $splits++
            $doc.Repaginate()
        }
        $i++
    }
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    $doc.Fields.Update() | Out-Null
    $doc.Repaginate()
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    $doc.Save()
    $pages = $doc.ComputeStatistics(2)
    if (-not $NoPdf) {
        $pdf = [System.IO.Path]::ChangeExtension($full, '.pdf')
        $doc.ExportAsFixedFormat($pdf, 17)
        Write-Output "PDF: $pdf"
    }
    Write-Output "Pages: $pages; table splits: $splits"
    $doc.Close($false)
} finally {
    $word.Quit()
}
