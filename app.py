import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Layanan Warga Sumedang", layout="centered")

st.title("📋 Form Layanan Warga Sumedang")
st.write("Silakan isi data di bawah untuk pengajuan surat")

# Form input
nama = st.text_input("Nama Lengkap")
nik = st.text_input("NIK")
alamat = st.text_area("Alamat Lengkap")
jenis_surat = st.selectbox("Jenis Surat", ["Surat Domisili", "Surat Keterangan Tidak Mampu", "Surat Pengantar RT/RW"])

if st.button("Kirim Data"):
    if nama and nik and alamat:
        # Bikin PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', size=16)
        pdf.cell(200, 10, txt="PEMERINTAH KELURAHAN", ln=True, align='C')
        pdf.cell(200, 10, txt="KECAMATAN SUMEDANG", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', size=14)
        pdf.cell(200, 10, txt=jenis_surat.upper(), ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Yang bertanda tangan di bawah ini menerangkan bahwa:", ln=True)
        pdf.ln(5)
        pdf.cell(200, 10, txt=f"Nama           : {nama}", ln=True)
        pdf.cell(200, 10, txt=f"NIK            : {nik}", ln=True)
        pdf.cell(200, 10, txt=f"Alamat         : {alamat}", ln=True)
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Surat ini dibuat pada tanggal {datetime.date.today().strftime('%d-%m-%Y')}", ln=True)
        pdf.ln(20)
        pdf.cell(200, 10, txt="Petugas Kelurahan", ln=True, align='R')
        
        # Simpen PDF
        filename = f"Surat_{jenis_surat.replace(' ', '_')}_{nama}.pdf"
        pdf.output(filename)
        
        # Tombol download
        with open(filename, "rb") as f:
            st.download_button(
                label="📄 Download Surat PDF",
                data=f,
                file_name=filename,
                mime="application/pdf"
            )
        
        st.success(f"✅ Data {nama} berhasil dibuat! Silakan download PDF di atas.")
    else:
        st.error("⚠️ Nama, NIK, dan Alamat wajib diisi semua ya bang!")

st.markdown("---")
st.caption("Dibuat untuk warga Sumedang 💙")
