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

The scheduler considers five constraints: task priority (HIGH/MEDIUM/LOW), time budget (how many minutes the owner has available), deadline hour (tasks that must start before a certain time), completion status (already-done tasks are skipped), and frequency (whether a task is even due today based on daily/weekly/once). I decided priority and time budget mattered most because they affect every task — deadlines only apply to a subset, and frequency is more of a pre-filter than a real constraint.

**b. Tradeoffs**

The conflict detection flags any two tasks that share the same deadline_hour as a potential overlap, but it doesn't check whether their combined duration actually fits before the deadline. So two 5-minute tasks both due by 9am — when the day starts at 8am and there's a full hour — still get flagged even though they'd both easily fit. That's a false positive.

I kept this simpler version because the math to check exact duration fit adds a lot of complexity, and for a pet care app it's better to warn the owner too often than to miss a real conflict. The user can always look at the schedule and decide for themselves whether the warning matters.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI throughout basically every phase of this project. At the start it helped me brainstorm the classes — I described what the app needed to do and it suggested a starting structure. During implementation it was useful for filling in method bodies once I had the stubs written, especially for things like the `timedelta` logic for recurring tasks and the `defaultdict` pattern for conflict detection. When something wasn't working, I'd paste the broken function and ask what was wrong. The prompts that worked best were specific ones — like "given this skeleton, how should Scheduler retrieve tasks from Owner's pets" — rather than broad ones like "write me a scheduler." Narrow, focused questions got better answers.

Agent mode was the most useful feature overall. Being able to say "implement these method stubs based on the class design" and have it write across multiple methods at once saved a lot of time. Inline chat was good for smaller things like fixing a single method or asking why a test was failing.

**b. Judgment and verification**

When AI suggested using a list comprehension to replace the `for` loop inside `_detect_conflicts()`, I looked at it and decided not to use it. The comprehension version put everything on one long line that was hard to read at a glance. The original loop version was more lines but you could follow the logic step by step. I ran the tests either way and they passed both times, so the behavior was identical — the only difference was readability. I kept the loop because I'd rather have code I can understand quickly over code that's technically shorter. I also double-checked the conflict detection output against `main.py` to make sure both versions produced the same warnings.

---

## 4. Testing and Verification

**a. What you tested**

I tested 14 behaviors across five areas. Task behavior: marking a task complete, adding tasks to a pet, and making sure completed tasks are excluded from the generated schedule. Recurring tasks: daily tasks reschedule for tomorrow, weekly tasks for one week later, and one-off tasks stop after completion. Sorting: `sort_by_time()` returns tasks in deadline order with no-deadline tasks at the end. Scheduling logic: HIGH priority always comes before LOW, the time budget is respected so tasks over budget go to skipped, and completed tasks never appear in the plan. Conflict detection: two tasks with the same deadline trigger an overlap warning, and a single time-sensitive task produces no false positive.

These tests mattered because the scheduling logic has a lot of moving parts — priority, deadlines, frequency, budget — and it's easy for one thing to silently break another. Having tests meant I could change the sort logic or conflict detection and immediately know if something else stopped working.

**b. Confidence**

I'm fairly confident in the core behaviors — all 14 tests pass and they cover both happy paths and edge cases. The area I'm least sure about is the weekly frequency logic. Right now a weekly task only runs on Mondays, which works as a simple rule but isn't really "every 7 days from last completion." If I had more time I'd test what happens when you complete a weekly task on a Wednesday, and whether the next occurrence lands correctly. I'd also want to test what happens when an owner has zero available minutes, and whether the UI handles an empty plan gracefully.

---

## 5. Reflection

**a. What went well**

The part I'm most satisfied with is how the scheduling logic turned out. `generate_plan()` handles priority, deadlines, budget, completion status, and frequency all at once and still produces a clean explainable output. The fact that every slot in the plan has a `reason` string — so the owner always knows why a task was placed when it was — felt like a good design decision that paid off when connecting it to the UI.

**b. What you would improve**

If I had another iteration I'd redesign the weekly frequency logic to track actual days since last completion rather than just "run on Mondays." I'd also add the ability to edit or reorder tasks in the UI rather than only being able to add them. Right now if you add a task with the wrong priority you have to remove it and re-add it, which is clunky. A simple edit form would make the app much more usable.

**c. Key takeaway**

The biggest thing I learned is that AI is genuinely useful as a collaborator, but only if you stay in charge of the design. The AI would happily write code that worked but didn't fit the structure I had planned — like early on when it kept wanting to put task logic inside the Scheduler instead of on the Pet. I had to keep pushing back and saying "no, tasks belong to the pet, not the scheduler." Once I held that line the whole system fit together cleanly. The takeaway is: decide your architecture first, then use AI to fill it in. Don't let it decide the architecture for you.
