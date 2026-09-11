# BabyWegweiser · Schwangerschaft in Österreich

A single-file, offline-capable pregnancy guide for Austria. No backend, no
accounts, no cookies, no analytics. Everything the user types stays in their
own browser.

**Live demo:** _(fill in your GitHub Pages URL after step 6 below)_

---

## What it is

One HTML file. Open it, it works. Ships in 6 languages, tracks the 40 weeks
with fruit-and-veg size comparisons, carries the official Austrian to-do list
(Eltern-Kind-Pass, Mutterschutz, Wochengeld, Kinderbetreuungsgeld,
Familienbeihilfe, Karenz), calculates money and dates, exports reminders to
any calendar app, and links every claim back to an official source.

### Features

| | |
|---|---|
| **6 languages** | Deutsch, English, Türkçe, Bosanski·Hrvatski·Srpski, Română, Українська |
| **Week tracker** | 37 week entries with length, weight, and a produce comparison |
| **Timeline** | 22 milestones on three lanes: medical, legal, personal |
| **To-do list** | 33 official items across before / during / after pregnancy |
| **Diet plans** | Per trimester, with standard / vegetarian / vegan / halal / gestational-diabetes variants |
| **4 calculators** | Due date, Mutterschutz window, Wochengeld estimate, family benefits |
| **Calendar export** | RFC 5545 `.ics` — appointments and reminders, works in Google/Apple/Outlook |
| **Local notifications** | Browser notifications scheduled in-page, no push server |
| **Print view** | Clean stylesheet for taking the to-do list to an appointment |
| **Light / dark** | Follows the system theme, manual override |
| **Export / import** | JSON backup of your own data, sanitised on the way back in |

### Privacy — the whole point

- No server. No API. No fetch. `connect-src 'none'` in the CSP makes this
  enforceable, not just a promise. The one opt-in exception is a footer view
  counter — see below.
- All state lives in `localStorage`, with an in-memory fallback when storage
  is blocked.
- No third-party fonts, images, scripts, or trackers. Fonts are subset and
  embedded as base64. Artwork is original inline SVG.
- The only thing a host can see is the HTTP request for the page itself.
  That is stated plainly on the privacy page inside the app.

### Security

- Content-Security-Policy with per-script SHA-256 hashes, computed at build
  time. `default-src 'none'` baseline.
- Zero inline event handlers. All interaction runs through delegated
  `data-*` listeners so the hash policy can forbid inline execution.
- Imported JSON is whitelisted field by field with type and format checks —
  nothing from a file lands in state unvalidated.
- `referrer: no-referrer`, `base-uri 'none'`, `form-action 'none'`.

### View counter (optional)

The footer can show a page-load count, backed by a small Cloudflare Worker
you deploy and own — no third-party analytics service. Disabled by default
(the footer just shows a dash). See [`docs/view-counter.md`](docs/view-counter.md)
for setup; it's the only network request the site ever makes, and `mk.py`
scopes the CSP `connect-src` to exactly that one origin.

### SEO

The page ships with a meta description, Open Graph / Twitter Card tags,
`WebApplication` JSON-LD structured data, a static crawlable `<h1>` +
tagline inside `#hero` (overwritten by JS on load, seen by non-JS crawlers
and before hydration), and a `<noscript>` fallback. `robots.txt` and
`sitemap.xml` ship at the project root.

The canonical link / `og:url` tag and the two placeholder files use
`https://YOUR-USERNAME.github.io/babywegweiser/` until you set `SITE_URL`
in `mk.py` (same pattern as `COUNTER_URL`) and rebuild — replace the
placeholder in `robots.txt` and `sitemap.xml` by hand too, since those
aren't templated by `mk.py`.

---

## Files

```
babywegweiser.html          readable build   (~345 KB) — the one to read and debug
babywegweiser.min.html      minified build   (~316 KB) — the one to deploy
mk.py                       build script
build/                      source fragments (see below)
reel/                       60-second marketing videos, DE + EN, 1080×1920
pregnancy-austria-spec.md   product spec, traffic + monetisation analysis
reel-kit.md                 shot list, captions, hashtags, posting plan
security-headers.md         server header configs for various hosts
images-guide.md             image licensing, photo slots, typography, motion
view-counter.md              optional footer view counter, setup steps
worker/                      Cloudflare Worker source for the view counter
*.mjs                       Playwright test scripts
```

### `build/` fragments

| File | Contains |
|---|---|
| `p1.html` | `<head>`, design tokens, base CSS |
| `p2.html` | Body markup — header, the seven views, toasts, onboarding |
| `p3.html` | i18n core, German + English strings, `WEEKS` / `MS` / `TODO` data |
| `p4.html` | State, storage, charts, `DIET`, `DIETDAY`, `DIETPREF`, **`RATES`** |
| `p4b.html` | Applies the TR / BS / RO / UK language packs |
| `p5.html` | Tracker, to-do, diet, calculators, ICS export, notifications, init |
| `p6.html` | Icon and motion enhancement layer |
| `p7.html` | Artwork layer, **`PHOTO`** slots |
| `p8.html` | Scroll progress, tab ink, draw-in observers, confetti |
| `sprite.html` | ~44 duotone UI icons as `<symbol>` |
| `art.html` | 19 illustration symbols + gradients |
| `extra.css` … `extra4.css` | Layered styles: components, spacing, artwork, typography |
| `fonts.css` | Generated — base64 WOFF2 `@font-face` with `unicode-range` |
| `lang-*.js` | Source language packs (Turkish, BCS, Romanian, Ukrainian) |

---

## Building

Requires Python 3. For the minified build also Node with `terser` available
via `npx`.

```bash
cd /path/to/project
python3 mk.py           # writes babywegweiser.html
python3 mk.py --min     # also writes babywegweiser.min.html
```

Run it from the project root, not from inside `build/` — the paths are
relative.

`mk.py` concatenates the fragments, injects the CSS layers and the SVG
sprites, then computes a SHA-256 hash for every `<script>` block and writes
them into the CSP meta tag. **Any edit to a script block changes its hash, so
you must rebuild — editing the output HTML directly will break the CSP and
the page will silently stop running JavaScript.**

### Where to change things

- **Benefit amounts** → `RATES` in `build/p4.html`. Values are frozen at the
  2025–2027 figures. Check the linked BKA and Kinderbetreuungsgeld pages when
  the government updates them.
- **Photos** → `PHOTO` in `build/p7.html`. Empty strings by default (the app
  ships with SVG artwork only). Put a base64 data URI or a same-origin path
  in a slot and a photo frame appears in that view. Do not hotlink external
  images — the CSP blocks them and it would break the privacy promise. See
  `images-guide.md`.
- **Translations** → `build/lang-tr.js`, `lang-bs.js`, `lang-ro.js`,
  `lang-uk.js`. German is the fallback for every missing key. Official German
  terms (Eltern-Kind-Pass, Mutterschutz, Wochengeld, Kinderbetreuungsgeld,
  Familienbeihilfe, Karenz) deliberately stay German in every language —
  those are the words printed on the forms.
- **Week data** → `WEEKS` in `build/p3.html`.
- **To-do items** → `TODO` in `build/p3.html`, plus the matching entry in
  each language pack, keyed by item `id`.

### Testing

```bash
python3 -m http.server 8899          # notifications need a real origin
node t.mjs          # all views, screenshots
node m.mjs          # 390 px mobile
node d3.mjs         # horizontal-overflow check, must print docW=390
node langtest.mjs   # all 6 languages, must print ERRORS: none
node icsval.mjs     # parses the exported .ics with node-ical
node notiftest.mjs  # notification permission state machine
node rm.mjs         # prefers-reduced-motion
```

---

## Hosting on GitHub Pages — step by step

You need a GitHub account. Nothing else. It is free and it gives you HTTPS,
which the notification feature requires.

### 1. Create the repository

Go to <https://github.com/new>.

- **Repository name:** `babywegweiser` (or anything you like)
- **Visibility:** Public — GitHub Pages needs Public on free accounts
- Leave "Add a README" **unticked**, you already have one
- Click **Create repository**

### 2. Prepare the files locally

GitHub Pages serves `index.html` at the root of the site. Copy the minified
build to that name:

```bash
cd /path/to/project
cp babywegweiser.min.html index.html
```

Add an empty `.nojekyll` file so GitHub does not run the Jekyll processor
over your HTML:

```bash
touch .nojekyll
```

### 3. Push it

```bash
git init
git add index.html .nojekyll README.md
git commit -m "BabyWegweiser: initial site"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/babywegweiser.git
git push -u origin main
```

Replace `YOUR-USERNAME`. If GitHub asks for a password, it wants a Personal
Access Token, not your account password — create one at **Settings ▸
Developer settings ▸ Personal access tokens ▸ Tokens (classic)** with the
`repo` scope.

You can commit the whole project (`build/`, `mk.py`, the docs) too. Only
`index.html` gets served; the rest is just source history.

### 4. Turn on Pages

In your repository on github.com:

1. Click **Settings** (top bar of the repo)
2. Click **Pages** in the left sidebar
3. Under **Build and deployment ▸ Source**, choose **Deploy from a branch**
4. Under **Branch**, choose **main** and folder **/ (root)**
5. Click **Save**

### 5. Wait for the build

Go to the **Actions** tab. A "pages build and deployment" job runs. It takes
about one to two minutes. When the tick turns green, the site is live.

### 6. Open your site

```
https://YOUR-USERNAME.github.io/babywegweiser/
```

The URL is also shown at the top of **Settings ▸ Pages**. Put it in the
"Live demo" line at the top of this README.

### 7. Enforce HTTPS

Still in **Settings ▸ Pages**, tick **Enforce HTTPS**. It may be greyed out
for a few minutes while the certificate is issued. This matters: browser
notifications only work in a secure context, and the app will show
"insecure context" instead of the permission button over plain HTTP.

### 8. Updating the site later

```bash
python3 mk.py --min
cp babywegweiser.min.html index.html
git add -A
git commit -m "Update content"
git push
```

Pages redeploys automatically within a minute or two. If you do not see the
change, hard-refresh (Ctrl+Shift+R / Cmd+Shift+R) — the browser caches
aggressively.

### 9. Optional: your own domain

If you own e.g. `babywegweiser.at`:

1. Create a file named `CNAME` in the repository root containing exactly
   `babywegweiser.at` and push it.
2. At your DNS provider, for the apex domain add four **A** records pointing
   to `185.199.108.153`, `185.199.109.153`, `185.199.110.153`,
   `185.199.111.153`. For a `www` subdomain add a **CNAME** record pointing
   to `YOUR-USERNAME.github.io`.
3. In **Settings ▸ Pages ▸ Custom domain**, enter the domain and click
   **Save**. Wait for the DNS check to pass, then tick **Enforce HTTPS**
   again.

DNS changes can take up to 24 hours to propagate.

### A note on security headers

`security-headers.md` in this repo contains `_headers`, `.htaccess`, and
nginx configurations. **None of them work on GitHub Pages** — it does not let
you set custom response headers. On GitHub Pages your protection is the
in-page `<meta http-equiv="Content-Security-Policy">` tag that `mk.py`
generates, which covers the important parts. If you later want real
`Strict-Transport-Security`, `X-Frame-Options`, and `Permissions-Policy`
headers, move to Cloudflare Pages or Netlify — both are free, both read the
`_headers` file, and the deploy step is the same drag-and-drop of one file.

---

## Before you promote it publicly

Two things are your responsibility, not the app's:

1. **Impressum.** Austrian law (§ 5 ECG, § 24 MedienG) requires an imprint on
   a publicly reachable website. The app does not ship one because it cannot
   know who you are. Add your name and contact address to the privacy view in
   `build/p2.html` before you share the link widely.
2. **Medical disclaimer.** The app already states that it is information, not
   medical advice, and that a midwife or doctor decides. Do not weaken that
   wording. Do not add symptom-checking or dosage features.

Figures are frozen at their 2025–2027 values and every one of them links to
the official source. Re-check them each January.

---

## Official sources

All content links back to: oesterreich.gv.at, sozialministerium.gv.at,
gesundheit.gv.at, ÖGK (gesundheitskasse.at), Bundeskanzleramt
(bundeskanzleramt.gv.at), Arbeiterkammer (arbeiterkammer.at), and the
Frühe Hilfen network (fruehehilfen.at).

## Licence

Code and artwork: yours to do with as you like. The content summarises
publicly available official Austrian information; the linked authorities own
the underlying material.
