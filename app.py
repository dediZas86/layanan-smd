import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from PIL import Image
import os
import io

st.set_page_config(page_title="Bukti Potongan PDF", layout="centered")
st.title("📝 Bukti Potongan Gaji - PDF + Rekap")

if "pot_lain_list" not in st.session_state:
    st.session_state.pot_lain_list = []
if "rekap_data" not in st.session_state:
    st.session_state.rekap_data = []

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
    st.markdown("**Wajib diisi:** Nama Kantor, Nama Karyawan, Jumlah Hari Kerja")
    nama_kantor = st.text_input("Nama Kantor *")
    nama_karyawan = st.text_input("Nama Karyawan *")
    jumlah_hari_kerja = st.number_input("Jumlah Hari Kerja *", min_value=0, step=1, value=None, format="%d")

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

    st.subheader("Karyawan Tidak Masuk - Opsional")
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

    st.subheader("Karyawan Masuk/Keluar - Opsional")
    nama_keluar = st.text_input("Nama Karyawan Keluar")
    tgl_keluar = st.date_input("Tanggal Karyawan Keluar", value=None)
    nama_baru = st.text_input("Nama Karyawan Baru Masuk")
    tgl_masuk = st.date_input("Tanggal Karyawan Baru Masuk", value=None)

    st.subheader("Upload Lampiran - Opsional")
    ktp_baru = st.file_uploader("Upload KTP Karyawan Baru", type=["jpg", "jpeg", "png", "pdf"])
    surat_sakit = st.file_uploader("Upload Surat Keterangan Sakit", type=["jpg", "jpeg", "png", "pdf"])

    submit = st.form_submit_button("Generate PDF Bukti", use_container_width=True)

if submit:
    if nama_karyawan.strip() == "" or nama_kantor.strip() == "" or jumlah_hari_kerja is None:
        st.error("❌ Nama Kantor, Nama Karyawan & Jumlah Hari Kerja wajib diisi!")
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

    detail_pot_lain = []
    for pot in st.session_state.pot_lain_list:
        total_potongan += to_int(pot["jumlah"])
        if pot["nama"].strip()!= "":
            detail_pot_lain.append(f"{pot['nama']}:{to_int(pot['jumlah'])}:{to_int(pot['sisa'])}")

    # Simpan ke rekap
    data_baru = {
        "Tanggal": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "Nama Kantor": nama_kantor,
        "Nama Karyawan": nama_karyawan,
        "Hari Kerja": jumlah_hari_kerja,
        "Bon": potongan_bon,
        "Sisa Bon": sisa_bon,
        "Kredit": potongan_kredit,
        "Sisa Kredit": sisa_kredit,
        "Kecerobohan": potongan_kecerobohan,
        "Sisa Kecerobohan": sisa_kecerobohan,
        "Ket Kecerobohan": keterangan_kecerobohan,
        "Bon Prive": bon_prive,
        "Minus": minus_tunai,
        "Denda": denda_minus,
        "Tidak Masuk": jumlah_tidak_masuk,
        "Pot Tidak Masuk": potongan_tidak_masuk,
        "Ket Tidak Masuk": keterangan_tidak_masuk,
        "Pot Lain 1": f"{nama_potongan_lain}:{jumlah_potongan_lain}:{sisa_potongan_lain}" if nama_potongan_lain else "",
        "Pot Lainnya": "; ".join(detail_pot_lain),
        "Total": total_potongan
    }
    st.session_state.rekap_data.append(data_baru)

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

    if tgl_keluar or tgl_masuk:
        tgl_k = tgl_keluar.strftime('%Y-%m-%d') if tgl_keluar else "-"
        tgl_m = tgl_masuk.strftime('%Y-%m-%d') if tgl_masuk else "-"
        pdf.cell(0, 7, f"Tgl Keluar: {tgl_k} | Tgl Masuk: {tgl_m}", 0, 1)
    pdf.ln(5)

    ada_potongan = any([potongan_bon, potongan_kredit, potongan_kecerobohan, bon_prive, minus_tunai, denda_minus, potongan_tidak_masuk, jumlah_potongan_lain])
    if ada_potongan or detail_pot_lain:
        pdf.cell(0, 7, "Rincian Potongan:", 0, 1)
        if potongan_bon > 0:
            pdf.cell(0, 7, f"- Bon Panjar: Rp {potongan_bon:,} | Sisa: Rp {sisa_bon:,}".replace(",", "."), 0, 1)
        if potongan_kredit > 0:
            pdf.cell(0, 7, f"- Kredit Lunak: Rp {potongan_kredit:,} | Sisa: Rp {sisa_kredit:,}".replace(",", "."), 0, 1)
        if potongan_kecerobohan > 0:
            pdf.cell(0, 7, f"- Kecerobohan: Rp {potongan_kecerobohan:,} | Sisa: Rp {sisa_kecerobohan:,}".replace(",", "."), 0, 1)
            if keterangan_kecerobohan.strip()!= "":
                pdf.cell(0, 7, f" Keterangan: {keterangan_kecerobohan}", 0, 1)
        if bon_prive > 0:
            pdf.cell(0, 7, f"- Bon Prive: Rp {bon_prive:,}".replace(",", "."), 0, 1)
        if minus_tunai > 0:
            pdf.cell(0, 7, f"- Minus Tunai: Rp {minus_tunai:,}".replace(",", "."), 0, 1)
        if denda_minus > 0:
            pdf.cell(0, 7, f"- Denda Minus: Rp {denda_minus:,}".replace(",", "."), 0, 1)
        if jumlah_tidak_masuk > 0 and potongan_tidak_masuk > 0:
            pdf.cell(0, 7, f"- Tidak Masuk {jumlah_tidak_masuk} hari: Rp {potongan_tidak_masuk:,}".replace(",", "."), 0, 1)

        if nama_potongan_lain.strip()!= "" and jumlah_potongan_lain > 0:
            pdf.cell(0, 7, f"- Lainnya {nama_potongan_lain}: Rp {jumlah_potongan_lain:,} | Sisa: Rp {sisa_potongan_lain:,}".replace(",", "."), 0, 1)

        for pot in st.session_state.pot_lain_list:
            if pot["nama"].strip()!= "" and to_int(pot["jumlah"]) > 0:
                pdf.cell(0, 7, f"- Lainnya {pot['nama']}: Rp {to_int(pot['jumlah']):,} | Sisa: Rp {to_int(pot['sisa']):,}".replace(",", "."), 0, 1)

        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 7, f"TOTAL POTONGAN: Rp {total_potongan:,}".replace(",", "."), 0, 1)

    pdf.ln(8)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 6, "Mohon karyawan mengirim file PDF ini ke Admin HRD", 0, 1, "C")

    pdf.ln(5)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, "TTD HRD:........................ TTD Karyawan:........................", 0, 1)

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

# Tombol download rekap
if st.session_state.rekap_data:
    st.markdown("---")
    df = pd.DataFrame(st.session_state.rekap_data)

    col1, col2 = st.columns(2)
    with col1:
        excel_file = io.BytesIO()
        df.to_excel(excel_file, index=False, sheet_name="Rekap Potongan")
        excel_file.seek(0)
        st.download_button(
            label="📊 Download Rekap.xlsx",
            data=excel_file,
            file_name=f"Rekap_Potongan_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col2:
        # Generate PDF Rekap Landscape
        pdf_rekap = FPDF(orientation='L', unit='mm', format='A4')
        pdf_rekap.add_page()
        pdf_rekap.set_font("Arial", "B", 14)
        pdf_rekap.cell(0, 10, f"REKAP POTONGAN GAJI - {datetime.now().strftime('%Y-%m-%d')}", 0, 1, "C")
        pdf_rekap.ln(3)

        pdf_rekap.set_font("Arial", "", 7)
        col_widths = [25, 30, 30, 15, 15, 15, 15, 15, 15, 15, 25, 15, 15, 15, 15, 15, 25, 30, 20]
        headers = ["Tanggal", "Kantor", "Karyawan", "H.Kerja", "Bon", "S.Bon", "Kredit", "S.Kredit",
                   "Kecerobohan", "S.Kecerobohan", "Ket Kecerobohan", "Bon Prive", "Minus", "Denda",
                   "Tdk Masuk", "Pot Tdk Masuk", "Ket Tdk Masuk", "Pot Lainnya", "Total"]

        # Header
        for i, header in enumerate(headers):
            pdf_rekap.cell(col_widths[i], 7, header, 1, 0, "C")
        pdf_rekap.ln()

        # Data
        for _, row in df.iterrows():
            pdf_rekap.cell(col_widths[0], 6, str(row["Tanggal"])[:16], 1)
            pdf_rekap.cell(col_widths[1], 6, str(row["Nama Kantor"])[:12], 1)
            pdf_rekap.cell(col_widths[2], 6, str(row["Nama Karyawan"])[:12], 1)
            pdf_rekap.cell(col_widths[3], 6, str(row["Hari Kerja"]), 1, 0, "C")
            pdf_rekap.cell(col_widths[4], 6, f"{row['Bon']:,}".replace(",", "."), 1, 0, "R")
            pdf_rekap.cell(col_widths[5], 6, f"{row['Sisa Bon']:,}".replace(",", "."), 1, 0, "R")
            pdf_rekap.cell(col_widths[6], 6, f"{row['Kredit']:,}".replace(",", "."), 1, 0, "R")
            pdf_rekap.cell(col_widths[7], 6, f"{row['Sisa Kredit']:,}".replace(",", "."), 1, 0, "R")
            pdf_rekap.cell(col_widths[8], 6, f"{row['Kecerobohan']:,}".replace(",", "."), 1, 0, "R")
            pdf_rekap.cell(col_widths[9], 6, f"{row['Sisa Kecerobohan']:,}".replace(",", "."), 1, 0, "R")
            pdf_rekap.cell(col_widths[10], 6, str(row["Ket Kecerobohan"])[:15], 1)
            pdf_rekap.cell(col_widths[11], 6, f"{row['Bon Prive']:,}".replace(",", "."), 1, 0, "R")
            pdf_rekap.cell(col_widths[12], 6, f"{row['Minus']:,}".replace(",", "."), 1, 0, "R")
            pdf_rekap.cell(col_widths[13], 6, f"{row['Denda']:,}".replace(",", "."), 1, 0, "R")
            pdf_rekap.cell(col_widths[14], 6, str(row["Tidak Masuk"]), 1, 0, "C")
            pdf_rekap.cell(col_widths[15], 6, f"{row['Pot Tidak Masuk']:,}".replace(",", "."), 1, 0, "R")
            pdf_rekap.cell(col_widths[16], 6, str(row["Ket Tidak Masuk"])[:12], 1)
            pdf_rekap.cell(col_widths[17], 6, str(row["Pot Lainnya"])[:15], 1)
            pdf_rekap.cell(col_widths[18], 6, f"{row['Total']:,}".replace(",", "."), 1, 0, "R")
            pdf_rekap.ln()

        pdf_bytes = pdf_rekap.output(dest='S').encode('latin-1')
        st.download_button(
            label="📄 Download Rekap.pdf",
            data=pdf_bytes,
            file_name=f"Rekap_Potongan_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.caption(f"Total {len(st.session_state.rekap_data)} data karyawan tersimpan di sesi ini")
