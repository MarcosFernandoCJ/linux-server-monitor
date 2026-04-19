import psutil

def get():
    results = []
    for part in psutil.disk_partitions(all=False):
        try:
            u = psutil.disk_usage(part.mountpoint)
            results.append({
                'mountpoint': part.mountpoint,
                'percent':    u.percent,
                'used_gb':    round(u.used  / 1024**3, 2),
                'total_gb':   round(u.total / 1024**3, 2),
            })
        except PermissionError:
            continue
    return results