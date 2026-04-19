import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO
from collectors import cpu, memory, disk
from core.alerts import check
from config import INTERVAL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'monitor-secret'
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')

def collect_and_emit():
    """Bucle infinito: recolecta métricas y las emite por WebSocket."""
    while True:
        metrics = {
            'cpu':    cpu.get(),
            'memory': memory.get(),
            'disk':   disk.get(),
        }
        alerts = check(metrics)
        socketio.emit('metrics', metrics)
        if alerts:
            socketio.emit('alerts', alerts)
        eventlet.sleep(INTERVAL)

@app.route('/')
def index():
    return render_template('dashboard.html')

@socketio.on('connect')
def on_connect():
    print('Cliente conectado al dashboard')

if __name__ == '__main__':
    # Inicia el bucle de emisión en un hilo verde (eventlet)
    socketio.start_background_task(collect_and_emit)
socketio.run(
    app,
    host='0.0.0.0',
    port=5000,
    debug=False,   
    use_reloader=False 
)