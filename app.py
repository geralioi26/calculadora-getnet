import streamlit as st
from PIL import Image
import urllib.parse

# 1. IDENTIDAD Y CONFIGURACIÓN
try:
    img_favicon = Image.open("logo.png")
except:
    img_favicon = "⚙️"

st.set_page_config(page_title="Embragues Rosario", page_icon=img_favicon, layout="centered")

# 2. ENCABEZADO
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image("logo.png", width=80)
    except:
        st.write("🚗")
with col2:
    st.title("Embragues Rosario")
    st.caption("Crespo 4117, Rosario | IIBB: EXENTO")

# 3. ENTRADA DE PRECIO
st.markdown("---")
precio_base = st.number_input("Precio en EFECTIVO ($):", min_value=0.0, value=100000.0, step=1000.0)

# 4. CÁLCULOS (Recargos para recibir el precio base limpio)
t3_bna = precio_base * 1.10
t6_bna = precio_base * 1.18
qr_modo = precio_base * 1.01
debito = precio_base * 1.025
credito_1p = precio_base * 1.03

# 5. TABLA EN PANTALLA
col_efec, col_tarj = st.columns(2)

with col_efec:
    st.info("💵 **EFECTIVO / TRANSF.**")
    st.subheader(f"${precio_base:,.2f}")

with col_tarj:
    st.success("🏦 **BANCO NACIÓN (Maquinola)**")
    st.write(f"**3 cuotas de: ${t3_bna/3:,.2f}**")
    st.caption(f"Total: ${t3_bna:,.0f}")
    st.write(f"**6 cuotas de: ${t6_bna/6:,.2f}**")
    st.caption(f"Total: ${t6_bna:,.0f}")

# 6. FUNCIÓN DE WHATSAPP
# Armamos el texto que se va a enviar
mensaje = (
    f"🚗 *Presupuesto - Embragues Rosario*\n\n"
    f"📍 Dirección: Crespo 4117, Rosario\n"
    f"------------------------------------\n"
    f"💵 *Efectivo/Transferencia:* ${precio_base:,.2f}\n\n"
    f"💳 *Banco Nación (Maquinola):*\n"
    f"- 3 cuotas de: ${t3_bna/3:,.2f} (Total: ${t3_bna:,.0f})\n"
    f"- 6 cuotas de: ${t6_bna/6:,.2f} (Total: ${t6_bna:,.0f})\n\n"
    f"⚡ *Otros Medios:*\n"
    f"- QR MODO: ${qr_modo:,.0f}\n"
    f"- Débito: ${debito:,.0f}\n"
    f"------------------------------------\n"
    f"💰 *Aprovechá las cuotas bancarias con interés bajo.*"
)

# Convertimos el texto a formato de URL
texto_url = urllib.parse.quote(mensaje)
link_whatsapp = f"https://wa.me/?text={texto_url}"

# Mostramos el botón
st.markdown("---")
st.link_button("🟢 Enviar Presupuesto por WhatsApp", link_whatsapp)

# 7. OTROS MEDIOS (Visual)
with st.expander("Ver recargos de otros medios"):
    c1, c2, c3 = st.columns(3)
    c1.metric("QR MODO", f"${qr_modo:,.0f}")
    c2.metric("Débito POS", f"${debito:,.0f}")
    c3.metric("Crédito 1p", f"${credito_1p:,.0f}")

st.caption("Actualizado Feb-2026. Los recargos cubren la comisión bancaria por ser IIBB Exento.")
