from pawpal_system import Owner, Pet, Task, Priority, Scheduler

mochi = Pet(name="Mochi", species="dog", age=3)
mochi.add_task(Task(title="Grooming brush",   duration_minutes=15, priority=Priority.MEDIUM, category="grooming"))
mochi.add_task(Task(title="Morning walk",     duration_minutes=30, priority=Priority.HIGH,   category="exercise"))
mochi.add_task(Task(title="Breakfast feeding",duration_minutes=10, priority=Priority.HIGH,   category="feeding", deadline_hour=9))

luna = Pet(name="Luna", species="cat", age=5)
luna.add_task(Task(title="Playtime",        duration_minutes=20, priority=Priority.LOW,  category="enrichment"))
luna.add_task(Task(title="Medication dose", duration_minutes=5,  priority=Priority.HIGH, category="meds",    deadline_hour=8))
luna.add_task(Task(title="Evening feeding", duration_minutes=10, priority=Priority.HIGH, category="feeding", deadline_hour=18, completed=True))
luna.add_task(Task(title="Morning meds",    duration_minutes=5,  priority=Priority.HIGH, category="meds",    deadline_hour=8))

jordan = Owner(name="Jordan")
jordan.add_pet(mochi)
jordan.add_pet(luna)

scheduler = Scheduler(owner=jordan, available_minutes=90, day_start_hour=8)

# --- Sort by time ---
all_tasks = jordan.get_all_tasks()
sorted_by_time = scheduler.sort_by_time(all_tasks)
print("=" * 45)
print("  Tasks sorted by deadline (earliest first)")
print("=" * 45)
for t in sorted_by_time:
    deadline = f"by {t.deadline_hour}:00" if t.deadline_hour else "no deadline"
    print(f"  {t.title:<22} {deadline}")

# --- Filter by status ---
print()
print("=" * 45)
print("  Pending tasks (not yet completed)")
print("=" * 45)
for t in scheduler.filter_by_status(completed=False):
    print(f"  {t.title}")

print()
print("=" * 45)
print("  Completed tasks")
print("=" * 45)
completed = scheduler.filter_by_status(completed=True)
if completed:
    for t in completed:
        print(f"  {t.title}")
else:
    print("  None")

# --- Filter by pet ---
print()
print("=" * 45)
print("  Mochi's tasks only")
print("=" * 45)
for t in scheduler.filter_by_pet("Mochi"):
    print(f"  {t.title}")

# --- Full schedule ---
print()
print("=" * 45)
print("       🐾 PawPal+ — Today's Schedule")
print("=" * 45)
plan = scheduler.generate_plan()
print(plan.summary())
print("=" * 45)
