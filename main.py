
from scheduler import schedule_tasks
from helpers import monitor_deposits, monitor_borrows,monitor_tvl
from flask import Flask, jsonify
from threading import Thread

app = Flask(__name__)

# define the health check endpoint
@app.route('/health')
def health_check():
    return jsonify({'status': 'ok'})


if __name__ == "__main__":
    # create a new thread object and pass it the schedule_tasks() function as the target
    #t = Thread(target=schedule_tasks)
    # start the thread
    #t.start()

    deposits_alert_ids = [97,246,277,282,286]
    deposits_monitoring_thread = Thread(target=monitor_deposits, args=(deposits_alert_ids,))
    deposits_monitoring_thread.start()
    
    borrows_alert_ids = [94,244,279,283,288]
    borrows_monitoring_thread = Thread(target=monitor_borrows, args=(borrows_alert_ids,))
    borrows_monitoring_thread.start()
    
    #init_value=13000000
    #tvl_monitoring_thread = Thread(target=monitor_tvl, args=(init_value,))
    #tvl_monitoring_thread.start()

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
