from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Priority, Scheduler


def make_task(title="Morning walk", minutes=30, priority=Priority.MEDIUM, frequency="daily", deadline_hour=None):
    return Task(title=title, duration_minutes=minutes, priority=priority, category="exercise",
                frequency=frequency, deadline_hour=deadline_hour)


def make_scheduler(tasks, available_minutes=120, day_start_hour=8):
    pet = Pet(name="Mochi", species="dog", age=3)
    for t in tasks:
        pet.add_task(t)
    owner = Owner(name="Jordan")
    owner.add_pet(pet)
    return Scheduler(owner=owner, available_minutes=available_minutes, day_start_hour=day_start_hour)


# --- existing tests ---

def test_mark_complete_changes_status():
    task = make_task()
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.tasks) == 0
    pet.add_task(make_task("Morning walk"))
    pet.add_task(make_task("Evening feeding"))
    assert len(pet.tasks) == 2


def test_completing_daily_task_adds_next_occurrence():
    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_task(make_task("Morning walk", frequency="daily"))
    assert len(pet.tasks) == 1
    pet.complete_task("Morning walk")
    assert len(pet.tasks) == 2
    next_task = pet.tasks[1]
    assert next_task.completed is False
    assert next_task.due_date == date.today() + timedelta(days=1)


def test_completing_once_task_does_not_add_next_occurrence():
    pet = Pet(name="Luna", species="cat", age=2)
    pet.add_task(make_task("Vet visit", frequency="once"))
    pet.complete_task("Vet visit")
    assert len(pet.tasks) == 1
    assert pet.tasks[0].completed is True


def test_completing_weekly_task_adds_next_occurrence_one_week_later():
    pet = Pet(name="Luna", species="cat", age=2)
    pet.add_task(make_task("Bath time", frequency="weekly"))
    pet.complete_task("Bath time")
    assert len(pet.tasks) == 2
    assert pet.tasks[1].due_date == date.today() + timedelta(weeks=1)


# --- sorting correctness ---

def test_sort_by_time_orders_earliest_deadline_first():
    scheduler = make_scheduler([])
    tasks = [
        make_task("Late task",    deadline_hour=12),
        make_task("Early task",   deadline_hour=8),
        make_task("No deadline"),
        make_task("Mid task",     deadline_hour=10),
    ]
    result = scheduler.sort_by_time(tasks)
    deadlines = [t.deadline_hour if t.deadline_hour else 999 for t in result]
    assert deadlines == sorted(deadlines)


def test_generate_plan_schedules_high_priority_before_low():
    low  = make_task("Playtime",      minutes=20, priority=Priority.LOW)
    high = make_task("Morning walk",  minutes=20, priority=Priority.HIGH)
    scheduler = make_scheduler([low, high])
    plan = scheduler.generate_plan()
    assert plan.slots[0].task.title == "Morning walk"
    assert plan.slots[1].task.title == "Playtime"


# --- recurrence logic ---

def test_next_occurrence_daily_is_tomorrow():
    task = make_task(frequency="daily")
    next_t = task.next_occurrence()
    assert next_t is not None
    assert next_t.due_date == date.today() + timedelta(days=1)
    assert next_t.completed is False


def test_next_occurrence_once_returns_none():
    task = make_task(frequency="once")
    assert task.next_occurrence() is None


# --- conflict detection ---

def test_conflict_detected_for_two_tasks_with_same_deadline():
    t1 = make_task("Meds",     minutes=5, priority=Priority.HIGH, deadline_hour=9)
    t2 = make_task("Feeding",  minutes=5, priority=Priority.HIGH, deadline_hour=9)
    scheduler = make_scheduler([t1, t2])
    plan = scheduler.generate_plan()
    assert any("Overlap" in c for c in plan.conflicts)


def test_no_conflict_for_single_time_sensitive_task():
    t = make_task("Meds", minutes=5, priority=Priority.HIGH, deadline_hour=9)
    scheduler = make_scheduler([t])
    plan = scheduler.generate_plan()
    overlap_conflicts = [c for c in plan.conflicts if "Overlap" in c]
    assert len(overlap_conflicts) == 0


# --- edge cases ---

def test_pet_with_no_tasks_produces_empty_plan():
    scheduler = make_scheduler([])
    plan = scheduler.generate_plan()
    assert plan.slots == []
    assert plan.skipped_tasks == []
    assert plan.total_minutes_used == 0


def test_tasks_over_budget_are_skipped():
    t1 = make_task("Long task 1", minutes=70, priority=Priority.HIGH)
    t2 = make_task("Long task 2", minutes=70, priority=Priority.MEDIUM)
    scheduler = make_scheduler([t1, t2], available_minutes=90)
    plan = scheduler.generate_plan()
    assert len(plan.slots) == 1
    assert len(plan.skipped_tasks) == 1


def test_completed_tasks_excluded_from_plan():
    done = make_task("Already done", minutes=10, priority=Priority.HIGH)
    done.mark_complete()
    pending = make_task("Still todo", minutes=10, priority=Priority.MEDIUM)
    scheduler = make_scheduler([done, pending])
    plan = scheduler.generate_plan()
    scheduled_titles = [s.task.title for s in plan.slots]
    assert "Already done" not in scheduled_titles
    assert "Still todo" in scheduled_titles
