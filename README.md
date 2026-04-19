# Linux Server Monitor

Dashboard web en tiempo real para monitorear recursos de servidores Linux. Construido con Python, Flask-SocketIO y Chart.js, desplegable via Docker.

---

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Python 3.11 + Flask 3.0 |
| Tiempo real | Flask-SocketIO + Eventlet |
| Recolección | psutil (lee /proc del kernel) |
| Frontend | Chart.js + Socket.IO client |
| Contenedor | Docker + Docker Compose |

---

## Métricas monitoreadas

- **CPU** — uso global, por núcleo, frecuencia MHz, load average
- **RAM** — usado / total en GB y porcentaje
- **Swap** — uso de memoria de intercambio
- **Disco** — uso por partición montada

---

## Requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo

---

## Instalación y ejecución

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/server-monitor.git
cd server-monitor

# Construir la imagen (solo la primera vez)
docker-compose build

# Levantar el proyecto
docker-compose up
```

Abrir en el navegador: **http://localhost:5000**

```bash
# Correr en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

---

## Configuración

Editar `config.py` para ajustar umbrales e intervalo:

```python
INTERVAL = 2          # segundos entre cada muestreo

THRESHOLDS = {
    'cpu':    85.0,   # % para disparar alerta
    'memory': 80.0,
    'disk':   90.0,
}
```

Aplicar cambios: `docker-compose restart`

---

## Pruebas

**Unitarias** — verifica collectors y alertas:
```bash
docker exec -it linux-monitor python test_monitor.py
```

**Estrés** — genera carga real para ver alertas en el dashboard:
```bash
docker cp stress_test.py linux-monitor:/app/stress_test.py
docker exec -it linux-monitor python stress_test.py
```

**Alertas rápidas** — bajar umbrales en `config.py` a valores bajos (ej. `cpu: 5.0`) y hacer `docker-compose restart`. Restaurar valores reales al terminar.

---

## Despliegue en servidor Linux real

```bash
# Instalar Docker en Red Hat 7 / CentOS
sudo yum install -y docker
sudo systemctl enable --now docker

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Levantar
sudo docker-compose up -d

# Abrir puerto en firewall
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

Dashboard disponible en `http://IP-DEL-SERVIDOR:5000`

---

## Autor

Marcos Chooce