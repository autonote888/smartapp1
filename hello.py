import streamlit as st
from supabase import create_client, Client
from fpdf import FPDF

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="JITU PRESISI", page_icon="💰", layout="centered")

# --- 2. CSS CUSTOM: PREMIUM MOBILE UI ---
st.markdown("""
    <style>
    /* Paksa Background Utama */
    .stApp {
        background-color: #f8fafc !important;
    }
    
    /* Sembunyikan Header Bawaan Streamlit */
    header {visibility: hidden;}
    .block-container { padding-top: 0rem !important; }

    /* Header Melengkung Modern */
    .mobile-header {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        padding: 60px 20px 50px 20px;
        border-radius: 0 0 40px 40px;
        color: white !important;
        text-align: center;
        margin: -20px -20px 30px -20px;
        box-shadow: 0 10px 20px rgba(29, 78, 216, 0.2);
    }
    .mobile-header h1 { color: white !important; font-size: 2rem !important; font-weight: 800 !important; margin-bottom: 5px !important; }
    .mobile-header p { color: #bfdbfe !important; font-size: 0.9rem !important; }

    /* Card Putih Bersih */
    .premium-card {
        background: white;
        padding: 25px;
        border-radius: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #f1f5f9;
    }

    /* Styling Input */
    .stTextInput label { color: #475569 !important; font-weight: 600 !important; }
    .stTextInput input {
        background-color: #f8fafc !important;
        color: #1e293b !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 15px !important;
        padding: 12px !important;
    }

    /* Tombol Biru Solid */
    div.stButton > button {
        width: 100%;
        border-radius: 15px;
        height: 3.5em;
        background-color: #1d4ed8 !important;
        color: white !important;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3);
        transition: 0.3s;
    }
    div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(29, 78, 216, 0.4); }

    /* Dashboard Metrics */
    .metric-box {
        background: #ffffff;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 15px;
        border-left: 6px solid #1d4ed8;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .metric-label { color: #64748b; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; }
    .metric-val { color: #1e293b; font-size: 1.5rem; font-weight: 700; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. KONEKSI SUPABASE ---
try:
    URL = st.secrets["SUPABASE_URL"]
    KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(URL, KEY)
except:
    st.error("Gagal terhubung ke Database. Cek Secrets.")
    st.stop()

# --- 4. FUNGSI PDF ---
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 15, "SLIP GAJI DIGITAL - JITU PRESISI", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 10, f"Nama : {data['nama']}", ln=True)
    pdf.cell(0, 10, f"NIP  : {data['nip']}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, f"Gaji Pokok : Rp {data['gaji']:,}", ln=True)
    pdf.cell(0, 10, f"Tukin      : Rp {data['tukin']:,}", ln=True)
    pdf.cell(0, 15, f"TOTAL PENERIMAAN : Rp {data['total']:,}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- 5. LOGIKA NAVIGASI ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # --- UI LOGIN ---
    st.markdown('<div class="mobile-header"><h1>JITU PRESISI</h1><p>Puskeu Presisi Monitoring</p></div>', unsafe_allow_html=True)
    
    # Bungkus form dalam container putih (Premium Card)
    with st.container():
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        email_in = st.text_input("📧 Email Dinas", placeholder="nama@polri.go.id")
        pass_in = st.text_input("🔒 Password", type="password", placeholder="******")
        st.write("")
        if st.button("MASUK KE SISTEM"):
            res = supabase.table("pegawai").select("*").eq("email", email_in).eq("password", pass_in).execute()
            if len(res.data) > 0:
                st.session_state.user_info = res.data[0]
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Akses Ditolak! Cek ID/Password.")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # --- UI DASHBOARD ---
    if "user_info" in st.session_state:
        u = st.session_state.user_info
        st.markdown(f"""
            <div class="mobile-header">
                <p style="margin:0; opacity:0.8;">Selamat Datang,</p>
                <h2 style="color:white; margin:0; font-size:1.6rem;">{u['nama_lengkap']}</h2>
                <code style="background:rgba(255,255,255,0.2); color:white; padding:2px 8px; border-radius:5px;">NIP: {u['nip']}</code>
            </div>
        """, unsafe_allow_html=True)

        # Ambil Data Payroll
        res_p = supabase.table("payroll").select("*").eq("pegawai_id", u['id']).order("created_at", desc=True).limit(1).execute()
        
        if len(res_p.data) > 0:
            pay = res_p.data[0]
            
            # Kartu Gaji Modern
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Gaji Pokok</div>
                    <div class="metric-val">Rp {int(pay['nominal_gaji_pokok']):,}</div>
                </div>
                <div class="metric-box" style="border-left-color: #60a5fa;">
                    <div class="metric-label">Tunjangan Kinerja</div>
                    <div class="metric-val" style="color:#2563eb;">Rp {int(pay['nominal_tukin_cair']):,}</div>
                </div>
                <div class="metric-box" style="border-left-color: #10b981;">
                    <div class="metric-label">Total Diterima</div>
                    <div class="metric-val" style="color:#059669;">Rp {int(pay['total_diterima']):,}</div>
                </div>
            """, unsafe_allow_html=True)

            # Tombol Cetak
            pdf_bytes = generate_pdf({
                "nama": u['nama_lengkap'], "nip": u['nip'],
                "gaji": int(pay['nominal_gaji_pokok']), "tukin": int(pay['nominal_tukin_cair']),
                "total": int(pay['total_diterima'])
            })
            st.download_button("📄 DOWNLOAD SLIP GAJI", pdf_bytes, f"Slip_{u['nama_lengkap']}.pdf", "application/pdf")
        
        st.write("")
        if st.button("Keluar"):
            st.session_state.logged_in = False
            st.rerun()
