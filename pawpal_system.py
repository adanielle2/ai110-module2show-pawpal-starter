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
class Task:
    title: str
    duration_minutes: int
    priority: Priority
    category: str
    deadline_hour: Optional[int] = None
    frequency: str = "daily"
    completed: bool = False

    def is_time_sensitive(self) -> bool:
        """Return True if this task has a hard deadline constraint."""
        return self.deadline_hour is not None


@dataclass
class Pet:
    name: str
    species: str
    age: int
    notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        self.tasks = [t for t in self.tasks if t.title != title]


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_pets(self) -> list[Pet]:
        return list(self.pets)

    def get_all_tasks(self) -> list[Task]:
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


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
        owner: Owner,
        available_minutes: int,
        day_start_hour: int = 8,
    ) -> None:
        self.owner = owner
        self.available_minutes = available_minutes
        self.day_start_hour = day_start_hour

    @property
    def pet(self) -> Optional[Pet]:
        return self.owner.pets[0] if self.owner.pets else None

    def generate_plan(self) -> DailyPlan:
        """Retrieve all tasks from the owner's pets, sort by priority, fit into budget, return a DailyPlan."""
        plan = DailyPlan()
        used = 0
        current_minutes = self.day_start_hour * 60

        for task in self._sort_by_priority():
            if task.completed:
                continue
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
        """Return all tasks from owner's pets sorted HIGH → MEDIUM → LOW (time-sensitive first within each tier)."""
        return sorted(
            self.owner.get_all_tasks(),
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
