"""Treatment menu for the Heaven On Earth concept site.

Source: the studio's live Booksy page (booksy.com, business 7335), read on 3 November 2026.
Names are tidied into sentence case and obvious typos are fixed; prices and durations are as listed on Booksy.
Short descriptions are taken from the studio's own Booksy text (or its current website), trimmed to one line.

Each row: (name, minutes, price, description)
price strings: "350", "1300+" (from), "Varies" or "Free"
group:  (tab title, None, [(subheading or None, [rows])])
"""

BOOKSY_URL = "https://booksy.com/en-za/7335_heaven-on-earth-skin-body-laser-studio_skin-care_54437_roodepoort"
BOOKSY_RATING = "4.8"
BOOKSY_REVIEWS = 290
BOOKSY_CHECKED = "November 2026"

HOURS = [("Monday", "09:00 to 15:00"), ("Tuesday to Friday", "08:30 to 17:00"),
         ("Saturday", "08:30 to 14:00"), ("Sunday", "Closed")]
POLICY = "Appointments only, no walk-ins."
AMENITIES = ["Parking", "Card payments accepted", "Wheelchair accessible", "Wi-Fi", "Loyalty programme"]
STAFF_ON_BOOKSY = ["Rachel", "Nikki", "Chanté"]

EMS_LINE = "EMS Sculpt is a non-invasive solution for fat loss and muscle toning."

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
            ("Natural volume lashes", None, [(None, [
                ("Full set", 90, "900", "A full set of volume lashes, luxurious, soft and full."),
                ("1 week fill", 30, "200", ""),
                ("2 week fill", 60, "400", ""),
                ("3 week fill", 60, "480", ""),
                ("4 week fill", 60, "600", "")])]),
            ("Glamour volume lashes", None, [(None, [
                ("Full set", 120, "1200", ""),
                ("1 week fill", 30, "250", ""),
                ("2 week fill", 60, "450", ""),
                ("3 week fill", 60, "550", ""),
                ("4 week fill", 60, "700", "")])]),
            ("Removal", None, [(None, [
                ("Lash removal", 30, "150", "")])]),
        ],
    },
    {
        "slug": "hairless",
        "file": "hairless.html",
        "name": "Hairless",
        "short": "With our powerful Venus Versa machine you are at ease with the quick, virtually pain-free Laser Hair Removal.",
        "intro": "With our powerful Venus Versa machine you are at ease with the quick, virtually pain-free Laser Hair Removal. 8 to 12 sessions are recommended at 4 week intervals. Waxing requires skill and we have a lot of it, using top quality products we ensure a pleasant experience.",
        "img": "laser",
        "side": "legs",
        "tabs": True,
        "groups": [
            ("Laser hair removal", None, [
                ("Face", [
                    ("Lip or chin", 15, "300", ""),
                    ("Lip and chin", 15, "550", ""),
                    ("Half face", 20, "650", ""),
                    ("Full face", 30, "900", ""),
                    ("Neck", 15, "500", "")]),
                ("Arms and body", [
                    ("Underarm", 15, "500", ""),
                    ("Underarm, students", 15, "350", ""),
                    ("Half arm", 30, "850", ""),
                    ("Full arm", 40, "1500", ""),
                    ("Fingers or toes", 15, "300", ""),
                    ("Tummy garden path", 15, "500", ""),
                    ("Back or chest, upper or lower", 30, "1200", ""),
                    ("Full back or chest", 45, "2400", "")]),
                ("Bikini", [
                    ("Side bikini", 15, "600", ""),
                    ("Brazilian", 20, "850", ""),
                    ("Hollywood", 40, "1100", "Full bikini including the buttocks."),
                    ("Full buttocks", 30, "1000", "")]),
                ("Legs", [
                    ("Half leg", 30, "1450", ""),
                    ("Three-quarter leg", 30, "1750", ""),
                    ("Full leg", 60, "2300", "")]),
                ("Men", [
                    ("Full leg, male", 60, "2500", ""),
                    ("Full bikini, male", 30, "2000", "Full front and buttocks.")]),
            ]),
            ("Waxing", None, [
                ("Face", [
                    ("Brow wax", 15, "100", ""),
                    ("Upper lip", 10, "100", ""),
                    ("Chin", 10, "90", ""),
                    ("Lip and chin", 15, "180", ""),
                    ("Nose", 15, "90", "")]),
                ("Body", [
                    ("Underarm", 15, "150", ""),
                    ("Tummy", 20, "200", "")]),
                ("Bikini", [
                    ("Side bikini", 20, "150", ""),
                    ("Brazilian or G-string", 25, "250", "Leaves a landing strip."),
                    ("Hollywood", 30, "350", "Full wax including the buttocks.")]),
                ("Legs", [
                    ("Half leg", 30, "220", ""),
                    ("Three-quarter leg", 30, "240", ""),
                    ("Full leg", 40, "280", "")]),
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
            ("Facials", None, [
                ("Start here", [
                    ("Skin consultation", 30, "Free", "A professional assessment of your skin to identify concerns and recommend treatments and products.")]),
                ("Facials", [
                    ("Dermaplaning", 30, "300", ""),
                    ("Dermaplane facial", 30, "400", "Removes dead skin cells and fine peach fuzz with a sterile blade."),
                    ("Derma teen facial", 60, "450", ""),
                    ("Target treatment facial", 45, "500", "Designed for your skin's needs, with hydrodermabrasion and LED light therapy."),
                    ("Male facial with brow clean-up", 45, "500", ""),
                    ("Oxygen facial", 60, "550", "Micro-exfoliation, oxygenation and massage for healthy, glowing skin."),
                    ("Hydration facial", 70, "550", "Treatment for dry, dehydrated skin, finished with oxygen therapy."),
                    ("Hollywood carbon laser facial", 60, "650", ""),
                    ("Anti-aging facial", 75, "750", "Just over an hour of pure skin indulgence, tailored to your skin concerns."),
                    ("Hydrapen skin treatment", 45, "800", "Fractional mesotherapy that renews the skin inside and out.")]),
            ]),
            ("Peels", None, [
                ("Lamelle peels", [
                    ("Lamelle Beta Peel", 30, "600", "A 15 or 20% peel for specific skin concerns."),
                    ("Lamelle Beta Plus", 45, "600", "For acne and breakouts, with extractions and LED light."),
                    ("TCA Lamelle Peel", 30, "700", "A deeper peel for stubborn pigmentation and scars."),
                    ("Face and neck Lamelle Beta Peel", 40, "800", ""),
                    ("Face, neck and décolleté Lamelle Beta Peel", 45, "1200", "")]),
                ("Professional peels", [
                    ("Alpha peel", 40, "600", "A brightening peel for acne, ageing, texture and pigmentation."),
                    ("Periocular peel", 45, "600", "Designed for the eye area: dark circles, fine lines and pigmentation."),
                    ("Lacti Firm peel", 45, "650", "Ideal for a first peel. Brightens, plumps and hydrates."),
                    ("Synergy peel", 30, "800", "A hybrid TCA and lactic acid peel. A course of 3 is recommended."),
                    ("Medi A Peel", 30, "800", ""),
                    ("Synergy Medi A combo", 45, "1300", "Face and neck. Peeling lasts roughly 3 to 5 days.")]),
                ("Noon Aesthetics", [
                    ("G-Peel 30 nano-constructed", 30, "800", ""),
                    ("G-Peel 50 solution", 30, "800", ""),
                    ("G-Peel 50 nano-constructed", 30, "850", ""),
                    ("P-Peel 20 nano-constructed", 30, "950+", ""),
                    ("P-Peel 40 nano-constructed", 30, "950+", "")]),
                ("Combos", [
                    ("Dermaplane and chemical peel add-on", 60, "850", ""),
                    ("Dermaplane and peel combo", 60, "850", "")]),
            ]),
            ("Laser rejuvenation", None, [
                ("IPL laser rejuvenation", [
                    ("Full face rejuvenation", 55, "1300+", "Treats sun damage, tightens skin, reduces pore size and brightens."),
                    ("Full face including radio frequency", 45, "1600", ""),
                    ("Full face including neck", 60, "2000", ""),
                    ("Full face, neck and décolleté", 60, "3000", ""),
                    ("Décolleté", 30, "1200", ""),
                    ("Hand rejuvenation", 30, "1000", ""),
                    ("Half arm", 45, "2000", ""),
                    ("Full arm", 60, "3000", ""),
                    ("Men's IPL rejuvenation", 30, "850", ""),
                    ("Spot treatment, per shot", 30, "50", ""),
                    ("IPL laser and peel combo", 45, "1800", "Laser skin rejuvenation followed by a selected peel."),
                    ("TriBella", 120, "4500", "IPL photofacial, radiofrequency and NanoFractional RF in one session.")]),
                ("Fractional radio frequency", [
                    ("Full face and neck", 120, "2500", ""),
                    ("Eyes", 15, "600", "Needle-free fractional RF to tighten around the eyes.")]),
                ("Laser", [
                    ("Tattoo removal", 60, "Varies", "")]),
            ]),
            ("Microneedling", None, [(None, [
                ("Lamelle hydration microneedling", 60, "900", "Full-face microneedling with a hydration serum, little to no downtime."),
                ("Anti-aging microneedling with retinol", 60, "1100", ""),
                ("RF microneedling", 120, "2500", "Microneedling combined with radio frequency energy."),
                ("Dermapen scarring treatment", 90, "Varies", ""),
                ("Dermapen stretch mark treatment", 90, "Varies", "")])]),
        ],
    },
    {
        "slug": "eyebrows-and-lashes",
        "file": "eyebrows-and-lashes.html",
        "name": "Eyebrows & Lashes",
        "short": "Professional sculpting of brows is an art so whatever it is you choose you are in good hands.",
        "intro": "Professional sculpting of brows is an art so whatever it is you choose you are in good hands. A Keratin Lash Lift lifts your natural lashes for healthy, strong lashes.",
        "img": "brows",
        "side": None,
        "tabs": False,
        "groups": [
            ("Brows", None, [(None, [
                ("Brow shape", 15, "100", ""),
                ("Brow tint", 15, "100", ""),
                ("Brow shaping with tint", 20, "180", ""),
                ("Keratin brow lamination", 60, "650", "")])]),
            ("Lash lift and tints", None, [(None, [
                ("Keratin lash lift", 60, "550", "Lifts the natural lash to reveal beautiful eyes."),
                ("Lash tint", 30, "100", ""),
                ("Lash and brow tint", 30, "180", ""),
                ("Lash tint with brow shape and tint", 40, "240", "")])]),
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
        "offer": ("6 skin tightening treatments for R2 880", "specials.html"),
        "groups": [
            ("Body sculpting", None, [(None, [
                ("Laser lipo treatment", 60, "350", "Low-level laser lipo for stubborn fatty areas. At least 10 sessions are recommended."),
                ("RF body contouring and cellulite", 45, "600", "Radio frequency for cellulite, skin smoothing and tightening."),
                ("EMSlim body sculpting", 30, "700", EMS_LINE),
                ("Body shaping combo", 90, "700", "Lipo-laser, radio frequency and cavitation, once a week for at least 8 treatments.")])]),
            ("Skin tightening", None, [(None, [
                ("Tummy", 45, "600", ""),
                ("Buttocks", 45, "600", ""),
                ("Legs, front", 45, "600", ""),
                ("Legs, back", 45, "600", ""),
                ("Knees", 45, "600", "8 treatments recommended, once a week."),
                ("Neck", 45, "600", "6 treatments recommended, once a week."),
                ("Full face", 45, "600", "6 treatments recommended, once a week."),
                ("Décolleté", 45, "600", "6 treatments recommended, once a week.")])]),
            ("Spray tan", None, [(None, [
                ("Tan Lab spray tan", 20, "350", "Sunless tanning, the healthy option.")])]),
        ],
    },
]

SPECIALS = {
    "slug": "specials",
    "file": "specials.html",
    "name": "Specials",
    "short": "Combos, packages and savings on laser hair removal.",
    "intro": "Combos, treatment packages and savings on laser hair removal. Book any special online, or message us on WhatsApp to ask which one suits you.",
    "img": "body",
    "side": None,
    "tabs": False,
    "groups": [
        ("Combos and packages", None, [(None, [
            ("Dermaplaning and microneedling combo", 60, "950", ""),
            ("Radio frequency, dermaplaning and peel combo", 60, "950", ""),
            ("Half leg laser hair removal", 30, "999", "8 to 12 sessions recommended, every 4 weeks."),
            ("Hollywood and underarm laser hair removal", 30, "1300", "10 to 12 sessions recommended, every 4 weeks."),
            ("6 EMS muscle sculpting treatments", 30, "2000", ""),
            ("6 skin tightening treatments", 45, "2880", ""),
            ("10 sessions of 5D lipo laser", 30, "3000", "Non-invasive fat reduction and body contouring."),
            ("6 EMSlim body sculpting treatments", 30, "3500", ""),
            ("8 body contouring and skin tightening treatments", 45, "3840", "")])]),
        ("Laser hair removal savings", None, [(None, [
            ("Any 2 areas, get the 3rd (cheapest) free", 30, "Varies", ""),
            ("6 to 8 session package, 15% off", 30, "Varies", ""),
            ("8 to 12 session package, 20% off", 30, "Varies", "")])]),
        ("Gift vouchers", None, [(None, [
            ("Gift voucher", 30, "Varies", "")])]),
    ],
}

# shown on the home page specials strip (names must match rows above)
HOME_SPECIALS = ["6 skin tightening treatments", "Half leg laser hair removal",
                 "Hollywood and underarm laser hair removal", "Dermaplaning and microneedling combo",
                 "10 sessions of 5D lipo laser"]
# price chips on the home hero: (page slug, row name, label)
HOME_CHIPS = [("hairless", "Lip or chin", "Laser lip or chin"),
              ("eyebrows-and-lashes", "Keratin lash lift", "Keratin lash lift"),
              ("all-about-skin", "Hydration facial", "Hydration facial")]
