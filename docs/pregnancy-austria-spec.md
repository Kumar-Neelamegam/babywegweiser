# Pregnancy Austria — Product & Build Specification

**Working title options:** `Schwanger.at`-style brand — suggestions: **BabyWegweiser**, **Neun Monate Österreich**, **MamaPapa.at**, **SSW Österreich**
**Status:** Specification for review — no code written yet
**Date:** 16 August 2026

---

## 1. What this is in one sentence

A free, multilingual, privacy-first pregnancy companion for anyone living in Austria that combines **official Austrian medical + legal + financial milestones** (Eltern-Kind-Pass, Mutterschutz, Wochengeld, Kinderbetreuungsgeld) with a **personal week-by-week tracker** — where every piece of personal data stays on the user's own device and is never sent to any server.

**Why it wins:** existing Austrian pregnancy sites are either (a) medical portals with no personalisation, or (b) German (DE) apps that give *German* law, not Austrian. Nobody serves the ~25% of Austrian residents whose first language isn't German with correct *Austrian* rules. That gap is the whole business.

---

## 2. Target users

| Segment | Need | Why they come back |
|---|---|---|
| First-time parents in Austria (primary) | "What do I have to do, and when?" | Weekly checklist + deadline reminders |
| Non-German-speaking residents | Austrian rules in their language | Nowhere else has this |
| Partners / fathers | Papamonat, Familienzeitbonus deadlines | Partner mode |
| Second+ time parents | Refresher on money & deadlines only | Calculators |
| Midwives / advisors | A link they can hand to clients | B2B / directory revenue |

**First-baby mode** is the default: nothing assumes prior knowledge, every term (SSW, EKP, Karenz, Wochengeld) has a one-tap plain-language explainer.

---

## 3. Official source base (everything links back)

All content is **summarised + linked**, never presented as our own medical or legal authority.

| Topic | Official source |
|---|---|
| Eltern-Kind-Pass examinations | gesundheit.gv.at — Eltern-Kind-Pass |
| Eltern-Kind-Pass overview & law | sozialministerium.gv.at |
| Rights, forms, procedures | oesterreich.gv.at (Familie und Partnerschaft) |
| Family benefit amounts | bundeskanzleramt.gv.at — Familienportal |
| Wochengeld, Mutterschutz, Karenz | ÖGK (gesundheitskasse.at) + Arbeiterkammer |
| Kinderbetreuungsgeld | bundeskanzleramt.gv.at / ÖGK |
| Free family support networks | fruehehilfen.at |
| Workplace protection | arbeitsinspektion.gv.at (Mutterschutzgesetz) |

### Verified facts already collected

**Eltern-Kind-Pass — pregnancy examinations (all 5 required in full for full Kinderbetreuungsgeld):**

| # | Window | Contents |
|---|---|---|
| 1 | by end of week 16 | history, gynae exam, due date; blood: group/Rh, Hb/Hkt, syphilis, rubella, toxoplasmosis, HIV offer |
| 2 | weeks 17–20 | gynae + internal exam |
| 3 | weeks 25–28 | gynae, Hb/Hkt, Hepatitis B, **oGTT** (gestational diabetes) |
| 4 | weeks 30–34 | gynae incl. cervix assessment |
| 5 | weeks 35–38 | urine, weight, blood pressure, abdominal circumference, extended gynae exam |

**Ultrasounds (3, not a KBG prerequisite):** weeks 8–12 · 18–22 · 30–34
**Midwife consultation:** weeks 18–22, ~1 hour

**Money (rates frozen at 2025 levels through 2027):**
- Familienbeihilfe/month: €138.40 (0–2) · €148.00 (3–9) · €171.80 (10–18) · €200.40 (19+)
- Kinderabsetzbetrag €70.90/month · Mehrkindzuschlag €24.40 · Schulstartgeld €121.40
- Kinderbetreuungsgeld: flat **€41.14/day**, income-dependent max **€80.12/day**
- Familienzeitbonus: **€54.87/day**
- Sibling bonus per child: €8.60 (2) · €21.10 (3) · €32.10 (4) · €38.90–63.10 (5+)

> Every number on the site carries a "Stand: <date> · Quelle: <official link>" stamp, and a single `data/official-rates.json` file so annual updates are a one-file edit.

---

## 4. Languages

Austria's official language is German; Burgenland-Croatian, Slovene and Hungarian have regional official status; Czech, Slovak and Romani are recognised Volksgruppen languages. The people who actually need this most also speak Turkish, BKS, Romanian, Ukrainian and Arabic.

**Phase 1 (launch):** Deutsch · English · Türkçe · Bosanski/Hrvatski/Srpski · Română · Українська
**Phase 2:** Slovenščina · Magyar · Burgenland-Croatian · Čeština · Slovenčina · Romani
**Phase 3 (highest traffic upside):** العربية · فارسی/دری — needs RTL layout, which the CSS is built for from day one.

Implementation: one JSON file per locale, URL-prefixed routes (`/de/`, `/en/`, `/tr/` …), `hreflang` tags for SEO, language switcher that preserves the current page. Official terms (Wochengeld, Mutterschutz, Eltern-Kind-Pass) always stay in German next to the translation — because that's the word on the form the user has to fill in.

---

## 5. Privacy architecture — the "nothing on our server" promise

| Layer | Decision |
|---|---|
| Backend | **None.** Fully static site. |
| Personal data | `localStorage` + `IndexedDB` on the user's device only |
| Accounts | None. No email, no login, no sign-up. |
| Cookies | None → **no cookie banner needed** |
| Analytics | Cookieless, aggregate-only, no personal data (Cloudflare Web Analytics) — or fully off, your call |
| Backup | "Export my data" → downloads a JSON file the user keeps; "Import" restores it |
| Device sync | Optional QR-code handoff between phone and laptop (data encoded in the link, still no server) |

**Honesty note:** any web host writes standard access logs (IP, user agent). So the wording is precise: *"Your entries never leave your device"* — not the unprovable *"we log nothing at all."* The privacy page will state exactly what the CDN sees, which is itself a trust asset.

**Consequence to accept:** true push notifications require a push server. The no-server-compliant alternatives are (a) local scheduled notifications while the PWA is installed, and (b) **.ics calendar export** — one tap adds every Eltern-Kind-Pass window and legal deadline to the user's own Google/Apple/Outlook calendar. (b) is actually more reliable than push and costs nothing.

---

## 6. Feature set

### 6.1 Onboarding (60 seconds, skippable, all local)
Due date (from last period **or** ultrasound date) → first baby? → Bundesland → employment status (employed / self-employed / student / not employed) → language → partner mode on/off → multiples. That's it. Every answer only unlocks relevant content; nothing is required.

### 6.2 Dashboard
Current SSW, days to go, trimester ring, "this week's 3 things", next official deadline with a countdown, next Eltern-Kind-Pass window.

### 6.3 Trimester tracker with fruit + vegetable size
Week-by-week baby size, weight, length — illustrated with produce people in Austria actually buy. Sample:

| SSW | Größe | Vergleich |
|---|---|---|
| 5 | 2 mm | Sesamkorn |
| 8 | 1.6 cm | Himbeere |
| 12 | 5.4 cm | Marille |
| 16 | 11.6 cm | Avocado |
| 20 | 25 cm | Banane |
| 24 | 30 cm | Melanzani |
| 28 | 37 cm | Melanzani/Karfiol |
| 32 | 42 cm | Kohlrabi-Bund |
| 36 | 47 cm | Kopfsalat |
| 40 | 51 cm | Wassermelone / Kürbis |

Local produce names (Marille, Melanzani, Erdapfel, Karfiol, Kürbis) are a small thing that makes it feel Austrian rather than translated.

### 6.4 Charts (per the dataviz standard — accessible, light + dark)
1. **Before / During / After timeline** — the headline graphic: one horizontal chart spanning pre-conception → 40 weeks → 12 months after birth, with three swim lanes: *Medical* (EKP exams, ultrasounds, midwife hour), *Legal* (employer notification, Mutterschutz start/end, Karenz notice deadlines), *Money* (Wochengeld, KBG, Familienzeitbonus, Familienbeihilfe).
2. Trimester progress ring
3. Growth curve (baby length/weight vs. week)
4. Personal log: weight, blood pressure, symptoms — device-only, with an "export for my doctor" print view
5. Money timeline — what lands in your account, when
6. Kick counter + contraction timer (third trimester)

### 6.5 Official TODO lists

**Before pregnancy** — folic acid 400 µg, rubella/varicella immunity check, dentist visit, stop smoking/alcohol, medication review, e-card/insurance status, get an Eltern-Kind-Pass-issuing doctor.

**During pregnancy** — the 5 EKP exams and 3 ultrasounds in their windows · midwife hour (18–22) · notify employer (this is what triggers legal protection) · Mutterschutz starts 8 weeks before due date · choose hospital/Hebamme and register · Geburtsvorbereitungskurs · pre-register the birth at the Standesamt · pack the Kliniktasche · decide KBG variant (Konto vs. income-dependent) · Familienzeitbonus notification deadlines for the partner.

**After birth** — birth registration & Geburtsurkunde · Meldezettel for the baby · e-card / insurance registration · Familienbeihilfe (largely automatic — the site explains when it isn't) · Kinderbetreuungsgeld application to ÖGK · Wochengeld for the 8 weeks after birth · child EKP examinations on schedule (these gate the full KBG) · Karenz notification deadlines · vaccination plan · Frühe Hilfen if support is wanted.

Each item: what · when (auto-dated from the due date) · which authority · official link · optional calendar export. Checked state stored locally.

### 6.6 Diet plans per trimester
Trimester-specific guidance built on official Austrian nutrition recommendations (Richtig essen von Anfang an / Gesundheitsportal): what to eat more of, the **food safety list** (raw milk cheese, raw meat/fish, unwashed salad — listeria/toxoplasmosis), caffeine and alcohol, iron/folate/iodine/omega-3, realistic extra-calorie figures per trimester, plus 7-day sample plans in **vegetarian / vegan / halal / no-pork / lactose-free / gestational-diabetes-friendly** variants. Non-negotiable framing: general information, not individual medical advice; always defer to the treating doctor or midwife.

### 6.7 Reminders & notifications
Auto-generated from the due date: EKP windows, legal deadlines, appointments the user adds. Delivery: in-app badges, installed-PWA local notifications, and **.ics export** (single event or the whole plan) so reminders live in the user's own calendar. No email, no account.

### 6.8 Calculators (the SEO engine)
Due-date calculator · SSW calculator · Wochengeld estimator · Kinderbetreuungsgeld Konto vs. income-dependent comparison · Mutterschutz start/end dates · Familienzeitbonus. All client-side, all shareable by URL without storing anything.

### 6.9 Partner mode
Separate checklist for the second parent: Papamonat/Familienzeitbonus deadlines (these are strict), Karenz split, what to do at the birth, what to do in the first 8 weeks.

### 6.10 Accessibility & reach
WCAG 2.1 AA, works on a €100 Android phone, full offline mode via service worker, print-friendly checklists, ~150 KB first load.

---

## 7. Technical plan

- **Astro** static site + React islands for the interactive parts, Tailwind, TypeScript
- Content in Markdown/JSON → 40 SSW pages × N languages generated at build time
- Charts: hand-built accessible SVG (no heavy chart library)
- PWA: installable, offline-first service worker
- Hosting: Cloudflare Pages or Netlify — free tier, global CDN, HTTPS
- Domain: `.at` domain (~€15/yr) is a meaningful local-SEO signal
- Repo + CI: GitHub → auto-deploy on push
- **Running cost at launch: domain only.**

### Legal must-haves for an Austrian site
Impressum (ECG §5 / MedienG), Datenschutzerklärung, medical disclaimer on every health page, "last reviewed" date on every content page. These are cheap to do right and expensive to skip.

---

## 8. Traffic strategy

1. **Programmatic SEO:** 40 week-pages ("SSW 12: Größe, Untersuchungen, was jetzt wichtig ist") × 6 languages ≈ 250+ indexed pages, each answering a real search.
2. **Calculator pages** rank for high-intent queries: *Wochengeld berechnen*, *Mutterschutz wann beginnt*, *Kinderbetreuungsgeld Rechner*, *errechneter Geburtstermin*.
3. **Zero-competition multilingual long tail:** "Wochengeld Österreich" in Turkish, Romanian, Ukrainian, BKS — essentially nobody is targeting these.
4. **Bundesland pages:** Frühe Hilfen contacts, hospitals with maternity wards, regional grants (Wien, NÖ, OÖ, Stmk…).
5. **Free printables** (Kliniktasche checklist, Geburtsplan, Behörden-Checkliste) — Pinterest and WhatsApp forwarding do the distribution.
6. **Distribution partners:** Hebammen, Geburtsvorbereitungskurse, Frühe Hilfen networks, Facebook groups for parents in Vienna, Reddit r/Austria, migrant community groups.
7. **Short video** (see §10) on Instagram Reels / TikTok / YouTube Shorts.

Realistic path: 0 → 5k monthly visits in 6 months with consistent content, 30k+ by month 18 if the multilingual pages land.

---

## 9. Monetisation after reach

Ordered by how early each becomes viable — all of them keep the "no personal data on a server" promise intact.

| Stage | Channel | Notes |
|---|---|---|
| ~1k/mo | Affiliate (Amazon.at PartnerNet, Awin: baby-walz, myToys) | contextual, clearly labelled |
| ~3k/mo | Premium printable packs (Geburtsplan, Behörden-Mappe, 40-week journal) | sold via Gumroad/Stripe link — payment lives on their platform, site stays serverless |
| ~5k/mo | **Paid directory listings**: midwives, birth-prep courses, prenatal yoga, photographers, per Bundesland | best margin, recurring, B2B — a Hebamme will pay €15–30/month for a listing in front of exactly her clients |
| ~10k/mo | Direct sponsorships: insurers (Kinder-Zusatzversicherung), pharmacies, dm/BIPA, prenatal clinics | Austrian parenting audience is a premium ad segment |
| ~25k/mo | Display ads (Ezoic → Mediavine at 50k sessions) | keep density low, or skip entirely and lean on directory + sponsorship |
| Anytime | **B2B white-label**: Gemeinden, Krankenkassen, employers, Apotheken license a branded version | the highest-value path; the privacy story is the sales pitch |
| Anytime | Consulting spin-off: "relocation + family benefits in Austria" advisory | fits your existing side-business direction |

Deliberately **not** doing: selling data (there is none), gated accounts, or anything that would break the privacy claim — the claim *is* the moat.

---

## 10. 60-second marketing reel — shot list

**Format:** 9:16, 1080×1920, subtitles burned in (85% watch muted), German version + English version, same cuts.
**Hook rule:** the promise lands in the first 2 seconds.

| Time | Visual | On-screen text (DE) | VO / caption |
|---|---|---|---|
| 0–3s | Phone in hand, pregnancy test on a table, quick zoom | **"Schwanger in Österreich. Und jetzt?"** | Hook |
| 3–8s | Fast cuts: stack of official forms, confusing website, sighing | "Mutterschutz? Wochengeld? Eltern-Kind-Pass?" | The pain |
| 8–14s | Site loads, onboarding: due date entered | "Ein Termin. Fertig." | Solution reveal |
| 14–22s | Dashboard: SSW counter, trimester ring, next deadline countdown | "Dein Plan – Woche für Woche" | Personalisation |
| 22–30s | Fruit/veg size animation cycling 8→20→32 SSW | "Wie groß ist dein Baby gerade?" | The shareable moment |
| 30–38s | Before/During/After timeline chart drawing itself | "Alle Fristen. Offiziell. Automatisch." | Authority |
| 38–45s | Language switcher cycling DE → EN → TR → BKS → RO → UK | "In deiner Sprache." | Differentiator |
| 45–52s | Checklist items ticking, calendar reminder popping | "Erinnerungen, To-do-Listen, Ernährungspläne" | Depth |
| 52–57s | Lock icon, phone with "0 KB an Server gesendet" | **"Deine Daten bleiben auf deinem Handy. Kein Konto. Kein Server."** | Trust punchline |
| 57–60s | Logo + URL + "kostenlos" | **"Jetzt kostenlos starten"** | CTA |

**Music:** warm, soft-percussive, ~110 BPM, build at 30s, drop out at 52s so the privacy line lands in near-silence.
**Deliverables:** the reel, a 15s cutdown (privacy angle only), 6 static carousel posts, and localised caption/hashtag sets.

---

## 11. Build phases

| Phase | Contents | Effort |
|---|---|---|
| **1 — Core** | Static site, DE + EN, onboarding, dashboard, SSW tracker + fruit sizes, before/during/after chart, 3 TODO lists, local storage, privacy page, Impressum | v1 shippable |
| **2 — Depth** | Diet plans, reminders + .ics export, calculators, partner mode, PWA/offline, export/import | |
| **3 — Reach** | TR / BKS / RO / UK, 40 SSW content pages, Bundesland pages, printables | |
| **4 — Revenue** | Directory module, affiliate slots, sponsorship placements, B2B white-label build | |

---

## 12. Open decisions for you

1. **Delivery format** — one self-contained HTML file (instantly viewable, easy to host anywhere) vs. a proper Astro multi-page project (needed for the SEO plan) vs. both (single-file prototype first, then the real build).
2. **Language scope for v1** — DE + EN only, or DE + EN + TR + BKS from the start.
3. **Analytics** — completely none (purest claim) vs. cookieless aggregate-only (needed to prove traffic to sponsors).
4. **Reel** — script only, or should I also produce the actual assets in Canva.
5. **Brand name + domain** — pick from the suggestions or your own.
