from datetime import date
from pawpal_system import User, Pet, Task, Day

owner = User("Caroline", available_start="08:00", available_end="18:00")

pinky = Pet(name="Pinky")
chungus = Pet(name="Chungus")

# --- Tasks added deliberately out of order ---
pinky.add_task(Task(title="Afternoon nap check", duration_minutes=10, priority="low", preferred_time="13:00"))
chungus.add_task(Task(title="Grooming", duration_minutes=45, priority="medium", preferred_time="10:00"))
pinky.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", preferred_time="08:00",
                     recurrence="daily", due_date=date.today()))
chungus.add_task(Task(title="Flea medication", duration_minutes=10, priority="high", preferred_time="09:00",
                       recurrence="weekly", due_date=date.today()))

# Two tasks at the SAME time to trigger conflict detection
chungus.add_task(Task(title="Breakfast", duration_minutes=15, priority="high", preferred_time="08:30"))
pinky.add_task(Task(title="Eye drops", duration_minutes=5, priority="high", preferred_time="08:30"))

owner.add_pet(pinky)
owner.add_pet(chungus)

today = Day(name="Today", start_time=owner.available_start, end_time=owner.available_end)

all_tasks = Day.expand_recurring([t for pet in owner.pets for t in pet.tasks])
for task in all_tasks:
    today.add_task(task)

owner.add_day(today)

# --- Sort by time and display ---
today.sort_by_time()
print("  Tasks sorted by time:")
for t in today.tasks:
    print(f"    {t.preferred_time}  {t.title} [{t.pet_name}]")

# --- Filter by pet ---
print("\n  Pinky's tasks:")
for t in today.filter_by_pet("Pinky"):
    print(f"    - {t.title} ({t.priority}, {t.preferred_time})")

print("\n  Chungus's tasks:")
for t in today.filter_by_pet("Chungus"):
    print(f"    - {t.title} ({t.priority}, {t.preferred_time})")

# --- Full schedule with conflict warnings ---
print(today.explain_plan())

# --- Demonstrate recurring task auto-renewal ---
print("  === Recurring task auto-renewal ===\n")

# Complete the daily "Morning walk" — mark_complete returns the next occurrence
walk_task = pinky.tasks[1]  # Morning walk (daily)
print(f"  Completing '{walk_task.title}' (due {walk_task.due_date})...")
next_walk = walk_task.mark_complete()
print(f"  -> Next occurrence created: '{next_walk.title}' due {next_walk.due_date}")
pinky.add_task(next_walk)

# Complete the weekly "Flea medication" — mark_complete returns next week's occurrence
flea_task = chungus.tasks[1]  # Flea medication (weekly)
print(f"\n  Completing '{flea_task.title}' (due {flea_task.due_date})...")
next_flea = flea_task.mark_complete()
print(f"  -> Next occurrence created: '{next_flea.title}' due {next_flea.due_date}")
chungus.add_task(next_flea)

# Complete a one-time task — mark_complete returns None
nap_task = pinky.tasks[0]  # Afternoon nap check (one-time)
print(f"\n  Completing '{nap_task.title}' (one-time)...")
result = nap_task.mark_complete()
print(f"  -> Next occurrence: {result}  (no renewal for one-time tasks)")

# --- Filter by status after completions ---
print("\n  Completed tasks:")
for t in today.filter_by_status(completed=True):
    print(f"    - {t.title} [done]")

print("\n  Remaining tasks:")
for t in today.filter_by_status(completed=False):
    print(f"    - {t.title}")

# --- Regenerate schedule (completed excluded) ---
print(today.explain_plan())
