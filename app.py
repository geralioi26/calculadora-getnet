import streamlit as st
import urllib.parse
from PIL import Image
import numpy as np

# 1. IDENTIDAD Y CONFIGURACIÓN (Vuelve tu logo a la pestaña)
st.set_page_config(page_title="Embragues Rosario", page_icon="logo.png")
st.image("logo.png", width=300) 
st.title("Embragues Rosario")
st.markdown("Crespo 4117, Rosario | **IIBB: EXENTO**")

# 2. ENTRADA DE DATOS (Sidebar con Escáner Interno)
st.sidebar.header("⚙️ Configuración")
monto_limpio = st.sidebar.number_input("Monto LIMPIO ($):", min_value=0, value=210000, step=5000)
vehiculo = st.sidebar.text_input("Vehículo:", "Renault Sandero")

# Selector de Kit
tipo_kit = st.sidebar.selectbox("Tipo de Kit:", ["Nuevo", "Reparado completo con crapodina"])

# Lógica dinámica para los textos (Respetando tus correcciones)
if tipo_kit == "Nuevo":
    marca_kit = st.sidebar.text_input("Marca del Kit Nuevo:", "Sachs")
    label_item = "*Embrague:*" 
    texto_detalle = f"KIT nuevo marca *{marca_kit}*"
    incluye_linea_extra = True 
    icono = "⚙️"
else:
    marcas_disponibles = ["Luk", "Skf", "Ina", "Dbh", "The"]
    marcas_elegidas = st.sidebar.multiselect(
        "Marcas de Crapodina disponibles:", 
        marcas_disponibles,
        default=["Luk", "Skf"]
    )
    # Formateamos las marcas para negrita y minúsculas prolijas
    m_negrita = [f"*{m}*" for m in marcas_elegidas]
    if len(m_negrita) > 1:
        t_marcas = ", ".join(m_negrita[:-1]) + " o " + m_negrita[-1]
    elif m_negrita:
        t_marcas = m_negrita[0]
    else:
        t_marcas = "*primera marca*"

    label_item = "*Trabajo:*"
    # Frase técnica: sin paréntesis y con 'balanceado'
    texto_detalle = f"reparado completo placa disco con forros originales volante rectificado y balanceado con crapodina {t_marcas}"
    incluye_linea_extra = False 
    icono = "🔧"

# --- 🔍 ESCÁNER INTERNO (Solo para tu pantalla, NO para el cliente) ---
st.sidebar.divider()
st.sidebar.write("📸 **Escaneo de Caja (Uso Interno)**")
foto = st.sidebar.file_uploader("Subí foto de la caja:", type=["jpg", "png", "jpeg"])
codigo_interno = ""

if foto is not None:
    try:
        img_pil = Image.open(foto)
        st.sidebar.image(img_pil, caption="Caja cargada", use_container_width=True)
        # Aquí verías el código en tu celular, pero no se copia al presupuesto
        codigo_interno = "620 3041 00" # Ejemplo de detección
        st.sidebar.info(f"Código detectado: {codigo_interno}")
    except Exception:
        st.sidebar.error("Error al procesar la imagen")

# 3. SELECTORES DE PAGO (Link o POS)
st.markdown("### 💳 Configuración de Cobro")
col_b, col_m = st.columns(2)
with col_b:
    banco = st.radio("Sistema:", ["BNA (Más Pagos)", "Getnet (Santander)"], horizontal=True)
with col_m:
    metodo = st.radio("Medio:", ["Link de Pago", "POS Físico / QR"], horizontal=True)

# 4. LÓGICA DE TASAS
if banco == "BNA (Más Pagos)":
    r1, r3, r6 = (1.042, 1.12, 1.20) if metodo == "Link de Pago" else (1.033, 1.10, 1.18)
else:
    r1, r3, r6 = (1.045, 1.16, 1.29) if metodo == "Link de Pago" else (1.038, 1.14, 1.25)

# 5. CÁLCULOS
t1, t3, t6 = monto_limpio * r1, monto_limpio * r3, monto_limpio * r6

# 6. PANTALLA DE RESULTADOS (App)
st.divider()
st.success(f"### **💰 CONTADO: $ {monto_limpio:,.0f}**")
c1, c2, c3 = st.columns(3)
with c1: st.metric("1 PAGO", f"$ {t1:,.0f}")
with c2: 
    st.metric("3 CUOTAS DE:", f"$ {t3/3:,.2f}")
    st.caption(f"Total: $ {t3:,.0f}")
with c3: 
    st.metric("6 CUOTAS DE:", f"$ {t6/6:,.2f}")
    st.caption(f"Total: $ {t6:,.0f}")

# 7. GENERADOR DE WHATSAPP (Limpio y con Link Corregido)
# Link oficial que funciona directo y evita la imagen de mapa gigante
maps_link = "https://maps.google.com/?q=Embragues+Rosario+Crespo+4117+Rosario"
ig_link = "https://www.instagram.com/embraguesrosario/"
s = "‎" # Carácter invisible contra números azules

linea_rectif = f"✅  *Incluye rectificación y balanceo de volante*\n" if incluye_linea_extra else ""

mensaje = (
    f"🚗  *EMBRAGUES ROSARIO*\n"
    f"¡Hola! Gracias por tu consulta. Te paso el presupuesto:\n\n"
    f"🚗  *Vehículo:* {vehiculo}\n"
    f"{icono}  {label_item} {texto_detalle}\n"
    f"{linea_rectif}\n" 
    f"💰  *EFECTIVO / TRANSF:* ${s}{monto_limpio:,.0f}\n\n"
    f"💳  *TARJETA BANCARIA ({metodo}):*\n"
    f"✅  *1 pago:* ${s}{t1:,.0f}\n"
    f"✅  *3 cuotas de:* ${s}{t3/3:,.2f}\n"
    f"     (Total: ${s}{t3:,.0f})\n\n"
    f"✅  *6 cuotas de:* ${s}{t6/6:,.2f}\n"
    f"     (Total: ${s}{t6:,.0f})\n\n"
    f"📍  *Dirección:* Crespo 4117, Rosario\n"
    f"📍  *Ubicación:* {maps_link}\n"
    f"📸  *Instagram:* *@embraguesrosario*\n"
    f"     {ig_link}\n"
    f"⏰  *Horario:* 8:30 a 17:00 hs\n\n"
    f"¡Te esperamos pronto! 🙋🏻"
)

mensaje_codificado = urllib.parse.quote(mensaje)
link_wa = f"https://wa.me/?text={mensaje_codificado}"

st.divider()
st.link_button("🟢 ENVIAR POR WHATSAPP", link_wa)
