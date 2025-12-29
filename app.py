import streamlit as st

# 1. Configuración de la pestaña (Usamos el link de la imagen directamente acá)
st.set_page_config(
    page_title="Embragues Rosario", 
    page_icon="https://cdn-icons-png.flaticon.com/512/3233/3233917.png", 
    layout="centered"
)

# 2. Refuerzo para el celular
st.markdown(
    """
    <head>
        <title>Embragues Rosario</title>
        <link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/3233/3233917.png">
        <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/3233/3233917.png">
    </head>
    """,
    unsafe_allow_html=True
)

st.title("⚙️ Embragues Rosario")
st.subheader("Calculadora de Cobros")
# ... (el resto del código igual)
