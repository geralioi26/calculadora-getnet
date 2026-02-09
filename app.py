import streamlit as st
import urllib.parse
from PIL import Image
import pandas as pd
import os
from datetime import datetime

# 1. IDENTIDAD Y CONFIGURACIÓN (Vuelve tu logo a la pestaña)
st.set_page_config(page_title="Embragues Rosario", page_icon="logo.png")
st.image("logo.png", width=300) 
st.title("Embragues Rosario")
st.markdown("Crespo 4117, Rosario | **IIBB: EXENTO**")

# --- LÓGICA DE GESTIÓN (Base de Datos sin Duplicados) ---
ARCHIVO_INVENTARIO = "inventario_ventas.csv"
COLUMNAS = ["Fecha", "Cliente", "Vehículo/Compatibilidad", "Detalle", "Venta $", "Compra $", "Proveedor", "Código Luk", "Código Sachs", "Observaciones"]

def guardar_o_actualizar(cliente, vehiculo, detalle, p_venta, p_compra, prov, c_luk, c_sachs, obs):
    fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
    if os.path.isfile(ARCHIVO_INVENTARIO):
        df = pd.read_csv(ARCHIVO_INVENTARIO)
    else:
        df = pd.DataFrame(columns=COLUMNAS)

    # Lógica inteligente para no duplicar repuestos
    existe_luk = (c_luk != "" and c_luk in df['Código Luk'].values)
    existe_sachs = (c_sachs != "" and c_sachs in df['Código Sachs'].values)

    if existe_luk or existe_sachs:
        idx = df[df['Código Luk'] == c_luk].index[0] if existe_luk else df[df['Código Sachs'] == c_sachs].index[0]
        # Sumamos compatibilidad si es un auto nuevo
        compat_actual = str(df.at[idx, 'Vehículo/Compatibilidad'])
        if vehiculo not in compat_actual:
            df.at[idx, 'Vehículo/Compatibilidad'] = f"{compat_actual}, {vehiculo}"
        # Actualizamos datos de la última operación
        df.at[idx, 'Fecha'] = fecha_hoy
        df.at[idx, 'Venta $'] = p_venta
        df.at[idx, 'Compra $'] = p_compra
        df.at[idx, 'Proveedor'] = prov
        # Agregamos observaciones nuevas al final
        if obs:
            obs_actual = str(df.at[idx, 'Observaciones']) if pd.notna(df.at[idx, 'Observaciones']) else ""
            df.at[idx, 'Observaciones'] = f"{obs_actual} | {obs}" if obs_actual else obs
        st.sidebar.info("📦 ¡Repuesto detectado! Se actualizó la información.")
    else:
        nueva_fila = pd.DataFrame([[fecha_hoy, cliente, vehiculo, detalle, p_venta, p_compra, prov, c_luk, c_sachs, obs]], columns=COLUMNAS)
        df = pd.concat([df, nueva_fila], ignore_index=True)
        st.sidebar.success("✅ Nuevo repuesto guardado con éxito.")
    df.to_csv(ARCHIVO_INVENTARIO, index=False)

# 2. CONFIGURACIÓN DEL PRESUPUESTO (Sidebar)
st.sidebar.header("⚙️ Configuración")
monto_limpio = st.sidebar.number_input("Precio de VENTA ($):", min_value=0, value=210000, step=5000)
vehiculo_input = st.sidebar.text_input("Vehículo:", "Renault Sandero")
cliente_input = st.sidebar.text_input("Nombre del Cliente:", "Consumidor Final")

tipo_kit = st.sidebar.selectbox("Tipo de Kit:", ["Nuevo", "Reparado completo con crapodina"])

if tipo_kit == "Nuevo":
    marca_kit = st.sidebar.text_input("Marca del Kit Nuevo:", "Sachs")
    label_item, texto_detalle, icono, incluye_rectif = "*Embrague:*", f"KIT nuevo marca *{marca_kit}*", "⚙️", True
else:
    marcas = st.sidebar.multiselect("Marcas de Crapodina:", ["Luk", "Skf", "Ina", "Dbh", "The"], default=["Luk", "Skf"])
    m_negrita = [f"*{m}*" for m in marcas]
    texto_m = ", ".join(m_negrita[:-1]) + " o " + m_negrita[-1] if len(m_negrita) > 1 else (m_negrita[0] if m_negrita else "*primera marca*")
    label_item, texto_detalle, icono, incluye_rectif = "*Trabajo:*", f"reparado completo placa disco con forros originales volante rectificado y balanceado con crapodina {texto_m}", "🔧", False

# --- 🔍 CONTROL DE STOCK (Carga Manual y Foto) ---
st.sidebar.divider()
st.sidebar.write("📸 **Carga de Repuesto (Interno)**")
c_luk = st.sidebar.text_input("Código LUK:")
c_sachs = st.sidebar.text_input("Código SACHS:")
obs_txt = st.sidebar.text_area("Observaciones:")

foto = st.sidebar.file_uploader("Subir foto de la caja:", type=["jpg", "png", "jpeg"])
if foto:
    st.sidebar.image(Image.open(foto), use_container_width=True)

st.sidebar.divider()
st.sidebar.write("📥 **Datos de Compra**")
p_compra = st.sidebar.number_input("Precio de COMPRA ($):", min_value=0, value=0)
proveedor = st.sidebar.text_input("Proveedor:", "icepar")

if st.sidebar.button("💾 GUARDAR O ACTUALIZAR"):
    guardar_o_actualizar(cliente_input, vehiculo_input, texto_detalle, monto_limpio, p_compra, proveedor, c_luk, c_sachs, obs_txt)
    st.rerun()

# 3. PAGOS Y CÁLCULOS
st.markdown("### 💳 Cobro")
banco = st.radio("Sistema:", ["BNA (Más Pagos)", "Getnet (Santander)"], horizontal=True)
metodo = st.radio("Medio:", ["Link de Pago", "POS Físico / QR"], horizontal=True)

if banco == "BNA (Más Pagos)":
    r1, r3, r6 = (1.042, 1.12, 1.20) if metodo == "Link de Pago" else (1.033, 1.10, 1.18)
else:
    r1, r3, r6 = (1.045, 1.16, 1.29) if metodo == "Link de Pago" else (1.038, 1.14, 1.25)

t1, t3, t6 = monto_limpio * r1, monto_limpio * r3, monto_limpio * r6

# 4. VISTA DE LA APP
st.divider()
st.success(f"### **💰 EFECTIVO / TRANSF: $ {monto_limpio:,.0f}**")
c1, c2, c3 = st.columns(3)
with c1: st.metric("1 PAGO", f"$ {t1:,.0f}")
with c2: st.metric("3 CUOTAS DE:", f"$ {t3/3:,.2f}"); st.caption(f"Total:
