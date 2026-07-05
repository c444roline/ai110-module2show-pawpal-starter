from pawpal_system import User, Pet, Task, Day

owner = User("Caroline", available_start="08:00", available_end="18:00")

pinky = Pet(name="Pinky")
chungus = Pet(name="Chungus")

pinky.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", preferred_time="08:00"))
pinky.add_task(Task(title="Flea medication", duration_minutes=10, priority="high", preferred_time="09:00"))
chungus.add_task(Task(title="Breakfast", duration_minutes=15, priority="high", preferred_time="08:30"))
chungus.add_task(Task(title="Grooming", duration_minutes=45, priority="medium", preferred_time="10:00"))
pinky.add_task(Task(title="Afternoon nap check", duration_minutes=10, priority="low", preferred_time="13:00"))

owner.add_pet(pinky)
owner.add_pet(chungus)

today = Day(name="Today", start_time=owner.available_start, end_time=owner.available_end)

for pet in owner.pets:
    for task in pet.tasks:
        today.add_task(task)

owner.add_day(today)

print(today.explain_plan())
