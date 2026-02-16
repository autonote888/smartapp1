import streamlit as st
from supabase import create_client, Client
from fpdf import FPDF
from datetime import datetime

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="JITU PRESISI", page_icon="💰", layout="centered")

# Custom CSS Minimalis Android-Style
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #3b82f6;
        color: white;
        font-weight: bold;
        border: none;
    }
    .metric-container {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #3b82f6;
    }
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: white;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. KONEKSI SUPABASE ---
try:
    URL = st.secrets["SUPABASE_URL"]
    KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(URL, KEY)
except:
    st.error("Konfigurasi Secrets (URL/KEY) belum diatur di Streamlit Cloud.")
    st.stop()

# --- 3. FUNGSI GENERATE PDF ---
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 15, "JITU PRESISI MOBILE - SLIP GAJI", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 10, f"Nama Lengkap : {data['nama']}", ln=True)
    pdf.cell(0, 10, f"NIP           : {data['nip']}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, f"Gaji Pokok    : Rp {data['gaji']:,}", ln=True)
    pdf.cell(0, 10, f"Tunjangan Kinerja : Rp {data['tukin']:,}", ln=True)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 15, f"TOTAL TERIMA  : Rp {data['total']:,}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- 4. LOGIKA LOGIN MANUAL (DARI TABEL PEGAWAI) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #3b82f6;'>JITU PRESISI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>Sistem Login Internal</p>", unsafe_allow_html=True)
    
    with st.container():
        email_user = st.text_input("Email / ID")
        pass_user = st.text_input("Password", type="password")
        
        if st.button("MASUK SEKARANG"):
            # Cek email dan password langsung ke tabel pegawai
            res = supabase.table("pegawai").select("*").eq("email", email_user).eq("password", pass_user).execute()
            
            if len(res.data) > 0:
                st.session_state.logged_in = True
                st.session_state.user_info = res.data[0]
                st.rerun()
            else:
                st.error("ID atau Password salah!")
else:
    # --- 5. DASHBOARD USER ---
    p = st.session_state.user_info
    
    st.markdown(f"### Selamat Datang,")
    st.markdown(f"<h2 style='color: #3b82f6; margin-top:-15px;'>{p['nama_lengkap']}</h2>", unsafe_allow_html=True)
    st.caption(f"NIP: {p['nip']} | {p['jabatan']}")
    st.write("---")

    # Ambil Data Payroll
    res_pay = supabase.table("payroll").select("*").eq("pegawai_id", p['id']).order("created_at", desc=True).limit(1).execute()
    
    if len(res_pay.data) > 0:
        pay = res_pay.data[0]
        
        # Kartu Gaji Android Style
        st.markdown(f"""
        <div class="metric-container">
            <small style='color: #94a3b8;'>Gaji Pokok</small><br>
            <b style='font-size: 20px; color: #f8fafc;'>Rp {int(pay['nominal_gaji_pokok']):,}</b>
        </div>
        <div class="metric-container" style="border-left-color: #60a5fa;">
            <small style='color: #94a3b8;'>Tunjangan Kinerja</small><br>
            <b style='font-size: 20px; color: #60a5fa;'>Rp {int(pay['nominal_tukin_cair']):,}</b>
        </div>
        <div class="metric-container" style="border-left-color: #10b981;">
            <small style='color: #94a3b8;'>Total Diterima</small><br>
            <b style='font-size: 24px; color: #10b981;'>Rp {int(pay['total_diterima']):,}</b>
        </div>
        """, unsafe_allow_html=True)

        # Download PDF
        pdf_payload = {
            "nama": p['nama_lengkap'],
            "nip": p['nip'],
            "gaji": int(pay['nominal_gaji_pokok']),
            "tukin": int(pay['nominal_tukin_cair']),
            "total": int(pay['total_diterima'])
        }
        pdf_bytes = generate_pdf(pdf_payload)
        
        st.download_button(
            label="📄 UNDUH SLIP GAJI (PDF)",
            data=pdf_bytes,
            file_name=f"Slip_Gaji_{p['nama_lengkap'].replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Data gaji belum tersedia untuk akun ini.")

    if st.button("Keluar Sistem"):
        st.session_state.logged_in = False
        st.rerun()
