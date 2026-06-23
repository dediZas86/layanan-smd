import streamlit as st
from datetime import datetime
from fpdf import FPDF
from PIL import Image
import os
import io

st.set_page_config(page_title="Bukti Potongan PDF", layout="centered")
st.title("📝 Bukti Potongan Gaji - PDF Only")

if "pot_lain_list" not in st.session_state:
    st.session_state.pot_lain_list = []

def to_int(val):
    return int(val) if val is not None else 0

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
        pdf_obj.cell(0, 7, f"File terlampir: {uploaded_file.name}", 0, 1)

with st.form("form_pdf"):
    nama_kantor = st.text_input("Nama Kantor *")
    nama_karyawan = st.text_input("Nama Karyawan *")
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
        keterangan_kecerobohan = st.text_input("Keterangan Tambahan Kecerobohan jika ada")
        bon_prive = st.number_input("Bon Prive", min_value=0, step=1000, value=None, format="%d")
        minus_tunai = st.number_input("Minus Tunai", min_value=0, step=1000, value=None, format="%d")
    
    denda_minus = st.number_input("Denda Minus", min_value=0, step=1000, value=None, format="%d")
    
    st.subheader("Karyawan Tidak Masuk")
    jumlah_tidak_masuk = st.number_input("Jumlah Hari Tidak Masuk", min_value=0, step=1, value=None, format="%d")
    keterangan_tidak_masuk = st.text_input("Keterangan Tidak Masuk Kerja")
    potongan_tidak_masuk = st.number_input("Potongan Tidak Masuk Kerja", min_value=0, step=1000, value=None, format="%d")
    
    st.subheader("Potongan Lainnya")
    nama_potongan_lain = st.text_input("Nama/Keterangan Potongan Lainnya 1")
    jumlah_potongan_lain = st.number_input("Jumlah Uang Potongan Lainnya 1", min_value=0, step=1000, value=None, format="%d")
    sisa_potongan_lain = st.number_input("Sisa Potongan Lainnya 1", min_value=0, step=1000, value=None, format="%d")
    
    st.markdown("---")
    st.write("**Tambah Potongan Lainnya Lagi**")
    for i, pot in enumerate(st.session_state.pot_lain_list):
        col1, col2, col3, col4 = st.columns([3,2,2,0.8])
        with col1:
            pot["nama"] = st.text_input(f"Nama Potongan {i+2}", value=pot["nama"], key=f"nama_lain_{i}")
        with col2:
            pot["jumlah"] = st.number_input(f"Jumlah {i+2}", min_value=0, step=1000, value=pot["jumlah"], format="%d", key=f"jumlah_lain_{i}")
        with col3:
            pot["sisa"] = st.number_input(f"Sisa {i+2}", min_value=0, step=1000, value=pot["sisa"], format="%d", key=f"sisa_lain_{i}")
        with col4:
            st.write("")
            if st.form_submit_button("❌", key=f"del_lain_{i}"):
                st.session_state.pot_lain_list.pop(i)
                st.rerun()
    
    if st.form_submit_button("+ Tambah Potongan Lainnya"):
        st.session_state.pot_lain_list.append({"nama": "", "jumlah": None, "sisa": None})
        st.rerun()
    
    st.subheader("Karyawan Masuk/Keluar")
    nama_keluar = st.text_input("Nama Karyawan Keluar")
    tgl_keluar = st.date_input("Tanggal Karyawan Keluar *", value=None)
    nama_baru = st.text_input("Nama Karyawan Baru Masuk")
    tgl_masuk = st.date_input("Tanggal Karyawan Baru Masuk *", value=None)
    
    st.subheader("Upload Lampiran")
    ktp_baru = st.file_uploader("Upload KTP Karyawan Baru", type=["jpg", "jpeg", "png", "pdf"])
    surat_sakit = st.file_uploader("Upload Surat Keterangan Sakit", type=["jpg", "jpeg", "png", "pdf"])
    
    submit = st.form_submit_button("Generate PDF Bukti", use_container_width=True)

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
    
    total_potongan = potongan_bon + potongan_kredit + potongan_kecerobohan + bon_prive + denda_minus + potongan_tidak_masuk + jumlah_potongan_lain
    
    for pot in st.session_state.pot_lain_list:
        total_potongan += to_int(pot["jumlah"])

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
    if keterangan_kecerobohan.strip() != "":
        pdf.cell(0, 7, f"  Keterangan: {keterangan_kecerobohan}", 0, 1)
    pdf.cell(0, 7, f"- Bon Prive: Rp {bon_prive:,}".replace(",", "."), 0, 1)
    pdf.cell(0, 7, f"- Minus Tunai: Rp {minus_tunai:,}".replace(",", "."), 0, 1)
    pdf.cell(0, 7, f"- Denda Minus: Rp {denda_minus:,}".replace(",", "."), 0, 1)
    pdf.cell(0, 7, f"- Tidak Masuk {jumlah_tidak_masuk} hari: Rp {potongan_tidak_masuk:,}".replace(",", "."), 0, 1)
    
    if nama_potongan_lain.strip() != "" and jumlah_potongan_lain > 0:
        pdf.cell(0, 7, f"- Lainnya {nama_potongan_lain}: Rp {jumlah_potongan_lain:,} | Sisa: Rp {sisa_potongan_lain:,}".replace(",", "."), 0, 1)
    
    for pot in st.session_state.pot_lain_list:
        if pot["nama"].strip() != "" and to_int(pot["jumlah"]) > 0:
            pdf.cell(0, 7, f"- Lainnya {pot['nama']}: Rp {to_int(pot['jumlah']):,} | Sisa: Rp {to_int(pot['sisa']):,}".replace(",", "."), 0, 1)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, f"TOTAL POTONGAN: Rp {total_potongan:,}".replace(",", "."), 0, 1)
    pdf.ln(10)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, "TTD HRD:........................    TTD Karyawan:........................", 0, 1)

    add_file_to_pdf(pdf, ktp_baru, "LAMPIRAN: KTP KARYAWAN BARU")
    add_file_to_pdf(pdf, surat_sakit, "LAMPIRAN: SURAT KETERANGAN SAKIT")

    pdf_file = f"Bukti_{nama_karyawan}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(pdf_file)
    with open(pdf_file, "rb") as f:
        pdf_output = f.read()
    os.remove(pdf_file)

    st.success("✅ PDF berhasil dibuat!")
    st.download_button(
        label="📄 Download PDF Bukti",
        data=pdf_output,
        file_name=pdf_file,
        mime="application/pdf",
        use_container_width=True
    )
