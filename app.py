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

def guardar_en_google(cat, cliente, vehiculo, detalle, p_venta, p_compra, proveedor, codigo):
    fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Nombres de columnas EXACTOS como en tu foto image_928686.jpg
    columnas = ["fecha", "categoria", "cliente", "vehiculo", "detalle", "venta $", "compra $", "proveedor", "codigo"]
    
    try:
        # worksheet="Ventas" con V mayúscula como en la pestaña de tu foto
        df_existente = conn.read(worksheet="Ventas")
        if df_existente is None or df_existente.empty:
            df_existente = pd.DataFrame(columns=columnas)
    except Exception:
        df_existente = pd.DataFrame(columns=columnas)
    
    # Creamos el nuevo registro
    nuevo_reg = pd.DataFrame([[fecha_hoy, cat, cliente, vehiculo, detalle, p_venta, p_compra, proveedor, codigo]], 
                             columns=columnas)
    
    # Unimos y guardamos
    df_actualizado = pd.concat([df_existente, nuevo_reg], ignore_index=True)
    
    # Esta es la parte que daba el error rosa
    conn.update(worksheet="Ventas", data=df_actualizado)

# 2. CONFIGURACIÓN (Sidebar)
st.sidebar.header("⚙️ Configuración")
monto_limpio = st.sidebar.number_input("Precio de VENTA ($):", min_value=0, value=0)
vehiculo_input = st.sidebar.text_input("Vehículo:", "Escribí el modelo acá")
cliente_input = st.sidebar.text_input("Nombre del Cliente:", "Consumidor Final")

tipo_item = st.sidebar.selectbox("Tipo de Trabajo:", 
                                ["Embrague Nuevo (Venta)", 
                                 "Reparación de Embrague", 
                                 "Kit de Distribución",
                                 "Solo Rectificación/Balanceo",
                                 "Otro / Solo Mano de Obra"])

# Sugerencias dinámicas
if "Nuevo" in tipo_item:
    cat_final, icono, incl_rectif = "Venta", "⚙️", True
    marca_kit = st.sidebar.text_input("Marca del Kit:", "Sachs")
    sugerencia = f"KIT nuevo marca *{marca_kit}*"
elif "Reparación" in tipo_item:
    cat_final, icono, incl_rectif = "Reparación", "🔧", False
    m_crap = st.sidebar.multiselect("Marcas de Crapodina:", ["Luk", "Skf", "Ina", "Dbh", "The"], default=["Luk", "Skf"])
    m_neg = [f"*{m}*" for m in m_crap]
    t_m = ", ".join(m_neg[:-1]) + " o " + m_neg[-1] if len(m_neg) > 1 else (m_neg[0] if m_neg else "*primera marca*")
    sugerencia = f"reparado completo placa disco con forros originales volante rectificado y balanceado con crapodina {t_m}"
elif "Distribución" in tipo_item:
    cat_final, icono, incl_rectif = "Venta", "🛠️", False
    marca_dist = st.sidebar.text_input("Marca:", "Skf")
    sugerencia = f"KIT de distribución marca *{marca_dist}*"
else:
    cat_final, icono, incl_rectif = "Trabajo", "🔧", False
    sugerencia = "Detalle del laburo..."

# Cuadro editable (Tu pedido)
st.sidebar.divider()
detalle_final = st.sidebar.text_area("Detalle final (podés editarlo):", value=sugerencia)
label_item = "*Producto:*" if cat_final == "Venta" else "*Trabajo:*"

# --- 🔍 CONTROL INTERNO ---
st.sidebar.divider()
st.sidebar.write("📸 **Uso Interno**")
codigo_manual = st.sidebar.text_input("Código de repuesto / Kit:")
precio_compra = st.sidebar.number_input("Precio de COMPRA ($):", min_value=0, value=0)
proveedor_input = st.sidebar.text_input("Proveedor:", "icepar")

if st.sidebar.button("💾 GUARDAR PARA SIEMPRE"):
    guardar_en_google(cat_final, cliente_input, vehiculo_input, detalle_final, monto_limpio, precio_compra, proveedor_input, codigo_manual)
    st.sidebar.success("¡Venta guardada en tu Excel de Google!")

# 3. COBRO BNA
st.markdown("### 💳 Cobro BNA (Más Pagos)")
metodo = st.radio("Medio:", ["Link de Pago", "POS Físico / QR"], horizontal=True)

r1, r3, r6 = (1.042, 1.12, 1.20) if metodo == "Link de Pago" else (1.033, 1.10, 1.18)
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
st.subheader("📋 Historial en la Nube")
try:
    df_ver = conn.read(worksheet="Ventas")
    if df_ver is not None and not df_ver.empty:
        st.dataframe(df_ver[::-1], use_container_width=True)
except:
    st.info("Conectando con el historial...")

# 5. WHATSAPP
maps_link = "http://googleusercontent.com/maps.google.com/search/Crespo+4117+Rosario"
s = "‎" # Espacio invisible
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
