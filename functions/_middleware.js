// Cloudflare Pages dáva projektu okrem vlastnej domény aj adresu
// viktoria-mikuskova.pages.dev a tú servíruje s kódom 200. Google si ju
// preto zaindexoval a vo výsledkoch hľadania sa portfólio ukazovalo pod
// adresou Cloudflare namiesto viktoriamikuskova.com.
//
// Kanonický odkaz v hlavičke stránky na to nestačil, je to len odporúčanie.
// Toto je pravidlo: čokoľvek, čo príde na produkčnú pages.dev adresu, sa
// natrvalo presmeruje na vlastnú doménu aj s cestou a parametrami.
//
// Náhľadové nasadenia (hash.viktoria-mikuskova.pages.dev) sa nechávajú tak.
// Tie už od Cloudflare dostávajú hlavičku x-robots-tag: noindex, takže sa
// neindexujú, a presmerovanie by znemožnilo pozrieť si nasadenie pred
// pustením na ostro.

const PAGES_HOST = "viktoria-mikuskova.pages.dev";
const DOMENA = "viktoriamikuskova.com";

export async function onRequest(context) {
  const url = new URL(context.request.url);

  if (url.hostname === PAGES_HOST) {
    url.hostname = DOMENA;
    url.protocol = "https:";
    url.port = "";
    return Response.redirect(url.toString(), 301);
  }

  return context.next();
}
