"""
Implement a watchdog using Celery
"""

from celery import Celery
from simple_watchdog import *


app = Celery('tasks', broker='amqp://localhost')


@app.task
def file_added(old_list_of_files: list, new_list_of_files: list) -> bool:

    """
    Check if a file was added between to lists of file names and move it
    to another folder
    :param old_list_of_files: An old list of file names.
    :param new_list_of_files: A new list of file names.
    """
    for i in new_list_of_files:
        if i not in old_list_of_files:
            print(i + " was added!")
            file_caught_path = join(Path(), i)
            new_path = join(Path(), "file_caught", i)
            shutil.move(file_caught_path, new_path)
            print(i + " was moved from " + file_caught_path + " to " + new_path)
            return False
    return True


main()
