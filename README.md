# OKD / Kubernetes YAML Secret Generator

Aplikasi web modern berbasis Docker untuk mengekstrak dan mengonversi daftar environment variable Kubernetes/OKD dari:
```yaml
- name: APP_KEY
    value: xxxxxx
```
menjadi format secretKeyRef:
```yaml
  - name: APP_KEY
    valueFrom:
      secretKeyRef:
        name: apps-data
        key: APP_KEY
```
Lengkap dengan panel daftar nama variabel (seperti pada gambar) dan fitur **1-Click Copy** yang 100% bebas tanda petik ganda (`"..."`).

---

## Cara Menjalankan dengan Docker

### Opsi 1: Menggunakan Docker Compose (Direkomendasikan)
```bash
cd okd-yaml-generator
docker compose up -d --build
```
Akses aplikasi di browser: **`http://localhost:5005`**

Untuk mematikan:
```bash
docker compose down
```

---

### Opsi 2: Menggunakan Docker Standalone
```bash
cd okd-yaml-generator
# Build image
docker build -t okd-yaml-generator .

# Jalankan container
docker run -d -p 5005:5005 --name okd-yaml-app okd-yaml-generator
```
Akses di browser: **`http://localhost:5005`**

---

## Fitur Utama
1. **Input Real-time**: Cukup paste YAML dengan format `- name: xxx 
 value: xxx` atau daftar nama variabel biasa. Tanda petik pembungkus pada value, jika ada, tidak ikut diproses sebagai bagian nilai.
2. **Extracted Names Box**: Menampilkan kumpulan list nama persis seperti di gambar.
3. **Secret Target Name Dinamis**: Ubah nama secret di input bar (default: `apps-data`), seluruh YAML otomatis ter-update.
4. **Secret YAML Full Format**: Mengubah setiap pasangan `name`/`value` menjadi manifest `Secret` bertipe `Opaque`, lengkap dengan metadata, `managedFields`, daftar field dinamis, dan encoding Base64 otomatis.
5. **Namespace Opsional**: Isi namespace pada header bila manifest akan ditujukan ke namespace tertentu.
6. **Bebas Tanda Petik Ganda**: Menggunakan API Clipboard bawaan browser sehingga saat di-paste ke VS Code / text editor langsung bersih dan rapi.
