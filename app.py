import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import urllib.parse
from PIL import Image

# 1. IDENTIDAD Y CONFIGURACIÓN
st.set_page_config(page_title="Embragues Rosario", page_icon="logo.png")
try:
    st.image("logo.png", width=300)
except:
    st.write("🔧") # Por si no carga la imagen
st.title("Embragues Rosario")
st.markdown("Crespo 4117, Rosario | **IIBB: EXENTO**")

# --- CONEXIÓN SEGURA A SECRETS ---
# Ahora que el botón azul funcionó, esto se conecta solo.
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.stop()

def guardar_en_google(cat, cliente, vehiculo, detalle, p_venta, p_compra, proveedor, codigo, f_pago):
    fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
    # Las 10 columnas exactas de tu Excel
    columnas = ["fecha", "categoria", "cliente", "vehiculo", "detalle", "venta $", "compra $", "proveedor", "codigo", "forma de pago"]
    
    try:
        # ttl=0 para que actualice al instante
        df_existente = conn.read(worksheet="Ventas", ttl=0)
    except:
        df_existente = pd.DataFrame(columns=columnas)
    
    # Aseguramos que existan todas las columnas
    for col in columnas:
        if col not in df_existente.columns:
            df_existente[col] = ""

    nuevo_reg = pd.DataFrame([[fecha_hoy, cat, cliente, vehiculo, detalle, p_venta, p_compra, proveedor, codigo, f_pago]], 
                             columns=columnas)
    
    df_actualizado = pd.concat([df_existente, nuevo_reg], ignore_index=True)
    conn.update(worksheet="Ventas", data=df_actualizado)

# 2. PANEL DE CARGA
st.sidebar.header("⚙️ Configuración")

# Primero definimos el tipo para la lógica de sugerencias
tipo_item = st.sidebar.selectbox("Tipo de Trabajo:", 
                                ["Embrague Nuevo (Venta)", 
                                 "Reparación de Embrague", 
                                 "Kit de Distribución",
                                 "Otro"])

# Lógica inteligente del Taller
if "Nuevo" in tipo_item:
    cat_f, icono, incl_rectif = "Venta", "⚙️", True
    m_kit = st.sidebar.text_input("Marca del Kit:", "Sachs")
    sugerencia = f"KIT nuevo marca *{m_kit}*"
elif "Reparación" in tipo_item:
    cat_f, icono, incl_rectif = "Reparación", "🔧", False
    m_crap = st.sidebar.multiselect("Marcas de Crapodina:", ["Luk", "Skf", "Ina", "Dbh", "The"], default=["Luk", "Skf"])
    
    # Armado del texto de marcas
    m_neg = [f"*{m}*" for m in m_crap]
    if len(m_neg) > 1:
        t_m = ", ".join(m_neg[:-1]) + " o " + m_neg[-1]
    elif m_neg:
        t_m = m_neg[0]
    else:
        t_m = "*primera marca*"
        
    sugerencia = f"reparado completo placa disco con forros originales volante rectificado y balanceado con crapodina {t_m}"
else:
    cat_f, icono, incl_rectif = "Venta", "🛠️", False
    sugerencia = "KIT de distribución"

# Inputs de datos
monto_limpio = st.sidebar.number_input("Precio de VENTA ($):", min_value=0, value=0)
vehiculo_input = st.sidebar.text_input("Vehículo:", "citroen c4 1.6")
cliente_input = st.sidebar.text_input("Nombre del Cliente:", "Consumidor Final")
f_pago_input = st.sidebar.selectbox("Forma de Pago Realizada:", 
                                   ["Efectivo (Contado)", "Transferencia", "Tarjeta BNA - 1 Pago", "Tarjeta BNA - 3 Cuotas", "Tarjeta BNA - 6 Cuotas", "Combinado"])

detalle_final = st.sidebar.text_area("Detalle final (editable):", value=sugerencia)
label_item = "*Producto:*" if cat_f == "Venta" else "*Trabajo:*"

st.sidebar.divider()
st.sidebar.write("📸 **Uso Interno**")
codigo_manual = st.sidebar.text_input("Código de repuesto:", "")
precio_compra = st.sidebar.number_input("Precio de COMPRA ($):", min_value=0, value=0)
proveedor_input = st.sidebar.text_input("Proveedor:", "icepar")

# BOTÓN DE GUARDADO
if st.sidebar.button("💾 GUARDAR VENTA"):
    guardar_en_google(cat_f, cliente_input, vehiculo_input, detalle_final, monto_limpio, precio_compra, proveedor_input, codigo_manual, f_pago_input)
    st.sidebar.success(f"¡Venta de $ {monto_limpio:,.0f} guardada!")

# 3. CALCULADORA BNA
st.markdown("### 💳 Cobro BNA (Más Pagos)")
metodo = st.radio("Medio de Cobro:", ["Link de Pago", "POS Físico / QR"], horizontal=True)
r1, r3, r6 = (1.042, 1.12, 1.20) if metodo == "Link de Pago" else (1.033, 1.10, 1.18)
t1, t3, t6 = monto_limpio * r1, monto_limpio * r3, monto_limpio * r6

st.divider()
st.success(f"### **💰 CONTADO: $ {monto_limpio:,.0f}**")
c1, c2, c3 = st.columns(3)
with c1: st.metric("1 PAGO", f"$ {t1:,.0f}")
with c2: st.metric("3 CUOTAS", f"$ {t3/3:,.2f}")
with c3: st.metric("6 CUOTAS", f"$ {t6/6:,.2f}")

# 4. WHATSAPP PROFESIONAL
maps_link = "http://googleusercontent.com/maps.google.com/search/Crespo+4117+Rosario"
mensaje = (
    f"🚗 *EMBRAGUES ROSARIO*\n"
    f"Vehículo: {vehiculo_input}\n"
    f"{icono} {label_item} {detalle_final}\n"
    f"💰 EFECTIVO: ${monto_limpio:,.0f}\n\n"
    f"💳 BNA:\n"
    f"1 pago: ${t1:,.0f}\n"
    f"3 cuotas: ${t3/3:,.2f}\n"
    f"6 cuotas: ${t6/6:,.2f}\n\n"
    f"📍 Ubicación: {maps_link}"
)
link_wa = f"https://wa.me/?text={urllib.parse.quote(mensaje)}"
st.link_button("🟢 ENVIAR PRESUPUESTO POR WHATSAPP", link_wa)

# 5. HISTORIAL
st.divider()
st.subheader("📋 Últimos Movimientos")
try:
    df_ver = conn.read(worksheet="Ventas", ttl=0)
    if not df_ver.empty:
        # Mostramos las últimas 5 invertidas para ver lo nuevo arriba
        st.dataframe(df_ver.tail(5)[::-1], use_container_width=True)
except:
    st.info("Conectando con Google Sheets...")
