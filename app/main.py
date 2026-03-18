"""
Kripto Takip Sistemi — main.py
─────────────────────────────────────────────────────────
Çalıştırma:
  python main.py              → Tek seferlik tam döngü
  python main.py --izle 60   → Her 60 saniyede bir çalış
  python main.py --rapor     → Sadece rapor + grafik üret
─────────────────────────────────────────────────────────
"""

import argparse
import time
from datetime import datetime

from fetcher import fiyat_getir, csv_kaydet, yazdir
from alarm   import alarm_kontrol, uyarilari_yazdir, ESIKLER
from report  import csv_oku, ozet_hesapla, rapor_yazdir, rapor_dosyaya_kaydet
from chart   import cizgi_grafigi, ozet_grafigi


def tek_dongu():
    """Fiyat çek → kaydet → alarm kontrol → ekrana yaz."""
    veri = fiyat_getir()
    yazdir(veri)
    csv_kaydet(veri)

    uyarilar = alarm_kontrol(veri)
    if uyarilar:
        uyarilari_yazdir(uyarilar)

    return veri


def rapor_ve_grafik():
    """CSV'deki bugünkü veriden rapor ve grafik üretir."""
    satirlar = csv_oku(gun_sayisi=1)
    if not satirlar:
        print("Henüz veri yok. Önce birkaç kez fiyat çek.")
        return

    ozet = ozet_hesapla(satirlar)
    rapor_yazdir(ozet)
    rapor_dosyaya_kaydet(ozet)
    cizgi_grafigi(satirlar)
    ozet_grafigi(ozet)


def izle_modu(aralik_sn=60):
    """Belirli aralıklarla sürekli fiyat çeker."""
    print(f"\nİzleme modu başladı — her {aralik_sn} saniyede bir güncelleniyor.")
    print("Durdurmak için Ctrl+C\n")

    dongu = 0
    try:
        while True:
            dongu += 1
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Döngü #{dongu}")
            tek_dongu()

            # Her 10 döngüde bir otomatik rapor
            if dongu % 10 == 0:
                print("\n--- Otomatik ara rapor ---")
                rapor_ve_grafik()

            time.sleep(aralik_sn)

    except KeyboardInterrupt:
        print("\nİzleme durduruldu.")
        print("Son rapor oluşturuluyor...\n")
        rapor_ve_grafik()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kripto Takip Sistemi")
    parser.add_argument("--izle",  type=int, metavar="SANİYE",
                        help="Sürekli izleme modu (örn: --izle 60)")
    parser.add_argument("--rapor", action="store_true",
                        help="Sadece rapor ve grafik üret")
    args = parser.parse_args()

    if args.rapor:
        rapor_ve_grafik()
    elif args.izle:
        izle_modu(aralik_sn=args.izle)
    else:
        tek_dongu()
        print("\nTam rapor için: python main.py --rapor")
        print("Sürekli izleme için: python main.py --izle 60")