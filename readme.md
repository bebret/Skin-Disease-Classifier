# 🩺 Skin Disease Classifier

Aplikasi web untuk klasifikasi penyakit kulit berbasis **Flask** dan **Ultralytics YOLO**.

Aplikasi ini memungkinkan pengguna untuk mengunggah gambar kondisi kulit, lalu sistem akan memberikan hasil prediksi berbasis AI berupa kelas penyakit, tingkat confidence, deskripsi, serta saran penanganan awal.

> ⚠️ **Disclaimer Medis:**  
> Aplikasi ini hanya dibuat untuk tujuan edukasi dan informasi.  
> Hasil prediksi dari AI **bukan diagnosis medis resmi**.  
> Selalu konsultasikan kondisi kulit kepada dokter atau dokter spesialis kulit untuk pemeriksaan dan penanganan yang tepat.

---

## 📌 Fitur

- Upload gambar kondisi kulit melalui tampilan web
- Klasifikasi gambar menggunakan model YOLO `.pt`
- Menampilkan prediksi utama beserta confidence score
- Menampilkan Top 5 hasil prediksi
- Menampilkan deskripsi penyakit dan saran penanganan awal
- Dapat dijalankan secara lokal di komputer sendiri
- Tidak memerlukan Google Colab
- Tidak memerlukan ngrok untuk penggunaan localhost

---

## 🖼️ Tampilan Aplikasi

Aplikasi ini menyediakan beberapa bagian utama:

- Area upload gambar
- Preview gambar yang diunggah
- Tombol analisis gambar
- Hasil prediksi utama
- Deskripsi penyakit
- Saran penanganan awal
- Daftar Top 5 prediksi

