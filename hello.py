import streamlit as st
from supabase import create_client, Client

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="JITU PRESISI MOBILE", 
    page_icon="🔵", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. KONEKSI DATABASE ---
try:
    URL = st.secrets["SUPABASE_URL"]
    KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(URL, KEY)
except:
    st.error("Koneksi database gagal.")
    st.stop()

# --- 3. CSS PROFESSIONAL UX/UI POLES ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@200;400;600;800&display=swap');

    /* Background Neutral Soft */
    .stApp {
        background-color: #f8fafc !important; 
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    .block-container {
        padding-top: 5rem !important;
        max-width: 420px !important;
    }

    /* HEADER: Visual Hierarchy */
    .header-container {
        text-align: center;
        margin-bottom: 50px;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .jitu-text { 
        font-size: 36px; 
        font-weight: 800; 
        color: #0f172a; 
        letter-spacing: -1px;
    }
    .presisi-text { 
        font-size: 36px; 
        font-weight: 200; 
        color: #f59e0b; /* Orange modern */
    }
    .mobile-badge {
        display: inline-block;
        font-size: 12px;
        font-weight: 600;
        color: #64748b;
        letter-spacing: 3px;
        border-top: 1px solid #e2e8f0;
        padding-top: 5px;
        margin-top: 5px;
        text-transform: uppercase;
    }

    /* INPUT FIELD: Modern Elevation */
    div[data-baseweb="input"] {
        width: 100% !important;
        border-radius: 16px !important; /* Modern rounded, not full pill */
        border: 1px solid #e2e8f0 !important; 
        background-color: #ffffff !important; 
        height: 60px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        margin-bottom: 12px !important;
        transition: all 0.2s ease;
    }
    
    div[data-baseweb="input"]:focus-within {
        border: 2px solid #3b82f6 !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08) !important;
        transform: translateY(-1px);
    }

    .stTextInput input {
        color: #1e293b !important;
        font-weight: 500 !important;
        font-size: 16px !important;
        background-color: transparent !important;
        padding: 0 20px !important;
    }

    /* BUTTON: Solid Action */
    div.stButton > button {
        width: 100% !important; 
        border-radius: 16px !important;
        height: 60px !important;
        background-color: #1d4ed8 !important; /* Deep Blue */
        color: #ffffff !important; 
        font-weight: 600 !important;
        font-size: 16px !important;
        border: none !important;
        margin-top: 15px !important;
        box-shadow: 0 10px 15px -3px rgba(29, 78, 216, 0.2) !important;
        transition: all 0.2s ease;
    }
    
    div.stButton > button:active {
        transform: scale(0.98);
    }

    /* SOCIAL LOGIN: Minimalist Outline */
    .social-btn-container {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
        border: 1px solid #e2e8f0;
        color: #334155;
        font-size: 14px;
        font-weight: 600;
        transition: background-color 0.2s;
    }
    .social-btn-container:hover {
        background-color: #f1f5f9;
    }

    .divider {
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        margin: 35px 0;
        position: relative;
    }
    .divider::before {
        content: "";
        position: absolute;
        width: 100%; height: 1px;
        background: #e2e8f0;
        left: 0; top: 50%; z-index: -1;
    }
    .divider span { background: #f8fafc; padding: 0 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIKA HALAMAN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Header Section
    st.markdown("""
        <div class="header-container">
            <span class="jitu-text">JITU</span><span class="presisi-text"> PRESISI</span><br>
            <span class="mobile-badge">Mobile System</span>
        </div>
    """, unsafe_allow_html=True)

    # Login Form
    nip_u = st.text_input("NIP", placeholder="NRP / NIP", label_visibility="collapsed")
    pas_u = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")

    if st.button("Masuk ke Akun"):
        if nip_u and pas_u:
            try:
                res = supabase.table("pegawai").select("*").eq("email", nip_u).eq("password", pas_u).execute()
                if len(res.data) > 0:
                    st.session_state.user_info = res.data[0]
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Kredensial tidak valid.")
            except:
                st.error("Koneksi gagal.")

    st.markdown('<div class="divider"><span>Atau lanjutkan dengan</span></div>', unsafe_allow_html=True)

    # Social Login
    st.markdown("""
        <div class="social-btn-container">
            <img src="https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-09-512.png" width="20" style="margin-right:12px;"> Akun Google
        </div>
        <div class="social-btn-container">
            <img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" width="18" style="margin-right:12px;"> Akun Apple
        </div>
    """, unsafe_allow_html=True)

else:
    # Dashboard View
    u = st.session_state.user_info
    st.markdown(f"### Selamat Datang kembali, **{u['nama_lengkap']}**")
    if st.button("Keluar Sistem"):
        st.session_state.logged_in = False
        st.rerun()
