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

# --- 3. CSS: GLASSMORPHISM PREMIUM LOOK ---
st.markdown("""
    <style>
    /* 1. Background Gradasi Gelap ala iOS/Notes */
    .stApp {
        background: radial-gradient(circle at top right, #2e1065, #0f172a) !important;
        background-attachment: fixed;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* 2. Container Center */
    .block-container {
        padding-top: 2rem !important;
        max-width: 450px !important;
    }

    /* 3. Logo J Box */
    .logo-box {
        width: 60px;
        height: 60px;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px auto;
        font-size: 30px;
        font-weight: bold;
        color: white;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }

    /* 4. Teks Welcome */
    .welcome-text {
        text-align: center;
        color: white !important;
        font-size: 28px !important;
        font-weight: 600 !important;
        margin-bottom: 30px !important;
        font-family: 'Inter', sans-serif;
    }

    /* 5. Input Field Glassmorphism */
    .stTextInput label {
        color: rgba(255, 255, 255, 0.7) !important;
        margin-bottom: 8px !important;
    }
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        color: white !important;
        padding: 15px 20px !important;
        height: 55px !important;
    }

    /* 6. Tombol Login Gradasi (Sunset Glow) */
    div.stButton > button {
        width: 100% !important;
        border-radius: 50px !important;
        height: 55px !important;
        background: linear-gradient(90deg, #a5b4fc 0%, #fdba74 100%) !important;
        color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border: none !important;
        margin-top: 20px !important;
        transition: 0.3s !important;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(253, 186, 116, 0.4);
    }

    /* 7. Divider Or */
    .divider {
        display: flex; align-items: center; text-align: center;
        color: rgba(255, 255, 255, 0.3); margin: 25px 0;
    }
    .divider::before, .divider::after {
        content: ''; flex: 1; border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .divider span { padding: 0 10px; font-size: 14px; }

    /* 8. Tombol Google & Apple (Dark Glass) */
    .social-btn {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        text-decoration: none;
        font-size: 14px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIKA HALAMAN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Header Section
    st.markdown('<div class="logo-box">J</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-text">Welcome to Jitu Presisi</div>', unsafe_allow_html=True)

    # Input Section
    nip_u = st.text_input("Email / NRP", placeholder="Enter your ID")
    pas_u = st.text_input("Password", type="password", placeholder="Enter your password")

    # Remember Me & Forgot (Simulasi UI)
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown('<p style="color:rgba(255,255,255,0.5); font-size:12px;">Remember me</p>', unsafe_allow_html=True)
    with col2:
        st.markdown('<p style="color:rgba(255,255,255,0.5); font-size:12px; text-align:right;">Forgot Password?</p>', unsafe_allow_html=True)

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
                    st.error("Invalid ID or Password")
            except Exception as e:
                st.error(f"Error: {e}")

    # Divider & Social Login
    st.markdown('<div class="divider"><span>Or</span></div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="social-btn">Google</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="social-btn">Apple</div>', unsafe_allow_html=True)

    st.markdown('<p style="text-align:center; color:rgba(255,255,255,0.5); font-size:13px; margin-top:30px;">Don\'t have an account? <b style="color:white;">Sign Up</b></p>', unsafe_allow_html=True)

else:
    # DASHBOARD
    u = st.session_state.user_info
    st.markdown(f"<h2 style='color:white; text-align:center;'>Halo, {u['nama_lengkap']}</h2>", unsafe_allow_html=True)
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
