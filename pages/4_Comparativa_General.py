# pages/4_Comparativa_General.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.decomposition import PCA # Para demostrar un PCA simplificado
from sklearn.linear_model import LinearRegression # Para una regresión simple
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

# --- Contenido de la Página Comparativa General ---
st.header("📊 Comparativa General de los Segmentos")
st.markdown("""
Esta sección permite comparar la adopción y el impacto social proyectado en los diferentes segmentos
(Cultural, Medio Ambiente, Desempeño Escolar) bajo las configuraciones actuales de la simulación.
Aquí también se exploran análisis de factores y consideraciones generales de la moneda digital.
""")

# Obtener parámetros globales de st.session_state
tasa_base_adopcion = st.session_state.get('tasa_base_adopcion', 0.05)
duracion_simulacion = st.session_state.get('duracion_simulacion', 24)
poblacion_total_urc = st.session_state.get('poblacion_total_urc', 25000)

st.subheader("Adopción de Incentivos por Segmento")
st.write("Visualiza cómo la participación en cada área se proyecta a crecer a lo largo del tiempo.")

# Para la comparativa, usamos valores por defecto para los factores específicos de cada segmento
# si el usuario no ha ajustado los sliders en las páginas individuales.
# Esto es una simplificación; en una app más robusta, se podrían guardar los últimos valores en session_state
# para que la comparativa refleje los ajustes hechos en cada página.
factor_interes_cultural_comp = st.session_state.get('cultural_factor_interes', 1.0)
capacidad_carga_cultural_comp = st.session_state.get('cultural_capacidad_carga', 0.2) * poblacion_total_urc

factor_conciencia_ambiental_comp = st.session_state.get('ambiental_factor_conciencia', 1.0)
capacidad_carga_ambiental_comp = st.session_state.get('ambiental_capacidad_carga', 0.15) * poblacion_total_urc

factor_motivacion_academica_comp = st.session_state.get('academico_factor_motivacion', 1.0)
capacidad_carga_academica_comp = st.session_state.get('academico_capacidad_carga', 0.3) * poblacion_total_urc


t = np.linspace(0, duracion_simulacion, 100)
N0 = 10 # Población inicial para todos los segmentos

# Simulación para Cultural
r_cultural_comp = tasa_base_adopcion * factor_interes_cultural_comp
sol_cultural_comp = odeint(modelo_logistico, N0, t, args=(r_cultural_comp, capacidad_carga_cultural_comp))
participantes_culturales_comp = sol_cultural_comp[:, 0]

# Simulación para Medio Ambiente
r_ambiental_comp = tasa_base_adopcion * factor_conciencia_ambiental_comp
sol_ambiental_comp = odeint(modelo_logistico, N0, t, args=(r_ambiental_comp, capacidad_carga_ambiental_comp))
participantes_ambientales_comp = sol_ambiental_comp[:, 0]

# Simulación para Desempeño Escolar
r_academica_comp = tasa_base_adopcion * factor_motivacion_academica_comp
sol_academica_comp = odeint(modelo_logistico, N0, t, args=(r_academica_comp, capacidad_carga_academica_comp))
participantes_academicos_comp = sol_academica_comp[:, 0]

df_comparativa_adopcion = pd.DataFrame({
    "Mes": t,
    "Cultural": participantes_culturales_comp,
    "Medio Ambiente": participantes_ambientales_comp,
    "Desempeño Escolar": participantes_academicos_comp
})

fig_comparativa_adopcion = px.line(df_comparativa_adopcion, x="Mes", y=["Cultural", "Medio Ambiente", "Desempeño Escolar"],
                                   labels={'value':'Número de Participantes', 'variable':'Segmento'},
                                   title='Crecimiento de Participantes por Segmento',
                                   line_shape="spline")
fig_comparativa_adopcion.update_traces(mode='lines')
st.plotly_chart(fig_comparativa_adopcion)

# --- Scorecard General de Incentivos ---
st.subheader("🏆 Scorecard General de Incentivos URC")
st.markdown("""
Este scorecard consolida el impacto proyectado de la moneda digital a través de los diferentes segmentos de incentivos,
ofreciendo una vista unificada del desempeño y la adopción. Los puntajes son proporcionales al número final de participantes proyectados.
""")

col1, col2, col3, col4 = st.columns(4)

# Calcular puntajes simplificados (se podrían usar métricas más complejas)
# El puntaje se basa en el porcentaje de la población total de URC que participa en cada segmento.
# Un factor de 1000 se usa para escalar a un número más legible para el scorecard.
score_cultural = int((participantes_culturales_comp[-1] / poblacion_total_urc) * 1000)
score_ambiental = int((participantes_ambientales_comp[-1] / poblacion_total_urc) * 1000)
score_academico = int((participantes_academicos_comp[-1] / poblacion_total_urc) * 1000)

# El puntaje total es la suma de los puntajes individuales
score_total = score_cultural + score_ambiental + score_academico

with col1:
    st.metric(label="Cultural", value=f"{score_cultural} Pts")
with col2:
    st.metric(label="Medio Ambiente", value=f"{score_ambiental} Pts")
with col3:
    st.metric(label="Desempeño Escolar", value=f"{score_academico} Pts")
with col4:
    st.metric(label="Total Score", value=f"{score_total} Pts", delta="Sumatoria de categorías")

st.markdown("""
<small>Nota: Los puntajes son una representación simplificada y podrían ajustarse con métricas de impacto más detalladas en un sistema real.</small>
""", unsafe_allow_html=True)

# Gráfico de la evolución del Scorecard Total (ejemplo)
st.subheader("Evolución Proyectada del Scorecard Total")
# Calcula un score total por cada punto en el tiempo 't'
scores_cultural_t = (participantes_culturales_comp / poblacion_total_urc) * 1000
scores_ambiental_t = (participantes_ambientales_comp / poblacion_total_urc) * 1000
scores_academico_t = (participantes_academicos_comp / poblacion_total_urc) * 1000
score_total_evol = scores_cultural_t + scores_ambiental_t + scores_academico_t

df_scorecard_evol = pd.DataFrame({
    "Mes": t,
    "Score Total": score_total_evol
})
fig_scorecard_evol = px.line(df_scorecard_evol, x="Mes", y="Score Total",
                             title='Evolución del Scorecard Total de Incentivos',
                             labels={'Score Total':'Puntaje Acumulado'},
                             line_shape="spline")
st.plotly_chart(fig_scorecard_evol)


# --- Análisis de Factores (PCA o Regresión Simple como ejemplo) ---
st.subheader("Análisis de Factores de Aceptación (Ejemplo con datos simulados)")
st.write("Este es un ejemplo simplificado de cómo se podría usar Estadística Multivariada (PCA) e IA (Regresión) para entender los factores que influyen en la aceptación general de la moneda o en la participación en los segmentos.")

# Generar datos simulados para un análisis de factores
np.random.seed(42) # Para reproducibilidad
num_observaciones = 100
confianza_usuario = np.random.rand(num_observaciones) * 100 # 0-100%
digitalizacion = np.random.rand(num_observaciones) * 100 # 0-100%
regulaciones = np.random.rand(num_observaciones) * 10 # 1-10 (escala arbitraria)
marketing = np.random.rand(num_observaciones) * 50 # 0-50 (impacto de campañas)
aceptacion_moneda = (0.5 * confianza_usuario + 0.3 * digitalizacion - 2 * regulaciones +
                     0.8 * marketing + np.random.randn(num_observaciones) * 10)
aceptacion_moneda = np.clip(aceptacion_moneda, 0, 100) # Limitar a 0-100%

df_factores = pd.DataFrame({
    'Confianza Usuario': confianza_usuario,
    'Digitalización': digitalizacion,
    'Regulaciones (escala 1-10)': regulaciones,
    'Marketing/Promoción': marketing,
    'Aceptación Moneda (%)': aceptacion_moneda
})

# Mostrar tabla de datos simulados
if st.checkbox("Mostrar datos simulados para análisis de factores"):
    st.dataframe(df_factores.head())

# PCA (Análisis de Componentes Principales)
st.markdown("##### Análisis de Componentes Principales (PCA)")
st.write("Identifica las variables más relevantes o las combinaciones de factores que explican la mayor varianza en la aceptación de la moneda.")
features = ['Confianza Usuario', 'Digitalización', 'Regulaciones (escala 1-10)', 'Marketing/Promoción']
X = df_factores[features]

pca = PCA(n_components=2) # Reducir a 2 componentes para visualización 2D
principal_components = pca.fit_transform(X)
df_pca = pd.DataFrame(data=principal_components, columns=['Componente Principal 1', 'Componente Principal 2'])
df_pca['Aceptación Moneda (%)'] = df_factores['Aceptación Moneda (%)'] # Añadir la variable de color

fig_pca = px.scatter(df_pca, x='Componente Principal 1', y='Componente Principal 2',
                     title='PCA de Factores de Aceptación',
                     color='Aceptación Moneda (%)', # Colorear por el nivel de aceptación
                     color_continuous_scale=px.colors.sequential.Viridis,
                     hover_data=df_pca.columns # Mostrar detalles al pasar el ratón
                     )
st.plotly_chart(fig_pca)
st.write(f"Varianza explicada por las 2 componentes principales: {pca.explained_variance_ratio_.sum():.2f}")
st.write("La PCA ayuda a entender qué combinaciones de factores influyen más en la aceptación general de la moneda.")

# Regresión Múltiple (Ejemplo de IA para predicción)
st.markdown("##### Predicción de Aceptación (Regresión Lineal Simple)")
st.write("Demuestra cómo se podría predecir la aceptación de la moneda basada en uno de los factores clave, como la confianza del usuario.")
# Seleccionamos una variable predictora para un ejemplo simple de regresión
x_reg = df_factores[['Confianza Usuario']]
y_reg = df_factores['Aceptación Moneda (%)']
model = LinearRegression()
model.fit(x_reg, y_reg)
y_pred = model.predict(x_reg)

fig_reg = px.scatter(df_factores, x='Confianza Usuario', y='Aceptación Moneda (%)',
                     title='Aceptación de la Moneda vs. Confianza del Usuario (Ejemplo Predictivo)',
                     labels={'Confianza Usuario': 'Confianza del Usuario (%)', 'Aceptación Moneda (%)': 'Aceptación de la Moneda (%)'})
# Añadir la línea de regresión
fig_reg.add_trace(px.line(x=x_reg['Confianza Usuario'], y=y_pred, color_discrete_sequence=['red'],
                          labels={'x':'Confianza Usuario', 'y':'Aceptacion Predicha'}).data[0])
st.plotly_chart(fig_reg)
st.write(f"Ecuación de regresión simplificada: Aceptación = {model.coef_[0]:.2f} * Confianza + {model.intercept_:.2f}")
st.markdown("""
Este modelo simple ilustra cómo la inteligencia artificial (en este caso, una regresión lineal)
podría ser utilizada para predecir la aceptación o el comportamiento de la moneda basándose en factores clave,
ayudando a tomar decisiones informadas.
""")

# --- Consideraciones de Base de Datos y Seguridad (Texto Descriptivo) ---
st.subheader("Consideraciones de Base de Datos y Seguridad")
st.markdown("""
Para el manejo de los datos de la moneda digital de incentivos en un entorno real, se consideraría una **arquitectura híbrida**:
* **Blockchain (concepto):** Sería la capa fundamental para registrar las transacciones de la moneda de forma inmutable, transparente y segura. Aunque no se implementa en esta simulación, es el pilar de una moneda digital descentralizada o semidescentralizada.
* **Base de Datos NoSQL (ej. Firestore/MongoDB/Cassandra):** Complementaría la blockchain para gestionar volúmenes masivos de datos de usuarios (perfiles, historial detallado de participación en actividades, saldo de la moneda, preferencias, etc.) y transacciones que no necesitan estar en la cadena de bloques principal. Esto permitiría una **escalabilidad** alta, **flexibilidad** en el esquema de datos y **agilidad** para consultas en tiempo real.
* **Seguridad:** Se implementarían algoritmos criptográficos robustos (como hashing SHA-256 para la integridad de datos, y firmas digitales para autenticación de transacciones) para proteger la integridad de las transacciones y la privacidad de los datos de los estudiantes. El uso de autenticación multifactor (MFA) para el acceso a las billeteras y auditorías regulares de seguridad serían esenciales.
""")

st.subheader("Dilemas Clave a Considerar")
st.markdown("""
La implementación de una moneda de incentivos en un entorno universitario plantea varios desafíos importantes:
* **Verificación de Acciones:** ¿Cómo se verifica de forma confiable la participación de los estudiantes en las actividades (culturales, ambientales, académicas) para otorgar las recompensas?
    * **Soluciones potenciales:** Uso de códigos QR o NFC en eventos, geolocalización, integración con sistemas académicos existentes (e.g., historial de calificaciones, asistencia), uso de formularios de reporte con evidencia fotográfica o validación por parte de personal.
* **Sostenibilidad del Valor:** ¿Qué mecanismo asegura que la moneda mantenga un valor percibido y utilidad a largo plazo dentro de la URC, más allá de la novedad inicial?
    * **Soluciones potenciales:** Convenios con comercios internos (cafeterías, librerías universitarias), acceso a servicios exclusivos (uso de laboratorios, biblioteca extendida), descuentos en cursos, talleres o actividades extra-curriculares, posibilidad de canjearla por material educativo.
* **Equidad y Acceso:** ¿Cómo se garantiza que todos los estudiantes, independientemente de su acceso a tecnología (smartphones, internet) o su familiaridad con monedas digitales, puedan participar y beneficiarse de los incentivos?
    * **Soluciones potenciales:** Provisión de puntos de acceso físico, interfaces de usuario simplificadas, programas de educación digital, soporte técnico accesible, opciones para canje de moneda sin necesidad de app.
* **Privacidad de Datos:** ¿Cómo se protegen los datos de participación y desempeño de los estudiantes que se recogen para otorgar incentivos, garantizando su privacidad frente a terceros y a la propia universidad?
    * **Soluciones potenciales:** Anonimización de datos siempre que sea posible, almacenamiento seguro con cifrado, políticas de privacidad claras y transparentes, cumplimiento de regulaciones de protección de datos (ej. LFPDPPP en México), control del usuario sobre sus datos.
""")
