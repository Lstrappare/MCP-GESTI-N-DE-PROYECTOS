# 🦆 Servidor MCP de Gestión de Proyectos

Este repositorio contiene el servidor de herramientas basado en el Model Context Protocol (MCP) para automatizar la gestión del proyecto MINTRANET.

---

## ✅ Requisitos previos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu computadora:

- [Node.js](https://nodejs.org/) (versión 18 o superior recomendada)
- [pnpm](https://pnpm.io/installation) — instalable con:
  ```bash
  npm install -g pnpm
  ```
- Python 3 con `venv` disponible

---

## 📦 1. Clonar el repositorio

```bash
git clone https://github.com/JosaSeCisneros/MCP-GESTI-N-DE-PROYECTOS.git
cd MCP-GESTI-N-DE-PROYECTOS
```

---

## 🐍 2. Activar el entorno virtual de Python

El servidor utiliza Python, por lo que necesitas activar el entorno virtual antes de iniciar.

### En macOS / Linux:

```bash
source venv/bin/activate
```

### En Windows (PowerShell o CMD):

```bash
venv\Scripts\activate
```

> Sabrás que está activo cuando veas `(venv)` al inicio de tu línea de comandos.

---
## 📥 3. Instalar dependencias
Una vez activado el entorno virtual, debes instalar las librerías necesarias del proyecto (solo la primera vez):
```bash
pip install -r requirements.txt
```

---
## 🔌 4. Iniciar el inspector del servidor

Con el entorno virtual activo, ejecuta el siguiente comando para levantar el servidor con el inspector de MCP:

```bash
pnpm dlx @modelcontextprotocol/inspector python server.py
```

Este comando:
1. Descarga y ejecuta el inspector de MCP usando `pnpm`
2. Lanza `server.py` como el servidor de pruebas

---

## 🌐 5. Acceder al inspector

Una vez que el servidor esté corriendo, abre tu navegador en la dirección que aparezca en la terminal (normalmente algo como `http://localhost:5173`).

---

## 🛑 Detener el servidor

Para detener el servidor, presiona `Ctrl + C` en la terminal.

Para desactivar el entorno virtual:

```bash
deactivate
```

---

## 📝 Notas

- Si el comando `pnpm` no se reconoce, verifica que esté instalado globalmente con `npm install -g pnpm`.
- Si `python` no funciona, intenta con `python3` en macOS/Linux.
- Si tienes dudas, contacta a José Manuel.