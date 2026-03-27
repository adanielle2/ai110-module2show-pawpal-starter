# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
1. Register a Pet Profile
The owner enters basic information about their pet such as name, species, age, and any special notes (e.g., "on medication," "anxious around strangers"). This profile is the foundation for everything else: the scheduler uses it to filter which tasks are relevant and to apply pet-specific constraints when building the daily plan.

2. Add and Manage Care Tasks
The owner creates tasks that need to happen during the day such as things like a morning walk, lunchtime feeding, an evening medication dose, or a weekly grooming session. Each task has at least a name, an estimated duration, and a priority level (e.g., High / Medium / Low). The owner can also edit or remove tasks as the pet's routine changes.

3. Generate and View the Daily Plan
The owner requests a daily schedule. The app considers all pending tasks, the owner's available time window for the day, and each task's priority, then produces an ordered plan that fits within the time budget. The plan is displayed clearly — showing each task, its scheduled time slot, and a short explanation of why it was placed where it was (e.g., "Medication scheduled first because it is High priority and time-sensitive").

Pet
— a plain data container for owner-entered profile info. No scheduling logic lives here; it just holds what the scheduler needs to know about the animal.
Task 
— represents a single care item. It knows its own duration, priority, category (walk, feeding, meds, etc.), and an optional time window (e.g. "must happen before 9am"). is_time_sensitive() lets the scheduler ask whether a task has a hard window constraint.
Priority 
— an IntEnum with values 1/2/3 so that sorting by priority is just a numeric sort. HIGH sorts before MEDIUM sorts before LOW.
Scheduler 
— the brain. It holds a Pet, a list of Tasks, and the owner's available minutes for the day. Its one public method, generate_plan(), applies the scheduling logic and returns a DailyPlan.
DailyPlan 
— the output. It holds an ordered list of PlanSlots (the tasks that fit), a count of total minutes used, and a list of tasks that couldn't be scheduled (budget exceeded or no valid window). summary() returns a human-readable string for the UI.
PlanSlot 
— wraps a single scheduled Task with its assigned start time and a reason string explaining why it was placed there (e.g. "High priority; scheduled first"). This is the key piece that makes the plan explainable.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
