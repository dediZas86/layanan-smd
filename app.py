import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from fpdf import FPDF
from datetime import datetime
from PIL import Image
import io

st.set_page_config(page_title="Data Potongan Gaji", layout="centered")
st.title("===Data Potongan Gaji===")

karyawan_list = ["Pilih...", "Tambah Karyawan Baru"]

with st.form("form_potongan"):
    nama_kantor = st.text_input("Nama Kantor")
    
    pilih_karyawan = st.selectbox("Nama Karyawan", karyawan_list)
    if pilih_karyawan == "Tambah Karyawan Baru":
        nama_karyawan = st.text_input("Ketik Nama Karyawan Baru")
    else:
        nama_karyawan = st.text_input("Nama Karyawan", value="" if pilih_karyawan=="Pilih..." else pilih_karyawan)
    
    jumlah_hari_kerja = st.number_input("Jumlah Hari Kerja", min_value=0, step=1)
    
    st.subheader("Bon Panjar")
    potongan_bon = st.number_input("Potongan Bon Panjar", min_value=0, step=1000)
    sisa_bon = st.number_input("Sisa Bon Panjar", min_value=0, step=1000)
    
    st.subheader("Kredit Lunak")
    potongan_kredit = st.number_input("Potongan Kredit Lunak", min_value=0, step=1000)
    sisa_kredit = st.number_input("Sisa Kredit Lunak", min_value=0, step=1000)
    
    st.subheader("Kecerobohan")
    potongan_kecerobohan = st.number_input("Potongan Kecerobohan", min_value=0, step=1000)
    sisa_kecerobohan = st.number_input("Sisa Kecerobohan", min_value=0, step=1000)
    
    st.subheader("Bon Prive")
    bon_prive = st.number_input("Bon Prive", min_value=0, step=1000)
    
    st.subheader("Minus")
    minus_tunai = st.number_input("Minus Tunai", min_value=0, step=1000)
    denda_minus = st.number_input("Denda Minus", min_value=0, step=1000)
    
    st.subheader("Tidak Masuk Kerja")
    jumlah_tidak_masuk = st.number_input("Jumlah Hari Karyawan Tidak Masuk Kerja", min_value=0, step=1)
    keterangan_tidak_masuk = st.text_area("Keterangan Tidak masuk Kerja")
    potongan_tidak_masuk = st.number_input("Potongan Tidak Masuk Kerja", min_value=0, step=1000)
    
    st.subheader("Potongan Lainnya")
    nama_potongan_lain = st.text_input("Potongan Lainnya (beri nama/keterangan Potongan)")
    jumlah_potongan_lain = st.number_input("Jumlah Uang yang di Potongan Lainnya", min_value=0, step=1000)
    sisa_potongan_lain = st.number_input("Sisa Potongan Lainnya", min_value=0, step=1000)
    
    st.subheader("Mutasi Karyawan")
    nama_keluar = st.text_input("Nama Karyawan Keluar")
    tgl_keluar = st.date_input("Tanggal Karyawan Keluar")
    nama_baru = st.text_input("Nama Karyawan Baru Masuk")
    tgl_masuk = st.date_input("Tanggal Karyawan Baru Masuk")
    
    st.subheader("Upload Dokumen")
    ktp_baru = st.file_uploader("Upload KTP Karyawan Baru", type=["jpg","jpeg","png","pdf"])
    surat_sakit = st.file_uploader("Upload Surat Keterangan Sakit dari Dokter/Klinik/Puskesmas", type=["jpg","jpeg","png","pdf"])
    
    st.caption("Keterangan: Sebelum kirim Cek Kembali Data yang anda kirimkan")
    submit = st.form_submit_button("Simpan Data", type="primary")

if submit:
    if nama_karyawan == "" or nama_kantor == "" or nama_karyawan == "Pilih...":
        st.error("Nama Kantor & Nama Karyawan wajib diisi!")
    else:
        try:
            nama_ktp = ktp_baru.name if ktp_baru else "-"
            nama_surat = surat_sakit.name if surat_sakit else "-"
            
            total_potongan = potongan_bon + potongan_kredit + potongan_kecerobohan + bon_prive + denda_minus + potongan_tidak_masuk + jumlah_potongan_lain
            
            data_baru = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                nama_kantor, nama_karyawan, jumlah_hari_kerja,
                potongan_bon, sisa_bon,
                potongan_kredit, sisa_kredit, 
                potongan_kecerobohan, sisa_kecerobohan,
                bon_prive, minus_tunai, denda_minus,
                jumlah_tidak_masuk, keterangan_tidak_masuk, potongan_tidak_masuk,
                nama_potongan_lain, jumlah_potongan_lain, sisa_potongan_lain,
                nama_keluar, str(tgl_keluar), 
                nama_baru, str(tgl_masuk), 
                nama_ktp, nama_surat, total_potongan
            ]
            
            # KONEK GOOGLE SHEETS
            scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
            client = gspread.authorize(creds)
            
            SHEET_ID = "1uyYO8BJY_yRwgeAaIQsOhIrzGwz5qkJ7gHuGX4Yc0YY"
            sheet = client.open_by_key(SHEET_ID).sheet1
            
            # Bikin header kalo sheet masih kosong
            if len(sheet.get_all_values()) == 0:
                header = ["Waktu", "Nama Kantor", "Nama Karyawan", "Jumlah Hari Kerja", "Potongan Bon Panjar", "Sisa Bon Panjar", "Potongan Kredit Lunak", "Sisa Kredit Lunak", "Potongan Kecerobohan", "Sisa Kecerobohan", "Bon Prive", "Minus Tunai", "Denda Minus", "Jumlah Hari Karyawan Tidak Masuk Kerja", "Keterangan Tidak Masuk Kerja", "Potongan Tidak Masuk Kerja", "Potongan Lainnya", "Jumlah Potongan Lainnya", "Sisa Potongan Lainnya", "Nama Karyawan Keluar", "Tanggal Keluar", "Nama Karyawan Baru Masuk", "Tanggal Masuk", "File KTP", "File Surat Sakit", "Total Potongan"]
                sheet.append_row(header)
            
            sheet.append_row(data_baru)
            
            st.success("✅ Data berhasil disimpan ke Google Sheets!")
            st.balloons()
            st.write(f"**Nama:** {nama_karyawan} | **Total Potongan:** Rp {total_potongan:,}".replace(",", "."))
            
            # FUNGSI PDF TETEP ADA
            def add_file_to_pdf(pdf_obj, uploaded_file, title):
                if uploaded_file is None:
                    return
                pdf_obj.add_page()
                pdf_obj.set_font("Arial", "B", 14)
                pdf_obj.cell(0, 10, title, 0, 1, "C")
                pdf_obj.ln(5)
                
                file_bytes = uploaded_file.getvalue()
                file_ext = uploaded_file.name.split('.')[-1].lower()
                
                if file_ext in ['jpg', 'jpeg', 'png']:
                    img = Image.open(io.BytesIO(file_bytes))
                    img_path = f"temp_img_{datetime.now().strftime('%H%M%S')}.jpg"
                    img.convert('RGB').save(img_path)
                    pdf_obj.image(img_path, x=10, y=30, w=190)
                    import os
                    os.remove(img_path)
                else:
                    pdf_obj.set_font("Arial", "", 11)
                    pdf_obj.cell(0, 10, f"File terlampir: {uploaded_file.name}", 0, 1)

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "BUKTI POTONGAN GAJI", 0, 1, "C")
            pdf.ln(5)
            pdf.set_font("Arial", "", 11)
            pdf.cell(0, 7, f"Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
            pdf.cell(0, 7, f"Nama Kantor: {nama_kantor}", 0, 1)
            pdf.cell(0, 7, f"Nama Karyawan: {nama_karyawan}", 0, 1)
            pdf.cell(0, 7, f"Jumlah Hari Kerja: {jumlah_hari_kerja} hari", 0, 1)
            pdf.ln(5)
            pdf.cell(0, 7, "Rincian Potongan:", 0, 1)
            pdf.cell(0, 7, f"- Bon Panjar: Rp {potongan_bon:,} | Sisa: Rp {sisa_bon:,}".replace(",", "."), 0, 1)
            pdf.cell(0, 7, f"- Kredit Lunak: Rp {potongan_kredit:,} | Sisa: Rp {sisa_kredit:,}".replace(",", "."), 0, 1)
            pdf.cell(0, 7, f"- Kecerobohan: Rp {potongan_kecerobohan:,} | Sisa: Rp {sisa_kecerobohan:,}".replace(",", "."), 0, 1)
            pdf.cell(0, 7, f"- Bon Prive: Rp {bon_prive:,}".replace(",", "."), 0, 1)
            pdf.cell(0, 7, f"- Minus Tunai: Rp {minus_tunai:,}".replace(",", "."), 0, 1)
            pdf.cell(0, 7, f"- Denda Minus: Rp {denda_minus:,}".replace(",", "."), 0, 1)
            pdf.cell(0, 7, f"- Tidak Masuk {jumlah_tidak_masuk} hari: Rp {potongan_tidak_masuk:,}".replace(",", "."), 0, 1)
            pdf.cell(0, 7, f"- Lainnya {nama_potongan_lain}: Rp {jumlah_potongan_lain:,} | Sisa: Rp {sisa_potongan_lain:,}".replace(",", "."), 0, 1)
            pdf.ln(5)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 7, f"TOTAL POTONGAN: Rp {total_potongan:,}".replace(",", "."), 0, 1)
            pdf.ln(10)
            pdf.set_font("Arial", "", 11)
            pdf.cell(0, 7, "TTD HRD:........................", 0, 1)

            add_file_to_pdf(pdf, ktp_baru, "LAMPIRAN: KTP KARYAWAN BARU")
            add_file_to_pdf(pdf, surat_sakit, "LAMPIRAN: SURAT KETERANGAN SAKIT")

            pdf_file = f"temp_{nama_karyawan}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            pdf.output(pdf_file)
            with open(pdf_file, "rb") as f:
                pdf_output = f.read()
            import os
            os.remove(pdf_file)

            st.download_button(
                label="📄 Download Bukti PDF Lengkap",
                data=pdf_output,
                file_name=f"Bukti_Lengkap_{nama_karyawan}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"❌ Gagal simpan: {e}")
            st.exception(e)
