import streamlit as st
from PIL import Image

# 1. CARGA DE IMAGEN PARA EL ÍCONO
# Intentamos cargar tu foto para que sea el ícono de la pestaña
try:
    img_favicon = Image.open("logo.png")
except:
    img_favicon = "🚗" # Si falla, pone un auto, nunca más un CD o engranaje

# 2. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Embragues Rosario",
    page_icon=img_favicon,
    layout="centered"
)

# 3. ENCABEZADO: LOGO Y TÍTULO
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image("logo.png", width=80)
    except:
        st.write("🚗")

with col2:
    st.title("Embragues Rosario")
    st.subheader("Calculadora de Cobros")

# 4. ENTRADA DE DINERO
monto = st.number_input("Monto que querés recibir limpio:", min_value=0.0, value=100000.0, step=1000.0)

st.divider()

# --- SECCIÓN 3 Y 6 CUOTAS ---
st.markdown("### 📊 Planes de 3 y 6 Cuotas")
c_mipyme, c_emisor = st.columns(2)

with c_mipyme:
    st.info("🏦 **Plan MiPyME**\n\n*(Bancarias)*")
    t3m = monto * 1.14
    t6m = monto * 1.265
    st.write(f"**3 Cuotas de: ${t3m/3:,.2f}**")
    st.write(f"**6 Cuotas de: ${t6m/6:,.2f}**")

with c_emisor:
    st.warning("💳 **Plan Emisor**\n\n*(Naranja / Otras)*")
    t3e = monto * 1.21
    t6e = monto * 1.37
    st.write(f"**3 Cuotas de: ${t3e/3:,.2f}**")
    st.write(f"**6 Cuotas de: ${t6e/6:,.2f}**")

st.divider()

# --- SECCIÓN PLANES LARGOS ---
st.markdown("### 📈 Planes Largos (Solo Plan Emisor)")
col_9, col_12 = st.columns(2)

with col_9:
    total_9 = monto * 1.58
    st.metric("Total 9 Cuotas", f"${total_9:,.2f}")
    st.write(f"👉 **9 cuotas de: ${total_9 / 9:,.2f}**")

with col_12:
    total_12 = monto * 1.80
    st.metric("Total 12 Cuotas", f"${total_12:,.2f}")
    st.write(f"👉 **12 cuotas de: ${total_12 / 12:,.2f}**")

st.divider()

# --- SECCIÓN OTROS MEDIOS ---
st.markdown("### ⚡ Medios Rápidos (8 días / Acto)")
c1, c2, c3 = st.columns(3)
c1.success(f"**QR**\n\n${monto * 1.01:,.2f}")
c2.success(f"**Débito**\n\n${monto * 1.012:,.2f}")
c3.success(f"**Crédito 1p**\n\n${monto * 1.025:,.2f}")

st.caption("Fórmulas actualizadas Getnet Dic-2025 - Rosario, Argentina.")
