import streamlit as st
from supabase import create_client, Client
from fpdf import FPDF

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="JITU PRESISI", page_icon="💰", layout="centered")

# --- 2. CSS "LIVIN STYLE" PREMIUM (GLOW & GLASS) ---
st.markdown("""
    <style>
    /* Background Gradient ala Perbankan */
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    }
    
    header {visibility: hidden;}
    .block-container { padding-top: 2rem !important; }

    /* Logo & Header Center */
    .brand-header {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 20px;
    }
    .brand-header h1 {
        font-size: 2.5rem !important;
        background: linear-gradient(to right, #60a5fa, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    /* Kartu Login Glassmorphism */
    .login-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 40px 30px;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin: 0 10px;
    }

    /* Input Box Menyala Blue Glow */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.07) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        transition: 0.3s all;
    }
    .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.5) !important;
    }

    /* Tombol Biru Menyala (Neon Glow) */
    div.stButton > button {
        width: 100%;
        border-radius: 15px;
        height: 3.8em;
        background: linear-gradient(90deg, #2563eb, #3b82f6) !important;
        color: white !important;
        font-weight: bold;
        border: none;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.4);
        transition: 0.4s;
        margin-top: 20px;
    }
    div.stButton > button:hover {
        box-shadow: 0 15px 30px rgba(37, 99, 235, 0.6);
        transform: translateY(-3px);
    }

    /* Label Input Putih */
    .stTextInput label {
        color: #94a3b8 !important;
        font-size: 0.9rem !important;
        margin-left: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. KONEKSI SUPABASE ---
try:
    URL = st.secrets["SUPABASE_URL"]
    KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(URL, KEY)
except:
    st.error("Konfigurasi Database Belum Siap.")
    st.stop()

# --- 4. LOGIKA LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # --- UI LOGIN SCREEN ---
    st.markdown('<div class="brand-header"><h1>JITU PRESISI</h1><p style="color:#64748b;">Financial Management System</p></div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        email_in = st.text_input("Username / Email Dinas", placeholder="nama@polri.go.id")
        pass_in = st.text_input("Password", type="password", placeholder="••••••••")
        
        st.write("")
        if st.button("Masuk Ke Sistem"):
            res = supabase.table("pegawai").select("*").eq("email", email_in).eq("password", pass_in).execute()
            if len(res.data) > 0:
                st.session_state.user_info = res.data[0]
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Akses Ditolak! Periksa kembali ID dan Password Anda.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Footer Aksesoris
        st.markdown("""
            <div style="text-align:center; margin-top:30px; color:#475569; font-size:0.8rem;">
                Puskeu Presisi Mobile v2.0<br>
                © 2026 Indonesian National Police Finance Center
            </div>
        """, unsafe_allow_html=True)

else:
    # --- DASHBOARD BERHASIL LOGIN ---
    u = st.session_state.user_info
    st.markdown(f'<div class="brand-header"><h1>Halo, {u["nama_lengkap"].split()[0]}!</h1></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.write(f"NIP: {u['nip']}")
    st.write(f"Jabatan: {u['jabatan']}")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
