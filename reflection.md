# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The system is split into six classes with clear, non-overlapping responsibilities:

- **`Pet`** — a plain dataclass that holds owner-entered profile info (name, species, age, notes). No scheduling logic lives here; it is purely a data container passed to the Scheduler.
- **`Task`** — a dataclass representing a single care item. It stores duration, priority, category, and an optional `deadline_hour`. Its one method, `is_time_sensitive()`, lets the Scheduler ask whether the task has a hard time constraint.
- **`Priority`** — an `IntEnum` (`HIGH=1`, `MEDIUM=2`, `LOW=3`). Using integers means sorting tasks by priority requires no custom comparator — a plain numeric sort works.
- **`Scheduler`** — the only class with real logic. It owns a `Pet`, a list of `Task`s, the owner's `available_minutes`, and a `day_start_hour`. Its public interface is a single method, `generate_plan()`, which returns a `DailyPlan`. Private helpers (`_sort_by_priority`, `_fits_in_budget`) keep the public method readable.
- **`DailyPlan`** — the output dataclass. It holds the ordered list of `PlanSlot`s that fit within the time budget, a count of `total_minutes_used`, a list of `skipped_tasks` (budget exceeded or deadline missed), and the `plan_date`. `summary()` formats it for the Streamlit UI.
- **`PlanSlot`** — wraps a scheduled `Task` with a concrete `start_time` string and a `reason` that explains the placement decision. This is what makes the plan explainable to the user.

**b. Design changes**

After an AI review of the skeleton, three changes were made:

1. **`time_window: Optional[str]` → `deadline_hour: Optional[int]`** — The original design stored the time constraint as a raw string (e.g., `"before 9am"`). The AI flagged that `is_time_sensitive()` would need to parse that string, which is fragile and error-prone. Replacing it with a plain integer hour (e.g., `9` meaning "must start before 9 AM") makes the constraint machine-readable without any parsing.

2. **Added `plan_date: date` to `DailyPlan`** — The original skeleton imported `date` from the standard library but never used it. A `DailyPlan` with no date field has no way to identify which day it belongs to. Adding `plan_date` (defaulting to today) fixes this missing relationship.

3. **Added `day_start_hour: int` to `Scheduler`** — Without knowing what time the day begins, `generate_plan()` cannot assign real clock times to `PlanSlot.start_time`. Adding `day_start_hour` (defaulting to `8` for 8 AM) gives the scheduler the anchor it needs to compute actual slot times.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
