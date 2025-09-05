☀️Simulador de Energía Solar Fotovoltaica
Descripción del Proyecto
Este proyecto es una aplicación web desarrollada en Python para el curso de Computación Numérica de la Universidad de Antioquia. La herramienta permite modelar y simular el rendimiento de un sistema de energía solar fotovoltaica para una ubicación geográfica y fecha específicas.

La aplicación calcula la posición del sol, estima la irradiancia en una superficie inclinada, simula la producción de energía de un panel y visualiza los resultados en una interfaz web limpia e interactiva.

🚀 Funcionalidades Principales
Esta aplicación cumple con todos los requisitos de modelado y visualización del proyecto:

Parámetros de Entrada Flexibles: Permite al usuario definir la latitud, longitud, fecha, inclinación y azimut del panel para una simulación personalizada.

Cálculo de Geometría Solar: Utiliza la librería pvlib para calcular con alta precisión la altitud y el azimut del sol a lo largo del día.

Modelo de Irradiancia: Simula la irradiancia de un día de cielo despejado (clearsky) y la proyecta sobre la superficie inclinada del panel, considerando componentes directas y difusas.

Simulación de Producción Energética: Calcula la potencia eléctrica (W) generada a cada momento y la energía diaria total (kWh) utilizando el modelo PVWatts de pvlib.

Visualización de Datos Profesional: Genera una gráfica con doble eje que muestra simultáneamente la potencia generada y la altitud solar, permitiendo un análisis visual claro de la relación entre ambas variables.

🛠️ Pila Tecnológica (Tech Stack)
Backend: Python 3

Framework Web: Flask

Librerías Científicas:

pvlib: Para todos los cálculos de física solar.

pandas: Para la manipulación de datos y series de tiempo.

matplotlib: Para la generación de gráficas.

Frontend: HTML5 y CSS3

⚙️ Guía de Instalación y Ejecución
Sigue estos pasos para ejecutar el simulador en tu máquina local.

1. Prerrequisitos
Tener Python 3 instalado en tu sistema.

2. Clonar el Repositorio
Clona este repositorio en tu máquina local (o simplemente descarga los archivos):

git clone [URL_DE_TU_REPOSITORIO_EN_GITHUB]
cd MiSimuladorSolar

3. Instalar las Dependencias
Abre una terminal en la carpeta del proyecto e instala todas las librerías necesarias ejecutando el siguiente comando. Esto leerá el archivo requirements.txt e instalará todo automáticamente.

py -m pip install -r requirements.txt

4. Ejecutar la Aplicación
Una vez instaladas las dependencias, inicia el servidor web de Flask con este comando:

python app.py

5. Abrir el Simulador
Abre tu navegador web y ve a la siguiente dirección:

http://127.0.0.1:5000

📖 ¿Cómo Usar?
Introduce los Parámetros: Rellena los campos del formulario. Se han incluido valores por defecto para Medellín, Colombia.

Elige una Fecha: Selecciona la fecha para la cual deseas realizar la simulación.

Ejecuta la Simulación: Haz clic en el botón "Ejecutar Simulación".

Analiza los Resultados: La página se recargará mostrando un resumen de la energía generada y la potencia máxima, junto con una gráfica detallada de la producción del día.