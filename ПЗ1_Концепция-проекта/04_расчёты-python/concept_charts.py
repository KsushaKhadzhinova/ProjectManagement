"""ПЗ1. Расчёты и схемы для концепции проекта NotaCode.

Запуск:  python concept_charts.py
Результат (../06_схемы/):
  - Матрица стейкхолдеров - NotaCode.png  (влияние × интерес, квадранты A–D шаблона)
  - MoSCoW - NotaCode.png                (распределение требований, проверка правила Must ≤ 60 %)
  - WBS декомпозиции цели - NotaCode.png (6 этапов, 20 задач — раздел 4 шаблона)
Данные совпадают с tools/build_pz1_notacode.py (заполненный шаблон .docx).
"""
import os
import subprocess

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '06_схемы')

STAKEHOLDERS = [
    ('Автор проекта (PO, разработчик)', 5, 5),
    ('Руководитель курсовой (ИТиВП)', 5, 3),
    ('Преподаватель «Управление проектами»', 4, 2),
    ('Конечные пользователи', 2, 5),
    ('AI-агенты разработки', 3, 1),
    ('Поставщики сервисов (LLM, хостинг)', 3, 1),
]

MOSCOW = {'Must have': 8, 'Should have': 6, 'Could have': 5, "Won't have": 4}

WBS = [
    ('1.0', 'Анализ и проектирование', ['1.1 SRS (FR, NFR, UC)', '1.2 Каталог нотаций', '1.3 Архитектура (C4, ADR)',
                                        '1.4 Мудборды интерфейса']),
    ('2.0', 'Фундамент разработки', ['2.1 Монорепо и CI', '2.2 Docker Compose', '2.3 Walking skeleton']),
    ('3.0', 'Серверная часть', ['3.1 CRUD в Gateway', '3.2 JWT, refresh', '3.3 Грамматика DSL (Lark)',
                                '3.4 Валидация нотаций', '3.5 История версий']),
    ('4.0', 'Клиентская часть', ['4.1 Оболочка IDE', '4.2 Monaco', '4.3 SVG-холст (elkjs)', '4.4 Сохранение, экспорт']),
    ('5.0', 'Интеграции', ['5.1 AI-заглушка', '5.2 4 режима AI', '5.3 GitHub, Google Drive']),
    ('6.0', 'Тестирование и сдача', ['6.1 E2E-тесты', '6.2 Lighthouse, аудит', '6.3 Записка и защита']),
]


def quadrant(influence, interest):
    if influence >= 4:
        return 'A' if interest >= 3 else 'D'
    return 'B' if interest >= 3 else 'C'


def stakeholder_matrix():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    ax.axhspan(3.5, 5.5, xmin=0, xmax=0.4, color='#fff2cc')
    ax.axhspan(3.5, 5.5, xmin=0.4, xmax=1, color='#f8cbad')
    ax.axhspan(0.5, 3.5, xmin=0, xmax=0.4, color='#e2efd9')
    ax.axhspan(0.5, 3.5, xmin=0.4, xmax=1, color='#ddebf7')
    labels = {
        (1.5, 5.3): 'D: минимальное информирование',
        (4.2, 5.3): 'A: активное вовлечение',
        (1.5, 0.7): 'C: минимальный контроль',
        (4.2, 0.7): 'B: консультирование',
    }
    for (x, y), t in labels.items():
        ax.text(x, y, t, ha='center', fontsize=11, fontweight='bold', color='#404040')
    seen = {}
    for name, infl, inter in STAKEHOLDERS:
        k = seen.get((infl, inter), 0)
        seen[(infl, inter)] = k + 1
        ax.scatter(inter, infl, s=120, color='#1f4e79', zorder=3)
        right = inter >= 4.5
        ax.annotate(f'{name} ({infl}/{inter}) → {quadrant(infl, inter)}', (inter, infl),
                    xytext=(-10 if right else 8, -16 - 14 * k if right else 6 - 14 * k), textcoords='offset points',
                    fontsize=9, ha='right' if right else 'left')
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)
    ax.axvline(2.5, color='gray', lw=1)
    ax.axhline(3.5, color='gray', lw=1)
    ax.set_xlabel('Заинтересованность (интерес), 1–5 — низкий 1–2 | высокий 3–5', fontsize=11)
    ax.set_ylabel('Влияние, 1–5 — низкое 1–3 | высокое 4–5', fontsize=11)
    ax.set_title('Матрица стейкхолдеров проекта NotaCode (влияние × интерес)', fontsize=13)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'Матрица стейкхолдеров - NotaCode.png'))
    plt.close(fig)


def moscow_chart():
    total = sum(MOSCOW.values())
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=150)
    colors = ['#c00000', '#ed7d31', '#ffc000', '#a5a5a5']
    bars = ax.bar(list(MOSCOW), list(MOSCOW.values()), color=colors, edgecolor='black')
    for b, v in zip(bars, MOSCOW.values()):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.15, f'{v} ({100 * v / total:.0f} %)', ha='center', fontsize=11)
    must = 100 * MOSCOW['Must have'] / total
    ax.axhline(0.6 * total, color='#c00000', ls='--', lw=1)
    ax.text(3.45, 0.6 * total + 0.2, 'предел Must = 60 %', ha='right', color='#c00000', fontsize=9)
    ax.set_ylim(0, 0.6 * total + 2)
    ax.set_ylabel('Количество требований')
    ax.set_title(f'MoSCoW-приоритизация NotaCode: всего {total}, Must = {must:.0f} % ≤ 60 % — правило выполнено')
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'MoSCoW - NotaCode.png'))
    plt.close(fig)
    return total, must


def wbs_tree():
    lines = ['digraph W {', '  graph [rankdir=TB, splines=ortho, nodesep=0.15, ranksep=0.4];',
             '  node [shape=box, style="rounded,filled", fontname="Arial", fontsize=10];', '  edge [arrowhead=none];',
             '  root [label="0 NotaCode — MVP\\n(SMART-цель до 13.12.2026)", fillcolor="#d9e2f3", fontsize=12];']
    for code, name, tasks in WBS:
        s = 's' + code[0]
        lines += [f'  {s} [label="{code}\\n{name}", fillcolor="#e2efd9"];', f'  root -> {s};']
        prev = s
        for k, t in enumerate(tasks):
            n = f'{s}_{k}'
            lines += [f'  {n} [label="{t}", fillcolor="#fff2cc", fontsize=9];', f'  {prev} -> {n};']
            prev = n
    lines.append('}')
    dot = os.path.join(OUT, 'WBS декомпозиции цели - NotaCode.dot')
    with open(dot, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    subprocess.run(['dot', '-Tpng', '-Gdpi=150', dot, '-o', dot[:-4] + '.png'], check=True)
    return sum(len(t) for _, _, t in WBS)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    stakeholder_matrix()
    total, must = moscow_chart()
    tasks = wbs_tree()
    print(f'MoSCoW: {total} требований, Must = {must:.1f} % (≤ 60 %: {must <= 60})')
    print(f'WBS: {len(WBS)} этапов, {tasks} задач (норма шаблона 15–25: {15 <= tasks <= 25})')
    for n, i, s in STAKEHOLDERS:
        print(f'{n}: влияние {i}, интерес {s} → квадрант {quadrant(i, s)}')
