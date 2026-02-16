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

# --- 3. CSS POLESAN PROFESIONAL & ANTI-DARK MODE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@200;400;600;800&display=swap');

    /* FIX: MEMAKSA BROWSER HP TETAP LIGHT MODE */
    :root {
        color-scheme: light !important;
    }

    .stApp { 
        background-color: #f8fafc !important; 
        color: #1e293b !important;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    .block-container {
        padding-top: 4rem !important;
        max-width: 420px !important;
    }

    /* HEADER */
    .header-container {
        text-align: center;
        margin-bottom: 40px;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .jitu-text { font-size: 36px; font-weight: 800; color: #0f172a; letter-spacing: -1px; }
    .presisi-text { font-size: 36px; font-weight: 200; color: #f59e0b; }

    /* INPUT & SHADOW: Dipastikan background putih solid */
    div[data-baseweb="input"] {
        width: 100% !important;
        border-radius: 16px !important;
        border: 1px solid #e2e8f0 !important; 
        background-color: #ffffff !important; /* WAJIB PUTIH */
        height: 60px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 8px !important;
    }

    .stTextInput input {
        color: #000000 !important; /* TEKS WAJIB HITAM */
        font-weight: 500 !important;
        background-color: transparent !important;
    }

    /* LUPA PASSWORD */
    .forgot-pw-container {
        text-align: right;
        margin-bottom: 25px;
        margin-right: 5px;
    }
    .forgot-pw-link {
        color: #3b82f6;
        font-size: 13px;
        font-weight: 600;
        text-decoration: none;
    }

    /* PRIMARY BUTTON */
    div.stButton > button {
        width: 100% !important; 
        border-radius: 16px !important;
        height: 60px !important;
        background-color: #1d4ed8 !important; 
        color: #ffffff !important; 
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 10px 15px -3px rgba(29, 78, 216, 0.2) !important;
    }

    /* SOCIAL BUTTON */
    .social-btn {
        background-color: #ffffff !important;
        border-radius: 16px;
        padding: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
        border: 1px solid #e2e8f0;
        color: #334155 !important;
        font-weight: 600;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }

    .divider {
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        margin: 30px 0;
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

# --- 4. LOGIKA NAVIGASI ---
if "page" not in st.session_state:
    st.session_state.page = "login"

if st.session_state.page == "login":
    st.markdown("""
        <div class="header-container">
            <span class="jitu-text">JITU</span><span class="presisi-text"> PRESISI</span>
        </div>
    """, unsafe_allow_html=True)

    nip_u = st.text_input("NIP", placeholder="NRP / NIP", label_visibility="collapsed")
    pas_u = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")

    st.markdown('<div class="forgot-pw-container"><a href="#" class="forgot-pw-link">Lupa Password?</a></div>', unsafe_allow_html=True)

    if st.button("Masuk"):
        if nip_u and pas_u:
            try:
                res = supabase.table("pegawai").select("*").eq("email", nip_u).eq("password", pas_u).execute()
                if len(res.data) > 0:
                    st.success("Berhasil!")
                else:
                    st.error("Kredensial salah.")
            except:
                st.error("Gangguan server.")

    st.markdown('<div class="divider"><span>Atau</span></div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="social-btn">
            <img src="https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-09-512.png" width="20" style="margin-right:12px;"> Akun Google
        </div>
    """, unsafe_allow_html=True)

    # Tombol pindah halaman dengan tombol Streamlit asli (lebih stabil)
    if st.button("Belum punya akun? Daftar"):
        st.session_state.page = "signup"
        st.rerun()

elif st.session_state.page == "signup":
    st.markdown("### Buat Akun")
    if st.button("Kembali ke Login"):
        st.session_state.page = "login"
        st.rerun()
