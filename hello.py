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

# --- 3. CSS: SNOW WHITE & PILL-SHAPED CUSTOM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400;800&display=swap');

    /* Background Putih Salju */
    .stApp {
        background-color: #FFFAFA !important; 
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    .block-container {
        padding-top: 2rem !important;
        max-width: 450px !important;
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
        letter-spacing: 1px;
    }
    .presisi-text {
        font-size: 32px;
        font-weight: 200; 
        color: #FF8C00; 
        letter-spacing: 1px;
    }
    .mobile-text {
        display: block;
        font-size: 14px;
        font-weight: 400;
        color: #64748b; 
        letter-spacing: 4px;
        margin-top: -5px;
        text-transform: uppercase;
    }

    .logo-box {
        width: 60px; height: 60px;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 15px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 15px auto;
        font-size: 30px; font-weight: bold; color: #001f3f;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    /* --- INPUT PILL-SHAPED (LOGIKA MATA OTOMATIS) --- */
    .stTextInput > div > div > input {
        background-color: #f1f5f9 !important; 
        border: none !important;
        border-radius: 100px !important; /* Bentuk Pil */
        color: #1e293b !important;
        height: 55px !important;
        padding: 0 25px !important;
    }
    
    /* Mengatur posisi ikon mata agar presisi di dalam bentuk pil */
    .stTextInput div[data-baseweb="input"] button {
        margin-right: 15px !important;
        color: #64748b !important;
    }

    /* Tombol Login Sunset */
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

    /* Card Dashboard */
    .data-card {
        background: #ffffff;
        border-radius: 20px; 
        padding: 20px;
        border: 1px solid #f1f5f9;
        margin-bottom: 15px; 
        color: #1e293b;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }

    .divider {
        display: flex; align-items: center; text-align: center;
        color: #94a3b8; margin: 25px 0;
    }
    .divider::before, .divider::after {
        content: ''; flex: 1; border-bottom: 1px solid #e2e8f0;
    }
    .divider span { padding: 0 10px; font-size: 14px; }

    .social-container { display: flex; gap: 15px; justify-content: center; }
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
    # --- TAMPILAN LOGIN ---
    st.markdown('<div class="logo-box">J</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="header-container">
            <span class="jitu-text">JITU</span><span class="presisi-text"> PRESISI</span>
            <span class="mobile-text">MOBILE</span>
        </div>
    """, unsafe_allow_html=True)

    # Input User
    nip_u = st.text_input("NIP", placeholder="NRP / NIP", label_visibility="collapsed")
    
    # Input Password (Otomatis ada fitur mata karena type="password")
    pas_u = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")

    if st.button("Log In"):
        if nip_u and pas_u:
            try:
                # Mencari data di tabel pegawai
                res = supabase.table("pegawai").select("*").eq("email", nip_u).eq("password", pas_u).execute()
                if len(res.data) > 0:
                    st.session_state.user_info = res.data[0]
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("NIP atau Password salah!")
            except Exception as e:
                st.error(f"Error: {e}")

    # Footer
    st.markdown('<div class="divider"><span>Or</span></div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="social-container">
            <div class="social-btn"><img src="https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-09-512.png" width="18" style="margin-right:8px;"> Google</div>
            <div class="social-btn"><img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" width="16" style="margin-right:8px;"> Apple</div>
        </div>
    """, unsafe_allow_html=True)
else:
    # --- DASHBOARD SETELAH LOGIN ---
    u = st.session_state.user_info
    st.markdown(f"### Selamat Datang, {u['nama_lengkap']}")
    
    try:
        # Menampilkan data penghasilan
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
