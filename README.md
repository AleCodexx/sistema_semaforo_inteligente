# 🚦 Sistema de Semáforo Inteligente

Este proyecto implementa un sistema inteligente de gestión de semáforos que:

✅ Detecta vehículos de emergencia (ambulancia, policía)  
✅ Detecta y cuenta peatones en tiempo real  
✅ Predice el nivel de congestión vehicular (bajo, alto)  
✅ Calcula automáticamente el tiempo verde peatonal recomendado

---

## 📝 **Requisitos**

- **Python** 3.10 o superior  
- Entorno virtual configurado (opcional pero recomendado)

---

## ⚙️ **Instalación y configuración**

1. **Clona el repositorio o descarga los archivos.**

2. Abre una terminal en la carpeta raíz del proyecto y crea un entorno virtual:

    ```bash
    python -m venv venv


3. Activa el entorno virtual:
    . Windows
        venv\Scripts\activate
        
    . Linux/Mac/Windows
        source venv/bin/activate

4. Instala las dependencias:

    pip install -r requirements.txt

## 🚀 ** Ejecución**

1. Asegúrate de tener conectada tu cámara web.

2. Ejecuta el sistema principal:

    python main.py

3. La ventana mostrará:

    🚶 Peatones detectados (rectángulo verde)

    🚨 Vehículos de emergencia detectados (rectángulo rojo)

    ⏱️ Tiempo verde peatonal sugerido

    🚗 Nivel de congestión predicho

4. Presiona la tecla 'q' para cerrar la ventana y finalizar el sistema.
