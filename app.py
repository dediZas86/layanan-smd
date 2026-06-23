import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from PIL import Image
import os
import io

st.set_page_config(page_title="Bukti Potongan PDF", layout="centered")
st.title("📝 Bukti Potongan Gaji - PDF Only")

if "pot_lain_list" not in st.session_state:
    st.session_state.pot_lain_list = []
if "rekap_list" not in st.session_state:
    st.session_state.rekap_list = []

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

def generate_pdf_bukti(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BUKTI POTONGAN GAJI", 0, 1, "C")
    pdf.ln(5)
    
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, f"Tanggal Input: {data['tanggal']}", 0, 1)
    pdf.cell(0, 7, f"Nama Kantor: {data['kantor']}", 0, 1)
    pdf.cell(0, 7, f"Nama Karyawan: {data['karyawan']}", 0, 1)
    pdf.cell(0, 7, f"Jumlah Hari Kerja: {data['hari_kerja']} hari", 0, 1)
    
    if data.get('tgl_keluar') or data.get('tgl_masuk'):
        tgl_k = data['tgl_keluar'].strftime('%Y-%m-%d') if data.get('tgl_keluar') else "-"
        tgl_m = data['tgl_masuk'].strftime('%Y-%m-%d') if data.get('tgl_masuk') else "-"
        pdf.cell(0, 7, f"Tgl Keluar: {tgl_k} | Tgl Masuk: {tgl_m}", 0, 1)
    pdf.ln(5)
    
    rincian = data['rincian']
    ada_potongan = any([rincian.get('bon',0), rincian.get('kredit',0), rincian.get('kecerobohan',0), 
                       rincian.get('bon_prive',0), rincian.get('minus',0), rincian.get('denda',0), 
                       rincian.get('pot_tdk_masuk',0), rincian.get('pot_lain_1',0)] + [p['jumlah'] for p in rincian.get('pot_lain',[])])
    
    if ada_potongan:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 7, "Rincian Potongan:", 0, 1)
        pdf.set_font("Arial", "", 11)
        
        if rincian.get('bon',0) > 0:
            pdf.cell(0, 6, f"- Bon Panjar: Rp {rincian['bon']:,} | Sisa: Rp {rincian['sisa_bon']:,}".replace(",", "."), 0, 1)
        if rincian.get('kredit',0) > 0:
            pdf.cell(0, 6, f"- Kredit Lunak: Rp {rincian['kredit']:,} | Sisa: Rp {rincian['sisa_kredit']:,}".replace(",", "."), 0, 1)
        if rincian.get('kecerobohan',0) > 0:
            pdf.cell(0, 6, f"- Kecerobohan: Rp {rincian['kecerobohan']:,} | Sisa: Rp {rincian['sisa_kecerobohan']:,}".replace(",", "."), 0, 1)
            if rincian.get('ket_kecerobohan'):
                pdf.cell(0, 6, f"  Keterangan: {rincian['ket_kecerobohan']}", 0, 1)
        if rincian.get('bon_prive',0) > 0:
            pdf.cell(0, 6, f"- Bon Prive: Rp {rincian['bon_prive']:,}".replace(",", "."), 0, 1)
        if rincian.get('minus',0) > 0:
            pdf.cell(0, 6, f"- Minus Tunai: Rp {rincian['minus']:,}".replace(",", "."), 0, 1)
        if rincian.get('denda',0) > 0:
            pdf.cell(0, 6, f"- Denda Minus: Rp {rincian['denda']:,}".replace(",", "."), 0, 1)
        if rincian.get('tdk_masuk_hari',0) > 0 and rincian.get('pot_tdk_masuk',0) > 0:
            pdf.cell(0, 6, f"- Tidak Masuk {rincian['tdk_masuk_hari']} hari: Rp {rincian['pot_tdk_masuk']:,}".replace(",", "."), 0, 1)
        
        if rincian.get('nama_pot_lain_1') and rincian.get('pot_lain_1',0) > 0:
            pdf.cell(0, 6, f"- Lainnya {rincian['nama_pot_lain_1']}: Rp {rincian['pot_lain_1']:,} | Sisa: Rp {rincian['sisa_pot_lain_1']:,}".replace(",", "."), 0, 1)
        
        for pot in rincian.get('pot_lain',[]):
            if pot['nama'].strip() != "" and pot['jumlah'] > 0:
                pdf.cell(0, 6, f"- Lainnya {pot['nama']}: Rp {pot['jumlah']:,} | Sisa: Rp {pot['sisa']:,}".replace(",", "."), 0, 1)
        
        pdf.ln(3)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 7, f"TOTAL POTONGAN: Rp {data['total']:,}".replace(",", "."), 0, 1)
    
    pdf.ln(8)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 6, "Mohon karyawan mengirim file PDF ini ke Admin HRD", 0, 1, "C")
    
    pdf.ln(5)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, "TTD HRD:........................    TTD Karyawan:........................", 0, 1)
    
    add_file_to_pdf(pdf, data.get('ktp_baru'), "LAMPIRAN: KTP KARYAWAN BARU")
    add_file_to_pdf(pdf, data.get('surat_sakit'), "LAMPIRAN: SURAT KETERANGAN SAKIT")
    
    pdf_file = f"temp_{datetime.now().strftime('%H%M%S%f')}.pdf"
    pdf.output(pdf_file)
    with open(pdf_file, "rb") as f:
        pdf_bytes = f.read()
    os.remove(pdf_file)
    return pdf_bytes

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
        detail_pot_lain.append({"nama": pot["nama"], "jumlah": to_int(pot["jumlah"]), "sisa": to_int(pot["sisa"])})
    
    data_bukti = {
        "tanggal": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "kantor": nama_kantor,
        "karyawan": nama_karyawan,
        "hari_kerja": jumlah_hari_kerja,
        "tgl_keluar": tgl_keluar,
        "tgl_masuk": tgl_masuk,
        "ktp_baru": ktp_baru,
        "surat_sakit": surat_sakit,
        "rincian": {
            "bon": potongan_bon, "sisa_bon": sisa_bon,
            "kredit": potongan_kredit, "sisa_kredit": sisa_kredit,
            "kecerobohan": potongan_kecerobohan, "sisa_kecerobohan": sisa_kecerobohan,
            "ket_kecerobohan": keterangan_kecerobohan,
            "bon_prive": bon_prive,
            "minus": minus_tunai,
            "denda": denda_minus,
            "tdk_masuk_hari": jumlah_tidak_masuk,
            "pot_tdk_masuk": potongan_tidak_masuk,
            "nama_pot_lain_1": nama_potongan_lain,
            "pot_lain_1": jumlah_potongan_lain,
            "sisa_pot_lain_1": sisa_potongan_lain,
            "pot_lain": detail_pot_lain
        },
        "total": total_potongan
    }
    
    st.session_state.rekap_list.append(data_bukti)
    pdf_bytes = generate_pdf_bukti(data_bukti)
    
    st.success("✅ PDF berhasil dibuat!")
    st.download_button(
        label="📄 Download PDF Bukti",
        data=pdf_bytes,
        file_name=f"Bukti_{nama_karyawan}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    st.session_state.pot_lain_list = []

# Tombol Rekap PDF
if st.session_state.rekap_list:
    st.markdown("---")
    st.subheader("📊 Rekap Semua Karyawan - Format List")
    
    if st.button("📄 Generate PDF Rekap Semua", use_container_width=True):
        pdf_rekap = FPDF()
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
            pdf_rekap.ln(5)
            
            rincian = data['rincian']
            ada_potongan = any([rincian.get('bon',0), rincian.get('kredit',0), rincian.get('kecerobohan',0), 
                               rincian.get('bon_prive',0), rincian.get('minus',0), rincian.get('denda',0), 
                               rincian.get('pot_tdk_masuk',0), rincian.get('pot_lain_1',0)] + [p['jumlah'] for p in rincian.get('pot_lain',[])])
            
            if ada_potongan:
                pdf_rekap.set_font("Arial", "B", 12)
                pdf_rekap.cell(0, 7, "Rincian Potongan:", 0, 1)
                pdf_rekap.set_font("Arial", "", 11)
                
                if rincian.get('bon',0) > 0:
                    pdf_rekap.cell(0, 6, f"- Bon Panjar: Rp {rincian['bon']:,} | Sisa: Rp {rincian['sisa_bon']:,}".replace(",", "."), 0, 1)
                if rincian.get('kredit',0) > 0:
                    pdf_rekap.cell(0, 6, f"- Kredit Lunak: Rp {rincian['kredit']:,} | Sisa: Rp {rincian['sisa_kredit']:,}".replace(",", "."), 0, 1)
                if rincian.get('kecerobohan',0) > 0:
                    pdf_rekap.cell(0, 6, f"- Kecerobohan: Rp {rincian['kecerobohan']:,} | Sisa: Rp {rincian['sisa_kecerobohan']:,}".replace(",", "."), 0, 1)
                    if rincian.get('ket_kecerobohan'):
                        pdf_rekap.cell(0, 6, f"  Keterangan: {rincian['ket_kecerobohan']}", 0, 1)
                if rincian.get('bon_prive',0) > 0:
                    pdf_rekap.cell(0, 6, f"- Bon Prive: Rp {rincian['bon_prive']:,}".replace(",", "."), 0, 1)
                if rincian.get('minus',0) > 0:
                    pdf_rekap.cell(0, 6, f"- Minus Tunai: Rp {rincian['minus']:,}".replace(",", "."), 0, 1)
                if rincian.get('denda',0) > 0:
                    pdf_rekap.cell(0, 6, f"- Denda Minus: Rp {rincian['denda']:,}".replace(",", "."), 0, 1)
                if rincian.get('tdk_masuk_hari',0) > 0 and rincian.get('pot_tdk_masuk',0) > 0:
                    pdf_rekap.cell(0, 6, f"- Tidak Masuk {rincian['tdk_masuk_hari']} hari: Rp {rincian['pot_tdk_masuk']:,}".replace(",", "."), 0, 1)
                
                if rincian.get('nama_pot_lain_1') and rincian.get('pot_lain_1',0) > 0:
                    pdf_rekap.cell(0, 6, f"- Lainnya {rincian['nama_pot_lain_1']}: Rp {rincian['pot_lain_1']:,} | Sisa: Rp {rincian['sisa_pot_lain_1']:,}".replace(",", "."), 0, 1)
                
                for pot in rincian.get('pot_lain',[]):
                    if pot['nama'].strip() != "" and pot['jumlah'] > 0:
                        pdf_rekap.cell(0, 6, f"- Lainnya {pot['nama']}: Rp {pot['jumlah']:,} | Sisa: Rp {pot['sisa']:,}".replace(",", "."), 0, 1)
                
                pdf_rekap.ln(3)
                pdf_rekap.set_font("Arial", "B", 12)
                pdf_rekap.cell(0, 7, f"TOTAL POTONGAN: Rp {data['total']:,}".replace(",", "."), 0, 1)
            
            pdf_rekap.ln(8)
            pdf_rekap.set_font("Arial", "I", 10)
            pdf_rekap.cell(0, 6, "Mohon karyawan mengirim file PDF ini ke Admin HRD", 0, 1, "C")
            pdf_rekap.ln(5)
            pdf_rekap.set_font("Arial", "", 11)
            pdf_rekap.cell(0, 7, "TTD HRD:........................    TTD Karyawan:........................", 0, 1)
        
        pdf_file = f"rekap_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf_rekap.output(pdf_file)
        with open(pdf_file, "rb") as f:
            pdf_bytes = f.read()
        os.remove(pdf_file)
        
        st.download_button(
            label="⬇️ Download PDF Rekap Semua Karyawan",
            data=pdf_bytes,
            file_name=f"Rekap_Semua_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    st.caption(f"Total {len(st.session_state.rekap_list)} data tersimpan")
