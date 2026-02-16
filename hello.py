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

# --- 3. CSS CUSTOM: CLEAN MINIMALIST ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* Background Biru Muda Lembut */
    .stApp {
        background-color: #f0f4f8 !important; 
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    .block-container {
        padding-top: 3rem !important;
        max-width: 450px !important;
    }

    /* Header Text Styling */
    .header-container {
        text-align: center;
        margin-bottom: 25px;
        font-family: 'Inter', sans-serif;
    }
    .jitu-text { font-size: 32px; font-weight: 800; color: #001f3f; }
    .presisi-text { font-size: 32px; font-weight: 300; color: #FF8C00; }
    .mobile-text { display: block; font-size: 14px; color: #94a3b8; letter-spacing: 4px; margin-top: -5px; text-transform: uppercase; }

    .sub-welcome {
        text-align: center;
        color: #1e293b;
        font-size: 22px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 5px;
        font-family: 'Inter', sans-serif;
    }
    .sub-text {
        text-align: center;
        color: #64748b;
        font-size: 14px;
        margin-bottom: 30px;
    }

    /* Input Field: Putih Bersih Pill-Shaped */
    div[data-baseweb="input"] {
        width: 100% !important;
        border-radius: 100px !important;
        border: none !important;
        background-color: #ffffff !important; 
        height: 55px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02) !important;
    }

    .stTextInput input {
        color: #000000 !important;
        font-weight: 400 !important;
        background-color: transparent !important;
        padding: 0 25px !important;
    }

    /* Tombol Log In Biru Solid */
    div.stButton > button {
        width: 100% !important; 
        border-radius: 100px !important;
        height: 55px !important;
        background-color: #3197e8 !important; 
        color: #ffffff !important; 
        font-weight: 600 !important;
        font-size: 16px !important;
        border: none !important;
        margin-top: 10px !important;
    }

    /* Social Buttons: Menumpuk ke Bawah */
    .social-btn-full {
        background-color: #ffffff;
        border-radius: 100px;
        padding: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
        border: 1px solid #e2e8f0;
        color: #1e293b;
        font-size: 14px;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }

    .divider {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        margin: 20px 0;
        position: relative;
    }
    .divider::before {
        content: "";
        position: absolute;
        width: 100%; height: 1px;
        background: #e2e8f0;
        left: 0; top: 50%; z-index: -1;
    }
    .divider span { background: #f0f4f8; padding: 0 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIKA HALAMAN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Header Teks Langsung
    st.markdown("""
        <div class="header-container">
            <span class="jitu-text">JITU</span><span class="presisi-text"> PRESISI</span>
            <span class="mobile-text">MOBILE</span>
        </div>
        <div class="sub-welcome">Let's login to your account</div>
        <div class="sub-text">Access your personalized performance dashboard</div>
    """, unsafe_allow_html=True)

    nip_u = st.text_input("NIP", placeholder="Enter your NRP / NIP", label_visibility="collapsed")
    pas_u = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")

    if st.button("Log in"):
        if nip_u and pas_u:
            try:
                res = supabase.table("pegawai").select("*").eq("email", nip_u).eq("password", pas_u).execute()
                if len(res.data) > 0:
                    st.session_state.user_info = res.data[0]
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
            except:
                st.error("Database connection failed.")

    st.markdown('<div class="divider"><span>Or continue with</span></div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="social-btn-full">
            <img src="https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-09-512.png" width="20" style="margin-right:12px;"> Sign up with Google
        </div>
        <div class="social-btn-full">
            <img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" width="18" style="margin-right:12px;"> Sign up with Apple
        </div>
        <p style="text-align:center; color:#64748b; font-size:13px; margin-top:20px;">
            Already have an account? <span style="color:#3197e8; font-weight:600;">Sign Up</span>
        </p>
    """, unsafe_allow_html=True)

else:
    # --- DASHBOARD ---
    u = st.session_state.user_info
    st.markdown(f"### Welcome, {u['nama_lengkap']}")
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
