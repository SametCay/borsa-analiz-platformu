"""
BIST Veri Cekici - MarketPulse icin
=====================================
Kullanim:
  1. pip install yfinance  (bir kez yap)
  2. python bist_veri_cek.py
  3. bist_data.json olusacak
  4. Her gun borsa kapandiktan sonra calistir (18:00 sonrasi)
"""

import json, time
from datetime import datetime

try:
    import yfinance as yf
except ImportError:
    print("yfinance kurulu degil:")
    print("  pip install yfinance")
    exit(1)

BIST_SEMBOLLER = [
    'THYAO','GARAN','AKBNK','ISCTR','EREGL','BIMAS','ASELS','KCHOL','SISE','TUPRS',
    'PGSUS','TCELL','FROTO','TOASO','SAHOL','ARCLK','VESTL','DOHOL','EKGYO','HEKTS',
    'KOZAL','KOZAA','PETKM','TAVHL','TKFEN','ULKER','MAVI','LOGO','NETAS','TTKOM',
    'CCOLA','AEFES','MGROS','SOKM','OYAKC','CIMSA','BRSAN','KRDMD','ALARK','ENKAI',
    'YKBNK','HALKB','VAKBN','TSKB','AKSEN','ZOREN','ODAS','ISGYO','TRGYO',
    'GUBRF','AGHOL','OTKAR','VESBE','ASUZU','DOAS','TTRAK','KORDS','GOODY','ANSGR',
    'AKGRT','TURSG','ISMEN','SELEC','INDES','KAREL','GLYHO','FENER','GSRAY','BJKAS',
    'TSPOR','CEMTS','DYOBY','KLNMA','HLGYO','BERA','KARTN','GESAN','IZMDC','ATAGY'
]

def temel_skor(fk, pddd, borcOran, karBuyume):
    """0-100 arasi temel analiz skoru hesapla."""
    skor = 50  # baslangic

    # F/K degerlendirmesi (BIST icin 5-15 ideal)
    if fk and fk > 0:
        if fk < 5:    skor += 15   # cok ucuz
        elif fk < 10: skor += 10   # ucuz
        elif fk < 15: skor += 5    # makul
        elif fk < 25: skor -= 5    # biraz pahali
        else:         skor -= 15   # cok pahali

    # PD/DD degerlendirmesi (1 altı ucuz)
    if pddd and pddd > 0:
        if pddd < 0.8:  skor += 15  # deger altinda
        elif pddd < 1.5: skor += 8  # makul
        elif pddd < 3:   skor -= 5  # pahali
        else:            skor -= 12 # cok pahali

    # Borc orani (dusuk borc iyi)
    if borcOran is not None:
        if borcOran < 0.3:   skor += 10
        elif borcOran < 0.6: skor += 5
        elif borcOran < 1.0: skor -= 5
        else:                skor -= 15

    # Kar buyumesi
    if karBuyume is not None:
        if karBuyume > 20:   skor += 10
        elif karBuyume > 5:  skor += 5
        elif karBuyume < 0:  skor -= 10

    return max(0, min(100, skor))

def temel_yorum(skor):
    if skor >= 75: return 'Degerli Hisse'
    if skor >= 60: return 'Makul Deger'
    if skor >= 45: return 'Nort'
    if skor >= 30: return 'Pahali'
    return 'Cok Pahali'

print("MarketPulse - BIST Veri Cekici (Fiyat + Temel Analiz)")
print("=" * 50)
print(f"Baslangic: {datetime.now().strftime('%H:%M:%S')}")
print(f"Toplam: {len(BIST_SEMBOLLER)} hisse\n")

result = {}
basarili = 0
basarisiz = []

for i, sym in enumerate(BIST_SEMBOLLER):
    yahoo_sym = sym + '.IS'
    try:
        ticker = yf.Ticker(yahoo_sym)

        # Fiyat ve hacim verisi
        hist = ticker.history(period='6mo', interval='1d', auto_adjust=True)
        if hist.empty or len(hist) < 10:
            raise ValueError("Yeterli veri yok")

        closes  = [round(float(v), 4) for v in hist['Close'].dropna().tolist()]
        volumes = [int(v) for v in hist['Volume'].fillna(0).tolist()]

        # Son kapanış = closes[-1], önceki kapanış = closes[-2]
        last_price = closes[-1]
        prev_close = closes[-2] if len(closes) >= 2 else closes[-1]
        change_pct = round((last_price - prev_close) / prev_close * 100, 2) if prev_close > 0 else 0.0

        # Temel analiz verisi
        info = {}
        try:
            info = ticker.info or {}
        except:
            pass

        fk        = info.get('trailingPE') or info.get('forwardPE')
        pddd      = info.get('priceToBook')
        piyasaDeg = info.get('marketCap')
        borcOran  = info.get('debtToEquity')
        karBuyume = info.get('earningsGrowth')
        temttu    = info.get('dividendYield')
        gelirBuy  = info.get('revenueGrowth')
        cariOran  = info.get('currentRatio')
        sektorPE  = info.get('industryPE') or info.get('sectorPE')

        if borcOran: borcOran = borcOran / 100
        if karBuyume: karBuyume = karBuyume * 100
        if temttu: temttu = round(temttu * 100, 2)
        if gelirBuy: gelirBuy = round(gelirBuy * 100, 2)

        tskor = temel_skor(fk, pddd, borcOran, karBuyume)
        tyorum = temel_yorum(tskor)

        temel = {
            'fk':        round(fk, 2) if fk else None,
            'pddd':      round(pddd, 2) if pddd else None,
            'piyasaDeg': piyasaDeg,
            'borcOran':  round(borcOran, 2) if borcOran else None,
            'karBuyume': round(karBuyume, 1) if karBuyume else None,
            'gelirBuy':  gelirBuy,
            'temttu':    temttu,
            'cariOran':  round(cariOran, 2) if cariOran else None,
            'sektorPE':  round(sektorPE, 2) if sektorPE else None,
            'skor':      tskor,
            'yorum':     tyorum,
        }

        # Saatlik veri (gün içi grafik için — son 5 gün)
        hourly = []
        hourly_times = []
        try:
            hist_h = ticker.history(period='5d', interval='1h', auto_adjust=True)
            if not hist_h.empty:
                hourly = [round(float(v), 4) for v in hist_h['Close'].dropna().tolist()]
                hourly_times = [str(t)[:16] for t in hist_h.index]
        except:
            pass

        # Saatlik veri (gün içi grafik için — son 5 gün)
        hourly = []
        hourly_times = []
        try:
            hist_h = ticker.history(period='5d', interval='1h', auto_adjust=True)
            if not hist_h.empty:
                hourly = [round(float(v), 4) for v in hist_h['Close'].dropna().tolist()]
                # UTC+3 (Türkiye saati) olarak kaydet
                import pytz
                tr_tz = pytz.timezone('Europe/Istanbul')
                idx = hist_h.index
                if idx.tzinfo is None:
                    idx = idx.tz_localize('UTC')
                idx_tr = idx.tz_convert(tr_tz)
                hourly_times = idx_tr.strftime('%Y-%m-%d %H:%M').tolist()
        except Exception as e:
            # pytz yoksa UTC olarak kaydet
            try:
                hist_h = ticker.history(period='5d', interval='1h', auto_adjust=True)
                if not hist_h.empty:
                    hourly = [round(float(v), 4) for v in hist_h['Close'].dropna().tolist()]
                    hourly_times = hist_h.index.strftime('%Y-%m-%d %H:%M').tolist()
            except:
                pass

        # Haftalık veri (orta vade — gerçek timeframe)
        weekly = []
        try:
            hist_w = ticker.history(period='2y', interval='1wk', auto_adjust=True)
            if not hist_w.empty:
                weekly = [round(float(v), 4) for v in hist_w['Close'].dropna().tolist()]
        except:
            pass

        # Aylık veri (uzun vade — gerçek timeframe)
        monthly = []
        try:
            hist_m = ticker.history(period='5y', interval='1mo', auto_adjust=True)
            if not hist_m.empty:
                monthly = [round(float(v), 4) for v in hist_m['Close'].dropna().tolist()]
        except:
            pass

        result[sym] = {
            'history':         closes,
            'history_hourly':  hourly,
            'history_hourly_times': hourly_times,
            'history_weekly':  weekly,
            'history_monthly': monthly,
            'volume':          volumes,
            'price':           last_price,
            'prev_close':      prev_close,
            'change':          change_pct,
            'temel':           temel,
        }
        basarili += 1

        fk_str = f"F/K:{fk:.1f}" if fk else "F/K:-"
        pd_str = f"PD/DD:{pddd:.1f}" if pddd else "PD/DD:-"
        print(f"  OK {sym:8s} -> {last_price:>8.2f} TL  (dün:{prev_close:.2f} | {'+' if change_pct>=0 else ''}{change_pct:.2f}%)  {fk_str} Temel:{tskor}/100")

    except Exception as e:
        basarisiz.append(sym)
        print(f"  HATA {sym:8s} -> {e}")

    if (i + 1) % 10 == 0:
        time.sleep(1)

with open('bist_data.json', 'w', encoding='utf-8') as f:
    json.dump({
        'updated_at': datetime.now().isoformat(),
        'data': result
    }, f, ensure_ascii=False, indent=2)

print(f"\n{'='*50}")
print(f"Basarili: {basarili}/{len(BIST_SEMBOLLER)} hisse")
if basarisiz:
    print(f"Basarisiz: {', '.join(basarisiz)}")
print("bist_data.json olusturuldu!")
print("Not: Her gun 18:00 sonrasi calistir.")
