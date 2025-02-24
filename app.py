from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
import logging
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

def update_time():
    while True:
        now = datetime.now().strftime('%H:%M:%S')
        socketio.emit('update_time', {'time': now}, namespace='/')
        logger.info(f'Updated time: {now}')
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    logger.info(f'Client connected')
    emit('update_time', {'time': datetime.now().strftime('%H:%M:%S')})

@socketio.on('disconnect')
def handle_disconnect():
    logger.info(f'Client disconnected')

if __name__ == '__main__':
    thread = threading.Thread(target=update_time)
    thread.daemon = True
    thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)
