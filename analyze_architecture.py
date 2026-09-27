#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Анализ архитектуры папок и файлов проекта Управление проектами
"""

import os
import sys
from collections import defaultdict, Counter
import json
from pathlib import Path

def analyze_project_structure(root_path):
    """Анализирует структуру проекта и возвращает статистику"""

    stats = {
        'total_files': 0,
        'total_dirs': 0,
        'file_types': Counter(),
        'dir_tree': {},
        'largest_files': [],
        'depth_analysis': defaultdict(int),
        'empty_dirs': [],
        'naming_patterns': Counter()
    }

    # Преобразуем в Path объект для удобной работы
    root = Path(root_path)

    # Храним информацию о файлах для сортировки по размеру
    files_info = []

    # Обходим всю директорию
    for dirpath, dirnames, filenames in os.walk(root):
        dirpath_obj = Path(dirpath)
        rel_path = dirpath_obj.relative_to(root)

        # Подсчитываем директории
        stats['total_dirs'] += len(dirnames)

        # Анализируем глубину
        depth = len(rel_path.parts)
        stats['depth_analysis'][depth] += 1

        # Проверяем пустые директории
        if not dirnames and not filenames:
            stats['empty_dirs'].append(str(rel_path))

        # Анализируем файлы
        for filename in filenames:
            stats['total_files'] += 1

            # Получаем расширение файла
            file_path = dirpath_obj / filename
            try:
                size = file_path.stat().st_size
                files_info.append((str(file_path.relative_to(root)), size))

                # Подсчитываем типы файлов
                if '.' in filename:
                    ext = filename.split('.')[-1].lower()
                    stats['file_types'][ext] += 1
                else:
                    stats['file_types']['no_extension'] += 1

                # Анализируем паттерны именования
                name_without_ext = filename.split('.')[0] if '.' in filename else filename
                if '_' in name_without_ext:
                    stats['naming_patterns']['underscore_separated'] += 1
                elif '-' in name_without_ext:
                    stats['naming_patterns']['hyphen_separated'] += 1
                elif any(c.isupper() for c in name_without_ext):
                    stats['naming_patterns']['camelCase_or_PascalCase'] += 1
                else:
                    stats['naming_patterns']['lowercase_or_numeric'] += 1

            except (OSError, PermissionError):
                # Пропускаем файлы, к которым нет доступа
                continue

    # Сортируем файлы по размеру (пять największych)
    files_info.sort(key=lambda x: x[1], reverse=True)
    stats['largest_files'] = files_info[:5]

    # Строим дерево директорий (упрощенное)
    for dirpath, dirnames, filenames in os.walk(root):
        dirpath_obj = Path(dirpath)
        rel_path = dirpath_obj.relative_to(root)
        if str(rel_path) == '.':
            rel_path = Path('')

        # Добавляем текущую директорию в дерево
        current_level = stats['dir_tree']
        for part in rel_path.parts:
            if part not in current_level:
                current_level[part] = {'__files__': [], '__dirs__': {}}
            current_level = current_level[part]['__dirs__']

        # Добавляем файлы в текущую директорию
        parent_level = stats['dir_tree']
        for part in rel_path.parts:
            if part == '':  # Корневая директория
                parent_level[part] = {'__files__': [], '__dirs__': {}}
                break
            if part not in parent_level:
                parent_level[part] = {'__files__': [], '__dirs__': {}}
            parent_level = parent_level[part]['__dirs__']

        if str(rel_path) == '.':
            # Особая обработка для корня
            stats['dir_tree']['__files__'] = filenames
            stats['dir_tree']['__dirs__'] = {d: {'__files__': [], '__dirs__': {}} for d in dirnames}
        else:
            # Добавляем файлы в соответствующую директорию в дереве
            # Это сложно сделать правильно в одном проходе, поэтому упростим
            pass

    # Для простоты, создадим текстовое представление дерева
    stats['tree_text'] = generate_tree_text(root)

    return stats

def generate_tree_text(root_path, prefix="", is_last=True):
    """Генерирует текстовое представление дерева директорий"""
    root = Path(root_path)
    tree_text = ""

    # Добавляем текущую директорию/файл
    if prefix:
        connector = "└── " if is_last else "├── "
        tree_text += f"{prefix}{connector}{root.name}\n"

    # Если это директория, рекурсивно обрабатываем содержимое
    if root.is_dir():
        try:
            contents = list(root.iterdir())
            # Сортируем: сначала директории, потом файлы
            contents.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

            for i, item in enumerate(contents):
                is_last_item = (i == len(contents) - 1)
                extension = "    " if is_last else "│   "
                new_prefix = prefix + extension

                if item.is_dir():
                    tree_text += generate_tree_text(item, new_prefix, is_last_item)
                else:
                    connector = "└── " if is_last_item else "├── "
                    tree_text += f"{new_prefix}{connector}{item.name}\n"
        except (PermissionError, OSError):
            # Если нет доступа к директории
            pass

    return tree_text

def save_analysis_to_md(stats, output_path):
    """Сохраняет анализ в markdown файл"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Анализ архитектуры проекта Управление проектами\n\n")

        f.write("## Общая статистика\n\n")
        f.write(f"- **Всего файлов:** {stats['total_files']}\n")
        f.write(f"- **Всего директорий:** {stats['total_dirs']}\n")
        f.write(f"- **Пустых директорий:** {len(stats['empty_dirs'])}\n\n")

        f.write("## Анализ глубины структуры\n\n")
        f.write("Глубина | Количество директорий\n")
        f.write("--------|----------------------\n")
        for depth in sorted(stats['depth_analysis'].keys()):
            f.write(f"{depth:>7} | {stats['depth_analysis'][depth]:>22}\n")
        f.write("\n")

        f.write("## Типы файлов\n\n")
        f.write("Тип | Количество\n")
        f.write("----|----------\n")
        for ext, count in stats['file_types'].most_common():
            f.write(f".{ext if ext != 'no_extension' else '(нет)'} | {count:>10}\n")
        f.write("\n")

        f.write("## Пять крупнейших файлов\n\n")
        f.write("Файл | Размер (байты)\n")
        f.write("----|--------------\n")
        for file_path, size in stats['largest_files']:
            # Обрезаем длинные пути для читаемости
            display_path = file_path if len(file_path) <= 50 else "..." + file_path[-47:]
            f.write(f"{display_path} | {size:>14}\n")
        f.write("\n")

        f.write("## Паттерны именования файлов\n\n")
        f.write("Паттерн | Количество\n")
        f.write("--------|----------\n")
        for pattern, count in stats['naming_patterns'].most_common():
            f.write(f"{pattern} | {count:>10}\n")
        f.write("\n")

        f.write("## Структура проекта (дерево)\n\n")
        f.write("```\n")
        f.write(stats['tree_text'])
        f.write("```\n\n")

        f.write("## Пустые директории\n\n")
        if stats['empty_dirs']:
            for empty_dir in stats['empty_dirs']:
                f.write(f"- `{empty_dir}`\n")
        else:
            f.write("Пустых директорий не найдено.\n")
        f.write("\n")

        f.write("*Анализ выполнен с помощью Python скрипта analyze_architecture.py*\n")

def main():
    """Основная функция"""
    project_root = r"E:\ИИТ\УправлениеПроектами"

    print("Анализ архитектуры проекта...")
    stats = analyze_project_structure(project_root)

    output_file = r"E:\ИИТ\УправлениеПроектами\PROJECT_ARCHITECTURE_ANALYSIS.md"
    save_analysis_to_md(stats, output_file)

    print(f"Анализ завершен. Результат сохранен в: {output_file}")
    print(f"Найдено файлов: {stats['total_files']}")
    print(f"Найдено директорий: {stats['total_dirs']}")

if __name__ == "__main__":
    main()