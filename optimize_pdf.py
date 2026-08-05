#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zmenší posielateľné PDF prevzorkovaním obrázkov.

    python3 optimize_pdf.py assets/dokumenty/Viktoria-Mikuskova-portfolio.pdf

Chromium vloží do PDF obrázky v pôvodnej veľkosti, takže portfólio vyšlo cez
11 MB. To je nad hranicou, ktorú znesie e-mailová príloha: väčšie sa buď
neodošle, alebo skončí v spame, a práve ako príloha k prihláške sa toto PDF
posiela. Preto sa po vygenerovaní obrázky preženú na 200 dpi a JPEG 82.

200 dpi je zámerný kompromis. Dokument sa číta na obrazovke a tlačí nanajvýš
kancelárskou tlačiarňou; na 300 dpi by bol dvojnásobne veľký bez viditeľného
rozdielu. Ak by sa niekedy tlačil ofsetom, vypni tento krok a pošli originál.

Spúšťa sa automaticky z make_pdf.js, netreba naň myslieť.
"""

import os
import sys

DPI_TARGET = 200
# Prevzorkujú sa len obrázky nad prahom; prah musí byť vyšší než cieľ.
DPI_THRESHOLD = 220
QUALITY = 82
# Pod týmto rozdielom sa neoplatí súbor prepisovať — ušetrené kilobajty
# nestoja za to, aby sa v gite menil dvanásťmegabajtový binárny súbor.
MIN_GAIN = 0.03


def optimize(path):
    try:
        import fitz
    except ImportError:
        print("  ! PyMuPDF nie je nainštalované — PDF sa nezmenšilo "
              "(pip install pymupdf)")
        return False

    if not os.path.exists(path):
        print(f"  ! {path} neexistuje")
        return False

    before = os.path.getsize(path)
    doc = fitz.open(path)
    doc.rewrite_images(dpi_threshold=DPI_THRESHOLD, dpi_target=DPI_TARGET,
                       quality=QUALITY)
    doc.subset_fonts()
    tmp = path + ".tmp"
    doc.save(tmp, garbage=4, deflate=True, clean=True)
    doc.close()

    after = os.path.getsize(tmp)
    if after >= before * (1 - MIN_GAIN):
        os.remove(tmp)
        print(f"  {os.path.basename(path)} — už je optimalizované "
              f"({before / 1e6:.1f} MB)")
        return True

    os.replace(tmp, path)
    print(f"  {os.path.basename(path)} — {before / 1e6:.1f} MB -> "
          f"{after / 1e6:.1f} MB ({100 - after * 100 // before} % dole)")
    if after > 10e6:
        print("  ! stále nad 10 MB — do e-mailu radšej pošli odkaz na web")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("použitie: python3 optimize_pdf.py <súbor.pdf> [...]")
    for p in sys.argv[1:]:
        optimize(p)
