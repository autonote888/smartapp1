import streamlit as st
from supabase import create_client, Client
from fpdf import FPDF

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="JITU PRESISI", page_icon="💰", layout="centered")

# --- 2. CSS CUSTOM UNTUK SMARTPHONE UI ---
st.markdown("""
    <style>
    /* Menghilangkan padding bawaan Streamlit agar pas di mobile */
    .block-container { padding: 1rem 1rem !important; }
    
    .main { background-color: #f8fafc; }
    
    /* Header Melengkung Ala App Mobile */
    .mobile-header {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        padding: 30px 20px;
        border-radius: 0 0 30px 30px;
        color: white;
        margin: -60px -20px 20px -20px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Card Gaji Modern */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 6px solid #3b82f6;
    }
    
    .metric-title { color: #64748b; font-size: 0.85rem; font-weight: 600; margin-bottom: 5px; }
    .metric-value { color: #1e293b; font-size: 1.4rem; font-weight: 700; }
    
    /* Input Style */
    .stTextInput > div > div > input {
        border-radius: 15px !important;
        padding: 12px !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* Tombol Style */
    div.stButton > button {
        width: 100%;
        border-radius: 15px;
        height: 3.5em;
        background-color: #3b82f6;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #2563eb; }
    
    /* Logout Button */
    .logout-btn { color: #ef4444; font-size: 0.9rem; text-align: center; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. KONEKSI SUPABASE ---
try:
    URL = st.secrets["SUPABASE_URL"]
    KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(URL, KEY)
except:
    st.error("Konfigurasi Secrets tidak ditemukan.")
    st.stop()

# --- 4. FUNGSI GENERATE PDF ---
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
    pdf.cell(0, 15, f"TOTAL      : Rp {data['total']:,}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- 5. LOGIKA APLIKASI ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # --- LOGIN SCREEN ---
    st.markdown('<div class="mobile-header"><h1>JITU PRESISI</h1><p>Monitoring Gaji Anggota</p></div>', unsafe_allow_html=True)
    
    with st.container():
        email_input = st.text_input("📧 Email / ID", placeholder="Masukkan email dinas")
        pass_input = st.text_input("🔒 Password", type="password", placeholder="Masukkan password")
        
        st.write(" ")
        if st.button("MASUK SEKARANG"):
            try:
                res = supabase.table("pegawai").select("*").eq("email", email_input).eq("password", pass_input).execute()
                if len(res.data) > 0:
                    st.session_state.user_info = res.data[0]
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Email atau Password salah!")
            except Exception as e:
                st.error(f"Error: {e}")
else:
    # --- DASHBOARD SCREEN ---
    if "user_info" in st.session_state:
        p = st.session_state.user_info
        
        # Header Info Profil
        st.markdown(f"""
            <div class="mobile-header">
                <small style="opacity: 0.8;">Selamat Datang,</small>
                <h2 style="margin: 0; font-size: 1.5rem;">{p['nama_lengkap']}</h2>
                <p style="font-size: 0.8rem; margin: 0; opacity: 0.9;">NIP: {p['nip']} | {p['jabatan']}</p>
            </div>
        """, unsafe_allow_html=True)

        # Ambil Data Payroll
        try:
            res_pay = supabase.table("payroll").select("*").eq("pegawai_id", p['id']).order("created_at", desc=True).limit(1).execute()
            
            if len(res_pay.data) > 0:
                pay = res_pay.data[0]
                
                # Kartu-kartu Gaji
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">GAJI POKOK</div>
                        <div class="metric-value">Rp {int(pay['nominal_gaji_pokok']):,}</div>
                    </div>
                    <div class="metric-card" style="border-left-color: #60a5fa;">
                        <div class="metric-title">TUNJANGAN KINERJA (CAIR)</div>
                        <div class="metric-value" style="color: #2563eb;">Rp {int(pay['nominal_tukin_cair']):,}</div>
                    </div>
                    <div class="metric-card" style="border-left-color: #10b981;">
                        <div class="metric-title">TOTAL PENERIMAAN</div>
                        <div class="metric-value" style="color: #059669; font-size: 1.6rem;">Rp {int(pay['total_diterima']):,}</div>
                    </div>
                """, unsafe_allow_html=True)

                # Tombol Download PDF
                pdf_payload = {
                    "nama": p['nama_lengkap'], "nip": p['nip'],
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
                st.warning("Data gaji belum tersedia untuk bulan ini.")
        except:
            st.error("Gagal memuat data.")

        # Tombol Keluar
        st.write("---")
        if st.button("Logout / Keluar"):
            st.session_state.logged_in = False
            st.session_state.user_info = None
            st.rerun()
    else:
        st.session_state.logged_in = False
        st.rerun()
