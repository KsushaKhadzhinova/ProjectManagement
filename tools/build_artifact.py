# -*- coding: utf-8 -*-
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "pz-wbs-gantt", "WBS-диаграмма-DiagramCode.png"), "rb") as f:
    WBS_B64 = base64.b64encode(f.read()).decode("ascii")

HTML = r"""<title>Разбор трёх практических</title>
<style>
:root{
  --bg:#F4F6FA; --surface:#FFFFFF; --surface-2:#ECEFF7;
  --ink:#1B2130; --muted:#5B6478; --border:#DCE1EE;
  --primary:#1E2761; --primary-soft:#E7EAF6;
  --accent:#C2622E; --accent-soft:#F5E4DA;
  --ok:#2F7A63; --ok-soft:#DFEFE9;
  --warn:#B08900; --warn-soft:#F5EED2;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#12141C; --surface:#191C28; --surface-2:#20243380;
    --ink:#E8EAF2; --muted:#A0A8C0; --border:#2B2F44;
    --primary:#95A4FF; --primary-soft:#232849;
    --accent:#E2916A; --accent-soft:#3A2A22;
    --ok:#5FBFA0; --ok-soft:#1E332C;
    --warn:#E0C25E; --warn-soft:#332C15;
  }
}
:root[data-theme="dark"]{
  --bg:#12141C; --surface:#191C28; --surface-2:#20243380;
  --ink:#E8EAF2; --muted:#A0A8C0; --border:#2B2F44;
  --primary:#95A4FF; --primary-soft:#232849;
  --accent:#E2916A; --accent-soft:#3A2A22;
  --ok:#5FBFA0; --ok-soft:#1E332C;
  --warn:#E0C25E; --warn-soft:#332C15;
}
*{box-sizing:border-box;}
body{background:var(--bg); color:var(--ink); margin:0; font-family:'Public Sans',system-ui,sans-serif;
  padding-inline:16px; padding-block:0;}
.wrap{max-width:880px; margin:0 auto; padding-block:28px 80px;}
h1,h2,h3{font-family:'Fraunces',Georgia,serif; text-wrap:balance; color:var(--ink); font-weight:600;}
h1{font-size:clamp(1.7rem,4vw,2.5rem); line-height:1.15; margin:0 0 6px;}
h2{font-size:clamp(1.3rem,3vw,1.7rem); margin:0 0 4px;}
h3{font-size:1.05rem; margin:0 0 8px; color:var(--primary);}
p{line-height:1.65; max-width:65ch; margin:0 0 14px; color:var(--ink);}
.lede{color:var(--muted); font-size:1.05rem; max-width:62ch;}
.mono{font-family:'IBM Plex Mono',monospace; font-variant-numeric:tabular-nums;}
a{color:var(--primary);}
.topbar{position:sticky; top:env(safe-area-inset-top,0px); z-index:20; background:color-mix(in srgb, var(--bg) 88%, transparent);
  backdrop-filter:blur(6px); border-bottom:1px solid var(--border); margin:0 -16px; padding:10px 16px;}
.pills{display:flex; gap:8px; max-width:880px; margin:0 auto; overflow-x:auto; padding-block:2px;}
.pill{flex:none; font-family:'IBM Plex Mono',monospace; font-size:12.5px; letter-spacing:.02em;
  padding:7px 12px; border-radius:999px; background:var(--surface-2); color:var(--muted);
  border:1px solid var(--border); text-decoration:none; white-space:nowrap;}
.pill.active{background:var(--primary); color:#fff; border-color:var(--primary);}
.hero{padding-block:26px 8px;}
.eyebrow{font-family:'IBM Plex Mono',monospace; font-size:12px; letter-spacing:.08em; text-transform:uppercase;
  color:var(--accent); margin:0 0 10px;}
.section{margin-top:56px; padding-top:8px; border-top:1px solid var(--border);}
.section-head{display:flex; align-items:baseline; gap:12px; flex-wrap:wrap; margin-bottom:6px;}
.badge{font-family:'IBM Plex Mono',monospace; font-size:12px; background:var(--primary-soft); color:var(--primary);
  padding:3px 9px; border-radius:6px; border:1px solid var(--border);}
.grid2{display:grid; grid-template-columns:1fr 1fr; gap:16px;}
@media (max-width:640px){.grid2{grid-template-columns:1fr;}}
.card{background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:16px 18px; margin-bottom:14px;}
.card h4{margin:0 0 8px; font-size:.95rem; font-family:'Public Sans',sans-serif; font-weight:700; color:var(--ink);}
.theory-card{background:var(--primary-soft); border:1px solid var(--border); border-radius:12px; padding:16px 18px; margin-bottom:14px;}
.theory-card h4{color:var(--primary); margin:0 0 6px; font-size:.85rem; font-family:'IBM Plex Mono',monospace;
  text-transform:uppercase; letter-spacing:.04em;}
ul.clean{margin:0 0 14px; padding-left:1.1em;}
ul.clean li{margin-bottom:6px; line-height:1.55; max-width:62ch;}
table{width:100%; border-collapse:collapse; margin:14px 0 20px; font-size:13.5px;}
th,td{border:1px solid var(--border); padding:7px 9px; text-align:left; vertical-align:top;}
th{background:var(--surface-2); font-family:'IBM Plex Mono',monospace; font-size:11.5px; text-transform:uppercase; letter-spacing:.02em; color:var(--muted);}
td.num, th.num{text-align:right; font-family:'IBM Plex Mono',monospace;}
.crit-row td{background:color-mix(in srgb, var(--accent-soft) 70%, transparent);}
.tablewrap{overflow-x:auto;}
figure{margin:22px 0; padding:0;}
figcaption{font-size:12.5px; color:var(--muted); margin-top:8px; text-align:center;}
.figure-frame{background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:14px;}
.legend{display:flex; gap:18px; flex-wrap:wrap; font-size:12.5px; color:var(--muted); margin-top:10px; justify-content:center;}
.legend span{display:inline-flex; align-items:center; gap:6px;}
.dot{width:10px; height:10px; border-radius:3px; display:inline-block;}
.note{font-size:13px; color:var(--muted); border-left:3px solid var(--accent); padding:8px 12px; background:var(--accent-soft);
  border-radius:0 8px 8px 0; margin:14px 0;}
.tag{font-family:'IBM Plex Mono',monospace; font-size:11px; padding:2px 7px; border-radius:5px; margin-right:4px;}
.tag.crit{background:var(--accent-soft); color:var(--accent);}
.tag.free{background:var(--ok-soft); color:var(--ok);}
footer{margin-top:60px; padding-top:20px; border-top:1px solid var(--border); color:var(--muted); font-size:13px;}
svg text{font-family:'IBM Plex Mono',monospace;}
svg .lbl{font-family:'Public Sans',sans-serif;}
</style>

<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Public+Sans:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">

<div class="topbar">
  <nav class="pills" id="nav">
    <a class="pill" href="#intro">Контекст</a>
    <a class="pill" href="#pz1">ПЗ1 · Концепция</a>
    <a class="pill" href="#pz2">ПЗ2 · WBS + Гант</a>
    <a class="pill" href="#pz3">ПЗ3 · Риски</a>
  </nav>
</div>

<div class="wrap">

  <section class="hero" id="intro">
    <p class="eyebrow">Управление проектами · гр. 60121 · разбор выполненного</p>
    <h1>Что и как сделано по трём практическим занятиям</h1>
    <p class="lede">Подробный разбор теории и практики по всем трём заданиям — концепция проекта, WBS и график Ганта,
      управление рисками — на примере одного и того же реального проекта, <span class="mono">DiagramCode</span>.
      Каждый раздел объясняет метод, показывает, что именно посчитано, и даёт схему, которая визуализирует расчёт.</p>
    <div class="note">Диаграммы ниже — объясняющие иллюстрации для понимания метода, а не замена скриншотов из
      настоящего Excel: те по-прежнему нужно снять самой (см. отдельную инструкцию в репозитории) для сдачи задания.</div>
  </section>

  <!-- ================= ПЗ1 — КОНЦЕПЦИЯ ================= -->
  <section class="section" id="pz1">
    <div class="section-head"><span class="badge">ПЗ1</span><h2>Концепция проекта (Business Case)</h2></div>
    <p class="lede">Цель занятия — доказать, что проект вообще стоит делать: кто его закажет, зачем, что именно
      он должен сделать, и когда мы поймём, что он сделан.</p>

    <h3>Теория</h3>
    <div class="grid2">
      <div class="theory-card">
        <h4>5W · бизнес-обоснование</h4>
        <p>Пять вопросов, на которые отвечает любой бизнес-кейс: <b>What</b> — что делаем и какую проблему решаем;
          <b>Who</b> — для кого, кто заказчик; <b>Why</b> — почему это важно и почему именно сейчас;
          <b>When</b> — когда будет MVP и релиз; <b>Where</b> — где и на каких платформах это будет использоваться.
          Если хотя бы на один вопрос нет внятного ответа — концепция ещё не готова.</p>
      </div>
      <div class="theory-card">
        <h4>SMART · формулировка цели</h4>
        <p><b>S</b>pecific — конкретная, без двойных толкований. <b>M</b>easurable — измеримая, есть способ
          проверить достижение. <b>A</b>chievable — достижимая имеющимися ресурсами. <b>R</b>elevant — связана с
          более широкой целью, а не существует сама по себе. <b>T</b>ime bound — у неё есть срок. Все пять
          критериев склеиваются в одно предложение — итоговую цель проекта.</p>
      </div>
      <div class="theory-card">
        <h4>MoSCoW · приоритизация</h4>
        <p>Требования делятся на четыре корзины: <b>Must have</b> — без этого проект не имеет смысла;
          <b>Should have</b> — важно, но можно отложить; <b>Could have</b> — хорошо бы, если останутся
          ресурсы; <b>Won't have</b> — сознательно не делаем сейчас. Практическое правило: Must have не должно
          превышать 60% от общего списка — иначе это не приоритизация, а просто список желаний.</p>
      </div>
      <div class="theory-card">
        <h4>Матрица стейкхолдеров</h4>
        <p>Каждый, кто влияет на проект или зависит от него, получает две оценки от 1 до 5: <b>влияние</b>
          (способность реально повлиять на решения) и <b>заинтересованность</b> (насколько ему важен результат).
          Комбинация этих двух осей даёт 4 квадранта — и для каждого своя стратегия работы.</p>
      </div>
    </div>

    <h3>Что сделано для DiagramCode</h3>
    <p>Бизнес-обоснование по 5W: <span class="mono">DiagramCode</span> — сервис визуального моделирования
      диаграмм через собственный текстовый язык (<span class="mono">DSL</span>), с версионированием как в
      <span class="mono">git</span> и <span class="mono">AI</span>-генерацией. Заказчик курсового среза —
      защита курсовой работы; срок — дата защиты; целевая платформа — веб-приложение в браузере.</p>
    <p>Итоговая SMART-цель: <i>«к дате защиты курсовой работы реализовать и продемонстрировать веб-сервис
      DiagramCode в объёме курсового среза (DSL-редактор, рендер и валидация нотации ERD, версионирование,
      аутентификация), подтверждённый прохождением всех автотестов и работающим сквозным пользовательским
      сценарием»</i>.</p>
    <p>MoSCoW: 6 пунктов Must have из 15 требований общего списка — это 40%, укладывается в правило «не более 60%».
      Явно исключены (Won't have): BPMN и сети Петри, реальная облачная база данных для продакшена, интеграция с
      внешним AI-провайдером, администрирование пользователей.</p>

    <h4 style="margin-top:22px;">Иерархическая структура работ (WBS)</h4>
    <p>Цель раскладывается на 4 этапа и 12 конкретных работ — эта же декомпозиция используется дальше как основа
      для расчёта графика Ганта в ПЗ2.</p>
    <figure>
      <div class="figure-frame">
        <img src="data:image/png;base64,__WBS_B64__" alt="WBS-диаграмма DiagramCode" style="display:block; margin:0 auto; max-width:100%; height:auto;">
      </div>
      <figcaption>Рис. 1 — WBS-диаграмма: 4 этапа, 12 работ, курсовой срез проекта DiagramCode</figcaption>
    </figure>

    <h4>Матрица стейкхолдеров</h4>
    <p>Шесть стейкхолдеров распределены по матрице «влияние × заинтересованность»:</p>
    <figure>
      <div class="figure-frame">
        <svg viewBox="0 0 640 420" width="100%" style="max-width:640px; display:block; margin:0 auto;">
          <!-- axes -->
          <text x="20" y="18" class="lbl" font-size="12" fill="var(--muted)">Влияние</text>
          <text x="560" y="410" class="lbl" font-size="12" fill="var(--muted)">Заинтересованность →</text>
          <!-- quadrant backgrounds -->
          <rect x="70" y="30" width="255" height="170" fill="var(--warn-soft)"/>
          <rect x="325" y="30" width="255" height="170" fill="var(--accent-soft)"/>
          <rect x="70" y="200" width="255" height="170" fill="var(--surface-2)"/>
          <rect x="325" y="200" width="255" height="170" fill="var(--ok-soft)"/>
          <!-- grid lines -->
          <line x1="70" y1="30" x2="580" y2="30" stroke="var(--border)"/>
          <line x1="70" y1="200" x2="580" y2="200" stroke="var(--border)" stroke-width="1.5"/>
          <line x1="70" y1="370" x2="580" y2="370" stroke="var(--border)"/>
          <line x1="70" y1="30" x2="70" y2="370" stroke="var(--border)"/>
          <line x1="325" y1="30" x2="325" y2="370" stroke="var(--border)" stroke-width="1.5"/>
          <line x1="580" y1="30" x2="580" y2="370" stroke="var(--border)"/>
          <!-- quadrant labels -->
          <text x="82" y="48" class="lbl" font-size="12" font-weight="700" fill="var(--warn)">D · минимальное информирование</text>
          <text x="337" y="48" class="lbl" font-size="12" font-weight="700" fill="var(--accent)">A · активное вовлечение</text>
          <text x="82" y="218" class="lbl" font-size="12" font-weight="700" fill="var(--muted)">C · минимальный контроль</text>
          <text x="337" y="218" class="lbl" font-size="12" font-weight="700" fill="var(--ok)">B · консультирование</text>
          <!-- axis scale labels -->
          <text x="60" y="120" class="lbl" font-size="11" fill="var(--muted)" text-anchor="end">высокое</text>
          <text x="60" y="290" class="lbl" font-size="11" fill="var(--muted)" text-anchor="end">низкое</text>
          <text x="150" y="390" class="lbl" font-size="11" fill="var(--muted)" text-anchor="middle">низкая</text>
          <text x="450" y="390" class="lbl" font-size="11" fill="var(--muted)" text-anchor="middle">высокая</text>
          <!-- stakeholder chips -->
          <g font-size="12" class="lbl">
            <rect x="345" y="70" width="160" height="26" rx="13" fill="var(--surface)" stroke="var(--accent)"/>
            <text x="425" y="87" text-anchor="middle" fill="var(--ink)">Разработчица (Ксения)</text>
            <rect x="345" y="105" width="160" height="26" rx="13" fill="var(--surface)" stroke="var(--accent)"/>
            <text x="425" y="122" text-anchor="middle" fill="var(--ink)">Фоновые ИИ-агенты</text>

            <rect x="345" y="240" width="160" height="26" rx="13" fill="var(--surface)" stroke="var(--ok)"/>
            <text x="425" y="257" text-anchor="middle" fill="var(--ink)">Конечный пользователь</text>

            <rect x="90" y="240" width="160" height="26" rx="13" fill="var(--surface)" stroke="var(--muted)"/>
            <text x="170" y="257" text-anchor="middle" fill="var(--ink)">AI-провайдер</text>
            <rect x="90" y="275" width="160" height="26" rx="13" fill="var(--surface)" stroke="var(--muted)"/>
            <text x="170" y="292" text-anchor="middle" fill="var(--ink)">Хостинг-провайдеры</text>

            <rect x="90" y="70" width="160" height="26" rx="13" fill="var(--surface)" stroke="var(--warn)"/>
            <text x="170" y="87" text-anchor="middle" fill="var(--ink)">Руководитель курсовой</text>
          </g>
        </svg>
      </div>
      <figcaption>Рис. 2 — Матрица стейкхолдеров DiagramCode: влияние × заинтересованность, 4 квадранта стратегии</figcaption>
    </figure>
    <p class="note">Полностью заполненный документ (все 6 разделов официального шаблона концепции) —
      <span class="mono">pz1-concept/шаблон пз1 ... .docx</span> в репозитории; связный университетский отчёт с этим же
      материалом — <span class="mono">Отчёт - ПЗ1 - Концепция проекта.docx</span>.</p>
  </section>

  <!-- ================= ПЗ2 — WBS + ГАНТ ================= -->
  <section class="section" id="pz2">
    <div class="section-head"><span class="badge">ПЗ2</span><h2>WBS-диаграмма и график Ганта</h2></div>
    <p class="lede">Цель занятия — превратить список работ из ПЗ1 в календарный план: когда что можно начать,
      когда что должно закончиться, и какие работы вообще нельзя задерживать.</p>

    <h3>Теория: метод критического пути (CPM)</h3>
    <div class="theory-card">
      <h4>Прямой проход (слева направо)</h4>
      <p><span class="mono">ES</span> (Early Start, раннее начало) — самый ранний день, когда работа может
        начаться: если предшественников нет, <span class="mono">ES = 1</span>; если есть — <span class="mono">ES</span>
        равен наибольшему из <span class="mono">EF</span> всех предшественников (нужно, чтобы <b>все</b> они уже
        закончились). <span class="mono">EF</span> (Early Finish, ранний финиш) = <span class="mono">ES + D</span>,
        где <span class="mono">D</span> — длительность работы.</p>
    </div>
    <div class="theory-card">
      <h4>Обратный проход (справа налево)</h4>
      <p><span class="mono">LF</span> (Late Finish, поздний финиш) — самый поздний день, когда работа должна
        закончиться, не сдвигая весь проект: для последней работы <span class="mono">LF</span> = общая длительность
        проекта; для остальных — наименьший из <span class="mono">LS</span> всех работ-последователей (нельзя
        закончиться позже, чем нужно начаться следующей). <span class="mono">LS</span> (Late Start) =
        <span class="mono">LF − D</span>.</p>
    </div>
    <div class="theory-card">
      <h4>Резерв и критический путь</h4>
      <p>Резерв (<span class="mono">TF</span>, total float) = <span class="mono">LS − ES</span> — насколько можно
        задержать работу, не сдвигая срок всего проекта. Работы с <span class="mono">TF = 0</span> задержать нельзя
        вообще — они образуют <b>критический путь</b>: самую длинную цепочку зависимых работ, которая и определяет
        минимальный срок проекта целиком.</p>
    </div>

    <h3>Практика: расчёт для DiagramCode</h3>
    <p>12 работ курсового среза посчитаны по методу выше. Результат — в таблице 1 и на диаграмме сети работ (рис. 3),
      где каждый узел устроен по классической схеме прецедентной диаграммы: <span class="mono">ES | D | EF</span>
      сверху, название работы посередине, <span class="mono">LS | TF | LF</span> снизу.</p>

    <div class="tablewrap">
    <table>
      <tr><th>№</th><th>Работа</th><th>Пред.</th><th class="num">D</th><th class="num">ES</th><th class="num">EF</th>
        <th class="num">LS</th><th class="num">LF</th><th class="num">Резерв</th><th>Крит.</th></tr>
      __GANTT_ROWS__
    </table>
    </div>

    <figure>
      <div class="figure-frame">
        __CPM_SVG__
      </div>
      <figcaption>Рис. 3 — Сетевая диаграмма проекта (precedence diagram): критический путь выделен оранжевым —
        1→2→4→6→8→10→11→12, общая длительность 38 рабочих дней</figcaption>
      <div class="legend">
        <span><i class="dot" style="background:var(--accent)"></i>критический путь (резерв = 0)</span>
        <span><i class="dot" style="background:var(--muted)"></i>есть резерв</span>
      </div>
    </figure>

    <h4>График Ганта</h4>
    <p>Тот же расчёт, но по оси времени: длина полосы — длительность работы, положение — с какого дня по какой
      день она идёт. В реальном файле полосы рисует условное форматирование Excel; ниже — та же картина,
      построенная по тем же числам для наглядности.</p>
    <figure>
      <div class="figure-frame">
        __GANTT_SVG__
      </div>
      <figcaption>Рис. 4 — График Ганта: 38 рабочих дней, 12 работ, критический путь — сплошные оранжевые полосы</figcaption>
    </figure>

    <div class="note">Задание на LMS буквально просит воспроизвести пример из методички («Обучение сотрудников
      кибербезопасности», критический путь 1→2→3→6→8→9→10→11→12, 56 дней) — этот вариант тоже полностью посчитан и
      лежит в репозитории (<span class="mono">Планировщик проекта - Пример 1 (методичка).xlsx</span>), просто не
      разбирается здесь подробно, чтобы не дублировать одну и ту же теорию дважды.</div>
  </section>

  <!-- ================= ПЗ3 — РИСКИ ================= -->
  <section class="section" id="pz3">
    <div class="section-head"><span class="badge">ПЗ3</span><h2>Управление рисками проекта</h2></div>
    <p class="lede">Цель занятия — заранее найти, что может пойти не так, оценить, насколько это вероятно и насколько
      больно ударит, и решить, что с этим делать до того, как оно случится.</p>

    <h3>Теория</h3>
    <div class="grid2">
      <div class="theory-card">
        <h4>Риск vs проблема</h4>
        <p>Риск — неопределённое событие, которое <i>может</i> повлиять на цели проекта. Как только оно
          происходит — это уже не риск, а проблема. Управление рисками работает <i>до</i> того, как риск
          реализовался.</p>
      </div>
      <div class="theory-card">
        <h4>6 процедур PMBOK</h4>
        <p>Планирование управления рисками → идентификация рисков → качественная оценка → количественная
          оценка → планирование реагирования → мониторинг и контроль. Мы прошли идентификацию и качественную
          оценку в явном виде.</p>
      </div>
      <div class="theory-card">
        <h4>Качественная оценка</h4>
        <p>Каждому риску присваивается вероятность возникновения (<span class="mono">F</span>, от 0 до 1) и сила
          воздействия на проект (<span class="mono">G</span>, от 0 до 1). Итоговый коэффициент приоритета —
          <span class="mono">H = F × G</span>: чем выше, тем раньше нужно этим заняться.</p>
      </div>
      <div class="theory-card">
        <h4>4 стратегии реагирования</h4>
        <p><b>Уклонение</b> — убрать источник риска целиком. <b>Передача</b> — переложить последствия на
          третью сторону (страховка, договор). <b>Снижение</b> — уменьшить вероятность и/или воздействие.
          <b>Принятие</b> — осознанно ничего не менять, но быть готовыми покрыть последствия.</p>
      </div>
    </div>

    <h3>Практика: реестр рисков DiagramCode</h3>
    <p>Девять рисков, упорядоченных по убыванию коэффициента <span class="mono">H</span> — так самые срочные
      идут первыми.</p>
    <div class="tablewrap">
    <table>
      <tr><th>№</th><th>Риск</th><th class="num">F</th><th class="num">G</th><th class="num">H=F×G</th></tr>
      __RISK_ROWS__
    </table>
    </div>

    <figure>
      <div class="figure-frame">
        __RISK_SVG__
      </div>
      <figcaption>Рис. 5 — Карта рисков: положение всех 9 рисков на матрице «вероятность × сила воздействия»;
        размер и цвет точки — величина коэффициента H</figcaption>
    </figure>
    <p>Два самых приоритетных риска (несмёрженные ветки разработки, H=0,45, и нереализованные обязательные
      нотации, H=0,42) обрабатываются стратегией <b>снижения</b>: ранний merge веток с прогоном тестов после
      каждого объединения, и резерв времени на доработку недостающих нотаций. Риск смещения даты защиты
      (H=0,10, самый низкий) обрабатывается стратегией <b>принятия</b> — с запасом времени в графике, но без
      специальных мер.</p>

    <div class="note">Диаграмма выше построена по тем же числам, что в файле <span class="mono">Карта рисков -
      DiagramCode.xlsx</span> — но встроенная диаграмма рассеяния Excel остаётся источником истины для сдачи
      задания; скриншот с неё нужен отдельно.</div>
  </section>

  <footer>
    Репозиторий: <a href="https://github.com/KsushaKhadzhinova/ProjectManagement">github.com/KsushaKhadzhinova/ProjectManagement</a>
    · Проект-основа: DiagramCode (VisualDSL-Platform)
  </footer>
</div>

<script>
try{
  const links=[...document.querySelectorAll('#nav .pill')];
  const targets=links.map(a=>document.querySelector(a.getAttribute('href')));
  const io=new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      if(e.isIntersecting){
        const idx=targets.indexOf(e.target);
        links.forEach(l=>l.classList.remove('active'));
        if(idx>=0) links[idx].classList.add('active');
      }
    });
  },{rootMargin:'-40% 0px -50% 0px'});
  targets.forEach(t=>t&&io.observe(t));
}catch(e){}
</script>
"""

HTML = HTML.replace("__WBS_B64__", WBS_B64)

# ---------- Gantt-style table rows (theory table, reuse CPM values) ----------
tasks = [
    (1, "Требования и архитектура", "—", 5, 1, 6, 1, 6, 0, True),
    (2, "DSL-грамматика, модель данных", "1", 4, 6, 10, 6, 10, 0, True),
    (3, "Окружение разработки и CI", "1", 2, 6, 8, 10, 12, 4, False),
    (4, "DSL-парсер (лексер, AST)", "2", 6, 10, 16, 10, 16, 0, True),
    (5, "Модель данных и репозитории", "2, 3", 5, 10, 15, 12, 17, 2, False),
    (6, "Нотация ERD: валидация, рендер", "4", 5, 16, 21, 16, 21, 0, True),
    (7, "Аутентификация (JWT, bcrypt)", "5", 4, 15, 19, 17, 21, 2, False),
    (8, "REST API диаграмм и версий", "6, 7", 6, 21, 27, 21, 27, 0, True),
    (9, "IDE-оболочка (React + Monaco)", "3", 7, 8, 15, 20, 27, 12, False),
    (10, "Канвас рендера, Run/Save/Export", "8, 9", 5, 27, 32, 27, 32, 0, True),
    (11, "Тестирование (pytest + Jest)", "10", 4, 32, 36, 32, 36, 0, True),
    (12, "Подготовка и защита курсовой", "11", 3, 36, 39, 36, 39, 0, True),
]

rows_html = []
for (num, name, pred, d, es, ef, ls, lf, tf, crit) in tasks:
    cls = ' class="crit-row"' if crit else ''
    crit_txt = "да" if crit else "нет"
    rows_html.append(
        f"<tr{cls}><td class='num'>{num}</td><td>{name}</td><td>{pred}</td>"
        f"<td class='num'>{d}</td><td class='num'>{es}</td><td class='num'>{ef}</td>"
        f"<td class='num'>{ls}</td><td class='num'>{lf}</td><td class='num'>{tf}</td><td>{crit_txt}</td></tr>"
    )
HTML = HTML.replace("__GANTT_ROWS__", "\n".join(rows_html))

# ---------- CPM network diagram (precedence diagram) SVG ----------
node_pos = {
    1: (90, 200), 2: (240, 90), 3: (240, 310),
    4: (390, 90), 5: (390, 200), 9: (390, 310),
    6: (540, 90), 7: (540, 200), 8: (690, 200),
    10: (840, 200), 11: (990, 200), 12: (1140, 200),
}
edges = [(1,2),(1,3),(2,4),(2,5),(3,5),(3,9),(4,6),(5,7),(6,8),(7,8),(8,10),(9,10),(10,11),(11,12)]
critical_edges = {(1,2),(2,4),(4,6),(6,8),(8,10),(10,11),(11,12)}
task_by_num = {t[0]: t for t in tasks}

BW, BH = 112, 76
svg_parts = ['<svg viewBox="0 0 1230 400" width="100%" style="min-width:900px;">']
svg_parts.append('<defs>'
                  '<marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
                  '<path d="M0,0 L8,4 L0,8 z" fill="var(--muted)"/></marker>'
                  '<marker id="arrowc" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
                  '<path d="M0,0 L8,4 L0,8 z" fill="var(--accent)"/></marker>'
                  '</defs>')

def edge_point(n, dx):
    cx, cy = node_pos[n]
    return cx + dx, cy

for (a, b) in edges:
    ax, ay = node_pos[a]; bx, by = node_pos[b]
    x1 = ax + BW/2; x2 = bx - BW/2
    is_crit = (a, b) in critical_edges
    stroke = 'var(--accent)' if is_crit else 'var(--muted)'
    marker = 'url(#arrowc)' if is_crit else 'url(#arrow)'
    width = 2.4 if is_crit else 1.4
    if ay == by:
        svg_parts.append(f'<line x1="{x1}" y1="{ay}" x2="{x2}" y2="{by}" stroke="{stroke}" stroke-width="{width}" marker-end="{marker}"/>')
    else:
        midx = (x1 + x2) / 2
        svg_parts.append(f'<path d="M{x1},{ay} C{midx},{ay} {midx},{by} {x2},{by}" fill="none" stroke="{stroke}" stroke-width="{width}" marker-end="{marker}"/>')

for num, (cx, cy) in node_pos.items():
    t = task_by_num[num]
    _, name, pred, d, es, ef, ls, lf, tf, crit = t
    x = cx - BW/2; y = cy - BH/2
    border = 'var(--accent)' if crit else 'var(--border)'
    bw_line = 2.4 if crit else 1.2
    head_fill = 'var(--accent-soft)' if crit else 'var(--surface-2)'
    short = name if len(name) <= 22 else name[:21] + '…'
    svg_parts.append(f'''
<g>
  <rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" fill="var(--surface)" stroke="{border}" stroke-width="{bw_line}"/>
  <rect x="{x}" y="{y}" width="{BW}" height="22" fill="{head_fill}"/>
  <line x1="{x}" y1="{y+22}" x2="{x+BW}" y2="{y+22}" stroke="{border}" stroke-width="1"/>
  <line x1="{x+BW/3}" y1="{y}" x2="{x+BW/3}" y2="{y+22}" stroke="{border}" stroke-width="0.7"/>
  <line x1="{x+2*BW/3}" y1="{y}" x2="{x+2*BW/3}" y2="{y+22}" stroke="{border}" stroke-width="0.7"/>
  <text x="{x+BW/6}" y="{y+15}" text-anchor="middle" font-size="10.5" fill="var(--ink)">{es}</text>
  <text x="{x+BW/2}" y="{y+15}" text-anchor="middle" font-size="10.5" fill="var(--ink)">{d}</text>
  <text x="{x+5*BW/6}" y="{y+15}" text-anchor="middle" font-size="10.5" fill="var(--ink)">{ef}</text>

  <text x="{cx}" y="{y+34}" text-anchor="middle" font-size="9.5" class="lbl" fill="var(--muted)">№{num}</text>
  <text x="{cx}" y="{y+47}" text-anchor="middle" font-size="9" class="lbl" fill="var(--ink)">{short}</text>

  <line x1="{x}" y1="{y+BH-22}" x2="{x+BW}" y2="{y+BH-22}" stroke="{border}" stroke-width="1"/>
  <line x1="{x+BW/3}" y1="{y+BH-22}" x2="{x+BW/3}" y2="{y+BH}" stroke="{border}" stroke-width="0.7"/>
  <line x1="{x+2*BW/3}" y1="{y+BH-22}" x2="{x+2*BW/3}" y2="{y+BH}" stroke="{border}" stroke-width="0.7"/>
  <text x="{x+BW/6}" y="{y+BH-8}" text-anchor="middle" font-size="10.5" fill="var(--ink)">{ls}</text>
  <text x="{x+BW/2}" y="{y+BH-8}" text-anchor="middle" font-size="10.5" fill="var(--ink)">{tf}</text>
  <text x="{x+5*BW/6}" y="{y+BH-8}" text-anchor="middle" font-size="10.5" fill="var(--ink)">{lf}</text>
</g>''')

svg_parts.append('<text x="8" y="14" font-size="9.5" fill="var(--muted)" class="lbl">ES | D | EF (сверху) &#183; LS | TF | LF (снизу)</text>')
svg_parts.append('</svg>')
CPM_SVG = "".join(svg_parts)
HTML = HTML.replace("__CPM_SVG__", CPM_SVG)

# ---------- Gantt bars SVG ----------
LABEL_W = 230
DAY_W = 18
ROW_H = 30
TOP = 34
duration = 38
chart_w = LABEL_W + duration * DAY_W + 20
chart_h = TOP + len(tasks) * ROW_H + 20

g_parts = [f'<svg viewBox="0 0 {chart_w} {chart_h}" width="100%" style="min-width:820px;">']
# day gridlines every 5 days
for day in range(0, duration + 1, 5):
    x = LABEL_W + day * DAY_W
    g_parts.append(f'<line x1="{x}" y1="{TOP-14}" x2="{x}" y2="{chart_h-10}" stroke="var(--border)" stroke-width="1"/>')
    g_parts.append(f'<text x="{x}" y="{TOP-20}" font-size="10" text-anchor="middle" fill="var(--muted)">{day}</text>')
g_parts.append(f'<text x="{LABEL_W + duration*DAY_W/2}" y="{chart_h-2}" font-size="10.5" text-anchor="middle" fill="var(--muted)" class="lbl">рабочие дни</text>')

for i, (num, name, pred, d, es, ef, ls, lf, tf, crit) in enumerate(tasks):
    y = TOP + i * ROW_H
    bx = LABEL_W + (es - 1) * DAY_W
    bw = d * DAY_W
    color = 'var(--accent)' if crit else 'var(--primary)'
    op = '1' if crit else '0.8'
    g_parts.append(f'<text x="4" y="{y+ROW_H/2+4}" font-size="10.5" class="lbl" fill="var(--ink)">{num}. {name}</text>')
    g_parts.append(f'<rect x="{bx}" y="{y+5}" width="{bw}" height="{ROW_H-12}" rx="4" fill="{color}" opacity="{op}"/>')
    g_parts.append(f'<text x="{bx+bw+6}" y="{y+ROW_H/2+4}" font-size="9.5" fill="var(--muted)" class="lbl">{d} дн.</text>')

g_parts.append('</svg>')
GANTT_SVG = "".join(g_parts)
HTML = HTML.replace("__GANTT_SVG__", GANTT_SVG)

# ---------- Risk table + matrix SVG ----------
risks = [
    (1, "Несмёрженные ветки разработки к дате защиты", 0.5, 0.9),
    (2, "Нотации uml.class и idef0 не реализованы к сроку", 0.6, 0.7),
    (3, "Качество кода фоновых ИИ-агентов при проверке", 0.5, 0.6),
    (4, "Разработчица перегружена/заболевает перед защитой", 0.3, 0.8),
    (5, "Смешение трёх обязательств в одном репозитории", 0.4, 0.6),
    (6, "Реальная БД Neon/Redis не проверена end-to-end", 0.4, 0.5),
    (7, "AI-провайдер остаётся в режиме заглушки", 0.6, 0.3),
    (8, "Хостинг-провайдер недоступен/меняет лимиты", 0.2, 0.7),
    (9, "Дата защиты курсовой смещается/уточняется поздно", 0.2, 0.5),
]
risk_rows_html = []
for (num, name, f, g) in risks:
    h = f * g
    risk_rows_html.append(
        f"<tr><td class='num'>{num}</td><td>{name}</td><td class='num'>{f:.1f}</td>"
        f"<td class='num'>{g:.1f}</td><td class='num'>{h:.2f}</td></tr>"
    )
HTML = HTML.replace("__RISK_ROWS__", "\n".join(risk_rows_html))

RM, RS = 60, 380  # margin, plot size
def risk_xy(f, g):
    return RM + f * RS, RM + RS - g * RS

r_parts = [f'<svg viewBox="0 0 {RM*2+RS} {RM*2+RS}" width="100%" style="max-width:520px; display:block; margin:0 auto;">']
r_parts.append(f'<rect x="{RM}" y="{RM}" width="{RS/2}" height="{RS/2}" fill="var(--surface-2)"/>')
r_parts.append(f'<rect x="{RM+RS/2}" y="{RM}" width="{RS/2}" height="{RS/2}" fill="var(--accent-soft)"/>')
r_parts.append(f'<rect x="{RM}" y="{RM+RS/2}" width="{RS/2}" height="{RS/2}" fill="var(--ok-soft)"/>')
r_parts.append(f'<rect x="{RM+RS/2}" y="{RM+RS/2}" width="{RS/2}" height="{RS/2}" fill="var(--warn-soft)"/>')
r_parts.append(f'<rect x="{RM}" y="{RM}" width="{RS}" height="{RS}" fill="none" stroke="var(--border)" stroke-width="1.5"/>')
for i in range(1, 4):
    x = RM + i * RS/4
    r_parts.append(f'<line x1="{x}" y1="{RM}" x2="{x}" y2="{RM+RS}" stroke="var(--border)" stroke-width="0.6" stroke-dasharray="3,3"/>')
    y = RM + i * RS/4
    r_parts.append(f'<line x1="{RM}" y1="{y}" x2="{RM+RS}" y2="{y}" stroke="var(--border)" stroke-width="0.6" stroke-dasharray="3,3"/>')
r_parts.append(f'<text x="{RM+RS/2}" y="{RM+RS+34}" text-anchor="middle" font-size="12" fill="var(--muted)" class="lbl">вероятность (F)</text>')
r_parts.append(f'<text x="18" y="{RM+RS/2}" text-anchor="middle" font-size="12" fill="var(--muted)" class="lbl" transform="rotate(-90 18 {RM+RS/2})">сила воздействия (G)</text>')
for v in [0, 0.5, 1]:
    x = RM + v * RS
    r_parts.append(f'<text x="{x}" y="{RM+RS+18}" text-anchor="middle" font-size="10" fill="var(--muted)">{v}</text>')
    y = RM + RS - v * RS
    r_parts.append(f'<text x="{RM-10}" y="{y+4}" text-anchor="end" font-size="10" fill="var(--muted)">{v}</text>')

for (num, name, f, g) in risks:
    h = f * g
    x, y = risk_xy(f, g)
    radius = 6 + h * 14
    color = 'var(--accent)' if h >= 0.35 else ('var(--warn)' if h >= 0.2 else 'var(--ok)')
    r_parts.append(f'<circle cx="{x}" cy="{y}" r="{radius:.1f}" fill="{color}" opacity="0.85" stroke="var(--surface)" stroke-width="1.5"/>')
    r_parts.append(f'<text x="{x}" y="{y+4}" text-anchor="middle" font-size="10" fill="var(--surface)" font-weight="700">{num}</text>')
r_parts.append('</svg>')
RISK_SVG = "".join(r_parts)
HTML = HTML.replace("__RISK_SVG__", RISK_SVG)

with open(os.path.join(HERE, "artifact_page.html"), "w", encoding="utf-8") as f:
    f.write(HTML)

print("built, length:", len(HTML))
