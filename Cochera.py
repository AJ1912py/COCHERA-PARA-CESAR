import streamlit as st
import os
from PIL import Image

# 1. CONFIGURACIÓN Y ESTADO INICIAL
st.set_page_config(page_title="Visualizador Cesar", page_icon="🏠", layout="wide")
PASSWORD_CORRECTA = "CesarM"

# Diccionario Global de Frases
frases = {
    "ConAlero": "Con este alero ganas un resguardo climático adicional.",
    "SinAlero": "Consigues pureza formal y fluidez espacial.",
    "Eficientes": "Líneas ortogonales que transmiten orden y estabilidad.",
    "Dinamicos": "Rompemos la monotonía con un carácter audaz.",
    "Ninguno": "La estructura desnuda celebra la honestidad de los materiales.",
    "Poco": "El equilibrio entre la funcionalidad y la estética.",
    "Mucho": "Un acabado integral que otorga identidad exclusiva.",
    "negro": "El negro aporta contraste rotundo y sofisticación.",
    "gris": "Tono industrial que ofrece versatilidad.",
    "rojo": "Terracota profundo que añade personalidad y calidez."
}

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if 'vista' not in st.session_state: st.session_state.vista = "Cam"
if 'color' not in st.session_state: st.session_state.color = "negro"
if 'ultima_frase' not in st.session_state: st.session_state.ultima_frase = "Prueba las combinaciones"

# --- FUNCIÓN PARA EL LOGO ---
def mostrar_logo():
    """Busca el logo y lo despliega"""
    logo_path = "COCHERA-PARA-CESAR/logo.png" 
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        # Si no hay imagen, un placeholder con el estilo de la marca
        st.markdown("<h1 style='color: #00FF00; text-align: center;'>CESAR</h1>", unsafe_allow_html=True)

# --- PANTALLA DE LOGIN ---
if not st.session_state.autenticado:
    st.markdown("<h2 style='text-align: center; color: #00FF00;'>Acceso Privado</h2>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1, 1])
    with col_login:
        pw = st.text_input("Contraseña:", type="password")
        modo = st.radio("Optimizar para:", ["Computadora (Web Completa)", "Celular (Versión Ligera)"])
        if st.button("Entrar"):
            if pw == PASSWORD_CORRECTA:
                st.session_state.autenticado = True
                st.session_state.modo_dispositivo = modo
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
    st.stop()

# --- FUNCIÓN DE RUTAS SEGURAS CON CACHÉ ---
@st.cache_data
def get_path_safe(v_target, cub, sop, rev, color_nom):
    CARPETA_IMAGENES = os.path.join(os.path.dirname(__file__), "renders")
    color_map = {"negro": "NEGRO", "gris": "GRIS", "rojo": "ROJO"}
    color_upper = color_map.get(color_nom, "NEGRO")
    intentos = [v_target, v_target.replace("Cam", "Camera")]
    for cam_var in intentos:
        ruta = os.path.join(CARPETA_IMAGENES, f"{cub}_{sop}_{rev}_{cam_var}_{color_upper}.jpg")
        if os.path.exists(ruta): 
            return ruta
    return None

# ==========================================
# OPCIÓN A: MODO COMPUTADORA (WEB)
# ==========================================
if st.session_state.modo_dispositivo == "Computadora (Web Completa)":
    st.markdown("""
        <style>
        .stApp { background-color: #050505; color: #E0E0E0; font-family: 'Segoe UI', sans-serif; }
        .main-title { background: linear-gradient(90deg, #00FF00, #00CC00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 28px !important; font-weight: 800; }
        .phrase-box { color: #FFB347; font-style: italic; font-size: 17px !important; border-left: 3px solid #FF8C00; padding-left: 12px; min-height: 40px; }
        .stSelectbox { margin-bottom: -12px !important; max-width: 50% !important; }
        
        button[key^="btn_"] { width: 38px !important; height: 38px !important; border-radius: 50% !important; border: 2px solid #555 !important; color: white !important; font-weight: bold !important; transition: 0.3s; }
        button[key="btn_negro"] { background-color: #222325 !important; }
        button[key="btn_gris"] { background-color: #6b6c6f !important; }
        button[key="btn_rojo"] { background-color: #392424 !important; }
        
        .color-block { width: 100%; height: 28px; border-radius: 4px; border: 1px solid #333; margin-top: 5px; }
        .bg-negro { background-color: #000000; } .bg-gris { background-color: #808080; } .bg-rojo { background-color: #8B0000; }
        
        .stButton button:not([key^="btn_"]):not([key^="m_"]):not([key="btn_rotar_vista"]) { width: 100% !important; background-color: #111 !important; color: #00FF00 !important; border-radius: 4px; height: 30px !important; font-size: 11px !important; }
        
        div[data-baseweb="select"] input { caret-color: transparent !important; pointer-events: none !important; }
        div[data-baseweb="select"] { cursor: pointer !important; }
        [data-testid="stStatusWidget"], [data-testid="stHeader"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)

    col_visor, col_ctrl = st.columns([3, 2])
    
    with col_ctrl:
        # Recuperamos el logo en la parte superior del panel de control
        mostrar_logo()
        
        st.markdown("<p class='main-title'>VISUALIZADOR PARA CESAR 🏠🚗</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='phrase-box'>{st.session_state.ultima_frase}</p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        c_m, c_c = st.columns([2.3, 1.2])
        with c_m:
            scub = st.selectbox("Cubierta", ["ConAlero", "SinAlero"], format_func=lambda x: "Compacta" if x=="SinAlero" else "Extendida")
            if st.session_state.get('p_cub') != scub: st.session_state.ultima_frase = frases[scub]; st.session_state.p_cub = scub; st.rerun()
            
            ssop = st.selectbox("Soportes", ["Eficientes", "Dinamicos"], format_func=lambda x: "Esencial" if x=="Eficientes" else "Dinámico")
            if st.session_state.get('p_sop') != ssop: st.session_state.ultima_frase = frases[ssop]; st.session_state.p_sop = ssop; st.rerun()
            
            srev = st.selectbox("Revestimiento", ["Ninguno", "Poco", "Mucho"], format_func=lambda x: "Base" if x=="Ninguno" else ("Parcial" if x=="Poco" else "Completo"))
            if st.session_state.get('p_rev') != srev: st.session_state.ultima_frase = frases[srev]; st.session_state.p_rev = srev; st.rerun()
        
        with c_c:
            st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)
            for k, l, cl, f in [("btn_negro","N","bg-negro","negro"), ("btn_gris","G","bg-gris","gris"), ("btn_rojo","R","bg-rojo","rojo")]:
                r1, r2 = st.columns([0.5, 1.2])
                with r1: 
                    if st.button(l, key=k): st.session_state.color=f; st.session_state.ultima_frase=frases[f]; st.rerun()
                with r2: st.markdown(f"<div class='color-block {cl}'></div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        v_ids = ["Cam", "Cam_001", "Cam_002"]
        v_noms = {"Cam": "VISTA OBLICUA", "Cam_001": "VISTA FRONTAL", "Cam_002": "VISTA LATERAL"}
        v_mins = [v for v in v_ids if v != st.session_state.vista]
        m1, m2 = st.columns(2)
        for i, vid in enumerate(v_mins):
            with [m1, m2][i]:
                if st.button(v_noms[vid], key=f"wv_{vid}"): st.session_state.vista=vid; st.rerun()
                p = get_path_safe(vid, scub, ssop, srev, st.session_state.color)
                if p: st.image(p, use_container_width=True)

    with col_visor:
        img = get_path_safe(st.session_state.vista, scub, ssop, srev, st.session_state.color)
        if img: st.image(img, use_container_width=True)

# ==========================================
# OPCIÓN B: MODO CELULAR (MÓVIL)
# ==========================================
else:
    st.markdown("""
        <style>
        .stApp { background-color: #050505; color: #E0E0E0; }
        .block-container { padding-top: 0rem !important; padding-bottom: 1rem !important; }
        div[data-baseweb="select"] input { caret-color: transparent !important; pointer-events: none !important; }
        .main-title-m { background: linear-gradient(90deg, #00FF00, #00CC00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 20px !important; font-weight: 800; text-align: center; margin-top: 10px !important; margin-bottom: 2px !important; }
        .phrase-box-m { color: #FFB347; font-style: italic; font-size: 14px !important; text-align: center; border-bottom: 1px solid #333; padding-bottom: 8px; margin-bottom: 15px; min-height: 35px; display: flex; align-items: center; justify-content: center; }
        .stSelectbox { margin-bottom: -12px !important; }
        div[data-baseweb="select"] { height: 34px !important; font-size: 13px !important; cursor: pointer !important; }
        label { font-size: 12px !important; margin-bottom: 4px !important; display: block; color: #aaa !important; }
        .stButton button { background-color: #111 !important; border: 1px solid #555 !important; color: white !important; border-radius: 20px !important; font-weight: bold !important; height: 42px !important; font-size: 10px !important; text-transform: uppercase; }
        .stButton button[key="btn_rotar_vista"], .stButton button[key="btn_rotar_color"] { border: 1px solid #00FF00 !important; color: #00FF00 !important; }
        [data-testid="stStatusWidget"], [data-testid="stHeader"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)

    # Logo centrado para móvil
    mostrar_logo()
    
    st.markdown(f"<p class='main-title-m'>VISUALIZADOR PARA CESAR 🏠🚗</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='phrase-box-m'>{st.session_state.ultima_frase}</p>", unsafe_allow_html=True)
    
    m_cub = st.selectbox("CUBIERTA", ["ConAlero", "SinAlero"], key="mc", format_func=lambda x: "Compacta" if x=="SinAlero" else "Extendida")
    m_sop = st.selectbox("SOPORTES", ["Eficientes", "Dinamicos"], key="ms", format_func=lambda x: "Esencial" if x=="Eficientes" else "Dinámico")
    m_rev = st.selectbox("REVESTIMIENTO", ["Ninguno", "Poco", "Mucho"], key="mr", format_func=lambda x: "Base" if x=="Ninguno" else ("Parcial" if x=="Poco" else "Completo"))

    actual_config = f"{m_cub}-{m_sop}-{m_rev}"
    if st.session_state.get('last_config_m') != actual_config:
        if st.session_state.get('prev_cub') != m_cub: st.session_state.ultima_frase = frases[m_cub]
        elif st.session_state.get('prev_sop') != m_sop: st.session_state.ultima_frase = frases[m_sop]
        elif st.session_state.get('prev_rev') != m_rev: st.session_state.ultima_frase = frases[m_rev]
        st.session_state.last_config_m = actual_config
        st.session_state.prev_cub = m_cub
        st.session_state.prev_sop = m_sop
        st.session_state.prev_rev = m_rev
        st.rerun()

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    c_btn1, c_btn2 = st.columns(2)
    
    colores_ciclo = ["negro", "gris", "rojo"]
    nombres_colores = {"negro": "NEGRO", "gris": "GRIS", "rojo": "TERRACOTA"}
    sig_col = colores_ciclo[(colores_ciclo.index(st.session_state.color) + 1) % 3]
    with c_btn1:
        if st.button(f"🎨 {nombres_colores[sig_col]}", key="btn_rotar_color", use_container_width=True):
            st.session_state.color = sig_col
            st.session_state.ultima_frase = frases[sig_col]
            st.rerun()

    v_ciclo = ["Cam", "Cam_001", "Cam_002"]
    v_noms_m = {"Cam": "OBLICUA", "Cam_001": "FRONTAL", "Cam_002": "LATERAL"}
    sig_v = v_ciclo[(v_ciclo.index(st.session_state.vista) + 1) % 3]
    with c_btn2:
        if st.button(f"🔄 {v_noms_m[sig_v]}", key="btn_rotar_vista", use_container_width=True):
            st.session_state.vista = sig_v
            st.rerun()

    img_m = get_path_safe(st.session_state.vista, m_cub, m_sop, m_rev, st.session_state.color)
    if img_m:
        st.image(img_m, use_container_width=True)