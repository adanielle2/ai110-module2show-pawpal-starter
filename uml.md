# PawPal+ UML Class Diagram

```mermaid
classDiagram
    class Pet {
        +str name
        +str species
        +int age
        +str notes
    }

    class Task {
        +str title
        +int duration_minutes
        +Priority priority
        +str category
        +str time_window
        +is_time_sensitive() bool
    }

    class Priority {
        <<enumeration>>
        HIGH = 1
        MEDIUM = 2
        LOW = 3
    }

    class Scheduler {
        +Pet pet
        +list~Task~ tasks
        +int available_minutes
        +add_task(task)
        +remove_task(title)
        +generate_plan() DailyPlan
        -_sort_by_priority() list~Task~
        -_fits_in_budget(task, used_minutes) bool
    }

    class DailyPlan {
        +list~PlanSlot~ slots
        +int total_minutes_used
        +list~Task~ skipped_tasks
        +summary() str
    }

    class PlanSlot {
        +Task task
        +str start_time
        +str reason
    }

    Scheduler "1" --> "1" Pet : schedules for
    Scheduler "1" --> "*" Task : manages
    Scheduler ..> DailyPlan : creates
    DailyPlan "1" *-- "*" PlanSlot : contains
    PlanSlot --> Task : wraps
    Task --> Priority : has
```

## Class Descriptions

| Class | Responsibility |
|---|---|
| `Pet` | Plain data container for owner-entered profile info (name, species, age, notes) |
| `Task` | A single care item with duration, priority, category, and optional time window; `is_time_sensitive()` flags hard window constraints |
| `Priority` | `IntEnum` with `HIGH=1`, `MEDIUM=2`, `LOW=3` so priority sorting is a plain numeric sort |
| `Scheduler` | Holds a `Pet`, task list, and available minutes; `generate_plan()` is the sole public method and returns a `DailyPlan` |
| `DailyPlan` | Output of the scheduler: ordered `PlanSlot`s, total minutes used, skipped tasks, and a `summary()` string for the UI |
| `PlanSlot` | Wraps a scheduled `Task` with its assigned start time and a human-readable reason (e.g. "High priority; scheduled first") |
