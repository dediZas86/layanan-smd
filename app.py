import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from PIL import Image
import io
import os

st.set_page_config(page_title="Bukti Potongan Gaji", layout="centered")
st.title("📝 Bukti Potongan Gaji - PDF Only")

if "pot_lain_list" not in st.session_state:
    st.session_state.pot_lain_list = []

def to_int(val):
    return int(val) if val is not None else 0

def add_file_to_pdf(pdf, uploaded_file, title):
    if uploaded_file is None:
        return
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, title, 0, 1, "C")
    pdf.ln(5)
    
    file_bytes = uploaded_file.getvalue()
    ext = uploaded_file.name.split('.')[-1].lower()
    
    if ext in ['jpg', 'jpeg', 'png']:
        img_path = f"temp_img_{datetime.now().strftime('%H%M%S%f')}.{ext}"
        with open(img_path, "wb") as f:
            f.write(file_bytes)
        pdf.image(img_path, x=20, w=170)
        os.remove(img_path)
    else:
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 7, f"File: {uploaded_file.name}", 0, 1)

with st.form("form_pdf"):
    st.markdown("**Data Wajib**")
    nama_kantor = st.text_input("Nama Kantor *")
    nama_karyawan = st.text_input("Nama Karyawan *")
    jml_hari_kerja = st.number_input("Jumlah Hari Kerja *", min_value=0, step=1, value=None)

    st.markdown("**Rincian Potongan**")
    pot_bon = st.number_input("Potongan Bon", min_value=0, step=1000, value=None)
    sisa_bon = st.number_input("Sisa Bon", min_value=0, step=1000, value=None)
    pot_kredit = st.number_input("Potongan Kredit", min_value=0, step=1000, value=None)
    sisa_kredit = st.number_input("Sisa Kredit", min_value=0, step=1000, value=None)
    pot_kecerobohan = st.number_input("Potongan Kecerobohan", min_value=0, step=1000, value=None)
    sisa_kecerobohan = st.number_input("Sisa Kecerobohan", min_value=0, step=1000, value=None)
    ket_kecerobohan = st.text_input("Keterangan Kecerobohan")
    pot_bon_prive = st.number_input("Potongan Bon Prive", min_value=0, step=1000, value=None)
    pot_minus = st.number_input("Potongan Minus Tunai", min_value=0, step=1000, value=None)
    denda_minus = st.number_input("Denda Minus", min_value=0, step=1000, value=None)
    tdk_masuk = st.number_input("Tidak Masuk", min_value=0, step=1, value=None)
    pot_tdk_masuk = st.number_input("Potongan Tidak Masuk", min_value=0, step=1000, value=None)

    st.markdown("**Potongan Lainnya - Klik + buat tambah**")
    col1, col2 = st.columns([3,1])
    with col1:
        nama_pot_lain = st.text_input("Nama Potongan Lain")
    with col2:
        jml_pot_lain = st.number_input("Jumlah", min_value=0, step=1000, value=None)
    if st.form_submit_button("+ Tambah Potongan Lain"):
        if nama_pot_lain.strip() != "" and jml_pot_lain and jml_pot_lain > 0:
            st.session_state.pot_lain_list.append({"nama": nama_pot_lain, "jumlah": jml_pot_lain})
            st.rerun()
    
    if st.session_state.pot_lain_list:
        st.write("Potongan lain tersimpan:")
        for i, p in enumerate(st.session_state.pot_lain_list):
            st.write(f"{i+1}. {p['nama']}: Rp {p['jumlah']:,}")

    st.markdown("**Lampiran**")
    ktp_baru = st.file_uploader("Upload KTP Karyawan Baru", type=['jpg','jpeg','png','pdf'])
    surat_sakit = st.file_uploader("Upload Surat Keterangan Sakit", type=['jpg','jpeg','png','pdf'])

    submitted = st.form_submit_button("Generate PDF Bukti", use_container_width=True)

if submitted:
    if not nama_kantor or not nama_karyawan or jml_hari_kerja is None:
        st.error("❌ Nama Kantor, Nama Karyawan & Jumlah Hari Kerja wajib diisi!")
    else:
        total_pot = to_int(pot_bon) + to_int(pot_kredit) + to_int(pot_kecerobohan) + to_int(pot_bon_prive) + to_int(pot_minus) + to_int(denda_minus) + to_int(pot_tdk_masuk)
        for p in st.session_state.pot_lain_list:
            total_pot += to_int(p["jumlah"])

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "BUKTI POTONGAN GAJI", 0, 1, "C")
        pdf.ln(5)

        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 7, f"Tanggal Input: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
        pdf.cell(0, 7, f"Nama Kantor: {nama_kantor}", 0, 1)
        pdf.cell(0, 7, f"Nama Karyawan: {nama_karyawan}", 0, 1)
        pdf.cell(0, 7, f"Jumlah Hari Kerja: {jml_hari_kerja} hari", 0, 1)
        pdf.ln(3)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 7, "Rincian Potongan:", 0, 1)
        pdf.set_font("Arial", "", 11)

        if pot_bon and pot_bon > 0:
            pdf.cell(0, 6, f"- Bon: Rp {pot_bon:,} | Sisa: Rp {to_int(sisa_bon):,}", 0, 1)
        if pot_kredit and pot_kredit > 0:
            pdf.cell(0, 6, f"- Kredit: Rp {pot_kredit:,} | Sisa: Rp {to_int(sisa_kredit):,}", 0, 1)
        if pot_kecerobohan and pot_kecerobohan > 0:
            pdf.cell(0, 6, f"- Kecerobohan: Rp {pot_kecerobohan:,} | Sisa: Rp {to_int(sisa_kecerobohan):,}", 0, 1)
            if ket_kecerobohan.strip():
                pdf.cell(0, 6, f"  Keterangan: {ket_kecerobohan}", 0, 1)
        if pot_bon_prive and pot_bon_prive > 0:
            pdf.cell(0, 6, f"- Bon Prive: Rp {pot_bon_prive:,}", 0, 1)
        if pot_minus and pot_minus > 0:
            pdf.cell(0, 6, f"- Minus Tunai: Rp {pot_minus:,}", 0, 1)
        if denda_minus and denda_minus > 0:
            pdf.cell(0, 6, f"- Denda Minus: Rp {denda_minus:,}", 0, 1)
        if tdk_masuk and tdk_masuk > 0 and pot_tdk_masuk and pot_tdk_masuk > 0:
            pdf.cell(0, 6, f"- Tidak Masuk {tdk_masuk} hari: Rp {pot_tdk_masuk:,}", 0, 1)
        
        for p in st.session_state.pot_lain_list:
            pdf.cell(0, 6, f"- Lainnya {p['nama']}: Rp {p['jumlah']:,} | Sisa: Rp 0", 0, 1)

        pdf.ln(3)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 7, f"TOTAL POTONGAN: Rp {total_pot:,}", 0, 1)

        pdf.ln(8)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 7, "TTD HRD:.......................... TTD Karyawan:..........................", 0, 1)

        add_file_to_pdf(pdf, ktp_baru, "LAMPIRAN: KTP KARYAWAN BARU")
        add_file_to_pdf(pdf, surat_sakit, "LAMPIRAN: SURAT KETERANGAN SAKIT")

        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.success("✅ PDF berhasil dibuat!")
        st.download_button(
            label="📄 Download PDF Bukti",
            data=pdf_output,
            file_name=f"Bukti_{nama_karyawan}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.markdown("---")
st.subheader("📊 Rekap Semua Karyawan - Format List PDF")

if st.session_state.get("rekap_list", []):
    if st.button("📄 Generate PDF Rekap Semua", use_container_width=True):
        pdf_rekap = FPDF(orientation='P', unit='mm', format='A4')
        
        for idx, data in enumerate(st.session_state.rekap_list):
            pdf_rekap.add_page()
            pdf_rekap.set_font("Arial", "B", 16)
            pdf_rekap.cell(0, 10, f"REKAP #{idx+1} - BUKTI POTONGAN GAJI", 0, 1, "C")
            pdf_rekap.ln(5)

            pdf_rekap.set_font("Arial", "", 11)
            pdf_rekap.cell(0, 7, f"Tanggal: {data['tanggal']}", 0, 1)
            pdf_rekap.cell(0, 7, f"Nama Kantor: {data['kantor']}", 0, 1)
            pdf_rekap.cell(0, 7, f"Nama Karyawan: {data['karyawan']}", 0, 1)
            pdf_rekap.cell(0, 7, f"Jumlah Hari Kerja: {data['hari_kerja']} hari", 0, 1)
            pdf_rekap.ln(3)

            pdf_rekap.set_font("Arial", "B", 12)
            pdf_rekap.cell(0, 7, "Rincian Potongan:", 0, 1)
            pdf_rekap.set_font("Arial", "", 11)

            rincian = data['rincian']
            if rincian.get('bon', 0) > 0:
                pdf_rekap.cell(0, 6, f"- Bon: Rp {rincian['bon']:,} | Sisa: Rp {rincian['sisa_bon']:,}", 0, 1)
            if rincian.get('kredit', 0) > 0:
                pdf_rekap.cell(0, 6, f"- Kredit: Rp {rincian['kredit']:,} | Sisa: Rp {rincian['sisa_kredit']:,}", 0, 1)
            if rincian.get('kecerobohan', 0) > 0:
                pdf_rekap.cell(0, 6, f"- Kecerobohan: Rp {rincian['kecerobohan']:,} | Sisa: Rp {rincian['sisa_kecerobohan']:,}", 0, 1)
                if rincian.get('ket_kecerobohan'):
                    pdf_rekap.cell(0, 6, f"  Keterangan: {rincian['ket_kecerobohan']}", 0, 1)
            if rincian.get('bon_prive', 0) > 0:
                pdf_rekap.cell(0, 6, f"- Bon Prive: Rp {rincian['bon_prive']:,}", 0, 1)
            if rincian.get('minus', 0) > 0:
                pdf_rekap.cell(0, 6, f"- Minus Tunai: Rp {rincian['minus']:,}", 0, 1)
            if rincian.get('denda', 0) > 0:
                pdf_rekap.cell(0, 6, f"- Denda Minus: Rp {rincian['denda']:,}", 0, 1)
            if rincian.get('tdk_masuk_hari', 0) > 0 and rincian.get('pot_tdk_masuk', 0) > 0:
                pdf_rekap.cell(0, 6, f"- Tidak Masuk {rincian['tdk_masuk_hari']} hari: Rp {rincian['pot_tdk_masuk']:,}", 0, 1)
            
            for p in rincian.get('pot_lain', []):
                pdf_rekap.cell(0, 6, f"- Lainnya {p['nama']}: Rp {p['jumlah']:,}", 0, 1)

            pdf_rekap.ln(3)
            pdf_rekap.set_font("Arial", "B", 12)
            pdf_rekap.cell(0, 7, f"TOTAL POTONGAN: Rp {data['total']:,}", 0, 1)

            pdf_rekap.ln(8)
            pdf_rekap.set_font("Arial", "", 11)
            pdf_rekap.cell(0, 7, "TTD HRD:.......................... TTD Karyawan:..........................", 0, 1)

        pdf_bytes = pdf_rekap.output(dest='S').encode('latin-1')
        st.download_button(
            label="⬇️ Download PDF Rekap Semua Karyawan",
            data=pdf_bytes,
            file_name=f"Rekap_Semua_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
else:
    st.info("Belum ada data rekap. Generate PDF bukti dulu minimal 1x.")

# Simpan ke rekap_list tiap submit
if submitted and nama_karyawan and nama_kantor and jml_hari_kerja is not None:
    if "rekap_list" not in st.session_state:
        st.session_state.rekap_list = []
    
    rincian_data = {
        'bon': to_int(pot_bon), 'sisa_bon': to_int(sisa_bon),
        'kredit': to_int(pot_kredit), 'sisa_kredit': to_int(sisa_kredit),
        'kecerobohan': to_int(pot_kecerobohan), 'sisa_kecerobohan': to_int(sisa_kecerobohan),
        'ket_kecerobohan': ket_kecerobohan,
        'bon_prive': to_int(pot_bon_prive),
        'minus': to_int(pot_minus), 'denda': to_int(denda_minus),
        'tdk_masuk_hari': to_int(tdk_masuk), 'pot_tdk_masuk': to_int(pot_tdk_masuk),
        'pot_lain': st.session_state.pot_lain_list.copy()
    }
    
    st.session_state.rekap_list.append({
        'tanggal': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'kantor': nama_kantor,
        'karyawan': nama_karyawan,
        'hari_kerja': jml_hari_kerja,
        'rincian': rincian_data,
        'total': total_pot
    })
    st.session_state.pot_lain_list = []
