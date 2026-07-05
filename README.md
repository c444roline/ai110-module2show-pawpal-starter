# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:
```
  Schedule for Today
  --------------------------------------------------
  08:00  [HIGH]   Morning walk [Pinky]  (30 min)
  08:30  [HIGH]   Breakfast [Chungus]  (15 min)
  09:00  [HIGH]   Flea medication [Pinky]  (10 min)
  10:00  [MEDIUM] Grooming [Chungus]  (45 min)
  13:00  [LOW]    Afternoon nap check [Pinky]  (10 min)
  --------------------------------------------------
  Total: 110 minutes
```
```
# Paste your pytest output here
```
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\owari\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 2 items

tests\test_pawpal.py ..                                                  [100%]

============================== 2 passed in 0.04s ==============================
## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Day.sort_by_time()`, `Day.sort_by_priority()`, `Day.sort_tasks(by=)` | `sort_by_time()` uses `sorted()` with a lambda that converts "HH:MM" strings to integer minutes for correct numeric ordering. `sort_tasks()` is a unified dispatcher accepting `"time"`, `"priority"`, or `"duration"`. |
| Filtering by pet | `Day.filter_by_pet(pet_name)` | Returns only tasks assigned to a specific pet via list comprehension matching `task.pet_name`. |
| Filtering by status | `Day.filter_by_status(completed)` | Returns tasks matching a completion status — pass `True` for done, `False` for pending. `generate_schedule()` also skips completed tasks automatically. |
| Conflict detection | `Day.detect_conflicts()` | Lightweight strategy: sorts tasks by preferred time, then does a forward pass comparing each task's end time (`start + duration`) against subsequent start times. Returns warning tuples instead of raising exceptions so the program never crashes. Warnings are printed at the bottom of `explain_plan()`. |
| Recurring tasks | `Task.mark_complete()`, `Day.expand_recurring(tasks)` | When a daily or weekly task is marked complete, `mark_complete()` automatically creates and returns a new `Task` with `due_date` advanced by `timedelta(days=1)` or `timedelta(weeks=1)`. One-time tasks return `None`. `expand_recurring()` filters a task list to those applicable to a given day. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
