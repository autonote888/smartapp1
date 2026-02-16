import streamlit as st
from supabase import create_client, Client

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="JITU PRESISI", 
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

# --- 3. CSS MINIMALIS POLOS & LONJONG ---
st.markdown("""
    <style>
    /* Sembunyikan Header & Footer Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Background Putih Bersih */
    .stApp { background-color: #ffffff !important; }

    /* Container Utama Responsif */
    .block-container {
        padding-top: 1rem !important;
    }

    @media (min-width: 800px) {
        .block-container {
            max-width: 450px !important;
            border: 1px solid #f1f5f9;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            border-radius: 30px;
            margin-top: 50px !important;
            padding: 40px !important;
        }
    }

    /* INPUT POLOSAN LONJONG */
    .stTextInput > div > div > input {
        border-radius: 50px !important; /* Lonjong Sempurna */
        padding: 12px 25px !important;
        height: 55px !important;
        border: 1px solid #e2e8f0 !important; /* Garis tipis halus */
        background-color: #f8fafc !important; /* Warna abu-abu sangat muda */
        color: #1e293b !important;
        box-shadow: none !important; /* Tanpa bayangan/glow */
        margin-bottom: 5px !important;
    }
    
    /* State saat diklik (Tetap Polos) */
    .stTextInput > div > div > input:focus {
        border-color: #cbd5e1 !important; /* Sedikit lebih gelap saat diklik */
        outline: none !important;
        box-shadow: none !important;
    }

    /* Styling Teks & Tombol */
    .main-container { text-align: center; font-family: 'sans-serif'; }
    .logo-text {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 2px;
        color: #002855;
        margin-top: 10px;
    }
    .akses-aman {
        background-color: #f1f5f9;
        color: #64748b;
        padding: 8px 0;
        border-radius: 15px;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 1px;
        margin: 20px 0;
        text-transform: uppercase;
    }

    /* Tombol MASUK Polos Navy */
    div.stButton > button {
        width: 100% !important;
        border-radius: 50px !important;
        height: 55px !important;
        background-color: #001f3f !important; /* Navy Polos */
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        margin-top: 15px !important;
    }

    .divider {
        display: flex; align-items: center; text-align: center;
        color: #94a3b8; margin: 25px 0;
    }
    .divider::before, .divider::after {
        content: ''; flex: 1; border-bottom: 1px solid #f1f5f9;
    }
    .divider span { padding: 0 10px; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIKA HALAMAN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # --- TAMPILAN LOGIN ---
    st.markdown("""
        <div class="main-container">
            <div style="text-align: right; color: #002855; font-weight: bold; font-size: 13px;">EN | ID</div>
            <div style="margin-top: 15px; margin-bottom: 5px;">
                <img src="https://logowik.com/content/uploads/images/j-letter7715.logowik.com.webp" width="65">
            </div>
            <div class="logo-text">JITU <span style="color:#d4af37">PRESISI</span></div>
            <div class="akses-aman">AKSES AMAN</div>
        </div>
    """, unsafe_allow_html=True)

    # Input NRP & Password
    nip_u = st.text_input("NIP", placeholder="NRP / NIP", label_visibility="collapsed")
    pas_u = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")

    # Link Lupa
    st.markdown('<div style="text-align: right; margin-top: 5px;"><a href="#" style="color:#002855; font-weight:bold; text-decoration:none; font-size:13px;">Lupa?</a></div>', unsafe_allow_html=True)

    if st.button("MASUK"):
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
                st.error(f"Error: {e}")

    # Footer Aksesoris
    st.markdown("""
        <div class="divider"><span>atau</span></div>
        <div style="text-align:center;">
            <button style="width:100%; border-radius:50px; padding:12px; border:1px solid #e2e8f0; background:white; font-weight:500; color:#1e293b; font-family:sans-serif; cursor:pointer;">
                <img src="https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-09-512.png" width="16" style="margin-right:8px; vertical-align:middle;"> Google
            </button>
            <p style="margin-top:30px; color:#64748b; font-size:13px;">Baru? <b style="color:#002855;">Daftar</b></p>
        </div>
    """, unsafe_allow_html=True)
else:
    # --- DASHBOARD SETELAH LOGIN ---
    u = st.session_state.user_info
    st.markdown(f"<div class='main-container'><h3>Selamat Datang,</h3><h2>{u['nama_lengkap']}</h2></div>", unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
