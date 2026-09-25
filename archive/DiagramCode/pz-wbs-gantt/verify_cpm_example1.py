# -*- coding: utf-8 -*-
"""
Независимая проверка метода критического пути (CPM) для готового учебного
"Примера 1" из методички курса («Обучение сотрудников кибербезопасности»,
12 работ) — без Excel, чистым Python. Числа здесь должны совпадать с тем, что
считает Excel-файл "Планировщик проекта - Пример 1 (методичка).xlsx" (лист
"ТАБЛИЦА ДАННЫХ") и с таблицей в
"ИНСТРУКЦИЯ - Excel-файлы (Гант и риски).md".

Это вариант "Б" — на случай, если для сдачи задания принципиально важно
буквально воспроизвести пример из методички, а не считать WBS/Гант по
DiagramCode (см. verify_cpm.py — вариант "А").

Запуск: python verify_cpm_example1.py
"""

tasks = {
    1: {"name": "Устав и стартовое совещание", "dur": 3, "pred": []},
    2: {"name": "Анализ регламентов ИБ", "dur": 5, "pred": [1]},
    3: {"name": "Фишинг-замер + отчет", "dur": 4, "pred": [2]},
    4: {"name": "Выбор вендора + договор", "dur": 6, "pred": [1]},
    5: {"name": "Учетные записи (200 чел.)", "dur": 3, "pred": [4]},
    6: {"name": "Настройка white-list", "dur": 3, "pred": [3, 4]},
    7: {"name": "Курс по ПДн (№ 99-З)", "dur": 8, "pred": [6]},
    8: {"name": "Модули, видео, тесты", "dur": 10, "pred": [6]},
    9: {"name": "Информирование сотрудников", "dur": 2, "pred": [7, 8]},
    10: {"name": "Микрообучение (4 недели)", "dur": 20, "pred": [9]},
    11: {"name": "Итоговый фишинг + тест", "dur": 4, "pred": [10]},
    12: {"name": "Анализ KPI + отчет + регламент", "dur": 5, "pred": [11]},
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

    header = f"{'№':>2} | {'Работа':<32} | {'D':>3} | {'ES':>3} | {'EF':>3} | {'LS':>3} | {'LF':>3} | {'TF':>3} | Крит"
    print(header)
    print("-" * len(header))
    for t in sorted(tasks):
        crit = "ДА" if TF[t] == 0 else "нет"
        print(f"{t:>2} | {tasks[t]['name']:<32} | {tasks[t]['dur']:>3} | {ES[t]:>3} | {EF[t]:>3} | {LS[t]:>3} | {LF[t]:>3} | {TF[t]:>3} | {crit}")

    elapsed = duration - min(ES.values())  # ES нумеруется с 1, а не с 0

    print()
    print("Критический путь:", " -> ".join(str(t) for t in critical_path))
    print(f"Внутренняя нумерация формул (EF последней работы): {duration}")
    print(f"Общая длительность проекта: {elapsed} рабочих дней")
