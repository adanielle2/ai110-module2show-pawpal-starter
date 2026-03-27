# 🐾 PawPal+

**PawPal+** is a Streamlit app that helps a busy pet owner stay consistent with daily pet care. Enter your pet's info, add care tasks, and let the scheduler build an intelligent daily plan — complete with explanations for every decision it makes.

---

## 📸 Demo

<a href="/course_images/ai110/pawpal_screenshot.png" target="_blank"><img src='/course_images/ai110/pawpal_screenshot.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

---

## ✨ Features

- **Priority-based scheduling** — Tasks are ranked HIGH → MEDIUM → LOW. Within each priority tier, tasks with the earliest deadlines are always placed first.
- **Sorting by deadline** — The task list in the UI is sorted by `deadline_hour` using a `lambda` key so the most time-critical tasks appear at the top.
- **Filtering by pet or status** — View only Mochi's tasks, only completed tasks, or only tasks in a specific category — without getting everything back at once.
- **Conflict warnings** — Before generating the plan, the scheduler scans for tasks that share the same deadline window or whose projected start time would already exceed their deadline. Warnings are surfaced in the UI as `st.warning` banners, never crashes.
- **Daily recurrence** — Marking a `"daily"` task complete automatically creates the next occurrence scheduled for tomorrow using Python's `timedelta`. Weekly tasks reschedule one week out. One-off tasks simply stop.
- **Skipped task reporting** — Any task that doesn't fit in the owner's available time budget is collected and shown in a collapsible section at the bottom of the plan.
- **Explainable plan** — Every scheduled slot includes a plain-English reason (e.g. "High priority and time-sensitive; must start before 9:00") so the owner always knows why a task was placed when it was.

---

## 🏗 Architecture

The system is split into a logic layer (`pawpal_system.py`) and a UI layer (`app.py`).

| Class | Role |
|---|---|
| `Task` | A single care item with duration, priority, deadline, frequency, and completion status |
| `Pet` | Holds a pet's profile and its task list; handles task completion and recurrence |
| `Owner` | Groups multiple pets; provides flat and filtered views of all tasks |
| `Scheduler` | The brain — retrieves tasks from the owner, sorts, detects conflicts, and builds the plan |
| `DailyPlan` | The output: ordered slots, total time used, skipped tasks, and conflict warnings |
| `PlanSlot` | A scheduled task paired with a start time and a reason string |

The final UML diagram is in `uml_final.md` (open in Cursor Markdown preview or paste into [mermaid.live](https://mermaid.live)).

---

## 🚀 Getting started

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 🧪 Testing PawPal+

```bash
python3 -m pytest tests/ -v
```

14 tests cover:

- Task behavior (mark complete, add, remove)
- Recurring tasks (daily → tomorrow, weekly → next week, once → stops)
- Sorting (`sort_by_time()` returns tasks in deadline order)
- Scheduling logic (priority order, budget enforcement, completed tasks excluded)
- Conflict detection (overlap warning for shared deadlines, no false positives)
- Edge cases (empty pet, all tasks over budget, mix of done and pending)

**Confidence level: ★★★★☆**
All core behaviors are verified. The one remaining gap is that `frequency="weekly"` schedules on Mondays only rather than exactly 7 days from last completion — it works, but could use more tests on non-Monday days.

---

## 🔁 Smarter Scheduling

PawPal+ uses four algorithms to go beyond a plain to-do list:

**1. Priority + deadline sort** — `_sort_by_priority()` uses a two-key `lambda`: priority value first, then `deadline_hour` (with `999` as a sentinel for tasks with no deadline). This means a HIGH-priority task due at 8 AM always beats one due at noon.

**2. Filtering** — `Scheduler` exposes `sort_by_time()`, `filter_by_status()`, and `filter_by_pet()`. `Owner` exposes `get_tasks_by_pet()`, `get_tasks_by_status()`, and `get_tasks_by_category()`.

**3. Recurring tasks** — `Task.next_occurrence()` uses `timedelta(days=1)` or `timedelta(weeks=1)` to compute the next due date. `Pet.complete_task()` calls it automatically and appends the result.

**4. Conflict detection** — `_detect_conflicts()` uses a `defaultdict(list)` to group tasks by `deadline_hour`. Any group with 2+ tasks gets an overlap warning. A second pass checks projected start times against deadlines.
