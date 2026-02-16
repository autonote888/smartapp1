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

# --- 3. CSS PREMIUM: GLOW & ROUNDED UI ---
st.markdown("""
    <style>
    /* Sembunyikan Header & Footer Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Background Putih Bersih */
    .stApp { background-color: #ffffff !important; }

    /* Pengaturan Kontainer Utama agar Responsif */
    .block-container {
        padding-top: 1rem !important;
    }

    @media (min-width: 800px) {
        .block-container {
            max-width: 450px !important;
            border: 1px solid #f8fafc;
            box-shadow: 0 15px 35px rgba(0,0,0,0.05);
            border-radius: 40px;
            margin-top: 40px !important;
            padding: 50px !important;
        }
    }

    /* Input Box Lonjong & Efek Menyala (Glow) */
    .stTextInput input {
        border-radius: 50px !important; /* Lonjong Sempurna */
        padding: 25px 25px !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #ffffff !important;
        color: #1e293b !important;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02);
    }
    
    /* Efek Menyala saat Klik (Focus) */
    .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.4) !important; /* Cahaya Biru Menyala */
        outline: none !important;
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
        padding: 10px 0;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 2px;
        margin: 25px 0;
        text-transform: uppercase;
    }

    /* Tombol MASUK Navy Berkilau */
    div.stButton > button {
        width: 100%;
        border-radius: 50px;
        height: 3.8em;
        background: linear-gradient(135deg, #002855 0%, #001f3f 100%) !important;
        color: white !important;
        font-weight: bold;
        font-size: 16px;
        border: none;
        box-shadow: 0 10px 20px rgba(0, 31, 63, 0.2);
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 25px rgba(0, 31, 63, 0.3);
    }

    .divider {
        display: flex; align-items: center; text-align: center;
        color: #94a3b8; margin: 30px 0;
    }
    .divider::before, .divider::after {
        content: ''; flex: 1; border-bottom: 1px solid #e2e8f0;
    }
    .divider span { padding: 0 10px; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIKA HALAMAN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # --- TAMPILAN LOGIN (FULL ANDROID LOOK) ---
    st.markdown("""
        <div class="main-container">
            <div style="text-align: right; color: #002855; font-weight: bold; font-size: 14px;">EN | ID</div>
            <div style="margin-top: 20px; margin-bottom: 10px;">
                <img src="https://logowik.com/content/uploads/images/j-letter7715.logowik.com.webp" width="75">
            </div>
            <div class="logo-text">JITU <span style="color:#d4af37">PRESISI</span></div>
            <div class="akses-aman">AKSES AMAN</div>
        </div>
    """, unsafe_allow_html=True)

    # Input User
    nip_user = st.text_input("NIP", placeholder="NRP / NIP", label_visibility="collapsed")
    pass_user = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")

    # Link Lupa
    st.markdown('<div style="text-align: right; margin-bottom: 25px;"><a href="#" style="color:#002855; font-weight:bold; text-decoration:none; font-size:14px;">Lupa?</a></div>', unsafe_allow_html=True)

    if st.button("MASUK"):
        if nip_user and pass_user:
            try:
                res = supabase.table("pegawai").select("*").eq("email", nip_user).eq("password", pass_user).execute()
                if len(res.data) > 0:
                    st.session_state.user_info = res.data[0]
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("NIP atau Password salah!")
            except Exception as e:
                st.error(f"Error: {e}")

    # Aksesoris Bawah
    st.markdown("""
        <div class="divider"><span>atau</span></div>
        <div style="text-align:center;">
            <button style="width:100%; border-radius:50px; padding:12px; border:1px solid #e2e8f0; background:white; font-weight:500; cursor:pointer; display:flex; align-items:center; justify-content:center;">
                <img src="https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-09-512.png" width="18" style="margin-right:10px;"> Google
            </button>
            <p style="margin-top:35px; color:#64748b; font-size:14px;">Baru? <b style="color:#002855;">Daftar</b></p>
        </div>
    """, unsafe_allow_html=True)
else:
    # --- DASHBOARD SETELAH LOGIN ---
    u = st.session_state.user_info
    st.markdown(f"""
        <div class='main-container'>
            <h3 style="color:#64748b;">Selamat Datang,</h3>
            <h2 style="color:#002855; margin-top:-10px;">{u['nama_lengkap']}</h2>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 20px 0;">
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Keluar"):
        st.session_state.logged_in = False
        st.rerun()
