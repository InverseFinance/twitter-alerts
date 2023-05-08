
import sched
import time
import sys
import datetime
from helpers import post_stable, post_volatile, post_liquidity


def task1():
    # write code for task 1 here
    post_stable()

def task2():
    # write code for task 2 here
    post_volatile()

def task3():
    # write code for task 3 here
    post_liquidity()


def schedule_tasks():
    # create a scheduler instance
    s = sched.scheduler(time.time, time.sleep)

    # schedule the tasks to run at different times
    schedule_next_task_func(14,0, task1, s)
    schedule_next_task_func(15,0, task2, s)
    schedule_next_task_func(22,0, task3, s)

    # start the scheduler
    s.run()

def schedule_next_task_func(hour, minute, task_func, s):
    # get the current time
    now = datetime.datetime.now()

    # compute the next time the task should run
    next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if next_run < now:
        next_run += datetime.timedelta(days=1)

    # calculate the delay until the next run
    delay = (next_run - now).total_seconds()

    # schedule the next run of the task
    s.enter(delay, 1, run_task, (hour, minute, task_func, s))

def run_task(hour, minute, task_func, s):
    # execute the task
    task_func()

    # schedule the next run of the task
    schedule_next_task_func(hour, minute, task_func, s)