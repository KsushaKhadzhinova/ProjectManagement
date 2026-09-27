Attribute VB_Name = "modRiskMap"
'===============================================================
' modRiskMap
' Файл: "Карта рисков в Excel_с форматированием -26 (3).xlsx"
' Назначение: заполнить реестр рисков проекта NotaCode на листе
' "Таблица с рисками", пересчитать коэффициенты, подписать точки
' на карте рисков и покрасить приоритет автоматически.
'
' Как использовать:
'   1. Открыть Карта рисков в Excel_с форматированием -26 (3).xlsx
'      (или его копию risk-map.xlsx в docs/project-management/).
'   2. Alt+F11 -> Insert -> Module -> вставить этот код.
'   3. Курсор в любую процедуру -> F5, либо запустить
'      FillRiskRegister из диалога макросов (Alt+F8).
'===============================================================
Option Explicit

Private Type TRisk
    Name As String
    Category As String
    Prob As Double      ' 1..5
    Impact As Double    ' 1..5
    Measures As String
End Type

Private Function GetRisks() As TRisk()
    Dim r() As TRisk
    ReDim r(1 To 15)

    r(1).Name = "Один разработчик держит весь проект (bus factor)"
    r(1).Category = "Организационный": r(1).Prob = 3: r(1).Impact = 5
    r(1).Measures = "Полная документация архитектуры и решений; AI-агенты как виртуальная команда Review Board"

    r(2).Name = "Требование 100% покрытия тестами замедляет разработку"
    r(2).Category = "Технический": r(2).Prob = 4: r(2).Impact = 3
    r(2).Measures = "TDD с первого дня, чистое доменное ядро, моки портов"

    r(3).Name = "Распределённая архитектура (5+ сервисов) слишком велика для срока"
    r(3).Category = "Технический": r(3).Prob = 4: r(3).Impact = 4
    r(3).Measures = "Walking skeleton в S0, подключение сервисов по одному, Could-функции за пределами MVP"

    r(4).Name = "Лимиты бесплатных AI-провайдеров и хостинга исчерпаны раньше защиты"
    r(4).Category = "Внешний": r(4).Prob = 3: r(4).Impact = 3
    r(4).Measures = "AI-заглушка по умолчанию, мониторинг квот, деградация до заглушки"

    r(5).Name = "Расхождение ключей нотаций между фронтом и бэком"
    r(5).Category = "Технический": r(5).Prob = 3: r(5).Impact = 4
    r(5).Measures = "Единый каталог нотаций в packages/contracts, общие контрактные тесты"

    r(6).Name = "Stored XSS при рендере SVG подписей узлов"
    r(6).Category = "Безопасность": r(6).Prob = 2: r(6).Impact = 5
    r(6).Measures = "Экранирование на сервере, DOMPurify, securityLevel=strict для Mermaid"

    r(7).Name = "Лабораторные работы съедают время продуктовой разработки"
    r(7).Category = "Процесс": r(7).Prob = 4: r(7).Impact = 3
    r(7).Measures = "Дорожка Expedite не более 1 карточки; лаба = часть продукта"

    r(8).Name = "Дата защиты курсовой не подтверждена официально"
    r(8).Category = "Внешний": r(8).Prob = 3: r(8).Impact = 3
    r(8).Measures = "Уточнить у руководителя; буфер в S12"

    r(9).Name = "Грамматика DSL допускает конструкции, отклоняемые профилем нотации"
    r(9).Category = "Технический": r(9).Prob = 3: r(9).Impact = 3
    r(9).Measures = "Общие тесты грамматики и профилей нотаций с первого спринта"

    r(10).Name = "Требования по волнам нотаций противоречивы (2 разных списка в ТЗ)"
    r(10).Category = "Требования": r(10).Prob = 4: r(10).Impact = 3
    r(10).Measures = "Зафиксировать волну 1 как единственный источник правды до старта E3"

    r(11).Name = "Совместное редактирование диаграммы вызовет гонку состояний"
    r(11).Category = "Технический": r(11).Prob = 2: r(11).Impact = 4
    r(11).Measures = "Вне MVP (Won't); при реализации - locking 'один активный редактор'"

    r(12).Name = "Секреты/API-ключи AI-провайдеров попадут в клиентский бандл"
    r(12).Category = "Безопасность": r(12).Prob = 2: r(12).Impact = 5
    r(12).Measures = "Ключи и системные промпты только на сервере, ревью nc-security"

    r(13).Name = "OAuth-квоты/условия GitHub, Google, LLM-провайдеров изменятся"
    r(13).Category = "Внешний": r(13).Prob = 2: r(13).Impact = 3
    r(13).Measures = "Мониторинг changelog/статус-страниц еженедельно"

    r(14).Name = "Демо-стенд недоступен в неделю защиты"
    r(14).Category = "Инфраструктура": r(14).Prob = 2: r(14).Impact = 5
    r(14).Measures = "Health-check (UptimeRobot), резервный запуск через Docker Compose"

    r(15).Name = "Скрытые 'кнопки-пустышки' обнаружатся поздно перед защитой"
    r(15).Category = "Качество": r(15).Prob = 3: r(15).Impact = 4
    r(15).Measures = "UI-чек-лист 'все кнопки работают' - часть DoD каждый спринт"

    GetRisks = r
End Function

Public Sub FillRiskRegister()
    Dim ws As Worksheet
    Dim risks() As TRisk
    Dim i As Long, rowIdx As Long
    Dim coeff As Double

    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets("Таблица с рисками")
    On Error GoTo 0
    If ws Is Nothing Then
        MsgBox "Лист 'Таблица с рисками' не найден.", vbCritical
        Exit Sub
    End If

    ws.Range("A1").Value = "NotaCode"

    risks = GetRisks()
    rowIdx = 4 ' первая строка данных в шаблоне
    For i = LBound(risks) To UBound(risks)
        ws.Cells(rowIdx, "C").Value = risks(i).Name          ' Наименование риска
        ws.Cells(rowIdx, "D").Value = risks(i).Category       ' Влияние/категория
        ws.Cells(rowIdx, "F").Value = risks(i).Prob / 5#      ' нормировано в 0..1
        ws.Cells(rowIdx, "G").Value = risks(i).Impact / 5#
        coeff = (risks(i).Prob / 5#) * (risks(i).Impact / 5#)
        ws.Cells(rowIdx, "H").Value = coeff                   ' итоговый коэффициент
        ws.Cells(rowIdx, "I").Value = risks(i).Measures
        rowIdx = rowIdx + 1
    Next i

    MsgBox "Реестр рисков заполнен: " & (UBound(risks) - LBound(risks) + 1) & " строк.", vbInformation
End Sub

' Автоматическое построение подписей данных на карте рисков:
' воспроизводит вручную описанные в файле шаги (добавить подписи,
' убрать "значения X"/"линии выноски", подставить подписи из ячеек
' с краткими названиями рисков).
Public Sub LabelRiskMapPoints()
    Dim wsMap As Worksheet
    Dim ch As ChartObject
    Dim wsData As Worksheet
    Dim namesRange As Range

    On Error Resume Next
    Set wsMap = ThisWorkbook.Worksheets("Карта рисков")
    Set wsData = ThisWorkbook.Worksheets("Таблица с рисками")
    On Error GoTo 0
    If wsMap Is Nothing Or wsData Is Nothing Then
        MsgBox "Не найдены листы 'Карта рисков' и/или 'Таблица с рисками'.", vbCritical
        Exit Sub
    End If

    If wsMap.ChartObjects.Count = 0 Then
        MsgBox "На листе 'Карта рисков' не найдено ни одной диаграммы.", vbExclamation
        Exit Sub
    End If

    Set namesRange = wsData.Range("C4:C18") ' краткие названия рисков

    For Each ch In wsMap.ChartObjects
        Dim srs As Series
        For Each srs In ch.Chart.SeriesCollection
            srs.HasDataLabels = True
            Dim dl As DataLabels
            Set dl = srs.DataLabels
            dl.ShowValue = False
            dl.ShowSeriesName = False
            dl.ShowCategoryName = False
            On Error Resume Next
            dl.ShowRange = True                 ' "Значение из ячеек" (Excel 2013+)
            srs.DataLabels.Format.TextFrame2.TextRange.Text = ""
            Dim j As Long
            For j = 1 To srs.Points.Count
                If j <= namesRange.Cells.Count Then
                    srs.Points(j).DataLabel.Text = namesRange.Cells(j, 1).Value
                End If
            Next j
            On Error GoTo 0
        Next srs
    Next ch

    MsgBox "Подписи точек на карте рисков обновлены.", vbInformation
End Sub

' Точка входа: заполнить реестр и сразу подписать карту.
Public Sub RunAll()
    FillRiskRegister
    LabelRiskMapPoints
End Sub
