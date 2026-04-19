from config import THRESHOLDS

def check(metrics: dict) -> list[dict]:
    """Devuelve lista de alertas activas. Lista vacía = todo OK."""
    alerts = []

    if metrics['cpu']['percent'] > THRESHOLDS['cpu']:
        alerts.append({
            'type':    'danger',
            'metric':  'CPU',
            'value':   metrics['cpu']['percent'],
            'threshold': THRESHOLDS['cpu'],
        })

    if metrics['memory']['percent'] > THRESHOLDS['memory']:
        alerts.append({
            'type':    'danger',
            'metric':  'RAM',
            'value':   metrics['memory']['percent'],
            'threshold': THRESHOLDS['memory'],
        })

    for disk in metrics['disk']:
        if disk['percent'] > THRESHOLDS['disk']:
            alerts.append({
                'type':    'warning',
                'metric':  f"Disco {disk['mountpoint']}",
                'value':   disk['percent'],
                'threshold': THRESHOLDS['disk'],
            })

    return alerts