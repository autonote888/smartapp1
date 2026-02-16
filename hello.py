import streamlit as st
from supabase import create_client, Client
from fpdf import FPDF

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
    st.error("Koneksi database gagal. Cek Secrets.")
    st.stop()

# --- 3. CSS: GLASSMORPHISM & HEADER CUSTOM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400;800&display=swap');

    .stApp {
        background: radial-gradient(circle at top right, #2e1065, #0f172a) !important;
        background-attachment: fixed;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    .block-container {
        padding-top: 2rem !important;
        max-width: 450px !important;
    }

    /* --- HEADER STYLING SESUAI INSTRUKSI --- */
    .header-container {
        text-align: center;
        margin-bottom: 30px;
        font-family: 'Inter', sans-serif;
    }
    .jitu-text {
        font-size: 32px;
        font-weight: 800; /* Font Tebal */
        color: #001f3f; /* Dongker Gelap */
        letter-spacing: 1px;
    }
    .presisi-text {
        font-size: 32px;
        font-weight: 200; /* Font Tipis */
        color: #FF8C00; /* Orange */
        letter-spacing: 1px;
    }
    .mobile-text {
        display: block;
        font-size: 14px;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.6);
        letter-spacing: 4px;
        margin-top: -5px;
        text-transform: uppercase;
    }

    .logo-box {
        width: 60px; height: 60px;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 15px auto;
        font-size: 30px; font-weight: bold; color: white;
    }

    /* Input & Button Styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        color: white !important;
        height: 55px !important;
    }

    div.stButton > button {
        width: 100% !important; border-radius: 50px !important;
        height: 55px !important;
        background: linear-gradient(90deg, #a5b4fc 0%, #fdba74 100%) !important;
        color: #1e293b !important; font-weight: 700 !important;
        border: none !important;
    }

    .data-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        border-radius: 20px; padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 15px; color: white;
    }

    .social-container { display: flex; gap: 15px; justify-content: center; margin-top: 20px;}
    .social-btn {
        flex: 1; background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px; padding: 12px;
        text-align: center; color: white; font-size: 14px;
        display: flex; align-items: center; justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIKA NAVIGASI ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # --- UI LOGIN ---
    st.markdown('<div class="logo-box">J</div>', unsafe_allow_html=True)
    
    # Header sesuai permintaan Bapak
    st.markdown("""
        <div class="header-container">
            <span class="jitu-text">JITU</span><span class="presisi-text"> PRESISI</span>
            <span class="mobile-text">MOBILE</span>
        </div>
    """, unsafe_allow_html=True)

    nip_u = st.text_input("Email / NRP", placeholder="Enter your ID", label_visibility="collapsed")
    pas_u = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")

    if st.button("Log In"):
        if nip_u and pas_u:
            try:
                # Cek tabel pegawai di Supabase
                res = supabase.table("pegawai").select("*").eq("email", nip_u).eq("password", pas_u).execute()
                if len(res.data) > 0:
                    st.session_state.user_info = res.data[0]
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid ID or Password")
            except Exception as e:
                st.error(f"Error: {e}")

    # Social Login
    st.markdown("""
        <div class="social-container">
            <div class="social-btn">
                <img src="https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-09-512.png" width="18" style="margin-right:8px;"> Google
            </div>
            <div class="social-btn">
                <img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" width="16" style="margin-right:8px; filter: brightness(0) invert(1);"> Apple
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    # --- DASHBOARD SETELAH LOGIN ---
    u = st.session_state.user_info
    st.markdown(f"<h2 style='color:white; text-align:center;'>Halo, {u['nama_lengkap']}</h2>", unsafe_allow_html=True)
    
    try:
        # Menampilkan data tunkin
        res_uang = supabase.table("tunkin").select("*").eq("nrp_nip", u["nrp_nip"]).execute()
        if len(res_uang.data) > 0:
            d = res_uang.data[0]
            st.markdown(f'<div class="data-card"><small>Gaji Pokok</small><h3>Rp {d["gaji_pokok"]:,.0f}</h3></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="data-card"><small>Tunjangan Kinerja</small><h3>Rp {d["jumlah_tunkin"]:,.0f}</h3></div>', unsafe_allow_html=True)
    except:
        st.error("Data tidak ditemukan.")

    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
