# ==============================================================================
# PROYECTO FINAL: SIMULADOR DE ENERGÍA SOLAR (VERSIÓN CON GRÁFICA MEJORADA)
# Este script crea una aplicación web completa que cumple con todos los
# requisitos de software del proyecto de Computación Numérica.
# ==============================================================================

# --- Bloque 1: Importación de Librerías Esenciales ---
from flask import Flask, render_template, request, url_for
import pandas as pd
import pvlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import base64

# --- Bloque 2: Configuración Inicial de la Aplicación ---
app = Flask(__name__)
plt.ioff()

# --- Bloque 3: Función Principal de Simulación ("El Cerebro") ---
def ejecutar_simulacion_completa(lat, lon, fecha_obj, tilt, azimut):
    """
    Realiza una simulación solar completa y genera resultados y una gráfica mejorada.
    """
    # 3.1: Definir la ubicación y el rango de tiempo.
    tz = 'America/Bogota'
    loc = pvlib.location.Location(latitude=lat, longitude=lon, tz=tz)
    times = pd.date_range(start=fecha_obj, end=fecha_obj + pd.Timedelta(days=1), freq='15min', tz=tz)

    # 3.2: Modelo de Irradiancia de Cielo Despejado (Clear-Sky).
    clearsky = loc.get_clearsky(times)

    # 3.3: Cálculo de la Geometría Solar.
    solar_position = loc.get_solarposition(times)

    # 3.4: Cálculo de la Irradiancia en la Superficie Inclinada del Panel.
    total_irrad = pvlib.irradiance.get_total_irradiance(
        surface_tilt=tilt, surface_azimuth=azimut,
        solar_zenith=solar_position['apparent_zenith'], solar_azimuth=solar_position['azimuth'],
        dni=clearsky['dni'], ghi=clearsky['ghi'], dhi=clearsky['dhi']
    )

    # 3.5: Simulación de la Potencia Eléctrica del Panel (Modelo PVWatts).
    power_dc = pvlib.pvsystem.pvwatts_dc(
        g_poa_effective=total_irrad['poa_global'], temp_cell=25.0,
        pdc0=250, gamma_pdc=-0.004
    )

    # 3.6: Cálculo de los Resultados Numéricos Finales.
    energia_diaria = power_dc.sum() / (4 * 1000)
    potencia_maxima = power_dc.max()
    resultados_numericos = {
        'energia_diaria': f"{energia_diaria:.2f} kWh",
        'potencia_maxima': f"{potencia_maxima:.2f} W"
    }

    # ==============================================================================
    # --- Bloque 3.7: GENERACIÓN DE LA GRÁFICA MEJORADA ---
    # ==============================================================================
    fig, ax1 = plt.subplots(figsize=(11, 6)) # Un poco más grande para mayor claridad
    
    # Eje 1 (Izquierda): Potencia Generada (W).
    color1 = 'royalblue'
    ax1.set_ylabel('Potencia Generada (W)', color=color1, fontsize=12, fontweight='bold')
    line1, = ax1.plot(power_dc.index, power_dc, color=color1, lw=2.5, marker='o', markersize=4, label='Potencia Generada (W)')
    ax1.tick_params(axis='y', labelcolor=color1)
    # Rellenamos el área debajo de la curva de potencia para un mejor efecto visual.
    ax1.fill_between(power_dc.index, power_dc, color=color1, alpha=0.1)

    # Eje 2 (Derecha): Altitud Solar (°).
    ax2 = ax1.twinx()
    color2 = 'darkorange'
    ax2.set_ylabel('Altitud Solar (°)', color=color2, fontsize=12, fontweight='bold')
    line2, = ax2.plot(solar_position.index, solar_position['apparent_elevation'], color=color2, lw=2.5, linestyle='--', label='Altitud Solar (°)')
    ax2.tick_params(axis='y', labelcolor=color2)

    # Se formatea el eje X para que muestre la hora claramente.
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.set_xlabel('Hora del Día', fontsize=12, fontweight='bold')
    
    # Se mejora la rejilla
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # Se añaden títulos y una leyenda combinada.
    plt.title('Simulación de Producción Solar vs. Altitud del Sol', fontsize=16, fontweight='bold', pad=20)
    fig.legend(handles=[line1, line2], loc='upper center', bbox_to_anchor=(0.5, 0.95), ncol=2, frameon=False)
    fig.tight_layout(rect=[0, 0, 1, 0.9]) # Ajusta el layout para dar espacio a la leyenda

    # 3.8: Conversión de la Gráfica a formato web (Base64).
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100) # Aumentamos un poco la resolución
    plt.close(fig)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf8')

    return resultados_numericos, plot_url

# --- Bloque 4: Rutas de la Aplicación Web (Sin cambios) ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/simular', methods=['POST'])
def simular():
    try:
        lat = float(request.form['latitud'])
        lon = float(request.form['longitud'])
        fecha_str = request.form['fecha']
        tilt = float(request.form['inclinacion'])
        azimut = float(request.form['azimut'])
        
        tz = 'America/Bogota'
        fecha_obj = pd.to_datetime(fecha_str).tz_localize(tz)
        
        resultados, plot_url = ejecutar_simulacion_completa(lat, lon, fecha_obj, tilt, azimut)
        
        return render_template('index.html', resultados=resultados, plot_url=plot_url)
    except Exception as e:
        error_msg = f"Ocurrió un error inesperado: {e}. Por favor, verifica que todos los valores sean correctos."
        return render_template('index.html', error=error_msg)

# --- Bloque 5: Arranque del Servidor (Sin cambios) ---
if __name__ == '__main__':
    app.run(debug=True)