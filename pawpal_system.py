from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    pet_name: str = ""
    description: str = ""
    duration_minutes: int = 15
    priority: str = "medium"
    preferred_time: str = ""
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

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
        """Sort tasks by preferred time; tasks without one go last."""
        self.tasks.sort(key=lambda t: t.preferred_time if t.preferred_time else "99:99")

    def get_total_duration(self) -> int:
        """Return the combined duration of all tasks in minutes."""
        return sum(t.duration_minutes for t in self.tasks)

    def generate_schedule(self) -> list[dict]:
        """Build a time-slotted schedule sorted by priority then time."""
        self.sort_by_priority()
        self.sort_by_time()
        schedule = []
        current = self._time_to_minutes(self.start_time)
        for task in self.tasks:
            if task.preferred_time:
                preferred = self._time_to_minutes(task.preferred_time)
                if preferred >= current:
                    current = preferred
            schedule.append({
                "time": self._minutes_to_time(current),
                "task": task.title,
                "pet": task.pet_name,
                "duration": task.duration_minutes,
                "priority": task.priority,
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
            lines.append(
                f"  {entry['time']}  {tag:<8} {entry['task']}{pet_label}"
                f"  ({entry['duration']} min)"
            )
        lines.append(f"  {divider}")
        lines.append(f"  Total: {self.get_total_duration()} minutes\n")
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
