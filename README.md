# Heaven On Earth Skin, Body, Laser Studio: website concept

Concept website for Heaven On Earth Skin, Body, Laser Studio (VIP Village, Ruimsig, Roodepoort), designed by Pablo Lebelo (mrpoint.online).

Not the official website of Heaven On Earth Skin & Body Studio. Every page is marked `noindex` (meta tag and `X-Robots-Tag` header) and carries a "concept preview" banner.

## What it is

A multi-page static site with no build step at deploy time:

| Page | File |
| --- | --- |
| Home | `index.html` |
| About and team | `about.html` |
| Services overview | `services.html` |
| Lashes by Chanté | `lashes-by-chante.html` |
| Hairless (laser hair removal and waxing) | `hairless.html` |
| All About Skin | `all-about-skin.html` |
| Eyebrows & Lashes | `eyebrows-and-lashes.html` |
| Slim Me Up | `slim-me-up.html` |
| Online booking (demo flow) | `book.html` |
| Contact and map | `contact.html` |

The Services menu is a dropdown with one page per treatment area. Treatments, prices, durations, text, logo and photos come from the studio's current website (heavenonearthskinandbody.co.za). Photos are loaded from that site.

The booking flow and the contact form are demos: nothing is booked, stored or sent, and the times shown are samples.

## Editing

The pages are generated from `tools/build.py`, which holds all treatments and prices in one place.

```
python3 tools/build.py
```

Then commit the regenerated `.html` files. `styles.css`, `site.js` and `book.js` are edited directly.

## Deploying on Cloudflare

Workers & Pages, then Import a repository. There is no build command; the repository root is served as static assets (`.assetsignore` keeps `tools/` and this file out).
