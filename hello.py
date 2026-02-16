import streamlit as st
from supabase import create_client, Client
from fpdf import FPDF
import base64

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

# --- 3. FUNGSI CETAK PDF ---
def generate_slip_pdf(user, payroll):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "PUSKEU POLRI - JITU PRESISI", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 5, "SLIP GAJI & TUNJANGAN KINERJA DIGITAL", ln=True, align="C")
    pdf.line(10, 30, 200, 30)
    pdf.ln(10)
    
    # Data Pegawai
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"NAMA: {user['nama_lengkap']}", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"NRP/NIP: {user['nrp_nip']}", ln=True)
    pdf.cell(0, 10, f"JABATAN: {user['jabatan']}", ln=True)
    pdf.ln(5)
    
    # Rincian Keuangan
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, "RINCIAN", 1)
    pdf.cell(0, 10, "JUMLAH (RP)", 1, ln=True)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(100, 10, "Gaji Pokok", 1)
    pdf.cell(0, 10, f"{payroll['gaji_pokok']:,.0f}", 1, ln=True)
    pdf.cell(100, 10, "Tunjangan Kinerja", 1)
    pdf.cell(0, 10, f"{payroll['jumlah_tunkin']:,.0f}", 1, ln=True)
    
    pdf.set_font("Arial", "B", 12)
    total = payroll['gaji_pokok'] + payroll['jumlah_tunkin']
    pdf.cell(100, 10, "TOTAL PENERIMAAN", 1)
    pdf.cell(0, 10, f"{total:,.0f}", 1, ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

# --- 4. CSS PREMIUM GLASS UI ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #2e1065, #0f172a) !important; background-attachment: fixed; }
    header {visibility: hidden;} footer {visibility: hidden;}
    
    .stTextInput > div > div > input {
        border-radius: 100px !important; background: rgba(255, 255, 255, 0.05) !important;
        border: none !important; color: white !important; height: 50px !important; padding: 0 25px !important;
    }
    
    .card {
        background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(15px);
        border-radius: 25px; padding: 25px; border: 1px solid rgba(255, 255, 255, 0.1);
        color: white; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    div.stButton > button {
        width: 100% !important; border-radius: 100px !important; height: 50px !important;
        background: linear-gradient(90deg, #a5b4fc 0%, #fdba74 100%) !important;
        color: #1e293b !important; font-weight: bold !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. LOGIKA APLIKASI ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # --- UI LOGIN ---
    st.markdown("<div style='text-align:center; margin-bottom:30px;'><h1 style='color:white;'>JITU PRESISI</h1></div>", unsafe_allow_html=True)
    nip_u = st.text_input("NIP", placeholder="NRP / NIP", label_visibility="collapsed")
    pas_u = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
    
    if st.button("Masuk Ke Sistem"):
        if nip_u and pas_u:
            res = supabase.table("pegawai").select("*").eq("email", nip_u).eq("password", pas_u).execute()
            if len(res.data) > 0:
                st.session_state.user_info = res.data[0]
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("NIP atau Password salah!")
else:
    # --- DASHBOARD RINCIAN PENGHASILAN ---
    u = st.session_state.user_info
    
    st.markdown(f"<h3 style='color:white; margin-bottom:0;'>Halo, {u['nama_lengkap']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:rgba(255,255,255,0.6); margin-top:0;'>NRP/NIP: {u['nrp_nip']} | {u['jabatan']}</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    try:
        # Ambil data dari tabel 'tunkin'
        data_uang = supabase.table("tunkin").select("*").eq("nrp_nip", u["nrp_nip"]).execute()
        
        if len(data_uang.data) > 0:
            uang = data_uang.data[0]
            
            # Tampilan Card Rincian
            st.markdown(f"""
                <div class="card">
                    <small style="color:rgba(255,255,255,0.5);">Tunjangan Kinerja (Tunkin)</small>
                    <h2 style="margin:5px 0;">Rp {uang['jumlah_tunkin']:,.0f}</h2>
                    <span style="background:rgba(255,255,255,0.1); padding:2px 10px; border-radius:10px; font-size:12px;">{uang['status_bayar']}</span>
                </div>
                <div class="card">
                    <small style="color:rgba(255,255,255,0.5);">Gaji Pokok</small>
                    <h2 style="margin:5px 0;">Rp {uang['gaji_pokok']:,.0f}</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Persiapan Tombol PDF
            pdf_data = generate_slip_pdf(u, uang)
            st.download_button(
                label="📄 DOWNLOAD SLIP GAJI (PDF)",
                data=pdf_data,
                file_name=f"Slip_Gaji_{u['nrp_nip']}.pdf",
                mime="application/pdf"
            )
            
        else:
            st.warning("Rincian penghasilan belum tersedia di tabel 'tunkin'.")
    except:
        st.error("Gagal menarik data penghasilan. Cek koneksi Supabase.")

    st.write("<br>", unsafe_allow_html=True)
    if st.button("Keluar"):
        st.session_state.logged_in = False
        st.rerun()
