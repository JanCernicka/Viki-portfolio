#!/usr/bin/env bash
# Nasadenie webu na Cloudflare Pages.
#
#     ./deploy.sh
#
# Prečo cez dočasný priečinok a nie priamo `wrangler pages deploy .`:
# repozitár obsahuje aj veci, ktoré na internete byť nesmú. Priečinok
# career/ má plán oslovenia, zoznam firiem aj tabuľku s menami ľudí,
# ktorým Viktória písala. Pri nasadení celého priečinka boli tieto súbory
# verejne stiahnuteľné na uhádnuteľných adresách. Wrangler pre Pages
# nerešpektuje .assetsignore, takže sa musí kopírovať výber.
#
# Sem sa pridáva len to, čo má byť naozaj verejné.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$(mktemp -d)"
trap 'rm -rf "$OUT"' EXIT

cd "$ROOT"

# stránky, štýly, skript
cp -- *.html styles.css cv.css dokumenty.css script.js "$OUT/"
cp -- _headers _redirects "$OUT/"

# podstránky projektov a všetky obrázky, fonty a dokumenty na stiahnutie
cp -r projekt "$OUT/"
cp -r assets "$OUT/"

echo "Nasadzujem $(find "$OUT" -type f | wc -l | tr -d ' ') súborov"
echo "Nenasadzujem: career/, content/, *.py, make_pdf.js, README.md"

npx wrangler pages deploy "$OUT" \
  --project-name viktoria-mikuskova \
  --branch main \
  --commit-dirty=true
