# -*- coding: utf-8 -*-
"""
Независимая проверка метода критического пути (CPM) для WBS проекта DiagramCode —
без Excel, чистым Python. Числа здесь должны совпадать с тем, что считает Excel-файл
"Планировщик проекта - DiagramCode.xlsx" (лист "ТАБЛИЦА ДАННЫХ") и с таблицей в
"ИНСТРУКЦИЯ - Excel-файлы (Гант и риски).md".

Запуск: python verify_cpm.py
"""

tasks = {
    1: {"name": "Требования и архитектура", "dur": 5, "pred": []},
    2: {"name": "Проектирование DSL-грамматики и модели данных", "dur": 4, "pred": [1]},
    3: {"name": "Настройка окружения разработки и CI", "dur": 2, "pred": [1]},
    4: {"name": "Реализация DSL-парсера (лексер, AST)", "dur": 6, "pred": [2]},
    5: {"name": "Модель данных и репозитории (SQLAlchemy)", "dur": 5, "pred": [2, 3]},
    6: {"name": "Нотация ERD: валидация и рендер", "dur": 5, "pred": [4]},
    7: {"name": "Аутентификация (JWT, bcrypt)", "dur": 4, "pred": [5]},
    8: {"name": "REST API диаграмм и версий", "dur": 6, "pred": [6, 7]},
    9: {"name": "IDE-оболочка: React + Monaco редактор", "dur": 7, "pred": [3]},
    10: {"name": "Канвас рендера, интеграция Run/Save/Export", "dur": 5, "pred": [8, 9]},
    11: {"name": "Тестирование (pytest + Jest, интеграция)", "dur": 4, "pred": [10]},
    12: {"name": "Подготовка и защита курсовой (РПЗ, демо)", "dur": 3, "pred": [11]},
}


def topo_sort(tasks):
    visited, order = set(), []

    def visit(n):
        if n in visited:
            return
        visited.add(n)
        for p in tasks[n]["pred"]:
            visit(p)
        order.append(n)

    for n in tasks:
        visit(n)
    return order


def compute_cpm(tasks):
    successors = {t: [] for t in tasks}
    for t, info in tasks.items():
        for p in info["pred"]:
            successors[p].append(t)

    order = topo_sort(tasks)

    ES, EF = {}, {}
    for t in order:
        preds = tasks[t]["pred"]
        ES[t] = 1 if not preds else max(EF[p] for p in preds)
        EF[t] = ES[t] + tasks[t]["dur"]

    duration = max(EF.values())

    LF, LS = {}, {}
    for t in reversed(order):
        succs = successors[t]
        LF[t] = duration if not succs else min(LS[s] for s in succs)
        LS[t] = LF[t] - tasks[t]["dur"]

    TF = {t: LS[t] - ES[t] for t in tasks}
    critical_path = [t for t in order if TF[t] == 0]
    return order, ES, EF, LS, LF, TF, duration, critical_path


if __name__ == "__main__":
    order, ES, EF, LS, LF, TF, duration, critical_path = compute_cpm(tasks)

    header = f"{'№':>2} | {'Работа':<48} | {'D':>3} | {'ES':>3} | {'EF':>3} | {'LS':>3} | {'LF':>3} | {'TF':>3} | Крит"
    print(header)
    print("-" * len(header))
    for t in sorted(tasks):
        crit = "ДА" if TF[t] == 0 else "нет"
        print(f"{t:>2} | {tasks[t]['name']:<48} | {tasks[t]['dur']:>3} | {ES[t]:>3} | {EF[t]:>3} | {LS[t]:>3} | {LF[t]:>3} | {TF[t]:>3} | {crit}")

    print()
    print("Критический путь:", " -> ".join(str(t) for t in critical_path))
    print("Общая длительность проекта:", duration, "дней")
