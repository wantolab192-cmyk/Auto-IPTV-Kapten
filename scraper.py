import requests
import re

print("Memulai misi perburuan URL m3u8 rahasia...")

# 1. Menyamar sebagai Browser Komputer
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://malaysia-tv.net/'
}

url_video_asli = "https://gagal.com/token_tidak_ditemukan.m3u8"

try:
    # 2. Menggali kode HTML website target
    response = requests.get('https://malaysia-tv.net/tv3-live/', headers=headers)
    html = response.text
    
    # 3. JURUS REGEX CANGGIH: Cari teks apapun yang diawali 'http', mengandung '.m3u8', dan punya token '?'
    # Biasanya link disembunyikan di dalam tanda kutip (" atau ')
    cari_link = re.search(r'(https?://[^\s\'"]+\.m3u8\?[^\s\'"]+)', html)
    
    if cari_link:
        url_video_asli = cari_link.group(1)
        print(f"BERHASIL! URL Ditemukan: {url_video_asli[:40]}...")
    else:
        # Coba pola kedua (siapa tahu linknya tidak pakai tanda tanya '?')
        cari_link_2 = re.search(r'(https?://[^\s\'"]+\.m3u8)', html)
        if cari_link_2:
            url_video_asli = cari_link_2.group(1)
            print(f"BERHASIL (Pola 2)! URL Ditemukan: {url_video_asli[:40]}...")
        else:
            print("Gagal total. Website ini menyembunyikan linknya di dalam JavaScript tingkat lanjut!")

except Exception as e:
    print("Koneksi gagal:", e)

# 4. MERAKIT FILE PLAYLIST M3U8 (REDIRECT)
hls_content = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=3000000,RESOLUTION=1920x1080
{url_video_asli}
"""

# 5. MENYIMPANNYA
with open("tv3_auto.m3u8", "w", encoding="utf-8") as file:
    file.write(hls_content)

print("File tv3_auto.m3u8 berhasil diperbarui!")
