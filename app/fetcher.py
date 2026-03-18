## anlık fiyat çeker, CSV'ye kaydeder

import requests
import csv
import os
from datetime import datetime

KRIPTO_LISTESI = ["bitcoin", "ethereum", "solana"]
PARA_BIRIMI = "try"
CSV_DOSYA = "fiyatlar.csv"


def fiyat_getir():
    """CoinGecko'dan anlık fiyatları çeker."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(KRIPTO_LISTESI),
        "vs_currencies": PARA_BIRIMI,
        "include_24hr_change": "true",
        "include_24hr_vol": "true",
    }
    yanit = requests.get(url, params=params, timeout=10)
    yanit.raise_for_status()
    return yanit.json()


def csv_kaydet(veri):
    """Çekilen veriyi fiyatlar.csv dosyasına ekler."""
    dosya_var = os.path.exists(CSV_DOSYA)
    zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(CSV_DOSYA, mode="a", newline="", encoding="utf-8") as f:
        yazar = csv.writer(f)
        if not dosya_var:
            yazar.writerow(["zaman", "kripto", "fiyat_try", "degisim_24s", "hacim_24s"])
        for kripto, bilgi in veri.items():
            yazar.writerow([
                zaman,
                kripto,
                bilgi.get("try", 0),
                round(bilgi.get("try_24h_change", 0), 4),
                round(bilgi.get("try_24h_vol", 0), 2),
            ])


def yazdir(veri):
    """Terminale güzel formatlı çıktı verir."""
    print(f"\n{'─'*52}")
    print(f"  Kripto Fiyatları  |  {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"{'─'*52}")
    for kripto, bilgi in veri.items():
        fiyat   = bilgi.get("try", 0)
        degisim = bilgi.get("try_24h_change", 0)
        isaret  = "▲" if degisim >= 0 else "▼"
        print(f"  {kripto.upper():<12} {fiyat:>14,.0f} TRY   {isaret} %{degisim:+.2f}")
    print(f"{'─'*52}\n")


if __name__ == "__main__":
    print("Fiyatlar çekiliyor...")
    veri = fiyat_getir()
    yazdir(veri)
    csv_kaydet(veri)
    print(f"Veriler '{CSV_DOSYA}' dosyasına kaydedildi.")