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

```
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.0.3, pluggy-1.6.0 -- C:\Python314\python.exe
cachedir: .pytest_cache
rootdir: c:\Users\owari\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collecting ... collected 47 items

tests/test_pawpal.py::test_mark_complete PASSED                          [  2%]
tests/test_pawpal.py::test_add_task_increases_count PASSED               [  4%]
tests/test_pawpal.py::test_sort_tasks_by_time PASSED                     [  6%]
tests/test_pawpal.py::test_sort_tasks_by_priority PASSED                 [  8%]
tests/test_pawpal.py::test_sort_tasks_by_duration PASSED                 [ 10%]
tests/test_pawpal.py::test_filter_by_pet PASSED                          [ 12%]
tests/test_pawpal.py::test_filter_by_status PASSED                       [ 14%]
tests/test_pawpal.py::test_generate_schedule_skips_completed PASSED      [ 17%]
tests/test_pawpal.py::test_generate_schedule_notes_moved_tasks PASSED    [ 19%]
tests/test_pawpal.py::test_detect_conflicts_finds_overlap PASSED         [ 21%]
tests/test_pawpal.py::test_detect_conflicts_none_when_no_overlap PASSED  [ 23%]
tests/test_pawpal.py::test_expand_recurring_includes_all_valid PASSED    [ 25%]
tests/test_pawpal.py::test_recurrence_field_default PASSED               [ 27%]
tests/test_pawpal.py::test_daily_mark_complete_creates_next_day PASSED   [ 29%]
tests/test_pawpal.py::test_weekly_mark_complete_creates_next_week PASSED [ 31%]
tests/test_pawpal.py::test_onetime_mark_complete_returns_none PASSED     [ 34%]
tests/test_pawpal.py::test_recurring_preserves_pet_name PASSED           [ 36%]
tests/test_pawpal.py::test_detect_conflicts_same_time PASSED             [ 38%]
tests/test_pawpal.py::test_user_creation_and_defaults PASSED             [ 40%]
tests/test_pawpal.py::test_user_set_name PASSED                          [ 42%]
tests/test_pawpal.py::test_user_set_availability PASSED                  [ 44%]
tests/test_pawpal.py::test_user_add_and_remove_pet PASSED                [ 46%]
tests/test_pawpal.py::test_user_remove_pet_not_found PASSED              [ 48%]
tests/test_pawpal.py::test_pet_set_name PASSED                           [ 51%]
tests/test_pawpal.py::test_pet_add_task_tags_pet_name PASSED             [ 53%]
tests/test_pawpal.py::test_pet_remove_task PASSED                        [ 55%]
tests/test_pawpal.py::test_user_add_and_remove_day PASSED                [ 57%]
tests/test_pawpal.py::test_explain_plan_no_tasks PASSED                  [ 59%]
tests/test_pawpal.py::test_explain_plan_shows_task_details PASSED        [ 61%]
tests/test_pawpal.py::test_explain_plan_shows_conflicts PASSED           [ 63%]
tests/test_pawpal.py::test_explain_plan_shows_moved_note PASSED          [ 65%]
tests/test_pawpal.py::test_explain_plan_all_completed PASSED             [ 68%]
tests/test_pawpal.py::test_explain_plan_total_duration PASSED            [ 70%]
tests/test_pawpal.py::test_filter_by_pet_no_match PASSED                 [ 72%]
tests/test_pawpal.py::test_filter_by_pet_multiple_pets PASSED            [ 74%]
tests/test_pawpal.py::test_filter_by_pet_empty_day PASSED                [ 76%]
tests/test_pawpal.py::test_pet_with_no_tasks PASSED                      [ 78%]
tests/test_pawpal.py::test_daily_recurrence_no_due_date_uses_today PASSED [ 80%]
tests/test_pawpal.py::test_weekly_recurrence_no_due_date_uses_today PASSED [ 82%]
tests/test_pawpal.py::test_recurring_preserves_all_fields PASSED         [ 85%]
tests/test_pawpal.py::test_recurring_chain_multiple_completions PASSED   [ 87%]
tests/test_pawpal.py::test_add_task_within_capacity PASSED               [ 89%]
tests/test_pawpal.py::test_add_task_exceeds_capacity PASSED              [ 91%]
tests/test_pawpal.py::test_add_task_exactly_fills_capacity PASSED        [ 93%]
tests/test_pawpal.py::test_day_total_duration PASSED                     [ 95%]
tests/test_pawpal.py::test_day_total_duration_empty PASSED               [ 97%]
tests/test_pawpal.py::test_day_remove_task PASSED                        [100%]

============================= 47 passed in 0.15s ==============================
```

Confidence Level: 4/5

All 47 tests pass. The core scheduling logic is verified with both happy paths and edge cases (empty days, pets with no tasks, exact-capacity fill, same-time conflicts, chained recurring completions). One star removed because the test suite does not yet cover input validation or the Streamlit UI layer.

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
