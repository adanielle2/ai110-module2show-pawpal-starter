# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three core actions a user needs to be able to do:
1. Register a pet profile (name, species, age, any special notes)
2. Add and manage care tasks for the day (what needs doing, how long it takes, how urgent it is)
3. Generate a daily schedule and see why each task was placed when it was

To support those actions I came up with seven classes. `Pet` and `Task` are both dataclasses since they're basically just data holders — no logic needed. `Task` has `is_time_sensitive()` so the scheduler can check for hard deadlines without having to look inside the task itself. `Priority` is an IntEnum (1/2/3) so sorting tasks by urgency is just a number sort, no extra code required. `Owner` holds the owner's name and their list of pets, with a helper to add pets and get them back. `Scheduler` is where the actual logic lives — it takes an Owner and the available time for the day, then figures out what fits and what order to do it in. The output is a `DailyPlan` made up of `PlanSlot`s, where each slot pairs a task with a start time and a short reason explaining why it was scheduled there.

**b. Design changes**

After reviewing the skeleton, three things got changed. First, the time constraint on `Task` was originally a plain string like `"before 9am"` but that would have meant writing parsing code just to check if a deadline existed, which felt messy and easy to break. Switching it to `deadline_hour` as an integer (e.g. `9` for 9 AM) made `is_time_sensitive()` a one-liner. Second, `DailyPlan` was missing a date field even though `date` was already imported — a plan with no date has no way to say what day it's for, so `plan_date` got added. Third, `Scheduler` had no way to know what time the day started, which meant it couldn't compute real clock times for each slot, so `day_start_hour` was added with a default of 8 AM.

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
