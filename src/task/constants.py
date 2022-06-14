from enum import Enum


TASK_NOT_FOUND = "Task with this id doesn't exist"


class TaskType(int, Enum):
    russian_to_english = 1
    english_to_russian = 2
    join_phrase = 3
