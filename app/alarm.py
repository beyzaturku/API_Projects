# eşik aşılınca uyarı 

from fetcher import fiyat_getir, yazdir

# ─────────────────────────────────────────────────────
#  Alarm eşiklerini buradan ayarla
#  "ust": bu fiyatın ÜZERİNE çıkarsa uyarı ver
#  "alt": bu fiyatın ALTına düşerse uyarı ver
#  Kullanmak istemediğin eşiği None yap
# ─────────────────────────────────────────────────────
ESIKLER = {
    "bitcoin":  {"ust": 4_000_000, "alt": 2_500_000},
    "ethereum": {"ust":   200_000, "alt":   100_000},
    "solana":   {"ust":    10_000, "alt":     4_000},
}


def alarm_kontrol(veri):
    """
    Fiyatları eşiklerle karşılaştırır.
    Tetiklenen her alarm için uyarı mesajı döner.
    """
    uyarilar = []

    for kripto, bilgi in veri.items():
        fiyat = bilgi.get("try", 0)
        esik  = ESIKLER.get(kripto, {})

        ust = esik.get("ust")
        alt = esik.get("alt")

        if ust and fiyat > ust:
            uyarilar.append({
                "kripto": kripto,
                "tip":    "YUKARI",
                "fiyat":  fiyat,
                "esik":   ust,
                "mesaj":  f"{kripto.upper()} {fiyat:,.0f} TRY — ÜST eşik ({ust:,.0f} TRY) aşıldı! ▲",
            })

        if alt and fiyat < alt:
            uyarilar.append({
                "kripto": kripto,
                "tip":    "ASAGI",
                "fiyat":  fiyat,
                "esik":   alt,
                "mesaj":  f"{kripto.upper()} {fiyat:,.0f} TRY — ALT eşik ({alt:,.0f} TRY) altına düştü! ▼",
            })

    return uyarilar


def uyarilari_yazdir(uyarilar):
    if not uyarilar:
        print("  Aktif alarm yok.")
        return
    print(f"\n{'!'*52}")
    print("  ALARM!")
    print(f"{'!'*52}")
    for u in uyarilar:
        print(f"  {u['mesaj']}")
    print(f"{'!'*52}\n")


if __name__ == "__main__":
    print("Alarm kontrolü yapılıyor...")
    veri = fiyat_getir()
    yazdir(veri)

    uyarilar = alarm_kontrol(veri)
    uyarilari_yazdir(uyarilar)