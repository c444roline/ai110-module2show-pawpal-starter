from datetime import date, timedelta
from pawpal_system import Task, Pet, Day


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
