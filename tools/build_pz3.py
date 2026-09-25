import os
import re
import sys
import zipfile
from xml.sax.saxutils import escape

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from report_base import ROOT, Report

XLSX_TEMPLATE = os.path.join(ROOT, 'ПЗ3_Управление-рисками', '02_задание-оригиналы', 'Карта рисков в Excel_с форматированием -26.xlsx')
OUT_DIR = os.path.join(ROOT, 'ПЗ3_Управление-рисками', '07_результаты')
XLSX_OUT = os.path.join(OUT_DIR, 'Карта рисков - NotaCode - Хаджинова.xlsx')
REPORT_OUT = os.path.join(OUT_DIR, 'Отчёт - ПЗ3 - Управление рисками проекта - Хаджинова.docx')
MAP_PNG = os.path.join(OUT_DIR, 'Карта рисков - NotaCode.png')

PROJECT = 'NotaCode — веб-IDE «diagram as code»'
HIGH = 0.505
LOW = 0.14

RISKS = [
    dict(name='Объём распределённой архитектуры (7 сервисов) превышает ресурсы одного исполнителя',
         cat='Планирование', impact='Срыв MVP к 13.12.2026, неполная демонстрация на защите',
         trigger='Velocity ниже плана два спринта подряд', p=0.7, i=0.8, strategy='Снижение',
         action='Walking skeleton в S0, поэтапное подключение сервисов, перенос Could have в Post-MVP',
         boehm='2. Нереалистичные сроки и бюджет'),
    dict(name='Вытеснение продуктовых задач лабораторными работами ч. 2 (8 ЛР, 4 ПЗ)',
         cat='Организационный', impact='Сдвиг спринтов продукта, накопление долга по MVP',
         trigger='Лабораторная работа занимает более одного спринта', p=0.6, i=0.6, strategy='Снижение',
         action='Лабораторная работа реализуется как компонент продукта (Gateway, Web IDE); дорожка Expedite с WIP = 1',
         boehm='6. Непрекращающийся поток изменений'),
    dict(name='Расхождение грамматики DSL и профилей нотаций',
         cat='Технический', impact='Ошибки HTTP 500, ложная валидация, несовместимые синтаксисы',
         trigger='Падение контрактных тестов каталога нотаций', p=0.4, i=0.7, strategy='Уклонение',
         action='Единый каталог нотаций в packages/contracts; генерация подсветки, шаблонов и промптов из каталога',
         boehm='3. Реализация несоответствующей функциональности'),
    dict(name='Хранимая XSS-уязвимость через подписи узлов в SVG',
         cat='Безопасность', impact='Компрометация сессий пользователей, утечка данных',
         trigger='Замечание аудита безопасности, срабатывание CSP', p=0.3, i=0.9, strategy='Уклонение',
         action='Экранирование подписей в модели, санитизация SVG (DOMPurify), политика CSP',
         boehm='8. Недостатки в работах внешних ресурсов'),
    dict(name='Требования 100 % покрытия и отсутствия комментариев замедляют разработку',
         cat='Технический', impact='Рост трудоёмкости задач на 20–30 %',
         trigger='Блокировка слияния конвейером CI более двух дней', p=0.5, i=0.5, strategy='Снижение',
         action='TDD с первого спринта, чистое доменное ядро, моки портов, линтер-правило запрета комментариев',
         boehm='5. «Золотая сервировка», перфекционизм'),
    dict(name='Отказ в согласовании Python-сервисов при рекомендованном стеке Node.js',
         cat='Организационный', impact='Перенос Language и Workspace Service на Node.js, сдвиг MVP на 2–3 спринта',
         trigger='Замечание руководителя при утверждении раздела 2.1 записки', p=0.3, i=0.8, strategy='Снижение',
         action='Обоснование выбора в разделе 2.1, согласование в спринте S1; Gateway на Node.js закрывает требования ЛР1–ЛР8',
         boehm='10. Разрыв в квалификации разных областей'),
    dict(name='Перегрузка или болезнь единственного исполнителя',
         cat='Организационный', impact='Остановка всех работ проекта',
         trigger='Невыполнение цели спринта по причинам вне проекта', p=0.3, i=0.8, strategy='Принятие',
         action='Буферный спринт S12, документация и ADR в репозитории, автоматизация рутинных задач',
         boehm='1. Дефицит специалистов'),
    dict(name='Изменение или отмена бесплатных лимитов LLM API',
         cat='Внешний', impact='AI-ассистент доступен только в режиме заглушки',
         trigger='Ответы HTTP 429, отзыв ключа, закрытие сервиса провайдером', p=0.5, i=0.4, strategy='Снижение',
         action='Адаптеры нескольких провайдеров (Gemini, Groq, OpenRouter, Mistral), заглушка по умолчанию, локальный Ollama',
         boehm='7. Нехватка информации о внешних компонентах'),
    dict(name='Изменение бесплатных тарифов хостинга (Render, Neon, CloudAMQP, Upstash)',
         cat='Внешний', impact='Недоступность демонстрационного стенда на защите',
         trigger='Уведомление провайдера, превышение лимита', p=0.3, i=0.7, strategy='Передача',
         action='Резервный провайдер (Fly.io), локальный стенд docker compose для демонстрации',
         boehm='8. Недостатки в работах внешних ресурсов'),
    dict(name='Время Run превышает 300 мс для диаграммы из 200 узлов',
         cat='Технический', impact='Невыполнение NFR производительности, задержки интерфейса',
         trigger='Результаты нагрузочного теста анализа', p=0.3, i=0.5, strategy='Снижение',
         action='Кэш анализа в Redis по хэшу текста, раскладка elkjs в Web Worker, профилирование парсера',
         boehm='9. Недостаточная производительность'),
    dict(name='Перенос даты защиты на более ранний срок',
         cat='Планирование', impact='Сокращение объёма MVP',
         trigger='Объявление расписания защиты', p=0.3, i=0.6, strategy='Принятие',
         action='Запрос даты у руководителя в спринте S1, приоритизация MoSCoW, перенос Should have в Post-MVP',
         boehm='2. Нереалистичные сроки и бюджет'),
    dict(name='Утечка API-ключей и OAuth-токенов',
         cat='Безопасность', impact='Блокировка ключей, несанкционированные расходы, репутационный ущерб',
         trigger='Срабатывание secret scanning GitHub', p=0.2, i=0.8, strategy='Уклонение',
         action='Секреты только на сервере (env, Vault), шифрование токенов AES-GCM, gitleaks в CI',
         boehm='8. Недостатки в работах внешних ресурсов'),
    dict(name='Нарушение Закона РБ № 99-З при обработке персональных данных',
         cat='Правовой', impact='Штраф, проверка НЦЗПД',
         trigger='Запуск регистрации без политики обработки ПДн', p=0.2, i=0.6, strategy='Уклонение',
         action='Политика обработки ПДн, согласие при регистрации, минимизация состава данных (e-mail, хэш пароля)',
         boehm='—'),
]
N = len(RISKS)
for k, r in enumerate(RISKS, 1):
    r['no'] = k
    r['h'] = round(r['p'] * r['i'], 4)
    r['level'] = 'Высокий' if r['h'] >= HIGH else ('Средний' if r['h'] >= LOW else 'Низкий')
RANKED = sorted(RISKS, key=lambda r: (-r['h'], r['no']))
LAST_ROW = 3 + N


def num(v):
    return f'{v:g}'


def inline_cell(ref, style, text):
    return f'<c r="{ref}" s="{style}" t="inlineStr"><is><t xml:space="preserve">{escape(text)}</t></is></c>'


def number_cell(ref, style, value):
    return f'<c r="{ref}" s="{style}"><v>{num(value)}</v></c>'


def remove_rows(xml, rows):
    for r in rows:
        xml = re.sub(rf'<row r="{r}"[^>]*?(?:/>|>.*?</row>)', '', xml, flags=re.S)
    return xml


def remove_cells(xml, refs):
    for ref in refs:
        xml = re.sub(rf'<c r="{ref}"[^>]*?(?:/>|>.*?</c>)', '', xml, flags=re.S)
    return xml


def styles_of(row_xml):
    return dict(re.findall(r'<c r="([A-I])\d+" s="(\d+)"', row_xml))


def risk_row(xml_row, r):
    row_no = 3 + r['no']
    st = styles_of(xml_row)
    head = re.match(r'<row [^>]*>', xml_row).group()
    cells = [
        number_cell(f'A{row_no}', st['A'], r['no']),
        f'<c r="B{row_no}" s="{st["B"]}" t="str"><f>"R "&amp;Таблица1[[#This Row],[Номер риска]]&amp;" "</f>'
        f'<v xml:space="preserve">R {r["no"]} </v></c>',
        inline_cell(f'C{row_no}', st['C'], r['name']),
        inline_cell(f'D{row_no}', st['D'], r['impact']),
        inline_cell(f'E{row_no}', st['E'], r['trigger']),
        number_cell(f'F{row_no}', st['F'], r['p']),
        number_cell(f'G{row_no}', st['G'], r['i']),
        f'<c r="H{row_no}" s="{st["H"]}"><f>Таблица1[[#This Row],[Оценка вероятности возникновения риска]]*'
        f'Таблица1[[#This Row],[Оценка силы воздействия риска]]</f><v>{num(r["h"])}</v></c>',
        inline_cell(f'I{row_no}', st['I'], f'{r["strategy"]}: {r["action"]}'),
    ]
    return head + ''.join(cells) + '</row>'


def patch_risk_sheet(xml):
    xml = xml.replace('<c r="C1" s="7"/>', inline_cell('C1', '7', PROJECT))
    for r in RISKS:
        row_no = 3 + r['no']
        old = re.search(rf'<row r="{row_no}"[^>]*>.*?</row>', xml, re.S).group()
        xml = xml.replace(old, risk_row(old, r))
    xml = remove_rows(xml, list(range(LAST_ROW + 1, 24)) + list(range(41, 47)) + list(range(53, 69)))
    xml = re.sub(r'<dimension ref="[^"]+"/>', '<dimension ref="A1:K34"/>', xml)
    return xml


def patch_map_sheet(xml):
    xml = remove_cells(xml, ['K5', 'K6', 'K7', 'K8', 'K9', 'Y14', 'X22', 'U23'])
    xml = re.sub(r'(<c r="A1"[^>]*><f>[^<]*</f><v>)[^<]*(</v>)',
                 lambda m: m.group(1) + escape('Карта рисков для проекта ' + PROJECT) + m.group(2), xml)
    return xml


def num_cache(values):
    pts = ''.join(f'<c:pt idx="{k}"><c:v>{num(v)}</c:v></c:pt>' for k, v in enumerate(values))
    return f'<c:numCache><c:formatCode>General</c:formatCode><c:ptCount val="{len(values)}"/>{pts}</c:numCache>'


def patch_chart(xml):
    xml = xml.replace("'Таблица с рисками'!$F$4:$F$23", f"'Таблица с рисками'!$F$4:$F${LAST_ROW}")
    xml = xml.replace("'Таблица с рисками'!$G$4:$G$23", f"'Таблица с рисками'!$G$4:$G${LAST_ROW}")
    caches = re.findall(r'<c:numCache>.*?</c:numCache>', xml, re.S)
    xml = xml.replace(caches[0], num_cache([r['p'] for r in RISKS]), 1)
    xml = xml.replace(caches[1], num_cache([r['i'] for r in RISKS]), 1)
    labels = re.findall(r'<c:dLbl>.*?</c:dLbl>', xml, re.S)
    for lbl in labels:
        idx = int(re.search(r'<c:idx val="(\d+)"/>', lbl).group(1))
        if idx >= N:
            xml = xml.replace(lbl, '', 1)
            continue
        text = f'<a:p><a:r><a:rPr lang="ru-RU"/><a:t>R{idx + 1}</a:t></a:r></a:p>'
        xml = xml.replace(lbl, lbl.replace('<a:p><a:endParaRPr lang="en-US"/></a:p>', text), 1)
    return xml


def build_xlsx():
    src = zipfile.ZipFile(XLSX_TEMPLATE)
    files = {n: src.read(n) for n in src.namelist()}
    files['xl/worksheets/sheet2.xml'] = patch_risk_sheet(files['xl/worksheets/sheet2.xml'].decode()).encode()
    files['xl/worksheets/sheet3.xml'] = patch_map_sheet(files['xl/worksheets/sheet3.xml'].decode()).encode()
    files['xl/charts/chart1.xml'] = patch_chart(files['xl/charts/chart1.xml'].decode()).encode()
    table = files['xl/tables/table1.xml'].decode().replace('ref="A3:I23"', f'ref="A3:I{LAST_ROW}"')
    files['xl/tables/table1.xml'] = table.encode()
    wb = files['xl/workbook.xml'].decode().replace('<calcPr calcId="179021"', '<calcPr calcId="179021" fullCalcOnLoad="1"')
    files['xl/workbook.xml'] = wb.encode()
    files.pop('xl/calcChain.xml', None)
    rels = re.sub(r'<Relationship Id="[^"]+" Type="[^"]+/calcChain" Target="calcChain.xml"/>', '',
                  files['xl/_rels/workbook.xml.rels'].decode())
    files['xl/_rels/workbook.xml.rels'] = rels.encode()
    ct = re.sub(r'<Override PartName="/xl/calcChain.xml"[^>]*/>', '', files['[Content_Types].xml'].decode())
    files['[Content_Types].xml'] = ct.encode()
    with zipfile.ZipFile(XLSX_OUT, 'w', zipfile.ZIP_DEFLATED) as out:
        for name in src.namelist():
            if name in files:
                out.writestr(name, files[name])


def build_map():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    xs = np.linspace(0.001, 1, 400)
    ax.fill_between(xs, 0, 1, color='#e2efd9')
    ax.fill_between(xs, np.clip(LOW / xs, 0, 1), 1, color='#fff2cc')
    ax.fill_between(xs, np.clip(HIGH / xs, 0, 1), 1, color='#f8cbad')
    offsets = {}
    for r in RISKS:
        key = (r['p'], r['i'])
        k = offsets.get(key, 0)
        offsets[key] = k + 1
        ax.scatter(r['p'], r['i'], s=70, color='#1f4e79', zorder=3)
        ax.annotate(f'R{r["no"]}', (r['p'], r['i']), xytext=(7, 5 - 13 * k), textcoords='offset points',
                    fontsize=11, fontweight='bold', color='#1f4e79')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks(np.arange(0, 1.01, 0.1))
    ax.set_yticks(np.arange(0, 1.01, 0.1))
    ax.grid(color='white', linewidth=0.8)
    ax.set_xlabel('Оценка вероятности возникновения риска', fontsize=12)
    ax.set_ylabel('Оценка силы воздействия риска', fontsize=12)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color='#f8cbad', label=f'Высокий приоритет (H ≥ {HIGH})'),
                       Patch(color='#fff2cc', label=f'Средний приоритет ({LOW} ≤ H < {HIGH})'),
                       Patch(color='#e2efd9', label=f'Низкий приоритет (H < {LOW})')],
              loc='upper center', bbox_to_anchor=(0.5, -0.09), ncol=1, fontsize=11, frameon=False)
    fig.tight_layout()
    fig.savefig(MAP_PNG)
    plt.close(fig)


def build_report():
    rep = Report(3, 'Управление рисками проекта')
    rep.heading1('1 Цель работы', new_page=False)
    rep.text(
        'Освоение процессов управления рисками проекта по PMBOK: идентификация рисков, качественная оценка '
        'по вероятности и силе воздействия, построение реестра и карты рисков, выбор стратегий реагирования '
        'на примере программного проекта NotaCode.'
    )

    rep.heading1('2 Ход работы')
    rep.heading2('2.1 Теоретические сведения')
    rep.text(
        'Риск — неопределённое событие или условие, которое при наступлении влияет на цели проекта; '
        'проблема — реализовавшийся риск. Стандарт PMBOK выделяет шесть процессов управления рисками: '
        'планирование управления рисками, идентификация, качественная оценка, количественная оценка, '
        'планирование реагирования, мониторинг и контроль.'
    )
    rep.text(
        'Качественный анализ определяет приоритет риска по двум параметрам — вероятности наступления P '
        'и силе воздействия I на проект. Итоговый коэффициент H = P × I. Шаблон карты рисков задаёт пороги: '
        f'высокий приоритет — H от {HIGH} до 1, средний — от {LOW} до {HIGH}, низкий — менее {LOW}.'
    )
    rep.text(
        'Стратегии реагирования на негативные риски: уклонение (изменение плана, исключающее угрозу), '
        'передача (переложение последствий на третью сторону), снижение (уменьшение вероятности '
        'и/или последствий до приемлемого уровня), принятие (осознанный отказ от изменения плана '
        'с формированием резерва).'
    )

    rep.heading2('2.2 Объект анализа')
    rep.text(
        'Объект анализа — проект NotaCode: веб-IDE класса «diagram as code» для формальных нотаций '
        '(UML, ERD, IDEF0, IDEF1X, IDEF3, DFD). Архитектура — сервисная с событийной интеграцией: Web IDE '
        '(React), Edge Gateway (Node.js, Express), пять Python-сервисов (Workspace, Language, Conversion, AI, '
        'Integration), PostgreSQL, MongoDB, Redis, RabbitMQ. Исполнитель — один; план — 13 недельных '
        'спринтов до защиты курсовой работы (18.12.2026), бюджет — 0 BYN.'
    )

    rep.heading2('2.3 Идентификация рисков')
    rep.text('Для идентификации применены методы:')
    rep.bullets([
        'анализ документации — архитектура (C4, ADR), план спринтов, спецификация требований проекта;',
        'анализ контрольных листов — список 10 наиболее распространённых рисков программного проекта Б. Боэма;',
        'анализ предположений — допущения концепции проекта (ПЗ1, раздел 1.5);',
        'анализ предыдущих версий проекта — зафиксированные дефекты (несовместимые синтаксисы DSL, XSS в SVG, '
        'ключ API в клиентском бандле).',
    ])
    rep.text(f'Реестр идентифицированных рисков приведён в таблице {rep.next_table()}.')
    rep.table(
        'Реестр рисков проекта NotaCode',
        ['№', 'Риск', 'Категория', 'Последствия', 'Триггер'],
        [[f'R{r["no"]}', r['name'], r['cat'], r['impact'], r['trigger']] for r in RISKS],
        [1.2, 5, 2.6, 4.2, 4],
        size=11,
    )
    rep.text(
        f'Соответствие рисков контрольному листу Б. Боэма приведено в таблице {rep.next_table()}.'
    )
    rep.table(
        'Соответствие рисков списку Б. Боэма',
        ['№', 'Риск', 'Пункт списка Б. Боэма'],
        [[f'R{r["no"]}', r['name'], r['boehm']] for r in RISKS],
        [1.2, 9, 6.8],
        size=11,
    )

    rep.heading2('2.4 Качественная оценка рисков')
    rep.text(
        'Вероятность P и сила воздействия I оценены экспертным методом в диапазоне от 0 до 1 по справочным '
        'шкалам шаблона. Данные внесены в структурированную таблицу «Таблица1» листа «Таблица с рисками» '
        '(строки 4–16); столбец H вычисляется формулой =F×G. Результаты оценки, упорядоченные по убыванию '
        f'коэффициента, приведены в таблице {rep.next_table()}.'
    )
    rep.table(
        'Качественная оценка и ранжирование рисков',
        ['Ранг', '№', 'Риск', 'P', 'I', 'H = P × I', 'Приоритет'],
        [[k, f'R{r["no"]}', r['name'], num(r['p']), num(r['i']), num(r['h']), r['level']]
         for k, r in enumerate(RANKED, 1)],
        [1.2, 1.2, 7.4, 1.2, 1.2, 1.8, 2.4],
        size=11,
    )
    counts = {lvl: sum(1 for r in RISKS if r['level'] == lvl) for lvl in ('Высокий', 'Средний', 'Низкий')}
    top = RANKED[0]
    rep.text(
        f'Распределение по приоритетам: высокий — {counts["Высокий"]}, средний — {counts["Средний"]}, '
        f'низкий — {counts["Низкий"]}. Наибольший коэффициент H = {num(top["h"])} имеет риск R{top["no"]} '
        f'«{top["name"]}».'
    )

    rep.heading2('2.5 Карта рисков')
    rep.text(
        'Лист «Карта рисков» содержит точечную диаграмму, построенную по столбцам F (вероятность) и G '
        '(сила воздействия) таблицы рисков; подписи точек R1–R13 соответствуют номерам рисков. Карта рисков '
        f'с зонами приоритета по порогам шаблона приведена на рисунке {rep.next_figure()}.'
    )
    rep.figure(MAP_PNG, 'Карта рисков проекта NotaCode', width_cm=14)

    rep.heading2('2.6 Планирование реагирования на риски')
    rep.text(
        'Анализ выполнен в порядке убывания значимости риска. Выбранные стратегии и мероприятия '
        f'приведены в таблице {rep.next_table()}; мероприятия внесены в столбец I таблицы рисков.'
    )
    rep.table(
        'Стратегии и мероприятия реагирования',
        ['№', 'Стратегия', 'Мероприятия'],
        [[f'R{r["no"]}', r['strategy'], r['action']] for r in RANKED],
        [1.2, 2.6, 13.2],
        size=11,
    )
    strat = {s: sum(1 for r in RISKS if r['strategy'] == s) for s in ('Уклонение', 'Снижение', 'Передача', 'Принятие')}
    rep.text(
        f'Распределение стратегий: снижение — {strat["Снижение"]}, уклонение — {strat["Уклонение"]}, '
        f'передача — {strat["Передача"]}, принятие — {strat["Принятие"]}. Для принятых рисков R7 и R11 '
        'резервом служит буферный спринт S12.'
    )

    rep.heading2('2.7 Мониторинг и контроль рисков')
    rep.text(
        'Реестр рисков пересматривается на каждом Sprint Review: проверяется наступление триггеров, '
        'уточняются оценки P и I, фиксируются новые риски. Метрики потока (velocity, cycle time, WIP) '
        'служат ранними индикаторами для рисков R1, R2 и R5.'
    )

    rep.heading1('Выводы')
    rep.text(
        f'Для проекта NotaCode идентифицировано {N} рисков шести категорий (планирование, организационные, '
        'технические, безопасность, внешние, правовые). Качественная оценка выполнена в шаблоне '
        f'«Карта рисков»: высокий приоритет имеет {counts["Высокий"]} риск, средний — {counts["Средний"]}, '
        f'низкий — {counts["Низкий"]}. Наиболее значимый риск — R{top["no"]} (H = {num(top["h"])}), связанный с объёмом '
        'распределённой архитектуры при одном исполнителе. Для каждого риска определены стратегия '
        'реагирования и мероприятия; преобладает стратегия снижения. Построена карта рисков, '
        'реестр включён в процедуру Sprint Review.'
    )
    rep.save(REPORT_OUT)


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    build_xlsx()
    build_map()
    build_report()
    print('ok', N, [(r['no'], r['h'], r['level']) for r in RANKED])
