import streamlit as st
from supabase import create_client, Client

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="JITU PRESISI", page_icon="🔵", layout="centered")

# --- 2. CSS UNTUK MENYAMAKAN DESAIN (SAMA PERSIS GAMBAR) ---
st.markdown("""
    <style>
    /* Background Putih Bersih */
    .stApp {
        background-color: #ffffff !important;
    }
    
    header {visibility: hidden;}
    .block-container { padding-top: 1rem !important; }

    /* Container Utama */
    .main-container {
        max-width: 400px;
        margin: auto;
        text-align: center;
        font-family: 'sans-serif';
    }

    /* Logo J dan Teks (Simulasi dari Gambar) */
    .logo-section {
        margin-top: 20px;
        margin-bottom: 30px;
    }
    .logo-text {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: 2px;
        color: #002855; /* Biru Navy Polri */
        margin-top: 10px;
    }

    /* Akses Aman Badge */
    .akses-aman {
        background-color: #f1f5f9;
        color: #64748b;
        padding: 8px 0;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 30px;
        text-transform: uppercase;
    }

    /* Input Fields Style */
    .stTextInput input {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 30px !important; /* Melengkung Sempurna */
        padding: 25px 20px !important;
        color: #1e293b !important;
    }
    
    /* Tombol MASUK Navy */
    div.stButton > button {
        width: 100%;
        border-radius: 30px;
        height: 3.5em;
        background-color: #001f3f !important; /* Navy Gelap */
        color: white !important;
        font-weight: bold;
        font-size: 16px;
        border: none;
        margin-top: 10px;
    }

    /* Tombol Google Outline */
    .google-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: 12px;
        border: 1px solid #e2e8f0;
        border-radius: 30px;
        background: white;
        color: #1e293b;
        font-weight: 500;
        text-decoration: none;
        margin-top: 15px;
    }

    /* Teks Pembatas "atau" */
    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        color: #94a3b8;
        margin: 25px 0;
    }
    .divider::before, .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #e2e8f0;
    }
    .divider span { padding: 0 10px; font-size: 14px; }

    /* Footer Teks */
    .footer-text {
        margin-top: 40px;
        font-size: 14px;
        color: #64748b;
    }
    .footer-text b { color: #002855; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. KONEKSI DATABASE ---
try:
    URL = st.secrets["SUPABASE_URL"]
    KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(URL, KEY)
except:
    st.error("Gagal terhubung ke database.")
    st.stop()

# --- 4. LOGIKA HALAMAN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # TAMPILAN LOGIN (SAMA PERSIS REFERENSI)
    st.markdown("""
        <div class="main-container">
            <div style="text-align: right; color: #002855; font-weight: bold; font-size: 14px;">EN | ID</div>
            <div class="logo-section">
                <img src="https://logowik.com/content/uploads/images/j-letter7715.logowik.com.webp" width="60">
                <div class="logo-text">JITU <span style="color:#d4af37">PRESISI</span></div>
            </div>
            <div class="akses-aman">AKSES AMAN</div>
        </div>
    """, unsafe_allow_html=True)

    # Form Login
    email_in = st.text_input("NRP / NIP", placeholder="Masukkan NRP atau NIP")
    pass_in = st.text_input("Password", type="password", placeholder="Masukkan password")

    # Link Lupa Password & Icon Fingerprint (Hiasan UI)
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding: 0 10px;">
            <span style="font-size: 24px;">👤</span>
            <a href="#" style="text-decoration: none; color: #002855; font-weight: bold; font-size: 14px;">Lupa?</a>
        </div>
    """, unsafe_allow_html=True)

    if st.button("MASUK"):
        res = supabase.table("pegawai").select("*").eq("email", email_in).eq("password", pass_in).execute()
        if len(res.data) > 0:
            st.session_state.user_info = res.data[0]
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("NIP atau Password salah!")

    # Elemen Tambahan Google & Daftar
    st.markdown("""
        <div class="divider"><span>atau</span></div>
        <a href="#" class="google-btn">
            <img src="https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-09-512.png" width="20" style="margin-right:10px;"> Google
        </a>
        <div class="footer-text">Baru? <b>Daftar</b></div>
    """, unsafe_allow_html=True)

else:
    # HALAMAN SETELAH LOGIN
    u = st.session_state.user_info
    st.success(f"Selamat Datang, {u['nama_lengkap']}")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
