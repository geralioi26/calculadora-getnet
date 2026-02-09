import streamlit as st
import urllib.parse
from PIL import Image
import numpy as np
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. IDENTIDAD Y CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Embragues Rosario", page_icon="logo.png")
st.image("logo.png", width=300) 
st.title("Embragues Rosario")
st.markdown("Crespo 4117, Rosario | **IIBB: EXENTO**")

# --- 💾 CONEXIÓN PERMANENTE A GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def guardar_en_google(cat, cliente, vehiculo, detalle, p_venta, p_compra, proveedor, codigo):
    fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
    try:
        # Usamos "Ventas" con V mayúscula como está en tu planilla
        df_existente = conn.read(worksheet="Ventas")
    except:
        # Si la hoja está vacía, creamos los encabezados exactos de tu foto
        df_existente = pd.DataFrame(columns=["fecha", "categoria", "cliente", "vehiculo", "detalle", "venta $", "compra $", "proveedor", "codigo"])
    
    nuevo_reg = pd.DataFrame([[fecha_hoy, cat, cliente, vehiculo, detalle, p_venta, p_compra, proveedor, codigo]], 
                             columns=df_existente.columns)
    
    df_actualizado = pd.concat([df_existente, nuevo_reg], ignore_index=True)
    
    # Guardamos en la nube (Requiere permisos de Editor en Google Sheets)
    conn.update(worksheet="Ventas", data=df_actualizado)

# 2. CONFIGURACIÓN DEL TRABAJO (Sidebar)
st.sidebar.header("⚙️ Configuración")
monto_limpio = st.sidebar.number_input("Precio de VENTA ($):", min_value=0, value=0)
vehiculo_input = st.sidebar.text_input("Vehículo:", "citroen c4 motor tu5 1.6 16v")
cliente_input = st.sidebar.text_input("Nombre del Cliente:", "Consumidor Final")

tipo_item = st.sidebar.selectbox("Tipo de Trabajo:", 
                                ["Embrague Nuevo (Venta)", 
                                 "Reparación de Embrague", 
                                 "Kit de Distribución",
                                 "Solo Rectificación/Balanceo",
                                 "Otro / Solo Mano de Obra"])

# Lógica de sugerencias automáticas de texto
if "Nuevo" in tipo_item:
    cat, icono, incl_rectif = "Venta", "⚙️", True
    marca = st.sidebar.text_input("Marca del Kit:", "Sachs")
    sugerencia = f"KIT nuevo marca *{marca}*"
elif "Reparación" in tipo_item:
    cat, icono, incl_rectif = "Reparación", "🔧", False
    marcas_crap = st.sidebar.multiselect("Marcas de Crapodina:", ["Luk", "Skf", "Ina", "Dbh", "The"], default=["Luk", "Skf"])
    m_neg = [f"*{m}*" for m in marcas_crap]
    t_m = ", ".join(m_neg[:-1]) + " o " + m_neg[-1] if len(m_neg) > 1 else (m_neg[0] if m_neg else "*primera marca*")
    sugerencia = f"reparado completo placa disco con forros originales volante rectificado y balanceado con crapodina {t_m}"
elif "Distribución" in tipo_item:
    cat, icono, incl_rectif = "Venta", "🛠️", False
    m_dist = st.sidebar.text_input("Marca:", "Skf")
    sugerencia = f"KIT de distribución marca *{m_dist}*"
else:
    cat, icono, incl_rectif = "Trabajo", "🔧", False
    sugerencia = "Escribí acá el detalle del laburo..."

# --- ✍️ CAMPO EDITABLE (Para que cargues lo que quieras a mano) ---
st.sidebar.divider()
detalle_final = st.sidebar.text_area("Detalle final (podés editarlo):", value=sugerencia)
label_item = "*Producto:*" if cat == "Venta" else "*Trabajo:*"

# --- 🔍 DATOS DE CONTROL INTERNO ---
st.sidebar.divider()
st.sidebar.write("📸 **Uso Interno**")
codigo_manual = st.sidebar.text_input("Código de repuesto:")
foto = st.sidebar.file_uploader("Subir foto:", type=["jpg", "png", "jpeg"])

if foto is not None:
    try:
        # Corrección para el ValueError: usamos Pillow para procesar la imagen
        img_pil = Image.open(foto) 
        st.sidebar.image(img_pil, caption="Imagen cargada", use_container_width=True)
    except:
        st.sidebar.error("Error al procesar la imagen.")

st.sidebar.write("📥 **Costos**")
precio_compra = st.sidebar.number_input("Precio de COMPRA ($):", min_value=0, value=0)
proveedor_input = st.sidebar.text_input("Proveedor:", "Repuestos Rosario")

if st.sidebar.button("💾 GUARDAR PARA SIEMPRE"):
    guardar_en_google(cat, cliente_input, vehiculo_input, detalle_final, monto_limpio, precio_compra, proveedor_input, codigo_manual)
    st.sidebar.success("¡Venta guardada correctamente en el Excel de Google!")

# 3. CÁLCULO DE COBRO (SOLO BANCO NACIÓN)
st.markdown("### 💳 Cobro BNA (Más Pagos)")
metodo = st.radio("Medio:", ["Link de Pago", "POS Físico / QR"], horizontal=True)

# Tasas exclusivas de BNA (Quitamos Getnet)
if metodo == "Link de Pago":
    r1, r3, r6 = 1.042, 1.12, 1.20
else:
    r1, r3, r6 = 1.033, 1.10, 1.18

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

# --- 📜 HISTORIAL (Se actualiza solo desde Google) ---
st.divider()
st.subheader("📋 Historial de Ventas y Reparaciones")
try:
    df = conn.read(worksheet="Ventas")
    if not df.empty:
        # Mostramos los últimos movimientos primero
        st.dataframe(df[::-1], use_container_width=True)
        ganancia_bruta = df["venta $"].sum() - df["compra $"].sum()
        st.info(f"💰 **Utilidad Total Acumulada: $ {ganancia_bruta:,.2f}**")
except:
    st.info("No hay datos en la nube o falta conectar el link en 'Secrets'.")

# 5. WHATSAPP (Presupuesto limpio)
maps_link = "http://googleusercontent.com/maps.google.com/search/Crespo+4117+Rosario"
ig_link = "https://www.instagram.com/embraguesrosario/"
s = "‎" # Espacio invisible para evitar errores de formato en precios
linea_rectif = f"✅  *Incluye rectificación y balanceo de volante*\n" if incl_rectif else ""

mensaje = (
    f"🚗  *EMBRAGUES ROSARIO*\n"
    f"Te paso el presupuesto detallado:\n\n"
    f"🚗  *Vehículo:* {vehiculo_input}\n"
    f"{icono}  {label_item} {detalle_final}\n"
    f"{linea_rectif}\n"
    f"💰  *EFECTIVO / TRANSF:* ${s}{monto_limpio:,.0f}\n\n"
    f"💳  *TARJETA BANCARIA (BNA):*\n"
    f"✅  *1 pago:* ${s}{t1:,.0f}\n"
    f"✅  *3 cuotas de:* ${s}{t3/3:,.2f}\n"
    f"     (Total: ${s}{t3:,.0f})\n\n"
    f"✅  *6 cuotas de:* ${s}{t6/6:,.2f}\n"
    f"     (Total: ${s}{t6:,.0f})\n\n"
    f"📍  *Dirección:* Crespo 4117, Rosario\n"
    f"📍  *Ubicación:* {maps_link}\n"
    f"📸  *Instagram:* *@embraguesrosario*\n"
    f"⏰  *Horario:* 8:30 a 17:00 hs\n\n"
    f"¡Te esperamos! 🙋🏻"
)

link_wa = f"https://wa.me/?text={urllib.parse.quote(mensaje)}"
st.link_button("🟢 ENVIAR POR WHATSAPP", link_wa)
