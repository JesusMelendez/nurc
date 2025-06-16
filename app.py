# app_main.py (o Home.py)
import streamlit as st
import pandas as pd
import numpy as np 

# --- Configuración General de la Aplicación Streamlit ---
st.set_page_config(
    page_title="Simulación de Moneda Digital de Incentivos - NURC",
    page_icon="💰",
    layout="wide", # Usa el ancho completo de la página
    initial_sidebar_state="expanded" # Sidebar expandido por defecto
)

# --- Título Principal y Introducción ---
st.title("💰 Simulación de Moneda Digital de Incentivos - NURC")

st.markdown("""
Esta aplicación interactiva simula el funcionamiento de una nueva moneda digital diseñada
para incentivar comportamientos positivos en la comunidad de la Universidad Rosario Castellanos (URC).
Explora cómo los incentivos en las áreas Cultural, Medio Ambiente y Desempeño Escolar
pueden influir en la participación y el impacto social.

**Usa el menú de la izquierda para navegar por los diferentes segmentos de incentivos.**
""")

# --- Sidebar para Parámetros Globales (Accesibles a todas las páginas vía session_state) ---
# Los parámetros globales se definen aquí y se almacenan en st.session_state
# para que sean accesibles desde todas las páginas.
st.sidebar.header("Configuración de la Simulación Global")

st.session_state['tasa_base_adopcion'] = st.sidebar.slider(
    "Tasa base de adopción de la moneda", 0.01, 0.1, 0.05, 0.005,
    key="global_tasa_adopcion" # Clave única para el slider
)
st.session_state['duracion_simulacion'] = st.sidebar.slider(
    "Duración de la simulación (meses)", 12, 60, 24, 6,
    key="global_duracion_simulacion"
)
st.session_state['poblacion_total_urc'] = st.sidebar.number_input(
    "Población total de estudiantes URC", 1000, 50000, 25000, 1000,
    key="global_poblacion_urc"
)

st.sidebar.markdown("---")
st.sidebar.subheader("Navegación de la Aplicación")
# Streamlit crea automáticamente los enlaces a las páginas aquí basándose en la carpeta 'pages'

st.markdown("""

## El Rol Estratégico de los Incentivos

Los incentivos, desde una perspectiva económica, se definen como mecanismos de intervención que modifican los costos y beneficios materiales que los individuos enfrentan en sus alternativas de decisión para una situación económica dada. Su propósito fundamental es motivar o alentar un cambio de comportamiento de manera predecible hacia un determinado curso de acción. Estos pueden manifestarse como recompensas que fomentan una conducta o como penalizaciones que la desalientan. 
En el ámbito de las políticas públicas, la implementación de incentivos es una herramienta estratégica para corregir fallos de mercado y abordar externalidades negativas, promoviendo así comportamientos que benefician a la sociedad en su conjunto. Este enfoque busca equilibrar los costos y beneficios privados a corto plazo con los costos y beneficios sociales a mediano y largo plazo, especialmente en áreas críticas como la conservación ambiental.
- Punto 1
- Punto 2

**Texto en negrita**, *cursiva*, y más.

---
""")
# --- Notas al pie o información adicional ---
st.markdown("---")
st.markdown("""
<small>Desarrollado por el EQUIPO 3 para el Problema Prototípico del Semestre 2025-1, Licenciatura en Ciencias de Datos para Negocios, URC.</small>
""", unsafe_allow_html=True)
