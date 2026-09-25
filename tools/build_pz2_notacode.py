"""ПЗ2 для проекта NotaCode: заполненный Excel-планировщик, WBS, сетевой график, Гант и отчёт .docx.

Переиспользует функции build_pz2.py (вариант «Пример 1»), подменяя исходные данные.
1 период планировщика = 1 неделя = 0,25 месяца. Старт — 21.09.2026.
Запуск:  python tools/build_pz2_notacode.py
"""
import datetime as dt
import os
import sys

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pz2 as base
from report_base import ROOT, Report

LAB = os.path.join(ROOT, 'ПЗ2_WBS-и-диаграмма-Ганта')
OUT = os.path.join(LAB, '07_результаты')
base.XLSX_TEMPLATE = os.path.join(LAB, '02_задание-оригиналы', 'Планировщик проекта на основе диаграммы Ганта - 60121.xlsx')
base.XLSX_OUT = os.path.join(OUT, 'Планировщик проекта - NotaCode - Хаджинова.xlsx')
base.WBS_DOT = os.path.join(OUT, 'WBS - NotaCode (планировщик).dot')
base.WBS_PNG = os.path.join(OUT, 'WBS - NotaCode (планировщик).png')
base.NET_DOT = os.path.join(OUT, 'Сетевой график - NotaCode (недели).dot')
base.NET_PNG = os.path.join(OUT, 'Сетевой график - NotaCode (недели).png')
GANTT_PNG = os.path.join(OUT, 'Планировщик проекта - диаграмма Ганта - NotaCode.png')
REPORT_OUT = os.path.join(OUT, 'Отчёт - ПЗ2 - WBS и график Ганта - NotaCode - Хаджинова.docx')
SCHEMES = os.path.join(LAB, '06_схемы')

START = dt.date(2026, 9, 21)
base.PROJECT = 'NotaCode — MVP веб-IDE'
base.PERIOD = 12

base.STAGES = [
    ('1', 'Анализ и проектирование', [1, 2, 3]),
    ('2', 'Фундамент разработки', [4]),
    ('3', 'Серверная часть', [5, 6, 7, 8]),
    ('4', 'Клиентская часть', [9, 10, 11]),
    ('5', 'Интеграции', [12]),
    ('6', 'Тестирование и сдача', [13, 14]),
]
PERT = {1: (0.15, 0.25, 0.35), 2: (0.15, 0.25, 0.35), 3: (0.15, 0.25, 0.35), 4: (0.15, 0.25, 0.35),
        5: (0.5, 0.75, 1.0), 6: (0.25, 0.5, 0.75), 7: (0.25, 0.5, 0.75), 8: (0.15, 0.25, 0.35),
        9: (0.25, 0.5, 0.75), 10: (0.25, 0.5, 0.75), 11: (0.15, 0.25, 0.35), 12: (0.15, 0.25, 0.35),
        13: (0.15, 0.25, 0.35), 14: (0.15, 0.25, 0.35)}


def weeks(tid):
    o, m, p = PERT[tid]
    return round((o + 4 * m + p) / 6 * 4)


base.TASKS = [
    (1, 'Требования (SRS)', [], weeks(1), 'Формализация FR, NFR, UC; эксперт + PERT'),
    (2, 'Архитектура и каталог нотаций', [1], weeks(2), 'C4, ADR, каталог нотаций волны 1'),
    (3, 'Макеты интерфейса IDE', [1], weeks(3), 'Мудборды VS Code / draw.io, макеты'),
    (4, 'Фундамент: CI, Compose, skeleton', [2], weeks(4), 'Монорепо, линтеры, покрытие, walking skeleton'),
    (5, 'Грамматика DSL и парсер', [4], weeks(5), 'Lark, диагностика с номером строки'),
    (6, 'Валидация нотаций', [5], weeks(6), 'Профили UML, ERD, IDEF0/1X/3, DFD'),
    (7, 'Gateway: CRUD, JWT', [4], weeks(7), 'Express, Sequelize, refresh-токены'),
    (8, 'Workspace: история версий', [7], weeks(8), 'Коммиты, SHA-256-блобы, diff'),
    (9, 'Оболочка IDE и Monaco', [3, 4], weeks(9), 'Панели, темы, подсветка, маркеры'),
    (10, 'SVG-холст и кросс-подсветка', [5, 9], weeks(10), 'elkjs, pan/zoom, элемент ↔ строки'),
    (11, 'Сохранение и экспорт', [8, 10], weeks(11), 'Устройство, БД, SVG/PNG'),
    (12, 'AI-ассистент (заглушка)', [7], weeks(12), 'Адаптер LLM, 4 режима'),
    (13, 'E2E, Lighthouse, аудит', [6, 11, 12], weeks(13), 'Сквозные сценарии, ≥ 90, OWASP'),
    (14, 'Демо-стенд и записка', [13], weeks(14), 'Развёртывание, пояснительная записка'),
]
base.FULL_NAMES = {
    1: 'Анализ и формализация требований (SRS: FR, NFR, UC)',
    2: 'Архитектура (C4, ADR) и каталог нотаций волны 1',
    3: 'Мудборды и макеты интерфейса IDE',
    4: 'Монорепозиторий, CI, Docker Compose, walking skeleton',
    5: 'Грамматика DSL и парсер Lark с диагностикой',
    6: 'Профили и валидация нотаций волны 1',
    7: 'Gateway: CRUD проектов, аутентификация JWT',
    8: 'Workspace: коммиты и история версий',
    9: 'Оболочка IDE и интеграция Monaco',
    10: 'SVG-холст, раскладка elkjs, кросс-подсветка',
    11: 'Сохранение и экспорт SVG/PNG',
    12: 'AI-ассистент: заглушка и адаптер LLM',
    13: 'E2E-тестирование, Lighthouse, аудит безопасности',
    14: 'Развёртывание демо-стенда, пояснительная записка',
}

(base.BY_ID, base.SUCC, base.ES, base.EF, base.LS, base.LF, base.TF, base.FINISH) = base.cpm()
base.CRITICAL = [t for t in base.ES if base.TF[t] == 0]
base.DURATION = base.FINISH - 1
ES, EF, LS, LF, TF, SUCC = base.ES, base.EF, base.LS, base.LF, base.TF, base.SUCC


def date_of(period):
    return START + dt.timedelta(weeks=period - 1)


def build_gantt():
    n = len(base.TASKS)
    fig, ax = plt.subplots(figsize=(13, 6.5), dpi=150)
    for w in range(1, base.PERIOD + 1):
        ax.add_patch(Rectangle((w - 1, 0), 1, n, facecolor='#f2f2f2' if w % 2 else '#ffffff',
                               edgecolor='#d9d9d9', linewidth=0.4))
    for i, (tid, name, _, dur, _) in enumerate(base.TASKS):
        y = n - i - 1
        color = '#ed7d31' if TF[tid] == 0 else '#5b9bd5'
        for w in range(ES[tid], ES[tid] + dur):
            ax.add_patch(Rectangle((w - 1, y + 0.15), 1, 0.7, facecolor=color, edgecolor='white', linewidth=0.3))
    ax.set_xlim(0, base.PERIOD)
    ax.set_ylim(0, n)
    ax.set_yticks([n - i - 0.5 for i in range(n)])
    ax.set_yticklabels([f'{t[0]}. {t[1]}' for t in base.TASKS], fontsize=10)
    ax.set_xticks([w - 0.5 for w in range(1, base.PERIOD + 1)])
    ax.set_xticklabels([f'{w}\n{date_of(w):%d.%m}' for w in range(1, base.PERIOD + 1)], fontsize=8)
    ax.xaxis.tick_top()
    ax.tick_params(length=0)
    for side in ax.spines.values():
        side.set_visible(False)
    ax.set_xlabel('Периоды J4:U4 — недели (1 неделя = 0,25 мес.) и даты их начала', fontsize=10)
    ax.legend(handles=[Patch(color='#ed7d31', label='Критический путь (I = 100 %)'),
                       Patch(color='#5b9bd5', label='Работа с резервом (I = 0)')],
              loc='lower center', bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=10, frameon=False)
    fig.tight_layout()
    fig.savefig(GANTT_PNG)
    plt.close(fig)


def fmt_m(w):
    return f'{w / 4:g}'.replace('.', ',')


def build_report():
    rep = Report(2, 'Построение WBS и графика Ганта')
    rep.heading1('1 Цель работы', new_page=False)
    rep.text('Освоение методов календарно-сетевого планирования: построение иерархической структуры работ (WBS), '
             'оценка длительностей методом PERT, определение взаимосвязей, расчёт сроков методом критического пути '
             '(CPM) и построение диаграммы Ганта в Excel-планировщике на примере программного проекта NotaCode.')
    rep.heading1('2 Ход работы')
    rep.heading2('2.1 Теоретические сведения')
    rep.text('WBS — иерархическая декомпозиция проекта на этапы и пакеты работ; работы вне WBS не являются работами '
             'проекта. Длительность по PERT: T = (O + 4M + P) / 6, где O, M, P — оптимистичная, наиболее вероятная '
             'и пессимистичная оценки. Прямой проход: ES = max(EF предшественников), EF = ES + D. Обратный проход: '
             'LF = min(LS последователей), LS = LF – D. Резерв TS = LS – ES; работы с TS = 0 образуют критический путь.')
    rep.heading2('2.2 Объект планирования')
    rep.text('Проект NotaCode — веб-IDE класса «diagram as code» для формальных нотаций (UML, ERD, IDEF0, IDEF1X, '
             'IDEF3, DFD). Цель планирования — MVP (концепция ПЗ1, SMART-цель до 13.12.2026). Старт — 21.09.2026, '
             'исполнитель — один, процесс Scrumban с недельными спринтами. Единица планировщика — неделя (0,25 мес.).')
    rows = []
    for code, name, ids in base.STAGES:
        for tid in ids:
            rows.append([f'{code}.0 {name}', f'{tid}.0', base.FULL_NAMES[tid]])
    rep.text(f'Состав работ приведён в таблице {rep.next_table()}.')
    rep.table('Этапы и работы проекта NotaCode', ['Этап WBS', 'Код', 'Работа'], rows, [4.5, 1.4, 10.8])
    rep.heading2('2.3 Иерархическая структура работ')
    rep.text(f'Уровень 0 — проект, уровень 1 — 6 этапов по жизненному циклу, уровень 2 — 14 работ с кодами 1.0–14.0 '
             f'(рисунок {rep.next_figure()}).')
    rep.figure(os.path.join(SCHEMES, 'WBS - NotaCode (14 работ).png'), 'Иерархическая структура работ проекта NotaCode')
    rep.heading2('2.4 Оценка длительностей по PERT')
    rep.text(f'Оценки O, M, P даны экспертно в месяцах; результат переведён в недели (× 4). Расчёт — '
             f'в таблице {rep.next_table()}.')
    prow = []
    for t in base.TASKS:
        o, m, p = PERT[t[0]]
        c = lambda x: f'{x:g}'.replace('.', ',')
        prow.append([f'{t[0]}.0', t[1], c(o), c(m), c(p), c((o + 4 * m + p) / 6), t[3]])
    rep.table('Оценка длительностей методом PERT', ['Код', 'Работа', 'O', 'M', 'P', 'T, мес.', 'D, нед.'],
              prow, [1.3, 6.4, 1.3, 1.3, 1.3, 1.8, 1.6])
    rep.heading2('2.5 Взаимосвязи работ')
    rep.text(f'Все зависимости — «финиш – старт». Предшественники и последователи — в таблице {rep.next_table()}.')
    rep.table('Взаимосвязи работ', ['Код', 'Работа', 'Непосредственные предшественники', 'Последователи', 'Обоснование'],
              [[f'{t[0]}.0', t[1], ', '.join(f'{p}.0' for p in t[2]) or '—', ', '.join(f'{s}.0' for s in SUCC[t[0]]) or '—',
                t[4]] for t in base.TASKS], [1.3, 4.8, 2.6, 2.4, 5.6])
    rep.text('Операции слияния: 9.0 (3.0, 4.0), 10.0 (5.0, 9.0), 11.0 (8.0, 10.0), 13.0 (6.0, 11.0, 12.0). '
             'Дробящиеся операции: 1.0, 4.0, 5.0, 7.0. Параллельные ветви: сервер (5.0–8.0) и клиент (9.0–11.0).')
    rep.heading2('2.6 Расчёт методом критического пути')
    rep.text(f'Результаты прямого и обратного проходов (в неделях, отсчёт с ES = 1) — в таблице {rep.next_table()}.')
    rep.table('Параметры сетевого графика', ['Код', 'Работа', 'D', 'ES', 'EF', 'LS', 'LF', 'TS', 'Крит.', 'Даты'],
              [[f'{t[0]}.0', t[1], t[3], ES[t[0]], EF[t[0]], LS[t[0]], LF[t[0]], TF[t[0]],
                'ДА' if TF[t[0]] == 0 else 'НЕТ',
                f'{date_of(ES[t[0]]):%d.%m}–{date_of(EF[t[0]]) - dt.timedelta(days=1):%d.%m}'] for t in base.TASKS],
              [1.2, 4.6, 0.9, 1, 1, 1, 1, 1, 1.3, 2.6])
    path = ' → '.join(f'{t}.0' for t in base.CRITICAL)
    rep.text(f'Критический путь: {path}. Длительность проекта: {base.DURATION} недель = {fmt_m(base.DURATION)} мес. '
             f'(21.09.2026–06.12.2026). Резерв до SMART-срока MVP 13.12.2026 — 1 неделя, до защиты 18.12.2026 — '
             f'спринт S12. Наибольший резерв у работы 12.0 (AI-ассистент) — {TF[12]} нед.')
    rep.text(f'Сетевой график (метод предшествования) приведён на рисунке {rep.next_figure()}.')
    rep.figure(base.NET_PNG, 'Сетевой график NotaCode (сверху ES, №, EF; снизу LS, D и резерв, LF); критический путь — красным')
    rep.heading2('2.7 Excel-планировщик и диаграмма Ганта')
    rep.text('Работы внесены в строки 8–21 листа «ТАБЛИЦА ДАННЫХ»: F (ES) = MAX(H предшественников), H (EF) = F + G, '
             'J (LF) = MIN(I последователей), I (LS) = J – G, K (TS) = I – F, L = IF(K=0;"ДА";"НЕТ "). Лист «Планировщик '
             f'проекта» строит полосы условным форматированием; рассматриваемый период — {base.PERIOD} недель '
             f'(рисунок {rep.next_figure()}).')
    rep.figure(GANTT_PNG, 'Диаграмма Ганта NotaCode на листе «Планировщик проекта»; критический путь выделен цветом')
    rep.text(f'Полная диаграмма с резервами и календарными датами приведена на рисунке {rep.next_figure()}.')
    rep.figure(os.path.join(SCHEMES, 'Диаграмма Ганта - NotaCode.png'), 'Диаграмма Ганта NotaCode с резервами времени')
    rep.heading1('Выводы')
    rep.text(f'Для проекта NotaCode построена WBS из 6 этапов и 14 работ, длительности оценены методом PERT, '
             f'определены зависимости «финиш – старт». Критический путь {path} задаёт длительность '
             f'{base.DURATION} недель ({fmt_m(base.DURATION)} мес.): работы завершаются 06.12.2026, что укладывается '
             'в SMART-срок MVP 13.12.2026. Некритические работы 3.0, 6.0–9.0 и 12.0 имеют резервы 1–3 недели. '
             'Excel-планировщик заполнен формулами CPM, диаграмма Ганта выделяет критический путь.')
    rep.save(REPORT_OUT)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    assert base.DURATION == 11 and base.CRITICAL == [1, 2, 4, 5, 10, 11, 13, 14], (base.DURATION, base.CRITICAL)
    base.build_xlsx()
    base.build_wbs()
    base.build_network()
    build_gantt()
    build_report()
    print('ok', base.DURATION, base.CRITICAL)
