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
        self.completed = True

    def set_priority(self, priority: str) -> None:
        self.priority = priority

    def set_duration(self, minutes: int) -> None:
        self.duration_minutes = minutes

    def set_preferred_time(self, time: str) -> None:
        self.preferred_time = time


@dataclass
class Pet:
    name: str
    tasks: list[Task] = field(default_factory=list)

    def set_name(self, name: str) -> None:
        self.name = name

    def add_task(self, task: Task) -> None:
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, title: str) -> bool:
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
        hours, minutes = time_str.split(":")
        return int(hours) * 60 + int(minutes)

    def _minutes_to_time(self, total: int) -> str:
        return f"{total // 60:02d}:{total % 60:02d}"

    def add_task(self, task: Task) -> bool:
        available = self._time_to_minutes(self.end_time) - self._time_to_minutes(self.start_time)
        if self.get_total_duration() + task.duration_minutes > available:
            return False
        self.tasks.append(task)
        return True

    def remove_task(self, title: str) -> bool:
        for i, task in enumerate(self.tasks):
            if task.title == title:
                self.tasks.pop(i)
                return True
        return False

    def sort_by_priority(self) -> None:
        ranking = {"high": 0, "medium": 1, "low": 2}
        self.tasks.sort(key=lambda t: ranking.get(t.priority, 1))

    def sort_by_time(self) -> None:
        self.tasks.sort(key=lambda t: t.preferred_time if t.preferred_time else "99:99")

    def get_total_duration(self) -> int:
        return sum(t.duration_minutes for t in self.tasks)

    def generate_schedule(self) -> list[dict]:
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
        schedule = self.generate_schedule()
        if not schedule:
            return "No tasks scheduled for this day."
        lines = [f"Schedule for {self.name}:"]
        for entry in schedule:
            pet_label = f" for {entry['pet']}" if entry["pet"] else ""
            lines.append(
                f"  {entry['time']} - {entry['task']}{pet_label} "
                f"({entry['duration']} min, {entry['priority']} priority)"
            )
        lines.append(f"Total: {self.get_total_duration()} minutes")
        return "\n".join(lines)


class User:
    def __init__(self, name: str, available_start: str = "08:00", available_end: str = "18:00") -> None:
        self.name = name
        self.available_start = available_start
        self.available_end = available_end
        self.pets: list[Pet] = []
        self.days: list[Day] = []

    def set_name(self, name: str) -> None:
        self.name = name

    def set_availability(self, start: str, end: str) -> None:
        self.available_start = start
        self.available_end = end

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def remove_pet(self, name: str) -> bool:
        for i, pet in enumerate(self.pets):
            if pet.name == name:
                self.pets.pop(i)
                return True
        return False

    def add_day(self, day: Day) -> None:
        self.days.append(day)

    def remove_day(self, name: str) -> bool:
        for i, day in enumerate(self.days):
            if day.name == name:
                self.days.pop(i)
                return True
        return False
