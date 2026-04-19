# Intervalo de muestreo en segundos
INTERVAL = 2

# Umbrales para alertas (porcentaje)
THRESHOLDS = {
    'cpu':    85.0,
    'memory': 80.0,
    'disk':   90.0,
}

# Cuántos puntos históricos muestra la gráfica
HISTORY_SIZE = 60


# # config.py — modo PRUEBA
# INTERVAL = 2

# THRESHOLDS = {
#     'cpu':    5.0,   # ← casi cualquier cosa lo dispara
#     'memory': 10.0,  # ← se disparará de inmediato
#     'disk':   1.0,   # ← se disparará de inmediato
# }

# HISTORY_SIZE = 60