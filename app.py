import streamlit as st
import pandas as pd
from datetime import datetime, date
from fpdf import FPDF
from PIL import Image
import os
import io

st.set_page_config(page_title="Input Potongan Gaji", layout="centered")
st.title("📝 Form Input Potongan Gaji Karyawan")

file_excel = "Data_Potongan.xlsx"

if not os.path.exists(file_excel):
    cols = ["Waktu", "Nama Kantor", "Nama Karyawan", "Jumlah Hari Kerja",
            "Potongan Bon Panjar", "Sisa Bon Panjar", "Potongan Kredit Lunak", "Sisa Kredit Lunak",
            "Potongan Kecerobohan", "Sisa Kecerobohan", "Bon Prive", "Minus Tunai", "Denda Minus",
            "Jumlah Hari Karyawan Tidak Masuk Kerja", "Keterangan Tidak Masuk Kerja", "Potongan Tidak Masuk Kerja",
            "Potongan Lainnya (beri nama/keterangan Potongan)", "Jumlah Uang yang di Potongan Lainnya", "Sisa Potongan Lainnya",
            "Nama Karyawan Keluar", "Tanggal Karyawan Keluar", "Nama Karyawan Baru Masuk", "Tanggal Karyawan Baru Masuk",
            "File KTP", "File Surat Sakit", "Total Potongan"]
    pd.DataFrame(columns=cols).to_excel(file_excel, index=False)

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
        
        img_w, img_h = img.size
        page_w = 190
        max_h = 250
        
        ratio = min(page_w / img_w, max_h / img_h)
        new_w = img_w * ratio
        new_h = img_h * ratio
        
        x = (210 - new_w) / 2
        
        pdf_obj.image(img_path, x=x, y=30, w=new_w, h=new_h)
        os.remove(img_path)
    else:
        pdf_obj.set_font("Arial", "", 11)
        pdf_obj.cell(0, 10, f"File terlampir: {uploaded_file.name}", 0, 1)

def to_int(val):
    return int(val) if val is not None else 0

with st.form("form_potongan"):
    nama_kantor = st.text_input("Nama Kantor *")
    nama_karyawan = st.text_input("Nama Karyawan *")
    
    # KOSONG DARI AWAL PAKE value=None
    jumlah_hari_kerja = st.number_input("Jumlah Hari Kerja", min_value=0, step=1, value=None, format="%d")
    
    st.subheader("Rincian Potongan")
    col1, col2 = st.columns(2)
    with col1:
        potongan_bon = st.number_input("Potongan Bon Panjar", min_value=0, step=1000, value=None, format="%d")
        sisa_bon = st.number_input("Sisa Bon Panjar", min_value=0, step=1000, value=None, format="%d")
        potongan_kredit = st.number_input("Potongan Kredit Lunak", min_value=0, step=1000, value=None, format="%d")
        sisa_kredit = st.number_input("Sisa Kredit Lunak", min_value=0, step=1000, value=None, format="%d")
    with col2:
        potongan_kecerobohan = st.number_input("Potongan Kecerobohan", min_value=0, step=1000, value=None, format="%d")
        sisa_kecerobohan = st.number_input("Sisa Kecerobohan", min_value=0, step=1000, value=None, format="%d")
        bon_prive = st.number_input("Bon Prive", min_value=0, step=1000, value=None, format="%d")
        minus_tunai = st.number_input("Minus Tunai", min_value=0, step=1000, value=None, format="%d")
    
    denda_minus = st.number_input("Denda Minus", min_value=0, step=1000, value=None, format="%d")
    
    st.subheader("Karyawan Tidak Masuk")
    jumlah_tidak_masuk = st.number_input("Jumlah Hari Tidak Masuk", min_value=0, step=1, value=None, format="%d")
    keterangan_tidak_masuk = st.text_input("Keterangan Tidak Masuk Kerja")
    potongan_tidak_masuk = st.number_input("Potongan Tidak Masuk Kerja", min_value=0, step=1000, value=None, format="%d")
    
    st.subheader("Potongan Lainnya")
    nama_potongan_lain = st.text_input("Nama/Keterangan Potongan Lainnya")
    jumlah_potongan_lain = st.number_input("Jumlah Uang Potongan Lainnya", min_value=0, step=1000, value=None, format="%d")
    sisa_potongan_lain = st.number_input("Sisa Potongan Lainnya", min_value=0, step=1000, value=None, format="%d")
    
    st.subheader("Karyawan Masuk/Keluar")
    nama_keluar = st.text_input("Nama Karyawan Keluar")
    tgl_keluar = st.date_input("Tanggal Karyawan Keluar *", value=None)
    nama_baru = st.text_input("Nama Karyawan Baru Masuk")
    tgl_masuk = st.date_input("Tanggal Karyawan Baru Masuk *", value=None)
    
    st.subheader("Upload Lampiran")
    ktp_baru = st.file_uploader("Upload KTP Karyawan Baru", type=["jpg", "jpeg", "png", "pdf"])
    surat_sakit = st.file_uploader("Upload Surat Keterangan Sakit", type=["jpg", "jpeg", "png", "pdf"])
    
    submit = st.form_submit_button("Simpan Data", use_container_width=True)

if submit:
    error_list = []
    
    if nama_karyawan == "" or nama_kantor == "":
        error_list.append("Nama Kantor & Nama Karyawan wajib diisi!")
    
    if tgl_keluar is None:
        error_list.append("Tanggal Karyawan Keluar wajib dipilih!")
    if tgl_masuk is None:
        error_list.append("Tanggal Karyawan Baru Masuk wajib dipilih!")
    
    if error_list:
        for err in error_list:
            st.error(f"❌ {err}")
        st.stop()
    
    # Convert None jadi 0
    jumlah_hari_kerja = to_int(jumlah_hari_kerja)
    potongan_bon = to_int(potongan_bon)
    sisa_bon = to_int(sisa_bon)
    potongan_kredit = to_int(potongan_kredit)
    sisa_kredit = to_int(sisa_kredit)
    potongan_kecerobohan = to_int(potongan_kecerobohan)
    sisa_kecerobohan = to_int(sisa_kecerobohan)
    bon_prive = to_int(bon_prive)
    minus_tunai = to_int(minus_tunai)
    denda_minus = to_int(denda_minus)
    jumlah_tidak_masuk = to_int(jumlah_tidak_masuk)
    potongan_tidak_masuk = to_int(potongan_tidak_masuk)
    jumlah_potongan_lain = to_int(jumlah_potongan_lain)
    sisa_potongan_lain = to_int(sisa_potongan_lain)
    
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

    st.success("✅ Data berhasil disimpan!")
    st.write(f"**Nama:** {nama_karyawan} | **Total Potongan:** Rp {total_potongan:,}".replace(",", "."))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BUKTI POTONGAN GAJI", 0, 1, "C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, f"Tanggal Input: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
    pdf.cell(0, 7, f"Nama Kantor: {nama_kantor}", 0, 1)
    pdf.cell(0, 7, f"Nama Karyawan: {nama_karyawan}", 0, 1)
    pdf.cell(0, 7, f"Jumlah Hari Kerja: {jumlah_hari_kerja} hari", 0, 1)
    pdf.cell(0, 7, f"Tgl Keluar: {tgl_keluar} | Tgl Masuk: {tgl_masuk}", 0, 1)
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
st.subheader("📊 Download Data untuk HRD Pusat")

df = pd.read_excel(file_excel)

col1, col2 = st.columns(2)
with col1:
    st.download_button(
        label="📥 Download Excel Lengkap",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name=f"Rekap_Potongan_{datetime.now().strftime('%Y%m')}.csv",
        mime="text/csv"
    )

with col2:
    if st.button("📄 Generate PDF Rekap"):
        pdf_rekap = FPDF()
        pdf_rekap.add_page()
        pdf_rekap.set_font("Arial", "B", 16)
        pdf_rekap.cell(0, 10, "REKAPITULASI POTONGAN GAJI", 0, 1, "C")
        pdf_rekap.ln(5)
        pdf_rekap.set_font("Arial", "", 11)
        pdf_rekap.cell(0, 7, f"Periode: {datetime.now().strftime('%B %Y')}", 0, 1)
        pdf_rekap.ln(5)
        
        total_semua = 0
        for i, row in df.iterrows():
            pdf_rekap.cell(0, 6, f"{i+1}. {row['Nama Karyawan']} - {row['Nama Kantor']}", 0, 1)
            pdf_rekap.cell(0, 6, f"   Total Potongan: Rp {row['Total Potongan']:,}".replace(",", "."), 0, 1)
            pdf_rekap.ln(2)
            total_semua += row['Total Potongan']
        
        pdf_rekap.ln(5)
        pdf_rekap.set_font("Arial", "B", 12)
        pdf_rekap.cell(0, 7, f"GRAND TOTAL: Rp {total_semua:,}".replace(",", "."), 0, 1)
        
        pdf_file_rekap = f"rekap_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf_rekap.output(pdf_file_rekap)
        with open(pdf_file_rekap, "rb") as f:
            st.download_button(
                label="Download PDF Rekap",
                data=f.read(),
                file_name=f"Rekap_Potongan_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
        os.remove(pdf_file_rekap)

st.dataframe(df, use_container_width=True)
