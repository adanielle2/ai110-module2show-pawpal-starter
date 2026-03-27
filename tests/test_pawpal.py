from datetime import date, timedelta
from pawpal_system import Pet, Task, Priority


def make_task(title="Morning walk", minutes=30, priority=Priority.MEDIUM, frequency="daily"):
    return Task(title=title, duration_minutes=minutes, priority=priority, category="exercise", frequency=frequency)


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
