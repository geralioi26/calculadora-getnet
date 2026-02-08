import streamlit as st
import urllib.parse
from PIL import Image
import numpy as np

# 1. IDENTIDAD (Vuelve tu logo a la pestaña y arriba de todo)
st.set_page_config(page_title="Embragues Rosario", page_icon="logo.png")
st.image("logo.png", width=300) 
st.title("Embragues Rosario")
st.markdown("Crespo 4117, Rosario | **IIBB: EXENTO**")

# 2. CONFIGURACIÓN (Sidebar)
st.sidebar.header("⚙️ Configuración")
monto_limpio = st.sidebar.number_input("Monto LIMPIO ($):", min_value=0, value=210000, step=5000)
vehiculo = st.sidebar.text_input("Vehículo:", "Renault Sandero")

tipo_kit = st.sidebar.selectbox("Tipo de Kit:", ["Nuevo", "Reparado completo con crapodina"])

# Lógica de textos y marcas
if tipo_kit == "Nuevo":
    marca_kit = st.sidebar.text_input("Marca del Kit Nuevo:", "Sachs")
    label_item = "*Embrague:*"
    texto_detalle = f"KIT nuevo marca *{marca_kit}*"
    incluye_rectif = True 
    icono = "⚙️"
else:
    marcas_crap = st.sidebar.multiselect(
        "Marcas de Crapodina:", 
        ["Luk", "Skf", "Ina", "Dbh", "The"],
        default=["Luk", "Skf"]
    )
    m_negrita = [f"*{m}*" for m in marcas_crap]
    texto_marcas = ", ".join(m_negrita[:-1]) + " o " + m_negrita[-1] if len(m_negrita) > 1 else (m_negrita[0] if m_negrita else "*primera marca*")

    label_item = "*Trabajo:*"
    # Frase técnica exacta: balanceado y sin paréntesis
    texto_detalle = f"reparado completo placa disco con forros originales volante rectificado y balanceado con crapodina {texto_marcas}"
    incluye_rectif = False 
    icono = "🔧"

# --- 🔍 CONTROL INTERNO (Carga de Código y Foto) ---
st.sidebar.divider()
st.sidebar.write("📋 **Control de Stock (Uso Interno)**")

# ACÁ ESTÁ EL CAMPO MANUAL QUE FALTABA
codigo_manual = st.sidebar.text_input("Código de repuesto (Manual):", help="Este código NO se envía al cliente")

foto = st.sidebar.file_uploader("O cargar foto de la caja:", type=["jpg", "png", "jpeg"])
if foto is not None:
    try:
        img_pil = Image.open(foto)
        st.sidebar.image(img_pil, caption="Caja cargada", use_container_width=True)
    except Exception:
        st.sidebar.error("Error al procesar la imagen.")

# 3. SELECTORES DE PAGO
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

# 6. RESULTADOS APP
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

# 7. WHATSAPP (Limpio para el cliente y sin códigos)
# Link de búsqueda directa para evitar errores de ubicación
maps_link = "https://www.google.com/maps/search/Crespo+4117+Rosario"
ig_handle = "@embraguesrosario"
ig_link = "https://www.instagram.com/embraguesrosario/"
s = "‎" # Espacio invisible para evitar números azules

linea_extra = f"✅  *Incluye rectificación y balanceo de volante*\n" if incluye_rectif else ""

mensaje = (
    f"🚗  *EMBRAGUES ROSARIO*\n"
    f"¡Hola! Gracias por tu consulta. Te paso el presupuesto:\n\n"
    f"🚗  *Vehículo:* {vehiculo}\n"
    f"{icono}  {label_item} {texto_detalle}\n"
    f"{linea_extra}\n"
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
