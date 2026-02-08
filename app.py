import streamlit as st
import urllib.parse

# 1. IDENTIDAD Y CONFIGURACIÓN (Tu logo en la pestaña y encabezado)
st.set_page_config(page_title="Embragues Rosario", page_icon="logo.png")
st.image("logo.png", width=300) 
st.title("Embragues Rosario")
st.markdown("Crespo 4117, Rosario | **IIBB: EXENTO**")

# 2. ENTRADA DE DATOS (Sidebar con las nuevas funciones)
st.sidebar.header("🔧 Configuración del Trabajo")
monto_limpio = st.sidebar.number_input("Monto LIMPIO para vos ($):", min_value=0, value=210000, step=5000)
vehiculo = st.sidebar.text_input("Vehículo (ej: Peugeot 206 1.6 16v):", "Renault Sandero")

tipo_kit = st.sidebar.selectbox("Tipo de Kit:", ["Nuevo", "Reparado completo con crapodina"])

# Lógica de marcas que pediste
if tipo_kit == "Nuevo":
    marca_kit = st.sidebar.text_input("Marca del Kit Nuevo:", "Sachs")
    detalle_kit = f"Kit NUEVO marca {marca_kit}"
else:
    marca_crap = st.sidebar.text_input("Marca de la Crapodina:", "Luk")
    detalle_kit = f"Kit REPARADO COMPLETO con crapodina {marca_crap}"

# 3. SELECTORES DE PAGO (Link o POS para el lunes)
st.markdown("### 💳 Configuración de Cobro")
col_b, col_m = st.columns(2)
with col_b:
    banco = st.radio("Sistema:", ["BNA (Más Pagos)", "Getnet (Santander)"], horizontal=True)
with col_m:
    metodo = st.radio("Medio de pago:", ["Link de Pago", "POS Físico / QR"], horizontal=True)

# 4. LÓGICA DE TASAS (BNA: 3.00%+IVA Link / 2.30%+IVA POS)
if banco == "BNA (Más Pagos)":
    # r1: un pago | r3: 3 cuotas | r6: 6 cuotas
    r1, r3, r6 = (1.042, 1.12, 1.20) if metodo == "Link de Pago" else (1.033, 1.10, 1.18)
else:
    r1, r3, r6 = (1.045, 1.16, 1.29) if metodo == "Link de Pago" else (1.038, 1.14, 1.25)

# 5. CÁLCULOS
t1 = monto_limpio * r1
t3 = monto_limpio * r3
t6 = monto_limpio * r6

# 6. PANTALLA DE RESULTADOS (Cuota GRANDE, Total chiquito)
st.divider()
st.success(f"### **💰 EFECTIVO / TRANSFERENCIA: ${monto_limpio:,.0f}**")

col1, col2, col3 = st.columns(3) # Definimos las 3 para evitar el error NameError
with col1:
    st.metric("1 PAGO", f"${t1:,.0f}")
with col2:
    st.metric("3 CUOTAS DE:", f"${t3/3:,.2f}")
    st.caption(f"Total: ${t3:,.0f}")
with col3:
    st.metric("6 CUOTAS DE:", f"${t6/6:,.2f}")
    st.caption(f"Total: ${t6:,.0f}")

# 7. GENERADOR DE WHATSAPP CON "ONDA" ✨
# Incluye link de Google Maps y Tips de cuidado que ideamos antes
maps_link = "https://maps.app.goo.gl/rS3f5t3U3y3qF7uY8" 

mensaje = (
    f"🚗 *EMBRAGUES ROSARIO*\n"
    f"━━━━━━━━━━━━━━━━━━━\n"
    f"📦 *Presupuesto para:* {vehiculo}\n"
    f"⚙️ *Detalle:* {detalle_kit}\n"
    f"✅ *Incluye rectificación y balanceo de volante*\n"
    f"━━━━━━━━━━━━━━━━━━━\n\n"
    f"💵 *PRECIO CONTADO / TRANSF:* \n"
    f"👉 **${monto_limpio:,.0f}**\n\n"
    f"💳 *TARJETA DE CRÉDITO ({metodo}):*\n"
    f"🔹 **1 pago:** ${t1:,.0f}\n"
    f"🔹 **3 cuotas de:** *${t3/3:,.2f}* (Total: ${t3:,.0f})\n"
    f"🔹 **6 cuotas de:** *${t6/6:,.2f}* (Total: ${t6:,.0f})\n\n"
    f"📍 *Dirección:* Crespo 4117, Rosario\n"
    f"🗺️ *Cómo llegar:* {maps_link}\n"
    f"📸 *Instagram:* @embraguesrosario\n\n"
    f"💡 *Tip de cuidado:* Evitá dejar el pie sobre el pedal para que tu nuevo embrague dure mucho más. 😉\n\n"
    f"¡Te esperamos pronto! ✨🚀"
)

mensaje_codificado = urllib.parse.quote(mensaje)
link_wa = f"https://wa.me/?text={mensaje_codificado}"

st.divider()
st.link_button("🟢 ENVIAR POR WHATSAPP (Con Onda ✨)", link_wa)
