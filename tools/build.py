#!/usr/bin/env python3
"""Builds the static pages for the Heaven On Earth concept site.

Run from anywhere:  python3 tools/build.py
Writes the .html files into the repository root. No dependencies.
All treatments, prices, text, photos and the logo come from heavenonearthskinandbody.co.za.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------------------ studio facts (from the current site)
STUDIO = "Heaven On Earth Skin, Body, Laser Studio"
ADDRESS_1 = "VIP Village, 182 Hole-in-one Avenue"
ADDRESS_2 = "Ruimsig, Roodepoort"
PHONE = "011 662 2473"
PHONE_TEL = "+27116622473"
WHATSAPP = "082 852 8885"
WHATSAPP_URL = "https://wa.me/27828528885"
EMAIL = "info@heavenonearthskinandbody.co.za"
FACEBOOK = "https://www.facebook.com/heavenonearthskinandbody/"
INSTAGRAM = "https://www.instagram.com/heavenonearthskinandbodystudio/"
MAP_Q = "VIP Village, 182 Hole-in-one Avenue, Ruimsig, Roodepoort"
MAP_Q_URL = MAP_Q.replace(" ", "+").replace(",", "%2C")
MAP_EMBED = "https://www.google.com/maps?q=" + MAP_Q_URL + "&output=embed"
MAP_OPEN = "https://www.google.com/maps/search/?api=1&query=" + MAP_Q_URL
MAP_DIRECTIONS = "https://www.google.com/maps/dir/?api=1&destination=" + MAP_Q_URL

UP = "https://heavenonearthskinandbody.co.za/wp-content/uploads/"
IMG = {
    "logo": (UP + "2019/10/Logo-Full-Colour-600x424.png", 600, 424),
    "banner": (UP + "2023/02/Banner_1-1024x683.jpg", 1024, 683),
    "salon": (UP + "2023/02/Salon_bg-1024x683.jpg", 1024, 683),
    "facial": (UP + "2023/02/Slider_bg3.jpg", 1280, 958),
    "body": (UP + "2023/02/Slider_bg5.jpg", 1280, 958),
    "faces": (UP + "2023/02/Slider_bg1.jpg", 1200, 700),
    "legs": (UP + "2023/02/Slider_bg2.jpg", 1080, 996),
    "lashes": (UP + "2022/04/Service_Lashes.jpg", 1080, 1080),
    "laser": (UP + "2019/10/WhatsApp-Image-2019-11-12-at-9.52.16-AM.jpeg", 1080, 1080),
    "skin": (UP + "2019/10/Service_skin.jpg", 834, 834),
    "brows": (UP + "2019/10/Service_EyebrowLashes.jpg", 834, 834),
    "slim": (UP + "2019/10/Service_Slim.jpg", 1080, 1080),
}
ALT = {
    "logo": "Heaven On Earth Skin, Body, Laser Studio logo",
    "banner": "Treatment room at the studio with a teal treatment bed and an armchair",
    "salon": "Studio reception with a patterned screen and a front desk",
    "facial": "Facial treatment being given with a handheld device",
    "body": "Body contouring treatment with a handheld device",
    "faces": "Close-ups of different skin tones and skin concerns",
    "legs": "Smooth legs against a white background",
    "lashes": "Close-up of an eye with volume lash extensions",
    "laser": "Laser hair removal treatment on a leg",
    "skin": "Face with close-ups of skin concerns",
    "brows": "Eye with shaped brows and lashes",
    "slim": "Hands using a handheld device on the hip area",
}
TEAM = ["Rachel", "Lucy", "Bridget", "Leandra", "Nthabiseng", "Schola", "Cathy"]
TEAM_DIM = {"Schola": (401, 600), "Cathy": (700, 1050)}


def team_img(name):
    w, h = TEAM_DIM.get(name, (834, 1250))
    return UP + "2023/02/Team_%s.jpg" % name, w, h


# ------------------------------------------------------------------ treatments (from the current site)
# group = (title, intro_note, [(subtitle_or_None, [(name, duration_or_None, price)])])
# price strings: "350", "1200+", or "Varies"
SERVICES = [
    {
        "slug": "lashes-by-chante",
        "file": "lashes-by-chante.html",
        "name": "Lashes by Chanté",
        "short": "Professional sculpting of brows and lashes are an artform, so whatever you envision for your brows and lashes, you are in good hands with Chanté.",
        "intro": "Professional sculpting of brows and lashes are an artform, so whatever you envision for your brows and lashes, you are in good hands with Chanté.",
        "img": "lashes",
        "side": None,
        "tabs": False,
        "groups": [
            ("Volume eyelash extensions", None, [(None, [
                ("Full set", None, "1000"), ("2 week fill", None, "400"),
                ("3 week fill", None, "500"), ("4 week fill", None, "650")])]),
            ("Natural volume eyelash extensions", None, [(None, [
                ("Full set", None, "800"), ("2 week fill", None, "360"),
                ("3 week fill", None, "440"), ("4 week fill", None, "550")])]),
            ("Brow lamination", None, [(None, [("Keratin brow lamination", None, "650")])]),
            ("Removal", None, [(None, [("Eyelash extension removal", None, "150")])]),
        ],
    },
    {
        "slug": "hairless",
        "file": "hairless.html",
        "name": "Hairless",
        "short": "With our powerful Venus Versa machine you are at ease with the quick, virtually pain-free Laser Hair Removal.",
        "intro": "With our powerful Venus Versa machine you are at ease with the quick, virtually pain-free Laser Hair Removal. 6-10 sessions are recommended at 4 week intervals. Waxing requires skill and we have a lot of it, using top quality products we ensure a pleasant experience.",
        "img": "laser",
        "side": "legs",
        "tabs": True,
        "groups": [
            ("Laser hair removal", None, [
                ("Face", [("Lip or chin", None, "350"), ("Lip and chin", None, "550"),
                          ("Half face", None, "650"), ("Full face", None, "900")]),
                ("Body", [("Back or chest, upper or lower", None, "1200"), ("Full back or chest", None, "2400"),
                          ("Half arm", None, "850"), ("Full arm", None, "1500"),
                          ("Garden path", None, "500"), ("Underarm", None, "500")]),
                ("Bikini", [("Side bikini", None, "600"), ("Brazilian", None, "850"), ("Hollywood", None, "1100")]),
                ("Legs", [("Full leg", None, "2300"), ("Full leg, male", None, "2500"),
                          ("3/4 leg", None, "1750"), ("Half leg", None, "1450")]),
            ]),
            ("Waxing", None, [
                ("Face", [("Lip or chin", None, "70"), ("Lip and chin", None, "140"), ("Full face", None, "180")]),
                ("Arms", [("Arm", None, "160"), ("Underarm", None, "100")]),
                ("Bikini", [("Side bikini", None, "130"), ("Brazilian", None, "190"), ("Hollywood", None, "260")]),
                ("Legs", [("Full leg", None, "250"), ("3/4 leg", None, "175"), ("1/2 leg", None, "160")]),
            ]),
        ],
    },
    {
        "slug": "all-about-skin",
        "file": "all-about-skin.html",
        "name": "All About Skin",
        "short": "Professionals you can rely on, Rachel and Nikki, are your go to Skin Queens.",
        "intro": "Professionals you can rely on, Rachel and Nikki, are your go to Skin Queens. With their years of experience along with results-driven top-of-the-line equipment, you can be sure that there will be a solution for your skin concerns: from Pigmentation, Premature Aging, Sun Damage to just getting your GLOW back.",
        "img": "skin",
        "side": "facial",
        "tabs": True,
        "groups": [
            ("IPL and skin rejuvenation", None, [(None, [
                ("Full face rejuvenation", "30 min", "1200+"),
                ("Full face including radio frequency", "45 min", "1600"),
                ("Full face including neck", "1 h", "2000"),
                ("Full face, neck and décolleté", "1 h", "3000"),
                ("Hand rejuvenation", "30 min", "1000")])]),
            ("Peels", None, [(None, [
                ("Lamelle Beta Peel", "30 min", "480"),
                ("Lamelle Beta Plus", "30 min", "480"),
                ("Face and neck Lamelle Beta Peel", "40 min", "600"),
                ("Face, neck and décolleté Lamelle Beta Peel", "45 min", "800"),
                ("Lamelle Retistore Plus", "30 min", "1100")])]),
            ("Dermapen and collagen induction therapy", None, [(None, [
                ("Package of 5 Dermapen anti-aging treatments", "1 h 30 min", "5500"),
                ("Lamelle Hydration Microneedling", "1 h", "750"),
                ("Anti-aging microneedling treatment with retinol", "1 h", "900"),
                ("Bio-microneedling treatment", "1 h 15 min", "950"),
                ("Bio-microneedling with Bio-syntha C peel", "1 h 30 min", "1300"),
                ("Advanced microneedling for ultimate skin rejuvenation", "1 h 30 min", "1600"),
                ("Dermapen scarring treatment", "1 h 30 min", "Varies"),
                ("Dermapen stretch mark treatment", "1 h 30 min", "Varies")])]),
            ("Facials", None, [(None, [
                ("Pro Skin 30 facial", "30 min", "300"),
                ("Deep cleanse", "45 min", "390"),
                ("Target treatment facial", "45 min", "450"),
                ("Hydration facial", "1 h 10 min", "550"),
                ("Anti-aging facial", "1 h 15 min", "690"),
                ("Bio thermodynamic treatment", "1 h 15 min", "700"),
                ("Oxygen facial", "1 h 20 min", "750"),
                ("Bio Restore luxury skincare treatment", "1 h 30 min", "850")])]),
            ("Hollywood carbon laser", None, [(None, [
                ("Hollywood carbon laser facial", "45 min", "650")])]),
        ],
    },
    {
        "slug": "eyebrows-and-lashes",
        "file": "eyebrows-and-lashes.html",
        "name": "Eyebrows & Lashes",
        "short": "Professional sculpting of brows is an art so whatever it is you choose you are in good hands.",
        "intro": "Professional sculpting of brows is an art so whatever it is you choose you are in good hands. From Microblading by Sharon and Dimpho; Permanent Make-up by Sharon; Lash extensions by Schola or a traditional Keratin Lash Lift with BOTOX ensuring healthy, strong natural lashes.",
        "img": "brows",
        "side": None,
        "tabs": True,
        "groups": [
            ("Microblading", None, [(None, [
                ("Eyebrow embroidery follow-up", "1 h", "500"),
                ("Eyebrow embroidery", "1 h 30 min", "1900"),
                ("Embroidery", "2 h", "1900")])]),
            ("Brows and lashes", None, [(None, [
                ("Brow shape", "15 min", "90"),
                ("Brow tint", "15 min", "70"),
                ("Brow shaping with tint", "20 min", "140"),
                ("Lash and brow tint", "30 min", "145"),
                ("Lash tint with brow shape and tint", "40 min", "180"),
                ("Keratin lash lift and tint", "1 h", "550"),
                ("Powder eyebrows", "1 h 30 min", "2800"),
                ("Eyebrow yearly touch-up", "1 h", "550"),
                ("Powder eyebrows", "1 h", "700")])]),
            ("Permanent make-up", None, [(None, [
                ("Permanent eyeliner (top and bottom liner)", "1 h 30 min", "1600"),
                ("Permanent eyeliner (top or bottom liner only)", "1 h", "1000"),
                ("Permanent eyeliner touch-up", "1 h 30 min", "900"),
                ("Keratin lash lift", "45 min", "550"),
                ("Individual lashes, classic", "1 h 30 min", "650"),
                ("Lash fill", "1 h", "Varies")])]),
        ],
    },
    {
        "slug": "slim-me-up",
        "file": "slim-me-up.html",
        "name": "Slim Me Up",
        "short": "If it's body fat that you are worried about, or perhaps jiggly thighs, or a lumpy behind, we have many options to choose from.",
        "intro": "If it's body fat that you are worried about, or perhaps jiggly thighs, or a lumpy behind, we have many options to choose from. 10 treatments are recommended to see the best results.",
        "img": "slim",
        "side": "body",
        "tabs": True,
        "offer": "20% off Skin Tightening Packages",
        "groups": [
            ("Skin tightening", None, [(None, [
                ("Laser lipo treatment", "1 h", "350"),
                ("RF body contouring / cellulite treatment", "45 min", "600"),
                ("Tummy", "45 min", "600"),
                ("Arms", "45 min", "600"),
                ("Buttocks", "45 min", "600"),
                ("Knees", "45 min", "600"),
                ("Neck", "45 min", "600"),
                ("Legs, front", "45 min", "600"),
                ("Legs, back", "45 min", "600"),
                ("Full face", "45 min", "600")])]),
            ("EMS sculpting", "EMS", []),
        ],
    },
]
EMS_TEXT = ("EMS Sculpt is a non-invasive solution for fat loss and muscle toning. The procedure uses electromagnetic "
            "energy to stimulate powerful muscle contractions leading to fat reduction and muscle toning. 30 min of "
            "training is equal to 20,000 muscle contractions. Suggested 6-8 treatments done 1-2 times a week.")
ABOUT_TEXT = ("Our commitment to quality and service ensure that our clients are happy. With years of experience and "
              "continuing education, our dedicated staff are ready to assist with your beauty needs. We are happy to "
              "help you decide the best look for you.")

# ------------------------------------------------------------------ helpers
esc = lambda s: html.escape(str(s), quote=True)
NB = " "


def money(p):
    if p == "Varies":
        return "Varies"
    plus = p.endswith("+")
    n = int(p.rstrip("+"))
    s = "{:,}".format(n).replace(",", NB)
    return "R" + s + ("+" if plus else "")


def img(key, cls="", lazy=True, w=None, h=None, alt=None):
    src, iw, ih = IMG[key]
    return '<img src="%s" width="%d" height="%d" alt="%s"%s%s>' % (
        esc(src), w or iw, h or ih, esc(alt if alt is not None else ALT[key]),
        ' class="%s"' % cls if cls else "", ' loading="lazy" decoding="async"' if lazy else "")


def logo_crop(big=False):
    # the logo file has wide empty margins, so it is cropped to the artwork with CSS
    src, w, h = IMG["logo"]
    return ('<span class="logo-crop%s"><img src="%s" width="%d" height="%d" alt="%s"></span>'
            % (" big" if big else "", esc(src), w, h, esc(ALT["logo"])))


def catalog_json():
    out, n = [], 0
    for s in SERVICES:
        items = []
        for gtitle, _note, subs in s["groups"]:
            for sub, rows in subs:
                for name, dur, price in rows:
                    n += 1
                    label = name if not sub else "%s: %s" % (sub, name)
                    items.append({"id": "t%d" % n, "group": gtitle, "name": label, "dur": dur or "", "price": money(price)})
        out.append({"slug": s["slug"], "name": s["name"], "items": items})
    return out


def item_ids():
    """Map (service slug, group index, sub index, row index) -> booking id, in the same order as catalog_json."""
    ids, n = {}, 0
    for s in SERVICES:
        for gi, (_t, _n, subs) in enumerate(s["groups"]):
            for si, (_sub, rows) in enumerate(subs):
                for ri, _row in enumerate(rows):
                    n += 1
                    ids[(s["slug"], gi, si, ri)] = "t%d" % n
    return ids


IDS = item_ids()

NAV = [("index.html", "Home"), ("about.html", "About"), ("services.html", "Services"), ("contact.html", "Contact")]


def header(active):
    sub = "".join(
        '<li><a href="%s"%s>%s</a></li>' % (s["file"], ' aria-current="page"' if active == s["slug"] else "", esc(s["name"]))
        for s in SERVICES)
    sub += '<li class="sub-all"><a href="services.html">All treatments</a></li>'
    cur = lambda k: ' aria-current="page"' if active == k else ""
    services_cur = ' aria-current="page"' if active == "services" else ""
    return """
<a class="skip" href="#main">Skip to content</a>
<div class="concept-bar" role="note">Concept preview of a new Heaven On Earth website. This is not the live site. Designed by <a href="https://mrpoint.online">Pablo Lebelo, mrpoint.online</a></div>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="index.html" aria-label="Heaven On Earth, home">%(logo)s<span class="brand-name">Heaven On Earth</span></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav id="nav" aria-label="Main">
      <ul class="nav-list">
        <li><a class="nav-link" href="index.html"%(c_home)s>Home</a></li>
        <li><a class="nav-link" href="about.html"%(c_about)s>About</a></li>
        <li class="has-sub">
          <a class="nav-link" href="services.html"%(c_services)s>Services</a>
          <button class="sub-toggle" type="button" aria-expanded="false" aria-controls="sub-services"><span class="sr">Show treatment pages</span><svg width="12" height="8" viewBox="0 0 12 8" aria-hidden="true"><path d="M1 1.5l5 5 5-5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
          <ul class="sub" id="sub-services">%(sub)s</ul>
        </li>
        <li><a class="nav-link" href="contact.html"%(c_contact)s>Contact</a></li>
      </ul>
      <a class="btn btn-solid nav-cta" href="book.html">Book online</a>
    </nav>
  </div>
</header>""" % {
        "logo": logo_crop(), "sub": sub,
        "c_home": cur("home"), "c_about": cur("about"), "c_contact": cur("contact"), "c_services": services_cur,
    }


def footer():
    svc = "".join('<li><a href="%s">%s</a></li>' % (s["file"], esc(s["name"])) for s in SERVICES)
    return """
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">%(logo)s<p>Skin, Body, Laser Studio<br>%(a1)s<br>%(a2)s</p></div>
      <div><h4>Treatments</h4><ul>%(svc)s</ul></div>
      <div><h4>Studio</h4><ul>
        <li><a href="about.html">About us</a></li>
        <li><a href="book.html">Book online</a></li>
        <li><a href="contact.html">Contact and map</a></li>
        <li><a href="%(fb)s" rel="noopener">Facebook</a></li>
        <li><a href="%(ig)s" rel="noopener">Instagram</a></li></ul></div>
      <div><h4>Get in touch</h4><ul>
        <li><a href="tel:%(tel)s">%(phone)s</a></li>
        <li><a href="%(wa)s" rel="noopener">WhatsApp %(whatsapp)s</a></li>
        <li><a href="mailto:%(email)s">%(email)s</a></li></ul></div>
    </div>
    <div class="legal">
      <p>Concept website by Pablo Lebelo, <a href="https://mrpoint.online">mrpoint.online</a>, 073 708 6840. Not the official site of Heaven On Earth Skin &amp; Body Studio.</p>
      <p>Treatments, prices, text, photos and logo are from the studio's current website.</p>
    </div>
  </div>
</footer>
<div class="concept-chip" aria-hidden="true">Concept preview</div>""" % {
        "logo": logo_crop(big=True), "a1": esc(ADDRESS_1), "a2": esc(ADDRESS_2), "svc": svc,
        "fb": FACEBOOK, "ig": INSTAGRAM, "tel": PHONE_TEL, "phone": PHONE, "wa": WHATSAPP_URL,
        "whatsapp": WHATSAPP, "email": EMAIL,
    }


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700'
         '&family=Instrument+Serif:ital@0;1&display=swap">')
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Ccircle cx='38' cy='26' r='24' fill='%231d7a7f'/%3E%3Ccircle cx='22' cy='42' r='16' fill='%23ebe7e3'/%3E%3C/svg%3E")


def page(filename, title, description, active, body, scripts=("site.js",), head_extra=""):
    doc = """<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s | Heaven On Earth (concept)</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0f3f43">
<link rel="icon" href="%(fav)s">
%(fonts)s
<link rel="stylesheet" href="styles.css">
%(extra)s
</head>
<body>%(header)s
<main id="main">%(body)s
</main>%(footer)s
%(scripts)s
</body>
</html>
""" % {
        "title": esc(title), "desc": esc(description), "fav": FAVICON, "fonts": FONTS, "extra": head_extra,
        "header": header(active), "body": body, "footer": footer(),
        "scripts": "\n".join('<script src="%s" defer></script>' % s for s in scripts),
    }
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write(doc)


def orbs(main_key, side_key=None, pearl_text=None):
    out = ['<div class="orbs">', '<div class="orb orb-main">%s</div>' % img(main_key, lazy=False)]
    if side_key:
        out.append('<div class="orb orb-side">%s</div>' % img(side_key, lazy=False))
    elif pearl_text:
        out.append('<div class="orb orb-side orb-pearl"><span>%s</span></div>' % esc(pearl_text))
    out.append("</div>")
    return "".join(out)


def svc_rows():
    rows = []
    for s in SERVICES:
        rows.append(
            '<li class="svc-row"><div class="svc-orb">%s</div><div><h3>%s</h3><p>%s</p></div>'
            '<a class="go btn btn-line" href="%s">See treatments and prices</a></li>'
            % (img(s["img"], alt=""), esc(s["name"]), esc(s["short"]), s["file"]))
    return '<ul class="svc-list">%s</ul>' % "".join(rows)


def visit_band(heading="Visit the studio"):
    return """
<section class="section visit" aria-labelledby="visit-h">
  <div class="wrap visit-grid">
    <div>
      <h2 id="visit-h">%(heading)s</h2>
      <ul class="details">
        <li><span class="k">Address</span>%(a1)s, %(a2)s</li>
        <li><span class="k">Phone</span><a href="tel:%(tel)s">%(phone)s</a></li>
        <li><span class="k">WhatsApp</span><a href="%(wa)s" rel="noopener">%(whatsapp)s</a></li>
        <li><span class="k">Email</span><a href="mailto:%(email)s">%(email)s</a></li>
      </ul>
      <div class="btn-row"><a class="btn btn-light" href="%(dir)s" rel="noopener">Get directions</a><a class="btn btn-line" style="border-color:#fff;color:#fff" href="book.html">Book online</a></div>
    </div>
    <iframe class="map" title="Map showing %(studio)s" src="%(embed)s" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
  </div>
</section>""" % {
        "heading": heading, "a1": esc(ADDRESS_1), "a2": esc(ADDRESS_2), "tel": PHONE_TEL, "phone": PHONE,
        "wa": WHATSAPP_URL, "whatsapp": WHATSAPP, "email": EMAIL, "dir": MAP_DIRECTIONS, "studio": esc(STUDIO),
        "embed": MAP_EMBED,
    }


def cta_band(heading="Ready to book?", text="Choose a treatment, pick a time and send your details."):
    return """
<section class="cta">
  <div class="wrap">
    <div><h2>%s</h2><p>%s</p></div>
    <div class="btn-row"><a class="btn btn-light" href="book.html">Book online</a><a class="btn btn-line" style="border-color:#fff;color:#fff" href="%s" rel="noopener">WhatsApp us</a></div>
  </div>
</section>""" % (esc(heading), esc(text), WHATSAPP_URL)


# ------------------------------------------------------------------ pages
def build_home():
    offer = [s for s in SERVICES if s.get("offer")][0]
    body = """
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>Heaven On Earth</h1>
      <p class="strap">Skin, Body, Laser Studio in Ruimsig</p>
      <p class="lede">With years of experience and continuing education, our dedicated staff are ready to assist with your beauty needs.</p>
      <div class="btn-row"><a class="btn btn-solid" href="book.html">Book online</a><a class="btn btn-line" href="services.html">See all treatments</a></div>
      <p class="hero-meta">%(a1)s, %(a2)s<br>Call <a href="tel:%(tel)s">%(phone)s</a> or WhatsApp <a href="%(wa)s" rel="noopener">%(whatsapp)s</a></p>
    </div>
    %(orbs)s
  </div>
</section>
<aside class="offer" aria-label="Offer">
  <div class="wrap"><p><strong>%(offer)s</strong></p><a href="%(offer_file)s">See skin tightening</a></div>
</aside>
<section class="section" aria-labelledby="t-h">
  <div class="wrap">
    <div class="section-head"><h2 id="t-h">Treatments</h2><p>Each treatment area has its own page with the full price list.</p></div>
    %(rows)s
  </div>
</section>
<section class="section section-tint" aria-labelledby="a-h">
  <div class="wrap split">
    <div class="photo">%(salon)s</div>
    <div>
      <h2 id="a-h">About us</h2>
      <p>%(about)s</p>
      <p><a class="text-link" href="about.html">Meet the team</a></p>
    </div>
  </div>
</section>%(visit)s%(cta)s""" % {
        "a1": esc(ADDRESS_1), "a2": esc(ADDRESS_2), "tel": PHONE_TEL, "phone": PHONE, "wa": WHATSAPP_URL,
        "whatsapp": WHATSAPP,
        "orbs": orbs("banner", None, "Skin, body, laser studio"),
        "offer": esc(offer["offer"]), "offer_file": offer["file"],
        "rows": svc_rows(), "salon": img("salon"), "about": esc(ABOUT_TEXT),
        "visit": visit_band(), "cta": cta_band(),
    }
    page("index.html", "Skin, body and laser studio in Ruimsig",
         "Concept website for Heaven On Earth Skin, Body, Laser Studio in Ruimsig, Roodepoort: laser hair removal, skin treatments, lashes, brows and body sculpting.",
         "home", body)


def build_about():
    people = "".join(
        '<li><div class="portrait"><img src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"></div><span class="nm">%s</span></li>'
        % ((esc(team_img(n)[0]), team_img(n)[1], team_img(n)[2], esc(n), esc(n))) for n in TEAM)
    body = """
<section class="page-head">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> / <span aria-current="page">About us</span></p>
    <div class="split">
      <div>
        <h1>About us</h1>
        <p class="strap" style="font-family:var(--serif);font-style:italic;font-size:1.7rem;color:var(--teal);margin-bottom:.8em">Who we are</p>
        <p class="lede">%(about)s</p>
        <div class="btn-row"><a class="btn btn-solid" href="book.html">Book online</a><a class="btn btn-line" href="contact.html">Contact us</a></div>
      </div>
      <div class="photo">%(salon)s</div>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="team-h">
  <div class="wrap">
    <div class="section-head"><h2 id="team-h">The team</h2></div>
    <ul class="team">%(people)s</ul>
  </div>
</section>%(cta)s""" % {"about": esc(ABOUT_TEXT), "salon": img("salon", lazy=False), "people": people,
                        "cta": cta_band("Meet us at the studio", "Book a treatment or ask us which look suits you best.")}
    page("about.html", "About us", "About the team at Heaven On Earth Skin, Body, Laser Studio in Ruimsig.", "about", body)


def build_services():
    body = """
<section class="page-head">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> / <span aria-current="page">Services</span></p>
    <h1>Services</h1>
    <p class="lede">Choose a treatment area to see what is on offer and what it costs.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">%s</div>
</section>%s""" % (svc_rows(), cta_band("Not sure where to start?", "Contact us now and get special offers! Message us on WhatsApp and we will help you choose."))
    page("services.html", "Services", "Lashes, laser hair removal, skin treatments, brows and body sculpting at Heaven On Earth in Ruimsig.", "services", body)


def menu_rows(slug, gi, subs):
    out = []
    for si, (sub, rows) in enumerate(subs):
        if sub:
            out.append('<h4 class="menu-sub">%s</h4>' % esc(sub))
        lis = []
        for ri, (name, dur, price) in enumerate(rows):
            tid = IDS[(slug, gi, si, ri)]
            lis.append(
                '<li class="menu-row"><span class="nm">%s</span><span class="du">%s</span><span class="pr">%s</span>'
                '<a class="bk" href="book.html?t=%s" aria-label="Book %s"> Book</a></li>'
                % (esc(name), esc(dur or ""), money(price), tid, esc(name)))
        out.append('<ul class="menu-list">%s</ul>' % "".join(lis))
    return "".join(out)


def build_service(s, idx):
    others = "".join('<a href="%s">%s</a>' % (o["file"], esc(o["name"])) for o in SERVICES if o is not s)
    panels, tabs = [], []
    for gi, (title, marker, subs) in enumerate(s["groups"]):
        pid = "p-%s-%d" % (s["slug"], gi)
        if marker == "EMS":
            inner = ('<div class="ems"><p>%s</p><p class="form-note">Message us on WhatsApp or call to ask about EMS Sculpt treatments.</p>'
                     '<div class="btn-row" style="margin-top:14px"><a class="btn btn-solid" href="%s" rel="noopener">WhatsApp us</a><a class="btn btn-line" href="tel:%s">Call %s</a></div></div>'
                     % (esc(EMS_TEXT), WHATSAPP_URL, PHONE_TEL, PHONE))
        else:
            inner = menu_rows(s["slug"], gi, subs)
        if s["tabs"]:
            panels.append('<div class="tabpanel" role="tabpanel" id="%s" aria-labelledby="tab-%s"><h3 class="panel-title">%s</h3>%s</div>'
                          % (pid, pid, esc(title), inner))
            tabs.append('<button class="tab" role="tab" type="button" id="tab-%s" aria-controls="%s" aria-selected="%s" tabindex="%s">%s</button>'
                        % (pid, pid, "true" if gi == 0 else "false", "0" if gi == 0 else "-1", esc(title)))
        else:
            # short pages: every group is visible, no tabs needed
            panels.append('<div class="group" id="%s"><h3 class="panel-title" style="margin-top:%dpx">%s</h3>%s</div>'
                          % (pid, 0 if gi == 0 else 40, esc(title), inner))
    if s["tabs"]:
        menu = '<div data-tabs><div class="tablist" role="tablist" aria-label="%s treatment groups">%s</div>%s</div>' % (esc(s["name"]), "".join(tabs), "".join(panels))
    else:
        menu = "".join(panels)
    offer = ""
    if s.get("offer"):
        offer = '<aside class="offer" aria-label="Offer"><div class="wrap"><p><strong>%s</strong></p><a href="book.html?c=%s">Book a treatment</a></div></aside>' % (esc(s["offer"]), s["slug"])
    body = """
<section class="page-head">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> / <a href="services.html">Services</a> / <span aria-current="page">%(name)s</span></p>
    <div class="page-head-grid">
      <div>
        <h1>%(name)s</h1>
        <p class="lede">%(intro)s</p>
        <div class="btn-row"><a class="btn btn-solid" href="book.html?c=%(slug)s">Book online</a><a class="btn btn-line" href="%(wa)s" rel="noopener">WhatsApp us</a></div>
      </div>
      %(orbs)s
    </div>
  </div>
</section>%(offer)s
<section class="menu-wrap" aria-label="%(name)s treatments and prices">
  <div class="wrap">%(menu)s</div>
</section>
<section class="section section-tint" style="padding-block:44px">
  <div class="wrap"><h2 style="font-size:1.9rem">More treatments</h2><div class="others">%(others)s</div></div>
</section>%(cta)s""" % {
        "name": esc(s["name"]), "intro": esc(s["intro"]), "slug": s["slug"], "wa": WHATSAPP_URL,
        "orbs": orbs(s["img"], s["side"], None if s["side"] else "Contact us now and get special offers!"),
        "offer": offer, "menu": menu, "others": others,
        "cta": cta_band("Book %s" % s["name"], "Contact us now and get special offers!"),
    }
    page(s["file"], s["name"], "%s at Heaven On Earth Skin, Body, Laser Studio in Ruimsig: treatments, durations and prices." % s["name"], s["slug"], body)


def build_contact():
    body = """
<section class="page-head">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> / <span aria-current="page">Contact</span></p>
    <h1>Contact us</h1>
    <p class="lede">Call, WhatsApp or send a message. To book a treatment, use online booking.</p>
  </div>
</section>
<section class="section" style="padding-top:12px">
  <div class="wrap contact-grid">
    <div class="card">
      <h2 style="font-size:1.9rem">Find the studio</h2>
      <ul class="details">
        <li><span class="k">Address</span>%(a1)s, %(a2)s</li>
        <li><span class="k">Phone</span><a href="tel:%(tel)s">%(phone)s</a></li>
        <li><span class="k">WhatsApp</span><a href="%(wa)s" rel="noopener">%(whatsapp)s</a></li>
        <li><span class="k">Email</span><a href="mailto:%(email)s">%(email)s</a></li>
        <li><span class="k">Social</span><a href="%(fb)s" rel="noopener">Facebook</a> and <a href="%(ig)s" rel="noopener">Instagram</a></li>
      </ul>
      <div class="btn-row"><a class="btn btn-solid" href="%(dir)s" rel="noopener">Get directions</a><a class="btn btn-line" href="%(open)s" rel="noopener">Open in Google Maps</a></div>
    </div>
    <div class="card">
      <h2 style="font-size:1.9rem">Send a message</h2>
      <p class="form-note">For any other queries please complete the form below.</p>
      <form id="contact-form" novalidate>
        <div class="field"><label for="cf-name">Your name</label><input id="cf-name" name="name" autocomplete="name"></div>
        <div class="field"><label for="cf-phone">Phone</label><input id="cf-phone" name="phone" type="tel" autocomplete="tel"></div>
        <div class="field"><label for="cf-email">Email address</label><input id="cf-email" name="email" type="email" autocomplete="email" aria-describedby="cf-email-err" required><div class="err" id="cf-email-err" aria-live="polite"></div></div>
        <div class="field"><label for="cf-message">Message</label><textarea id="cf-message" name="message" aria-describedby="cf-message-err" required></textarea><div class="err" id="cf-message-err" aria-live="polite"></div></div>
        <button class="btn btn-solid" type="submit">Send message</button>
      </form>
      <div class="notice" id="cf-notice" tabindex="-1" role="status" hidden><strong>This is a concept preview, so nothing was sent.</strong> To reach the studio, call %(phone)s or WhatsApp %(whatsapp)s.</div>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap"><iframe class="map" style="height:440px" title="Map showing %(studio)s" src="%(embed)s" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
</section>""" % {
        "a1": esc(ADDRESS_1), "a2": esc(ADDRESS_2), "tel": PHONE_TEL, "phone": PHONE, "wa": WHATSAPP_URL, "whatsapp": WHATSAPP,
        "email": EMAIL, "fb": FACEBOOK, "ig": INSTAGRAM, "dir": MAP_DIRECTIONS, "open": MAP_OPEN, "studio": esc(STUDIO), "embed": MAP_EMBED,
    }
    page("contact.html", "Contact", "Address, phone, WhatsApp, email and map for Heaven On Earth Skin, Body, Laser Studio in Ruimsig.", "contact", body)


def build_book():
    cat_json = json.dumps(catalog_json(), ensure_ascii=False).replace("</", "<\\/")
    body = """
<section class="page-head" id="book-top">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> / <span aria-current="page">Book online</span></p>
    <h1>Book online</h1>
    <p class="lede">This is a demo of how online booking could work. Nothing is booked or sent, and the times shown are samples.</p>
  </div>
</section>
<div class="wrap book-grid">
  <div>
    <ol class="stepper" aria-label="Booking steps">
      <li><span class="n">1</span>Treatment</li><li><span class="n">2</span>Date and time</li><li><span class="n">3</span>Your details</li><li><span class="n">4</span>Review</li>
    </ol>

    <section class="step" id="step-treatment" aria-labelledby="h-treatment">
      <h2 id="h-treatment">Choose a treatment</h2>
      <div class="tablist" style="display:flex" id="cat-tabs" role="group" aria-label="Treatment area"></div>
      <div id="pick-list" class="pick"></div>
      <div class="step-actions"><button class="btn btn-solid" type="button" id="next-treatment" disabled>Continue to date and time</button></div>
    </section>

    <section class="step" id="step-when" aria-labelledby="h-when" hidden>
      <h2 id="h-when">Pick a date and time</h2>
      <div class="dates" id="dates" role="group" aria-label="Date"></div>
      <div class="slots" id="slots" role="group" aria-label="Time"></div>
      <p class="form-note" style="margin-top:16px">Sample availability for the demo. A live version would show the studio's real calendar and opening hours.</p>
      <div class="step-actions"><button class="btn btn-line" type="button" id="back-when">Back</button><button class="btn btn-solid" type="button" id="next-when" disabled>Continue to your details</button></div>
    </section>

    <section class="step" id="step-details" aria-labelledby="h-details" hidden>
      <h2 id="h-details">Your details</h2>
      <form id="details-form" novalidate>
        <div class="field"><label for="bk-name">Name</label><input id="bk-name" autocomplete="name" aria-describedby="bk-name-err" required><div class="err" id="bk-name-err" aria-live="polite"></div></div>
        <div class="field"><label for="bk-phone">Mobile number</label><input id="bk-phone" type="tel" autocomplete="tel" aria-describedby="bk-phone-err" required><div class="err" id="bk-phone-err" aria-live="polite"></div></div>
        <div class="field"><label for="bk-email">Email (optional)</label><input id="bk-email" type="email" autocomplete="email" aria-describedby="bk-email-err"><div class="err" id="bk-email-err" aria-live="polite"></div></div>
        <p class="form-note">Demo only: these details stay in this browser tab and are not stored or sent.</p>
        <div class="step-actions"><button class="btn btn-line" type="button" id="back-details">Back</button><button class="btn btn-solid" type="submit">Review booking</button></div>
      </form>
    </section>

    <section class="step" id="step-review" aria-labelledby="h-review" hidden>
      <h2 id="h-review">Review your booking</h2>
      <div id="review-wrap">
        <ul class="review" id="review-list"></ul>
        <div class="step-actions"><button class="btn btn-line" type="button" id="back-review">Back</button><button class="btn btn-solid" type="button" id="confirm">Confirm booking (demo)</button></div>
      </div>
      <div class="done-box" id="done" tabindex="-1" role="status" hidden>
        <h3>That is the demo flow</h3>
        <p>Nothing was booked or sent. In a live version, this is where the studio's confirmation would appear.</p>
        <div class="btn-row"><button class="btn btn-solid" type="button" id="restart">Start again</button><a class="btn btn-line" href="index.html">Back to home</a></div>
      </div>
    </section>
  </div>

  <aside class="summary" aria-label="Your booking so far">
    <h2>Your booking</h2>
    <dl>
      <dt>Treatment</dt><dd id="sum-treatment">Not chosen yet</dd>
      <dd id="sum-cat" style="font-weight:400;color:var(--muted)"></dd>
      <dt>Date and time</dt><dd id="sum-when">Not chosen yet</dd>
      <dt>Price and duration</dt><dd id="sum-price"></dd>
    </dl>
    <p class="demo">Concept preview: no booking is made. To book now, call <a href="tel:%(tel)s">%(phone)s</a> or WhatsApp <a href="%(wa)s" rel="noopener">%(whatsapp)s</a>.</p>
  </aside>
</div>
<script type="application/json" id="catalog">%(cat)s</script>""" % {
        "tel": PHONE_TEL, "phone": PHONE, "wa": WHATSAPP_URL, "whatsapp": WHATSAPP, "cat": cat_json}
    page("book.html", "Book online", "Demo of online booking for Heaven On Earth Skin, Body, Laser Studio. Nothing is booked or sent.", "book", body, scripts=("site.js", "book.js"))


if __name__ == "__main__":
    build_home()
    build_about()
    build_services()
    for i, s in enumerate(SERVICES):
        build_service(s, i)
    build_contact()
    build_book()
    print("Built pages in", ROOT)
