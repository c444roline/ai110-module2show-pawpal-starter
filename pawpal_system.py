from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    description: str = ""
    duration_minutes: int = 15
    priority: str = "medium"
    preferred_time: str = ""
    completed: bool = False

    def mark_complete(self) -> None:
        pass

    def set_priority(self, priority: str) -> None:
        pass

    def set_duration(self, minutes: int) -> None:
        pass

    def set_preferred_time(self, time: str) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str = "dog"
    tasks: list[Task] = field(default_factory=list)

    def set_name(self, name: str) -> None:
        pass

    def set_species(self, species: str) -> None:
        pass

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, title: str) -> bool:
        pass


@dataclass
class Day:
    name: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> bool:
        pass

    def remove_task(self, title: str) -> bool:
        pass

    def sort_by_priority(self) -> None:
        pass

    def sort_by_time(self) -> None:
        pass

    def get_total_duration(self) -> int:
        pass

    def generate_schedule(self) -> list[dict]:
        pass

    def explain_plan(self) -> str:
        pass


class User:
    def __init__(self, name: str, available_start: str = "08:00", available_end: str = "18:00") -> None:
        self.name = name
        self.available_start = available_start
        self.available_end = available_end
        self.pets: list[Pet] = []

    def set_name(self, name: str) -> None:
        pass

    def set_availability(self, start: str, end: str) -> None:
        pass

    def get_available_minutes(self) -> int:
        pass

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, name: str) -> bool:
        pass
