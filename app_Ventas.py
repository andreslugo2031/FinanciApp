import streamlit as st
import pandas as pd
import os
import urllib.parse

# Configuración de página
st.set_page_config(page_title="Catálogo Tito", layout="wide")

TELEFONO = "584121877291"
EXCEL_FILE = "COSTOS (4).xlsx"
FOTOS_DIR = "assets/productos/"

# Asegurar que la carpeta de fotos exista para que no de error al guardar
if not os.path.exists(FOTOS_DIR):
    os.makedirs(FOTOS_DIR)

# --- ESTILO LIMPIO ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .product-card {
        background-color: white; 
        border-radius: 12px; 
        padding: 15px;
        margin-bottom: 20px; 
        border: 1px solid #e2e8f0;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    .price-tag { font-size: 1.4rem; font-weight: bold; color: #1e40af; margin: 10px 0; }
    .ws-button {
        background-color: #25D366; color: white !important; padding: 10px;
        border-radius: 8px; text-decoration: none; font-weight: bold; display: block; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


def cargar_datos():
    try:
        df = pd.read_excel(EXCEL_FILE)
        # Asegurarnos de que exista la columna 'FOTO' en el DataFrame si no existe en el Excel
        if 'FOTO' not in df.columns:
            df['FOTO'] = None
        return df
    except Exception as e:
        st.error(f"Error al leer el archivo Excel: {e}")
        return pd.DataFrame()

# Cargamos los datos iniciales
df_original = cargar_datos()

# Filtrados para la visualización del catálogo (sin alterar el archivo para guardar)
if not df_original.empty:
    # Limpieza visual para el catálogo
    df_catalogo = df_original.dropna(subset=[df_original.columns[1]]).copy()
    df_catalogo = df_catalogo[df_catalogo.iloc[:, 5].notna() & (df_catalogo.iloc[:, 5] != 0)]
    df_catalogo = df_catalogo.drop_duplicates(subset=[df_catalogo.columns[1], df_catalogo.columns[2]])
    
    st.title("🛍️ Catálogo Tito")

    # ==========================================
    # 🛠️ PANEL DE ADMINISTRACIÓN (ZONA SUBIR FOTOS)
    # ==========================================
    with st.sidebar.expander("⚙️ Panel de Administrador (Subir Fotos)", expanded=False):
        st.write("Selecciona un producto para asignarle o cambiarle la foto:")
        
        # Lista de productos disponibles para asociar foto
        lista_productos = df_catalogo.apply(lambda r: f"{r.iloc[1]} ({r.iloc[2]})" if pd.notna(r.iloc[2]) else f"{r.iloc[1]}", axis=1).tolist()
        producto_seleccionado = st.selectbox("Buscar Producto", lista_productos)
        
        # Obtener el índice real en el dataframe original
        idx_match = df_catalogo.index[lista_productos.index(producto_seleccionado)]
        p_nombre_sel = df_original.loc[idx_match].iloc[1]
        p_marca_sel = df_original.loc[idx_match].iloc[2] if pd.notna(df_original.loc[idx_match].iloc[2]) else ""
        
        # Cargador de archivos de Streamlit
        foto_subida = st.file_uploader("Elige una imagen (JPG/PNG)", type=["jpg", "jpeg", "png"])
        
        if foto_subida is not None:
            # Creamos un nombre de archivo limpio basado en el producto
            ext = os.path.splitext(foto_subida.name)[1]
            nombre_foto_limpio = f"{p_nombre_sel}_{p_marca_sel}".replace(" ", "_").replace("/", "-") + ext
            ruta_guardado = os.path.join(FOTOS_DIR, nombre_foto_limpio)
            
            # Guardar el archivo físicamente en la carpeta assets
            with open(ruta_guardado, "wb") as f:
                f.write(foto_subida.getbuffer())
                
            # Actualizar la celda correspondiente en la columna 'FOTO' del Excel original
            df_original.at[idx_match, 'FOTO'] = ruta_guardado
            
            try:
                # Guardar los cambios directamente en el archivo Excel original
                df_original.to_excel(EXCEL_FILE, index=False)
                st.success(f"¡Foto guardada y vinculada a {p_nombre_sel} con éxito!")
                # Forzar recarga de la página para mostrar los cambios
                st.rerun()
            except Exception as e:
                st.error(f"No se pudo actualizar el Excel. Asegúrate de que esté cerrado. Error: {e}")

    # ==========================================
    # 🔍 BUSCADOR Y MOSTRAR CATÁLOGO
    # ==========================================
    search = st.text_input("🔍 Buscar producto...", placeholder="Escribe aquí...").upper()

    if search:
        mask = df_catalogo.astype(str).apply(lambda x: x.str.upper().str.contains(search)).any(axis=1)
        df_catalogo = df_catalogo[mask]

    cols = st.columns(2)
    
    for i, (original_idx, row) in enumerate(df_catalogo.iterrows()):
        p_nombre = str(row.iloc[1]).strip()
        p_marca = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ""
        p_espec = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
        p_precio = row.iloc[5]
        
        # Leer la ruta de la foto guardada en el Excel
        p_foto = row['FOTO'] if pd.notna(row['FOTO']) else None

        mensaje_ws = urllib.parse.quote(f"Hola Tito, me interesa el producto: {p_nombre} ({p_marca})")
        link_ws = f"https://wa.me/{TELEFONO}?text={mensaje_ws}"

        with cols[i % 2]:
            with st.container(border=True):
                # Validar si el archivo de la foto existe físicamente
                if p_foto and os.path.exists(str(p_foto)):
                    st.image(str(p_foto), use_container_width=True)
                else:
                    st.markdown('<div style="background:#f1f5f9;padding:40px;border-radius:10px;color:#94a3b8;text-align:center;">Sin Foto</div>', unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="product-card" style="border:none; padding:0; margin:0;">
                        <div style="margin-top:10px">
                            <h4 style="margin:0; color:#1e293b; font-size:1.1rem;">{p_nombre}</h4>
                            <p style="color:#64748b; font-size:0.8rem; margin:5px 0;">{p_marca} | {p_espec}</p>
                            <div class="price-tag">${p_precio:,.2f}</div>
                        </div>
                        <a href="{link_ws}" target="_blank" class="ws-button">Consultar</a>
                    </div>
                """, unsafe_allow_html=True)
else:
    st.error("Error al cargar el catálogo o el archivo Excel está vacío.")
