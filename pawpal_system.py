from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    title: str
    pet_name: str = ""
    description: str = ""
    duration_minutes: int = 15
    priority: str = "medium"
    preferred_time: str = ""
    completed: bool = False
    recurrence: str = ""
    due_date: date | None = None

    def mark_complete(self) -> Task | None:
        """Mark this task as completed. If the task is recurring ('daily' or
        'weekly'), automatically creates and returns a new Task instance with
        the due_date advanced by 1 day or 7 days using timedelta. Returns None
        for one-time tasks."""
        self.completed = True
        if self.recurrence == "daily":
            next_date = (self.due_date or date.today()) + timedelta(days=1)
            return Task(
                title=self.title,
                pet_name=self.pet_name,
                description=self.description,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                preferred_time=self.preferred_time,
                recurrence=self.recurrence,
                due_date=next_date,
            )
        if self.recurrence == "weekly":
            next_date = (self.due_date or date.today()) + timedelta(weeks=1)
            return Task(
                title=self.title,
                pet_name=self.pet_name,
                description=self.description,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                preferred_time=self.preferred_time,
                recurrence=self.recurrence,
                due_date=next_date,
            )
        return None

    def set_priority(self, priority: str) -> None:
        """Set the task priority to high, medium, or low."""
        self.priority = priority

    def set_duration(self, minutes: int) -> None:
        """Set the task duration in minutes."""
        self.duration_minutes = minutes

    def set_preferred_time(self, time: str) -> None:
        """Set the preferred start time in HH:MM format."""
        self.preferred_time = time


@dataclass
class Pet:
    name: str
    tasks: list[Task] = field(default_factory=list)

    def set_name(self, name: str) -> None:
        """Update the pet's name."""
        self.name = name

    def add_task(self, task: Task) -> None:
        """Add a task and tag it with this pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, title: str) -> bool:
        """Remove a task by title; return True if found."""
        for i, task in enumerate(self.tasks):
            if task.title == title:
                self.tasks.pop(i)
                return True
        return False


@dataclass
class Day:
    name: str
    start_time: str = "08:00"
    end_time: str = "18:00"
    tasks: list[Task] = field(default_factory=list)

    def _time_to_minutes(self, time_str: str) -> int:
        """Convert an HH:MM string to total minutes."""
        hours, minutes = time_str.split(":")
        return int(hours) * 60 + int(minutes)

    def _minutes_to_time(self, total: int) -> str:
        """Convert total minutes back to an HH:MM string."""
        return f"{total // 60:02d}:{total % 60:02d}"

    def add_task(self, task: Task) -> bool:
        """Add a task if it fits within the day's time window."""
        available = self._time_to_minutes(self.end_time) - self._time_to_minutes(self.start_time)
        if self.get_total_duration() + task.duration_minutes > available:
            return False
        self.tasks.append(task)
        return True

    def remove_task(self, title: str) -> bool:
        """Remove a task by title; return True if found."""
        for i, task in enumerate(self.tasks):
            if task.title == title:
                self.tasks.pop(i)
                return True
        return False

    def sort_by_priority(self) -> None:
        """Sort tasks by priority: high first, then medium, then low."""
        ranking = {"high": 0, "medium": 1, "low": 2}
        self.tasks.sort(key=lambda t: ranking.get(t.priority, 1))

    def sort_by_time(self) -> None:
        """Sort tasks by preferred time. Uses sorted() with a lambda key that
        converts each 'HH:MM' string to total minutes (e.g. '09:30' -> 570)
        for correct numeric ordering. Tasks without a preferred time sort last
        via float('inf')."""
        self.tasks = sorted(
            self.tasks,
            key=lambda t: self._time_to_minutes(t.preferred_time) if t.preferred_time else float("inf"),
        )

    def sort_tasks(self, by: str = "time") -> None:
        """Unified sort dispatcher. Accepts 'time' (HH:MM numeric sort),
        'priority' (high -> medium -> low), or 'duration' (shortest first)."""
        if by == "time":
            self.sort_by_time()
        elif by == "priority":
            self.sort_by_priority()
        elif by == "duration":
            self.tasks.sort(key=lambda t: t.duration_minutes)

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return only the tasks assigned to the given pet name. Uses a list
        comprehension that matches task.pet_name exactly."""
        return [t for t in self.tasks if t.pet_name == pet_name]

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return tasks matching the given completion status. Pass
        completed=True for finished tasks, completed=False for pending ones."""
        return [t for t in self.tasks if t.completed == completed]

    @staticmethod
    def expand_recurring(tasks: list[Task]) -> list[Task]:
        """Filter a task list to those that apply to a given day. Includes
        one-time tasks (recurrence=''), daily tasks, and weekly tasks."""
        return [t for t in tasks if t.recurrence in ("", "daily", "weekly")]

    def detect_conflicts(self) -> list[tuple[str, str, str]]:
        """Lightweight conflict detection that checks for overlapping preferred
        time slots among incomplete tasks. Sorts timed tasks, then does a single
        forward pass comparing each task's end time against subsequent start
        times. Returns a list of (task_a, task_b, warning_message) tuples
        rather than raising exceptions, so callers can display warnings without
        crashing the program."""
        timed = [t for t in self.tasks if t.preferred_time and not t.completed]
        timed.sort(key=lambda t: t.preferred_time)
        conflicts = []
        for i, a in enumerate(timed):
            a_start = self._time_to_minutes(a.preferred_time)
            a_end = a_start + a.duration_minutes
            for b in timed[i + 1:]:
                b_start = self._time_to_minutes(b.preferred_time)
                if b_start < a_end:
                    conflicts.append((
                        a.title,
                        b.title,
                        f"{a.title} ({a.preferred_time}-{self._minutes_to_time(a_end)}) "
                        f"overlaps with {b.title} ({b.preferred_time})",
                    ))
        return conflicts

    def get_total_duration(self) -> int:
        """Return the combined duration of all tasks in minutes."""
        return sum(t.duration_minutes for t in self.tasks)

    def generate_schedule(self) -> list[dict]:
        """Build a time-slotted schedule. Sorts by priority then time (stable
        sort preserves priority order within the same time slot). Walks a time
        cursor forward, honoring preferred times when possible and annotating
        tasks that had to be moved. Skips completed tasks."""
        self.sort_by_priority()
        self.sort_by_time()
        schedule = []
        current = self._time_to_minutes(self.start_time)
        for task in self.tasks:
            if task.completed:
                continue
            note = ""
            if task.preferred_time:
                preferred = self._time_to_minutes(task.preferred_time)
                if preferred >= current:
                    current = preferred
                else:
                    note = f"moved from {task.preferred_time}"
            schedule.append({
                "time": self._minutes_to_time(current),
                "task": task.title,
                "pet": task.pet_name,
                "duration": task.duration_minutes,
                "priority": task.priority,
                "note": note,
            })
            current += task.duration_minutes
        return schedule

    def explain_plan(self) -> str:
        """Return a formatted, human-readable schedule for the day."""
        schedule = self.generate_schedule()
        if not schedule:
            return "No tasks scheduled for this day."
        divider = "-" * 50
        lines = [f"\n  Schedule for {self.name}", f"  {divider}"]
        for entry in schedule:
            pet_label = f" [{entry['pet']}]" if entry["pet"] else ""
            tag = f"[{entry['priority'].upper()}]"
            note = f"  ** {entry['note']}" if entry.get("note") else ""
            lines.append(
                f"  {entry['time']}  {tag:<8} {entry['task']}{pet_label}"
                f"  ({entry['duration']} min){note}"
            )
        lines.append(f"  {divider}")
        active_duration = sum(e["duration"] for e in schedule)
        lines.append(f"  Total: {active_duration} minutes")
        conflicts = self.detect_conflicts()
        if conflicts:
            lines.append(f"\n  Conflicts detected:")
            for _, _, msg in conflicts:
                lines.append(f"    !! {msg}")
        lines.append("")
        return "\n".join(lines)


class User:
    def __init__(self, name: str, available_start: str = "08:00", available_end: str = "18:00") -> None:
        self.name = name
        self.available_start = available_start
        self.available_end = available_end
        self.pets: list[Pet] = []
        self.days: list[Day] = []

    def set_name(self, name: str) -> None:
        """Update the user's name."""
        self.name = name

    def set_availability(self, start: str, end: str) -> None:
        """Set the user's available time window in HH:MM format."""
        self.available_start = start
        self.available_end = end

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this user."""
        self.pets.append(pet)

    def remove_pet(self, name: str) -> bool:
        """Remove a pet by name; return True if found."""
        for i, pet in enumerate(self.pets):
            if pet.name == name:
                self.pets.pop(i)
                return True
        return False

    def add_day(self, day: Day) -> None:
        """Add a scheduled day to this user."""
        self.days.append(day)

    def remove_day(self, name: str) -> bool:
        """Remove a day by name; return True if found."""
        for i, day in enumerate(self.days):
            if day.name == name:
                self.days.pop(i)
                return True
        return False
