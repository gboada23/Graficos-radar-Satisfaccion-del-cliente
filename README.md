# 📊 Gráficos Radar de Satisfacción del Cliente

Este proyecto utiliza **Streamlit** para generar gráficos radar que resumen la satisfacción del cliente para diferentes empresas, basado en datos almacenados en **Google Sheets**. Los datos se pueden filtrar por mes y región, y los gráficos resultantes están disponibles para descarga en formato PNG.

---

## 📝 Resumen

El proyecto permite visualizar gráficamente las respuestas de los clientes a una serie de preguntas. Estas respuestas, provenientes de la base de datos de satisfacción del cliente, se transforman en gráficos radar que muestran el porcentaje de satisfacción para cada pregunta. Los resultados ayudan a identificar áreas clave para la mejora y monitorear la satisfacción en diferentes regiones y meses.

## 🔍 Características Principales

- **Generación de gráficos radar** 📊: Visualiza los resultados de cada pregunta en un gráfico radar, con un rango de porcentaje de 1% a 100%.
- **Filtros dinámicos** 🎛️: Filtra los datos por **mes** y **región** para análisis específicos.
- **Descarga de gráficos** ⬇️: Guarda el gráfico radar como una imagen PNG directamente desde la aplicación.
- **Interfaz personalizable** 🎨: La aplicación carga un archivo CSS para un estilo visual mejorado.

## 🛠️ Tecnologías Utilizadas

- **Streamlit** 🌐: Framework para crear aplicaciones web interactivas en Python.
- **Google Sheets API** 📊: Almacena y recupera los datos de satisfacción del cliente.
- **Python** 🐍: Lenguaje de programación principal.
- **Pandas** 📋: Manipulación de datos.
- **Matplotlib** 📈: Generación de gráficos radar.
- **NumPy** 🔢: Operaciones numéricas.
- **gspread** 🔗: Integración con Google Sheets.
- **Google OAuth2** 🔒: Autenticación para Google Sheets.

## 📂 Estructura del Proyecto

- **app**: Contiene el archivo principal `app.py` para ejecutar la aplicación en Streamlit.
- **styles**: Archivos CSS para personalizar el aspecto de la aplicación.
- **images**: Carpeta para almacenar imágenes, incluidos ejemplos de gráficos generados.

Ejemplo Visual

![Grafico de radar](images/grafico.png)
