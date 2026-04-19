import psutil

def get():
    freq = psutil.cpu_freq()
    return {
        'percent':   psutil.cpu_percent(interval=0.5),
        'per_core':  psutil.cpu_percent(interval=0.5, percpu=True),
        'freq_mhz':  round(freq.current, 1) if freq else 0,
        'load_avg':  [round(x, 2) for x in psutil.getloadavg()],
        'cores':     psutil.cpu_count(logical=False),
        'threads':   psutil.cpu_count(logical=True),
    }