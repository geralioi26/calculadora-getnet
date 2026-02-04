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
    st.caption("Dirección: Crespo 4117, Rosario | Condición: IIBB EXENTO")

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

# 5. VISUALIZACIÓN EN PANTALLA (Con totales para el cliente)
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.info("💵 **EFECTIVO**")
    st.subheader(f"${precio_base:,.2f}")
    st.caption("Billete / Transf.")

with col_b:
    st.success("🏦 **BNA (3 y 6)**")
    st.write(f"3 x ${t3_bna/3:,.2f}")
    st.write(f"**Total: ${t3_bna:,.0f}**")
    st.divider()
    st.write(f"6 x ${t6_bna/6:,.2f}")
    st.write(f"**Total: ${t6_bna:,.0f}**")

with col_c:
    st.warning("📈 **LARGOS**")
    st.write(f"9 x ${t9_largo/9:,.2f}")
    st.write(f"**Total: ${t9_largo:,.0f}**")
    st.divider()
    st.write(f"12 x ${t12_largo/12:,.2f}")
    st.write(f"**Total: ${t12_largo:,.0f}**")

# 6. FUNCIÓN DE WHATSAPP (Mensaje amable y completo)
mensaje = (
    f"👋 *¡Hola! Muchas gracias por consultar en Embragues Rosario.*\n\n"
    f"Aquí tenés el presupuesto que solicitaste para tu comodidad:\n"
    f"------------------------------------\n"
    f"💵 *PRECIO EN EFECTIVO:* ${precio_base:,.2f}\n"
    f"*(Billete o Transferencia)*\n\n"
    f"💳 *CON TARJETA BANCARIA:*\n"
    f"- 3 cuotas de: ${t3_bna/3:,.2f} (Total: ${t3_bna:,.0f})\n"
    f"- 6 cuotas de: ${t6_bna/6:,.2f} (Total: ${t6_bna:,.0f})\n\n"
    f"📈 *PLANES LARGOS (9 y 12):*\n"
    f"- 9 cuotas de: ${t9_largo/9:,.2f} (Total: ${t9_largo:,.0f})\n"
    f"- 12 cuotas de: ${t12_largo/12:,.2f} (Total: ${t12_largo:,.0f})\n\n"
    f"⚡ *OTROS:* QR MODO: ${qr_modo:,.0f} | Débito: ${debito:,.0f}\n"
    f"------------------------------------\n"
    f"📍 *Dirección:* Crespo 4117, Rosario\n"
    f"⏰ *Horario:* 8:30 a 17:00 hs\n"
    f"📸 *Instagram:* @embraguesrosario\n\n"
    f"✨ *¡Muchas gracias por elegirnos y te esperamos pronto en el taller!*"
)

texto_url = urllib.parse.quote(mensaje)
link_whatsapp = f"https://wa.me/?text={texto_url}"

st.divider()
st.link_button("🟢 Enviar Presupuesto por WhatsApp", link_whatsapp)

# 7. NOTA INTERNA PARA GERARDO
with st.expander("📝 Nota para el mostrador (Uso interno)"):
    st.write("Para recibir el precio de efectivo limpio, cobrar en la Maquinola el **Total** que figura en pantalla y elegir **'Cuotas sin interés'**.")

st.caption("Fórmulas actualizadas Feb-2026. Los recargos cubren la comisión bancaria por ser IIBB Exento.")
