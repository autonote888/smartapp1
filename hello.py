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

# --- 3. CSS CUSTOM: SNOW WHITE & LOGO CENTER ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400;800&display=swap');

    /* Background Utama Putih Salju */
    .stApp {
        background-color: #FFFAFA !important; 
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    .block-container {
        padding-top: 1.5rem !important;
        max-width: 450px !important;
    }

    /* Memastikan Logo Berada di Tengah */
    .stImage {
        display: flex;
        justify-content: center;
        margin-bottom: 0px !important;
    }

    /* Header Text Styling */
    .header-container {
        text-align: center;
        margin-bottom: 30px;
        font-family: 'Inter', sans-serif;
    }
    .jitu-text { font-size: 32px; font-weight: 800; color: #001f3f; }
    .presisi-text { font-size: 32px; font-weight: 200; color: #FF8C00; }
    .mobile-text { display: block; font-size: 14px; color: #94a3b8; letter-spacing: 4px; margin-top: -5px; text-transform: uppercase; }

    /* Input Field Styling */
    div[data-baseweb="input"] {
        width: 100% !important;
        border-radius: 100px !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #f8fafc !important;
        height: 55px !important;
        margin-bottom: 5px;
    }

    .stTextInput input {
        color: #000000 !important;
        font-weight: 500 !important;
        background-color: transparent !important;
        padding: 0 25px !important;
    }

    /* Tombol Login Gradasi */
    div.stButton > button {
        width: 100% !important; 
        border-radius: 100px !important;
        height: 55px !important;
        background: linear-gradient(90deg, #a5b4fc 0%, #fdba74 100%) !important;
        color: #1e293b !important; 
        font-weight: 700 !important;
        border: none !important;
        margin-top: 15px !important;
    }

    /* Social Buttons */
    .social-container { display: flex; gap: 15px; justify-content: center; margin-top: 25px;}
    .social-btn {
        flex: 1; background: #ffffff; border: 1px solid #e2e8f0;
        border-radius: 15px; padding: 12px;
        display: flex; align-items: center; justify-content: center;
        color: #1e293b; font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIKA NAVIGASI ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # --- MENAMPILKAN LOGO jitu.png DI TENGAH ---
    # Menggunakan kolom untuk centering tambahan agar kualitas gambar terjaga
    col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 2, 1])
    with col_logo_2:
        try:
            st.image("jitu.png", width=100)
        except:
            st.markdown('<div style="text-align:center; font-size:40px; font-weight:bold; color:#001f3f;">J</div>', unsafe_allow_html=True)

    # Header Teks
    st.markdown("""
        <div class="header-container">
            <span class="jitu-text">JITU</span><span class="presisi-text"> PRESISI</span>
            <span class="mobile-text">MOBILE</span>
        </div>
    """, unsafe_allow_html=True)

    nip_u = st.text_input("NIP", placeholder="NRP / NIP", label_visibility="collapsed")
    pas_u = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")

    if st.button("Log In"):
        if nip_u and pas_u:
            try:
                # Login ke Supabase
                res = supabase.table("pegawai").select("*").eq("email", nip_u).eq("password", pas_u).execute()
                if len(res.data) > 0:
                    st.session_state.user_info = res.data[0]
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("NIP atau Password salah!")
            except Exception as e:
                st.error("Terjadi kesalahan koneksi.")

    # Footer Social Login
    st.markdown("""
        <div class="social-container">
            <div class="social-btn"><img src="https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-09-512.png" width="18" style="margin-right:8px;"> Google</div>
            <div class="social-btn"><img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" width="16" style="margin-right:8px;"> Apple</div>
        </div>
    """, unsafe_allow_html=True)
else:
    # DASHBOARD SEDERHANA
    u = st.session_state.user_info
    st.markdown(f"### Selamat Datang, {u['nama_lengkap']}")
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
