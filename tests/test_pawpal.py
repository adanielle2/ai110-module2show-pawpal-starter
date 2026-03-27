from pawpal_system import Pet, Task, Priority


def make_task(title="Morning walk", minutes=30, priority=Priority.MEDIUM):
    return Task(title=title, duration_minutes=minutes, priority=priority, category="exercise")


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
