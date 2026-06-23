import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os
from PIL import Image
import io

st.set_page_config(page_title="Data Potongan Gaji", layout="centered")
st.title("===Data Potongan Gaji===")

karyawan_list = ["Pilih...", "Tambah Karyawan Baru"]
file_excel = "rekap_potongan.xlsx"

# Bikin file Excel kalo belum ada
if not os.path.exists(file_excel):
    pd.DataFrame(columns=[
        "Waktu", "Nama Kantor", "Nama Karyawan", "Jumlah Hari Kerja",
        "Potongan Bon Panjar", "Sisa Bon Panjar",
        "Potongan Kredit Lunak", "Sisa Kredit Lunak", 
        "Potongan Kecerobohan", "Sisa Kecerobohan",
        "Bon Prive",
        "Minus Tunai", "Denda Minus",
        "Jumlah Hari Karyawan Tidak Masuk Kerja", "Keterangan Tidak Masuk Kerja", "Potongan Tidak Masuk Kerja",
        "Potongan Lainnya (beri nama/keterangan Potongan)", "Jumlah Uang yang di Potongan Lainnya", "Sisa Potongan Lainnya",
        "Nama Karyawan Keluar", "Tanggal Karyawan Keluar", 
        "Nama Karyawan Baru Masuk", "Tanggal Karyawan Baru Masuk", 
        "File KTP", "File Surat Sakit", "Total Potongan"
    ]).to_excel(file_excel, index=False)

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
        nama_ktp = ktp_baru.name if ktp_baru else "-"
        nama_surat = surat_sakit.name if surat_sakit else "-"
        
        total_potongan = potongan_bon + potongan_kredit + potongan_kecerobohan + bon_prive + denda_minus + potongan_tidak_masuk + jumlah_potongan_lain
        
        data_baru = {
            "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nama Kantor": nama_kantor,
            "Nama Karyawan": nama_karyawan,
            "Jumlah Hari Kerja": jumlah_hari_kerja,
            "Potongan Bon Panjar": potongan_bon,
            "Sisa Bon Panjar": sisa_bon,
            "Potongan Kredit Lunak": potongan_kredit,
            "Sisa Kredit Lunak": sisa_kredit,
            "Potongan Kecerobohan": potongan_kecerobohan,
            "Sisa Kecerobohan": sisa_kecerobohan,
            "Bon Prive": bon_prive,
            "Minus Tunai": minus_tunai,
            "Denda Minus": denda_minus,
            "Jumlah Hari Karyawan Tidak Masuk Kerja": jumlah_tidak_masuk,
            "Keterangan Tidak Masuk Kerja": keterangan_tidak_masuk,
            "Potongan Tidak Masuk Kerja": potongan_tidak_masuk,
            "Potongan Lainnya (beri nama/keterangan Potongan)": nama_potongan_lain,
            "Jumlah Uang yang di Potongan Lainnya": jumlah_potongan_lain,
            "Sisa Potongan Lainnya": sisa_potongan_lain,
            "Nama Karyawan Keluar": nama_keluar,
            "Tanggal Karyawan Keluar": tgl_keluar,
            "Nama Karyawan Baru Masuk": nama_baru,
            "Tanggal Karyawan Baru Masuk": tgl_masuk,
            "File KTP": nama_ktp,
            "File Surat Sakit": nama_surat,
            "Total Potongan": total_potongan
        }
        
        df_lama = pd.read_excel(file_excel)
        df_baru = pd.DataFrame([data_baru])
        df_gabung = pd.concat([df_lama, df_baru], ignore_index=True)
        df_gabung.to_excel(file_excel, index=False)

        st.success("✅ Data berhasil disimpan! Cek kembali sebelum kirim ke atasan")
        st.write(f"**Nama:** {nama_karyawan} | **Total Potongan:** Rp {total_potongan:,}".replace(",", "."))

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
                img_path = f"temp_img_{datetime.now().strftime('%H%M%S%f')}.jpg"
                img.convert('RGB').save(img_path)
                pdf_obj.image(img_path, x=10, y=30, w=190)
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

        pdf_file = f"temp_{nama_karyawan}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.pdf"
        pdf.output(pdf_file)
        with open(pdf_file, "rb") as f:
            pdf_output = f.read()
        os.remove(pdf_file)

        st.download_button(
            label="📄 Download Bukti PDF Lengkap",
            data=pdf_output,
            file_name=f"Bukti_Lengkap_{nama_karyawan}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.divider()
st.subheader("📁 Download Semua Data Jadi 1 File")

if os.path.exists(file_excel):
    df_rekap = pd.read_excel(file_excel)
    
    col1, col2 = st.columns(2)
    
    # FIX: PAKE BytesIO BIAR GA ERROR
    with col1:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_rekap.to_excel(writer, index=False, sheet_name='Rekap')
        excel_bytes = output.getvalue()
        
        st.download_button(
            label="📊 Download Excel Lengkap",
            data=excel_bytes,
            file_name=f"Rekap_Potongan_Gaji_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col2:
        pdf_rekap = FPDF()
        pdf_rekap.add_page()
        pdf_rekap.set_font("Arial", "B", 16)
        pdf_rekap.cell(0, 10, "REKAP POTONGAN GAJI", 0, 1, "C")
        pdf_rekap.set_font("Arial", "", 10)
        pdf_rekap.cell(0, 7, f"Tanggal Cetak: {datetime.now().strftime('%d-%m-%Y %H:%M')}", 0, 1)
        pdf_rekap.cell(0, 7, f"Total Karyawan: {len(df_rekap)} orang", 0, 1)
        pdf_rekap.ln(5)
        
        total_semua = 0
        for i, row in df_rekap.iterrows():
            pdf_rekap.set_font("Arial", "B", 11)
            pdf_rekap.cell(0, 7, f"{i+1}. {row['Nama Karyawan']} - {row['Nama Kantor']}", 0, 1)
            pdf_rekap.set_font("Arial", "", 10)
            pdf_rekap.cell(0, 6, f"   Hari Kerja: {row['Jumlah Hari Kerja']} hari", 0, 1)
            pdf_rekap.cell(0, 6, f"   Bon Panjar: Rp {row['Potongan Bon Panjar']:,} | Sisa: Rp {row['Sisa Bon Panjar']:,}".replace(",", "."), 0, 1)
            pdf_rekap.cell(0, 6, f"   Kredit Lunak: Rp {row['Potongan Kredit Lunak']:,} | Sisa: Rp {row['Sisa Kredit Lunak']:,}".replace(",", "."), 0, 1)
            pdf_rekap.cell(0, 6, f"   Kecerobohan: Rp {row['Potongan Kecerobohan']:,} | Sisa: Rp {row['Sisa Kecerobohan']:,}".replace(",", "."), 0, 1)
            pdf_rekap.cell(0, 6, f"   Bon Prive: Rp {row['Bon Prive']:,}".replace(",", "."), 0, 1)
            pdf_rekap.cell(0, 6, f"   Denda Minus: Rp {row['Denda Minus']:,}".replace(",", "."), 0, 1)
            pdf_rekap.cell(0, 6, f"   Tidak Masuk: {row['Jumlah Hari Karyawan Tidak Masuk Kerja']} hari - Rp {row['Potongan Tidak Masuk Kerja']:,}".replace(",", "."), 0, 1)
            pdf_rekap.set_font("Arial", "B", 11)
            pdf_rekap.cell(0, 7, f"   >>> TOTAL POTONGAN: Rp {row['Total Potongan']:,}".replace(",", "."), 0, 1)
            pdf_rekap.ln(3)
            total_semua += row['Total Potongan']
        
        pdf_rekap.ln(5)
        pdf_rekap.set_font("Arial", "B", 12)
        pdf_rekap.cell(0, 8, f"GRAND TOTAL SEMUA KARYAWAN: Rp {total_semua:,}".replace(",", "."), 0, 1, "C")
        
        pdf_rekap_file = f"rekap_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.pdf"
        pdf_rekap.output(pdf_rekap_file)
        with open(pdf_rekap_file, "rb") as f:
            pdf_rekap_bytes = f.read()
        os.remove(pdf_rekap_file)
        
        st.download_button(
            label="📄 Download PDF Rekap",
            data=pdf_rekap_bytes,
            file_name=f"Rekap_Semua_Karyawan_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
else:
    st.info("Belum ada data masuk. Isi & Simpan Data dulu")
