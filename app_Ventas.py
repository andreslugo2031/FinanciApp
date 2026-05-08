import streamlit as st
import pandas as pd
import os
import urllib.parse
from PIL import Image

# Configuración de página
st.set_page_config(page_title="Admin Catálogo Tito", layout="wide")

# --- DISEÑO ---
st.markdown("""
    <style>
    .stApp { background-color: #f1f5f9; }
    .product-card {
        background-color: white; border-radius: 20px; padding: 20px;
        margin-bottom: 25px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        text-align: center; min-height: 550px; display: flex;
        flex-direction: column; justify-content: space-between;
    }
    .price-tag { font-size: 1.9rem; font-weight: 800; color: #1e40af; margin: 15px 0; }
    .ws-button {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        color: white !important; padding: 14px 25px; border-radius: 50px;
        text-decoration: none; font-weight: bold; display: inline-block; width: 90%;
    }
    </style>
    """, unsafe_allow_html=True)

TELEFONO = "584121877291" 
EXCEL_FILE = "COSTOS (4).xlsx"
FOTOS_DIR = "assets/productos/"

# Crear carpeta de fotos si no existe
if not os.path.exists(FOTOS_DIR):
    os.makedirs(FOTOS_DIR)

@st.cache_data
def cargar_datos():
    try:
        df = pd.read_excel(EXCEL_FILE)
        df = df.dropna(subset=[df.columns[1]]) 
        return df
    except:
        return pd.DataFrame()

df = cargar_datos()

# --- PANEL DE SUBIDA (SIDEBAR) ---
st.sidebar.title("🛠 Panel de Control")
with st.sidebar.expander("📸 Subir Foto de Producto"):
    if not df.empty:
        # Lista de productos para seleccionar
        nombres_productos = df[df.columns[1]].unique().tolist()
        producto_sel = st.selectbox("Selecciona el producto:", nombres_productos)
        
        # Obtener la marca para el nombre del archivo
        fila = df[df[df.columns[1]] == producto_sel].iloc[0]
        marca_sel = str(fila.iloc[2]).strip() if pd.notna(fila.iloc[2]) else ""
        
        archivo_foto = st.file_uploader("Elige la imagen", type=['jpg', 'jpeg', 'png'])
        
        if st.button("Guardar Foto"):
            if archivo_foto is not None:
                # Crear el nombre del archivo igual a como lo busca el catálogo
                nombre_archivo = f"{producto_sel}_{marca_sel}".replace(" ", "_") + ".jpg"
                ruta_final = os.path.join(FOTOS_DIR, nombre_archivo)
                
                # Procesar y guardar
                img = Image.open(archivo_foto)
                img = img.convert("RGB") # Asegurar compatibilidad
                img.save(ruta_final, "JPEG")
                
                st.success(f"¡Foto de {producto_sel} guardada con éxito!")
                st.balloons()
            else:
                st.error("Por favor, selecciona una imagen primero.")

# --- CUERPO DEL CATÁLOGO ---
if not df.empty:
    st.title("💎 Catálogo Exclusivo Tito")
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        search = st.text_input("🔍 ¿Qué buscas hoy?", placeholder="Ej: Nevera...").upper()

    col_idx_prod = 1
    col_idx_marca = 2
    col_idx_espec = 3
    col_idx_precio = 5

    if search:
        mask = df.astype(str).apply(lambda x: x.str.upper().str.contains(search)).any(axis=1)
        df = df[mask]

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
            
            if os.path.exists(foto_path):
                st.image(foto_path, use_container_width=True)
            else:
                st.image(f"https://via.placeholder.com/400x300/f1f5f9/64748b?text={id_foto}", use_container_width=True)

            st.markdown(f"""
                <div>
                    <h3 style="color:#0f172a; margin: 10px 0; font-size: 1.4rem;">{p_nombre}</h3>
                    <p style="color:#64748b; font-weight: 600;">Marca: {p_marca}</p>
                    <p style="color:#475569; font-size: 0.9rem; height: 45px; overflow: hidden;">{p_espec}</p>
                    <div class="price-tag">${p_precio}</div>
                </div>
            """, unsafe_allow_html=True)
            
            mensaje = f"¡Hola Tito! 👋 Vi esto en tu catálogo:\n*Producto:* {p_nombre}\n*Precio:* ${p_precio}"
            link_ws = f"https://wa.me/{TELEFONO}?text={urllib.parse.quote(mensaje)}"
            st.markdown(f'<a href="{link_ws}" target="_blank" class="ws-button">Consultar Ahora</a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
