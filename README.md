
# **Nombre de la Aplicación**

Breve descripción de la aplicación.

---

## **Tabla de Contenidos**

- [Descripción](#descripción)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
  - [Clonar el Repositorio](#clonar-el-repositorio)
  - [Backend (FastAPI)](#backend-fastapi)
  - [Frontend (Next.js)](#frontend-nextjs)
- [Ejecución de la Aplicación](#ejecución-de-la-aplicación)
  - [Ejecutar el Backend](#ejecutar-el-backend)
  - [Ejecutar el Frontend](#ejecutar-el-frontend)
- [Uso](#uso)
- [Rutas y Endpoints](#rutas-y-endpoints)
  - [Backend (API)](#backend-api)
- [Notas Adicionales](#notas-adicionales)
- [Autores](#autores)
- [Licencia](#licencia)

---

## **Descripción**

Esta aplicación es un proyecto que utiliza **FastAPI** para el backend y **Next.js** para el frontend. Proporciona una interfaz web para realizar cálculos de convección y otros procesos relacionados con la ingeniería química. El backend se ejecuta en el puerto **8000**, mientras que el frontend se ejecuta en el puerto **3000**.

---

## **Tecnologías Utilizadas**

- **Python 3.x**
- **FastAPI**: Framework moderno y de alto rendimiento para construir APIs con Python.
- **Uvicorn**: Servidor ASGI para Python, utilizado para ejecutar aplicaciones FastAPI.
- **Next.js**: Framework de React para el desarrollo de aplicaciones web del lado del servidor.
- **Node.js**: Entorno de ejecución para JavaScript en el servidor.
- **NPM**: Gestor de paquetes para Node.js.
- **NumPy**, **SciPy**, **SymPy**: Librerías para cálculos matemáticos y científicos en Python.

---

## **Requisitos Previos**

Antes de comenzar, asegúrate de tener instaladas las siguientes herramientas:

- **Python 3.x** y **pip**
- **Node.js** y **npm**
- **Git** (opcional, para clonar el repositorio)
- **Virtualenv** (opcional, para entornos virtuales de Python)

---

## **Instalación**

### **Clonar el Repositorio**

Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/tuusuario/tuaplicacion.git
cd tuaplicacion
```

### **Backend (FastAPI)**

1. Navega al directorio del backend:

   ```bash
   cd backend
   ```

2. (Opcional) Crea y activa un entorno virtual:

   - **En Windows:**

     ```bash
     python -m venv venv
     venv\Scriptsctivate
     ```

   - **En Unix/MacOS:**

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

### **Frontend (Next.js)**

1. Navega al directorio del frontend:

   ```bash
   cd ../frontend
   ```

2. Instala las dependencias:

   ```bash
   npm install
   ```

---

## **Ejecución de la Aplicación**

### **Ejecutar el Backend**

1. Asegúrate de que el entorno virtual esté activado (si creaste uno).

2. Navega al directorio del backend si no lo has hecho:

   ```bash
   cd backend
   ```

3. Ejecuta el servidor:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Esto iniciará el servidor en `http://localhost:8000`.

### **Ejecutar el Frontend**

1. Abre una nueva terminal.

2. Navega al directorio del frontend:

   ```bash
   cd frontend
   ```

3. Ejecuta la aplicación:

   ```bash
   npm run dev
   ```

   Esto iniciará la aplicación en `http://localhost:3000`.

---

## **Uso**

Abre tu navegador y visita `http://localhost:3000` para acceder a la interfaz de usuario de la aplicación. Desde allí, puedes interactuar con las diferentes funcionalidades que ofrece la aplicación, como realizar cálculos de convección.

---

## **Rutas y Endpoints**

### **Backend (API)**

- **Documentación Swagger UI**: `http://localhost:8000/docs`
- **Documentación ReDoc**: `http://localhost:8000/redoc`

#### **Endpoints Disponibles**

- **POST** `/convection/calculate`

  Realiza cálculos de convección basados en los datos proporcionados.

  **Cuerpo de la Solicitud (JSON):**

  ```json
  {
    "thickness": 0.087,
    "thermal_diffusivity": 0.000117,
    "conductivity_coefficient": 401.0,
    "convection_coefficient": 80.0,
    "initial_temperature": 118.0,
    "ambient_temperature": 22.0,
    "density": 8933.0,
    "specific_heat": 385.0,
    "distance": 1e-12,
    "time": 840.0,
    "iterations": 200,
    "biot": 0.008678304,
    "geometry": "sphere"
  }
  ```

  **Respuesta Exitosa (JSON):**

  ```json
  {
    "message": "Success",
    "data": {
      "thickness": 0.087,
      "thermal_diffusivity": 0.000117,
      "conductivity_coefficient": 401.0,
      "convection_coefficient": 80.0,
      "initial_temperature": 118.0,
      "ambient_temperature": 22.0,
      "density": 8933.0,
      "specific_heat": 385.0,
      "distance": 1e-12,
      "time": 840.0,
      "iterations": 200,
      "biot": 0.008678304,
      "geometry": "sphere",
      "q_max": -113837.58574472205,
      "calc1": {
        "value_a": 1.0026836144386382,
        "value_theta_o": 0.24921177579159925,
        "value_theta": 0.24921177579159925,
        "value_q": 0.24854443650606772
      },
      "calc2": {
        "value_a": -0.003955471804134711,
        "value_theta_o": -0.0,
        "value_theta": -0.0,
        "value_q": 0.0
      },
      "calc3": {
        "value_a": 0.00226515114101885,
        "value_theta_o": 0.0,
        "value_theta": 0.0,
        "value_q": 0.0
      },
      "lamb": {
        "lambda1": 0.1637181888706048,
        "lambda2": 4.495340795963502,
        "lambda3": 7.726375204883762
      },
      "value_a": 1.0009932937755224,
      "value_theta_o": 0.24921177579159925,
      "value_theta": 0.24921177579159925,
      "value_q": 0.24854443650606772,
      "tem": 45.92433047599353,
      "q": -85543.88714258894
    }
  }
  ```

---

## **Notas Adicionales**

- **Variables de Entorno**: Si es necesario, configura las variables de entorno en ambos proyectos para apuntar al backend y frontend correctos.

- **Manejo de Errores**: El servidor retornará errores HTTP adecuados en caso de datos inválidos o errores internos.

- **Construcción para Producción**:

  - **Backend**: Ejecuta el servidor sin la opción `--reload`.

    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

  - **Frontend**: Construye y ejecuta la aplicación en modo producción.

    ```bash
    npm run build
    npm start
    ```

---

## **Autores**

- **Tu Nombre** - *Desarrollador Principal* - [Tu GitHub](https://github.com/tuusuario)

---

## **Licencia**

Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE](LICENSE) para más detalles.

---

**¡Gracias por utilizar nuestra aplicación!** Si tienes alguna pregunta o sugerencia, no dudes en contactarnos.
