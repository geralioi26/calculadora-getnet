
import streamlit as st

st.set_page_config(page_title="Embragues Rosario", page_icon="⚙️")

st.title("⚙️ Embragues Rosario")
st.subheader("Calculadora de Cobros")

monto = st.number_input("Monto que querés recibir limpio:", min_value=0.0, value=100000.0, step=1000.0)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏦 Plan MiPyME\n*(Bancarias)*")
    st.metric("3 Cuotas", f"${monto * 1.14:,.2f}")
    st.metric("6 Cuotas", f"${monto * 1.265:,.2f}")

with col2:
    st.markdown("### 💳 Plan Emisor\n*(Naranja / Otras)*")
    st.metric("3 Cuotas", f"${monto * 1.21:,.2f}")
    st.metric("6 Cuotas", f"${monto * 1.37:,.2f}")

st.divider()
st.markdown("### ⚡ Otros (Plata en el acto/breve)")
c1, c2, c3 = st.columns(3)
c1.info(f"**QR**\n\n${monto * 1.01:,.2f}")
c2.info(f"**Débito**\n\n${monto * 1.012:,.2f}")
c3.info(f"**1 Pago**\n\n${monto * 1.025:,.2f}")