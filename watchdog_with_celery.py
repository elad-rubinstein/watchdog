import os
from os.path import isfile, join
import time
import shutil
from celery import Celery


app = Celery('tasks', broker='amqp://localhost')

@app.task
def name_changed(old_list_of_files, new_list_of_files):
    """
    Check if a file was changed by it's name between to lists of file names
    :param old_list_of_files: An old list of file names.
    :param new_list_of_files: A new list of file names.
    """
    for i in old_list_of_files:
        if i not in new_list_of_files:
            for j in new_list_of_files:
                if j not in old_list_of_files:
                    print(i + " was changed to " + j)

@app.task
def file_deleted(old_list_of_files, new_list_of_files):
    """
    Check if a file was deleted between to lists of file names
    :param old_list_of_files: An old list of file names.
    :param new_list_of_files: A new list of file names.
    """
    for i in old_list_of_files:
        if i not in new_list_of_files:
            print(i + " was deleted!")

@app.task
def file_added(old_list_of_files, new_list_of_files):
    """
    Check if a file was added between to lists of file names and move it
    to another folder
    :param old_list_of_files: An old list of file names.
    :param new_list_of_files: A new list of file names.
    """
    for i in new_list_of_files:
        if i not in old_list_of_files:
            print(i + " was added!")
            file_caught_path = r'/home/user/elad_projects/watchdog/' + i
            new_path = r'/home/user/elad_projects/watchdog/file_caught/' + i
            shutil.move(file_caught_path, new_path)
            print(i + " was moved from " + file_caught_path + " to " + new_path)
            return False
    return True


@app.task
def main():
    """
    Execute a loop in which every time a function is called to check the status
    of files in a specific path and operate accordingly
    """
    per = True
    path = r"/home/user/elad_projects/watchdog"
    new_list_of_files = [f for f in os.listdir(path) if isfile(join(path, f))]
    while True:
        old_list_of_files = new_list_of_files
        time.sleep(0.05)
        new_list_of_files = [f for f in os.listdir(path) if isfile(join(path, f))]
        if len(old_list_of_files) == len(new_list_of_files):
            name_changed(old_list_of_files, new_list_of_files)
        elif len(old_list_of_files) > len(new_list_of_files) and per:
            file_deleted(old_list_of_files, new_list_of_files)
        elif len(old_list_of_files) < len(new_list_of_files):
            per = file_added(old_list_of_files, new_list_of_files)
        else:
            per = True


if __name__ == '__main__':
    main()
