import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import gspread
from google.oauth2 import service_account
from io import BytesIO
# Configuración para Google Sheets usando las credenciales almacenadas en secrets.toml
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Cargar las credenciales desde st.secrets
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

# Autenticar con gspread usando las credenciales cargadas
gc = gspread.authorize(credentials)

# CONFIGURAMOS LA PAGINA
layout = "centered"
page_title = "Satisfaccion | Cliente"
page_icon = ":star"

st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    layout=layout)

# CARGAMOS EL CSS
# AÑADIMOS EL ESTILO
css_file = "styles/main.css"

with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Función para obtener los datos de Serviplus
# Función para obtener los datos de Serviplus con filtro de región y mes
def get_serviplus_data(region=None, mes=None):
    grupo = gc.open('EVALUACIONES COLECTIVAS').worksheet('SATISFACCION CLIENTE')
    agencias = gc.open('EVALUACIONES COLECTIVAS').worksheet('AGENCIAS')
    AGE = pd.DataFrame(agencias.get_all_records())
    CLIE = pd.DataFrame(grupo.get_all_records())
    
    # Ajustamos los nombres de las columnas según los datos
    AGE = AGE[['REGIÓN', 'CAPITAL', 'CODIGO']].copy()
    CLIE['Mes'] = pd.to_datetime(CLIE['FECHA'],format="%d/%m/%Y").dt.month  # Asegúrate de tener una columna 'Fecha'
    
    # Unimos los datos de clientes con agencias
    merged_df = pd.merge(AGE, CLIE, left_on='CODIGO', right_on='OFICINA', how='inner')

    # Filtramos por región y mes si están definidos
    if region:
        merged_df = merged_df[merged_df['CAPITAL'] == region]
    if mes:
        merged_df = merged_df[merged_df['Mes'] == mes]

    # Verifica si hay datos después del filtrado
    if merged_df.empty:
        raise ValueError("No hay datos para este mes.")

    # Calculamos la media de las preguntas
    promedios = merged_df[['Pregunta 1', 'Pregunta 2', 'Pregunta 3 ', 'Pregunta 4', 'Pregunta 5', 'Pregunta 6']].mean()
    return promedios

# Función para obtener los datos de Transporte con filtro de mes
def get_transporte_data(mes=None):
    grupo = gc.open('BD TRANSPORTE').worksheet('SATISFACCION DEL CLIENTE')
    trans = pd.DataFrame(grupo.get_all_records())
    trans['Mes'] = pd.to_datetime(trans['FECHA'], format="%d/%m/%Y").dt.month  # Ajusta el formato de fecha si es necesario
    
    # Aplicamos el filtro de mes, si está definido
    if mes:
        filtered_df = trans[trans['Mes'] == mes]
    else:
        filtered_df = trans

    # Verifica si hay datos después del filtrado
    if filtered_df.empty:
        raise ValueError("No hay datos para este mes.")
    
    # Calculamos la media de las preguntas
    return filtered_df[['Pregunta 1', 'Pregunta 2', 'Pregunta 3', 'Pregunta 4', 'Pregunta 5', 'Pregunta 6', 'Pregunta 7']].mean()

# Función para crear el gráfico radar
def crear_grafico_radar_general(datos, etiquetas, titulo, colores_fondo):
    num_vars = len(etiquetas)
    angulos = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    datos = np.concatenate((datos, [datos[0]]))
    angulos += angulos[:1]
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.spines['polar'].set_visible(False)
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(etiquetas)

    for i in range(1, 5):
        ax.fill(angulos, [i] * len(angulos), color=colores_fondo[i-1], alpha=0.4)

    ax.plot(angulos, datos, color='darkred', linewidth=1.5)
    ax.scatter(angulos[:-1], datos[:-1], color='darkblue', s=20)

    for i in range(len(etiquetas)):
        porcentaje = f"{int(datos[i] / 4 * 100)}%"
        ax.text(angulos[i], datos[i] + 0.1, porcentaje, color='black', fontsize=10, ha='right', va='baseline', fontweight='bold')

    ax.set_yticks([1, 2, 3, 4])
    ax.set_yticklabels(['  Debe\nmejorar', 'Regular', 'Bueno', 'Excelente'], color='black', size=10)
    ax.yaxis.set_tick_params(labelrotation=0)
    ax.grid(True, alpha=0.8, color="white")
    plt.ylim(0.5, 4.5)
    plt.title(titulo, size=16, color='darkblue', y=1.1, weight='bold')
    st.pyplot(fig)
    
    # Retornar el objeto fig para guardarlo
    return fig

# Aplicación en Streamlit
st.markdown("## Evaluación de Satisfacción del Cliente")

# Select box para seleccionar la empresa
empresa = st.selectbox("Selecciona la empresa", ["Serviplus", "Transporte"])

# Filtros adicionales
if empresa == "Serviplus":
    # Obtener las regiones
    regiones = gc.open('EVALUACIONES COLECTIVAS').worksheet('AGENCIAS').col_values(3)[1:]  # Ajusta el índice si es necesario
    region_seleccionada = st.selectbox("Selecciona la región", ["Todas"] + sorted(set(regiones)))
    
    # Crear un selectbox para los meses del 1 al 12
    mes_seleccionado = st.selectbox("Selecciona el mes", list(range(1, 13)))

    # Manejo de excepción para datos no disponibles
    try:
        with st.spinner("Cargando gráfico..."):
            if region_seleccionada == "Todas":
                region_seleccionada = None
            promedios_generales = get_serviplus_data(region=region_seleccionada, mes=mes_seleccionado)
            etiquetas = ['Pregunta 1', 'Pregunta 2', 'Pregunta 3', 'Pregunta 4', 'Pregunta 5', 'Pregunta 6']
            colores_fondo = ['#E05666', '#E3787B', '#E09498', '#E0B2A3']  # Colores para Serviplus
            fig = crear_grafico_radar_general(promedios_generales.values, etiquetas, 'Satisfacción del Cliente Serviplus', colores_fondo)
            # Guardar el gráfico en un buffer de memoria y crear el botón de descarga
            buf = BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            st.download_button(
                label="Descargar gráfico como PNG",
                data=buf,
                file_name=f"satisfaccion_seviplus_{region_seleccionada}y_mes_{mes_seleccionado}.png",
                mime="image/png"
            )
    except ValueError as e:
        st.warning(e)

elif empresa == "Transporte":
    mes_seleccionado = st.selectbox("Selecciona el mes", list(range(1, 13)))
    
    try:
        with st.spinner("Cargando gráfico..."):
            promedios_generales = get_transporte_data(mes=mes_seleccionado)
            etiquetas = ['Pregunta 1', 'Pregunta 2', 'Pregunta 3', 'Pregunta 4', 'Pregunta 5', 'Pregunta 6', 'Pregunta 7']
            colores_fondo = ['#283593', '#303F9F', '#3949AB', '#3F51B5']
            fig = crear_grafico_radar_general(promedios_generales.values, etiquetas, 'Evaluación Satisfacción del Cliente Transporte', colores_fondo)
            # Guardar el gráfico en un buffer de memoria y crear el botón de descarga
            buf = BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            st.download_button(
                label="Descargar gráfico como PNG",
                data=buf,
                file_name=f"satisfaccion_transporte_mes_{mes_seleccionado}.png",
                mime="image/png"
            )
    except ValueError as e:
        st.warning(e)
