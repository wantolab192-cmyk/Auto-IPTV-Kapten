import requests
import re
from datetime import datetime

print("Memulai misi penangkapan token...")

# 1. Menyamar sebagai Browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://malaysia-tv.net/'
}

# 2. TARGET: Mencuri token (Contoh dasar)
try:
    response = requests.get('https://malaysia-tv.net/tv3-live/', headers=headers)
    html = response.text
    
    # Mencari token di dalam HTML
    cari_token = re.search(r'token=([A-Za-z0-9_-]+)', html)
    
    if cari_token:
        token_segar = cari_token.group(1)
        print(f"BERHASIL! Token ditangkap: {token_segar[:5]}...")
    else:
        token_segar = "TOKEN_DARURAT_12345"
        print("Gagal mencari token, menggunakan token darurat.")

except Exception as e:
    token_segar = "ERROR_TOKEN"
    print("Koneksi gagal:", e)

# 3. MERAKIT URL ASLI + TOKEN SEGAR
url_video_asli = f"https://b-cdn.net/tv3/master.m3u8?token={token_segar}"

# 4. JURUS REDIRECT HLS (Membuat Playlist Video M3U8)
# Ini adalah trik agar ExoPlayer di Android TV langsung membaca URL aslinya
hls_content = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=3000000,RESOLUTION=1920x1080
{url_video_asli}
"""

# 5. MENYIMPANNYA SEBAGAI FILE VIDEO (.m3u8)
with open("tv3_auto.m3u8", "w", encoding="utf-8") as file:
    file.write(hls_content)

print("Misi Selesai! File tv3_auto.m3u8 berhasil dibuat.")
