from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import IntEnum
from typing import Optional


class Priority(IntEnum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


@dataclass
class Pet:
    name: str
    species: str
    age: int
    notes: str = ""


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Priority
    category: str
    deadline_hour: Optional[int] = None

    def is_time_sensitive(self) -> bool:
        """Return True if this task has a hard deadline constraint."""
        return self.deadline_hour is not None


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

    def summary(self) -> str:
        """Return a human-readable summary of the plan for display in the UI."""
        lines = [
            f"Daily Plan — {self.plan_date.strftime('%A, %B %d %Y')}",
            f"Time used: {self.total_minutes_used} min",
            "",
        ]
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
        pet: Pet,
        available_minutes: int,
        day_start_hour: int = 8,
    ) -> None:
        self.pet = pet
        self.available_minutes = available_minutes
        self.day_start_hour = day_start_hour
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler's task list."""
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove a task by title from the task list."""
        self.tasks = [t for t in self.tasks if t.title != title]

    def generate_plan(self) -> DailyPlan:
        """Sort tasks by priority, fit them into the time budget, and return a DailyPlan."""
        plan = DailyPlan()
        used = 0
        current_minutes = self.day_start_hour * 60

        for task in self._sort_by_priority():
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

    def _sort_by_priority(self) -> list[Task]:
        """Return tasks sorted HIGH → MEDIUM → LOW (time-sensitive tasks first within each tier)."""
        return sorted(
            self.tasks,
            key=lambda t: (t.priority.value, not t.is_time_sensitive()),
        )

    def _fits_in_budget(self, task: Task, used_minutes: int) -> bool:
        """Return True if adding this task would not exceed available_minutes."""
        return used_minutes + task.duration_minutes <= self.available_minutes

    def _minutes_to_time(self, minutes: int) -> str:
        hour = (minutes // 60) % 24
        minute = minutes % 60
        period = "AM" if hour < 12 else "PM"
        display_hour = hour % 12 or 12
        return f"{display_hour}:{minute:02d} {period}"
