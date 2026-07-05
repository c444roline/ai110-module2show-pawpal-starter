from pawpal_system import Task, Pet


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
