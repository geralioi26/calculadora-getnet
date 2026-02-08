import streamlit as st
import urllib.parse

# 1. IDENTIDAD (Logo en pestaña y encabezado)
st.set_page_config(page_title="Embragues Rosario", page_icon="logo.png")

st.image("logo.png", width=300) 
st.title("Embragues Rosario")
st.markdown("Crespo 4117, Rosario | **IIBB: EXENTO**")

# 2. CONFIGURACIÓN DEL TRABAJO
st.sidebar.header("⚙️ Configuración del Kit")
monto_limpio = st.sidebar.number_input("Monto LIMPIO para vos ($):", min_value=0, value=210000, step=5000)
vehiculo = st.sidebar.text_input("Vehículo (ej: Renault Sandero):", "Renault Sandero")

tipo_kit = st.sidebar.selectbox("Tipo de Kit:", ["Nuevo", "Reparado completo con crapodina"])

# Lógica de marcas separada como pediste
if tipo_kit == "Nuevo":
    marca_kit = st.sidebar.text_input("Marca del Kit Nuevo:", "Sachs")
    detalle_kit = f"Kit NUEVO marca {marca_kit}"
else:
    marca_crap = st.sidebar.text_input("Marca de la Crapodina:", "Luk")
    detalle_kit = f"Kit REPARADO COMPLETO con crapodina {marca_crap}"

# 3. SELECTORES DE PAGO (Link o POS)
st.markdown("### 💳 Configuración de Cobro")
col_b, col_m = st.columns(2)
with col_b:
    banco = st.radio("Sistema:", ["BNA (Más Pagos)", "Getnet (Santander)"], horizontal=True)
with col_m:
    metodo = st.radio("Medio de pago:", ["Link de Pago", "POS Físico / QR"], horizontal=True)

# 4. LÓGICA DE TASAS (BNA: 3.00%+IVA Link / 2.30%+IVA POS)
if banco == "BNA (Más Pagos)":
    r1, r3, r6 = (1.042, 1.12, 1.20) if metodo == "Link de Pago" else (1.033, 1.10, 1.18)
else:
    r1, r3, r6 = (1.045, 1.16, 1.29) if metodo == "Link de Pago" else (1.038, 1.14, 1.25)

# 5. CÁLCULOS
t1 = monto_limpio * r1
t3 = monto_limpio * r3
t6 = monto_limpio * r6

# 6. RESULTADOS EN APP (Cuota GRANDE, Total chiquito)
st.divider()
st.success(f"### **💰 CONTADO / TRANSF: ${monto_limpio:,.0f}**")

# Arreglado el NameError de la línea 53 definiendo las 3 juntas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("1 PAGO", f"${t1:,.0f}")
with col2:
    st.metric("3 CUOTAS DE:", f"${t3/3:,.2f}")
    st.caption(f"Total: ${t3:,.0f}")
with col3:
    st.metric("6 CUOTAS DE:", f"${t6/6:,.2f}")
    st.caption(f"Total: ${t6:,.0f}")

# 7. GENERADOR DE WHATSAPP (Con la "onda" de antes)
maps_link = "https://maps.app.goo.gl/rs3f5t3U3y3qF7uy8" # Tu link de Maps corregido

mensaje = (
    f"🚗 *EMBRAGUES ROSARIO*\n"
    f"¡Hola! Gracias por tu consulta. Te paso el presupuesto:\n\n"
    f"📦 *Vehículo:* {vehiculo}\n"
    f"⚙️ *Detalle:* {detalle_kit}\n"
    f"✅ *Incluye rectificación y balanceo de volante*\n\n"
    f"💰 *CONTADO / TRANSF:* **${monto_limpio:,.0f}**\n\n"
    f"💳 *TARJETA BANCARIA ({metodo}):*\n"
    f"✅ **1 pago:** ${t1:,.0f}\n"
    f"✅ **3 cuotas de:** *${t3/3:,.2f}* (Total: ${t3:,.0f})\n"
    f"✅ **6 cuotas de:** *${t6/6:,.2f}* (Total: ${t6:,.0f})\n\n"
    f"📍 *Crespo 4117, Rosario*\n"
    f"🗺️ *Cómo llegar:* {maps_link}\n"
    f"📸 *Instagram:* @embraguesrosario\n\n"
    f"¡Te esperamos pronto! ✨🚀"
)

mensaje_codificado = urllib.parse.quote(mensaje)
link_wa = f"https://wa.me/?text={mensaje_codificado}"

st.divider()
st.link_button("🟢 ENVIAR POR WHATSAPP (Con Onda ✨)", link_wa)
