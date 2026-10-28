@echo off
cd /d "%~dp0"
echo.
echo ========================================
echo   MarketPulse - Veri Guncelleniyor...
echo ========================================
echo.
echo [1/3] BIST fiyat ve hacim verisi cekiliyor...
python bist_veri_cek.py
echo.
echo [2/3] Haberler cekiliyor...
python kap_veri_cek.py
echo.
echo ========================================
echo   Sunucu baslatiliyor...
echo ========================================
echo.
start "" http://localhost:8000/borsa-analiz.html
python sunucu.py
