import streamlit as st
import pandas as pd
import os
import urllib.parse

st.set_page_config(page_title="Tito Inventory", layout="wide")

# CONFIGURACIÓN: Pon tu número aquí (Ej: 584121234567)
TELEFONO = "584121877291" 

# Estilo Terminal Retro
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    * { color: #00FF41 !important; font-family: 'Courier New', Courier, monospace !important; }
    .product-card { border: 1px solid #00FF41; padding: 15px; margin-bottom: 20px; background-color: #050505; border-radius: 4px; text-align: center; min-height: 500px; }
    .stButton>button { 
        border: 1px solid #00FF41 !important; 
        background-color: #000000 !important; 
        color: #00FF41 !important; 
        width: 100%; 
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #00FF41 !important;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

EXCEL_FILE = "COSTOS (4).xlsx"
FOTOS_DIR = "assets/productos/"

@st.cache_data
def cargar_datos():
    df = pd.read_excel(EXCEL_FILE)
    df = df.dropna(subset=[df.columns[1]]) 
    return df

try:
    df = cargar_datos()

    st.title(" ⧉ TERMINAL DE VENTAS - PUNTO FIJO")
    st.write(f"SISTEMA ONLINE | WHATSAPP CONFIGURADO: +{TELEFONO}")

    search = st.text_input("🔍 BUSCAR PRODUCTO (Ej: Nevera, Hyundai, Cocina):").upper()

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

        # Nombre de la foto
        id_foto = f"{p_nombre}_{p_marca}".replace(" ", "_")
        foto_path = os.path.join(FOTOS_DIR, f"{id_foto}.jpg")

        with cols[i % 3]:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            
            if os.path.exists(foto_path):
                st.image(foto_path, use_container_width=True)
            else:
                st.image(f"https://via.placeholder.com/300x200/000000/00FF41?text={id_foto}", use_container_width=True)

            st.subheader(p_nombre)
            st.write(f"MARCA: {p_marca}")
            st.write(f"INFO: {p_espec}")
            st.markdown(f"## ${p_precio}")
            
            # --- LÓGICA DEL BOTÓN DE WHATSAPP ---
            mensaje = f"Hola Tito! Me interesa este producto de tu catálogo:\n\n*Producto:* {p_nombre}\n*Marca:* {p_marca}\n*Precio:* ${p_precio}"
            msg_encoded = urllib.parse.quote(mensaje)
            link_ws = f"https://wa.me/{TELEFONO}?text={msg_encoded}"
            
            # Botón que actúa como link
            st.markdown(f'''<a href="{link_ws}" target="_blank" style="text-decoration: none;">
                            <button style="width: 100%; background-color: #000000; color: #00FF41; border: 1px solid #00FF41; padding: 10px; cursor: pointer; font-family: 'Courier New'; font-weight: bold;">
                            COMPRAR POR WHATSAPP
                            </button></a>''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"SISTEMA BLOQUEADO: {e}")