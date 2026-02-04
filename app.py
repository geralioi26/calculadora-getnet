import streamlit as st
from PIL import Image

# 1. IDENTIDAD DEL TALLER
try:
    img_favicon = Image.open("logo.png")
except:
    img_favicon = "🚗"

st.set_page_config(
    page_title="Embragues Rosario",
    page_icon=img_favicon,
    layout="centered"
)

# 2. ENCABEZADO
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image("logo.png", width=80)
    except:
        st.write("⚙️")

with col2:
    st.title("Embragues Rosario")
    st.caption("Dirección: Crespo 4117, Rosario | Condición: IIBB EXENTO")

# 3. ENTRADA DE DINERO (Lo que vos querés que te quede en mano)
st.markdown("---")
monto = st.number_input("Monto limpio para el taller ($):", min_value=0.0, value=100000.0, step=1000.0)

# 4. SECCIÓN DE CUOTAS (Comparativa para el cliente)
st.markdown("### 💳 Pago en Cuotas (Tarjetas Bancarias)")
st.write("Aquí podés comparar cuánto paga el cliente por mes y el total final.")

col_bna, col_get = st.columns(2)

with col_bna:
    st.success("🏦 **OPCIÓN BANCO NACIÓN**")
    # Cálculos con Cuota Simple (Recargos: 10% en 3 y 18% en 6)
    t3_bna = monto * 1.10
    t6_bna = monto * 1.18
    
    st.write(f"**En 3 cuotas de: ${t3_bna/3:,.2f}**")
    st.write(f"👉 Total a cobrar: ${t3_bna:,.0f}")
    
    st.write(f"**En 6 cuotas de: ${t6_bna/6:,.2f}**")
    st.write(f"👉 Total a cobrar: ${t6_bna:,.0f}")

with col_get:
    st.warning("🟠 **OPCIÓN GETNET**")
    # Cálculos Getnet (Recargos: 14% en 3 y 26.5% en 6)
    t3_get = monto * 1.14
    t6_get = monto * 1.265
    
    st.write(f"**En 3 cuotas de: ${t3_get/3:,.2f}**")
    st.write(f"👉 Total a cobrar: ${t3_get:,.0f}")
    
    st.write(f"**En 6 cuotas de: ${t6_get/6:,.2f}**")
    st.write(f"👉 Total a cobrar: ${t6_get:,.0f}")

# 5. PLANES LARGOS (Solo tarjetas no bancarias)
st.markdown("---")
st.markdown("### 📈 Planes Largos (Tarjetas No Bancarias)")
col_9, col_12 = st.columns(2)

with col_9:
    total_9 = monto * 1.58
    st.write(f"**9 cuotas de: ${total_9 / 9:,.2f}**")
    st.caption(f"Total: ${total_9:,.0f}")

with col_12:
    total_12 = monto * 1.80
    st.write(f"**12 cuotas de: ${total_12 / 12:,.2f}**")
    st.caption(f"Total: ${total_12:,.0f}")

# 6. MEDIOS RÁPIDOS
st.markdown("---")
st.markdown("### ⚡ Otros Medios de Pago")
c1, c2, c3 = st.columns(3)

# Porcentajes ajustados para cubrir comisiones de la Maquinola y QR
c1.metric("QR MODO", f"${monto * 1.01:,.0f}", "Recargo 1%")
c2.metric("Débito POS", f"${monto * 1.025:,.0f}", "Recargo 2.5%")
c3.metric("Crédito 1p", f"${monto * 1.03:,.0f}", "Recargo 3%")

st.caption("Fórmulas actualizadas Feb-2026. Los montos finales ya incluyen el IVA de la comisión.")
