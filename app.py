import streamlit as st
import pandas as pd

# 1. Configuración visual de la aplicación
st.set_page_config(page_title="PK2 Angelicales - Ventas", layout="centered")

st.title("💎 Registro de Ventas PK2")
st.markdown("---")

# 2. Conexión con tu Google Sheet
# Reemplaza 'TU_URL_AQUI' por el link de tu Sheet terminado en /export?format=csv
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS_H-Vn.../pub?output=csv"

@st.cache_data(ttl=600)
def cargar_datos():
    return pd.read_csv(SHEET_URL)

try:
    df = cargar_datos()

    # --- LÓGICA DE FILTROS INTELIGENTES ---

    # A. Selector de Producto (Elimina duplicados automáticamente)
    lista_productos = sorted(df['PRODUCTO'].unique())
    producto_seleccionado = st.selectbox("🛍️ Selecciona el Modelo", lista_productos)

    # B. Filtrar Tallas (Solo muestra lo que existe para ese modelo)
    df_producto = df[df['PRODUCTO'] == producto_seleccionado]
    lista_tallas = sorted(df_producto['TALLA'].unique())
    talla_seleccionada = st.selectbox("📏 Selecciona la Talla", lista_tallas)

    # C. Filtrar Colores (Solo lo que hay en ese modelo y esa talla)
    df_talla = df_producto[df_producto['TALLA'] == talla_seleccionada]
    lista_colores = sorted(df_talla['COLOR'].unique())
    color_seleccionado = st.selectbox("🎨 Selecciona el Color", lista_colores)

    # D. Mostrar Stock y Precio
    fila_final = df_talla[df_talla['COLOR'] == color_seleccionado].iloc[0]
    stock_actual = fila_final['STOCK_ACTUAL']
    precio_venta = fila_final['PRECIO VENTA']

    st.warning(f"Stock disponible: {stock_actual} unidades")
    st.info(f"Precio por unidad: S/ {precio_venta}")

    # --- REGISTRO DE VENTA ---
    
    cantidad = st.number_input("Cantidad a vender", min_value=1, max_value=int(stock_actual), step=1)
    vendedora = st.text_input("Nombre de la Vendedora")

    if st.button("🚀 Registrar Venta"):
        if vendedora:
            st.success(f"¡Venta de {cantidad} {producto_seleccionado} registrada!")
            st.balloons()
        else:
            st.error("Por favor, ingresa el nombre de la vendedora.")

except Exception as e:
    st.error("⚠️ Error: Asegúrate de que la URL de tu Google Sheet sea correcta y pública.")
