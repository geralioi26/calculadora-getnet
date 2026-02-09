import streamlit as st
import urllib.parse
from PIL import Image
import numpy as np
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. IDENTIDAD Y CONFIGURACIÓN
st.set_page_config(page_title="Embragues Rosario", page_icon="logo.png")
st.image("logo.png", width=300) 
st.title("Embragues Rosario")
st.markdown("Crespo 4117, Rosario | **IIBB: EXENTO**")

# --- 💾 CONEXIÓN PERMANENTE (Google Sheets) ---
conn = st.connection("gsheets", type=GSheetsConnection)

def guardar_en_google(cliente, vehiculo, detalle, p_venta, p_compra, proveedor, codigo):
    fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
    # Leemos lo que ya hay
    try:
        existente = conn.read(worksheet="Ventas")
    except:
        existente = pd.DataFrame(columns=["Fecha", "Cliente", "Vehículo", "Detalle", "Venta $", "Compra $", "Proveedor", "Código"])
    
    # Sumamos el nuevo renglón
    nuevo = pd.DataFrame([[fecha_hoy, cliente, vehiculo, detalle, p_venta, p_compra, proveedor, codigo]], 
                         columns=existente.columns)
    actualizado = pd.concat([existente, nuevo], ignore_index=True)
    
    # Guardamos en la nube
    conn.update(worksheet="Ventas", data=actualizado)

# 2. CONFIGURACIÓN DEL TRABAJO (Sidebar)
st.sidebar.header("⚙️ Configuración")
monto_limpio = st.sidebar.number_input("Precio de VENTA ($):", min_value=0, value=210000, step=5000)
vehiculo = st.sidebar.text_input("Vehículo:", "Renault Sandero")
cliente_nombre = st.sidebar.text_input("Nombre del Cliente:", "Consumidor Final")

tipo_kit = st.sidebar.selectbox("Tipo de Kit:", ["Nuevo", "Reparado completo con crapodina"])

if tipo_kit == "Nuevo":
    marca_kit = st.sidebar.text_input("Marca del Kit Nuevo:", "Sachs")
    label_item, texto_detalle, icono, incluye_rectif = "*Embrague:*", f"KIT nuevo marca *{marca_kit}*", "⚙️", True
else:
    marcas_disponibles = ["Luk", "Skf", "Ina", "Dbh", "The"]
    marcas_elegidas = st.sidebar.multiselect("Marcas de Crapodina:", marcas_disponibles, default=["Luk", "Skf"])
    m_negrita = [f"*{m}*" for m in marcas_elegidas]
    texto_marcas = ", ".join(m_negrita[:-1]) + " o " + m_negrita[-1] if len(m_negrita) > 1 else (m_negrita[0] if m_negrita else "*primera marca*")
    label_item, texto_detalle, icono, incluye_rectif = "*Trabajo:*", f"reparado completo placa disco con forros originales volante rectificado y balanceado con crapodina {texto_marcas}", "🔧", False

# --- 🔍 CONTROL DE STOCK (Uso Interno) ---
st.sidebar.divider()
st.sidebar.write("📸 **Control de Stock**")
codigo_manual = st.sidebar.text_input("Código de repuesto (Manual):")
foto = st.sidebar.file_uploader("Subir foto de caja:", type=["jpg", "png", "jpeg"])

if foto is not None:
    try:
        img_pil = Image.open(foto)
        st.sidebar.image(img_pil, caption="Foto cargada", use_container_width=True)
    except Exception:
        st.sidebar.error("Error al procesar la imagen.")

st.sidebar.divider()
st.sidebar.write("📥 **Datos de Compra**")
precio_compra = st.sidebar.number_input("Precio de COMPRA ($):", min_value=0, value=0)
proveedor = st.sidebar.text_input("Proveedor:", "Repuestos Rosario")

if st.sidebar.button("💾 GUARDAR EN GOOGLE SHEETS"):
    guardar_en_google(cliente_nombre, vehiculo, texto_detalle, monto_limpio, precio_compra, proveedor, codigo_manual)
    st.sidebar.success(f"¡Venta de {vehiculo} guardada para siempre!")

# 3. CÁLCULOS DE COBRO
st.markdown("### 💳 Cobro")
banco = st.radio("Sistema:", ["BNA (Más Pagos)", "Getnet (Santander)"], horizontal=True)
metodo = st.radio("Medio:", ["Link de Pago", "POS Físico / QR"], horizontal=True)

if banco == "BNA (Más Pagos)":
    r1, r3, r6 = (1.042, 1.12, 1.20) if metodo == "Link de Pago" else (1.033, 1.10, 1.18)
else:
    r1, r3, r6 = (1.045, 1.16, 1.29) if metodo == "Link de Pago" else (1.038, 1.14, 1.25)

t1, t3, t6 = monto_limpio * r1, monto_limpio * r3, monto_limpio * r6

# 4. RESULTADOS EN PANTALLA
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

# --- 📜 HISTORIAL (Desde Google Sheets) ---
st.divider()
st.subheader("📋 Historial Permanente (Nube)")
try:
    df = conn.read(worksheet="Ventas")
    if not df.empty:
        st.dataframe(df[::-1], use_container_width=True)
        ganancia = df["Venta $"].sum() - df["Compra $"].sum()
        st.info(f"💰 **Ganancia Total: $ {ganancia:,.2f}**")
except:
    st.info("No hay datos guardados en la nube aún.")

# 5. WHATSAPP (Presupuesto Limpio)
maps_link = "https://www.google.com/maps/search/Crespo+4117+Rosario"
s = "\u200e" # Espacio invisible

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
    f"📸  *Instagram:* *@embraguesrosario*\n"
    f"⏰  *Horario:* 8:30 a 17:00 hs\n\n"
    f"¡Te esperamos pronto! 🙋🏻"
)

link_wa = f"https://wa.me/?text={urllib.parse.quote(mensaje)}"
st.link_button("🟢 ENVIAR POR WHATSAPP", link_wa)
