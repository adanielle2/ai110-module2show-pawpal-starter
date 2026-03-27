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
    time_window: Optional[str] = None  # e.g. "before 9am"

    def is_time_sensitive(self) -> bool:
        """Return True if this task has a hard time-window constraint."""
        ...


@dataclass
class PlanSlot:
    task: Task
    start_time: str
    reason: str


@dataclass
class DailyPlan:
    slots: list[PlanSlot] = field(default_factory=list)
    total_minutes_used: int = 0
    skipped_tasks: list[Task] = field(default_factory=list)

    def summary(self) -> str:
        """Return a human-readable summary of the plan for display in the UI."""
        ...


class Scheduler:
    def __init__(self, pet: Pet, available_minutes: int) -> None:
        self.pet = pet
        self.available_minutes = available_minutes
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler's task list."""
        ...

    def remove_task(self, title: str) -> None:
        """Remove a task by title from the task list."""
        ...

    def generate_plan(self) -> DailyPlan:
        """Sort tasks by priority, fit them into the time budget, and return a DailyPlan."""
        ...

    def _sort_by_priority(self) -> list[Task]:
        """Return tasks sorted HIGH → MEDIUM → LOW (time-sensitive tasks first within each tier)."""
        ...

    def _fits_in_budget(self, task: Task, used_minutes: int) -> bool:
        """Return True if adding this task would not exceed available_minutes."""
        ...
