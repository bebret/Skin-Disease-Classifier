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

---

## 🚀 Quick Start (Windows)

Jika Anda belum memiliki salinan proyek di komputer, clone repo terlebih dahulu (butuh Git):

```powershell
# Contoh: ganti dengan URL repo Anda
git clone https://github.com/your-username/your-repo.git
cd skin-disease-app
```

Jika belum memasang Git di Windows, unduh dan pasang dari https://git-scm.com/download/win

1. Buat virtual environment dan aktifkan:

```powershell
python -m venv venv
venv\\Scripts\\Activate.ps1   # PowerShell
```

2. Instal dependensi:

```powershell
pip install -r requirements.txt
```

3. Letakkan file model `model.pt` di direktori proyek (sama dengan `app.py`).

4. Jalankan aplikasi:

```powershell
python app.py
```

5. Buka browser ke: http://127.0.0.1:5000

---

## 📁 Struktur Proyek

- `app.py` : server Flask + template HTML/JS (UI & endpoint `/predict`).
- `model.pt` : model terlatih (letakkan di root proyek).
- `requirements.txt` : daftar paket Python.
- `Software Engineering/` : materi pendukung (jika ada).

---

## ⚙️ Dependensi

Disediakan di `requirements.txt`:

- `ultralytics`
- `flask`
- `pillow`

Catatan: beberapa instalasi `ultralytics` mungkin memerlukan `torch` terpasang secara eksplisit. Jika Anda ingin memanfaatkan GPU, pasang `torch` sesuai versi CUDA Anda:

```powershell
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

---

## 📡 API

- POST `/predict`
	- Form field: `image` (file)
	- Response: JSON `{ "predictions": {"ClassName": probability, ...} }`

Contoh `curl`:

```bash
curl -X POST -F "image=@/path/to/image.jpg" http://127.0.0.1:5000/predict
```

Contoh respons:

```json
{
	"predictions": {
		"Acne": 0.72,
		"Eczema": 0.12
	}
}
```

---

## 🛠️ Penjelasan Teknis Singkat

- `app.py` memuat model dengan `ultralytics.YOLO(MODEL_PATH)`.
- Untuk inferensi, kode memanggil `model(image, imgsz=416)` dan mengambil `results[0].probs`.
- Frontend adalah HTML yang dirender dari `app.py` (template string). Hasil diproses di JavaScript untuk menampilkan Top-5 dan detail per kelas.

---

## 🧩 Penempatan Model

Pastikan `model.pt` ada di folder yang sama dengan `app.py`. Jika model punya nama atau lokasi berbeda, ubah variabel `MODEL_PATH` di `app.py`.

---

## ❗ Troubleshooting

- Jika aplikasi tidak menemukan model: cek nama file dan path `MODEL_PATH` di `app.py`.
- Jika `ultralytics` error terkait PyTorch: install `torch` versi yang kompatibel.
- Jika ingin akses dari device lain di jaringan lokal, ganti `host="127.0.0.1"` di `app.run()` ke `0.0.0.0` (perhatikan aspek keamanan).

---

## 📚 Pengembangan & Training

Repository ini tidak menyertakan skrip pelatihan. Untuk melatih ulang, gunakan pipeline Ultralytics/YOLO dengan dataset berlabel, hasilkan checkpoint `.pt`, lalu ganti `model.pt`.

---

## 📄 Lisensi & Kontak

- Tambahkan file `LICENSE` jika perlu (mis. MIT/Apache).
- Untuk pertanyaan atau permintaan fitur, tambahkan issues atau hubungi pemilik proyek.

---

Ingin saya tambahkan badge, contoh dataset, atau instruksi pelatihan detil? Beri tahu saya langkah yang Anda inginkan selanjutnya.

