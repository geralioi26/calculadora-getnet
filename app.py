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

# 3. ENTRADA DE PRECIO
st.markdown("---")
precio_base = st.number_input("Precio en EFECTIVO ($):", min_value=0.0, value=100000.0, step=1000.0)

# 4. CÁLCULOS (Recargos para recibir precio base limpio)
credito_1p = precio_base * 1.03
t3_bna = precio_base * 1.10
t6_bna = precio_base * 1.18
t9_largo = precio_base * 1.58
t12_largo = precio_base * 1.80
qr_modo = precio_base * 1.01
debito = precio_base * 1.025

# 5. VISUALIZACIÓN EN PANTALLA
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.info("💵 **EFECTIVO**")
    st.subheader(f"${precio_base:,.2f}")
    st.caption("Billete / Transf.")

with col_b:
    st.success("🏦 **BANCO NACIÓN**")
    st.write(f"1 pago: **${credito_1p:,.0f}**")
    st.write(f"3 x **${t3_bna/3:,.2f}**")
    st.write(f"6 x **${t6_bna/6:,.2f}**")

with col_c:
    st.warning("📈 **LARGOS**")
    st.write(f"9 x **${t9_largo/9:,.2f}**")
    st.write(f"12 x **${t12_largo/12:,.2f}**")

# 6. FUNCIÓN DE WHATSAPP (Mensaje con más "onda" y negritas)
mensaje = (
    f"👋 *¡HOLA! MUCHAS GRACIAS POR CONSULTAR EN EMBRAGUES ROSARIO.*\n\n"
    f"Aquí tenés el presupuesto detallado para tu comodidad:\n"
    f"------------------------------------\n"
    f"💵 *PRECIO EN EFECTIVO:* **${precio_base:,.2f}**\n"
    f"*(Billete o Transferencia)*\n\n"
    f"💳 *CON TARJETA DE CRÉDITO (BANCARIA):*\n"
    f"▶ *1 PAGO:* **${credito_1p:,.0f}**\n"
    f"▶ *3 CUOTAS DE:* **${t3_bna/3:,.2f}** (Total: ${t3_bna:,.0f})\n"
    f"▶ *6 CUOTAS DE:* **${t6_bna/6:,.2f}** (Total: ${t6_bna:,.0f})\n\n"
    f"📈 *PLANES LARGOS (9 y 12):*\n"
    f"▶ *9 CUOTAS DE:* **${t9_largo/9:,.2f}** (Total: ${t9_largo:,.0f})\n"
    f"▶ *12 CUOTAS DE:* **${t12_largo/12:,.2f}** (Total: ${t12_largo:,.0f})\n\n"
    f"⚡ *OTROS:* QR MODO: **${qr_modo:,.0f}** | DÉBITO: **${debito:,.0f}**\n"
    f"------------------------------------\n"
    f"📍 *DIRECCIÓN:* **Crespo 4117, Rosario**\n"
    f"⏰ *HORARIO:* **8:30 a 17:00 hs**\n"
    f"📸 *INSTAGRAM:* **@embraguesrosario**\n\n"
    f"✨ *¡MUCHAS GRACIAS POR ELEGIRNOS Y TE ESPERAMOS PRONTO EN EL TALLER!*"
)

texto_url = urllib.parse.quote(mensaje)
link_whatsapp = f"https://wa.me/?text={texto_url}"

st.divider()
st.link_button("🟢 ENVIAR PRESUPUESTO POR WHATSAPP", link_whatsapp)

# 7. NOTA INTERNA
with st.expander("📝 Nota para el mostrador"):
    st.write("Recordá cobrar el **Total** en la Maquinola y elegir **'Sin Interés'**.")

st.caption("Fórmulas actualizadas Feb-2026. IIBB: EXENTO.")
