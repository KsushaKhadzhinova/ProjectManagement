// Строит в Google Таблице листы «WBS-Гант DiagramCode», «WBS-Гант Пример 1» и «Риски»:
// данные, формулы, раскраску графика Ганта и две диаграммы (полосовой Гант и карта рисков).
// Файл setup_sheets.js генерируется из этого шаблона скриптом generate_tsv.py — не править руками.

var DATA = /*__DATA__*/null;

var COLORS = {
  header: '#1E2761', headerText: '#FFFFFF', subHeader: '#ECEFF7',
  crit: '#E8743B', free: '#5B8DD6', critRow: '#FCE8DC', border: '#C9CFDD', note: '#5B6478',
  high: '#F4C7C3', mid: '#FCE8B2', low: '#D9EAD3'
};

function main(ss) {
  ss = ss || SpreadsheetApp.getActiveSpreadsheet();
  try {
    var leftover = ss.getSheetByName('WBS-Гант');
    if (leftover && leftover.getLastRow() === 0 && !ss.getSheetByName('WBS-Гант DiagramCode')) {
      leftover.setName('WBS-Гант DiagramCode');
    }
  } catch (e) {
    Logger.log('Пустую вкладку WBS-Гант переименовать не удалось: ' + e);
  }
  buildCpm_(ss, 'WBS-Гант DiagramCode', DATA.a, 'DiagramCode, курсовой срез');
  buildCpm_(ss, 'WBS-Гант Пример 1', DATA.b, 'Пример 1 из методички');
  buildRisks_(ss, 'Риски', DATA.r);
  ss.setActiveSheet(ss.getSheetByName('WBS-Гант DiagramCode'));
  SpreadsheetApp.flush();
  return 'OK';
}

function prepareSheet_(ss, name) {
  var sh = ss.getSheetByName(name);
  if (!sh) {
    return ss.insertSheet(name);
  }
  sh.getCharts().forEach(function (c) { sh.removeChart(c); });
  sh.setConditionalFormatRules([]);
  sh.setFrozenRows(0);
  sh.setFrozenColumns(0);
  sh.clear();
  return sh;
}

function ensureSize_(sh, rows, cols) {
  if (sh.getMaxRows() < rows) sh.insertRowsAfter(sh.getMaxRows(), rows - sh.getMaxRows());
  if (sh.getMaxColumns() < cols) sh.insertColumnsAfter(sh.getMaxColumns(), cols - sh.getMaxColumns());
}

function countLeadingRows_(rows) {
  var n = 0;
  for (var i = 1; i < rows.length; i++) {
    if (rows[i][0] === '') break;
    n++;
  }
  return n;
}

function buildCpm_(ss, name, rows, title) {
  var sh = prepareSheet_(ss, name);
  var width = rows[0].length;
  var nTasks = countLeadingRows_(rows);
  var days = width - 11;
  var lastTaskRow = nTasks + 1;
  ensureSize_(sh, 80, width);

  sh.getRange(1, 1, lastTaskRow, width).setValues(rows.slice(0, lastTaskRow));

  var r = lastTaskRow + 2;
  for (var k = lastTaskRow + 1; k < rows.length; k++) {
    if (rows[k][0] === '') continue;
    sh.getRange(r, 2).setValue(rows[k][0]).setFontWeight('bold');
    sh.getRange(r, 3).setValue(rows[k][1]).setFontWeight('bold').setFontColor(COLORS.crit);
    r++;
  }

  sh.getRange(1, 1, 1, 10).setFontWeight('bold').setBackground(COLORS.header)
    .setFontColor(COLORS.headerText).setWrap(true).setVerticalAlignment('middle');
  sh.getRange(1, 12, 1, days).setFontWeight('bold').setHorizontalAlignment('center')
    .setFontSize(8).setBackground(COLORS.subHeader);
  sh.setFrozenRows(1);
  sh.setColumnWidth(1, 36);
  sh.setColumnWidth(2, 320);
  sh.setColumnWidth(3, 120);
  sh.setColumnWidths(4, 7, 72);
  sh.setColumnWidth(11, 16);
  sh.setColumnWidths(12, days, 22);
  sh.getRange(2, 1, nTasks, 1).setHorizontalAlignment('center');
  sh.getRange(2, 3, nTasks, 8).setHorizontalAlignment('center');
  sh.getRange(1, 1, lastTaskRow, 10)
    .setBorder(true, true, true, true, true, true, COLORS.border, SpreadsheetApp.BorderStyle.SOLID);

  var gantt = sh.getRange(2, 12, nTasks, days);
  gantt.setHorizontalAlignment('center').setFontSize(8);
  sh.setConditionalFormatRules([
    SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('█')
      .setBackground(COLORS.crit).setFontColor(COLORS.crit).setRanges([gantt]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('░')
      .setBackground(COLORS.free).setFontColor(COLORS.free).setRanges([gantt]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenFormulaSatisfied('=$J2="ДА"')
      .setBackground(COLORS.critRow).setRanges([sh.getRange(2, 1, nTasks, 10)]).build()
  ]);

  var noteRow = r + 1;
  sh.getRange(noteRow, 2).setValue('Данные для полосовой диаграммы Ганта — формулы, берутся из таблицы выше')
    .setFontStyle('italic').setFontColor(COLORS.note);
  var hdr = noteRow + 1;
  sh.getRange(hdr, 2, 1, 4).setValues([['Работа', 'Смещение (ES − 1)', 'Критический путь', 'Есть резерв']])
    .setFontWeight('bold').setBackground(COLORS.subHeader);
  var helper = [];
  for (var t = 0; t < nTasks; t++) {
    var src = t + 2;
    helper.push([
      '=A' + src + '&". "&B' + src,
      '=E' + src + '-1',
      '=IF(J' + src + '="ДА",D' + src + ',0)',
      '=IF(J' + src + '="ДА",0,D' + src + ')'
    ]);
  }
  sh.getRange(hdr + 1, 2, nTasks, 4).setValues(helper);

  var chart = sh.newChart()
    .setChartType(Charts.ChartType.BAR)
    .addRange(sh.getRange(hdr, 2, nTasks + 1, 4))
    .setNumHeaders(1)
    .setOption('isStacked', true)
    .setOption('title', 'Диаграмма Ганта — ' + title + ': ' + days + ' рабочих дней')
    .setOption('legend', { position: 'bottom' })
    .setOption('series', {
      0: { color: '#FFFFFF', visibleInLegend: false },
      1: { color: COLORS.crit },
      2: { color: COLORS.free }
    })
    .setOption('hAxis', { title: 'Рабочие дни', viewWindow: { min: 0, max: days } })
    .setOption('width', 980)
    .setOption('height', 80 + nTasks * 34)
    .setPosition(hdr + nTasks + 2, 2, 0, 0)
    .build();
  sh.insertChart(chart);
}

function buildRisks_(ss, name, rows) {
  var sh = prepareSheet_(ss, name);
  var width = rows[0].length;
  var n = countLeadingRows_(rows);
  var hc = width + 2;
  ensureSize_(sh, 80, hc + n);

  sh.getRange(1, 1, n + 1, width).setValues(rows.slice(0, n + 1));
  sh.getRange(n + 3, 1).setValue(rows[rows.length - 1][0]).setFontStyle('italic').setFontColor(COLORS.note);

  sh.getRange(1, 1, 1, width).setFontWeight('bold').setBackground(COLORS.header)
    .setFontColor(COLORS.headerText).setWrap(true).setVerticalAlignment('middle');
  sh.setFrozenRows(1);
  [36, 90, 300, 280, 280, 100, 100, 110, 100, 80, 320].forEach(function (w, i) {
    sh.setColumnWidth(i + 1, w);
  });
  sh.getRange(2, 1, n, width).setWrap(true).setVerticalAlignment('top');
  sh.getRange(2, 6, n, 3).setNumberFormat('0.00').setHorizontalAlignment('center');
  sh.getRange(2, 1, n, 2).setHorizontalAlignment('center');
  sh.getRange(2, 9, n, 2).setHorizontalAlignment('center');
  sh.getRange(1, 1, n + 1, width)
    .setBorder(true, true, true, true, true, true, COLORS.border, SpreadsheetApp.BorderStyle.SOLID);

  var prio = sh.getRange(2, 9, n, 1);
  sh.setConditionalFormatRules([
    SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('Высокий').setBackground(COLORS.high).setRanges([prio]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('Средний').setBackground(COLORS.mid).setRanges([prio]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('Низкий').setBackground(COLORS.low).setRanges([prio]).build()
  ]);

  var helper = [['Вероятность (F)']];
  for (var j = 0; j < n; j++) helper[0].push('R' + rows[j + 1][0]);
  for (var i = 0; i < n; i++) {
    var rr = i + 2;
    var line = ['=F' + rr];
    for (var s = 0; s < n; s++) line.push(s === i ? '=G' + rr : '');
    helper.push(line);
  }
  sh.getRange(1, hc, n + 1, n + 1).setValues(helper);
  sh.getRange(1, hc, 1, n + 1).setFontWeight('bold').setBackground(COLORS.subHeader);
  sh.getRange(n + 3, hc).setValue('Данные для карты рисков: каждый риск — отдельная серия, чтобы у точки была своя подпись в легенде')
    .setFontStyle('italic').setFontColor(COLORS.note);

  var chart = sh.newChart()
    .setChartType(Charts.ChartType.SCATTER)
    .addRange(sh.getRange(1, hc, n + 1, n + 1))
    .setNumHeaders(1)
    .setOption('title', 'Карта рисков DiagramCode: вероятность × сила воздействия')
    .setOption('hAxis', { title: 'Вероятность возникновения (F)', viewWindow: { min: 0, max: 1 } })
    .setOption('vAxis', { title: 'Сила воздействия (G)', viewWindow: { min: 0, max: 1 } })
    .setOption('pointSize', 12)
    .setOption('legend', { position: 'right' })
    .setOption('width', 760)
    .setOption('height', 520)
    .setPosition(n + 5, 3, 0, 0)
    .build();
  sh.insertChart(chart);
}
