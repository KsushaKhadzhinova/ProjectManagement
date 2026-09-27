# Анализ архитектуры проекта Управление проектами

## Общая статистика

- **Всего файлов:** 188
- **Всего директорий:** 92
- **Пустых директорий:** 2

## Анализ глубины структуры

Глубина | Количество директорий
--------|----------------------
      0 |                      1
      1 |                      9
      2 |                     12
      3 |                     69
      4 |                      2

## Типы файлов

Тип | Количество
----|----------
.(нет) |         88
.md |         38
.pptx |         15
.sample |         14
.docx |         11
.xlsx |          6
.png |          5
.ppt |          3
.py |          2
.xlsm |          2
.bas |          2
.graph |          1
.csv |          1

## Пять крупнейших файлов

Файл | Размер (байты)
----|--------------
tasks\theory\Тема 2 УРПО (5).pptx |        7599709
tasks.md\theory\Тема 2 УРПО (5).pptx |        7599709
theory\Тема 2 УРПО (5).pptx |        7599709
...jects\bd\0091715095b6ed6c10b4576d49d04f3246d064 |        7210880
tasks\to do\УП-ПЗ1-60121 (3).pptx |        2876565

## Паттерны именования файлов

Паттерн | Количество
--------|----------
lowercase_or_numeric |         95
camelCase_or_PascalCase |         45
hyphen_separated |         35
underscore_separated |         13

## Структура проекта (дерево)

```
    ├── .git
    │   ├── gk
    │   │   └── config
    │   ├── hooks
    │   │   ├── applypatch-msg.sample
    │   │   ├── commit-msg.sample
    │   │   ├── fsmonitor-watchman.sample
    │   │   ├── post-update.sample
    │   │   ├── pre-applypatch.sample
    │   │   ├── pre-commit.sample
    │   │   ├── pre-merge-commit.sample
    │   │   ├── pre-push.sample
    │   │   ├── pre-rebase.sample
    │   │   ├── pre-receive.sample
    │   │   ├── prepare-commit-msg.sample
    │   │   ├── push-to-checkout.sample
    │   │   ├── sendemail-validate.sample
    │   │   └── update.sample
    │   ├── info
    │   │   └── exclude
    │   ├── logs
    │   │   ├── refs
    │   │   │   └── heads
    │   │   │       └── master
    │   │   └── HEAD
    │   ├── objects
    │   │   ├── 05
    │   │   │   ├── c0e682fc947293999a06af8c122d9b5541ae09
    │   │   │   └── d9d2b57319545af2a8a2e20f7f5e5d71e3669d
    │   │   ├── 09
    │   │   │   └── 8a0d6e05242db362731b87b07acf0a14f6266a
    │   │   ├── 10
    │   │   │   ├── 6a1a2b1dad0690c07d02c95831ea7bc9c97f48
    │   │   │   └── 70fd1999f7c72c55bf503cfb14e05e09d01f18
    │   │   ├── 15
    │   │   │   ├── 25654f2805d9f234f0f6c67848764d16088dec
    │   │   │   └── c8cb117a2202e845ea783bd3cd9484b8786cf5
    │   │   ├── 17
    │   │   │   └── f98be1c8a1649147b2467b19667e533140c3c9
    │   │   ├── 18
    │   │   │   └── 6277b3f9d31ab35d8a75f3842e30aad0fed314
    │   │   ├── 1a
    │   │   │   └── 3bb283e5c964da3cafba10ca7700803564c1ff
    │   │   ├── 1b
    │   │   │   ├── 6e1392b1242e79c97161905ab3f1371c744b60
    │   │   │   └── 8d19f77ad80613238eebb682ed75f72db2ef36
    │   │   ├── 1d
    │   │   │   └── 752ea86875ce926f0b9da6d165d7ab0c86c97d
    │   │   ├── 1f
    │   │   │   └── 79891c9bddbfd5bd1f07c8ed189738af95ef99
    │   │   ├── 23
    │   │   │   └── 9e9ada86d5a7127ac485e8ed5c2264d8fe5a08
    │   │   ├── 28
    │   │   │   └── 54a5c18fda46de7fd81c86bbad1a0e00d3d7cb
    │   │   ├── 30
    │   │   │   └── b054193c0a69406b5650239382fcb1c99c3a89
    │   │   ├── 32
    │   │   │   └── f10b7c322fddbde481afb34a4d3ad9456c8e33
    │   │   ├── 35
    │   │   │   └── 431be98b89c62892c02811c26cce1081cfb40d
    │   │   ├── 3d
    │   │   │   └── a6060b84e25f6fabc5223fcd790d52a2efe0f2
    │   │   ├── 40
    │   │   │   └── 3c98ed8d53e46cd001a63fd19f82285fcc384a
    │   │   ├── 41
    │   │   │   └── f678a2ce196870315b71359412ac495392ef4f
    │   │   ├── 46
    │   │   │   └── b401b097b236b048e9de2496d09e15c8a65183
    │   │   ├── 4d
    │   │   │   └── 2702ddf8a03a03b239d14c69581f70137281b6
    │   │   ├── 4f
    │   │   │   ├── 841b0e4a7587619608f49b9ea1bced622afa7a
    │   │   │   └── f2549159490def03134aaf23276f59262f9d61
    │   │   ├── 57
    │   │   │   └── 97d827aceaca074bb117f52ad0f3d1a59be945
    │   │   ├── 5d
    │   │   │   └── 8cd580f082cbda3991ef9f4a0c94efc25a8aa7
    │   │   ├── 60
    │   │   │   └── 631a72c4e0a4599a95ef5bf7d7c1dfd1ba77fe
    │   │   ├── 64
    │   │   │   └── d10ee5adb2da0cb66086ce7c0bcf0cabcfe1f9
    │   │   ├── 67
    │   │   │   └── 5ae14db8ac22def22f0ce8c61871989d1e7044
    │   │   ├── 72
    │   │   │   └── 4220d6fbbbc26e3b86e8d9bf0090d1011e10c4
    │   │   ├── 76
    │   │   │   └── 35211b0ee5c5cb356eee99dd2a5553b7bfe15b
    │   │   ├── 78
    │   │   │   └── 8ffb4ea91846c934678c2df7c79e6a6c9d4161
    │   │   ├── 7d
    │   │   │   └── 9f1ef9f7b3c6b63c6a710fa72b5f5038c60a81
    │   │   ├── 7e
    │   │   │   └── 8c4327ab323884dbd0ab61f066f828dfb87532
    │   │   ├── 86
    │   │   │   └── 37cc3ef0fc9385c80b75eeec3726e46de6a237
    │   │   ├── 87
    │   │   │   └── 64df056d472e7030bdc02798f3aff75fb43680
    │   │   ├── 88
    │   │   │   └── db4594c55b550a4584216fd037650a58433a0e
    │   │   ├── 8b
    │   │   │   └── 65c13f0c7687b33ed8162a15a0ee16817bb354
    │   │   ├── 8c
    │   │   │   └── 917cbbb5316561b1990493ff550ec2616ab960
    │   │   ├── 8e
    │   │   │   └── 5942b7e4e30daa30a6817ff9acdcada082108e
    │   │   ├── 8f
    │   │   │   └── e1f15a70614c3fba016667a8ba8488cb1851b2
    │   │   ├── 99
    │   │   │   └── ef8e1742aeb8d325ebc71a207643f982c1fa11
    │   │   ├── 9c
    │   │   │   └── 7e3d3d9f37c3a4cf98807283c0bd41f15538ba
    │   │   ├── a3
    │   │   │   └── b6a4fe8d56757a22a78f8b632a21c84aece45c
    │   │   ├── ac
    │   │   │   └── 7f488bf1def89622dc301cc700c9c2bdf280bd
    │   │   ├── ad
    │   │   │   └── 1c52770b21b80b8f811dfd200b596a8d62cc5e
    │   │   ├── b1
    │   │   │   └── fb709d9bad7837803d6b510d009d4f79f2aca7
    │   │   ├── b5
    │   │   │   └── 9d7c481625dd418f8a8adc8e366377957393fe
    │   │   ├── b6
    │   │   │   └── 3733af90b7ed692e3e0acabab181b41f2a3839
    │   │   ├── b8
    │   │   │   └── bd051f5265321aa641043714e9dc04610a7fbb
    │   │   ├── bd
    │   │   │   └── 0091715095b6ed6c10b4576d49d04f3246d064
    │   │   ├── c0
    │   │   │   └── 5f25c7005ff2b33a37a0bb08dace0275473bcb
    │   │   ├── c4
    │   │   │   └── 0f104114893b818a01cf2ab0671deec3150fdf
    │   │   ├── c5
    │   │   │   └── e2e3517f0fb180aa5095f0e4b1109dbe865bc6
    │   │   ├── d5
    │   │   │   └── 8b7b221892c13249af7335953732d2f155867e
    │   │   ├── d7
    │   │   │   └── 70664a201500c387121a768919836d18372708
    │   │   ├── d9
    │   │   │   └── bc18f0e88e227828a50ebac8aa7c275737e3f0
    │   │   ├── db
    │   │   │   └── d7df7199b24e727086a12c2cc3ea3c4f70c096
    │   │   ├── dd
    │   │   │   └── e248f6f0c66a10fc774e875fdf56746eb2dfa4
    │   │   ├── de
    │   │   │   ├── 9249e269029e884f4b0603f6addd31b3d0ecac
    │   │   │   └── db69af6cc000e72d1dd9d582ffbcce602be5c0
    │   │   ├── e1
    │   │   │   ├── 6f1f6838ec9e242a97a7febb489735ffa06db8
    │   │   │   ├── ceb31b06b2f7079d93ac5b7e527016dd631d2c
    │   │   │   └── ee00bf10bd43ef825ccbe666df71fcbd9db71e
    │   │   ├── e5
    │   │   │   └── 2d0c1f8bf1e998a43d7280fd5cf8f433098c2b
    │   │   ├── e8
    │   │   │   ├── 13c7ea735bd91ed2afde414bc28c74f3717323
    │   │   │   └── 63b5bebe4fbd9a71adbf0c9d013db44aca79d6
    │   │   ├── ea
    │   │   │   └── d52e450006c71d58cd94a49433aca6310fffcc
    │   │   ├── ee
    │   │   │   ├── 45a3363ef33293357d393a33f854300384751c
    │   │   │   ├── 68d9df40e11e149a08b1e88e6e29e11499be7d
    │   │   │   └── 97a35bffbfdb4940c5088a840fa9e982d1d945
    │   │   ├── f3
    │   │   │   └── 3d43c8b9b30a1bfdfec520cddc7f3e8d9ae3a8
    │   │   ├── f5
    │   │   │   └── 7ab7bbf23dd8251a27be234f6c5b435629a28f
    │   │   ├── info
    │   │   │   └── commit-graphs
    │   │   │       ├── commit-graph-chain
    │   │   │       └── graph-35216276634c05ea2bb03099ed929ef03d3de423.graph
    │   │   └── pack
    │   ├── refs
    │   │   ├── heads
    │   │   │   └── master
    │   │   └── tags
    │   ├── COMMIT_EDITMSG
    │   ├── config
    │   ├── description
    │   ├── HEAD
    │   └── index
    ├── gantt-planner
    │   ├── gantt-planner.xlsm
    │   ├── modGanttCriticalPath.bas
    │   └── README.md
    ├── pz1
    │   ├── img
    │   │   ├── risk_map.png
    │   │   └── stakeholder_quadrant.png
    │   ├── checklist.md
    │   ├── instructions.md
    │   ├── plan.md
    │   ├── report.docx
    │   ├── report.md
    │   └── summary.md
    ├── pz4
    │   ├── img
    │   │   ├── cpm_table.csv
    │   │   ├── gantt_critical_path.png
    │   │   └── network_diagram.png
    │   ├── calc_and_charts.py
    │   ├── checklist.md
    │   ├── instructions.md
    │   ├── plan.md
    │   ├── report.docx
    │   ├── report.md
    │   └── summary.md
    ├── risk-map
    │   ├── modRiskMap.bas
    │   ├── README.md
    │   ├── risk-map.xlsm
    │   └── risk_map.png
    ├── tasks
    │   ├── theory
    │   │   ├── Кто такие стейкхолдеры (6).docx
    │   │   ├── Тема 2 УРПО (5).pptx
    │   │   ├── Тема 3 Модели процесса разработки ПО 08.06 (4).pptx
    │   │   ├── УП тема 1 2024 (5).pptx
    │   │   ├── УП Тема 2 24 (5).ppt
    │   │   ├── Управление рисками - 2026 (3).pptx
    │   │   └── Что такое SMART (6).docx
    │   └── to do
    │       ├── Карта рисков в Excel_с форматированием -26 (3).xlsx
    │       ├── Планировщик проекта на основе диаграммы Ганта - 60121 (3).xlsx
    │       ├── УП-ПЗ1-60121 (3).pptx
    │       └── шаблон пз1 -УП- 26 (4).docx
    ├── tasks.md
    │   ├── theory
    │   │   ├── SMART-цели.md
    │   │   ├── Кто такие стейкхолдеры (6).docx
    │   │   ├── Стейкхолдеры проекта.md
    │   │   ├── Тема 1. Введение в управление проектами.md
    │   │   ├── Тема 2 УРПО (5).pptx
    │   │   ├── Тема 2. Жизненный цикл разработки ПО.md
    │   │   ├── Тема 3 Модели процесса разработки ПО 08.06 (4).pptx
    │   │   ├── Тема 3. Классические методологии разработки ПО.md
    │   │   ├── УП тема 1 2024 (5).pptx
    │   │   ├── УП Тема 2 24 (5).ppt
    │   │   ├── Управление рисками - 2026 (3).pptx
    │   │   ├── Управление рисками проекта.md
    │   │   └── Что такое SMART (6).docx
    │   └── to do
    │       ├── Инструмент — Карта рисков в Excel.md
    │       ├── Инструмент — Планировщик проекта (диаграмма Ганта).md
    │       ├── Карта рисков в Excel_с форматированием -26 (3).xlsx
    │       ├── ПЗ1. Шаблон отчёта — Разработка концепции проекта.md
    │       ├── ПЗ4. Диаграмма Ганта и сетевое планирование — задание.md
    │       ├── Планировщик проекта на основе диаграммы Ганта - 60121 (3).xlsx
    │       ├── УП-ПЗ1-60121 (3).pptx
    │       └── шаблон пз1 -УП- 26 (4).docx
    ├── theory
    │   ├── SMART-цели.md
    │   ├── Кто такие стейкхолдеры (6).docx
    │   ├── Стейкхолдеры проекта.md
    │   ├── Тема 1. Введение в управление проектами.md
    │   ├── Тема 2 УРПО (5).pptx
    │   ├── Тема 2. Жизненный цикл разработки ПО.md
    │   ├── Тема 3 Модели процесса разработки ПО 08.06 (4).pptx
    │   ├── Тема 3. Классические методологии разработки ПО.md
    │   ├── УП тема 1 2024 (5).pptx
    │   ├── УП Тема 2 24 (5).ppt
    │   ├── Управление рисками - 2026 (3).pptx
    │   ├── Управление рисками проекта.md
    │   └── Что такое SMART (6).docx
    ├── to do
    │   ├── Инструмент — Карта рисков в Excel.md
    │   ├── Инструмент — Планировщик проекта (диаграмма Ганта).md
    │   ├── Карта рисков в Excel_с форматированием -26 (3).xlsx
    │   ├── ПЗ1. Шаблон отчёта — Разработка концепции проекта.md
    │   ├── ПЗ4. Диаграмма Ганта и сетевое планирование — задание.md
    │   ├── Планировщик проекта на основе диаграммы Ганта - 60121 (3).xlsx
    │   ├── УП-ПЗ1-60121 (3).pptx
    │   └── шаблон пз1 -УП- 26 (4).docx
    ├── analyze_architecture.py
    ├── ARCHITECTURE.md
    ├── CHECKLIST-1-ALL-TASKS.md
    ├── CHECKLIST-2-SOURCE-REQUIREMENTS.md
    ├── CHECKLIST-3-CLAUDE-ASSISTANCE.md
    ├── LICENSE
    ├── PROJECT_ARCHITECTURE_ANALYSIS.md
    ├── README.md
    └── risk-management-sheets
```

## Пустые директории

- `.git\objects\pack`
- `.git\refs\tags`

*Анализ выполнен с помощью Python скрипта analyze_architecture.py*
