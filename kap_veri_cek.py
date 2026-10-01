"""
Haber Cekici - Google News RSS ile
=====================================
Kurulum (bir kez):
  pip install requests

Kullanim:
  python kap_veri_cek.py
  kap_data.json olusur
"""

import json, time, requests, re
from datetime import datetime

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

SEMBOLLER = {
    'THYAO': 'Turk Hava Yollari THYAO', 'GARAN': 'Garanti Bankasi GARAN',
    'AKBNK': 'Akbank AKBNK', 'ISCTR': 'Is Bankasi ISCTR',
    'EREGL': 'Eregli Demir Celik EREGL', 'BIMAS': 'BIM Magazalar BIMAS',
    'ASELS': 'Aselsan ASELS', 'KCHOL': 'Koc Holding KCHOL',
    'SISE': 'Sise Cam SISE', 'TUPRS': 'Tupras TUPRS',
    'PGSUS': 'Pegasus PGSUS', 'TCELL': 'Turkcell TCELL',
    'FROTO': 'Ford Otosan FROTO', 'TOASO': 'Tofas TOASO',
    'SAHOL': 'Sabanci Holding SAHOL', 'ARCLK': 'Arcelik ARCLK',
    'VESTL': 'Vestel VESTL', 'DOHOL': 'Dogan Holding DOHOL',
    'EKGYO': 'Emlak Konut EKGYO', 'HEKTS': 'Hektas HEKTS',
    'KOZAL': 'Koza Altin KOZAL', 'KOZAA': 'Koza Anadolu KOZAA',
    'PETKM': 'Petkim PETKM', 'TAVHL': 'TAV Havalimanlari TAVHL',
    'TKFEN': 'Tekfen Holding TKFEN', 'ULKER': 'Ulker ULKER',
    'MAVI': 'Mavi Giyim MAVI', 'LOGO': 'Logo Yazilim LOGO',
    'NETAS': 'Netas Telekom NETAS', 'TTKOM': 'Turk Telekom TTKOM',
    'CCOLA': 'Coca Cola Icecek CCOLA', 'AEFES': 'Anadolu Efes AEFES',
    'MGROS': 'Migros MGROS', 'SOKM': 'Sok Marketler SOKM',
    'OYAKC': 'Oyak Cimento OYAKC', 'CIMSA': 'Cimsa CIMSA',
    'BRSAN': 'Borcelik BRSAN', 'KRDMD': 'Kardemir KRDMD',
    'ALARK': 'Alarko Holding ALARK', 'ENKAI': 'Enka Insaat ENKAI',
    'YKBNK': 'Yapi Kredi Bankasi YKBNK', 'HALKB': 'Halkbank HALKB',
    'VAKBN': 'Vakifbank VAKBN', 'TSKB': 'TSKB', 'QNBFB': 'QNB Finansbank QNBFB',
    'AKSEN': 'Aksa Enerji AKSEN', 'ZOREN': 'Zorlu Enerji ZOREN',
    'ODAS': 'Odas Elektrik ODAS', 'ISGYO': 'Is GYO ISGYO',
    'TRGYO': 'Torunlar GYO TRGYO', 'GUBRF': 'Gubre Fabrikalari GUBRF',
    'AGHOL': 'AG Anadolu Grubu AGHOL', 'OTKAR': 'Otokar OTKAR',
    'VESBE': 'Vestel Beyaz Esya VESBE', 'ASUZU': 'Anadolu Isuzu ASUZU',
    'DOAS': 'Dogus Otomotiv DOAS', 'TTRAK': 'Turk Traktor TTRAK',
    'KORDS': 'Kordsa KORDS', 'GOODY': 'Goodyear GOODY',
    'ANSGR': 'Anadolu Sigorta ANSGR', 'AKGRT': 'Aksigorta AKGRT',
    'TURSG': 'Turkiye Sigorta TURSG', 'ISMEN': 'Is Yatirim ISMEN',
    'SELEC': 'Selcuk Ecza SELEC', 'INDES': 'Indeks Bilgisayar INDES',
    'KAREL': 'Karel Elektronik KAREL', 'GLYHO': 'Global Yatirim GLYHO',
    'FENER': 'Fenerbahce SK FENER', 'GSRAY': 'Galatasaray SK GSRAY',
    'BJKAS': 'Besiktas SK BJKAS', 'TSPOR': 'Trabzonspor TSPOR',
    'CEMTS': 'Cementas CEMTS', 'DYOBY': 'DYO Boya DYOBY',
    'KLNMA': 'Kalkinma Bankasi KLNMA', 'HLGYO': 'Halk GYO HLGYO',
    'BERA': 'Bera Holding BERA', 'KARTN': 'Kartonsan KARTN',
    'GESAN': 'Gesa Seramik GESAN', 'IZMDC': 'Izmir Demir Celik IZMDC',
    'ATAGY': 'Ata GYO ATAGY',
}

def google_news_cek(sembol, arama, adet=3):
    try:
        sorgu = requests.utils.quote(arama + ' hisse borsa')
        url = f'https://news.google.com/rss/search?q={sorgu}&hl=tr&gl=TR&ceid=TR:tr'
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            return []

        # RSS XML parse
        items = re.findall(r'<item>(.*?)</item>', res.text, re.DOTALL)
        haberler = []
        for item in items[:adet]:
            baslik = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
            tarih  = re.search(r'<pubDate>(.*?)</pubDate>', item)
            link   = re.search(r'<link/>\s*(.*?)\s*<', item)
            if not link:
                link = re.search(r'<link>(.*?)</link>', item)
            kaynak = re.search(r'<source[^>]*>(.*?)</source>', item)

            if baslik:
                b = re.sub(r'<[^>]+>', '', baslik.group(1)).strip()
                # Kaynak adini basliktan temizle (Google News ekler)
                b = re.sub(r'\s*-\s*[^-]+$', '', b).strip()
                haberler.append({
                    'tarih':  tarih.group(1)[:16] if tarih else '',
                    'baslik': b[:200],
                    'kaynak': kaynak.group(1) if kaynak else '',
                    'link':   link.group(1).strip() if link else ''
                })
        return haberler
    except Exception as e:
        return []

print("MarketPulse - Haber Cekici (Google News)")
print("=" * 40)
print(f"Baslangic: {datetime.now().strftime('%H:%M:%S')}\n")

result = {}
basarili = 0
bos = []

for sym, arama in SEMBOLLER.items():
    haberler = google_news_cek(sym, arama)
    result[sym] = haberler
    if haberler:
        basarili += 1
        print(f"  OK {sym:8s} -> {len(haberler)} haber | {haberler[0]['baslik'][:55]}")
    else:
        bos.append(sym)
        print(f"  -- {sym:8s} -> haber yok")
    time.sleep(0.5)

with open('kap_data.json', 'w', encoding='utf-8') as f:
    json.dump({
        'updated_at': datetime.now().isoformat(),
        'data': result
    }, f, ensure_ascii=False, indent=2)

print(f"\nBasarili: {basarili}/{len(SEMBOLLER)}")
if bos:
    print(f"Bos: {', '.join(bos)}")
print("\nkap_data.json olusturuldu!")
