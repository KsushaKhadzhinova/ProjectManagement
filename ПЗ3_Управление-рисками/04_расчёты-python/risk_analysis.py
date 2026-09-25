"""ПЗ3. Качественный и количественный анализ рисков проекта NotaCode.

Запуск:  python risk_analysis.py
Результат:
  ../07_результаты/Реестр рисков - NotaCode.md и .csv — реестр, H = P × I, приоритет, стратегия, ранжирование
  ../06_схемы/Карта рисков (зоны) - NotaCode.png      — точечная карта с зонами порогов 0,14 / 0,505
  ../06_схемы/Тепловая матрица 5x5 - NotaCode.png      — матрица «вероятность × воздействие» по шкалам 1–5
  ../06_схемы/Ранжирование рисков - NotaCode.png       — H по убыванию (диаграмма Парето)
  ../06_схемы/Стратегии реагирования - NotaCode.png    — распределение стратегий
  ../06_схемы/Монте-Карло - NotaCode.png               — число реализовавшихся рисков (10 000 прогонов)
Данные совпадают с tools/build_pz3.py (заполненный Excel-шаблон и отчёт .docx).
"""
import csv
import os

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMES = os.path.join(HERE, '..', '06_схемы')
RESULTS = os.path.join(HERE, '..', '07_результаты')
HIGH, LOW = 0.505, 0.14

RISKS = [
    ('Объём распределённой архитектуры (7 сервисов) превышает ресурсы одного исполнителя', 'Планирование', 0.7, 0.8, 'Снижение',
     'Velocity ниже плана два спринта подряд', 'Walking skeleton в S0, поэтапное подключение сервисов, перенос Could have в Post-MVP'),
    ('Вытеснение продуктовых задач лабораторными работами ч. 2', 'Организационный', 0.6, 0.6, 'Снижение',
     'Лабораторная занимает более одного спринта', 'ЛР реализуется как компонент продукта; дорожка Expedite, WIP = 1'),
    ('Расхождение грамматики DSL и профилей нотаций', 'Технический', 0.4, 0.7, 'Уклонение',
     'Падение контрактных тестов каталога нотаций', 'Единый каталог нотаций в packages/contracts, генерация подсветки и шаблонов'),
    ('Хранимая XSS через подписи узлов в SVG', 'Безопасность', 0.3, 0.9, 'Уклонение',
     'Замечание аудита, срабатывание CSP', 'Экранирование, DOMPurify, политика CSP'),
    ('Требования 100 % покрытия и отсутствия комментариев замедляют разработку', 'Технический', 0.5, 0.5, 'Снижение',
     'CI блокирует слияние > 2 дней', 'TDD с первого спринта, моки портов, линтер-правило'),
    ('Отказ в согласовании Python-сервисов', 'Организационный', 0.3, 0.8, 'Снижение',
     'Замечание руководителя по разделу 2.1', 'Обоснование в записке, согласование в S1'),
    ('Перегрузка или болезнь единственного исполнителя', 'Организационный', 0.3, 0.8, 'Принятие',
     'Цель спринта не выполнена по внешним причинам', 'Буферный спринт S12, ADR и документация в репозитории'),
    ('Изменение бесплатных лимитов LLM API', 'Внешний', 0.5, 0.4, 'Снижение',
     'HTTP 429, отзыв ключа', 'Несколько провайдеров, заглушка по умолчанию, локальный Ollama'),
    ('Изменение бесплатных тарифов хостинга', 'Внешний', 0.3, 0.7, 'Передача',
     'Уведомление провайдера, превышение лимита', 'Резервный провайдер Fly.io, локальный стенд docker compose'),
    ('Время Run > 300 мс для 200 узлов', 'Технический', 0.3, 0.5, 'Снижение',
     'Нагрузочный тест анализа', 'Кэш в Redis, elkjs в Web Worker, профилирование'),
    ('Перенос даты защиты на более ранний срок', 'Планирование', 0.3, 0.6, 'Принятие',
     'Объявление расписания защиты', 'Уточнение даты в S1, перенос Should have в Post-MVP'),
    ('Утечка API-ключей и OAuth-токенов', 'Безопасность', 0.2, 0.8, 'Уклонение',
     'Secret scanning GitHub', 'Секреты только на сервере, AES-GCM, gitleaks в CI'),
    ('Нарушение Закона РБ № 99-З о персональных данных', 'Правовой', 0.2, 0.6, 'Уклонение',
     'Регистрация без политики обработки ПДн', 'Политика ПДн, согласие, минимизация данных'),
]


def level(h):
    return 'Высокий' if h >= HIGH else ('Средний' if h >= LOW else 'Низкий')


def to5(x):
    """Перевод оценки 0–1 в шкалу 1–5 шаблона (0,2 → 1 … 1,0 → 5)."""
    return int(min(5, max(1, round(x * 5 + 1e-9))))


def rows():
    out = []
    for k, (name, cat, p, i, strat, trig, act) in enumerate(RISKS, 1):
        h = round(p * i, 4)
        out.append(dict(no=k, name=name, cat=cat, p=p, i=i, h=h, lvl=level(h), strat=strat, trig=trig, act=act,
                        p5=to5(p), i5=to5(i)))
    return out


def fmt(x):
    return f'{x:g}'.replace('.', ',')


def write_register(data):
    ranked = sorted(data, key=lambda r: (-r['h'], r['no']))
    with open(os.path.join(RESULTS, 'Реестр рисков - NotaCode.md'), 'w', encoding='utf-8') as f:
        f.write('# Реестр и ранжирование рисков — NotaCode\n\nСгенерировано `04_расчёты-python/risk_analysis.py`. '
                f'Пороги шаблона: высокий H ≥ {fmt(HIGH)}, средний {fmt(LOW)} ≤ H < {fmt(HIGH)}, низкий H < {fmt(LOW)}.\n\n')
        f.write('| Ранг | № | Риск | Категория | P | I | H = P×I | P (1–5) | I (1–5) | P×I (1–25) | Приоритет | Стратегия |\n')
        f.write('|---|---|---|---|---|---|---|---|---|---|---|---|\n')
        for k, r in enumerate(ranked, 1):
            f.write(f'| {k} | R{r["no"]} | {r["name"]} | {r["cat"]} | {fmt(r["p"])} | {fmt(r["i"])} | {fmt(r["h"])} | '
                    f'{r["p5"]} | {r["i5"]} | {r["p5"] * r["i5"]} | {r["lvl"]} | {r["strat"]} |\n')
        cnt = {l: sum(r['lvl'] == l for r in data) for l in ('Высокий', 'Средний', 'Низкий')}
        f.write(f'\nИтого: {len(data)} рисков; высокий — {cnt["Высокий"]}, средний — {cnt["Средний"]}, '
                f'низкий — {cnt["Низкий"]}. Суммарная ожидаемая «мера риска» ΣH = {fmt(round(sum(r["h"] for r in data), 3))}.\n')
    with open(os.path.join(RESULTS, 'Реестр рисков - NotaCode.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['№', 'Риск', 'Категория', 'Триггер', 'P', 'I', 'H', 'Приоритет', 'Стратегия', 'Мероприятия'])
        for r in data:
            w.writerow([f'R{r["no"]}', r['name'], r['cat'], r['trig'], fmt(r['p']), fmt(r['i']), fmt(r['h']),
                        r['lvl'], r['strat'], r['act']])
    return ranked, cnt


def risk_map(data):
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    xs = np.linspace(0.001, 1, 400)
    ax.fill_between(xs, 0, 1, color='#e2efd9')
    ax.fill_between(xs, np.clip(LOW / xs, 0, 1), 1, color='#fff2cc')
    ax.fill_between(xs, np.clip(HIGH / xs, 0, 1), 1, color='#f8cbad')
    seen = {}
    for r in data:
        k = seen.get((r['p'], r['i']), 0)
        seen[(r['p'], r['i'])] = k + 1
        ax.scatter(r['p'], r['i'], s=70, color='#1f4e79', zorder=3)
        ax.annotate(f'R{r["no"]}', (r['p'], r['i']), xytext=(7, 5 - 13 * k), textcoords='offset points',
                    fontsize=11, fontweight='bold', color='#1f4e79')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks(np.arange(0, 1.01, 0.1))
    ax.set_yticks(np.arange(0, 1.01, 0.1))
    ax.grid(color='white')
    ax.set_xlabel('Оценка вероятности возникновения риска (P)')
    ax.set_ylabel('Оценка силы воздействия риска (I)')
    ax.set_title('Карта рисков проекта NotaCode')
    ax.legend(handles=[Patch(color='#f8cbad', label=f'Высокий (H ≥ {fmt(HIGH)})'),
                       Patch(color='#fff2cc', label=f'Средний ({fmt(LOW)} ≤ H < {fmt(HIGH)})'),
                       Patch(color='#e2efd9', label=f'Низкий (H < {fmt(LOW)})')], loc='lower left')
    fig.tight_layout()
    fig.savefig(os.path.join(SCHEMES, 'Карта рисков (зоны) - NotaCode.png'))
    plt.close(fig)


def heat_matrix(data):
    m = np.fromfunction(lambda r, c: (r + 1) * (c + 1), (5, 5))
    fig, ax = plt.subplots(figsize=(9, 7.5), dpi=150)
    ax.imshow(m, cmap='RdYlGn_r', origin='lower', extent=(0.5, 5.5, 0.5, 5.5), vmin=1, vmax=25)
    cells = {}
    for r in data:
        cells.setdefault((r['p5'], r['i5']), []).append(f'R{r["no"]}')
    for p in range(1, 6):
        for i in range(1, 6):
            txt = f'{p * i}'
            if (p, i) in cells:
                txt += '\n' + ', '.join(cells[(p, i)])
            ax.text(p, i, txt, ha='center', va='center', fontsize=9, fontweight='bold')
    ax.set_xticks(range(1, 6), ['1 Очень низкая', '2 Низкая', '3 Средняя', '4 Высокая', '5 Очень высокая'], fontsize=8)
    ax.set_yticks(range(1, 6), ['1 Очень низкое', '2 Низкое', '3 Среднее', '4 Высокое', '5 Очень высокое'], fontsize=8)
    ax.set_xlabel('Вероятность (шкала шаблона 1–5)')
    ax.set_ylabel('Воздействие (шкала шаблона 1–5)')
    ax.set_title('Тепловая матрица рисков NotaCode (приоритет = В × Вл)')
    fig.tight_layout()
    fig.savefig(os.path.join(SCHEMES, 'Тепловая матрица 5x5 - NotaCode.png'))
    plt.close(fig)


def pareto(ranked):
    fig, ax = plt.subplots(figsize=(11, 5), dpi=150)
    colors = ['#c00000' if r['lvl'] == 'Высокий' else '#ffc000' if r['lvl'] == 'Средний' else '#70ad47' for r in ranked]
    ax.bar([f'R{r["no"]}' for r in ranked], [r['h'] for r in ranked], color=colors, edgecolor='black')
    cum = np.cumsum([r['h'] for r in ranked]) / sum(r['h'] for r in ranked) * 100
    ax2 = ax.twinx()
    ax2.plot(range(len(ranked)), cum, color='#1f4e79', marker='o')
    ax2.set_ylim(0, 105)
    ax2.set_ylabel('Накопленная доля ΣH, %')
    ax.axhline(HIGH, ls='--', color='#c00000', lw=1)
    ax.axhline(LOW, ls='--', color='#70ad47', lw=1)
    ax.set_ylabel('H = P × I')
    ax.set_title('Ранжирование рисков NotaCode (диаграмма Парето)')
    fig.tight_layout()
    fig.savefig(os.path.join(SCHEMES, 'Ранжирование рисков - NotaCode.png'))
    plt.close(fig)


def strategies(data):
    names = ['Уклонение', 'Снижение', 'Передача', 'Принятие']
    vals = [sum(r['strat'] == n for r in data) for n in names]
    fig, ax = plt.subplots(figsize=(7, 5), dpi=150)
    ax.pie(vals, labels=[f'{n} — {v}' for n, v in zip(names, vals)], autopct='%1.0f%%',
           colors=['#5b9bd5', '#ed7d31', '#a5a5a5', '#ffc000'], startangle=90)
    ax.set_title('Стратегии реагирования на риски NotaCode')
    fig.tight_layout()
    fig.savefig(os.path.join(SCHEMES, 'Стратегии реагирования - NotaCode.png'))
    plt.close(fig)
    return dict(zip(names, vals))


def monte_carlo(data, n=10_000, seed=42):
    rng = np.random.default_rng(seed)
    p = np.array([r['p'] for r in data])
    hits = (rng.random((n, len(p))) < p).sum(axis=1)
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=150)
    ax.hist(hits, bins=np.arange(-0.5, len(p) + 1.5), color='#5b9bd5', edgecolor='black')
    ax.axvline(hits.mean(), color='#c00000', ls='--', label=f'среднее = {hits.mean():.2f}')
    ax.set_xlabel('Число реализовавшихся рисков за проект')
    ax.set_ylabel('Частота (из 10 000 прогонов)')
    ax.set_title('Моделирование Монте-Карло: сколько рисков NotaCode наступит')
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(SCHEMES, 'Монте-Карло - NotaCode.png'))
    plt.close(fig)
    return hits.mean(), np.percentile(hits, 90)


if __name__ == '__main__':
    os.makedirs(SCHEMES, exist_ok=True)
    os.makedirs(RESULTS, exist_ok=True)
    data = rows()
    ranked, cnt = write_register(data)
    risk_map(data)
    heat_matrix(data)
    pareto(ranked)
    st = strategies(data)
    mean, p90 = monte_carlo(data)
    print('Приоритеты:', cnt)
    print('Топ-3:', [(f'R{r["no"]}', r['h']) for r in ranked[:3]])
    print('Стратегии:', st)
    print(f'Монте-Карло: в среднем наступит {mean:.2f} риска, в 90 % случаев — не более {p90:.0f}')
