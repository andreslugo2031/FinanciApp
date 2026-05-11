import streamlit as st
import pandas as pd
import os
import urllib.parse

# Configuración de página
st.set_page_config(page_title="Catálogo Tito", layout="wide")

# --- ESTILO LIMPIO Y COMPACTO ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .product-card {
        background-color: white; border-radius: 12px; padding: 15px;
        margin-bottom: 20px; border: 1px solid #e2e8f0;
        text-align: center; height: 100%; display: flex;
        flex-direction: column; justify-content: space-between;
    }
    .price-tag { font-size: 1.5rem; font-weight: bold; color: #1e40af; margin: 10px 0; }
    .ws-button {
        background-color: #25D366; color: white !important; padding: 10px;
        border-radius: 8px; text-decoration: none; font-weight: bold; display: block;
    }
    /* Arregla espacios en blanco en móvil */
    [data-testid="stVerticalBlock"] > div { padding: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

TELEFONO = "584121877291"
EXCEL_FILE = "COSTOS (4).xlsx"
FOTOS_DIR = "assets/productos/"

@st.cache_data
def cargar_datos():
    try:
        df = pd.read_excel(EXCEL_FILE)
        # 1. Quitar filas donde el nombre esté vacío
        df = df.dropna(subset=[df.columns[1]])
        # 2. Quitar filas donde el precio sea 0 o vacío (Evita el $nan)
        df = df[df.iloc[:, 5].notna() & (df.iloc[:, 5] != 0)]
        # 3. ELIMINAR DUPLICADOS (Basado en nombre y marca)
        df = df.drop_duplicates(subset=[df.columns[1], df.columns[2]])
        return df
    except:
        return pd.DataFrame()

df = cargar_datos()

if not df.empty:
    st.title("🛍️ Catálogo Tito")
    
    search = st.text_input("🔍 Buscar producto...", placeholder="Escribe aquí...").upper()

    if search:
        mask = df.astype(str).apply(lambda x: x.str.upper().str.contains(search)).any(axis=1)
        df = df[mask]

    # Grid de 2 columnas para que en móvil no se vea eterno
    cols = st.columns(2) if st.columns(1) else st.columns(2)
    
    # Usamos un contenedor de columnas dinámico
    for i, (_, row) in enumerate(df.iterrows()):
        p_nombre = str(row.iloc[1]).strip()
        p_marca = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ""
        p_espec = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
        p_precio = row.iloc[5]

        id_foto = f"{p_nombre}_{p_marca}".replace(" ", "_")
        foto_path = os.path.join(FOTOS_DIR, f"{id_foto}.jpg")

        with cols[i % 2]:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            
            # Imagen con tamaño controlado
            if os.path.exists(foto_path):
                st.image(foto_path, use_container_width=True)
            else:
                # Placeholder minimalista si no hay foto
                st.markdown(f'<div style="background:#f1f5f9;padding:40px;border-radius:10px;color:#94a3b8">Sin Foto</div>', unsafe_allow_html=True)

            st.markdown(f"""
                <div style="margin-top:10px">
                    <h4 style="margin:0; color:#1e293b;">{p_nombre}</h4>
                    <p style="color:#64748b; font-size:0.8rem; margin:5px 0;">{p_marca} | {p_espec}</p>
                    <div class="price-tag">${p_precio}</div>
                </div>
            """, unsafe_allow_html=True)
            
            link_ws = f"https://wa.me/{TELEFONO}?text=Hola Tito, me interesa: {p_nombre}"
            st.markdown(f'<a href="{link_ws}" class="ws-button">Consultar</a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Revisa tu archivo Excel: parece que hay precios vacíos o nombres repetidos.")
