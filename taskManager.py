
"""
Tasks Manage

Usage:
    taskManager.py add <title>
    taskManager.py list [--completed | --pending]
    taskManager.py remove [<id> | --completed | --all]
    taskManager.py update  <id> (completed | pending)

Options:
    --help          Show this screen
    --completed     Completed  tasks
    --pending       Pinding tasks
    --all           All tasks

"""
import os
import pickle
from docopt import docopt
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class Task:
    title: str
    created: str
    status: str = 'Pending'

class Dbase:
    def __init__(self, db : str) -> None:
        self.db =  db
        if not os.path.exists(self.db):
            with open(self.db, 'wb') as f:
                pickle.dump([],f)

    def load(self) -> list:
        data = []
        with open(self.db, 'rb') as f:
            data = pickle.load(f)
        return data

    def save(self, data) -> None:
        with open(self.db, 'wb') as f:
            pickle.dump(data, f)

def alert(msg : str) -> None:
    print('\033[0;91m')
    print(f'Task Manager v1.0 - {msg})')
    print('\033[0m')

def success(msg : str) -> None:
    print('\033[0;92m')
    print(f'Task Manager v1.0 - {msg}')
    print('\033[0m')



# Helper function for creating tasks lists
def tlist(data : list , state  : str = 'all') -> None:

    if state == 'completed':
        data = [item for item in data if item['status'] == 'Completed']

    if state == 'pending':
        data =  [item for item in data if item['status'] == 'Pending']

    if len(data) == 0:
         print('\033[0;91m')
         print(f'Task Manager v1.0 - Tasks list({state.capitalize()})')
         print('No tasks to show!')
         print('\033[0m')
         return

    print('\033[0;92m')
    print(f'Task Manager v1.0 - Tasks list({state.capitalize()})')
    print(f'+----+---------------------------------------------+------------+----------+')
    print(f'|{"ID":^4}|{"Title":^45}|{"Created":^12}|{"Status":^10}|')
    print(f'+----+---------------------------------------------+------------+----------+')
    for _id, task in enumerate(data):
        print(f'|{_id + 1:^4}|{task["title"]:^45}|{task["created"]:^12}|{task["status"]:^10}|')
        print(f'+----+---------------------------------------------+------------+----------+')
    print('\033[0m')

# App start point Func
def main() -> None:
    # Just for windows to activate color codes
    os.system("")

    args = docopt(__doc__, version = 'TaskManager CLI  1.0')

    # Create dtabase object
    db = Dbase('tasks.pkl')

    # Load tasks data from database
    tasks = db.load()

    # App respnse based on command lin args
    # Add new task
    if args['add']:
        title = args['<title>']
        created = datetime.today().strftime("%Y-%m-%d")
        task = asdict(Task(title, created))
        tasks.append(task)
        db.save(tasks)
        success('New task has ben added succesfuly.')

    # Remove task based on task id or tasks state
    if args['remove']:
        index : int = 0
        try:

            if args['<id>']:
                index  = int(args['<id>']) - 1
                print(index)
                tasks.pop(index)
                success(f'Task {index + 1} removed succesfuly.')


            if args['--completed']:
                tasks = [task for task in tasks if task['status'] != 'Completed']
                success('Completed tasks has been removed succesfuly.')

            if args['--all']:
                tasks = []
                success('All tasks has been removed succesfuly.')

            db.save(tasks)

        except IndexError:
            alert(f'Task can not be removed, wrong task id = {index + 1}!')
        except Exception as e:
            alert(str(e))

    # Update task using its ID
    if args['update']:
        index = int(args['<id>']) - 1
        try:
            if args['completed']:
                tasks[index]['status'] = 'Completed'
            else:
                tasks[index]['status'] = 'Pending'

            db.save(tasks)

            success(f'Task {index + 1} updated.')

        except IndexError:
            alert(f'Task can not be updated, wrong id = {index + 1}!')

    # List tasks (completed or pending or all)
    if args['list']:

        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        tasks = db.load()

        if args['--completed']:
            tlist(tasks, state='completed')
        elif args['--pending']:
            tlist(tasks, state='pending')
        else:
            tlist(tasks)

if __name__ == '__main__':
    main()
