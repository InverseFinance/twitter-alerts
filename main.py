import sched
import time
import sys
import datetime
import helpers
import threading
from flask import Flask, jsonify

app = Flask(__name__)

# define the health check endpoint
@app.route('/health')
def health_check():
    return jsonify({'status': 'ok'})

def task1():
    # write code for task 1 here
    helpers.post_stable()

def task2():
    # write code for task 2 here
    helpers.post_volatile()

def task3():
    # write code for task 3 here
    helpers.post_liquidity()

def waiting_indicator():
    symbols = ['-', '\\', '|', '/']
    while True:
        for symbol in symbols:
            sys.stdout.write("\rWaiting " + symbol)
            sys.stdout.flush()
            time.sleep(0.2)

def schedule_tasks():
    # create a scheduler instance
    s = sched.scheduler(time.time, time.sleep)

    # schedule the tasks to run at different times
    schedule_next_task_func(14,0, task1, s)
    schedule_next_task_func(15,0, task2, s)
    schedule_next_task_func(22,0, task3, s)

    # start the waiting indicator in a separate thread
    waiting_thread = threading.Thread(target=waiting_indicator, daemon=True)
    waiting_thread.start()

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

if __name__ == "__main__":
    # create a new thread object and pass it the schedule_tasks() function as the target
    t = threading.Thread(target=schedule_tasks)
    # start the thread
    t.start()
    
    # configure the production server
    from gunicorn.app.base import BaseApplication

    class MyApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            for key, value in self.options.items():
                if key in self.cfg.settings and value is not None:
                    self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {
        'bind': '0.0.0.0:8080',
        'workers': 4,
    }

    # start the production server
    MyApplication(app, options).run()
