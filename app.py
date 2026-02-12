import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
import urllib.parse
from PIL import Image

# 1. IDENTIDAD
st.set_page_config(page_title="Embragues Rosario", page_icon="logo.png")
try:
    st.image("logo.png", width=300)
except:
    pass
st.title("Embragues Rosario")
st.markdown("Crespo 4117, Rosario | **IIBB: EXENTO**")

# ==========================================
# 🚨 PEGA TU LINK ACÁ ABAJO ENTRE LAS COMILLAS
# ==========================================
SHEET_URL = "https://docs.google.com/spreadsheets/d/1YJHJ006kr-izLHG9Ib5CRUX5VUdu6INRDsKn4u0x32Y/edit?gid=0#gid=0" 
# Ejemplo: "https://docs.google.com/spreadsheets/d/12345abcd/edit"
# ==========================================

# --- CONEXIÓN SEGURA ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.stop()

# --- CARGA DE CATÁLOGOS (NUEVO) ---
try:
    # Leemos las 4 hojas de una para tenerlas listas
    df = conn.read(spreadsheet=SHEET_URL, worksheet="Ventas", ttl=0)
    df_kits = conn.read(spreadsheet=SHEET_URL, worksheet="Catalogo_Kits", ttl=0)
    df_crapo = conn.read(spreadsheet=SHEET_URL, worksheet="Catalogo_Crapodinas", ttl=0)
    df_distri = conn.read(spreadsheet=SHEET_URL, worksheet="Catalogo_Distribucion", ttl=0)
except:
    st.warning("⚠️ Todavía no pude leer los catálogos. (Si recién creaste las hojas, dame unos segundos)")

def guardar_en_google(cat, cliente, vehiculo, detalle, p_venta, p_compra, proveedor, codigo, f_pago):
# Ajuste horario Argentina
    fecha_hoy = (datetime.now() - timedelta(hours=3)).strftime("%d/%m/%Y %H:%M")
    columnas = ["fecha", "categoria", "cliente", "vehiculo", "detalle", "venta $", "compra $", "proveedor", "codigo", "forma de pago"]
    
    try:
        # Usamos el LINK EXACTO que pusiste arriba
        df_existente = conn.read(spreadsheet=SHEET_URL, worksheet="Ventas", ttl=0)
    except Exception as e:
        st.error(f"No encuentro la hoja. Revisá que el link sea correcto y que hayas compartido con el robot. Error: {e}")
        st.stop()
    
    # Aseguramos columnas
    for col in columnas:
        if col not in df_existente.columns:
            df_existente[col] = ""

    nuevo_reg = pd.DataFrame([[fecha_hoy, cat, cliente, vehiculo, detalle, p_venta, p_compra, proveedor, codigo, f_pago]], 
                             columns=columnas)
    
    df_actualizado = pd.concat([df_existente, nuevo_reg], ignore_index=True)
    
    # Guardamos forzando el link
    conn.update(spreadsheet=SHEET_URL, worksheet="Ventas", data=df_actualizado)

# 2. PANEL DE CARGA
st.sidebar.header("⚙️ Configuración")

tipo_item = st.sidebar.selectbox("Tipo de Trabajo:", 
                                ["Embrague Nuevo (Venta)", 
                                 "Reparación de Embrague", 
                                 "Kit de Distribución",
                                 "Otro"])

if "Nuevo" in tipo_item:
    cat_f, icono, incl_rectif = "Venta", "⚙️", True
    m_kit = st.sidebar.text_input("Marca del Kit:", "Sachs")
    sugerencia = f"KIT nuevo marca *{m_kit}*"
elif "Reparación" in tipo_item:
    cat_f, icono, incl_rectif = "Reparación", "🔧", False
    m_crap = st.sidebar.multiselect("Marcas de Crapodina:", ["Luk", "Skf", "Ina", "Dbh", "The"], default=["Luk", "Skf"])
    
    m_neg = [f"*{m}*" for m in m_crap]
    if len(m_neg) > 1: t_m = ", ".join(m_neg[:-1]) + " o " + m_neg[-1]
    elif m_neg: t_m = m_neg[0]
    else: t_m = "*primera marca*"
        
    sugerencia = f"reparado completo placa disco con forros originales volante rectificado y balanceado con crapodina {t_m}"
else:
    cat_f, icono, incl_rectif = "Venta", "🛠️", False
    sugerencia = "KIT de distribución"

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

if st.sidebar.button("💾 GUARDAR VENTA"):
    guardar_en_google(cat_f, cliente_input, vehiculo_input, detalle_final, monto_limpio, precio_compra, proveedor_input, codigo_manual, f_pago_input)
    st.sidebar.success(f"¡Venta de $ {monto_limpio:,.0f} guardada!")
# 3. CALCULADORA MULTI-POS (GETNET vs MÁS PAGOS)
st.markdown("### 💳 Calculadora de Cuotas")

# Selector de POSNET
tipo_pos = st.radio("¿Qué POS vas a usar?", ["GETNET (Plan MiPyME)", "MÁS PAGOS (BNA)"], horizontal=True)

# Check de Link de Pago
es_link = st.checkbox("🔗 Es Link de Pago (+1% costo extra)")
extra_link = 1.01 if es_link else 1.00

# COEFICIENTES BASE (Interés + Comisión + IVA)
if "GETNET" in tipo_pos:
    # Getnet: Comisión Venta ~2% + IVA
    # Recargos Finales: 1(2.5%), 3(11.3%), 6(20.5%), 9(42.4%), 12(56.2%)
    c1, c3, c6, c9, c12 = 1.025, 1.113, 1.205, 1.424, 1.562
    nombre_pos = "GETNET"
else:
    # Más Pagos: Comisión Venta ~3% + IVA
    # Recargos Finales: 1(3.8%), 3(12.7%), 6(21.9%), 9(44.2%), 12(58.2%)
    c1, c3, c6, c9, c12 = 1.038, 1.127, 1.219, 1.442, 1.582
    nombre_pos = "MÁS PAGOS"

# Calculamos los Totales (Precio Limpio * Coeficiente * Extra Link)
t1 = monto_limpio * c1 * extra_link
t3 = monto_limpio * c3 * extra_link
t6 = monto_limpio * c6 * extra_link
t9 = monto_limpio * c9 * extra_link
t12 = monto_limpio * c12 * extra_link
# MOSTRAR PORCENTAJES (Para control interno)
p_1, p_3, p_6, p_9, p_12 = [(x * extra_link - 1) * 100 for x in [c1, c3, c6, c9, c12]]
st.info(f"📊 **Recargos Reales:** 1p: {p_1:.1f}% | 3c: {p_3:.1f}% | 6c: {p_6:.1f}% | 9c: {p_9:.1f}% | 12c: {p_12:.1f}%")

st.divider()
# PRECIO CONTADO DESTACADO (Tu pedido: que llame la atención)
st.markdown(f"""
    <div style='background-color: #d4edda; padding: 10px; border-radius: 5px; text-align: center; border: 2px solid #28a745;'>
        <h2 style='color: #155724; margin:0;'>💰 CONTADO / TRANSF: $ {monto_limpio:,.0f}</h2>
        <p style='margin:0; font-size: 0.9em;'>(Este monto te queda limpio)</p>
    </div>
    """, unsafe_allow_html=True)

st.write(f"**Precios de Lista con {nombre_pos}** {'(Link)' if es_link else '(Físico)'}:")

col_a, col_b, col_c = st.columns(3)
with col_a: st.metric("1 PAGO", f"$ {t1:,.0f}")
with col_b: st.metric("3 CUOTAS", f"$ {t3/3:,.2f}", f"Total: ${t3:,.0f}")
with col_c: st.metric("6 CUOTAS", f"$ {t6/6:,.2f}", f"Total: ${t6:,.0f}")

col_d, col_e = st.columns(2)
with col_d: st.metric("9 CUOTAS", f"$ {t9/9:,.2f}", f"Total: ${t9:,.0f}")
with col_e: st.metric("12 CUOTAS", f"$ {t12/12:,.2f}", f"Total: ${t12:,.0f}")

# 4. WHATSAPP (DISEÑO GERARDO + DATOS POS)
if incl_rectif:
    txt_rectif = "\n✅ *Incluye rectificación y balanceo de volante*"
else:
    txt_rectif = ""

# LINKS CORREGIDOS
maps_link = "https://www.google.com/maps?q=Crespo+4117+Rosario"
ig_link = "https://www.instagram.com/embraguesrosario?igsh=MWsxNzI1MTN4ZWJ3eg=="

metodo_txt = f"{nombre_pos} {'(Link)' if es_link else '(Posnet)'}"

mensaje = (
    f"🚗 *EMBRAGUES ROSARIO*\n"
    f"¡Hola! Gracias por tu consulta. Te paso el presupuesto:\n\n"
    f"🚗 *Vehículo:* {vehiculo_input}\n"
    f"{icono} *Embrague:* {detalle_final}"
    f"{txt_rectif}\n\n"
    f"💰 *EFECTIVO / TRANSF:* ${monto_limpio:,.0f}\n\n"
    f"💳 *TARJETA BANCARIA ({metodo_txt}):*\n"
    f"✅ *1 pago:* ${t1:,.0f}\n"
    f"✅ *3 cuotas de:* ${t3/3:,.2f}\n"
    f"     (Total: ${t3:,.0f})\n\n"
    f"✅ *6 cuotas de:* ${t6/6:,.2f}\n"
    f"     (Total: ${t6:,.0f})\n\n"
    f"✅ *12 cuotas de:* ${t12/12:,.2f}\n"
    f"     (Total: ${t12:,.0f})\n\n"
    f"📍 *Dirección:* Crespo 4117, Rosario\n"
    f"📍 *Ubicación:* {maps_link}\n"
    f"📸 *Instagram:* *@embraguesrosario*\n"
    f"     {ig_link}\n"
    f"⏰ *Horario:* 8:30 a 17:00 hs\n\n"
    f"¡Te esperamos pronto! 🙋🏻"
)

link_wa = f"https://wa.me/?text={urllib.parse.quote(mensaje)}"
st.link_button("🟢 ENVIAR PRESUPUESTO POR WHATSAPP", link_wa)

# 5. HISTORIAL (RECUPERADO)
st.divider()
st.subheader("📋 Últimos Movimientos")
try:
    # Usamos conn que ya definimos arriba
    df_ver = conn.read(spreadsheet=SHEET_URL, worksheet="Ventas", ttl=0)
    if not df_ver.empty:
        # Mostramos las últimas 5 ventas (invertido para ver la más reciente arriba)
        st.dataframe(df_ver.tail(5)[::-1], use_container_width=True)
    else:
        st.info("La planilla está vacía todavía.")
except Exception as e:
    st.info("Conectando con Google Sheets...")

# --- PRUEBA DE CONEXIÓN (BORRAR DESPUÉS) ---
st.divider()
st.subheader("🧪 TEST DE CONEXIÓN")
st.write("Si ves las tablas vacías acá abajo, es que conectó perfecto:")

st.caption("📂 Catálogo de KITS:")
st.dataframe(df_kits)

st.caption("📂 Catálogo de CRAPODINAS:")
st.dataframe(df_crapo)

st.caption("📂 Catálogo de DISTRIBUCIÓN:")
st.dataframe(df_distri)


