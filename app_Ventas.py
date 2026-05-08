import streamlit as st
import pandas as pd
import os
import urllib.parse

# Configuración de página
st.set_page_config(page_title="Catálogo Tito - Premium", layout="wide")

# --- DISEÑO UI MODERNO ---
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Títulos */
    h1 {
        color: #1e293b !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800 !important;
    }

    /* Card de Producto */
    .product-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #e2e8f0;
        text-align: center;
        min-height: 520px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    /* Efecto al pasar el mouse sobre la tarjeta */
    .product-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: #3b82f6;
    }

    /* Estilo de la imagen */
    .stImage img {
        border-radius: 10px;
    }

    /* Precio con relieve */
    .price-tag {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2563eb;
        margin: 10px 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
    }

    /* Botón de WhatsApp Estilo Moderno */
    .ws-button {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        color: white !important;
        padding: 12px 20px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        display: block;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3);
        transition: all 0.3s ease;
        border: none;
        margin-top: 15px;
    }

    .ws-button:hover {
        box-shadow: 0 6px 20px rgba(37, 211, 102, 0.5);
        transform: scale(1.02);
        color: white !important;
    }

    /* Buscador */
    .stTextInput input {
        border-radius: 10px !important;
        border: 1px solid #cbd5e1 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# CONFIGURACIÓN
TELEFONO = "585077657563"
EXCEL_FILE = "COSTOS (4).xlsx"
FOTOS_DIR = "assets/productos/"

@st.cache_data
def cargar_datos():
    try:
        df = pd.read_excel(EXCEL_FILE)
        df = df.dropna(subset=[df.columns[1]]) 
        return df
    except:
        return pd.DataFrame()

df = cargar_datos()

if not df.empty:
    st.title("🚀 Catálogo de Productos")
    st.write("Selecciona un producto para consultar por WhatsApp")

    # Buscador con estilo
    search = st.text_input("🔍 ¿Qué estás buscando hoy?", placeholder="Ej: Nevera, Congelador...").upper()

    col_idx_prod = 1
    col_idx_marca = 2
    col_idx_espec = 3
    col_idx_precio = 5

    if search:
        mask = df.astype(str).apply(lambda x: x.str.upper().str.contains(search)).any(axis=1)
        df = df[mask]

    # Grid de productos
    cols = st.columns(3)
    for i, (_, row) in enumerate(df.iterrows()):
        p_nombre = str(row.iloc[col_idx_prod]).strip()
        p_marca = str(row.iloc[col_idx_marca]).strip() if pd.notna(row.iloc[col_idx_marca]) else ""
        p_espec = str(row.iloc[col_idx_espec]).strip() if pd.notna(row.iloc[col_idx_espec]) else ""
        p_precio = row.iloc[col_idx_precio]

        id_foto = f"{p_nombre}_{p_marca}".replace(" ", "_")
        foto_path = os.path.join(FOTOS_DIR, f"{id_foto}.jpg")

        with cols[i % 3]:
            # Contenedor de la tarjeta
            st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
            
            # Imagen
            if os.path.exists(foto_path):
                st.image(foto_path, use_container_width=True)
            else:
                st.image(f"https://via.placeholder.com/400x300/f1f5f9/64748b?text={p_nombre}", use_container_width=True)

            # Información
            st.markdown(f"""
                <div style="padding-top:10px;">
                    <h3 style="color:#0f172a; margin-bottom:0;">{p_nombre}</h3>
                    <p style="color:#64748b; font-size:0.9rem;">Marca: {p_marca}</p>
                    <p style="color:#475569; font-size:0.85rem; height:40px; overflow:hidden;">{p_espec}</p>
                    <div class="price-tag">${p_precio}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Botón de WhatsApp
            mensaje = f"¡Hola Tito! Me interesa:\n*Producto:* {p_nombre}\n*Precio:* ${p_precio}"
            link_ws = f"https://wa.me/{TELEFONO}?text={urllib.parse.quote(mensaje)}"
            
            st.markdown(f'<a href="{link_ws}" target="_blank" class="ws-button">Consultar Precio</a>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("No se pudo cargar el archivo Excel. Revisa el nombre en GitHub.")
