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
    st.divider()
    st.write(f"3 x **${t3_bna/3:,.2f}**")
    st.write(f"Total: **${t3_bna:,.0f}**")
    st.divider()
    st.write(f"6 x **${t6_bna/6:,.2f}**")
    st.write(f"Total: **${t6_bna:,.0f}**")

with col_c:
    st.warning("📈 **LARGOS**")
    st.write(f"9 x **${t9_largo/9:,.2f}**")
    st.write(f"Total: **${t9_largo:,.0f}**")
    st.divider()
    st.write(f"12 x **${t12_largo/12:,.2f}**")
    st.write(f"Total: **${t12_largo:,.0f}**")

# 6. FUNCIÓN DE WHATSAPP (Formato corregido para negritas en celular)
mensaje = (
    f"🚗 *EMBRAGUES ROSARIO*\n"
    f"¡Hola! Gracias por tu consulta. Te paso el presupuesto:\n\n"
    f"💰 *EFECTIVO / TRANSF:* *${precio_base:,.2f}*\n\n"
    f"💳 *TARJETA BANCARIA:*\n"
    f"✅ 1 pago: *${credito_1p:,.0f}*\n"
    f"✅ 3 cuotas: *${t3_bna/3:,.2f}* (Total: *${t3_bna:,.0f}*)\n"
    f"✅ 6 cuotas: *${t6_bna/6:,.2f}* (Total: *${t6_bna:,.0f}*)\n\n"
    f"📈 *PLANES LARGOS:*\n"
    f"👉 9 pagos de: *${t9_largo/9:,.2f}* (Total: *${t9_largo:,.0f}*)\n"
    f"👉 12 pagos de: *${t12_largo/12:,.2f}* (Total: *${t12_largo:,.0f}*)\n\n"
    f"📱 *QR:* *${qr_modo:,.0f}* | 💳 *DÉBITO:* *${debito:,.0f}*\n\n"
    f"📍 *Crespo 4117*\n"
    f"⏰ *8:30 a 17:00 hs*\n"
    f"📸 *@embraguesrosario*\n\n"
    f"¡Te esperamos pronto! ✨"
)

texto_url = urllib.parse.quote(mensaje)
link_whatsapp = f"https://wa.me/?text={texto_url}"

st.divider()
st.link_button("🟢 ENVIAR POR WHATSAPP", link_whatsapp)

# 7. NOTA INTERNA
with st.expander("📝 Nota para el mostrador"):
    st.write("Recordá cobrar el *Total* en la Maquinola y elegir *'Sin Interés'*.")

st.caption("Fórmulas actualizadas Feb-2026. IIBB: EXENTO.")
