import streamlit as st
import pandas as pd
import os
import urllib.parse

# Configuración de página
st.set_page_config(page_title="Catálogo Tito - Premium", layout="wide")

# --- DISEÑO UI MODERNO V2 ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f1f5f9;
    }
    
    h1 {
        color: #1e293b !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 30px;
    }

    .product-card {
        background-color: white;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid #e2e8f0;
        text-align: center;
        min-height: 550px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .product-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
        border-color: #2563eb;
    }

    .price-tag {
        font-size: 1.9rem;
        font-weight: 800;
        color: #1e40af;
        margin: 15px 0;
    }

    .ws-button {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        color: white !important;
        padding: 14px 25px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.4);
        transition: all 0.3s ease;
        width: 90%;
        margin: 0 auto;
    }

    .ws-button:hover {
        box-shadow: 0 8px 20px rgba(37, 211, 102, 0.6);
        transform: scale(1.05);
        color: white !important;
    }

    /* Estilo para el buscador */
    div[data-baseweb="input"] {
        border-radius: 15px !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# CONFIGURACIÓN CORREGIDA
TELEFONO = "584121877291" 
EXCEL_FILE = "COSTOS (4).xlsx"
FOTOS_DIR = "assets/productos/"

@st.cache_data
def cargar_datos():
    try:
        df = pd.read_excel(EXCEL_FILE)
        # Limpieza: quitamos filas donde el nombre del producto esté vacío
        df = df.dropna(subset=[df.columns[1]]) 
        return df
    except:
        return pd.DataFrame()

df = cargar_datos()

if not df.empty:
    st.title("💎 Catálogo Exclusivo Tito")
    
    # Buscador centrado
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        search = st.text_input("🔍 ¿Qué buscas hoy?", placeholder="Ej: Nevera, Peinadora...").upper()

    # Columnas del Excel (Posiciones)
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
            st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
            
            # Imagen con bordes redondeados
            if os.path.exists(foto_path):
                st.image(foto_path, use_container_width=True)
            else:
                st.image(f"https://via.placeholder.com/400x300/f1f5f9/64748b?text={p_nombre}", use_container_width=True)

            # Contenido de la tarjeta
            st.markdown(f"""
                <div>
                    <h3 style="color:#0f172a; margin: 10px 0 5px 0; font-size: 1.4rem;">{p_nombre}</h3>
                    <p style="color:#64748b; font-weight: 600; margin-bottom: 2px;">Marca: {p_marca}</p>
                    <p style="color:#475569; font-size: 0.9rem; line-height: 1.2; height: 45px; overflow: hidden;">{p_espec}</p>
                    <div class="price-tag">${p_precio}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Link de WhatsApp
            mensaje = f"¡Hola Tito! 👋 Vi esto en tu catálogo y me interesa:\n\n*Producto:* {p_nombre}\n*Precio:* ${p_precio}"
            link_ws = f"https://wa.me/{58412877291}?text={urllib.parse.quote(mensaje)}"
            
            st.markdown(f'<a href="{link_ws}" target="_blank" class="ws-button">Consultar Ahora</a>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("⚠️ Esperando conexión con el inventario o archivo Excel vacío.")
