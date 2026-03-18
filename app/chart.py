# grafik oluşturur 

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from report import csv_oku, ozet_hesapla
from collections import defaultdict
from datetime import datetime

RENKLER = {
    "bitcoin":  "#F7931A",
    "ethereum": "#627EEA",
    "solana":   "#9945FF",
}


def veri_hazirla(satirlar):
    """Satırları kripto bazında gruplar, zamana göre sıralar."""
    gruplar = defaultdict(list)
    for satir in satirlar:
        gruplar[satir["kripto"]].append(satir)
    for kripto in gruplar:
        gruplar[kripto].sort(key=lambda x: x["zaman"])
    return gruplar


def cizgi_grafigi(satirlar, kaydet=True):
    """Her kripto için zaman serisi çizgi grafiği."""
    gruplar = veri_hazirla(satirlar)

    fig, eksenler = plt.subplots(len(gruplar), 1,
                                  figsize=(12, 4 * len(gruplar)),
                                  sharex=False)

    if len(gruplar) == 1:
        eksenler = [eksenler]

    fig.suptitle("Fiyat Geçmişi", fontsize=16, fontweight="bold", y=1.01)

    for ax, (kripto, kayitlar) in zip(eksenler, gruplar.items()):
        zamanlar = [k["zaman"] for k in kayitlar]
        fiyatlar = [k["fiyat"] for k in kayitlar]
        renk     = RENKLER.get(kripto, "#888888")

        ax.plot(zamanlar, fiyatlar, color=renk, linewidth=2, label=kripto.upper())
        ax.fill_between(zamanlar, fiyatlar, alpha=0.08, color=renk)

        # Min / Max işaretleri
        min_idx = fiyatlar.index(min(fiyatlar))
        max_idx = fiyatlar.index(max(fiyatlar))
        ax.annotate(f"Min\n{fiyatlar[min_idx]:,.0f}",
                    xy=(zamanlar[min_idx], fiyatlar[min_idx]),
                    xytext=(10, -30), textcoords="offset points",
                    fontsize=8, color=renk,
                    arrowprops=dict(arrowstyle="->", color=renk, lw=0.8))
        ax.annotate(f"Max\n{fiyatlar[max_idx]:,.0f}",
                    xy=(zamanlar[max_idx], fiyatlar[max_idx]),
                    xytext=(10, 10), textcoords="offset points",
                    fontsize=8, color=renk,
                    arrowprops=dict(arrowstyle="->", color=renk, lw=0.8))

        ax.set_title(kripto.upper(), fontsize=13, color=renk)
        ax.set_ylabel("TRY")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m %H:%M"))
        ax.tick_params(axis="x", rotation=30, labelsize=8)
        ax.grid(True, alpha=0.2)
        ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()

    if kaydet:
        dosya = f"grafik_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
        plt.savefig(dosya, dpi=150, bbox_inches="tight")
        print(f"Grafik '{dosya}' olarak kaydedildi.")

    plt.show()


def ozet_grafigi(ozet, kaydet=True):
    """Min/Ortalama/Max karşılaştırma çubuk grafiği."""
    kriptolar = list(ozet.keys())
    x         = range(len(kriptolar))
    genislik  = 0.25

    fig, ax = plt.subplots(figsize=(10, 5))

    minler = [ozet[k]["min"] for k in kriptolar]
    ortlar = [ozet[k]["ort"] for k in kriptolar]
    maxler = [ozet[k]["max"] for k in kriptolar]

    ax.bar([i - genislik for i in x], minler, genislik, label="Min",      color="#ef5350", alpha=0.8)
    ax.bar([i            for i in x], ortlar, genislik, label="Ortalama", color="#42a5f5", alpha=0.8)
    ax.bar([i + genislik for i in x], maxler, genislik, label="Max",      color="#66bb6a", alpha=0.8)

    ax.set_xticks(list(x))
    ax.set_xticklabels([k.upper() for k in kriptolar])
    ax.set_ylabel("TRY")
    ax.set_title("Min / Ortalama / Max Karşılaştırması")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.legend()
    ax.grid(axis="y", alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()

    if kaydet:
        dosya = f"ozet_grafik_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
        plt.savefig(dosya, dpi=150, bbox_inches="tight")
        print(f"Özet grafik '{dosya}' olarak kaydedildi.")

    plt.show()


if __name__ == "__main__":
    print("Grafik oluşturuluyor...")
    satirlar = csv_oku(gun_sayisi=1)

    if not satirlar:
        print("Yeterli veri yok. Önce birkaç kez fetcher.py çalıştır.")
    else:
        ozet = ozet_hesapla(satirlar)
        cizgi_grafigi(satirlar)
        ozet_grafigi(ozet)