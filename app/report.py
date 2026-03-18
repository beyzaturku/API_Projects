# günlük özet raporu üretir

import csv
import os
from datetime import datetime, timedelta
from collections import defaultdict

CSV_DOSYA = "fiyatlar.csv"


def csv_oku(gun_sayisi=1):
    """
    CSV'den son N günün verilerini okur.
    gun_sayisi=1 → bugünün verisi
    gun_sayisi=7 → son 7 günün verisi
    """
    if not os.path.exists(CSV_DOSYA):
        print(f"Hata: '{CSV_DOSYA}' bulunamadı. Önce fetcher.py çalıştır.")
        return []

    sinir = datetime.now() - timedelta(days=gun_sayisi)
    satirlar = []

    with open(CSV_DOSYA, encoding="utf-8") as f:
        okuyucu = csv.DictReader(f)
        for satir in okuyucu:
            try:
                zaman = datetime.strptime(satir["zaman"], "%Y-%m-%d %H:%M:%S")
                if zaman >= sinir:
                    satirlar.append({
                        "zaman":      zaman,
                        "kripto":     satir["kripto"],
                        "fiyat":      float(satir["fiyat_try"]),
                        "degisim":    float(satir["degisim_24s"]),
                    })
            except (ValueError, KeyError):
                continue

    return satirlar


def ozet_hesapla(satirlar):
    """Her kripto için min/max/ortalama/ilk/son fiyatları hesaplar."""
    gruplar = defaultdict(list)
    for satir in satirlar:
        gruplar[satir["kripto"]].append(satir)

    ozet = {}
    for kripto, kayitlar in gruplar.items():
        kayitlar.sort(key=lambda x: x["zaman"])
        fiyatlar = [k["fiyat"] for k in kayitlar]
        ozet[kripto] = {
            "ilk":       fiyatlar[0],
            "son":       fiyatlar[-1],
            "min":       min(fiyatlar),
            "max":       max(fiyatlar),
            "ort":       sum(fiyatlar) / len(fiyatlar),
            "degisim":   kayitlar[-1]["degisim"],
            "kayit_say": len(kayitlar),
        }
    return ozet


def rapor_yazdir(ozet, baslik="Günlük Özet Raporu"):
    bugun = datetime.now().strftime("%d.%m.%Y")
    print(f"\n{'═'*60}")
    print(f"  {baslik}  —  {bugun}")
    print(f"{'═'*60}")

    for kripto, veri in ozet.items():
        degisim_str = f"%{veri['degisim']:+.2f}"
        isaret = "▲" if veri["degisim"] >= 0 else "▼"
        print(f"\n  {kripto.upper()}")
        print(f"    Son fiyat : {veri['son']:>14,.0f} TRY  {isaret} {degisim_str}")
        print(f"    En yüksek : {veri['max']:>14,.0f} TRY")
        print(f"    En düşük  : {veri['min']:>14,.0f} TRY")
        print(f"    Ortalama  : {veri['ort']:>14,.0f} TRY")
        print(f"    Kayıt say.: {veri['kayit_say']}")

    print(f"\n{'═'*60}\n")


def rapor_dosyaya_kaydet(ozet, baslik="Günlük Özet Raporu"):
    """Raporu txt dosyasına da kaydeder."""
    bugun = datetime.now().strftime("%Y-%m-%d")
    dosya = f"rapor_{bugun}.txt"

    with open(dosya, "w", encoding="utf-8") as f:
        f.write(f"{baslik} — {bugun}\n")
        f.write("="*60 + "\n")
        for kripto, veri in ozet.items():
            f.write(f"\n{kripto.upper()}\n")
            f.write(f"  Son fiyat : {veri['son']:,.0f} TRY\n")
            f.write(f"  En yüksek : {veri['max']:,.0f} TRY\n")
            f.write(f"  En düşük  : {veri['min']:,.0f} TRY\n")
            f.write(f"  Ortalama  : {veri['ort']:,.0f} TRY\n")
            f.write(f"  24s değ.  : %{veri['degisim']:+.2f}\n")

    print(f"Rapor '{dosya}' olarak kaydedildi.")
    return dosya


if __name__ == "__main__":
    print("Rapor oluşturuluyor...")
    satirlar = csv_oku(gun_sayisi=1)

    if satirlar:
        ozet = ozet_hesapla(satirlar)
        rapor_yazdir(ozet)
        rapor_dosyaya_kaydet(ozet)
    else:
        print("Yeterli veri yok. Önce birkaç kez fetcher.py çalıştır.")