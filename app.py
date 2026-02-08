import streamlit as st
import urllib.parse

# 1. IDENTIDAD Y CONFIGURACIÓN
st.set_page_config(page_title="Embragues Rosario", page_icon="📍")
st.image("logo.png", width=300) 
st.title("Embragues Rosario")
st.markdown("Crespo 4117, Rosario | **IIBB: EXENTO**")

# 2. ENTRADA DE DATOS (Sidebar)
st.sidebar.header("⚙️ Configuración")
monto_limpio = st.sidebar.number_input("Monto LIMPIO para vos ($):", min_value=0, value=210000, step=5000)
vehiculo = st.sidebar.text_input("Vehículo:", "Renault Sandero")

# Opciones de Kit
tipo_kit = st.sidebar.selectbox("Tipo de Kit:", ["Nuevo", "Reparado completo con crapodina"])

# Lógica dinámica para los textos del presupuesto
if tipo_kit == "Nuevo":
    marca_kit = st.sidebar.text_input("Marca del Kit Nuevo:", "Sachs")
    label_dinamico = "Kit Embrague" # Agregamos 'Kit' como pediste
    texto_detalle = f"NUEVO marca {marca_kit}"
    icono = "⚙️"
else:
    marca_crap = st.sidebar.text_input("Marca de la Crapodina:", "Luk")
    label_dinamico = "Trabajo"
    texto_detalle = f"(reparado) completo con crapodina {marca_crap}"
    icono = "🔧"

# 3. SELECTORES DE PAGO (Link o POS)
st.markdown("### 💳 Configuración de Cobro")
col_b, col_m = st.columns(2)
with col_b:
    banco = st.radio("Sistema:", ["BNA (Más Pagos)", "Getnet (Santander)"], horizontal=True)
with col_m:
    metodo = st.radio("Medio:", ["Link de Pago", "POS Físico / QR"], horizontal=True)

# 4. LÓGICA DE TASAS (BNA vs Getnet)
if banco == "BNA (Más Pagos)":
    r1, r3, r6 = (1.042, 1.12, 1.20) if metodo == "Link de Pago" else (1.033, 1.10, 1.18)
else:
    r1, r3, r6 = (1.045, 1.16, 1.29) if metodo == "Link de Pago" else (1.038, 1.14, 1.25)

# 5. CÁLCULOS
t1, t3, t6 = monto_limpio * r1, monto_limpio * r3, monto_limpio * r6

# 6. PANTALLA DE RESULTADOS (Cuota GRANDE, Total chiquito)
st.divider()
st.success(f"### **💰 EFECTIVO / TRANSF: $ {monto_limpio:,.0f}**")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("1 PAGO", f"$ {t1:,.0f}")
with col2:
    st.metric("3 CUOTAS DE:", f"$ {t3/3:,.2f}")
    st.caption(f"Total: $ {t3:,.0f}")
with col3:
    st.metric("6 CUOTAS DE:", f"$ {t6/6:,.2f}")
    st.caption(f"Total: $ {t6:,.0f}")

# 7. GENERADOR DE WHATSAPP (Optimizado para Celular)
maps_link = "http://googleusercontent.com/maps.google.com/rs3f5t3U3y3qF7uy8"
ig_handle = "@embraguesrosario"
ig_link = "https://www.instagram.com/embraguesrosario/"

# Usamos espacios estratégicos para evitar los números azules y saltos de línea para los totales
mensaje = (
    f"🚗  *EMBRAGUES ROSARIO*\n"
    f"¡Hola! Gracias por tu consulta. Te paso el presupuesto:\n\n"
    f"🚗  *Vehículo:* {vehiculo}\n"
    f"{icono}  *{label_dinamico}:* {texto_detalle}\n"
    f"✅  *Incluye rectificación y balanceo de volante*\n\n"
    f"💰  *EFECTIVO / TRANSF:* $ {monto_limpio:,.0f}\n\n"
    f"💳  *TARJETA BANCARIA ({metodo}):*\n"
    f"✅  *1 pago:* $ {t1:,.0f}\n"
    f"✅  *3 cuotas de:* $ {t3/3:,.2f}\n"
    f"     (Total: $ {t3:,.0f})\n\n"
    f"✅  *6 cuotas de:* $ {t6/6:,.2f}\n"
    f"     (Total: $ {t6:,.0f})\n\n"
    f"📍  *Dirección:* Crespo 4117\n"
    f"📍  *Ubicación:* {maps_link}\n"
    f"📸  *Instagram:* *{ig_handle}*\n"
    f"     {ig_link}\n"
    f"⏰  *Horario:* 8:30 a 17:00 hs\n\n"
    f"¡Te esperamos pronto! ✨"
)

mensaje_codificado = urllib.parse.quote(mensaje)
link_wa = f"https://wa.me/?text={mensaje_codificado}"

st.divider()
st.link_button("🟢 ENVIAR POR WHATSAPP", link_wa)
