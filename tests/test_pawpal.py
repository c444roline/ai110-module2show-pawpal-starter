from datetime import date, timedelta
from pawpal_system import Task, Pet, Day, User


def test_mark_complete():
    task = Task(title="Morning walk")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Pinky")
    assert len(pet.tasks) == 0
    pet.add_task(Task(title="Feeding"))
    assert len(pet.tasks) == 1
    pet.add_task(Task(title="Grooming"))
    assert len(pet.tasks) == 2


def test_sort_tasks_by_time():
    day = Day(name="Test")
    day.tasks = [
        Task(title="Late", preferred_time="14:00"),
        Task(title="Early", preferred_time="08:00"),
        Task(title="Mid", preferred_time="11:00"),
    ]
    day.sort_tasks(by="time")
    assert [t.title for t in day.tasks] == ["Early", "Mid", "Late"]


def test_sort_tasks_by_priority():
    day = Day(name="Test")
    day.tasks = [
        Task(title="Low", priority="low"),
        Task(title="High", priority="high"),
        Task(title="Med", priority="medium"),
    ]
    day.sort_tasks(by="priority")
    assert [t.title for t in day.tasks] == ["High", "Med", "Low"]


def test_sort_tasks_by_duration():
    day = Day(name="Test")
    day.tasks = [
        Task(title="Long", duration_minutes=60),
        Task(title="Short", duration_minutes=10),
        Task(title="Mid", duration_minutes=30),
    ]
    day.sort_tasks(by="duration")
    assert [t.title for t in day.tasks] == ["Short", "Mid", "Long"]


def test_filter_by_pet():
    day = Day(name="Test")
    day.tasks = [
        Task(title="Walk", pet_name="Pinky"),
        Task(title="Feed", pet_name="Chungus"),
        Task(title="Play", pet_name="Pinky"),
    ]
    result = day.filter_by_pet("Pinky")
    assert [t.title for t in result] == ["Walk", "Play"]


def test_filter_by_status():
    day = Day(name="Test")
    t1 = Task(title="Done task")
    t1.mark_complete()
    t2 = Task(title="Pending task")
    day.tasks = [t1, t2]

    done = day.filter_by_status(completed=True)
    assert [t.title for t in done] == ["Done task"]

    pending = day.filter_by_status(completed=False)
    assert [t.title for t in pending] == ["Pending task"]


def test_generate_schedule_skips_completed():
    day = Day(name="Test", start_time="08:00", end_time="18:00")
    t1 = Task(title="Done", preferred_time="08:00", duration_minutes=30)
    t1.mark_complete()
    t2 = Task(title="Active", preferred_time="09:00", duration_minutes=30)
    day.tasks = [t1, t2]

    schedule = day.generate_schedule()
    assert len(schedule) == 1
    assert schedule[0]["task"] == "Active"


def test_generate_schedule_notes_moved_tasks():
    day = Day(name="Test", start_time="08:00", end_time="18:00")
    day.tasks = [
        Task(title="First", preferred_time="08:00", duration_minutes=60),
        Task(title="Second", preferred_time="08:30", duration_minutes=30),
    ]
    schedule = day.generate_schedule()
    assert schedule[1]["note"] == "moved from 08:30"


def test_detect_conflicts_finds_overlap():
    day = Day(name="Test", start_time="08:00", end_time="18:00")
    day.tasks = [
        Task(title="Task A", preferred_time="08:00", duration_minutes=60),
        Task(title="Task B", preferred_time="08:30", duration_minutes=30),
    ]
    conflicts = day.detect_conflicts()
    assert len(conflicts) == 1
    assert "Task A" in conflicts[0][2]
    assert "Task B" in conflicts[0][2]


def test_detect_conflicts_none_when_no_overlap():
    day = Day(name="Test", start_time="08:00", end_time="18:00")
    day.tasks = [
        Task(title="Task A", preferred_time="08:00", duration_minutes=30),
        Task(title="Task B", preferred_time="09:00", duration_minutes=30),
    ]
    conflicts = day.detect_conflicts()
    assert len(conflicts) == 0


def test_expand_recurring_includes_all_valid():
    tasks = [
        Task(title="Daily", recurrence="daily"),
        Task(title="Weekly", recurrence="weekly"),
        Task(title="Once", recurrence=""),
    ]
    result = Day.expand_recurring(tasks)
    assert len(result) == 3


def test_recurrence_field_default():
    task = Task(title="Test")
    assert task.recurrence == ""


def test_daily_mark_complete_creates_next_day():
    today = date(2026, 7, 5)
    task = Task(title="Walk", recurrence="daily", due_date=today)
    next_task = task.mark_complete()
    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False
    assert next_task.title == "Walk"
    assert next_task.recurrence == "daily"


def test_weekly_mark_complete_creates_next_week():
    today = date(2026, 7, 5)
    task = Task(title="Flea med", recurrence="weekly", due_date=today)
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == today + timedelta(weeks=1)
    assert next_task.recurrence == "weekly"


def test_onetime_mark_complete_returns_none():
    task = Task(title="Vet visit", recurrence="")
    result = task.mark_complete()
    assert task.completed is True
    assert result is None


def test_recurring_preserves_pet_name():
    task = Task(title="Feed", pet_name="Pinky", recurrence="daily", due_date=date(2026, 7, 5))
    next_task = task.mark_complete()
    assert next_task.pet_name == "Pinky"


def test_detect_conflicts_same_time():
    day = Day(name="Test", start_time="08:00", end_time="18:00")
    day.tasks = [
        Task(title="Breakfast", pet_name="Chungus", preferred_time="08:30", duration_minutes=15),
        Task(title="Eye drops", pet_name="Pinky", preferred_time="08:30", duration_minutes=5),
    ]
    conflicts = day.detect_conflicts()
    assert len(conflicts) == 1
    assert "Breakfast" in conflicts[0][2]
    assert "Eye drops" in conflicts[0][2]


# ── Behavior 1: Configuring user and pet information ──


def test_user_creation_and_defaults():
    user = User(name="Alice")
    assert user.name == "Alice"
    assert user.available_start == "08:00"
    assert user.available_end == "18:00"
    assert user.pets == []
    assert user.days == []


def test_user_set_name():
    user = User(name="Alice")
    user.set_name("Bob")
    assert user.name == "Bob"


def test_user_set_availability():
    user = User(name="Alice")
    user.set_availability("06:00", "20:00")
    assert user.available_start == "06:00"
    assert user.available_end == "20:00"


def test_user_add_and_remove_pet():
    user = User(name="Alice")
    user.add_pet(Pet(name="Pinky"))
    user.add_pet(Pet(name="Chungus"))
    assert len(user.pets) == 2
    assert user.remove_pet("Pinky") is True
    assert len(user.pets) == 1
    assert user.pets[0].name == "Chungus"


def test_user_remove_pet_not_found():
    user = User(name="Alice")
    assert user.remove_pet("Ghost") is False


def test_pet_set_name():
    pet = Pet(name="Pinky")
    pet.set_name("Pinky Jr.")
    assert pet.name == "Pinky Jr."


def test_pet_add_task_tags_pet_name():
    pet = Pet(name="Pinky")
    task = Task(title="Walk")
    pet.add_task(task)
    assert task.pet_name == "Pinky"


def test_pet_remove_task():
    pet = Pet(name="Pinky")
    pet.add_task(Task(title="Walk"))
    pet.add_task(Task(title="Feed"))
    assert pet.remove_task("Walk") is True
    assert len(pet.tasks) == 1
    assert pet.remove_task("Nonexistent") is False


def test_user_add_and_remove_day():
    user = User(name="Alice")
    user.add_day(Day(name="Monday"))
    assert len(user.days) == 1
    assert user.remove_day("Monday") is True
    assert len(user.days) == 0
    assert user.remove_day("Monday") is False


# ── Behavior 2: Viewing the schedule ──


def test_explain_plan_no_tasks():
    day = Day(name="Monday")
    result = day.explain_plan()
    assert result == "No tasks scheduled for this day."


def test_explain_plan_shows_task_details():
    day = Day(name="Monday", start_time="08:00", end_time="18:00")
    day.tasks = [
        Task(title="Walk Pinky", pet_name="Pinky", preferred_time="08:00",
             duration_minutes=30, priority="high"),
    ]
    plan = day.explain_plan()
    assert "Monday" in plan
    assert "Walk Pinky" in plan
    assert "[Pinky]" in plan
    assert "[HIGH]" in plan
    assert "30 min" in plan
    assert "08:00" in plan


def test_explain_plan_shows_conflicts():
    day = Day(name="Monday", start_time="08:00", end_time="18:00")
    day.tasks = [
        Task(title="Walk", preferred_time="08:00", duration_minutes=60),
        Task(title="Feed", preferred_time="08:30", duration_minutes=15),
    ]
    plan = day.explain_plan()
    assert "Conflicts detected" in plan
    assert "overlaps" in plan


def test_explain_plan_shows_moved_note():
    day = Day(name="Monday", start_time="08:00", end_time="18:00")
    day.tasks = [
        Task(title="Walk", preferred_time="08:00", duration_minutes=60),
        Task(title="Feed", preferred_time="08:30", duration_minutes=15),
    ]
    plan = day.explain_plan()
    assert "moved from 08:30" in plan


def test_explain_plan_all_completed():
    day = Day(name="Monday", start_time="08:00", end_time="18:00")
    t = Task(title="Done task", preferred_time="08:00", duration_minutes=30)
    t.mark_complete()
    day.tasks = [t]
    plan = day.explain_plan()
    assert plan == "No tasks scheduled for this day."


def test_explain_plan_total_duration():
    day = Day(name="Monday", start_time="08:00", end_time="18:00")
    day.tasks = [
        Task(title="Walk", preferred_time="08:00", duration_minutes=30),
        Task(title="Feed", preferred_time="09:00", duration_minutes=15),
    ]
    plan = day.explain_plan()
    assert "Total: 45 minutes" in plan


# ── Behavior 3: Listing tasks for each pet ──


def test_filter_by_pet_no_match():
    day = Day(name="Monday")
    day.tasks = [Task(title="Walk", pet_name="Pinky")]
    result = day.filter_by_pet("Ghost")
    assert result == []


def test_filter_by_pet_multiple_pets():
    day = Day(name="Monday")
    day.tasks = [
        Task(title="Walk Pinky", pet_name="Pinky"),
        Task(title="Feed Chungus", pet_name="Chungus"),
        Task(title="Groom Pinky", pet_name="Pinky"),
        Task(title="Vet Chungus", pet_name="Chungus"),
    ]
    pinky_tasks = day.filter_by_pet("Pinky")
    chungus_tasks = day.filter_by_pet("Chungus")
    assert [t.title for t in pinky_tasks] == ["Walk Pinky", "Groom Pinky"]
    assert [t.title for t in chungus_tasks] == ["Feed Chungus", "Vet Chungus"]


def test_filter_by_pet_empty_day():
    day = Day(name="Monday")
    result = day.filter_by_pet("Pinky")
    assert result == []


def test_pet_with_no_tasks():
    pet = Pet(name="Lazy")
    assert pet.tasks == []
    day = Day(name="Monday")
    result = day.filter_by_pet("Lazy")
    assert result == []


# ── Behavior 4 (additional): Recurring task management ──


def test_daily_recurrence_no_due_date_uses_today():
    task = Task(title="Walk", recurrence="daily")
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == date.today() + timedelta(days=1)


def test_weekly_recurrence_no_due_date_uses_today():
    task = Task(title="Flea meds", recurrence="weekly")
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == date.today() + timedelta(weeks=1)


def test_recurring_preserves_all_fields():
    task = Task(
        title="Walk", pet_name="Pinky", description="Morning walk",
        duration_minutes=45, priority="high", preferred_time="07:00",
        recurrence="daily", due_date=date(2026, 7, 5),
    )
    next_task = task.mark_complete()
    assert next_task.title == "Walk"
    assert next_task.pet_name == "Pinky"
    assert next_task.description == "Morning walk"
    assert next_task.duration_minutes == 45
    assert next_task.priority == "high"
    assert next_task.preferred_time == "07:00"
    assert next_task.recurrence == "daily"
    assert next_task.completed is False


def test_recurring_chain_multiple_completions():
    task = Task(title="Feed", recurrence="daily", due_date=date(2026, 7, 1))
    second = task.mark_complete()
    third = second.mark_complete()
    assert task.completed is True
    assert second.completed is True
    assert third.completed is False
    assert second.due_date == date(2026, 7, 2)
    assert third.due_date == date(2026, 7, 3)


# ── Behavior 5 (additional): Day capacity / time window management ──


def test_add_task_within_capacity():
    day = Day(name="Monday", start_time="08:00", end_time="09:00")
    task = Task(title="Walk", duration_minutes=60)
    assert day.add_task(task) is True
    assert len(day.tasks) == 1


def test_add_task_exceeds_capacity():
    day = Day(name="Monday", start_time="08:00", end_time="09:00")
    day.add_task(Task(title="Walk", duration_minutes=50))
    assert day.add_task(Task(title="Feed", duration_minutes=20)) is False
    assert len(day.tasks) == 1


def test_add_task_exactly_fills_capacity():
    day = Day(name="Monday", start_time="08:00", end_time="09:00")
    assert day.add_task(Task(title="Walk", duration_minutes=30)) is True
    assert day.add_task(Task(title="Feed", duration_minutes=30)) is True
    assert day.add_task(Task(title="Play", duration_minutes=1)) is False


def test_day_total_duration():
    day = Day(name="Monday")
    day.tasks = [
        Task(title="Walk", duration_minutes=30),
        Task(title="Feed", duration_minutes=15),
    ]
    assert day.get_total_duration() == 45


def test_day_total_duration_empty():
    day = Day(name="Monday")
    assert day.get_total_duration() == 0


def test_day_remove_task():
    day = Day(name="Monday")
    day.tasks = [Task(title="Walk"), Task(title="Feed")]
    assert day.remove_task("Walk") is True
    assert len(day.tasks) == 1
    assert day.remove_task("Ghost") is False
