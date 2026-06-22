import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os

st.set_page_config(page_title="Data Potongan Gaji", layout="centered")
st.title("===Data Potongan Gaji===")
st.caption("Keterangan: Sebelum kirim Cek Kembali Data yang anda kirimkan")

karyawan_list = ["Pilih...", "Tambah Karyawan Baru"]
file_excel = "rekap_potongan.xlsx"

# Bikin excel kosong + header kalo belum ada
if not os.path.exists(file_excel):
    pd.DataFrame(columns=[
        "Waktu", "Nama Kantor", "Nama Karyawan", "Jumlah Hari Kerja",
        "Potongan Kredit Lunak", "Sisa Kredit Lunak", 
        "Potongan Kecerobohan", "Sisa Kecerobohan",
        "Potongan Bon Panjar",
        "Minus Tunai", "Denda Minus",
        "Jumlah Hari Tidak Masuk", "Keterangan Tidak Masuk", "Potongan Tidak Masuk",
        "Nama Potongan Lain", "Jumlah Potongan Lain", "Sisa Potongan Lain",
        "Total Potongan", "Nama Karyawan Keluar", "Tanggal Keluar", 
        "Nama Karyawan Baru", "Tanggal Masuk Baru", "File KTP", "File Surat Sakit"
    ]).to_excel(file_excel, index=False)

with st.form("form_potongan"):
    nama_kantor = st.text_input("Nama Kantor")
    
    pilih_karyawan = st.selectbox("Nama Karyawan", karyawan_list)
    if pilih_karyawan == "Tambah Karyawan Baru":
        nama_karyawan = st.text_input("Ketik Nama Karyawan Baru")
    else:
        nama_karyawan = st.text_input("Nama Karyawan", value="" if pilih_karyawan=="Pilih..." else pilih_karyawan)
    
    jumlah_hari_kerja = st.number_input("Jumlah Hari Kerja", min_value=0, step=1)
    
    st.subheader("Kredit Lunak")
    potongan_kredit = st.number_input("Potongan Kredit Lunak", min_value=0, step=1000)
    sisa_kredit = st.number_input("Sisa Kredit Lunak", min_value=0, step=1000)
    
    st.subheader("Kecerobohan")
    potongan_kecerobohan = st.number_input("Potongan Kecerobohan", min_value=0, step=1000)
    sisa_kecerobohan = st.number_input("Sisa Kecerobohan", min_value=0, step=1000)
    
    st.subheader("Bon Panjar")
    potongan_bon = st.number_input("Potongan Bon Panjar", min_value=0, step=1000)
    
    st.subheader("Minus")
    minus_tunai = st.number_input("Minus Tunai", min_value=0, step=1000)
    denda_minus = st.number_input("Denda Minus", min_value=0, step=1000)
    
    st.subheader("Tidak Masuk Kerja")
    jumlah_tidak_masuk = st.number_input("Jumlah Hari Karyawan Tidak Masuk Kerja", min_value=0, step=1)
    keterangan_tidak_masuk = st.text_area("Keterangan Tidak Masuk Kerja")
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
    ktp_baru = st.file_uploader("Upload KTP Karyawan Baru", type=["jpg","png","pdf"])
    surat_sakit = st.file_uploader("Upload Surat Keterangan Sakit dari Dokter/Klinik/Puskesmas", type=["jpg","png","pdf"])
    
    submit = st.form_submit_button("Simpan Data", type="primary")

if submit:
    if nama_karyawan == "" or nama_kantor == "" or nama_karyawan == "Pilih...":
        st.error("Nama Kantor & Nama Karyawan wajib diisi!")
    else:
        nama_ktp = ktp_baru.name if ktp_baru else "-"
        nama_surat = surat_sakit.name if surat_sakit else "-"
        
        total_potongan = potongan_bon + potongan_kredit + potongan_kecerobohan + denda_minus + potongan_tidak_masuk + jumlah_potongan_lain
        
        data_baru = {
            "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nama Kantor": nama_kantor,
            "Nama Karyawan": nama_karyawan,
            "Jumlah Hari Kerja": jumlah_hari_kerja,
            "Potongan Kredit Lunak": potongan_kredit,
            "Sisa Kredit Lunak": sisa_kredit,
            "Potongan Kecerobohan": potongan_kecerobohan,
            "Sisa Kecerobohan": sisa_kecerobohan,
            "Potongan Bon Panjar": potongan_bon,
            "Minus Tunai": minus_tunai,
            "Denda Minus": denda_minus,
            "Jumlah Hari Tidak Masuk": jumlah_tidak_masuk,
            "Keterangan Tidak Masuk": keterangan_tidak_masuk,
            "Potongan Tidak Masuk": potongan_tidak_masuk,
            "Nama Potongan Lain": nama_potongan_lain,
            "Jumlah Potongan Lain": jumlah_potongan_lain,
            "Sisa Potongan Lain": sisa_potongan_lain,
            "Total Potongan": total_potongan,
            "Nama Karyawan Keluar": nama_keluar,
            "Tanggal Keluar": tgl_keluar,
            "Nama Karyawan Baru": nama_baru,
            "Tanggal Masuk Baru": tgl_masuk,
            "File KTP": nama_ktp,
            "File Surat Sakit": nama_surat
        }
        
        # Simpan ke Excel
        df_lama = pd.read_excel(file_excel)
        df_baru = pd.DataFrame([data_baru])
        df_gabung = pd.concat([df_lama, df_baru], ignore_index=True)
        df_gabung.to_excel(file_excel, index=False)

        st.success("✅ Data berhasil disimpan! Cek kembali sebelum kirim ke atasan")
        st.dataframe(df_baru, use_container_width=True)

        # BIKIN PDF - FIX ERROR DOWNLOAD_BUTTON
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
        pdf.cell(0, 7, f"- Kredit Lunak: Rp {potongan_kredit:,}".replace(",", "."), 0, 1)
        pdf.cell(0, 7, f"- Kecerobohan: Rp {potongan_kecerobohan:,}".replace(",", "."), 0, 1)
        pdf.cell(0, 7, f"- Bon Panjar: Rp {potongan_bon:,}".replace(",", "."), 0, 1)
        pdf.cell(0, 7, f"- Denda Minus: Rp {denda_minus:,}".replace(",", "."), 0, 1)
        pdf.cell(0, 7, f"- Tidak Masuk: Rp {potongan_tidak_masuk:,}".replace(",", "."), 0, 1)
        pdf.cell(0, 7, f"- Lainnya: Rp {jumlah_potongan_lain:,}".replace(",", "."), 0, 1)
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 7, f"TOTAL POTONGAN: Rp {total_potongan:,}".replace(",", "."), 0, 1)
        pdf.ln(10)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 7, "TTD HRD:........................", 0, 1)

        # FIX: pake dest="S" + encode latin-1 biar Streamlit mau
        pdf_output = pdf.output(dest="S").encode("latin-1", "ignore")

        st.download_button(
            label="📄 Download Bukti PDF",
            data=pdf_output,
            file_name=f"Bukti_{nama_karyawan}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf"
        )

# REKAP DATA
st.divider()
if st.checkbox("Lihat Rekap Semua Data"):
    if os.path.exists(file_excel):
        df_rekap = pd.read_excel(file_excel)
        st.dataframe(df_rekap, use_container_width=True)
        st.metric("Total Data Masuk", len(df_rekap))
    else:
        st.info("Belum ada data masuk")
