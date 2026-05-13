import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Mi Catálogo Pro", page_icon="🛍️", layout="wide")

# Estilos personalizados para el Modo Oscuro y Botones
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .product-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #464b5d;
        margin-bottom: 20px;
    }
    .whatsapp-button {
        background-color: #25D366;
        color: white !important;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛍️ Catálogo de Productos")
st.write("Bienvenido a la versión mejorada de tu tienda.")

# --- DATOS DE PRODUCTOS ---
# Tip: Si usas una URL de imagen de internet, no se borrará nunca.
productos = [
    {
        "nombre": "Producto Ejemplo 1",
        "precio": "25.00",
        "imagen": "https://via.placeholder.com/300", # Cambia por ruta local o URL real
        "descripcion": "Descripción detallada del producto."
    },
    {
        "nombre": "Producto Ejemplo 2",
        "precio": "40.00",
        "imagen": "https://via.placeholder.com/300",
        "descripcion": "Otra descripción interesante."
    }
]

# --- RENDERIZADO DEL CATÁLOGO ---
cols = st.columns(2) # Divide en 2 columnas

for i, producto in enumerate(productos):
    with cols[i % 2]:
        st.markdown(f"""
            <div class="product-card">
                <img src="{producto['imagen']}" style="width:100%; border-radius:5px;">
                <h3>{producto['nombre']}</h3>
                <p>{producto['descripcion']}</p>
                <p style="font-size: 20px; font-weight: bold;">${producto['precio']}</p>
                <a href="https://wa.me/58411877291-+?text=Hola,%20me%20interesa%20el%20producto:%20{producto['nombre']}" 
                   target="_blank" class="whatsapp-button">
                   Chat en WhatsApp 💬
                </a>
            </div>
            """, unsafe_allow_html=True)
