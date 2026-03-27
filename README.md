# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

Run the full test suite with:

```bash
python3 -m pytest tests/ -v
```

The suite has 14 tests covering:

- **Task behavior** — marking complete, adding to a pet, removing by title
- **Recurring tasks** — daily tasks reschedule for tomorrow, weekly for next week, one-off tasks stop after completion
- **Sorting** — `sort_by_time()` returns tasks in deadline order (earliest first, no-deadline tasks last)
- **Scheduling logic** — HIGH priority tasks are always placed before LOW, time budget is respected, completed tasks are excluded
- **Conflict detection** — two tasks sharing a deadline hour trigger an overlap warning; a single time-sensitive task produces no false positive
- **Edge cases** — pet with no tasks, all tasks over budget, mix of completed and pending

**Confidence level: ★★★★☆**
The core scheduling behaviors are all verified. The one gap is that `frequency="weekly"` uses day-of-week (Monday only) rather than a true 7-day interval from last completion — that logic works but could use a few more tests around non-Monday runs before I'd call it fully reliable.

---

## Smarter Scheduling

PawPal+ goes beyond a simple to-do list. The scheduler includes four pieces of algorithmic intelligence:

**Sorting by deadline**
Tasks are sorted by priority first (HIGH before MEDIUM before LOW), then by `deadline_hour` within each tier so the most urgent task in a group always schedules first.

**Filtering**
The `Scheduler` exposes `sort_by_time()`, `filter_by_status()`, and `filter_by_pet()` methods. `Owner` also provides `get_tasks_by_pet()`, `get_tasks_by_status()`, and `get_tasks_by_category()` so the UI can show targeted views without returning everything.

**Recurring tasks**
Each `Task` has a `frequency` field (`"daily"`, `"weekly"`, or `"once"`). When `Pet.complete_task()` is called, it marks the task done and automatically appends the next occurrence with a new `due_date` calculated using `timedelta`. One-off tasks are not repeated.

**Conflict detection**
Before building the plan, `_detect_conflicts()` scans for two types of problems: tasks that share the same `deadline_hour` (potential overlap) and tasks whose projected start time already exceeds their deadline. Conflicts are collected as warning strings and shown at the top of the plan — the scheduler never crashes, it just tells you what to watch out for.
