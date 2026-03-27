from pawpal_system import Owner, Pet, Task, Priority, Scheduler

mochi = Pet(name="Mochi", species="dog", age=3)
mochi.add_task(Task(title="Morning walk", duration_minutes=30, priority=Priority.HIGH, category="exercise"))
mochi.add_task(Task(title="Breakfast feeding", duration_minutes=10, priority=Priority.HIGH, category="feeding", deadline_hour=9))
mochi.add_task(Task(title="Grooming brush", duration_minutes=15, priority=Priority.MEDIUM, category="grooming"))

luna = Pet(name="Luna", species="cat", age=5)
luna.add_task(Task(title="Medication dose", duration_minutes=5, priority=Priority.HIGH, category="meds", deadline_hour=8))
luna.add_task(Task(title="Playtime", duration_minutes=20, priority=Priority.LOW, category="enrichment"))

jordan = Owner(name="Jordan")
jordan.add_pet(mochi)
jordan.add_pet(luna)

scheduler = Scheduler(owner=jordan, available_minutes=90, day_start_hour=8)
plan = scheduler.generate_plan()

print("=" * 45)
print("        🐾 PawPal+ — Today's Schedule")
print("=" * 45)
print(plan.summary())
print("=" * 45)
