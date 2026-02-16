import streamlit as st
from supabase import create_client, Client
from fpdf import FPDF

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

# --- 3. CSS: GLASSMORPHISM DENGAN PERBAIKAN SPASI ---
st.markdown("""
    <style>
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

    .logo-box {
        width: 60px; height: 60px;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 20px auto;
        font-size: 30px; font-weight: bold; color: white;
    }

    .welcome-text {
        text-align: center; color: white !important;
        font-size: 28px !important; font-weight: 600 !important;
        margin-bottom: 30px !important;
    }

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

    /* CARD DATA KEUANGAN */
    .data-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 15px;
        color: white;
    }

    .divider {
        display: flex; align-items: center; text-align: center;
        color: rgba(255, 255, 255, 0.3); margin: 25px 0;
    }
    .divider::before, .divider::after {
        content: ''; flex: 1; border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .divider span { padding: 0 10px; font-size: 14px; }

    /* PERBAIKAN SPASI TOMBOL SOSIAL */
    .social-container {
        display: flex;
        gap: 15px; /* MEMBERIKAN JARAK ANTAR TOMBOL */
        justify-content: center;
    }
    .social-btn {
        flex: 1; /* AGAR LEBARNYA SAMA */
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 12px;
        text-align: center;
        color: white;
        font-size: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNGSI PDF ---
def generate_pdf(user, financial):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "PUSKEU POLRI - SLIP GAJI", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Nama: {user['nama_lengkap']}", ln=True)
    pdf.cell(0, 10, f"Gaji Pokok: Rp {financial['gaji_pokok']:,.0f}", ln=True)
    pdf.cell(0, 10, f"Tunkin: Rp {financial['jumlah_tunkin']:,.0f}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- 5. LOGIKA NAVIGASI ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div class="logo-box">J</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-text">Welcome to Jitu Presisi</div>', unsafe_allow_html=True)

    nip_u = st.text_input("Email / NRP", placeholder="Enter your ID")
    pas_u = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Log In"):
        if nip_u and pas_u:
            try:
                res = supabase.table("pegawai").select("*").eq("email", nip_u).eq("password", pas_u).execute()
                if len(res.data) > 0:
                    st.session_state.user_info = res.data[0]
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid ID or Password")
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown('<div class="divider"><span>Or</span></div>', unsafe_allow_html=True)
    
    # MENGGUNAKAN CONTAINER DENGAN GAP
    st.markdown("""
        <div class="social-container">
            <div class="social-btn">
                <img src="https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-09-512.png" width="18" style="margin-right:8px;"> Google
            </div>
            <div class="social-btn">
                <span style="font-size:18px; margin-right:8px;">🍎</span> Apple
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    u = st.session_state.user_info
    st.markdown(f"<h2 style='color:white; text-align:center;'>Halo, {u['nama_lengkap']}</h2>", unsafe_allow_html=True)
    
    try:
        res_uang = supabase.table("tunkin").select("*").eq("nrp_nip", u["nrp_nip"]).execute()
        if len(res_uang.data) > 0:
            d = res_uang.data[0]
            st.markdown(f'<div class="data-card"><small>Gaji Pokok</small><h3>Rp {d["gaji_pokok"]:,.0f}</h3></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="data-card"><small>Tunkin</small><h3>Rp {d["jumlah_tunkin"]:,.0f}</h3></div>', unsafe_allow_html=True)
            
            pdf_bytes = generate_pdf(u, d)
            st.download_button("📄 DOWNLOAD SLIP GAJI", pdf_bytes, f"Slip_{u['nrp_nip']}.pdf", "application/pdf")
    except:
        st.error("Gagal memuat data.")

    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
