# pages/3_Desempeno_Escolar.py
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

# --- Contenido de la Página Desempeño Escolar ---
st.header("📚 Incentivos para el Desempeño Escolar")
st.markdown("""
Este segmento simula cómo la moneda digital puede motivar la mejora académica a través de
recompensas por buenas calificaciones, asistencia, participación en proyectos de investigación o tutorías
dentro de la URC.
""")

# Parámetros específicos del segmento Desempeño Escolar, usando valores de session_state
tasa_base_adopcion = st.session_state.get('tasa_base_adopcion', 0.05)
duracion_simulacion = st.session_state.get('duracion_simulacion', 24)
poblacion_total_urc = st.session_state.get('poblacion_total_urc', 25000)

st.subheader("Parámetros de Desempeño Escolar")
factor_motivacion_academica = st.slider(
    "Factor de motivación académica (afecta adopción)", 0.5, 2.0, 1.0, 0.1,
    key="academico_factor_motivacion"
)
recompensa_calif_excelente = st.number_input(
    "Monedas por calificación > 90/100", 20, 200, 50,
    key="academico_recompensa_calif"
)
capacidad_carga_academica = st.number_input(
    "Máx. estudiantes con mejora académica (%)", 0.1, 1.0, 0.3, 0.05,
    key="academico_capacidad_carga"
) * poblacion_total_urc


# --- Simulación de Adopción Académica (Ecuaciones Diferenciales) ---
st.subheader("Simulación de Mejora en Desempeño Escolar")
st.write("La simulación muestra el crecimiento de estudiantes con desempeño escolar mejorado o excelente a lo largo del tiempo.")
t = np.linspace(0, duracion_simulacion, 100) # 't' tiene 100 puntos y abarca toda la duración
N0 = 10 # Población inicial
r_academica = tasa_base_adopcion * factor_motivacion_academica

sol_academica = odeint(modelo_logistico, N0, t, args=(r_academica, capacidad_carga_academica))
participantes_academicos = sol_academica[:, 0]

fig_academica = px.line(x=t, y=participantes_academicos,
                            labels={'x':'Meses de Simulación', 'y':'Número de Estudiantes con Desempeño Mejorado'}, # Etiqueta mejorada
                            title='Crecimiento de Estudiantes con Desempeño Académico Mejorado',
                            line_shape="spline")
fig_academica.update_traces(mode='lines+markers')
st.plotly_chart(fig_academica)

st.markdown(f"""
**Análisis:**
El número de estudiantes con desempeño académico mejorado/excelente alcanzaría un máximo de
aproximadamente **{int(participantes_academicos[-1]):,}** estudiantes. Se otorgan
**{recompensa_calif_excelente}** monedas por una calificación mayor a 90/100, incentivando así la excelencia académica.
""")

# --- Visualización de Impacto Académico (ejemplo de datos) ---
st.subheader("Impacto en el Desempeño Escolar Proyectado")
st.write("Se muestra un ejemplo del impacto acumulado en el desempeño escolar en la URC.")
# Datos hipotéticos para el impacto académico. 't' es usado directamente para el eje de tiempo.
proyectos_investigacion_por_mes = (participantes_academicos / 10).astype(int) # 1 proyecto por cada 10 estudiantes
tutorias_impartidas = (participantes_academicos / 5).astype(int) # 1 tutoria por cada 5 estudiantes

df_academico_impacto = pd.DataFrame({
    "Mes de Simulación": t, # Corregido: Usar 't' directamente para el eje de tiempo
    "Proyectos Investigación (acum.)": np.cumsum(proyectos_investigacion_por_mes),
    "Tutorías Impartidas (acum.)": np.cumsum(tutorias_impartidas)
})
fig_impacto_academico = px.area(df_academico_impacto, x="Mes de Simulación", y=["Proyectos Investigación (acum.)", "Tutorías Impartidas (acum.)"],
                                    title="Impacto en el Desempeño Escolar Acumulado",
                                    labels={"value": "Cantidad Acumulada", "variable": "Métrica de Impacto"})
st.plotly_chart(fig_impacto_academico)

st.markdown("""
**Métricas Clave:** La simulación proyecta un aumento en la calidad académica, evidenciado por
la generación de proyectos de investigación y el apoyo entre compañeros a través de tutorías,
fortaleciendo el ambiente de aprendizaje colaborativo.
""")
