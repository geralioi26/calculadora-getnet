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

# --- FUNCIÓN AUXILIAR: GUARDAR EN CATÁLOGO ---
def actualizar_catalogo_kits(vehiculo, codigo, precio, marca):
    try:
        # 1. Leemos el catálogo actual
        df_kits = conn.read(spreadsheet=SHEET_URL, worksheet="Catalogo_Kits", ttl=0)
        
        # 2. Creamos una fila nueva vacía
        nueva_fila = {col: "" for col in df_kits.columns}
        nueva_fila["Vehiculo"] = vehiculo
        
        # 3. Llenamos la columna EXACTA de la marca
        col_codigo = f"Codigo_{marca}"
        col_precio = f"Precio_{marca}"
        
        if col_codigo in nueva_fila:
            nueva_fila[col_codigo] = codigo
            nueva_fila[col_precio] = precio
            
            # 4. Guardamos
            df_nuevo = pd.DataFrame([nueva_fila])
            df_final = pd.concat([df_kits, df_nuevo], ignore_index=True)
            conn.update(spreadsheet=SHEET_URL, worksheet="Catalogo_Kits", data=df_final)
            st.toast(f"✅ Catálogo actualizado: {marca} guardado!", icon="📒")
        else:
            st.warning(f"⚠️ No encontré la columna '{col_codigo}' en el Excel.")
    except Exception as e:
        st.error(f"Error al guardar en catálogo: {e}")

# --- FUNCIÓN PARA GUARDAR CRAPODINAS NUEVAS (Versión Completa) ---
def actualizar_catalogo_crapodinas(vehiculo, descripcion, codigo, precio, marca):
    try:
        # 1. Leemos el catálogo
        df_crapo = conn.read(spreadsheet=SHEET_URL, worksheet="Catalogo_Crapodinas", ttl=5) # Bajamos a 5 seg para pruebas
        marca_limpia = str(marca).upper()
        col_cod = f"Codigo_{marca_limpia}"
        col_pre = f"Precio_{marca_limpia}"

        if col_cod not in df_crapo.columns:
            st.warning(f"⚠️ La marca {marca_limpia} no tiene columnas.")
            return

        # Limpiamos los datos para comparar (sacamos espacios y pasamos a minúsculas)
        vehiculo_limpio = str(vehiculo).strip().lower()
        desc_limpia = str(descripcion).strip().lower()
        # El código lo limpiamos de ".0" por si el Excel lo tomó como número
        cod_buscado = str(codigo).split('.')[0].strip()

        # --- BUSCADORES ROBUSTOS ---
        # 1. ¿Existe el auto con ese tipo?
        filtro_exacto = (df_crapo['Vehiculo'].astype(str).str.strip().str.lower() == vehiculo_limpio) & \
                        (df_crapo['Descripcion'].astype(str).str.strip().str.lower() == desc_limpia)
        
        # 2. ¿Existe el código en esa marca? (Limpiamos la columna de códigos también)
        codigos_col = df_crapo[col_cod].astype(str).str.split('.').str[0].str.strip()
        filtro_codigo = codigos_col == cod_buscado

        if filtro_exacto.any():
            # CASO A: El auto ya está. Actualizamos esa fila.
            idx = df_crapo.index[filtro_exacto][0]
            df_crapo.at[idx, col_cod] = codigo
            df_crapo.at[idx, col_pre] = precio
            msg = f"✅ Datos actualizados: {vehiculo} ({marca_limpia})"

        elif filtro_codigo.any():
            # CASO B: El código ya existe (Equivalencia). Unimos nombres.
            idx = df_crapo.index[filtro_codigo][0]
            v_actual = str(df_crapo.at[idx, 'Vehiculo'])
            if vehiculo_limpio not in v_actual.lower():
                df_crapo.at[idx, 'Vehiculo'] = f"{v_actual} / {vehiculo}"
            df_crapo.at[idx, col_pre] = precio
            msg = f"🔗 Equivalencia: {codigo} ahora también en {vehiculo}"

        else:
            # CASO C: Todo nuevo.
            nueva_fila = {col: "" for col in df_crapo.columns}
            nueva_fila["Vehiculo"] = vehiculo
            nueva_fila["Descripcion"] = descripcion
            nueva_fila[col_cod] = codigo
            nueva_fila[col_pre] = precio
            df_crapo = pd.concat([df_crapo, pd.DataFrame([nueva_fila])], ignore_index=True)
            msg = f"✨ Nuevo en catálogo: {vehiculo}"

        # 2. GUARDADO
        conn.update(spreadsheet=SHEET_URL, worksheet="Catalogo_Crapodinas", data=df_crapo)
        st.toast(msg, icon="⚙️")

    except Exception as e:
        st.error(f"Error en catálogo: {e}")
        # 3. Guardamos en el Excel
        conn.update(spreadsheet=SHEET_URL, worksheet="Catalogo_Crapodinas", data=df_crapo)
        st.toast(msg, icon="⚙️")

    except Exception as e:
        st.error(f"Error en el catálogo inteligente: {e}")
        # 4. Guardamos
        df_final = pd.concat([df_crapo, nueva_fila], ignore_index=True)
        conn.update(spreadsheet=SHEET_URL, worksheet="Catalogo_Crapodinas", data=df_final)
        st.toast(f"✅ Nueva Crapodina guardada: {codigo}", icon="⚙️")
    except Exception as e:
        st.error(f"Error al actualizar catálogo de crapodinas: {e}")

def guardar_en_google(categoria, cliente, vehiculo, detalle, monto, costo, proveedor, cod_kit, cod_crap, f_pago, e_cliente, e_prov, m_forros, c_forros, costo_f, ganancia):
    # Ajuste horario Argentina
    fecha_hoy = (datetime.now() - timedelta(hours=3)).strftime("%d/%m/%Y %H:%M")
    
    # TUS COLUMNAS EXACTAS
    columnas = [
        "Fecha", "Categoría", "Cliente", "Vehículo", "Detalle", 
        "Venta $", "Compra $", "Proveedor", "Código", "Cod_Crapodina", 
        "Forma_de_pago", "Estado_Cobro", "Estado_Pago_Prov", 
        "Marca_Forros", "Cod_Forros", "Costo_Forros", "Ganancia"
    ]
    
    try:
        # Leemos la hoja
        df_existente = conn.read(spreadsheet=SHEET_URL, worksheet="Ventas", ttl=10)
    except Exception as e:
        st.error(f"Error al leer hoja Ventas: {e}")
        st.stop()
    
    # ACÁ ESTABA EL ERROR (Línea 100):
    # Antes decía 'codigo', ahora dice 'cod_kit, cod_crap' para llenar las dos columnas
    nuevo_reg = pd.DataFrame([[fecha_hoy, categoria, cliente, vehiculo, detalle, monto, costo, proveedor, cod_kit, cod_crap, f_pago, e_cliente, e_prov, m_forros, c_forros, costo_f, ganancia]], columns=columnas)
    
    # Guardamos
    df_actualizado = pd.concat([df_existente, nuevo_reg], ignore_index=True)
    conn.update(spreadsheet=SHEET_URL, worksheet="Ventas", data=df_actualizado)
# 2. PANEL DE CARGA
st.sidebar.header("⚙️ Configuración")

# --- INICIALIZACIÓN DE VARIABLES (Anti-Errores) ---
# Esto evita que la App explote si falta algún dato
m_kit = ""
m_forros = ""
forros_codigo = ""
forros_costo = 0
crap_codigo = ""
crap_costo = 0

# Selector de Tipo de Trabajo
tipo_item = st.sidebar.selectbox("Tipo de Trabajo:", 
                                ["Embrague Nuevo (Venta)", 
                                 "Reparación de Embrague", 
                                 "Kit de Distribución",
                                 "Otro"])


if "Nuevo" in tipo_item:
    cat_f, icono, incl_rectif = "Venta", "⚙️", True
    # --- Selector de Marca (NUEVO) ---
    lista_marcas = ["LUK", "SACHS", "VALEO", "PHC_VALEO", "ORIGINAL", "OTRA"]
    m_kit = st.sidebar.selectbox("Marca del Kit:", lista_marcas)
    sugerencia = f"KIT nuevo marca *{m_kit}*"
elif "Reparación" in tipo_item:
        cat_f, icono, incl_rectif = "Reparación", "🔧", False
        m_crap = st.sidebar.multiselect("Marcas de Crapodina:", ["Luk", "Skf", "Ina", "Dbh", "The"], default=["Luk", "Skf"])
        
        # --- CAMPOS DE COSTO INTERNO (NUEVO) ---
        crap_codigo = st.sidebar.text_input("Código de Crapodina:", "")
        crap_costo = st.sidebar.number_input("Costo de Crapodina ($):", min_value=0, value=0)
        # Esto te va a permitir elegir antes de guardar
        tipo_crap = st.sidebar.selectbox("⚙️ Tipo de Crapodina:", ["Hidráulica", "Mecánica"])

        # --- DATOS DE LOS FORROS ---
        m_forros = st.sidebar.selectbox("Marca de Forros:", ["IAR", "Fras-le", "Termolite", "Otro"])
        forros_codigo = st.sidebar.text_input("Código de Forros:", "")
        forros_costo = st.sidebar.number_input("Costo de Forros ($):", min_value=0, value=0)
    
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
#f_pago_input = st.sidebar.selectbox("Forma de Pago Realizada:", 
                                   #["Efectivo (Contado)", "Transferencia", "Tarjeta BNA - 1 Pago", "Tarjeta BNA - 3 Cuotas", "Tarjeta BNA - 6 Cuotas", "Combinado"])

# 1. ESTO ES NUEVO (Solo para el Excel, cortito)
detalle_excel = st.sidebar.text_input("📝 Detalle para Excel:", value="Reparación completa")

# 2. ESTO ES LO DE SIEMPRE (Para que el WhatsApp siga saliendo largo y vendedor)
detalle_final = st.sidebar.text_area("💬 Detalle en WhatsApp:", value=sugerencia)

st.sidebar.divider()
st.sidebar.write("📸 **Uso Interno**")

# --- LÓGICA DE COSTOS Y CÓDIGOS ---
if cat_f == "Reparación":
    # Si es reparación, toma los datos de arriba
    codigo_manual = crap_codigo
    precio_compra = crap_costo + forros_costo
    st.sidebar.info(f"💰 Costo Materiales: ${precio_compra:,.0f}")
else:
    # Si es venta, te pide los datos
    codigo_manual = st.sidebar.text_input("Código de repuesto:", "")
    precio_compra = st.sidebar.number_input("Precio de COMPRA ($):", min_value=0, value=0)

# --- LA CÁMARA (Siempre visible) ---
foto_repuesto = st.sidebar.file_uploader("📷 Sacar foto a la caja/repuesto", type=["jpg", "png", "jpeg"])
if foto_repuesto:
    st.sidebar.image(foto_repuesto, caption="Vista previa", use_container_width=True)

# --- GANANCIA EN PANTALLA (ESTO ES LO NUEVO QUE TE FALTA) ---
if monto_limpio > 0:
    ganancia = monto_limpio - precio_compra
    st.sidebar.metric("Ganancia Estimada", f"$ {ganancia:,.0f}")
else:
    ganancia = 0
proveedor_input = st.sidebar.text_input("Proveedor:", "icepar")
# --- SECCIÓN: ESTADOS DE PAGO (NUEVO) ---
st.sidebar.divider()
st.sidebar.subheader("💰 Estado de la Operación")
        
estado_cliente = st.sidebar.selectbox(
    "Estado del Cliente:", 
    ["Pagado", "Debe", "Seña"],
    index=0
)
                
# Si marca Pagado, se activa el menú de "Cómo pagó"
f_pago_input = "N/A" # Valor por defecto si debe
if estado_cliente == "Pagado":
    lista_pagos = [
        "Efectivo", "Transferencia", "Débito", 
        "BNA - 1 Pago", "BNA - 3 Cuotas", "BNA - 6 Cuotas",
        "Getnet - 1 Pago", "Getnet - 3 Cuotas", "Getnet - 6 Cuotas", "Getnet - 9 Cuotas", "Getnet - 12 Cuotas",
        "Combinado", "Otro"
    ]
    f_pago_input = st.sidebar.selectbox("¿Cómo pagó el cliente?:", lista_pagos)
        
estado_p_prov = st.sidebar.selectbox(
    "Estado al Proveedor:", 
        ["Pagado", "Cuenta Corriente", "N/A"],
        index=0
)

# --- LÓGICA PARA SEPARAR CÓDIGOS (ESTO FALTABA) ---
if cat_f == "Reparación":
    cod_kit_final = ""            # Si es reparación, la columna Kit queda vacía
    cod_crap_final = crap_codigo  # Y usamos el código de la Crapodina
else:
    cod_kit_final = codigo_manual # Si es venta, usamos el código del Kit
    cod_crap_final = ""           # Y la columna Crapodina queda vacía

if st.sidebar.button("💾 GUARDAR VENTA"):
    # 1. Guarda la venta normal (lo que ya hacíamos)
    guardar_en_google(cat_f, cliente_input, vehiculo_input, detalle_excel, monto_limpio, precio_compra, proveedor_input, cod_kit_final, cod_crap_final, f_pago_input, estado_cliente, estado_p_prov, m_forros, forros_codigo, forros_costo, ganancia)
    
    # 2. NUEVO: Si hay código de Kit, lo guarda en el catálogo de Kits
    if cod_kit_final:
        actualizar_catalogo_kits(vehiculo_input, cod_kit_final, monto_limpio, m_kit if 'm_kit' in locals() else "OTRA")
    
    # 3. ACTUALIZADO: Guarda en Catálogo de Crapodinas con Marca y Vehículo
    if cod_crap_final:
        # Agarramos la marca del multiselect de WhatsApp
        marca_elegida = m_crap[0] if m_crap else "OTRA"
        # Le mandamos los 5 datos: Vehiculo, Descrip, Codigo, Precio y Marca
        # Ahora usamos 'tipo_crap' para que guarde lo que vos elegiste (Mecánica o Hidráulica)
        actualizar_catalogo_crapodinas(vehiculo_input, f"Crapodina {tipo_crap}", cod_crap_final, crap_costo, marca_elegida)

    st.sidebar.success(f"¡Venta de $ {monto_limpio:,.0f} guardada y catálogos actualizados!")
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





# ==========================================
# 🔍 SECCIÓN: BUSCADOR DE CATÁLOGO
# ==========================================
st.divider() # Línea separadora
st.header("🔍 Consultar Catálogo")

# 1. Elegir qué buscar
tipo_busqueda = st.radio("¿Qué estás buscando?", ["Embragues (Kits)", "Crapodinas", "Distribución"], horizontal=True)

# 2. La Caja de Búsqueda
busqueda = st.text_input("✍️ Escribí Modelo de Auto o Código (Ej: 'Gol', '620 3000', 'Ranger'):")

# 3. Lógica de Búsqueda
if busqueda:
    st.caption(f"Resultados para: '{busqueda}'")
    
    # Buscamos en KITS
    if tipo_busqueda == "Embragues (Kits)":
        # Filtro mágico: Busca lo que escribiste en CUALQUIER columna
        mask = df_kits.astype(str).apply(lambda x: x.str.contains(busqueda, case=False, na=False)).any(axis=1)
        resultados = df_kits[mask]
        
        if not resultados.empty:
            st.dataframe(resultados, hide_index=True)
        else:
            st.info("No encontré kits con ese dato. ¿Probaste otra palabra?")

    # Buscamos en CRAPODINAS
    elif tipo_busqueda == "Crapodinas":
        mask = df_crapo.astype(str).apply(lambda x: x.str.contains(busqueda, case=False, na=False)).any(axis=1)
        resultados = df_crapo[mask]
        
        if not resultados.empty:
            st.dataframe(resultados, hide_index=True)
        else:
            st.info("No encontré crapodinas así.")

    # Buscamos en DISTRIBUCIÓN
    elif tipo_busqueda == "Distribución":
        mask = df_distri.astype(str).apply(lambda x: x.str.contains(busqueda, case=False, na=False)).any(axis=1)
        resultados = df_distri[mask]
        
        if not resultados.empty:
            st.dataframe(resultados, hide_index=True)
        else:
            st.info("Nada en Distribución todavía.")


















