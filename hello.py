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
    st.error("Gagal terhubung ke database. Cek Secrets di Streamlit Cloud.")
    st.stop()

# --- 3. CSS "FULL SCREEN" & ANDROID UI ---
st.markdown("""
    <style>
    /* Menghilangkan Toolbar Streamlit (Garis Hitam & Footer) */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Background Putih Bersih */
    .stApp { background-color: #ffffff !important; }
    
    /* Padding Konten */
    .block-container { 
        padding-top: 2rem !important; 
        max-width: 450px !important;
    }

    /* Logo & Teks Styling */
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
        border-radius: 15px;
        font-size: 13px;
        font-weight: bold;
        letter-spacing: 2px;
        margin: 25px 0;
        text-transform: uppercase;
    }

    /* Input Fields (Rounded) */
    .stTextInput input {
        border-radius: 30px !important;
        padding: 25px 20px !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #ffffff !important;
        color: #1e293b !important;
    }
    
    /* Tombol Navy */
    div.stButton > button {
        width: 100%;
        border-radius: 30px;
        height: 3.8em;
        background-color: #001f3f !important;
        color: white !important;
        font-weight: bold;
        font-size: 16px;
        border: none;
        margin-top: 10px;
    }

    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        color: #94a3b8;
        margin: 30px 0;
    }
    .divider::before, .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #e2e8f0;
    }
    .divider span { padding: 0 10px; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIKA NAVIGASI ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # --- TAMPILAN LOGIN SCREEN ---
    st.markdown("""
        <div class="main-container">
            <div style="text-align: right; color: #002855; font-weight: bold; margin-bottom: 20px;">EN | ID</div>
            <div style="margin-bottom: 10px;">
                <img src="https://logowik.com/content/uploads/images/j-letter7715.logowik.com.webp" width="70">
            </div>
            <div class="logo-text">JITU <span style="color:#d4af37">PRESISI</span></div>
            <div class="akses-aman">AKSES AMAN</div>
        </div>
    """, unsafe_allow_html=True)

    # Form Input (Menggunakan label_visibility untuk tampilan bersih)
    nip_input = st.text_input("NIP", placeholder="NRP / NIP", label_visibility="collapsed")
    pwd_input = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")

    st.markdown('<div style="text-align: right; margin-bottom: 20px;"><a href="#" style="color:#002855; font-weight:bold; text-decoration:none; font-size:14px;">Lupa?</a></div>', unsafe_allow_html=True)

    if st.button("MASUK"):
        if nip_input and pwd_input:
            try:
                # Cek ke tabel pegawai (Mencocokkan email/nip dan password)
                res = supabase.table("pegawai").select("*").eq("email", nip_input).eq("password", pwd_input).execute()
                
                if len(res.data) > 0:
                    st.session_state.user_info = res.data[0]
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("NIP atau Password salah!")
            except Exception as e:
                st.error(f"Error Database: {e}")
        else:
            st.warning("Harap isi NIP dan Password.")

    # Footer Aksesoris
    st.markdown("""
        <div class="divider"><span>atau</span></div>
        <div style="text-align:center;">
            <button style="width:100%; border-radius:30px; padding:12px; border:1px solid #e2e8f0; background:white; font-weight:500; cursor:pointer;">
                <img src="https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-09-512.png" width="18" style="vertical-align:middle; margin-right:10px;"> Google
            </button>
            <p style="margin-top:30px; color:#64748b; font-size:14px;">Baru? <b style="color:#002855;">Daftar</b></p>
        </div>
    """, unsafe_allow_html=True)

else:
    # --- TAMPILAN DASHBOARD (SETELAH LOGIN) ---
    u = st.session_state.user_info
    st.markdown(f"""
        <div class="main-container">
            <h2 style="color:#002855;">Selamat Datang,</h2>
            <h3>{u['nama_lengkap']}</h3>
            <hr>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
