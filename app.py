import streamlit as st

st.set_page_config(page_title="Layanan Warga Sumedang", layout="centered")

st.title("📋 Form Layanan Warga Sumedang")
st.write("Silakan isi data untuk pengajuan surat")

nama = st.text_input("Nama Lengkap")
nik = st.text_input("NIK")
alamat = st.text_area("Alamat Lengkap")
keperluan = st.selectbox("Jenis Surat", ["Surat Domisili", "SKCK", "Surat Pindah", "Lainnya"])

if st.button("Kirim Data"):
    if nama and nik and alamat:
        st.success(f"Data {nama} berhasil dikirim! Petugas kelurahan akan hubungi Anda.")
    else:
        st.error("Mohon isi semua data dengan lengkap!")
