# Assasin Dork Scanner v2.0

Assasin Dork Scanner v2.0, Google üzerinden özel dork sorguları ile hedef sistemler hakkında bilgi toplayan ve hedef sistemdeki sql ve xss açıklarını test edebilen bir araçtır.

## ℹ️ Özellikler

1. Dork Tarama 

2. SQL Injection Zafiyet Taraması (Çıktılardaki URLlerde SQL açığı arar.)

3. XSS Zafiyet Taraması (Çıktılardaki URLlerde XSS açığı arar.)

4. URL Engelleme

## 🛠️ Kurulum

Python 3.8+ sürümü ve Google Chrome yüklü olmalıdır.

Sisteme uygun ChromeDriver indirilip çalıştığınız klasöre atılmalı veya PATH'e eklenmelidir.

`git clone https://github.com/fy-9/Assasin-Dork-Scanner`

`pip install -r requirements.txt`

## ▶️ Kullanım

**main.py** dosyasını bir klasöre çıkarın. Sonrasında **dorks.txt** ve **cikti.txt** dosyaları oluşturun.,

`python main.py`

## ⚠️ Yasal Uyarı
Bu araç yalnızca **eğitim**, **test**, **siber güvenlik araştırmaları** ve **bilgi amaçlı** geliştirilmiştir. Yetkisiz sistemlere erişim sağlamak, bu aracı kötüye kullanmak yasal olarak suçtur. Tüm sorumluluk kullanıcıya aittir.
