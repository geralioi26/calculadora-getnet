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

# --- LÓGICA DE GESTIÓN (Base de Datos Inteligente) ---
ARCHIVO_INVENTARIO = "inventario_ventas.csv"
COLUMNAS = ["Fecha", "Cliente", "Vehículo/Compatibilidad", "Detalle", "Venta $", "Compra $", "Proveedor", "Código Luk", "Código Sachs", "Observaciones"]

def guardar_o_actualizar(cliente, vehiculo, detalle, p_venta, p_compra, prov, c_luk, c_sachs, obs):
    fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
    if os.path.isfile(ARCHIVO_INVENTARIO):
        df = pd.read_csv(ARCHIVO_INVENTARIO)
    else:
        df = pd.DataFrame(columns=COLUMNAS)

    # Buscamos si el código ya existe para no duplicar
    existe_luk = (c_luk != "" and c_luk in df['Código Luk'].values)
    existe_sachs = (c_sachs != "" and c_sachs in df['Código Sachs'].values)

    if existe_luk or existe_sachs:
        idx = df[df['Código Luk'] == c_luk].index[0] if existe_luk else df[df['Código Sachs'] == c_sachs].index[0]
        # Sumamos el nuevo vehículo a la lista de compatibilidad si no estaba
        compat_actual = str(df.at[idx, 'Vehículo/Compatibilidad'])
        if vehiculo not in compat_actual:
            df.at[idx, 'Vehículo/Compatibilidad'] = f"{compat_actual}, {vehiculo}"
        
        df.at[idx, 'Fecha'] = fecha_hoy
        df.at[idx, 'Venta $'] = p_venta
        df.at[idx, 'Compra $'] = p_compra
        df.at[idx, 'Proveedor'] = prov
        
        if obs:
            obs_actual = str(df.at[idx, 'Observaciones']) if pd.notna(df.at[idx, 'Observaciones']) else ""
            df.at[idx, 'Observaciones'] = f"{obs_actual} | {obs}" if obs_actual else obs
        st.sidebar.info("📦 ¡Repuesto detectado! Se actualizó la información.")
    else:
        nueva_fila = pd.DataFrame([[fecha_hoy, cliente, vehiculo, detalle, p_venta, p_compra, prov, c_luk, c_sachs, obs]], columns=COLUMNAS)
        df = pd.concat([df, nueva_fila], ignore_index=True)
        st.sidebar.success("✅ Nuevo repuesto guardado.")
    df.to_csv(ARCHIVO_INVENTARIO, index=False)

# 2. CONFIGURACIÓN DEL PRESUPUESTO (Sidebar)
st.sidebar.header("⚙️ Configuración")
monto_limpio = st.sidebar.number_input("Precio de VENTA ($):", min_value=0, value=210000, step=5000)
vehiculo_input = st.sidebar.text_input("Vehículo:", "Renault Sandero")
cliente_input = st.sidebar.text_input("Nombre del Cliente:", "Consumidor Final")

tipo_kit = st.sidebar.selectbox("Tipo de Kit:", ["Nuevo", "Reparado completo con crapodina"])

if tipo_kit == "Nuevo":
    marca_kit = st.sidebar.text_input("Marca del Kit Nuevo:", "Sachs")
    # Cambiamos el engranaje por un ícono de herramientas
    label_item, texto_detalle, icono, incluye_rectif = "*Embrague:*", f"KIT nuevo marca *{marca_kit}*", "🛠️", True
else:
    marcas = st.sidebar.multiselect("Marcas de Crapodina:", ["Luk", "Skf", "Ina", "Dbh", "The"], default=["Luk", "Skf"])
    m_negrita = [f"*{m}*" for m in marcas]
    texto_m = ", ".join(m_negrita[:-1]) + " o " + m_negrita[-1] if len(m_negrita) > 1 else (m_negrita[0] if m_negrita else "*primera marca*")
    label_item, texto_detalle, icono, incluye_rectif = "*Trabajo:*", f"reparado completo placa disco con forros originales volante rectificado y balanceado con crapodina {texto_m}", "🔧", False

# --- 🔍 CONTROL DE STOCK (Carga Manual y Foto) ---
st.sidebar.divider()
st.sidebar.write("📸 **Carga de Repuesto (Uso Interno)**")
c_luk = st.sidebar.text_input("Código LUK:")
c_sachs = st.sidebar.text_input("Código SACHS:")
obs_txt = st.sidebar.text_area("Observaciones (Ej: cruce con otros modelos):")

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
with c2: st.metric("3 CUOTAS DE:", f"$ {t3/3:,.2f}"); st.caption(f"Total: $ {t3:,.0f}")
with c3: st.metric("6 CUOTAS DE:", f"$ {t6/6:,.2f}"); st.caption(f"Total: $ {t6:,.0f}")

# --- 📜 BUSCADOR E HISTORIAL EDITABLE ---
st.divider()
st.subheader("📋 Buscador y Gestión de Laburos")
if os.path.isfile(ARCHIVO_INVENTARIO):
    df_res = pd.read_csv(ARCHIVO_INVENTARIO)
    query = st.text_input("🔍 Buscar por vehículo, marca, código u observación:")
    if query:
        df_res = df_res[df_res.apply(lambda r: query.lower() in r.astype(str).str.lower().values, axis=1)]
    
    # Editor interactivo (Nuevo arriba)
    df_edit = st.data_editor(df_res[::-1], use_container_width=True, num_rows="dynamic")
    
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        if st.button("💾 GUARDAR CAMBIOS EN TABLA"):
            df_edit[::-1].to_csv(ARCHIVO_INVENTARIO, index=False)
            st.success("Historial actualizado."); st.rerun()
    with col_h2:
        if st.button("🗑️ Borrar Historial"):
            os.remove(ARCHIVO_INVENTARIO); st.rerun()
    
    ganancia = df_res["Venta $"].sum() - df_res["Compra $"].sum()
    st.info(f"💰 **Ganancia Acumulada: $ {ganancia:,.2f}**")
else:
    st.info("No hay registros todavía.")

# 5. WHATSAPP (Formato Rosario Impecable)
ig_link = "https://www.instagram.com/embraguesrosario?igsh=MWsxNzI1MTN4ZWJ3eg=="
# Link de búsqueda directo para evitar el error 404
maps_url = "https://www.google.com/maps/search/Crespo+4117+Rosario"
s = "‎" # Espacio invisible anti-subrayado

linea_rectif = f"✅  *Incluye rectificación y balanceo de volante*\n" if incluye_rectif else ""
mensaje = (
    f"🚗  *EMBRAGUES ROSARIO*\n"
    f"¡Hola! Gracias por tu consulta. Te paso el presupuesto:\n\n"
    f"🚗  *Vehículo:* {vehiculo_input}\n"
    f"{icono}  {label_item} {texto_detalle}\n"
    f"{linea_rectif}\n" 
    f"💰  *EFECTIVO / TRANSF:* ${s}{monto_limpio:,.0f}\n\n"
    f"💳  *TARJETA BANCARIA ({metodo}):*\n"
    f"✅  *1 pago:* ${s}{t1:,.0f}\n"
    f"✅  *3 cuotas de:* ${s}{t3/3:,.2f}  (Total: ${s}{t3:,.0f})\n"
    f"✅  *6 cuotas de:* ${s}{t6/6:,.2f}  (Total: ${s}{t6:,.0f})\n\n"
    f"📍  *Dirección:* Crespo 4117, Rosario\n"
    f"📍  *Ubicación:* {maps_url}\n"
    f"📸  *Instagram:* *@embraguesrosario*\n"
    f"     {ig_link}\n"
    f"⏰  *Horario:* 8:30 a 17:00 hs\n\n"
    f"¡Te esperamos pronto! 🙋🏻"
)

link_wa = f"https://wa.me/?text={urllib.parse.quote(mensaje)}"
st.divider()
st.link_button("🟢 ENVIAR POR WHATSAPP", link_wa)
