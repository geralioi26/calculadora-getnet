import streamlit as st
from PIL import Image

# 1. CONFIGURACIÓN DE IDENTIDAD
try:
    img_favicon = Image.open("logo.png")
except:
    img_favicon = "🚗"

st.set_page_config(
    page_title="Embragues Rosario",
    page_icon=img_favicon,
    layout="centered"
)

# 2. ENCABEZADO PROFESIONAL
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image("logo.png", width=80)
    except:
        st.write("⚙️") # Plan B si no carga la foto

with col2:
    st.title("Embragues Rosario")
    st.subheader("Calculadora de Cobros")
    st.caption("Crespo 4117, Rosario | IIBB: EXENTO")

# 3. ENTRADA DE DINERO
monto = st.number_input("Monto limpio que querés recibir:", min_value=0.0, value=100000.0, step=1000.0)

st.divider()

# 4. COMPARATIVA 3 Y 6 CUOTAS (BNA VS GETNET)
st.markdown("### 📊 Comparativa: Banco Nación vs. Getnet")
col_bna, col_get = st.columns(2)

with col_bna:
    st.success("🏦 **BANCO NACIÓN (Maquinola)**")
    # Recargos para recibir el monto limpio (incluye comisión e interés de Cuota Simple)
    t3_bna = monto * 1.10
    t6_bna = monto * 1.18
    st.write(f"**3 cuotas de: ${t3_bna/3:,.2f}**")
    st.write(f"**6 cuotas de: ${t6_bna/6:,.2f}**")
    st.caption(f"Total a cobrar: ${t3_bna:,.0f} / ${t6_bna:,.0f}")

with col_get:
    st.warning("🟠 **GETNET (Santander)**")
    # Recargos que usabas antes
    t3_get = monto * 1.14
    t6_get = monto * 1.265
    st.write(f"**3 cuotas de: ${t3_get/3:,.2f}**")
    st.write(f"**6 cuotas de: ${t6_get/6:,.2f}**")
    st.caption(f"Total a cobrar: ${t3_get:,.0f} / ${t6_get:,.0f}")

st.divider()

# 5. PLANES LARGOS (SOLO GETNET/EMISOR)
# Agregamos esto para que no sientas que falta info del código viejo
st.markdown("### 📈 Planes Largos (Getnet Emisor)")
col_9, col_12 = st.columns(2)
with col_9:
    total_9 = monto * 1.58
    st.write(f"**9 cuotas de: ${total_9 / 9:,.2f}**")
with col_12:
    total_12 = monto * 1.80
    st.write(f"**12 cuotas de: ${total_12 / 12:,.2f}**")

st.divider()

# 6. OTROS MEDIOS (MODO / POS BNA)
st.markdown("### ⚡ Otros Medios (Banco Nación)")
c1, c2, c3 = st.columns(3)
# Ya cubren la comisión de la Maquinola por ser IIBB Exento
c1.metric("QR MODO", f"${monto * 1.01:,.0f}")
c2.metric("Débito POS", f"${monto * 1.025:,.0f}")
c3.metric("Crédito 1p", f"${monto * 1.03:,.0f}")

st.caption("Actualizado Feb-2026 para Embragues Rosario.")
