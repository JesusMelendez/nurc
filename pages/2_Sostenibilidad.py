# pages/2_Medio_Ambiente.py
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

# --- Contenido de la Página Medio Ambiente ---
st.header("🌳 Incentivos para el Cuidado del Medio Ambiente")
st.markdown("""
Este segmento simula cómo la moneda digital puede promover comportamientos sostenibles
como el reciclaje, uso de transporte ecológico o participación en jornadas de limpieza
dentro y fuera del campus de la URC.
""")

# Parámetros específicos del segmento Medio Ambiente, usando valores de session_state
tasa_base_adopcion = st.session_state.get('tasa_base_adopcion', 0.05)
duracion_simulacion = st.session_state.get('duracion_simulacion', 24)
poblacion_total_urc = st.session_state.get('poblacion_total_urc', 25000)

st.subheader("Parámetros Medio Ambientales")
factor_conciencia_ambiental = st.slider(
    "Factor de conciencia ambiental (afecta adopción)", 0.5, 2.0, 1.0, 0.1,
    key="ambiental_factor_conciencia"
)
recompensa_reciclaje_kg = st.number_input(
    "Monedas por kg reciclado", 0.1, 5.0, 1.0, 0.1,
    key="ambiental_recompensa_reciclaje"
)
capacidad_carga_ambiental = st.number_input(
    "Máx. participantes ambientales (%)", 0.1, 1.0, 0.15, 0.05,
    key="ambiental_capacidad_carga"
) * poblacion_total_urc

# --- Simulación de Adopción Ambiental (Ecuaciones Diferenciales) ---
st.subheader("Simulación de Adopción de Incentivos Ambientales")
st.write("La simulación muestra el crecimiento de la participación en iniciativas medioambientales a lo largo del tiempo.")
t = np.linspace(0, duracion_simulacion, 100) # 't' tiene 100 puntos y abarca toda la duración
N0 = 10 # Población inicial de participantes
r_ambiental = tasa_base_adopcion * factor_conciencia_ambiental

sol_ambiental = odeint(modelo_logistico, N0, t, args=(r_ambiental, capacidad_carga_ambiental))
participantes_ambientales = sol_ambiental[:, 0]

fig_ambiental = px.line(x=t, y=participantes_ambientales,
                            labels={'x':'Meses de Simulación', 'y':'Número de Participantes Ambientales'}, # Etiqueta mejorada
                            title='Crecimiento de Participantes en Iniciativas Ambientales',
                            line_shape="spline")
fig_ambiental.update_traces(mode='lines+markers')
st.plotly_chart(fig_ambiental)

st.markdown(f"""
**Análisis:**
La participación en iniciativas ambientales incentivadas alcanzaría un máximo de aproximadamente
**{int(participantes_ambientales[-1]):,}** estudiantes. Se otorgan **{recompensa_reciclaje_kg}** monedas por kg reciclado,
promoviendo activamente un campus más verde y sostenible.
""")

# --- Visualización de Impacto Ambiental (ejemplo de datos) ---
st.subheader("Impacto Medio Ambiental Proyectado")
st.write("Se muestra un ejemplo del impacto acumulado de las acciones medioambientales en la URC.")
# Datos hipotéticos para el impacto ambiental. 't' es usado directamente para el eje de tiempo.
kg_reciclados_por_mes = (participantes_ambientales * 0.5).astype(int) # Asumiendo 0.5 kg por participante/mes
arboles_plantados_equivalente = (participantes_ambientales / 20).astype(int) # Asumiendo 1 árbol por cada 20 participantes

df_ambiental_impacto = pd.DataFrame({
    "Mes de Simulación": t, # Corregido: Usar 't' directamente para el eje de tiempo
    "Kg Reciclados (acum.)": np.cumsum(kg_reciclados_por_mes),
    "Árboles Plantados (equiv. acum.)": np.cumsum(arboles_plantados_equivalente)
})
fig_impacto_ambiental = px.area(df_ambiental_impacto, x="Mes de Simulación", y=["Kg Reciclados (acum.)", "Árboles Plantados (equiv. acum.)"],
                                    title="Impacto Medio Ambiental Acumulado",
                                    labels={"value": "Cantidad Acumulada", "variable": "Métrica de Impacto"})
st.plotly_chart(fig_impacto_ambiental)

st.markdown("""
**Métricas Clave:** La simulación proyecta una mejora tangible en la gestión de residuos y una contribución
significativa a la reforestación o reducción de la huella de carbono, fomentando una cultura de sostenibilidad en la comunidad universitaria.
""")
