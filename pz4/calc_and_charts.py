# -*- coding: utf-8 -*-
"""
Расчёты и диаграммы для ПЗ1 и ПЗ4 (проект NotaCode).
Генерирует:
  pz4/img/gantt_critical_path.png   - диаграмма Ганта с критическим путём
  pz4/img/network_diagram.png       - сетевой график (узлы = работы)
  pz4/img/cpm_table.csv             - таблица ES/EF/LS/LF/Резерв
  pz1/img/stakeholder_quadrant.png  - матрица стейкхолдеров (квадранты)
  pz1/img/risk_map.png              - карта рисков (вероятность/воздействие)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import csv, os

OUT_PZ4 = r"C:\Users\zheny\AppData\Local\Temp\pm-repo-check\ProjectManagement\pz4\img"
OUT_PZ1 = r"C:\Users\zheny\AppData\Local\Temp\pm-repo-check\ProjectManagement\pz1\img"
os.makedirs(OUT_PZ4, exist_ok=True)
os.makedirs(OUT_PZ1, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. WBS проекта NotaCode: код, название, длительность (мес.), предшественники
# ---------------------------------------------------------------------------
tasks = {
    "1.0":  {"name": "Бизнес-анализ и требования",              "dur": 0.5, "pred": []},
    "2.0":  {"name": "Архитектура и ADR",                        "dur": 0.5, "pred": ["1.0"]},
    "3.0":  {"name": "Фундамент (CI, Docker, walking skeleton)",  "dur": 0.5, "pred": ["2.0"]},
    "4.0":  {"name": "Gateway и доступ (Express, Sequelize, JWT)","dur": 1.0, "pred": ["3.0"]},
    "5.0":  {"name": "Язык DSL (грамматика, парсер, диагностика)","dur": 1.0, "pred": ["3.0"]},
    "6.0":  {"name": "Web IDE (оболочка, Monaco, темы, панели)",  "dur": 1.5, "pred": ["5.0"]},
    "7.0":  {"name": "Нотации волны 1 (UML, ERD, IDEF0)",        "dur": 1.5, "pred": ["5.0"]},
    "8.0":  {"name": "Холст (SVG, elkjs, подсветка)",             "dur": 1.0, "pred": ["5.0"]},
    "9.0":  {"name": "Сохранение и интеграции (БД, GitHub, Drive)","dur": 1.0, "pred": ["4.0", "6.0"]},
    "10.0": {"name": "Экспорт/импорт форматов",                   "dur": 0.5, "pred": ["7.0"]},
    "11.0": {"name": "AI-ассистент (заглушка, режимы)",           "dur": 0.5, "pred": ["6.0"]},
    "12.0": {"name": "Версии, diff, откат",                       "dur": 0.5, "pred": ["9.0"]},
    "13.0": {"name": "Качество и наблюдаемость (тесты, Lighthouse)","dur": 0.5,"pred": ["7.0","8.0","9.0","10.0","11.0","12.0"]},
    "14.0": {"name": "Документация и РПЗ курсовой",               "dur": 0.75,"pred": ["13.0"]},
    "15.0": {"name": "Стабилизация MVP, буфер, защита",           "dur": 0.25,"pred": ["14.0"]},
}

order = list(tasks.keys())

# --- Прямой проход (ES/EF) ---
for code in order:
    t = tasks[code]
    if not t["pred"]:
        t["ES"] = 0.0
    else:
        t["ES"] = max(tasks[p]["EF"] for p in t["pred"])
    t["EF"] = t["ES"] + t["dur"]

project_duration = max(t["EF"] for t in tasks.values())

# --- Обратный проход (LS/LF) ---
successors = {code: [] for code in order}
for code, t in tasks.items():
    for p in t["pred"]:
        successors[p].append(code)

for code in reversed(order):
    t = tasks[code]
    succ = successors[code]
    if not succ:
        t["LF"] = project_duration
    else:
        t["LF"] = min(tasks[s]["LS"] for s in succ)
    t["LS"] = t["LF"] - t["dur"]
    t["float"] = round(t["LS"] - t["ES"], 3)
    t["critical"] = abs(t["float"]) < 1e-6

critical_path = [c for c in order if tasks[c]["critical"]]

print("Длительность проекта (мес.):", project_duration)
print("Критический путь:", " -> ".join(critical_path))

# --- CSV-таблица ---
csv_path = os.path.join(OUT_PZ4, "cpm_table.csv")
with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Код", "Название работы", "Длительность (мес.)", "Предшественники",
                "ES", "EF", "LS", "LF", "Резерв", "Критическая"])
    for code in order:
        t = tasks[code]
        w.writerow([code, t["name"], t["dur"], ", ".join(t["pred"]) or "-",
                    round(t["ES"], 3), round(t["EF"], 3), round(t["LS"], 3), round(t["LF"], 3),
                    t["float"], "ДА" if t["critical"] else "нет"])
print("Сохранено:", csv_path)

# ---------------------------------------------------------------------------
# 2. Диаграмма Ганта с критическим путём
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6))
yticks = []
ylabels = []
for i, code in enumerate(order):
    t = tasks[code]
    color = "#d62728" if t["critical"] else "#1f77b4"
    ax.barh(i, t["dur"], left=t["ES"], height=0.55, color=color, edgecolor="black")
    if not t["critical"] and t["float"] > 0:
        ax.barh(i, t["float"], left=t["EF"], height=0.15, color="#cccccc", edgecolor="black", hatch="//")
    yticks.append(i)
    ylabels.append(f"{code} {t['name']}")

ax.set_yticks(yticks)
ax.set_yticklabels(ylabels, fontsize=8)
ax.invert_yaxis()
ax.set_xlabel("Месяцы от старта проекта")
ax.set_title("Диаграмма Ганта проекта NotaCode (критический путь — красный)")
ax.grid(axis="x", linestyle="--", alpha=0.5)
crit_patch = mpatches.Patch(color="#d62728", label="Критическая работа")
noncrit_patch = mpatches.Patch(color="#1f77b4", label="Некритическая работа")
float_patch = mpatches.Patch(facecolor="#cccccc", edgecolor="black", hatch="//", label="Резерв времени")
ax.legend(handles=[crit_patch, noncrit_patch, float_patch], loc="lower right", fontsize=8)
plt.tight_layout()
gantt_path = os.path.join(OUT_PZ4, "gantt_critical_path.png")
plt.savefig(gantt_path, dpi=150)
plt.close(fig)
print("Сохранено:", gantt_path)

# ---------------------------------------------------------------------------
# 3. Сетевой график (узлы = работы, метод предшествования, PDM)
# ---------------------------------------------------------------------------
import networkx as nx

G = nx.DiGraph()
for code, t in tasks.items():
    G.add_node(code, label=f"{code}\n{t['name'][:22]}\nD={t['dur']}")
for code, t in tasks.items():
    for p in t["pred"]:
        G.add_edge(p, code)

pos = nx.spring_layout(G, seed=7, k=1.4)
# для наглядности расположим по уровням (topological)
levels = {}
for code in nx.topological_sort(G):
    preds = list(G.predecessors(code))
    levels[code] = 0 if not preds else max(levels[p] for p in preds) + 1
by_level = {}
for code, lvl in levels.items():
    by_level.setdefault(lvl, []).append(code)
pos = {}
for lvl, codes in by_level.items():
    for i, code in enumerate(codes):
        pos[code] = (lvl * 2.2, -i * 1.6 + (len(codes) - 1) * 0.8)

fig, ax = plt.subplots(figsize=(13, 7))
node_colors = ["#d62728" if tasks[c]["critical"] else "#9ecae1" for c in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_size=2600, node_color=node_colors, edgecolors="black", ax=ax)
nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=15, ax=ax,
                        edge_color=["#d62728" if (tasks[u]["critical"] and tasks[v]["critical"]) else "#888888"
                                    for u, v in G.edges()],
                        width=[2.2 if (tasks[u]["critical"] and tasks[v]["critical"]) else 1.0
                               for u, v in G.edges()])
labels = {c: G.nodes[c]["label"] for c in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, font_size=6.5, ax=ax)
ax.set_title("Сетевой график NotaCode (метод предшествования, PDM) — критический путь красным")
ax.axis("off")
plt.tight_layout()
net_path = os.path.join(OUT_PZ4, "network_diagram.png")
plt.savefig(net_path, dpi=150)
plt.close(fig)
print("Сохранено:", net_path)

# ---------------------------------------------------------------------------
# 4. Матрица стейкхолдеров (квадранты влияние/интерес) — ПЗ1
# ---------------------------------------------------------------------------
stakeholders = [
    ("SH-01 PO",            5, 5),
    ("SH-02 Разработчик",   4, 5),
    ("SH-05 Рук. курсовой", 5, 3),
    ("SH-06 Преп. лаб.",    5, 3),
    ("SH-08 Комиссия",      5, 2),
    ("SH-03 Scrum Master",  2, 4),
    ("SH-04 Review Board",  3, 4),
    ("SH-09 Студенты",      2, 4),
    ("SH-10 Бизнес-аналит.",2, 3),
    ("SH-11 Архитекторы",   2, 3),
    ("SH-12 Преп.-польз.",  3, 2),
    ("SH-07 Преп. ИИТ",     4, 3),
    ("SH-13 AI-провайдеры", 4, 1),
    ("SH-15 Хостинг",       3, 1),
    ("SH-17 Регулятор",     4, 1),
]

fig, ax = plt.subplots(figsize=(8, 8))
ax.axvline(3, color="black", linewidth=1)
ax.axhline(3, color="black", linewidth=1)
ax.set_xlim(0.5, 5.5)
ax.set_ylim(0.5, 5.5)
for name, infl, interest in stakeholders:
    ax.scatter(interest, infl, s=140, color="#3182bd", edgecolors="black", zorder=3)
    ax.annotate(name, (interest, infl), textcoords="offset points", xytext=(6, 4), fontsize=7)
ax.set_xlabel("Заинтересованность (интерес), 1–5")
ax.set_ylabel("Влияние, 1–5")
ax.set_title("Матрица стейкхолдеров NotaCode: влияние / интерес")
ax.text(1.3, 5.3, "D: Мин. информирование", fontsize=8, color="gray")
ax.text(3.3, 5.3, "A: Активное вовлечение", fontsize=8, color="gray")
ax.text(1.3, 0.8, "C: Мин. контроль", fontsize=8, color="gray")
ax.text(3.3, 0.8, "B: Консультирование", fontsize=8, color="gray")
ax.grid(alpha=0.3)
plt.tight_layout()
sh_path = os.path.join(OUT_PZ1, "stakeholder_quadrant.png")
plt.savefig(sh_path, dpi=150)
plt.close(fig)
print("Сохранено:", sh_path)

# ---------------------------------------------------------------------------
# 5. Карта рисков (вероятность x воздействие, 1..5, размер = коэффициент)
# ---------------------------------------------------------------------------
risks = [
    ("R1 Bus factor", 3, 5),
    ("R2 100% покрытие", 4, 3),
    ("R3 Распред. архитектура", 4, 4),
    ("R4 AI/хостинг квоты", 3, 3),
    ("R5 Расхождение ключей нотаций", 3, 4),
    ("R6 XSS в SVG", 2, 5),
    ("R7 Лабы съедают время", 4, 3),
    ("R8 Дата защиты не подтверждена", 3, 3),
    ("R9 Противоречия волн нотаций", 4, 3),
    ("R10 Совместное редактирование", 2, 4),
    ("R11 Утечка ключей", 2, 5),
    ("R12 OAuth/квоты сторонние", 2, 3),
    ("R13 Недоступность демо-стенда", 2, 5),
    ("R14 Кнопки-пустышки", 3, 4),
]

fig, ax = plt.subplots(figsize=(9, 8))
# зоны приоритета
ax.axvspan(0.5, 2.5, ymin=0, ymax=1, color="#2ca02c", alpha=0.08)
ax.axvspan(2.5, 3.5, color="#ff7f0e", alpha=0.08)
ax.axvspan(3.5, 5.5, color="#d62728", alpha=0.08)
for name, prob, impact in risks:
    coeff = prob * impact
    color = "#d62728" if coeff >= 16 else ("#ff7f0e" if coeff >= 9 else "#2ca02c")
    ax.scatter(prob, impact, s=coeff * 18, color=color, edgecolors="black", alpha=0.75, zorder=3)
    ax.annotate(name, (prob, impact), textcoords="offset points", xytext=(6, 4), fontsize=7)
ax.set_xlim(0.5, 5.5)
ax.set_ylim(0.5, 5.5)
ax.set_xlabel("Вероятность, 1–5")
ax.set_ylabel("Воздействие, 1–5")
ax.set_title("Карта рисков проекта NotaCode (размер точки = коэффициент В×Вл)")
ax.grid(alpha=0.3)
plt.tight_layout()
risk_path = os.path.join(OUT_PZ1, "risk_map.png")
plt.savefig(risk_path, dpi=150)
plt.close(fig)
print("Сохранено:", risk_path)

print("\nГотово.")
