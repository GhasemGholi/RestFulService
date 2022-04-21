from core import app_api, app_users
import threading

def run_app_api():
    app_api.run(host='127.0.0.1', port=5000, debug=False, threaded=True)

def run_app_users():
    app_users.run(host='127.0.0.1', port=5001, debug=False, threaded=True)

if __name__ == '__main__':
        # Executing the Threads seperatly.
    threading.Thread(target=run_app_api).start()
    threading.Thread(target=run_app_users).start()