import requests
import re
from datetime import datetime

print("Memulai misi penangkapan token...")

# 1. Menyamar sebagai Browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://malaysia-tv.net/'
}

# 2. TARGET: Mencuri token dari website TV
# (Ini hanya contoh URL penangkap token, kamu harus sesuaikan dengan web aslinya nanti)
try:
    # Ceritanya bot membuka halaman website secara diam-diam
    response = requests.get('https://malaysia-tv.net/tv3-live/', headers=headers)
    html = response.text
    
    # 3. MENCARI TOKEN MENGGUNAKAN REGEX (Sandi Pola)
    # Ini mencari teks seperti: token=aBcD123...
    cari_token = re.search(r'token=([A-Za-z0-9_-]+)', html)
    
    if cari_token:
        token_segar = cari_token.group(1)
        print(f"BERHASIL! Token ditangkap: {token_segar[:5]}...")
    else:
        # Jika gagal mencari, gunakan token darurat/dummy untuk contoh
        token_segar = "TOKEN_DARURAT_12345"
        print("Gagal mencari token, menggunakan token darurat.")

except Exception as e:
    token_segar = "ERROR_TOKEN"
    print("Koneksi gagal:", e)

# 4. MERAKIT FILE PLAYLIST.M3U
waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

m3u_content = f"""#EXTM3U x-tvg-url="https://epg.provider.com/epg.xml"
# Update Terakhir: {waktu_sekarang}

#EXTINF:-1 tvg-id="TV3" tvg-logo="https://logo.com/tv3.png" group-title="TV Malaysia", TV3 (Auto-Token)
https://b-cdn.net/tv3/master.m3u8?token={token_segar}

#EXTINF:-1 tvg-id="TV1" tvg-logo="https://logo.com/tv1.png" group-title="TV Malaysia", TV1 RTM
https://d25tgymtnqzu8s.cloudfront.net/main/A0jYR3/master.m3u8
"""

# 5. MENULIS HASILNYA KE FILE
with open("playlist.m3u", "w", encoding="utf-8") as file:
    file.write(m3u_content)

print("Misi Selesai! File playlist.m3u berhasil dibuat/diperbarui.")
