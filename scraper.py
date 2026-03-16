from playwright.sync_api import sync_playwright

print("Memulai Jurus 2: Melepaskan Chrome Hantu ke medan perang...")

def jalankan_chrome_hantu():
    target_url = "https://malaysia-tv.net/tv3-live/"
    url_rahasia = "https://gagal.com/robot_tidak_menemukan_link.m3u8"

    # Memulai Playwright
    with sync_playwright() as p:
        # Meluncurkan Chrome Hantu (headless=True artinya tanpa layar)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # ALAT PENYADAP JARINGAN (Meniru F12 tab Network)
        def tangkap_jaringan(request):
            nonlocal url_rahasia
            # Jika ada request yang berakhiran .m3u8 dan mengandung token, TANGKAP!
            if ".m3u8" in request.url and "token=" in request.url:
                url_rahasia = request.url
                print(f"\n[BINGO!] Jaring berhasil menangkap URL: {url_rahasia[:60]}...\n")

        # Pasang alat penyadap ke Chrome Hantu
        page.on("request", tangkap_jaringan)

        try:
            print(f"Menyusup ke {target_url}...")
            # Buka halamannya dan biarkan JavaScript mereka bekerja
            page.goto(target_url, wait_until="networkidle", timeout=30000)
            
            print("Menunggu 10 detik agar video berputar di latar belakang...")
            page.wait_for_timeout(10000) 
            
        except Exception as e:
            print(f"Ada sedikit halangan: {e}")
        finally:
            browser.close()

    return url_rahasia

# Eksekusi Jurus 2
url_video_asli = jalankan_chrome_hantu()

# MERAKIT FILE PLAYLIST M3U8 (REDIRECT)
hls_content = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=3000000,RESOLUTION=1920x1080
{url_video_asli}
"""

# MENYIMPANNYA
with open("tv3_auto.m3u8", "w", encoding="utf-8") as file:
    file.write(hls_content)

print("Misi Jurus 2 Selesai! File tv3_auto.m3u8 siap dihidangkan.")
