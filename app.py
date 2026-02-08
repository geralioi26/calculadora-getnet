import streamlit as st
import urllib.parse

# 1. IDENTIDAD Y ESTILO
st.set_page_config(page_title="Embragues Rosario - Calculadora", page_icon="⚙️")
st.title("⚙️ Embragues Rosario")
st.markdown("Crespo 4117, Rosario | **IIBB: EXENTO**")

# 2. ENTRADA DE DATOS (Mantenemos lo que ya funcionaba)
st.sidebar.header("🔧 Configuración del Kit")
monto_limpio = st.sidebar.number_input("Monto LIMPIO para vos ($):", min_value=0, value=210000, step=5000)
tipo_kit = st.sidebar.selectbox("Tipo de Kit:", ["Nuevo", "Reparado Completo", "Reparado + Crapodina"])
marca = st.sidebar.text_input("Marca / Vehículo:", "Sachs")

# 3. SELECTORES DE BANCO Y MEDIO (Los nuevos "goles")
st.markdown("### 💳 Configuración de Cobro")
col_b, col_m = st.columns(2)
with col_b:
    banco = st.radio("Sistema:", ["BNA (Más Pagos)", "Getnet (Santander)"], horizontal=True)
with col_m:
    metodo = st.radio("Medio de pago:", ["Link de Pago", "POS Físico / QR"], horizontal=True)

# 4. LÓGICA DE PORCENTAJES (Basado en tus fotos y IIBB Exento)
# BNA: 3.00% + IVA (Link) / 2.30% + IVA (POS)
if banco == "BNA (Más Pagos)":
    if metodo == "Link de Pago":
        f1, f3, f6 = 1.042, 1.12, 1.20  # Recargos para Link
    else:
        f1, f3, f6 = 1.033, 1.10, 1.18  # Recargos para POS (Más barato)
# Getnet: Tasas estándar
else:
    if metodo == "Link de Pago":
        f1, f3, f6 = 1.045, 1.16, 1.29
    else:
        f1, f3, f6 = 1.038, 1.14, 1.25

# 5. CÁLCULOS
total_1p = monto_limpio * f1
total_3p = monto_limpio * f3
total_6p = monto_limpio * f6

# 6. PANTALLA DE RESULTADOS
st.divider()
# Marcamos en negrita el precio de efectivo como pediste
st.success(f"### **EFECTIVO / TRANSFERENCIA: ${monto_limpio:,.0f}**")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("1 PAGO", f"${total_1p:,.0f}")
with c2:
    st.metric("3 CUOTAS TOTAL", f"${total_3p:,.0f}")
    st.caption(f"3 x ${total_3p/3:,.2f}")
with col3:
    st.metric("6 CUOTAS TOTAL", f"${total_6p:,.0f}")
    st.caption(f"6 x ${total_6p/6:,.2f}")

# 7. GENERADOR DE WHATSAPP (Con la frase exacta del volante)
frase_volante = "Incluye rectificación y balanceo de volante."

mensaje = (
    f"🚗 *EMBRAGUES ROSARIO*\n"
    f"Presupuesto para Kit {tipo_kit} marca {marca}.\n"
    f"{frase_volante}\n\n"
    f"💰 **EFECTIVO / TRANSFERENCIA: ${monto_limpio:,.0f}**\n\n"
    f"💳 *OPCIONES CON {metodo.upper()} ({banco}):*\n"
    f"✅ 1 pago: *${total_1p:,.0f}*\n"
    f"✅ 3 cuotas: *${total_3p/3:,.2f}* (Total: *${total_3p:,.0f}*)\n"
    f"✅ 6 cuotas: *${total_6p/6:,.2f}* (Total: *${total_6p:,.0f}*)\n\n"
    f"📍 Crespo 4117, Rosario\n"
    f"📸 @embraguesrosario\n"
    f"¡Te esperamos! ✨"
)

mensaje_codificado = urllib.parse.quote(mensaje)
link_wa = f"https://wa.me/?text={mensaje_codificado}"

st.divider()
st.link_button("🟢 ENVIAR POR WHATSAPP", link_wa)
