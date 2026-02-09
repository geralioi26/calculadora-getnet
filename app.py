import streamlit as st
import urllib.parse
from PIL import Image
import numpy as np
import pandas as pd
import os
from datetime import datetime

# 1. IDENTIDAD Y CONFIGURACIÓN (Vuelve tu logo a la pestaña)
st.set_page_config(page_title="Embragues Rosario", page_icon="logo.png")
st.image("logo.png", width=300) 
st.title("Embragues Rosario")
st.markdown("Crespo 4117, Rosario | **IIBB: EXENTO**")

# --- LÓGICA DE GESTIÓN (Ventas, Compras y Fecha) ---
ARCHIVO_INVENTARIO = "inventario_ventas.csv"

def guardar_operacion(cliente, vehiculo, detalle, p_venta, p_compra, proveedor, codigo):
    fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
    nuevo_registro = pd.DataFrame([[fecha_hoy, cliente, vehiculo, detalle, p_venta, p_compra, proveedor, codigo]], 
                                  columns=["Fecha", "Cliente", "Vehículo", "Detalle", "Venta $", "Compra $", "Proveedor", "Código"])
    if not os.path.isfile(ARCHIVO_INVENTARIO):
        nuevo_registro.to_csv(ARCHIVO_INVENTARIO, index=False)
    else:
        nuevo_registro.to_csv(ARCHIVO_INVENTARIO, mode='a', header=False, index=False)

# 2. CONFIGURACIÓN DEL TRABAJO (Sidebar)
st.sidebar.header("⚙️ Configuración")
monto_limpio = st.sidebar.number_input("Precio de VENTA ($):", min_value=0, value=210000, step=5000)
vehiculo = st.sidebar.text_input("Vehículo:", "Renault Sandero")
cliente_nombre = st.sidebar.text_input("Nombre del Cliente:", "Consumidor Final")

tipo_kit = st.sidebar.selectbox("Tipo de Kit:", ["Nuevo", "Reparado completo con crapodina"])

# Lógica dinámica fiel a tus pedidos (balanceado / sin paréntesis)
if tipo_kit == "Nuevo":
    marca_kit = st.sidebar.text_input("Marca del Kit Nuevo:", "Sachs")
    label_item, texto_detalle, icono = "*Embrague:*", f"KIT nuevo marca *{marca_kit}*", "⚙️"
    incluye_rectif = True 
else:
    marcas_disponibles = ["Luk", "Skf", "Ina", "Dbh", "The"]
    marcas_elegidas = st.sidebar.multiselect("Marcas de Crapodina:", marcas_disponibles, default=["Luk", "Skf"])
    m_negrita = [f"*{m}*" for m in marcas_elegidas]
    texto_marcas = ", ".join(m_negrita[:-1]) + " o " + m_negrita[-1] if len(m_negrita) > 1 else (m_negrita[0] if m_negrita else "*primera marca*")
    label_item, texto_detalle, icono = "*Trabajo:*", f"reparado completo placa disco con forros originales volante rectificado y balanceado con crapodina {texto_marcas}", "🔧"
    incluye_rectif = False 

# --- 🔍 CONTROL DE STOCK (Carga Manual y Foto arreglada) ---
st.sidebar.divider()
st.sidebar.write("📸 **Control de Stock (Uso Interno)**")
codigo_manual = st.sidebar.text_input("Código de repuesto (Manual):")

foto = st.sidebar.file_uploader("O subir foto de caja para código:", type=["jpg", "png", "jpeg"])
if foto is not None:
    try:
        # Arreglo para el ValueError: convertimos la foto para que la app la entienda
        img_pil = Image.open(foto)
        img_array = np.array(img_pil) 
        st.sidebar.image(img_pil, caption="Foto cargada correctamente", use_container_width=True)
    except Exception:
        st.sidebar.error("Error al procesar la imagen.")

st.sidebar.divider()
st.sidebar.write("📥 **Datos de Compra**")
precio_compra = st.sidebar.number_input("Precio de COMPRA ($):", min_value=0, value=0)
proveedor = st.sidebar.text_input("Proveedor:", "Repuestos Rosario")

if st.sidebar.button("💾 GUARDAR OPERACIÓN"):
    guardar_operacion(cliente_nombre, vehiculo, texto_detalle, monto_limpio, precio_compra, proveedor, codigo_manual)
    st.sidebar.success(f"¡Venta de {vehiculo} guardada!")

# 3. CÁLCULOS DE COBRO
st.markdown("### 💳 Cobro")
col_b, col_m = st.columns(2)
with col_b:
    banco = st.radio("Sistema:", ["BNA (Más Pagos)", "Getnet (Santander)"], horizontal=True)
with col_m:
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

# --- 📜 HISTORIAL (Lo más nuevo arriba) ---
st.divider()
st.subheader("📋 Laburos Realizados (Nuevo primero)")
if os.path.isfile(ARCHIVO_INVENTARIO):
    df = pd.read_csv(ARCHIVO_INVENTARIO)
    st.dataframe(df[::-1], use_container_width=True)
    ganancia = df["Venta $"].sum() - df["Compra $"].sum()
    st.info(f"💰 **Ganancia Acumulada: $ {ganancia:,.2f}**")
    if st.button("🗑️ Borrar Historial"):
        os.remove(ARCHIVO_INVENTARIO)
        st.rerun()
else:
    st.info("No hay operaciones registradas.")

# 5. WHATSAPP (Limpio para el cliente y ubicación directa)
maps_link = "https://www.google.com/maps/search/Crespo+4117+Rosario"
ig_link = "https://www.instagram.com/embraguesrosario/"
s = "‎" # Espacio invisible para evitar subrayados azules

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
    f"     {ig_link}\n"
    f"⏰  *Horario:* 8:30 a 17:00 hs\n\n"
    f"¡Te esperamos pronto! 🙋🏻"
)

link_wa = f"https://wa.me/?text={urllib.parse.quote(mensaje)}"
st.link_button("🟢 ENVIAR POR WHATSAPP", link_wa)
