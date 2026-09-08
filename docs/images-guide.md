# Images — what I shipped, and how to add photos

## Short version

Every illustration now in the page is **original SVG artwork drawn for this project**.
No stock licence, no attribution line, no external request, no CSP change, ~9 KB for
the whole set. That was deliberate, and the reasons are below. If you want real
photographs on top of it, the page already has slots for them — one line each.

---

## About the Magnific link you sent

`magnific.com` is **Freepik rebranded** (Freepik acquired Magnific in 2024 and has
since moved its stock library onto that domain). That matters, because Freepik's
free tier is *not* the same thing as a public-domain licence:

- Free assets require an **attribution line** ("Designed by Freepik" or equivalent)
  on the page or in the credits.
- The free licence restricts redistribution and standalone use of the asset.
- Anything marked Premium needs an active paid subscription, and the licence is tied
  to that subscription staying active.

For a public health-adjacent site that you may later license to a Gemeinde or an
insurer (the B2B path in the original plan), a licence with attribution strings
attached is friction you don't need. The sources below have none.

I also could not pull images from that domain directly — it disallows automated
fetching in its robots.txt, and I don't work around that.

---

## Where to get genuinely free photos

| Source | Attribution | Commercial use | Watch out for |
|---|---|---|---|
| **Unsplash** | **Not required** ("You do not need to ask permission from or provide credit… although it is appreciated") | Yes | You may not "compile images from Unsplash to replicate a similar or competing service" |
| **Pexels** | Not required | Yes | No identifiable people in a way that implies endorsement; don't resell unaltered |
| **Pixabay** | Not required | Yes | Content licence, not CC0 anymore — check per-asset |
| **Wikimedia Commons** | **Usually required** (CC-BY / CC-BY-SA) | Yes | Per-file licence varies; the share-alike ones are viral |
| Magnific / Freepik free | **Required** | Yes | Restrictions on redistribution |

**For this site specifically:** pregnancy photography almost always contains an
identifiable person. Both Unsplash and Pexels licence the *photographer's* copyright,
not the *subject's* likeness rights. On a health site the safest choices are hands on
a belly, a bump silhouette, a nursery detail, produce, or a midwife's hands — imagery
where nobody is identifiable. That sidesteps model-release questions entirely.

Good search terms: `pregnancy silhouette`, `baby bump hands`, `nursery detail`,
`midwife hands`, `newborn feet`, `vegetables flat lay`.

---

## How to drop a photo in

Near the top of the artwork script there is one config object:

```js
const PHOTO={ hero:"", track:"", diet:"", todo:"", credit:"" };
```

Fill a slot and that section renders a wide photo banner with a readable text scrim
over it. Leave it empty and the illustration stays. Two ways to fill it:

**A · Local file (recommended for a real deployment)**

```js
const PHOTO={ hero:"img/hero.jpg", track:"", diet:"img/veg.jpg", todo:"", credit:"Photo: Unsplash" };
```

Put the files next to the HTML in an `img/` folder. Already allowed by the CSP
(`img-src 'self' data:`) — nothing to change.

**B · Embedded, so the file stays self-contained**

```bash
# resize + compress first, then inline as a data: URI
magick hero.jpg -resize 1600x -quality 78 hero-small.jpg
python3 -c "import base64;print('data:image/jpeg;base64,'+base64.b64encode(open('hero-small.jpg','rb').read()).decode())" > hero.txt
```

Paste the result into the slot. Keeps the one-file property and the offline
behaviour, at roughly 130–180 KB per photo.

**What NOT to do:** hotlink `images.unsplash.com` or any CDN. It would break the CSP,
and every visitor's IP and referrer would be handed to a third party — which
contradicts the privacy page, the strongest claim the product has.

---

## Optimise before shipping

```bash
# JPEG, 1600px wide is plenty for a 21:9 banner
magick in.jpg -resize 1600x -strip -quality 78 out.jpg

# or WebP, roughly 30% smaller again
magick in.jpg -resize 1600x -strip -quality 72 out.webp
```

Target under 150 KB per image. The slots already set `loading="lazy"` and
`decoding="async"`, so photos below the fold cost nothing on first paint.

---

## What the illustrations cover

| Where | Artwork |
|---|---|
| Hero | Arcs, drawn baby-in-the-round motif, leaf, dots — masked so it never fights the text |
| Trimester cards | Three scenes: sprout, blossom, moon |
| Week tracker orb | The same motif, faded behind the produce |
| To-do lists | Clipboard with ticks |
| Nutrition | Bowl with vegetables |
| Reminders | Bell with sound arcs |
| Calculators | Calculator and coin |
| Privacy | Shield with padlock |
| Empty log | Chart with a sprouting plant |
| Footer | Parent holding a swaddled baby |

All of it uses CSS custom properties for colour, so the whole set re-tints itself in
dark mode rather than looking like a pasted-on light-mode graphic.

---

# Typography

**Poppins**, subsetted to Latin and embedded straight into the file as WOFF2 —
**9 KB per weight**, two weights (500, 700). SIL Open Font License 1.1, so it can be
embedded and redistributed freely, including commercially.

- Headings, the logo, stat numbers and money figures use Poppins.
- Body text stays on the **system UI face** — it is already on the device, renders
  instantly, and covers every script the site speaks.
- The `@font-face` carries a `unicode-range` limited to Latin, so **Ukrainian never
  falls into a synthesised or mismatched style** — Cyrillic headings simply use the
  system face. `font-synthesis-weight:none` stops browsers faking a bold.
- `font-display:swap` — text is readable before the font arrives, and since the font
  is inline there is no network round trip at all.

**Fluid scale.** Every size is a `clamp()` between a 360px phone and a 1200px desktop,
so type grows smoothly instead of jumping at breakpoints. Headings use
`text-wrap:balance` (no orphaned last word), body copy uses `text-wrap:pretty`.

**Long-word handling.** German and Ukrainian produce compounds like
*Kinderbetreuungsgeld-Variante* that overflow narrow columns. Hyphenation is enabled
per language via the `lang` attribute the app already sets.

**Numbers.** Stat values, the money column and table figures use
`font-variant-numeric:tabular-nums`, so digits line up in columns and a counting
animation doesn't make the layout jitter.

The CSP was updated to `font-src 'self' data:` to allow the embedded face — that is
the only change, and it still permits nothing external.

# Motion

| Where | What happens |
|---|---|
| Top of page | Scroll progress bar |
| Tab bar | Indicator glides between tabs |
| Hero | Motif breathes slowly; artwork masked so text always wins |
| Week tracker orb | Heartbeat ring pulses outward |
| All artwork | Fades up and strokes draw themselves in when scrolled into view |
| Trimester bars | Fill animates, with a slow light sweep across the active one |
| Primary buttons | Slow gradient drift, sheen on hover |
| Chips | Spring on selection |
| To-do items | Tick pops, the row flashes green |
| Finishing a phase | Confetti burst |
| Week strip | Active week pops and scrolls itself into view |

Every one of these is disabled under `prefers-reduced-motion: reduce` — verified: no
scroll bar is injected, all artwork renders at full opacity immediately, and nothing
is left mid-animation.
