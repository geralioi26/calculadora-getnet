import streamlit as st
import urllib.parse
from PIL import Image
import numpy as np

# 1. IDENTIDAD Y CONFIGURACIÓN (Logo en pestaña y encabezado)
st.set_page_config(page_title="Embragues Rosario", page_icon="logo.png")
st.image("logo.png", width=300) 
st.title("Embragues Rosario")
st.markdown("Crespo 4117, Rosario | **IIBB: EXENTO**")

# 2. ENTRADA DE DATOS (Sidebar con Escáner Interno)
st.sidebar.header("⚙️ Configuración")
monto_limpio = st.sidebar.number_input("Monto LIMPIO para vos ($):", min_value=0, value=210000, step=5000)
vehiculo = st.sidebar.text_input("Vehículo:", "Renault Sandero")

# Selector de Kit
tipo_kit = st.sidebar.selectbox("Tipo de Kit:", ["Nuevo", "Reparado completo con crapodina"])

# Lógica dinámica para los textos y marcas
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
    
    marcas_negrita = [f"*{m}*" for m in marcas_elegidas]
    if len(marcas_negrita) > 1:
        texto_marcas = ", ".join(marcas_negrita[:-1]) + " o " + marcas_negrita[-1]
    elif marcas_negrita:
        texto_marcas = marcas_negrita[0]
    else:
        texto_marcas = "*primera marca*"

    label_item = "*Trabajo:*"
    texto_detalle = f"reparado completo placa disco con forros originales volante rectificado y balanceado con crapodina {texto_marcas}"
    incluye_linea_extra = False 
    icono = "🔧"

# --- 🔍 ESCÁNER INTERNO (Solo para vos) ---
st.sidebar.divider()
st.sidebar.write("📸 **Escaneo de Caja (Interno)**")
foto = st.sidebar.file_uploader("Subí foto de la caja:", type=["jpg", "png", "jpeg"])

if foto is not None:
    try:
        # Convertimos la foto para que la app no tire ValueError
        img_pil = Image.open(foto)
        img_array = np.array(img_pil)
        st.sidebar.image(img_pil, caption="Caja cargada", use_container_width=True)
        # Aquí podés ver el código en la pantalla, pero NO se va al WhatsApp
        st.sidebar.info("Código detectado: (Ejemplo 620 3041 00)") 
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

# 7. GENERADOR DE WHATSAPP (Limpio y sin códigos para el cliente)
maps_link = "http://googleusercontent.com/maps.google.com/search/Crespo+4117+Rosario"
ig_handle = "@embraguesrosario"
ig_link = "https://www.instagram.com/embraguesrosario/"
s = "‎" # Espacio invisible para evitar números azules

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
    f"📸  *Instagram:* *{ig_handle}*\n"
    f"     {ig_link}\n"
    f"⏰  *Horario:* 8:30 a 17:00 hs\n\n"
    f"¡Te esperamos pronto! 🙋🏻"
)

mensaje_codificado = urllib.parse.quote(mensaje)
link_wa = f"https://wa.me/?text={mensaje_codificado}"

st.divider()
st.link_button("🟢 ENVIAR POR WHATSAPP", link_wa)
