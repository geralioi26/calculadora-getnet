import streamlit as st

# 1. Configuración básica
st.set_page_config(
    page_title="Embragues Rosario",
    page_icon="🚗", 
    layout="centered"
)

# 2. Encabezado con imagen local (la que vas a subir a GitHub)
col_logo, col_tit = st.columns([1, 4])
with col_logo:
    try:
        # Intenta cargar logo.png desde tu repositorio
        st.image("logo.png", width=80)
    except:
        # Si la imagen no está, muestra un emoji para que no de error
        st.write("⚙️")

with col_tit:
    st.title("Embragues Rosario")

st.write("### Calculadora de Cobros Getnet")

# Entrada de dinero
monto = st.number_input("Monto que querés recibir limpio:", min_value=0.0, value=100000.0, step=1000.0)

st.divider()

# --- SECCIÓN 3 Y 6 CUOTAS ---
st.markdown("### 📊 Planes de 3 y 6 Cuotas")
col1, col2 = st.columns(2)

with col1:
    st.info("🏦 **Plan MiPyME**\n\n*(Bancarias)*")
    t3m = monto * 1.14
    t6m = monto * 1.265
    st.write(f"**3 Cuotas de: ${t3m/3:,.2f}**")
    st.write(f"**6 Cuotas de: ${t6m/6:,.2f}**")

with col2:
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
st.markdown("### ⚡ Medios Rápidos")
c1, c2, c3 = st.columns(3)
c1.success(f"**QR**\n\n${monto * 1.01:,.2f}")
c2.success(f"**Débito**\n\n${monto * 1.012:,.2f}")
c3.success(f"**Crédito 1p**\n\n${monto * 1.025:,.2f}")

st.caption("Fórmulas actualizadas 2025 - Rosario, Argentina.")
