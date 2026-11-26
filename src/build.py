#!/usr/bin/env python3
"""Build the Aurova Insure static site into ../docs.

Every page shares one header, footer and <head>. Page bodies live in src/pages/*.html.
Contact details live in src/contact.json.
Run:  python3 src/build.py
"""
import json
import pathlib
import re
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent / "docs"
BASE = "https://aurovainsure.co.uk"
TODAY = date.today().isoformat()

CONTACT = json.loads((ROOT / "contact.json").read_text(encoding="utf-8"))

BIZ = {
    "brand": "Aurova Insure",
    "descriptor": "Outsourced business administration",
    "company": "SBR Ventures Limited",
    "ch_url": "https://find-and-update.company-information.service.gov.uk/company/15417174",
    "company_no": "15417174",
    "reg_office": "Sabichi House, 5 Wadsworth Road, Perivale, London UB6 7JD",
    "address": "Sabichi House, 5 Wadsworth Road, Perivale, London UB6 7JD",
    "cal_url": "https://cal.com/gurpreetaurova/discovery-call",
    "phone_display": "07884 691080",
    "phone_link": "+447884691080",
    # Shown publicly on the site.
    "email": CONTACT["email"],
    "email_alt": CONTACT["email_alt"],
    # Free form-delivery key from web3forms.com. Blank = the form opens the visitor's email app instead.
    "web3forms_key": CONTACT.get("web3forms_key", ""),
}

# path, title, description, nav label (None = not in nav), breadcrumb label
PAGES = [
    ("", "Outsourced Admin Support for UK Businesses | Aurova Insure",
     "Reliable outsourced administration for UK letting agents and small businesses. Managed from London, delivered by a supervised team in India. Book a discovery call.",
     None, "Home"),
    ("letting-agents/", "Letting Agency Admin Support & Property Admin Outsourcing | Aurova Insure",
     "Outsourced property management administration for UK letting agents: compliance diaries, tenancy paperwork, maintenance logging, correspondence and CRM updates.",
     "Letting agents", "Letting agents"),
    ("services/", "Outsourced Administration Services | Aurova Insure",
     "Property, inbox, customer, CRM, document, invoicing, scheduling and general admin support for UK businesses, done inside your own systems.",
     "Services", "Services"),
    ("how-it-works/", "How Outsourced Admin Support Works | Aurova Insure",
     "From a first conversation to a supervised team working in your systems: how we scope, set up secure access, start work and review performance.",
     "How it works", "How it works"),
    ("other-businesses/", "Admin Support for Tradespeople, Accountants & SMEs | Aurova Insure",
     "Outsourced admin for tradespeople, accountants and bookkeepers, professional service firms and other UK small businesses: enquiries, quotes, diaries and payment follow-ups.",
     "Other businesses", "Other businesses"),
    ("about/", "About Aurova Insure (SBR Ventures Limited) | UK-Led Admin Support",
     "Aurova Insure is a trading name of SBR Ventures Limited (company no. 15417174), a UK-led administration business with a delivery team in Mumbai, India.",
     "About", "About"),
    ("contact/", "Contact Us | Book a Discovery Call | Aurova Insure",
     "Tell us about the administration you'd like to hand over. Book a discovery call or discuss your backlog with Aurova Insure.",
     "Contact", "Contact"),
    ("free-health-check/", "Free Renters' Rights Act Health Check for Letting Agents | Aurova Insure",
     "A free, no-obligation compliance health check on 25 of your managed properties: tenancy, deposit, gas, EICR, EPC, alarms and licensing, with a red, amber and green report.",
     None, "Free health check"),
    ("sample-report/", "Sample Health Check Report | Aurova Insure",
     "See an example of the red, amber and green health check report Aurova Insure prepares for letting agents, using a fictional agency.",
     None, "Sample report"),
    ("privacy/", "Privacy Policy | Aurova Insure",
     "How Aurova Insure (SBR Ventures Limited) collects and uses personal data, including website enquiries and client work.",
     None, "Privacy policy"),
    ("terms/", "Terms of Service | Aurova Insure",
     "Website terms of use and a summary of the terms on which Aurova Insure provides administrative support services.",
     None, "Terms of service"),
]

LOGO = ('<svg viewBox="0 0 30 30" aria-hidden="true"><rect x="1" y="1" width="28" height="28" rx="7" fill="#E8A33D"/>'
        '<path d="M8.5 15.5l4.2 4.2 8.8-9.4" fill="none" stroke="#14213D" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def nav_html(current):
    links = []
    for p, _, _, label, _ in PAGES:
        if not label:
            continue
        cur = ' aria-current="page"' if p == current else ""
        links.append(f'<a href="/{p}"{cur}>{label}</a>')
    links.append(f'<a class="btn btn-primary btn-sm nav-cta" href="{BIZ["cal_url"]}" rel="noopener">Book a discovery call</a>')
    return "\n        ".join(links)


def header(current):
    return f"""<a class="skip" href="#main">Skip to content</a>
<aside class="topbar" aria-label="Company details">
  <div class="wrap">
    <span><strong>{BIZ['brand']}</strong> is a trading name of <strong>{BIZ['company']}</strong><span class="tb-long">, registered in England and Wales</span>, company registration no. <a href="{BIZ['ch_url']}" rel="noopener">{BIZ['company_no']}</a></span>
  </div>
</aside>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="{BIZ['brand']} home">
      {LOGO}
      <span class="brand-text"><span class="brand-name">{BIZ['brand']}</span><span class="brand-sub">{BIZ['descriptor']}</span></span>
    </a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
        {nav_html(current)}
    </nav>
    <div class="header-cta">
      <a class="header-phone" href="tel:{BIZ['phone_link']}">{BIZ['phone_display']}</a>
      <a class="btn btn-primary btn-sm" href="{BIZ['cal_url']}" rel="noopener">Book a discovery call</a>
    </div>
  </div>
</header>"""


def email_items():
    items = f'<li><a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a></li>'
    if BIZ["email_alt"]:
        items += f'\n          <li><a href="mailto:{BIZ["email_alt"]}">{BIZ["email_alt"]}</a></li>'
    return items


def footer():
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="/">{LOGO}<span class="brand-text"><span class="brand-name">{BIZ['brand']}</span><span class="brand-sub">{BIZ['descriptor']}</span></span></a>
        <p>Administrative support for UK businesses, managed from London and delivered by a supervised team in India.</p>
        <p class="small">A trading name of {BIZ['company']}.</p>
      </div>
      <div>
        <h2 class="footer-h">Who we help</h2>
        <ul>
          <li><a href="/letting-agents/">Letting agents</a></li>
          <li><a href="/other-businesses/#tradespeople">Tradespeople</a></li>
          <li><a href="/other-businesses/#accountants">Accountants and bookkeepers</a></li>
          <li><a href="/other-businesses/#professional-services">Professional services</a></li>
          <li><a href="/other-businesses/#small-businesses">Other small businesses</a></li>
        </ul>
      </div>
      <div>
        <h2 class="footer-h">Company</h2>
        <ul>
          <li><a href="/services/">Services</a></li>
          <li><a href="/how-it-works/">How it works</a></li>
          <li><a href="/about/">About</a></li>
          <li><a href="/privacy/">Privacy policy</a></li>
          <li><a href="/terms/">Terms of service</a></li>
        </ul>
      </div>
      <div>
        <h2 class="footer-h">Contact</h2>
        <ul>
          <li><a href="tel:{BIZ['phone_link']}">{BIZ['phone_display']}</a></li>
          {email_items()}
          <li>{BIZ['address']}</li>
          <li><a href="{BIZ['cal_url']}" rel="noopener">Book a discovery call</a></li>
          <li><a href="/free-health-check/">Free 25-property health check</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <p>{BIZ['brand']} is a trading name of {BIZ['company']}, registered in England and Wales, company number <a href="{BIZ['ch_url']}" rel="noopener">{BIZ['company_no']}</a> (view on Companies House). Registered office: {BIZ['reg_office']}.</p>
      <p>We provide administrative support only. We are not an insurer and do not sell insurance. We do not give legal, financial, accounting or tax advice.</p>
      <p>&copy; <span data-year>2026</span> {BIZ['company']}. This site uses no tracking or advertising cookies.</p>
    </div>
  </div>
</footer>"""


def breadcrumb_ld(path, label):
    if not path:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": label, "item": f"{BASE}/{path}"},
        ],
    }


def org_ld():
    return {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": BASE + "/#organisation",
        "name": BIZ["brand"],
        "legalName": BIZ["company"],
        "alternateName": "SBR Ventures Limited trading as Aurova Insure",
        "sameAs": [BIZ["ch_url"]],
        "description": "Outsourced business administration for UK letting agents and small businesses, delivered by a supervised team in India.",
        "url": BASE + "/",
        "logo": BASE + "/assets/img/logo-512.png",
        "image": BASE + "/assets/img/og.png",
        "telephone": BIZ["phone_link"],
        "email": BIZ["email"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Sabichi House, 5 Wadsworth Road, Perivale",
            "addressLocality": "London",
            "postalCode": "UB6 7JD",
            "addressCountry": "GB",
        },
        "areaServed": {"@type": "Country", "name": "United Kingdom"},
        "identifier": {"@type": "PropertyValue", "propertyID": "Companies House", "value": BIZ["company_no"]},
    }


def head(path, title, desc, extra_ld, robots="index, follow"):
    url = f"{BASE}/{path}"
    ld_html = "\n".join(
        f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' for ld in extra_ld if ld
    )
    csp = ("default-src 'self'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self'; img-src 'self' data:; font-src 'self'; "
           "connect-src 'self' https://api.web3forms.com https://cloudflareinsights.com; form-action 'self' https://api.web3forms.com mailto:; "
           "base-uri 'self'; object-src 'none'; frame-src 'none'")
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{csp}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#14213D">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BIZ['brand']}">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/img/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/space-grotesk.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css">
{ld_html}
<!-- Cloudflare Web Analytics (cookieless) --><script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "e048b4566db244b88958bd933ed53e7d"}}'></script>
</head>"""


def faq_ld(body):
    """Build FAQPage data from the visible <details> blocks so the two never disagree."""
    items = re.findall(r'<details>\s*<summary>(.*?)</summary>\s*<div class="answer">(.*?)</div>\s*</details>', body, re.S)
    if not items:
        return None

    def clean(s):
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": clean(q), "acceptedAnswer": {"@type": "Answer", "text": clean(a)}}
            for q, a in items
        ],
    }


def render(body):
    for k, v in BIZ.items():
        body = body.replace("{{" + k + "}}", v)
    return body


def page(path, title, desc, body, extra, robots="index, follow", current=None):
    return (f"{head(path, title, desc, extra, robots)}\n<body>\n{header(current if current is not None else path)}\n"
            f'<main id="main">\n{body}\n</main>\n{footer()}\n'
            f'<script src="/assets/js/site.js" defer></script>\n</body>\n</html>\n')


def build():
    for path, title, desc, _, crumb in PAGES:
        name = path.strip("/") or "home"
        body = render((ROOT / "pages" / f"{name}.html").read_text(encoding="utf-8"))
        extra = [org_ld() if not path else None, breadcrumb_ld(path, crumb), faq_ld(body)]
        if path == "letting-agents/":
            extra.append({
                "@context": "https://schema.org",
                "@type": "Service",
                "name": "Letting agency administration support",
                "serviceType": "Outsourced property management administration",
                "provider": {"@id": BASE + "/#organisation"},
                "areaServed": {"@type": "Country", "name": "United Kingdom"},
                "audience": {"@type": "BusinessAudience", "audienceType": "Letting agents and property managers"},
            })
        if path:
            crumbs = (f'<nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> / '
                      f'<span aria-current="page">{crumb}</span></nav>')
            body = body.replace("{{breadcrumb}}", crumbs)
        dest = OUT / path / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page(path, title, desc, body, extra), encoding="utf-8")

    body404 = render((ROOT / "pages" / "404.html").read_text(encoding="utf-8"))
    (OUT / "404.html").write_text(
        page("404.html", "Page not found | Aurova Insure", "This page could not be found.", body404, [],
             robots="noindex", current="404"),
        encoding="utf-8")

    urls = "\n".join(f"  <url><loc>{BASE}/{p}</loc><lastmod>{TODAY}</lastmod></url>" for p, *_ in PAGES)
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n",
        encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    (OUT / "CNAME").write_text("aurovainsure.co.uk\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print("Built", len(PAGES) + 1, "pages into", OUT)


if __name__ == "__main__":
    build()
