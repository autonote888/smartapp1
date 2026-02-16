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

# --- 3. CSS PERBAIKAN (MENGHAPUS TEPI HITAM) ---
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

    /* Menghilangkan border kotak bawaan Streamlit yang bikin tepi hitam */
    div[data-baseweb="input"] {
        border-radius: 100px !important;
        border: none !important;
        background-color: transparent !important;
    }

    /* Styling Kolom Input NRP & Password */
    .stTextInput > div > div {
        background-color: #f1f5f9 !important; /* Warna abu-abu muda polos */
        border-radius: 100px !important;
        border: none !important;
    }

    .stTextInput input {
        background-color: transparent !important;
        border-radius: 100px !important;
        border: none !important;
        height: 55px !important;
        padding: 0 25px !important;
        color: #1e293b !important;
    }

    /* Menghilangkan highlight saat klik agar tidak muncul kotak hitam */
    .stTextInput input:focus {
        box-shadow: none !important;
        outline: none !important;
    }

    /* Ikon Mata Password agar presisi */
    button[title="Show password"] {
        margin-right: 10px !important;
    }

    /* --- HEADER STYLING --- */
    .header-container {
        text-align: center;
        margin-bottom: 30px;
        font-family: 'Inter', sans-serif;
    }
    .jitu-text {
        font-size: 32px;
        font-weight: 800; 
        color: #001f3f; 
    }
    .presisi-text {
        font-size: 32px;
        font-weight: 200; 
        color: #FF8C00; 
    }
    .mobile-text {
        display: block;
        font-size: 14px;
        color: #64748b; 
        letter-spacing: 4px;
        margin-top: -5px;
    }

    .logo-box {
        width: 60px; height: 60px;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 15px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 15px auto;
        font-size: 30px; font-weight: bold; color: #001f3f;
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
    }

    /* Tombol Sosial */
    .social-container { display: flex; gap: 15px; justify-content: center; margin-top: 20px;}
    .social-btn {
        flex: 1; background: #ffffff; border: 1px solid #e2e8f0;
        border-radius: 15px; padding: 12px;
        display: flex; align-items: center; justify-content: center;
        color: #1e293b; font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIKA HALAMAN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div class="logo-box">J</div>', unsafe_allow_html=True)
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
                res = supabase.table("pegawai").select("*").eq("email", nip_u).eq("password", pas_u).execute()
                if len(res.data) > 0:
                    st.session_state.user_info = res.data[0]
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("NIP atau Password salah!")
            except Exception as e:
                st.error("Terjadi kesalahan sistem.")

    st.markdown("""
        <div class="social-container">
            <div class="social-btn"><img src="https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-09-512.png" width="18" style="margin-right:8px;"> Google</div>
            <div class="social-btn"><img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" width="16" style="margin-right:8px;"> Apple</div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"### Selamat Datang, {st.session_state.user_info['nama_lengkap']}")
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
