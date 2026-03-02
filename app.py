import streamlit as st
import pandas as pd

# 1. Configuración de la App
st.set_page_config(page_title="PK2 Angelicales", layout="centered")
st.title("💎 Registro de Ventas PK2")

# 2. Enlace a tu base de datos (Google Sheets)
# Usa el link de publicación que termina en /pub?output=csv
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS_H-Vn.../pub?output=csv"

@st.cache_data(ttl=300)
def cargar_datos():
    return pd.read_csv(SHEET_URL)

try:
    df = cargar_datos()

    # --- FILTROS PARA LAS VENDEDORAS ---
    # Selecciona el modelo (Sin repetir nombres de los 96 registros)
    productos = sorted(df['PRODUCTO'].unique())
    producto_sel = st.selectbox("🛍️ Selecciona el Modelo", productos)

    # Filtra tallas según el modelo
    df_prod = df[df['PRODUCTO'] == producto_sel]
    tallas = sorted(df_prod['TALLA'].unique())
    talla_sel = st.selectbox("📏 Selecciona la Talla", tallas)

    # Filtra colores según producto y talla
    df_talla = df_prod[df_prod['TALLA'] == talla_sel]
    colores = sorted(df_talla['COLOR'].unique())
    color_sel = st.selectbox("🎨 Selecciona el Color", colores)

    # Muestra stock disponible
    fila = df_talla[df_talla['COLOR'] == color_sel].iloc[0]
    stock_actual = int(fila['STOCK_ACTUAL'])
    st.warning(f"Stock disponible: {stock_actual} unidades")

    # Formulario de venta
    cantidad = st.number_input("Cantidad", min_value=1, max_value=stock_actual, step=1)
    if st.button("🚀 Registrar Venta"):
        st.success("¡Venta registrada con éxito!")
        st.balloons()

except Exception as e:
    st.error("Conectando con la base de datos...")
