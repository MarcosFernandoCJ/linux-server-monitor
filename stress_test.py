import threading
import psutil
import time

def cpu_stress(duration_seconds=30):
    """Usa un núcleo al 100% durante N segundos."""
    print(f"Estresando CPU por {duration_seconds}s...")
    end = time.time() + duration_seconds
    while time.time() < end:
        pass  # bucle vacío = 100% CPU en ese núcleo

def ram_stress(mb=200, duration_seconds=20):
    """Reserva N MB de RAM durante N segundos."""
    print(f"Reservando {mb}MB de RAM por {duration_seconds}s...")
    data = bytearray(mb * 1024 * 1024)  # reserva memoria real
    time.sleep(duration_seconds)
    del data
    print("RAM liberada")

def mostrar_metricas(duration_seconds=35):
    """Muestra métricas en consola mientras dura la prueba."""
    end = time.time() + duration_seconds
    while time.time() < end:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        bar_cpu = '█' * int(cpu / 5) + '░' * (20 - int(cpu / 5))
        bar_mem = '█' * int(mem / 5) + '░' * (20 - int(mem / 5))
        print(f"CPU [{bar_cpu}] {cpu:5.1f}%  |  RAM [{bar_mem}] {mem:5.1f}%")

if __name__ == '__main__':
    print("=== Prueba de estrés iniciada ===")
    print("Abre http://localhost:5000 y observa las alertas\n")

    # Lanza CPU stress en hilos separados (uno por núcleo lógico)
    nucleos = psutil.cpu_count(logical=True)
    hilos_cpu = []
    for i in range(nucleos):
        t = threading.Thread(target=cpu_stress, args=(30,))
        t.daemon = True
        hilos_cpu.append(t)

    # Lanza RAM stress
    hilo_ram = threading.Thread(target=ram_stress, args=(300, 25))
    hilo_ram.daemon = True

    # Arranca todo
    for t in hilos_cpu:
        t.start()
    hilo_ram.start()

    # Muestra métricas en consola
    mostrar_metricas(35)

    print("\n=== Prueba terminada ===")