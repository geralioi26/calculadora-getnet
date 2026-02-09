import streamlit as st
import urllib.parse
from PIL import Image
import numpy as np
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. IDENTIDAD
st.set_page_config(page_title="Embragues Rosario", page_icon="logo.png")
st.image("logo.png", width=300) 
st.title("Embragues Rosario")
st.markdown("Crespo 4117, Rosario | **IIBB: EXENTO**")

# --- 💾 CONEXIÓN A GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def guardar_en_google(categoria, cliente, vehiculo, detalle, p_venta, p_compra, proveedor, codigo):
    fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
    try:
        df_existente = conn.read(worksheet="Ventas")
    except:
        df_existente = pd.DataFrame(columns=["Fecha", "Categoría", "Cliente", "Vehículo", "Detalle", "Venta $", "Compra $", "Proveedor", "Código"])
    
    nuevo_reg = pd.DataFrame([[fecha_hoy, categoria, cliente, vehiculo, detalle, p_venta, p_compra, proveedor, codigo]], 
                             columns=df_existente.columns)
    
    df_actualizado = pd.concat([df_existente, nuevo_reg], ignore_index=True)
    conn.update(worksheet="Ventas", data=df_actualizado)

# 2. CONFIGURACIÓN (Sidebar)
st.sidebar.header("⚙️ Configuración")
monto_limpio = st.sidebar.number_input("Precio de VENTA ($):", min_value=0, value=210000)
vehiculo = st.sidebar.text_input("Vehículo:", "Renault Sandero")
cliente_nombre = st.sidebar.text_input("Nombre del Cliente:", "Consumidor Final")

tipo_item = st.sidebar.selectbox("Tipo de Trabajo:", 
                                ["Embrague Nuevo (Venta)", 
                                 "Reparación de Embrague", 
                                 "Kit de Distribución",
                                 "Otro / Solo Mano de Obra"])

# Lógica de sugerencia de texto
if "Nuevo" in tipo_item:
    categoria, icono, incluye_rectif = "Venta", "⚙️", True
    marca = st.sidebar.text_input("Marca del Kit:", "Sachs")
    sugerencia = f"KIT nuevo marca *{marca}*"
elif "Reparación" in tipo_item:
    categoria, icono, incluye_rectif = "Reparación", "🔧", False
    marcas_crap = st.sidebar.multiselect("Marcas de Crapodina:", ["Luk", "Skf", "Ina", "Dbh", "The"], default=["Luk", "Skf"])
    m_neg = [f"*{m}*" for m in marcas_crap]
    texto_marcas = ", ".join(m_neg[:-1]) + " o " + m_neg[-1] if len(m_neg) > 1 else (m_neg[0] if m_neg else "*primera marca*")
    sugerencia = f"reparado completo placa disco con forros originales volante rectificado y balanceado con crapodina {texto_marcas}"
elif "Distribución" in tipo_item:
    categoria, icono, incluye_rectif = "Venta", "🛠️", False
    marca_dist = st.sidebar.text_input("Marca:", "Skf")
    sugerencia = f"KIT de distribución marca *{marca_dist}*"
else:
    categoria, icono, incluye_rectif = "Trabajo", "🛠️", False
    sugerencia = "Escribí acá qué le hiciste..."

# --- ✍️ CAMPO EDITABLE (Lo que vos pediste) ---
st.sidebar.divider()
texto_detalle_final = st.sidebar.text_area("Detalle final (podés editarlo a mano):", value=sugerencia)
label_item = "*Trabajo:*" if categoria != "Venta" else "*Producto:*"

# --- 🔍 STOCK E INTERNO ---
st.sidebar.divider()
st.sidebar.write("📸 **Control Interno**")
codigo_manual = st.sidebar.text_input("Código o Nro de Serie:")
foto = st.sidebar.file_uploader("Subir foto:", type=["jpg", "png", "jpeg"])

if foto is not None:
    try:
        img_pil = Image.open(foto)
        st.sidebar.image(img_pil, caption="Imagen cargada", use_container_width=True)
    except:
        st.sidebar.error("Error al procesar la imagen.")

st.sidebar.write("📥 **Costos**")
precio_compra = st.sidebar.number_input("Costo real ($):", min_value=0, value=0)
proveedor = st.sidebar.text_input("Proveedor:", "Repuestos Rosario")

if st.sidebar.button("💾 GUARDAR OPERACIÓN"):
    guardar_en_google(categoria, cliente_nombre, vehiculo, texto_detalle_final, monto_limpio, precio_compra, proveedor, codigo_manual)
    st.sidebar.success(f"¡Guardado en la Nube!")

# 3. COBRO BNA
st.markdown("### 💳 Cobro BNA (Más Pagos)")
metodo = st.radio("Medio:", ["Link de Pago", "POS Físico / QR"], horizontal=True)

if metodo == "Link de Pago":
    r1, r3, r6 = 1.042, 1.12, 1.20
else:
    r1, r3, r6 = 1.033, 1.10, 1.18

t1, t3, t6 = monto_limpio * r1, monto_limpio * r3, monto_limpio * r6

# 4. RESULTADOS
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

# --- 📜 HISTORIAL ---
st.divider()
st.subheader("📋 Historial de Movimientos")
try:
    df = conn.read(worksheet="Ventas")
    if not df.empty:
        st.dataframe(df[::-1], use_container_width=True)
except:
    st.info("Conectá tu Google Sheet para ver el historial.")

# 5. WHATSAPP
maps_link = "http://googleusercontent.com/maps.google.com/search/Crespo+4117+Rosario"
s = "\u200e" 
linea_extra = f"✅  *Incluye rectificación y balanceo de volante*\n" if incluye_rectif else ""

mensaje = (
    f"🚗  *EMBRAGUES ROSARIO*\n"
    f"Te paso el presupuesto detallado:\n\n"
    f"🚗  *Vehículo:* {vehiculo}\n"
    f"{icono}  {label_item} {texto_detalle_final}\n"
    f"{linea_extra}\n"
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
