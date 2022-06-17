import json

from src.db.db_config import get_session
from src.task.models import Task


db_session = get_session()


def update_task_table(load_data, db_session):
    orders_entries = []
    for task in load_data["tasks"]:
        task_obj = Task(type=task['type'], answer=task['answer'], question=task['question'])
        orders_entries.append(task_obj)
    db_session.add_all(orders_entries)
    db_session.commit()


if __name__ == "__main__":
    with open('task_legacy/db_load.json', 'r') as file:
        data = json.loads(file.read())
        print(data)
        update_task_table(data, db_session)
