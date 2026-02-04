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

# 3. ENTRADA DE PRECIO (Base Efectivo)
st.markdown("---")
precio_base = st.number_input("Precio en EFECTIVO ($):", min_value=0.0, value=100000.0, step=1000.0)

# 4. CÁLCULOS
t3_bna = precio_base * 1.10
t6_bna = precio_base * 1.18
t9_largo = precio_base * 1.58
t12_largo = precio_base * 1.80
qr_modo = precio_base * 1.01
debito = precio_base * 1.025

# 5. VISUALIZACIÓN EN PANTALLA (3 Bloques Clave)
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.info("💵 **EFECTIVO**")
    st.subheader(f"${precio_base:,.2f}")
    st.caption("Billete / Transf.")

with col_b:
    st.success("🏦 **BNA (3 y 6)**")
    st.write(f"3 x ${t3_bna/3:,.2f}")
    st.write(f"6 x ${t6_bna/6:,.2f}")
    st.caption("Interés Bajo")

with col_c:
    st.warning("📈 **LARGOS**")
    st.write(f"9 x ${t9_largo/9:,.2f}")
    st.write(f"12 x ${t12_largo/12:,.2f}")
    st.caption("Tasa Estándar")

# 6. FUNCIÓN DE WHATSAPP (Mensaje para el cliente)
mensaje = (
    f"👋 *¡Hola! Muchas gracias por consultar en Embragues Rosario.*\n\n"
    f"Aquí tenés el presupuesto detallado:\n"
    f"------------------------------------\n"
    f"💵 *Precio Efectivo / Transferencia:* ${precio_base:,.2f}\n\n"
    f"💳 *Con Tarjeta de Crédito (Bancaria):*\n"
    f"- 3 pagos de: ${t3_bna/3:,.2f} (Total: ${t3_bna:,.0f})\n"
    f"- 6 pagos de: ${t6_bna/6:,.2f} (Total: ${t6_bna:,.0f})\n\n"
    f"📈 *Opciones en 9 y 12 cuotas:*\n"
    f"- 9 pagos de: ${t9_largo/9:,.2f} (Total: ${t9_largo:,.0f})\n"
    f"- 12 pagos de: ${t12_largo/12:,.2f} (Total: ${t12_largo:,.0f})\n\n"
    f"⚡ *Otros:* QR MODO: ${qr_modo:,.0f} | Débito: ${debito:,.0f}\n"
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

# 7. NOTA INTERNA PARA GERARDO
with st.expander("📝 Nota para el mostrador (Uso interno)"):
    st.write("Al usar la Maquinola, cobrar el **Total** que figura arriba y seleccionar **'Cuotas sin interés'**.")
    st.write("Como sos **IIBB EXENTO**, recibís el precio efectivo limpio.")

st.caption("Fórmulas actualizadas Feb-2026 - Rosario, Argentina.")
