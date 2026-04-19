import psutil

def get():
    r = psutil.virtual_memory()
    s = psutil.swap_memory()
    return {
        'percent':       r.percent,
        'used_gb':       round(r.used   / 1024**3, 2),
        'total_gb':      round(r.total  / 1024**3, 2),
        'available_gb':  round(r.available / 1024**3, 2),
        'swap_percent':  s.percent,
        'swap_used_gb':  round(s.used   / 1024**3, 2),
    }