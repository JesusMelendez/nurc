# pages/1_Cultural.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.integrate import odeint

# --- Función para simular el crecimiento logístico (Ecuaciones Diferenciales) ---
def modelo_logistico(N, t, r, K):
    """
    N: Población actual
    t: Tiempo
    r: Tasa de crecimiento intrínseca
    K: Capacidad de carga (población máxima)
    """
    dndt = r * N * (1 - N / K)
    return dndt

# --- Contenido de la Página Cultural ---
st.header("🎭 Incentivos para el Desarrollo Cultural")
st.markdown("""
Este segmento simula cómo la moneda digital incentiva la participación en actividades culturales
como asistencia a eventos, talleres o creación artística dentro de la URC.
""")

# Parámetros específicos del segmento Cultural, usando valores de session_state si están disponibles
# Se obtienen los parámetros globales de st.session_state
tasa_base_adopcion = st.session_state.get('tasa_base_adopcion', 0.05)
duracion_simulacion = st.session_state.get('duracion_simulacion', 24)
poblacion_total_urc = st.session_state.get('poblacion_total_urc', 25000)


st.subheader("Parámetros Culturales")
factor_interes_cultural = st.slider(
    "Factor de interés cultural (afecta adopción)", 0.5, 2.0, 1.0, 0.1,
    key="cultural_factor_interes" # Clave única para este slider
)
recompensa_evento_cultural = st.number_input(
    "Monedas por asistencia a evento", 1, 100, 10,
    key="cultural_recompensa_evento"
)
capacidad_carga_cultural = st.number_input(
    "Máx. participantes culturales (%)", 0.1, 1.0, 0.2, 0.05,
    key="cultural_capacidad_carga"
) * poblacion_total_urc # Se multiplica por la población total de la URC

# --- Simulación de Adopción Cultural (Ecuaciones Diferenciales) ---
st.subheader("Simulación de Adopción de Incentivos Culturales")
st.write("La simulación muestra el crecimiento de la participación cultural incentivada a lo largo del tiempo.")
t = np.linspace(0, duracion_simulacion, 100) # 't' tiene 100 puntos y abarca toda la duración
N0 = 10 # Población inicial de participantes
r_cultural = tasa_base_adopcion * factor_interes_cultural # Tasa de crecimiento intrínseca ajustada

sol_cultural = odeint(modelo_logistico, N0, t, args=(r_cultural, capacidad_carga_cultural))
participantes_culturales = sol_cultural[:, 0]

fig_cultural = px.line(x=t, y=participantes_culturales,
                       labels={'x':'Meses de Simulación', 'y':'Número de Participantes Culturales'}, # Etiqueta mejorada
                       title='Crecimiento de Participantes en Actividades Culturales',
                       line_shape="spline") # Añade un poco de suavizado a la línea
fig_cultural.update_traces(mode='lines+markers')
st.plotly_chart(fig_cultural)

st.markdown(f"""
**Análisis:**
Según la simulación, la participación en actividades culturales incentivadas alcanzaría un máximo de aproximadamente
**{int(participantes_culturales[-1]):,}** estudiantes. Se otorgan **{recompensa_evento_cultural}** monedas por evento
asistido, lo que busca fomentar la interacción y el aprecio cultural.
""")

# --- Visualización de Impacto Cultural (ejemplo de datos) ---
st.subheader("Impacto Social Cultural Proyectado")
st.write("Se muestra un ejemplo del impacto acumulado de la participación cultural en la URC.")
# Datos hipotéticos para el impacto cultural. 't' es usado directamente para el eje de tiempo.
eventos_por_mes = (participantes_culturales / 10).astype(int) # Asumiendo 10 estudiantes por evento en promedio
obras_creadas = (participantes_culturales / 50).astype(int) # Asumiendo una obra por cada 50 participantes

df_cultural_impacto = pd.DataFrame({
    "Mes de Simulación": t, # Corregido: Usar 't' directamente para el eje de tiempo
    "Eventos Asistidos (acum.)": np.cumsum(eventos_por_mes),
    "Obras/Contenido Creado (acum.)": np.cumsum(obras_creadas)
})
fig_impacto_cultural = px.area(df_cultural_impacto, x="Mes de Simulación", y=["Eventos Asistidos (acum.)", "Obras/Contenido Creado (acum.)"],
                               title="Impacto Cultural Acumulado",
                               labels={"value": "Cantidad Acumulada", "variable": "Métrica de Impacto"})
st.plotly_chart(fig_impacto_cultural)

st.markdown("""
**Métricas Clave:** La simulación proyecta un aumento significativo en la asistencia a eventos y la generación
de contenido cultural original, demostrando cómo la moneda puede enriquecer el ambiente artístico y creativo de la universidad.
""")
df_cultural_impacto