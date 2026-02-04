import streamlit as st
from PIL import Image
import urllib.parse

# 1. IDENTIDAD DEL TALLER
try:
    img_favicon = Image.open("logo.png")
except:
    img_favicon = "⚙️"

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
        st.write("🚗")

with col2:
    st.title("Embragues Rosario")
    st.caption("Crespo 4117, Rosario | Condición: IIBB EXENTO")

# 3. ENTRADA DE PRECIO
st.markdown("---")
precio_base = st.number_input("Precio en EFECTIVO ($):", min_value=0.0, value=100000.0, step=1000.0)

# 4. CÁLCULOS DE RECARGOS (Para recibir precio base limpio)
t3_bna = precio_base * 1.10
t6_bna = precio_base * 1.18
t9_largo = precio_base * 1.58
t12_largo = precio_base * 1.80
qr_modo = precio_base * 1.01
debito = precio_base * 1.025

# 5. SECCIÓN 3 Y 6 CUOTAS (BANCO NACIÓN)
st.markdown("### 🏦 Cuotas Banco Nación (Interés Bajo)")
col_3, col_6 = st.columns(2)

with col_3:
    st.success(f"**3 PAGOS DE: ${t3_bna/3:,.2f}**")
    st.write(f"👉 **TOTAL A COBRAR: ${t3_bna:,.0f}**")

with col_6:
    st.success(f"**6 PAGOS DE: ${t6_bna/6:,.2f}**")
    st.write(f"👉 **TOTAL A COBRAR: ${t6_bna:,.0f}**")

st.divider()

# 6. SECCIÓN PLANES LARGOS (9 Y 12 CUOTAS)
st.markdown("### 📈 Planes Largos (9 y 12 Cuotas)")
col_9, col_12 = st.columns(2)

with col_9:
    st.warning(f"**9 PAGOS DE: ${t9_largo/9:,.2f}**")
    st.write(f"👉 **TOTAL A COBRAR: ${t9_largo:,.0f}**")

with col_12:
    st.warning(f"**12 PAGOS DE: ${t12_largo/12:,.2f}**")
    st.write(f"👉 **TOTAL A COBRAR: ${t12_largo:,.0f}**")

# 7. FUNCIÓN DE WHATSAPP
mensaje = (
    f"👋 *¡Hola! Muchas gracias por consultar en Embragues Rosario.*\n\n"
    f"Aquí tenés el presupuesto detallado:\n"
    f"------------------------------------\n"
    f"💵 *Efectivo / Transferencia:* ${precio_base:,.2f}\n\n"
    f"💳 *Cuotas Banco Nación (Bancarias):*\n"
    f"- 3 pagos de: ${t3_bna/3:,.2f} (Total: ${t3_bna:,.0f})\n"
    f"- 6 pagos de: ${t6_bna/6:,.2f} (Total: ${t6_bna:,.0f})\n\n"
    f"📈 *Planes Largos:*\n"
    f"- 9 pagos de: ${t9_largo/9:,.2f} (Total: ${t9_largo:,.0f})\n"
    f"- 12 pagos de: ${t12_largo/12:,.2f} (Total: ${t12_largo:,.0f})\n\n"
    f"⚡ *Otros Medios:* QR MODO: ${qr_modo:,.0f} | Débito: ${debito:,.0f}\n"
    f"------------------------------------\n"
    f"📍 *Dirección:* Crespo 4117, Rosario\n"
    f"⏰ *Horario:* 8:30 a 17:00 hs\n"
    f"📸 *Instagram:* @embraguesrosario\n\n"
    f"✨ *¡Muchas gracias por elegirnos y te esperamos pronto!*"
)

texto_url = urllib.parse.quote(mensaje)
link_whatsapp = f"https://wa.me/?text={texto_url}"

st.divider()
st.link_button("🟢 Enviar Presupuesto por WhatsApp", link_whatsapp)

# 8. OTROS MEDIOS (DÉBITO / QR)
with st.expander("Ver otros medios (Débito y QR)"):
    st.write(f"QR MODO: ${qr_modo:,.0f}")
    st.write(f"Débito POS: ${debito:,.0f}")

st.caption("Fórmulas actualizadas Feb-2026. Los recargos cubren la comisión bancaria por ser IIBB Exento.")
