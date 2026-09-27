Attribute VB_Name = "modGanttCriticalPath"
'===============================================================
' modGanttCriticalPath
' Файл: "Планировщик проекта на основе диаграммы Ганта - 60121 (3).xlsx"
' Назначение: заполнить лист "ТАБЛИЦА ДАННЫХ" работами WBS проекта
' NotaCode, рассчитать по методу критического пути (CPM) ранние и
' поздние сроки (ES/EF/LS/LF), резерв времени, и покрасить критический
' путь на листе "Планировщик проекта" красным цветом.
'
' Как использовать:
'   1. Открыть Планировщик проекта на основе диаграммы Ганта - 60121 (3).xlsx.
'   2. Alt+F11 -> Insert -> Module -> вставить этот код.
'   3. Alt+F8 -> RunAll -> Выполнить.
'===============================================================
Option Explicit

Private Type TTask
    Code As String
    Name As String
    Dur As Double        ' длительность, месяцы
    PredList As String   ' коды предшественников через запятую, "-" если нет
    ES As Double
    EF As Double
    LS As Double
    LF As Double
    Slack As Double
    Critical As Boolean
End Type

Private Function GetTasks() As TTask()
    Dim t() As TTask
    ReDim t(1 To 15)

    t(1).Code = "1.0": t(1).Name = "Бизнес-анализ и требования": t(1).Dur = 0.5: t(1).PredList = "-"
    t(2).Code = "2.0": t(2).Name = "Архитектура и ADR": t(2).Dur = 0.5: t(2).PredList = "1.0"
    t(3).Code = "3.0": t(3).Name = "Фундамент (CI, Docker, walking skeleton)": t(3).Dur = 0.5: t(3).PredList = "2.0"
    t(4).Code = "4.0": t(4).Name = "Gateway и доступ (Express, Sequelize, JWT)": t(4).Dur = 1: t(4).PredList = "3.0"
    t(5).Code = "5.0": t(5).Name = "Язык DSL (грамматика, парсер, диагностика)": t(5).Dur = 1: t(5).PredList = "3.0"
    t(6).Code = "6.0": t(6).Name = "Web IDE (оболочка, Monaco, темы, панели)": t(6).Dur = 1.5: t(6).PredList = "5.0"
    t(7).Code = "7.0": t(7).Name = "Нотации волны 1 (UML, ERD, IDEF0)": t(7).Dur = 1.5: t(7).PredList = "5.0"
    t(8).Code = "8.0": t(8).Name = "Холст (SVG, elkjs, подсветка)": t(8).Dur = 1: t(8).PredList = "5.0"
    t(9).Code = "9.0": t(9).Name = "Сохранение и интеграции (БД, GitHub, Drive)": t(9).Dur = 1: t(9).PredList = "4.0,6.0"
    t(10).Code = "10.0": t(10).Name = "Экспорт/импорт форматов": t(10).Dur = 0.5: t(10).PredList = "7.0"
    t(11).Code = "11.0": t(11).Name = "AI-ассистент (заглушка, режимы)": t(11).Dur = 0.5: t(11).PredList = "6.0"
    t(12).Code = "12.0": t(12).Name = "Версии, diff, откат": t(12).Dur = 0.5: t(12).PredList = "9.0"
    t(13).Code = "13.0": t(13).Name = "Качество и наблюдаемость": t(13).Dur = 0.5: t(13).PredList = "7.0,8.0,9.0,10.0,11.0,12.0"
    t(14).Code = "14.0": t(14).Name = "Документация и РПЗ курсовой": t(14).Dur = 0.75: t(14).PredList = "13.0"
    t(15).Code = "15.0": t(15).Name = "Стабилизация MVP, буфер, защита": t(15).Dur = 0.25: t(15).PredList = "14.0"

    GetTasks = t
End Function

Private Function FindIndex(tasks() As TTask, code As String) As Long
    Dim i As Long
    For i = LBound(tasks) To UBound(tasks)
        If tasks(i).Code = code Then
            FindIndex = i
            Exit Function
        End If
    Next i
    FindIndex = -1
End Function

Private Function SplitPreds(s As String) As String()
    If s = "-" Or Trim(s) = "" Then
        SplitPreds = Split("", ",")
    Else
        SplitPreds = Split(s, ",")
    End If
End Function

Public Sub CalculateCPM()
    Dim tasks() As TTask
    Dim i As Long, j As Long
    Dim preds() As String
    Dim projectDuration As Double

    tasks = GetTasks()

    ' --- Прямой проход: ES/EF (задачи уже в топологическом порядке) ---
    For i = LBound(tasks) To UBound(tasks)
        preds = SplitPreds(tasks(i).PredList)
        Dim maxEF As Double
        maxEF = 0
        For j = LBound(preds) To UBound(preds)
            If Trim(preds(j)) <> "" Then
                Dim idx As Long
                idx = FindIndex(tasks, Trim(preds(j)))
                If idx >= 0 Then
                    If tasks(idx).EF > maxEF Then maxEF = tasks(idx).EF
                End If
            End If
        Next j
        tasks(i).ES = maxEF
        tasks(i).EF = tasks(i).ES + tasks(i).Dur
    Next i

    projectDuration = 0
    For i = LBound(tasks) To UBound(tasks)
        If tasks(i).EF > projectDuration Then projectDuration = tasks(i).EF
    Next i

    ' --- Обратный проход: LF/LS (идём с конца, ищем последователей) ---
    For i = UBound(tasks) To LBound(tasks) Step -1
        Dim minLS As Double
        Dim hasSucc As Boolean
        hasSucc = False
        minLS = projectDuration
        For j = LBound(tasks) To UBound(tasks)
            preds = SplitPreds(tasks(j).PredList)
            Dim k As Long
            For k = LBound(preds) To UBound(preds)
                If Trim(preds(k)) = tasks(i).Code Then
                    hasSucc = True
                    If tasks(j).LS < minLS Then minLS = tasks(j).LS
                End If
            Next k
        Next j
        If Not hasSucc Then
            tasks(i).LF = projectDuration
        Else
            tasks(i).LF = minLS
        End If
        tasks(i).LS = tasks(i).LF - tasks(i).Dur
        tasks(i).Slack = Round(tasks(i).LS - tasks(i).ES, 3)
        tasks(i).Critical = (Abs(tasks(i).Slack) < 0.0001)
    Next i

    ' --- Запись в лист "ТАБЛИЦА ДАННЫХ" ---
    Dim ws As Worksheet
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets("ТАБЛИЦА ДАННЫХ")
    On Error GoTo 0
    If ws Is Nothing Then
        MsgBox "Лист 'ТАБЛИЦА ДАННЫХ' не найден.", vbCritical
        Exit Sub
    End If

    Dim rowIdx As Long
    rowIdx = 8 ' первая строка данных в шаблоне
    For i = LBound(tasks) To UBound(tasks)
        ws.Cells(rowIdx, "B").Value = i                       ' №
        ws.Cells(rowIdx, "C").Value = tasks(i).Name           ' ЗАДАЧА
        ws.Cells(rowIdx, "D").Value = tasks(i).PredList       ' ПРЕДШЕСТВУЮЩИЕ РАБОТЫ
        ws.Cells(rowIdx, "F").Value = tasks(i).ES             ' РАННИЙ СТАРТ
        ws.Cells(rowIdx, "G").Value = tasks(i).Dur            ' ДЛИТЕЛЬНОСТЬ
        ws.Cells(rowIdx, "H").Value = tasks(i).EF             ' РАННИЙ ФИНИШ
        ws.Cells(rowIdx, "I").Value = tasks(i).LS             ' ПОЗДНИЙ СТАРТ
        ws.Cells(rowIdx, "J").Value = tasks(i).LF             ' ПОЗДНИЙ ФИНИШ
        ws.Cells(rowIdx, "K").Value = tasks(i).Slack          ' РЕЗЕРВ
        ws.Cells(rowIdx, "L").Value = IIf(tasks(i).Critical, "ДА", "НЕТ ") ' КРИТИЧЕСКИЙ ПУТЬ
        rowIdx = rowIdx + 1
    Next i

    MsgBox "Расчёт CPM выполнен. Длительность проекта: " & projectDuration & " мес." & vbCrLf & _
           "Критических работ: " & CriticalCount(tasks), vbInformation

    HighlightCriticalPath tasks
End Sub

Private Function CriticalCount(tasks() As TTask) As Long
    Dim i As Long, c As Long
    For i = LBound(tasks) To UBound(tasks)
        If tasks(i).Critical Then c = c + 1
    Next i
    CriticalCount = c
End Function

' Красит строки критического пути на листе "Планировщик проекта"
' (столбец I "КРИТИЧЕСКИЙ ПУТЬ" = 100%) в красный цвет заливки строки 3..29.
Private Sub HighlightCriticalPath(tasks() As TTask)
    Dim wsPlan As Worksheet
    On Error Resume Next
    Set wsPlan = ThisWorkbook.Worksheets("Планировщик проекта")
    On Error GoTo 0
    If wsPlan Is Nothing Then Exit Sub

    Dim r As Long
    For r = 5 To 5 + UBound(tasks) - LBound(tasks)
        Dim critVal As Variant
        critVal = wsPlan.Cells(r, "I").Value
        If critVal = 1 Or critVal = "100%" Then
            wsPlan.Range(wsPlan.Cells(r, "C"), wsPlan.Cells(r, "F")).Interior.Color = RGB(255, 199, 206)
            wsPlan.Range(wsPlan.Cells(r, "C"), wsPlan.Cells(r, "F")).Font.Color = RGB(156, 0, 6)
        End If
    Next r
End Sub

Public Sub RunAll()
    CalculateCPM
End Sub
