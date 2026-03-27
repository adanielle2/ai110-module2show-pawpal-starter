# PawPal+ — Final UML Class Diagram

```mermaid
classDiagram
    class Priority {
        <<enumeration>>
        HIGH = 1
        MEDIUM = 2
        LOW = 3
    }

    class Task {
        +str title
        +int duration_minutes
        +Priority priority
        +str category
        +int deadline_hour
        +str frequency
        +bool completed
        +date due_date
        +is_time_sensitive() bool
        +mark_complete() None
        +should_run_today(today) bool
        +next_occurrence() Task
    }

    class Pet {
        +str name
        +str species
        +int age
        +str notes
        +list~Task~ tasks
        +add_task(task) None
        +remove_task(title) None
        +complete_task(title) Task
    }

    class Owner {
        +str name
        +list~Pet~ pets
        +add_pet(pet) None
        +get_all_pets() list~Pet~
        +get_all_tasks() list~Task~
        +get_tasks_by_pet(name) list~Task~
        +get_tasks_by_status(completed) list~Task~
        +get_tasks_by_category(category) list~Task~
    }

    class Scheduler {
        +Owner owner
        +int available_minutes
        +int day_start_hour
        +pet() Pet
        +generate_plan() DailyPlan
        +sort_by_time(tasks) list~Task~
        +filter_by_status(completed) list~Task~
        +filter_by_pet(name) list~Task~
        -_sort_by_priority(today) list~Task~
        -_fits_in_budget(task, used) bool
        -_detect_conflicts(tasks) list~str~
        -_minutes_to_time(minutes) str
    }

    class DailyPlan {
        +date plan_date
        +list~PlanSlot~ slots
        +int total_minutes_used
        +list~Task~ skipped_tasks
        +list~str~ conflicts
        +summary() str
    }

    class PlanSlot {
        +Task task
        +str start_time
        +str reason
    }

    Owner "1" *-- "1..*" Pet : owns
    Pet "1" *-- "*" Task : has
    Owner "1" --> "1" Scheduler : drives
    Scheduler ..> DailyPlan : creates
    DailyPlan "1" *-- "*" PlanSlot : contains
    PlanSlot --> Task : wraps
    Task --> Priority : has
```

## What changed from the initial UML

| Change | Reason |
|---|---|
| Added `Owner` class | Required by the assignment; `Scheduler` now takes an `Owner` instead of a bare `Pet` |
| `Task` gained `deadline_hour`, `frequency`, `completed`, `due_date` | Needed for conflict detection, recurring tasks, and schedule filtering |
| `Task` gained `mark_complete()`, `should_run_today()`, `next_occurrence()` | Recurring task logic — a task knows how to reschedule itself |
| `Pet` gained `tasks[]` and `complete_task()` | Tasks belong to pets, not the scheduler; `complete_task()` auto-appends the next occurrence |
| `Scheduler` takes `Owner`, not `Pet` | Allows scheduling across multiple pets |
| `Scheduler` gained public methods: `sort_by_time()`, `filter_by_status()`, `filter_by_pet()` | Expose sorting and filtering to the UI layer |
| `Scheduler` gained private helpers: `_detect_conflicts()`, `_minutes_to_time()` | Conflict detection and clock-time formatting |
| `DailyPlan` gained `plan_date` and `conflicts[]` | Plans need a date; conflict warnings surface to the UI |
| Removed `Scheduler → Task` (manages) relationship | Tasks no longer live on the scheduler — they live on `Pet` |
