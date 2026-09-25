Attribute VB_Name = "PZ3_NotaCode"
' =====================================================================
' ПЗ3. Реестр и карта рисков — NotaCode
' Файл-шаблон: "Карта рисков в Excel_с форматированием -26.xlsx"
'
' Как запустить:
'   1. Открыть шаблон, сохранить копию как .xlsm.
'   2. Alt+F11 -> File -> Import File... -> ПЗ3_NotaCode_Risks.bas (кодировка Windows-1251).
'   3. Alt+F8 -> PZ3_RunAll -> Выполнить.
'
' Что делает макрос:
'   - "Таблица с рисками": название проекта (C1), 13 рисков в Таблица1
'     (наименование, влияние, триггер, P, I, мероприятия), H = P*I — формула шаблона;
'     столбец J «Приоритет» (пороги 0,505 и 0,14), столбец K «Стратегия»,
'     условное форматирование H (красный/жёлтый/зелёный); удаляет образцы преподавателя (строки 41–68);
'   - "Карта рисков": точечная диаграмма шаблона перенастраивается на 13 рисков,
'     подписи точек R1…R13 берутся из столбца B;
'   - новый лист "Ранжирование": риски по убыванию H;
'   - новый лист "Тепловая матрица": 5x5 по шкалам шаблона 1–5 с номерами рисков.
' =====================================================================
Option Explicit

Private Const N As Long = 13
Private Const HIGH_T As Double = 0.505
Private Const LOW_T As Double = 0.14
Private Const PROJECT As String = "NotaCode — веб-IDE «diagram as code»"

Private rName(1 To N) As String, rImpact(1 To N) As String, rTrig(1 To N) As String
Private rP(1 To N) As Double, rI(1 To N) As Double, rStrat(1 To N) As String, rAct(1 To N) As String

Private Sub R(k As Long, nm As String, imp As String, trg As String, pp As Double, ii As Double, st As String, act As String)
    rName(k) = nm: rImpact(k) = imp: rTrig(k) = trg: rP(k) = pp: rI(k) = ii: rStrat(k) = st: rAct(k) = act
End Sub

Private Sub LoadRisks()
    R 1, "Объём распределённой архитектуры (7 сервисов) превышает ресурсы одного исполнителя", _
        "Срыв MVP к 13.12.2026, неполная демонстрация на защите", "Velocity ниже плана два спринта подряд", 0.7, 0.8, "Снижение", _
        "Walking skeleton в S0, поэтапное подключение сервисов, перенос Could have в Post-MVP"
    R 2, "Вытеснение продуктовых задач лабораторными работами ч. 2 (8 ЛР, 4 ПЗ)", _
        "Сдвиг спринтов продукта, накопление долга по MVP", "Лабораторная работа занимает более одного спринта", 0.6, 0.6, "Снижение", _
        "ЛР реализуется как компонент продукта (Gateway, Web IDE); дорожка Expedite с WIP = 1"
    R 3, "Расхождение грамматики DSL и профилей нотаций", _
        "Ошибки HTTP 500, ложная валидация, несовместимые синтаксисы", "Падение контрактных тестов каталога нотаций", 0.4, 0.7, "Уклонение", _
        "Единый каталог нотаций в packages/contracts; генерация подсветки, шаблонов и промптов из каталога"
    R 4, "Хранимая XSS-уязвимость через подписи узлов в SVG", _
        "Компрометация сессий пользователей, утечка данных", "Замечание аудита безопасности, срабатывание CSP", 0.3, 0.9, "Уклонение", _
        "Экранирование подписей, санитизация SVG (DOMPurify), политика CSP"
    R 5, "Требования 100 % покрытия и отсутствия комментариев замедляют разработку", _
        "Рост трудоёмкости задач на 20–30 %", "Блокировка слияния конвейером CI более двух дней", 0.5, 0.5, "Снижение", _
        "TDD с первого спринта, чистое доменное ядро, моки портов, линтер-правило запрета комментариев"
    R 6, "Отказ в согласовании Python-сервисов при рекомендованном стеке Node.js", _
        "Перенос Language и Workspace Service на Node.js, сдвиг MVP на 2–3 спринта", "Замечание руководителя по разделу 2.1 записки", 0.3, 0.8, "Снижение", _
        "Обоснование выбора в разделе 2.1, согласование в спринте S1; Gateway на Node.js закрывает ЛР1–ЛР8"
    R 7, "Перегрузка или болезнь единственного исполнителя", _
        "Остановка всех работ проекта", "Невыполнение цели спринта по причинам вне проекта", 0.3, 0.8, "Принятие", _
        "Буферный спринт S12, документация и ADR в репозитории, автоматизация рутинных задач"
    R 8, "Изменение или отмена бесплатных лимитов LLM API", _
        "AI-ассистент доступен только в режиме заглушки", "Ответы HTTP 429, отзыв ключа, закрытие сервиса", 0.5, 0.4, "Снижение", _
        "Адаптеры нескольких провайдеров (Gemini, Groq, OpenRouter, Mistral), заглушка по умолчанию, Ollama"
    R 9, "Изменение бесплатных тарифов хостинга (Render, Neon, CloudAMQP, Upstash)", _
        "Недоступность демо-стенда на защите", "Уведомление провайдера, превышение лимита", 0.3, 0.7, "Передача", _
        "Резервный провайдер (Fly.io), локальный стенд docker compose для демонстрации"
    R 10, "Время Run превышает 300 мс для диаграммы из 200 узлов", _
        "Невыполнение NFR производительности", "Результаты нагрузочного теста анализа", 0.3, 0.5, "Снижение", _
        "Кэш анализа в Redis по хэшу текста, elkjs в Web Worker, профилирование парсера"
    R 11, "Перенос даты защиты на более ранний срок", _
        "Сокращение объёма MVP", "Объявление расписания защиты", 0.3, 0.6, "Принятие", _
        "Запрос даты у руководителя в S1, приоритизация MoSCoW, перенос Should have в Post-MVP"
    R 12, "Утечка API-ключей и OAuth-токенов", _
        "Блокировка ключей, несанкционированные расходы, репутационный ущерб", "Срабатывание secret scanning GitHub", 0.2, 0.8, "Уклонение", _
        "Секреты только на сервере, шифрование токенов AES-GCM, gitleaks в CI"
    R 13, "Нарушение Закона РБ № 99-З при обработке персональных данных", _
        "Штраф, проверка НЦЗПД", "Запуск регистрации без политики обработки ПДн", 0.2, 0.6, "Уклонение", _
        "Политика обработки ПДн, согласие при регистрации, минимизация данных (e-mail, хэш пароля)"
End Sub

Private Function Level(h As Double) As String
    If h >= HIGH_T Then
        Level = "Высокий"
    ElseIf h >= LOW_T Then
        Level = "Средний"
    Else
        Level = "Низкий"
    End If
End Function

Private Function GetSheet(nameS As String) As Worksheet
    On Error Resume Next
    Set GetSheet = ThisWorkbook.Worksheets(nameS)
    On Error GoTo 0
    If GetSheet Is Nothing Then
        Set GetSheet = ThisWorkbook.Worksheets.Add(After:=ThisWorkbook.Worksheets(ThisWorkbook.Worksheets.Count))
        GetSheet.Name = nameS
    End If
End Function

Private Sub FillRiskTable()
    Dim ws As Worksheet, lo As ListObject, k As Long, rr As Long, fc As FormatCondition
    Set ws = ThisWorkbook.Worksheets("Таблица с рисками")
    ws.Range("C1").Value = PROJECT
    Set lo = ws.ListObjects(1)
    ' образцы преподавателя ниже таблицы шкал удаляются, шкалы (строки 27–34) сохраняются
    ws.Range("A41:K68").Clear
    lo.DataBodyRange.Columns(3).ClearContents
    lo.DataBodyRange.Columns(4).ClearContents
    lo.DataBodyRange.Columns(5).ClearContents
    lo.DataBodyRange.Columns(6).ClearContents
    lo.DataBodyRange.Columns(7).ClearContents
    lo.DataBodyRange.Columns(9).ClearContents
    For k = 1 To N
        rr = lo.HeaderRowRange.Row + k
        ws.Cells(rr, 1).Value = k
        ws.Cells(rr, 3).Value = rName(k)
        ws.Cells(rr, 4).Value = rImpact(k)
        ws.Cells(rr, 5).Value = rTrig(k)
        ws.Cells(rr, 6).Value = rP(k)
        ws.Cells(rr, 7).Value = rI(k)
        ws.Cells(rr, 9).Value = rStrat(k) & ": " & rAct(k)
    Next k
    ' таблица сокращается до 13 строк: строки 17–23 освобождаются
    lo.Resize ws.Range(lo.HeaderRowRange.Cells(1, 1), ws.Cells(lo.HeaderRowRange.Row + N, lo.HeaderRowRange.Column + 8))
    ws.Range(ws.Cells(lo.HeaderRowRange.Row + N + 1, 1), ws.Cells(23, 9)).Clear
    ' дополнительные столбцы
    ws.Cells(lo.HeaderRowRange.Row, 10).Value = "Приоритет"
    ws.Cells(lo.HeaderRowRange.Row, 11).Value = "Стратегия"
    For k = 1 To N
        rr = lo.HeaderRowRange.Row + k
        ws.Cells(rr, 10).FormulaR1C1 = "=IF(RC8>=" & Replace(CStr(HIGH_T), ",", ".") & ",""Высокий"",IF(RC8>=" & _
            Replace(CStr(LOW_T), ",", ".") & ",""Средний"",""Низкий""))"
        ws.Cells(rr, 11).Value = rStrat(k)
    Next k
    ' пороги в служебных ячейках M1:M3 — условия форматирования не зависят от языка Excel
    ws.Range("M1").Value = HIGH_T: ws.Range("M2").Value = LOW_T: ws.Range("M3").Value = HIGH_T - 0.0001
    ws.Range("L1").Value = "Пороги:"
    With ws.Range(ws.Cells(lo.HeaderRowRange.Row + 1, 8), ws.Cells(lo.HeaderRowRange.Row + N, 8))
        .FormatConditions.Delete
        Set fc = .FormatConditions.Add(xlCellValue, xlGreaterEqual, "=$M$1")
        fc.Interior.Color = RGB(248, 203, 173)
        Set fc = .FormatConditions.Add(xlCellValue, xlBetween, "=$M$2", "=$M$3")
        fc.Interior.Color = RGB(255, 242, 204)
        Set fc = .FormatConditions.Add(xlCellValue, xlLess, "=$M$2")
        fc.Interior.Color = RGB(226, 239, 217)
    End With
    ws.Range(ws.Cells(lo.HeaderRowRange.Row, 10), ws.Cells(lo.HeaderRowRange.Row + N, 11)).Borders.LineStyle = xlContinuous
    ws.Range(ws.Cells(lo.HeaderRowRange.Row, 10), ws.Cells(lo.HeaderRowRange.Row, 11)).Font.Bold = True
    ws.Columns("J:K").ColumnWidth = 14
End Sub

Private Sub UpdateChart()
    Dim ws As Worksheet, co As ChartObject, s As Series, k As Long, firstRow As Long, lastRow As Long
    Dim src As Worksheet
    Set src = ThisWorkbook.Worksheets("Таблица с рисками")
    firstRow = src.ListObjects(1).HeaderRowRange.Row + 1
    lastRow = firstRow + N - 1
    Set ws = ThisWorkbook.Worksheets("Карта рисков")
    ws.Range("K5:K9").ClearContents
    If ws.ChartObjects.Count = 0 Then
        Set co = ws.ChartObjects.Add(20, 40, 520, 420)
        co.Chart.ChartType = xlXYScatter
        co.Chart.SeriesCollection.NewSeries
    End If
    Set co = ws.ChartObjects(1)
    Set s = co.Chart.SeriesCollection(1)
    s.XValues = src.Range(src.Cells(firstRow, 6), src.Cells(lastRow, 6))
    s.Values = src.Range(src.Cells(firstRow, 7), src.Cells(lastRow, 7))
    s.Name = "Риски"
    s.HasDataLabels = True
    For k = 1 To N
        s.Points(k).DataLabel.Text = "R" & k
    Next k
    With co.Chart
        .HasTitle = True
        .ChartTitle.Text = "Карта рисков для проекта " & PROJECT
        .Axes(xlCategory).MinimumScale = 0: .Axes(xlCategory).MaximumScale = 1
        .Axes(xlValue).MinimumScale = 0: .Axes(xlValue).MaximumScale = 1
        .Axes(xlCategory).HasTitle = True
        .Axes(xlCategory).AxisTitle.Text = "Оценка вероятности возникновения риска"
        .Axes(xlValue).HasTitle = True
        .Axes(xlValue).AxisTitle.Text = "Оценка силы воздействия риска"
    End With
End Sub

Private Sub BuildRanking()
    Dim ws As Worksheet, k As Long, j As Long, idx(1 To N) As Long, t As Long, h(1 To N) As Double
    Set ws = GetSheet("Ранжирование")
    ws.Cells.Clear
    For k = 1 To N: idx(k) = k: h(k) = rP(k) * rI(k): Next k
    For k = 1 To N - 1
        For j = k + 1 To N
            If h(idx(j)) > h(idx(k)) Then t = idx(k): idx(k) = idx(j): idx(j) = t
        Next j
    Next k
    ws.Range("A1").Value = "Ранжирование рисков по H = P x I — " & PROJECT
    ws.Range("A1").Font.Bold = True
    ws.Range("A3:H3").Value = Array("Ранг", "№", "Риск", "P", "I", "H", "Приоритет", "Стратегия")
    For k = 1 To N
        ws.Cells(3 + k, 1).Value = k
        ws.Cells(3 + k, 2).Value = "R" & idx(k)
        ws.Cells(3 + k, 3).Value = rName(idx(k))
        ws.Cells(3 + k, 4).Value = rP(idx(k))
        ws.Cells(3 + k, 5).Value = rI(idx(k))
        ws.Cells(3 + k, 6).FormulaR1C1 = "=RC4*RC5"
        ws.Cells(3 + k, 7).Value = Level(h(idx(k)))
        ws.Cells(3 + k, 8).Value = rStrat(idx(k))
    Next k
    ws.Range("A3:H3").Font.Bold = True
    ws.Range("A3:H" & 3 + N).Borders.LineStyle = xlContinuous
    ws.Cells(5 + N, 3).Value = "Высокий: H >= 0,505; средний: 0,14 <= H < 0,505; низкий: H < 0,14"
    ws.Cells(6 + N, 3).Value = "Высокий — " & Application.WorksheetFunction.CountIf(ws.Range("G4:G" & 3 + N), "Высокий") & _
        ", средний — " & Application.WorksheetFunction.CountIf(ws.Range("G4:G" & 3 + N), "Средний") & _
        ", низкий — " & Application.WorksheetFunction.CountIf(ws.Range("G4:G" & 3 + N), "Низкий")
    ws.Columns("C").ColumnWidth = 70
End Sub

Private Function To5(x As Double) As Long
    To5 = CLng(Int(x * 5 + 0.5 + 0.000001))
    If To5 < 1 Then To5 = 1
    If To5 > 5 Then To5 = 5
End Function

Private Sub BuildHeatMatrix()
    Dim ws As Worksheet, pp As Long, ii As Long, k As Long, txt As String, v As Long
    Set ws = GetSheet("Тепловая матрица")
    ws.Cells.Clear
    ws.Range("A1").Value = "Тепловая матрица 5x5 (приоритет = вероятность x воздействие по шкалам шаблона 1–5)"
    ws.Range("A1").Font.Bold = True
    For pp = 1 To 5
        ws.Cells(9, 2 + pp).Value = pp
        For ii = 1 To 5
            ws.Cells(9 - ii, 2).Value = ii
            v = pp * ii
            txt = CStr(v)
            For k = 1 To N
                If To5(rP(k)) = pp And To5(rI(k)) = ii Then txt = txt & vbLf & "R" & k
            Next k
            With ws.Cells(9 - ii, 2 + pp)
                .Value = txt
                .WrapText = True
                .HorizontalAlignment = xlCenter
                .VerticalAlignment = xlCenter
                If v >= 15 Then
                    .Interior.Color = RGB(248, 105, 107)
                ElseIf v >= 8 Then
                    .Interior.Color = RGB(255, 235, 132)
                Else
                    .Interior.Color = RGB(99, 190, 123)
                End If
            End With
        Next ii
    Next pp
    ws.Range("A4").Value = "Воздействие"
    ws.Range("E10").Value = "Вероятность"
    ws.Range("C4:G8").Borders.LineStyle = xlContinuous
    ws.Rows("4:8").RowHeight = 48
    ws.Columns("C:G").ColumnWidth = 14
End Sub

Public Sub PZ3_RunAll()
    Application.ScreenUpdating = False
    LoadRisks
    FillRiskTable
    Application.Calculate
    UpdateChart
    BuildRanking
    BuildHeatMatrix
    Application.ScreenUpdating = True
    ThisWorkbook.Worksheets("Карта рисков").Activate
    MsgBox "Готово: 13 рисков внесены, карта перестроена, созданы листы «Ранжирование» и «Тепловая матрица»." & vbCrLf & _
        "Максимальный H = 0,56 (R1, высокий приоритет).", vbInformation, "ПЗ3 — NotaCode"
End Sub
