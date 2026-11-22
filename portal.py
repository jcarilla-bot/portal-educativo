
import base64
from pathlib import Path
import streamlit as st
from laboratorio import mostrar_laboratorio
from simuladores.osmosis import mostrar_osmosis
from simuladores.ecosistemas import mostrar_ecosistemas

FOTO = Path(__file__).resolve().parent / "assets" / "jesus_carilla.jpg"

# CONFIGURACIÓN GENERAL
st.set_page_config(
    page_title="Portal Educativo de Jesús Carilla",
    page_icon=str(FOTO),
    layout="wide"
)

URL_PROFESOR = "https://profesor-virtual.streamlit.app/"

def abrir_simuladores():
    st.session_state["portal_pagina"] = "🧪 Simuladores científicos"


def abrir_matematicas():
    st.session_state["portal_pagina"] = "📐 Matemáticas"


def abrir_laboratorio():
    st.session_state["portal_pagina"] = "🔬 Laboratorio virtual"


# MENÚ LATERAL
st.sidebar.image(str(FOTO), width=60)
st.sidebar.title("Portal Educativo de Jesús Carilla")

pagina = st.sidebar.radio(
    "Selecciona una sección:",
    [
        "🏠 Inicio",
        "🤖 Profesor Virtual",
        "📐 Matemáticas",
        "🧪 Simuladores científicos",
        "🔬 Laboratorio virtual"
    ],
    key="portal_pagina"
)

st.sidebar.divider()
st.sidebar.caption("ESO y Bachillerato")

# PÁGINA DE INICIO
if pagina == "🏠 Inicio":

    foto_base64 = base64.b64encode(FOTO.read_bytes()).decode("ascii")
    st.markdown(
        '<div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">'
        f'<img src="data:image/jpeg;base64,{foto_base64}" alt="Jesús Carilla" '
        'style="width:60px;height:60px;object-fit:cover;flex-shrink:0;border-radius:6px">'
        '<h1 style="margin:0;padding:0;line-height:1.2">Portal Educativo de Jesús Carilla</h1>'
        '</div>',
        unsafe_allow_html=True
    )
    st.subheader(
        "Ciencias, Matemáticas e Inteligencia Artificial"
    )

    st.write(
        "Bienvenido a un espacio de aprendizaje "
        "interactivo para ESO y Bachillerato."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("🤖 Profesor Virtual")
            st.write("Asistente de Biología y Geología.")
            st.link_button(
                "Acceder al Profesor Virtual",
                URL_PROFESOR,
                use_container_width=True
            )

        with st.container(border=True):
            st.subheader("🧪 Simuladores científicos")
            st.write("Ósmosis celular y dinámica de ecosistemas.")
            st.button(
                "Ir a simuladores",
                on_click=abrir_simuladores,
                use_container_width=True
            )

    with col2:
        with st.container(border=True):
            st.subheader("📐 Matemáticas")
            st.write("Factorización de polinomios y ecuaciones de segundo grado.")
            st.button(
                "Ir a Matemáticas",
                on_click=abrir_matematicas,
                use_container_width=True
            )

        with st.container(border=True):
            st.subheader("🔬 Laboratorio virtual")
            st.write("Compara células animales y vegetales e identifica sus estructuras.")
            st.button(
                "Ir al Laboratorio virtual",
                on_click=abrir_laboratorio,
                use_container_width=True
            )

# PROFESOR VIRTUAL
elif pagina == "🤖 Profesor Virtual":

    st.title("🤖 Profesor Virtual")

    st.write(
        "Asistente de inteligencia artificial "
        "especializado en Biología y Geología."
    )

    st.link_button(
        "🚀 Abrir Profesor Virtual",
        URL_PROFESOR
    )

# MATEMÁTICAS
elif pagina == "📐 Matemáticas":

    st.title("📐 Matemáticas")

    st.write("Elige una actividad para practicar álgebra.")

    with st.container(border=True):
        st.subheader("Factorización de polinomios")
        st.write("Actividad para trabajar la factorización de polinomios.")
        st.link_button(
            "Practicar factorización de polinomios",
            "https://factoriza-cuarto-eso-colob.artfulchair257.chatgpt.site/",
            use_container_width=True
        )

    with st.container(border=True):
        st.subheader("Ecuaciones de segundo grado")
        st.write("Actividad para trabajar la ecuación de segundo grado.")
        st.link_button(
            "Practicar ecuaciones de segundo grado",
            "https://app.astra-ai.co/es-ES/share/a/BXnWor1wibl4w_7A",
            use_container_width=True
        )

# SIMULADORES
elif pagina == "🧪 Simuladores científicos":

    st.title("🧪 Simuladores científicos")

    simulador = st.selectbox(
        "Selecciona un simulador:",
        [
            "Ósmosis celular",
            "Genética mendeliana (próximamente)",
            "Actividad enzimática (próximamente)",
            "Dinámica de ecosistemas"
        ]
    )

    if simulador == "Ósmosis celular":
        mostrar_osmosis()
    elif simulador == "Dinámica de ecosistemas":
        mostrar_ecosistemas()
    else:
        st.info("Este simulador está en desarrollo.")
        
# LABORATORIO
elif pagina == "🔬 Laboratorio virtual":

    mostrar_laboratorio()

st.divider()
st.caption("Portal Educativo de Jesús Carilla | ESO y Bachillerato")
