import streamlit as st
from supabase import create_client, Client
from fpdf import FPDF

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="JITU PRESISI", page_icon="💰", layout="centered")

# --- 2. CSS PREMIUM UI/UX 3.0 ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f4f8 !important; }
    header {visibility: hidden;}
    .block-container { padding-top: 0rem !important; }

    /* Header Profile Modern */
    .app-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 60px 25px 80px 25px;
        border-radius: 0 0 50px 50px;
        color: white !important;
        text-align: center;
        margin: -20px -20px 0 -20px;
        box-shadow: 0 10px 30px rgba(30, 58, 138, 0.3);
    }

    /* Floating Navigation */
    .stTabs [data-baseweb="tab-list"] {
        background-color: white;
        padding: 10px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin: -30px 10px 20px 10px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] { font-weight: 600; color: #64748b; }
    .stTabs [aria-selected="true"] { color: #1e3a8a !important; border-bottom-color: #1e3a8a !important; }

    /* Premium Card Design */
    .content-card {
        background: white;
        padding: 25px;
        border-radius: 25px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.04);
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }

    /* Social Media Icons */
    .social-footer {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 30px;
        padding-bottom: 30px;
    }
    .social-icon {
        background: white;
        width: 45px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        text-decoration: none;
        font-size: 20px;
    }

    /* Style Button & Input */
    div.stButton > button {
        border-radius: 15px;
        background: #1e3a8a;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stTextInput input { border-radius: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. KONEKSI SUPABASE ---
try:
    URL = st.secrets["SUPABASE_URL"]
    KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(URL, KEY)
except:
    st.error("Koneksi Database Gagal.")
    st.stop()

# --- 4. LOGIKA LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div class="app-header"><h1>JITU PRESISI</h1><p>Digital Financial Monitoring</p></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        em = st.text_input("📧 Email User")
        ps = st.text_input("🔒 Password", type="password")
        if st.button("MASUK SISTEM"):
            res = supabase.table("pegawai").select("*").eq("email", em).eq("password", ps).execute()
            if len(res.data) > 0:
                st.session_state.user_info = res.data[0]
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Login Gagal!")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # --- DASHBOARD BERMENU ---
    u = st.session_state.user_info
    st.markdown(f"""
        <div class="app-header">
            <h2 style="color:white; margin:0;">Halo, {u['nama_lengkap'].split()[0]}!</h2>
            <p style="opacity:0.9;">Puskeu Polri - Presisi</p>
        </div>
    """, unsafe_allow_html=True)

    # MENU TAB (Fitur Aksesoris)
    tab1, tab2, tab3 = st.tabs(["💰 Slip Gaji", "📝 Kuesioner", "🌐 Info"])

    with tab1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        res_p = supabase.table("payroll").select("*").eq("pegawai_id", u['id']).order("created_at", desc=True).limit(1).execute()
        if len(res_p.data) > 0:
            pay = res_p.data[0]
            st.metric("Total Penerimaan", f"Rp {int(pay['total_diterima']):,}")
            st.write(f"Gaji Pokok: Rp {int(pay['nominal_gaji_pokok']):,}")
            st.write(f"Tukin: Rp {int(pay['nominal_tukin_cair']):,}")
            st.button("📄 DOWNLOAD PDF")
        else:
            st.info("Data gaji bulan ini belum diinput.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Kuesioner Kepuasan")
        rating = st.select_slider("Seberapa puas Anda dengan aplikasi ini?", options=["Buruk", "Cukup", "Baik", "Sangat Baik"])
        feedback = st.text_area("Saran dan Masukan untuk Puskeu:")
        if st.button("Kirim Masukan"):
            st.success("Terima kasih! Masukan Anda telah terkirim ke sistem.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.write("**Tentang JITU PRESISI**")
        st.write("Aplikasi ini merupakan inisiatif digital untuk transparansi pembayaran tunjangan kinerja.")
        st.write(f"**NIP:** {u['nip']}")
        st.write(f"**Jabatan:** {u['jabatan']}")
        st.markdown('</div>', unsafe_allow_html=True)

    # FOOTER MEDIA SOSIAL
    st.markdown("""
        <div class="social-footer">
            <a href="https://instagram.com/puskeupolri" class="social-icon">📸</a>
            <a href="https://youtube.com" class="social-icon">📺</a>
            <a href="https://puskeu.polri.go.id" class="social-icon">🌐</a>
        </div>
        <p style="text-align:center; color:#94a3b8; font-size:12px;">© 2026 Puskeu Presisi. Created by Yusuf Hambali</p>
    """, unsafe_allow_html=True)

    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
