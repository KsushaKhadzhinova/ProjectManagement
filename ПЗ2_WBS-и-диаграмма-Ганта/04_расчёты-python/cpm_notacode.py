"""ПЗ2. Расчёт PERT и метода критического пути (CPM) для проекта NotaCode.

Запуск:  python cpm_notacode.py
Результат: таблицы в ../07_результаты/Расчёт CPM - NotaCode.md и .csv,
           рисунки в ../06_схемы/ (WBS, сетевой график PDM, диаграмма Ганта).
Дополнительно проверяются учебные примеры методички (Пример 1, Пример 2, «Бизнес-центр»).
"""
import csv
import datetime as dt
import os
import subprocess

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMES = os.path.join(HERE, '..', '06_схемы')
RESULTS = os.path.join(HERE, '..', '07_результаты')

PROJECT = 'NotaCode — MVP веб-IDE «diagram as code»'
START = dt.date(2026, 9, 21)
WEEKS_PER_MONTH = 4

WBS_GROUPS = [
    ('A', 'Анализ и проектирование', ['1.0', '2.0', '3.0']),
    ('B', 'Фундамент разработки', ['4.0']),
    ('C', 'Серверная часть', ['5.0', '6.0', '7.0', '8.0']),
    ('D', 'Клиентская часть', ['9.0', '10.0', '11.0']),
    ('E', 'Интеграции', ['12.0']),
    ('F', 'Тестирование и сдача', ['13.0', '14.0']),
]

TASKS = [
    ('1.0', 'Анализ и формализация требований (SRS: FR, NFR, UC)', 0.15, 0.25, 0.35, []),
    ('2.0', 'Архитектура (C4, ADR) и каталог нотаций волны 1', 0.15, 0.25, 0.35, ['1.0']),
    ('3.0', 'Мудборды и макеты интерфейса IDE', 0.15, 0.25, 0.35, ['1.0']),
    ('4.0', 'Монорепозиторий, CI, Docker Compose, walking skeleton', 0.15, 0.25, 0.35, ['2.0']),
    ('5.0', 'Грамматика DSL и парсер Lark с диагностикой', 0.50, 0.75, 1.00, ['4.0']),
    ('6.0', 'Профили и валидация нотаций волны 1', 0.25, 0.50, 0.75, ['5.0']),
    ('7.0', 'Gateway: CRUD проектов, аутентификация JWT', 0.25, 0.50, 0.75, ['4.0']),
    ('8.0', 'Workspace: коммиты и история версий', 0.15, 0.25, 0.35, ['7.0']),
    ('9.0', 'Оболочка IDE и интеграция Monaco', 0.25, 0.50, 0.75, ['3.0', '4.0']),
    ('10.0', 'SVG-холст, раскладка elkjs, кросс-подсветка', 0.25, 0.50, 0.75, ['5.0', '9.0']),
    ('11.0', 'Сохранение и экспорт SVG/PNG', 0.15, 0.25, 0.35, ['8.0', '10.0']),
    ('12.0', 'AI-ассистент: заглушка и адаптер LLM', 0.15, 0.25, 0.35, ['7.0']),
    ('13.0', 'E2E-тестирование, Lighthouse, аудит безопасности', 0.15, 0.25, 0.35, ['6.0', '11.0', '12.0']),
    ('14.0', 'Развёртывание демо-стенда, пояснительная записка', 0.15, 0.25, 0.35, ['13.0']),
]


def pert(o, m, p):
    return (o + 4 * m + p) / 6


def sigma(o, p):
    return (p - o) / 6


def cpm(tasks):
    """tasks: list of (id, name, duration, preds). Возвращает dict id -> параметры."""
    res = {t[0]: dict(id=t[0], name=t[1], d=t[2], preds=list(t[3]), succ=[]) for t in tasks}
    order = [t[0] for t in tasks]
    for tid in order:
        for p in res[tid]['preds']:
            res[p]['succ'].append(tid)
    for tid in order:
        r = res[tid]
        r['es'] = max((res[p]['ef'] for p in r['preds']), default=0)
        r['ef'] = r['es'] + r['d']
    finish = max(r['ef'] for r in res.values())
    for tid in reversed(order):
        r = res[tid]
        r['lf'] = min((res[s]['ls'] for s in r['succ']), default=finish)
        r['ls'] = r['lf'] - r['d']
        r['ts'] = round(r['ls'] - r['es'], 6)
        r['crit'] = abs(r['ts']) < 1e-9
    return res, finish


def critical_path(res, order):
    path, cur = [], None
    starts = [t for t in order if res[t]['crit'] and not res[t]['preds']]
    cur = starts[0]
    while cur:
        path.append(cur)
        nxt = [s for s in res[cur]['succ'] if res[s]['crit'] and abs(res[s]['es'] - res[cur]['ef']) < 1e-9]
        cur = nxt[0] if nxt else None
    return path


def to_date(months):
    return START + dt.timedelta(weeks=months * WEEKS_PER_MONTH)


def fmt(x):
    return f'{x:g}'.replace('.', ',')


def build_wbs_png():
    lines = ['digraph WBS {',
             '  graph [rankdir=TB, splines=ortho, nodesep=0.2, ranksep=0.45, fontname="Arial"];',
             '  node [shape=box, style="rounded,filled", fontname="Arial", fontsize=10];',
             '  edge [arrowhead=none];',
             f'  root [label="0 {PROJECT}", fillcolor="#d9e2f3", fontsize=12];']
    names = {t[0]: t[1] for t in TASKS}
    for gid, gname, items in WBS_GROUPS:
        lines.append(f'  g{gid} [label="{gname}", fillcolor="#e2efd9"];')
        lines.append(f'  root -> g{gid};')
        prev = f'g{gid}'
        for code in items:
            nid = 't' + code.replace('.', '_')
            words, row, rows = names[code].split(), '', []
            for w in words:
                if len(row) + len(w) > 24:
                    rows.append(row.strip())
                    row = ''
                row += w + ' '
            rows.append(row.strip())
            label = code + '\\n' + '\\n'.join(rows)
            lines.append(f'  {nid} [label="{label}", fillcolor="#fff2cc", fontsize=9];')
            lines.append(f'  {prev} -> {nid};')
            prev = nid
    lines.append('}')
    dot = os.path.join(SCHEMES, 'WBS - NotaCode (14 работ).dot')
    with open(dot, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    subprocess.run(['dot', '-Tpng', '-Gdpi=150', dot, '-o', dot[:-4] + '.png'], check=True)


def build_network_png(res, order):
    lines = ['digraph PDM {',
             '  graph [rankdir=LR, nodesep=0.35, ranksep=0.55, fontname="Arial"];',
             '  node [shape=plaintext, fontname="Arial", fontsize=9];',
             '  edge [color="#555555"];',
             '  start [shape=circle, label="Старт", style=filled, fillcolor="#d9e2f3"];',
             '  finish [shape=doublecircle, label="Финиш", style=filled, fillcolor="#d9e2f3"];']
    for tid in order:
        r = res[tid]
        color = '#f8cbad' if r['crit'] else '#ffffff'
        short = r['name'] if len(r['name']) <= 28 else r['name'][:27] + '…'
        label = (f'<<table border="1" cellborder="1" cellspacing="0" bgcolor="{color}">'
                 f'<tr><td>{fmt(r["es"])}</td><td><b>{tid}</b></td><td>{fmt(r["ef"])}</td></tr>'
                 f'<tr><td>TS {fmt(r["ts"])}</td><td colspan="2">{short}</td></tr>'
                 f'<tr><td>{fmt(r["ls"])}</td><td>D={fmt(r["d"])}</td><td>{fmt(r["lf"])}</td></tr></table>>')
        lines.append(f'  n{tid.replace(".", "_")} [label={label}];')
    for tid in order:
        r = res[tid]
        a = 'n' + tid.replace('.', '_')
        if not r['preds']:
            lines.append(f'  start -> {a} [color="#c00000", penwidth=2];')
        for s in r['succ']:
            crit = r['crit'] and res[s]['crit'] and abs(res[s]['es'] - r['ef']) < 1e-9
            style = ' [color="#c00000", penwidth=2]' if crit else ''
            lines.append(f'  {a} -> n{s.replace(".", "_")}{style};')
        if not r['succ']:
            lines.append(f'  {a} -> finish [color="#c00000", penwidth=2];')
    lines.append('}')
    dot = os.path.join(SCHEMES, 'Сетевой график PDM - NotaCode.dot')
    with open(dot, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    subprocess.run(['dot', '-Tpng', '-Gdpi=150', dot, '-o', dot[:-4] + '.png'], check=True)


def build_gantt_png(res, order, finish):
    fig, ax = plt.subplots(figsize=(14, 7.5), dpi=150)
    for k, tid in enumerate(order):
        r = res[tid]
        y = len(order) - 1 - k
        ax.barh(y, r['d'], left=r['es'], color='#c00000' if r['crit'] else '#5b9bd5', edgecolor='black', height=0.6)
        if r['ts'] > 0:
            ax.barh(y, r['ts'], left=r['ef'], color='none', edgecolor='#7f7f7f', hatch='///', height=0.6)
        ax.text(r['ef'] + 0.02, y, f'{fmt(r["d"])} мес.', va='center', fontsize=8)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([f'{t}  {res[t]["name"]}' for t in reversed(order)], fontsize=8.5)
    ticks = [x / 4 for x in range(0, int(finish * 4) + 2)]
    ax.set_xticks(ticks)
    ax.set_xticklabels([f'{fmt(t)}\n{to_date(t):%d.%m}' for t in ticks], fontsize=8)
    ax.set_xlim(0, finish + 0.35)
    ax.grid(axis='x', linestyle=':', color='#999999')
    ax.set_xlabel('Время от старта, мес. (1 мес. = 4 недели = 4 спринта) / дата начала недели')
    ax.set_title(f'Диаграмма Ганта — {PROJECT}\nСтарт {START:%d.%m.%Y}, длительность {fmt(finish)} мес., '
                 f'окончание работ {to_date(finish) - dt.timedelta(days=1):%d.%m.%Y}', fontsize=11)
    ax.legend(handles=[Patch(color='#c00000', label='Критическая работа (TS = 0)'),
                       Patch(color='#5b9bd5', label='Некритическая работа'),
                       Patch(facecolor='none', edgecolor='#7f7f7f', hatch='///', label='Резерв времени TS')],
              loc='lower left', fontsize=8.5)
    fig.tight_layout()
    fig.savefig(os.path.join(SCHEMES, 'Диаграмма Ганта - NotaCode.png'))
    plt.close(fig)


def write_tables(res, order, finish, path):
    md = os.path.join(RESULTS, 'Расчёт CPM - NotaCode.md')
    with open(md, 'w', encoding='utf-8') as f:
        f.write(f'# Расчёт PERT и CPM — {PROJECT}\n\n')
        f.write('Сгенерировано скриптом `04_расчёты-python/cpm_notacode.py`.\n\n')
        f.write('## 1. Оценка длительностей по PERT, мес.\n\n')
        f.write('| Код | Работа | O | M | P | T = (O+4M+P)/6 | σ = (P−O)/6 |\n|---|---|---|---|---|---|---|\n')
        for t in TASKS:
            f.write(f'| {t[0]} | {t[1]} | {fmt(t[2])} | {fmt(t[3])} | {fmt(t[4])} | '
                    f'{fmt(round(pert(t[2], t[3], t[4]), 4))} | {fmt(round(sigma(t[2], t[4]), 4))} |\n')
        f.write('\n## 2. Прямой и обратный проход, мес.\n\n')
        f.write('| Код | Работа | Предш. | Послед. | D | ES | EF | LS | LF | TS | Крит. | Начало | Окончание |\n')
        f.write('|---|---|---|---|---|---|---|---|---|---|---|---|---|\n')
        for tid in order:
            r = res[tid]
            f.write(f'| {tid} | {r["name"]} | {", ".join(r["preds"]) or "—"} | {", ".join(r["succ"]) or "—"} | '
                    f'{fmt(r["d"])} | {fmt(r["es"])} | {fmt(r["ef"])} | {fmt(r["ls"])} | {fmt(r["lf"])} | '
                    f'{fmt(r["ts"])} | {"ДА" if r["crit"] else "нет"} | {to_date(r["es"]):%d.%m.%Y} | '
                    f'{to_date(r["ef"]) - dt.timedelta(days=1):%d.%m.%Y} |\n')
        var = sum(sigma(t[2], t[4]) ** 2 for t in TASKS if t[0] in path)
        f.write(f'\n**Длительность проекта:** {fmt(finish)} мес. ({int(finish * WEEKS_PER_MONTH)} недель).  \n')
        f.write(f'**Критический путь:** {" → ".join(path)}.  \n')
        f.write(f'**σ критического пути:** √{fmt(round(var, 4))} = {fmt(round(var ** 0.5, 3))} мес.; '
                f'с вероятностью ≈ 95 % (T + 2σ) проект завершится за '
                f'{fmt(round(finish + 2 * var ** 0.5, 2))} мес.\n')
    with open(os.path.join(RESULTS, 'Расчёт CPM - NotaCode.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['Код', 'Работа', 'Предшественники', 'Последователи', 'D', 'ES', 'EF', 'LS', 'LF', 'TS', 'Критическая'])
        for tid in order:
            r = res[tid]
            w.writerow([tid, r['name'], ', '.join(r['preds']), ', '.join(r['succ']),
                        fmt(r['d']), fmt(r['es']), fmt(r['ef']), fmt(r['ls']), fmt(r['lf']), fmt(r['ts']),
                        'ДА' if r['crit'] else 'НЕТ'])


def verify_textbook():
    ex1 = [('1', '', 3, []), ('2', '', 5, ['1']), ('3', '', 4, ['2']), ('4', '', 6, ['1']), ('5', '', 3, ['4']),
           ('6', '', 3, ['3', '4']), ('7', '', 8, ['6']), ('8', '', 10, ['6']), ('9', '', 2, ['7', '8']),
           ('10', '', 20, ['9']), ('11', '', 4, ['10']), ('12', '', 5, ['11'])]
    ex2 = [('1', '', 2, []), ('2', '', 1.5, ['1']), ('3', '', 2, ['1']), ('4', '', 1.5, ['1']), ('5', '', 4, ['3', '4']),
           ('6', '', 4, ['3', '5']), ('7', '', 2, ['5']), ('8', '', 2, ['6']), ('9', '', 5, ['1']),
           ('10', '', 3, ['6', '9']), ('11', '', 2, ['5', '6', '7', '10']), ('12', '', 1, ['11'])]
    bc = [('A', '', 5, []), ('B', '', 15, ['A']), ('C', '', 10, ['A']), ('D', '', 5, ['A']), ('E', '', 15, ['B', 'C']),
          ('F', '', 10, ['B', 'C', 'D']), ('G', '', 170, ['F']), ('H', '', 35, ['E', 'G'])]
    out = []
    for name, data, expected in [('Пример 1 (дни)', ex1, 56), ('Пример 2 (мес.)', ex2, 18), ('Бизнес-центр (дни)', bc, 235)]:
        res, fin = cpm(data)
        path = critical_path(res, [t[0] for t in data])
        assert abs(fin - expected) < 1e-9, (name, fin)
        out.append(f'{name}: длительность {fmt(fin)}, критический путь {" → ".join(path)} — совпадает с методичкой')
    return out


def main():
    os.makedirs(SCHEMES, exist_ok=True)
    os.makedirs(RESULTS, exist_ok=True)
    data = [(t[0], t[1], round(pert(t[2], t[3], t[4]), 4), t[5]) for t in TASKS]
    res, finish = cpm(data)
    order = [t[0] for t in TASKS]
    path = critical_path(res, order)
    build_wbs_png()
    build_network_png(res, order)
    build_gantt_png(res, order, finish)
    write_tables(res, order, finish, path)
    print('Длительность:', fmt(finish), 'мес.; критический путь:', ' → '.join(path))
    for line in verify_textbook():
        print(line)


if __name__ == '__main__':
    main()
