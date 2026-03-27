from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import IntEnum
from typing import Optional


class Priority(IntEnum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Priority
    category: str
    deadline_hour: Optional[int] = None
    frequency: str = "daily"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def is_time_sensitive(self) -> bool:
        """Return True if this task has a hard deadline constraint."""
        return self.deadline_hour is not None

    def mark_complete(self) -> None:
        """Mark this task as done so the scheduler knows to skip it."""
        self.completed = True

    def should_run_today(self, today: date) -> bool:
        """Return True if this task is due to run on the given date based on its frequency."""
        if self.frequency == "once":
            return not self.completed
        if self.frequency == "weekly":
            return today.weekday() == 0
        return True

    def next_occurrence(self) -> Optional[Task]:
        """Return a fresh copy of this task scheduled for its next due date, or None if it only runs once."""
        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(weeks=1)
        else:
            return None
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            deadline_hour=self.deadline_hour,
            frequency=self.frequency,
            completed=False,
            due_date=next_date,
        )


@dataclass
class Pet:
    name: str
    species: str
    age: int
    notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove a task from this pet's list by its title."""
        self.tasks = [t for t in self.tasks if t.title != title]

    def complete_task(self, title: str) -> Optional[Task]:
        """Mark a task complete and, if it recurs, automatically add the next occurrence to this pet's list."""
        for task in self.tasks:
            if task.title == title and not task.completed:
                task.mark_complete()
                next_task = task.next_occurrence()
                if next_task:
                    self.tasks.append(next_task)
                return next_task
        return None


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's household."""
        self.pets.append(pet)

    def get_all_pets(self) -> list[Pet]:
        """Return a copy of the owner's pet list."""
        return list(self.pets)

    def get_all_tasks(self) -> list[Task]:
        """Collect and return every task across all of this owner's pets."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

    def get_tasks_by_pet(self, pet_name: str) -> list[Task]:
        """Return all tasks belonging to the pet with the given name."""
        for pet in self.pets:
            if pet.name == pet_name:
                return list(pet.tasks)
        return []

    def get_tasks_by_status(self, completed: bool) -> list[Task]:
        """Return all tasks that match the given completion status."""
        return [t for t in self.get_all_tasks() if t.completed == completed]

    def get_tasks_by_category(self, category: str) -> list[Task]:
        """Return all tasks that belong to the given category."""
        return [t for t in self.get_all_tasks() if t.category == category]


@dataclass
class PlanSlot:
    task: Task
    start_time: str
    reason: str


@dataclass
class DailyPlan:
    plan_date: date = field(default_factory=date.today)
    slots: list[PlanSlot] = field(default_factory=list)
    total_minutes_used: int = 0
    skipped_tasks: list[Task] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)

    def summary(self) -> str:
        """Return a human-readable summary of the plan for display in the UI."""
        lines = [
            f"Daily Plan — {self.plan_date.strftime('%A, %B %d %Y')}",
            f"Time used: {self.total_minutes_used} min",
            "",
        ]
        if self.conflicts:
            lines.append("⚠️  Conflicts detected:")
            for c in self.conflicts:
                lines.append(f"  ! {c}")
            lines.append("")
        if self.slots:
            lines.append("Scheduled:")
            for slot in self.slots:
                lines.append(
                    f"  {slot.start_time}  {slot.task.title}"
                    f" ({slot.task.duration_minutes} min) — {slot.reason}"
                )
        if self.skipped_tasks:
            lines.append("")
            lines.append("Skipped (over budget or deadline missed):")
            for task in self.skipped_tasks:
                lines.append(f"  • {task.title}")
        return "\n".join(lines)


class Scheduler:
    def __init__(
        self,
        owner: Owner,
        available_minutes: int,
        day_start_hour: int = 8,
    ) -> None:
        self.owner = owner
        self.available_minutes = available_minutes
        self.day_start_hour = day_start_hour

    @property
    def pet(self) -> Optional[Pet]:
        """Quick access to the owner's first pet, or None if they don't have any."""
        return self.owner.pets[0] if self.owner.pets else None

    def generate_plan(self) -> DailyPlan:
        """Retrieve all tasks from the owner's pets, sort by priority, fit into budget, return a DailyPlan."""
        today = date.today()
        plan = DailyPlan()
        used = 0
        current_minutes = self.day_start_hour * 60

        sorted_tasks = self._sort_by_priority(today)
        plan.conflicts = self._detect_conflicts(sorted_tasks)

        for task in sorted_tasks:
            if self._fits_in_budget(task, used):
                start_time = self._minutes_to_time(current_minutes)
                if task.priority == Priority.HIGH and task.is_time_sensitive():
                    reason = f"High priority and time-sensitive; must start before {task.deadline_hour}:00"
                elif task.priority == Priority.HIGH:
                    reason = "High priority; scheduled first"
                elif task.is_time_sensitive():
                    reason = f"Time-sensitive; must start before {task.deadline_hour}:00"
                else:
                    reason = f"{task.priority.name.capitalize()} priority"
                plan.slots.append(PlanSlot(task=task, start_time=start_time, reason=reason))
                used += task.duration_minutes
                current_minutes += task.duration_minutes
            else:
                plan.skipped_tasks.append(task)

        plan.total_minutes_used = used
        return plan

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort a list of tasks by deadline hour, earliest first; tasks with no deadline go last."""
        return sorted(
            tasks,
            key=lambda t: t.deadline_hour if t.deadline_hour is not None else 999,
        )

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return all tasks across the owner's pets that match the given completion status."""
        return [t for t in self.owner.get_all_tasks() if t.completed == completed]

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return all tasks belonging to a specific pet by name."""
        return self.owner.get_tasks_by_pet(pet_name)

    def _sort_by_priority(self, today: date) -> list[Task]:
        """Sort tasks HIGH→LOW; within each tier, earliest deadline first; skip completed and non-recurring."""
        eligible = [
            t for t in self.owner.get_all_tasks()
            if not t.completed and t.should_run_today(today)
        ]
        return sorted(
            eligible,
            key=lambda t: (t.priority.value, t.deadline_hour if t.deadline_hour is not None else 999),
        )

    def _fits_in_budget(self, task: Task, used_minutes: int) -> bool:
        """Return True if adding this task would not exceed available_minutes."""
        return used_minutes + task.duration_minutes <= self.available_minutes

    def _detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Flag any time-sensitive task that would start after its deadline given the current order."""
        conflicts = []
        current_minutes = self.day_start_hour * 60
        for task in tasks:
            if task.is_time_sensitive():
                start_hour = current_minutes / 60
                if start_hour >= task.deadline_hour:
                    conflicts.append(
                        f"'{task.title}' needs to start before {task.deadline_hour}:00 "
                        f"but would start at {self._minutes_to_time(current_minutes)}"
                    )
            current_minutes += task.duration_minutes
        return conflicts

    def _minutes_to_time(self, minutes: int) -> str:
        """Convert a number of minutes since midnight into a readable time like '8:30 AM'."""
        hour = (minutes // 60) % 24
        minute = minutes % 60
        period = "AM" if hour < 12 else "PM"
        display_hour = hour % 12 or 12
        return f"{display_hour}:{minute:02d} {period}"
