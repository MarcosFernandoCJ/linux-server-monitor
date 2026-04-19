# test_monitor.py
import sys
import psutil
from collectors import cpu, memory, disk
from core.alerts import check

# ── colores para la consola ──────────────────────────────
OK   = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"
INFO = "\033[94m→\033[0m"

def assert_test(nombre, condicion, detalle=""):
    if condicion:
        print(f"  {OK}  {nombre}")
    else:
        print(f"  {FAIL}  {nombre} — {detalle}")
        sys.exit(1)

# ── Test 1: CPU collector ────────────────────────────────
print("\n[1] CPU collector")
datos_cpu = cpu.get()
print(f"  {INFO} Resultado: {datos_cpu}")

assert_test("retorna dict",        isinstance(datos_cpu, dict))
assert_test("tiene 'percent'",     'percent'  in datos_cpu)
assert_test("CPU entre 0-100",     0 <= datos_cpu['percent'] <= 100,
            f"valor: {datos_cpu['percent']}")
assert_test("tiene 'per_core'",    isinstance(datos_cpu['per_core'], list))
assert_test("tiene 'load_avg'",    'load_avg' in datos_cpu)
assert_test("load_avg tiene 3",    len(datos_cpu['load_avg']) == 3)

# ── Test 2: Memory collector ─────────────────────────────
print("\n[2] Memory collector")
datos_mem = memory.get()
print(f"  {INFO} Resultado: {datos_mem}")

assert_test("retorna dict",        isinstance(datos_mem, dict))
assert_test("tiene 'percent'",     'percent'  in datos_mem)
assert_test("RAM entre 0-100",     0 <= datos_mem['percent'] <= 100)
assert_test("total_gb > 0",        datos_mem['total_gb'] > 0,
            f"valor: {datos_mem['total_gb']}")
assert_test("usado <= total",      datos_mem['used_gb'] <= datos_mem['total_gb'])

# ── Test 3: Disk collector ───────────────────────────────
print("\n[3] Disk collector")
datos_disk = disk.get()
print(f"  {INFO} Particiones encontradas: {len(datos_disk)}")

assert_test("retorna lista",       isinstance(datos_disk, list))
assert_test("al menos 1 partición", len(datos_disk) > 0)
assert_test("tiene 'mountpoint'",  'mountpoint' in datos_disk[0])
assert_test("tiene 'percent'",     'percent'    in datos_disk[0])
assert_test("disco entre 0-100",   0 <= datos_disk[0]['percent'] <= 100)

# ── Test 4: Sistema de alertas — sin alerta ───────────────
print("\n[4] Alerts — sin alertas (umbrales altos)")
metricas_ok = {
    'cpu':    {'percent': 10.0},
    'memory': {'percent': 20.0},
    'disk':   [{'mountpoint': '/', 'percent': 30.0}]
}

class CfgFalsa:
    """Simula el objeto config con umbrales altos."""
    def __getitem__(self, key):
        return {'cpu': 85.0, 'memory': 80.0, 'disk': 90.0}

alertas = check(metricas_ok)
assert_test("0 alertas con métricas normales", len(alertas) == 0,
            f"se generaron {len(alertas)} alertas inesperadas")

# ── Test 5: Sistema de alertas — con alerta ───────────────
print("\n[5] Alerts — con alertas (umbrales superados)")
metricas_altas = {
    'cpu':    {'percent': 95.0},
    'memory': {'percent': 90.0},
    'disk':   [{'mountpoint': '/', 'percent': 95.0}]
}
alertas = check(metricas_altas)
print(f"  {INFO} Alertas generadas: {[a['metric'] for a in alertas]}")

assert_test("genera alerta de CPU",   any(a['metric'] == 'CPU'  for a in alertas))
assert_test("genera alerta de RAM",   any(a['metric'] == 'RAM'  for a in alertas))
assert_test("genera alerta de disco", any('Disco' in a['metric'] for a in alertas))
assert_test("alerta tiene 'type'",    'type'  in alertas[0])
assert_test("alerta tiene 'value'",   'value' in alertas[0])

# ── Resumen ───────────────────────────────────────────────
print("\n" + "─" * 40)
print("  Todos los tests pasaron correctamente")
print("─" * 40 + "\n")