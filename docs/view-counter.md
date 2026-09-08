# View counter

The site's footer shows how many times the page has loaded. This is the one
deliberate exception to "no server, no fetch, no third party" — everything
else in BabyWegweiser stays fully client-side. If you don't want the
exception, skip this doc entirely; the counter fails silently and just
doesn't render a number.

The counter is a small [Cloudflare Worker](https://workers.dev) that you
deploy and own. It stores a single integer in Cloudflare KV and does nothing
else — no IPs, no user agents, no logs, no analytics. Free tier covers
100,000 reads and 1,000 writes per day, i.e. up to ~1,000 page loads/day
before you'd need a paid KV plan.

## 1. Create the Worker

You need a free Cloudflare account and Node installed.

```bash
cd worker
npm install -g wrangler   # or use `npx wrangler` below instead
wrangler login
```

## 2. Create the KV namespace

```bash
wrangler kv namespace create COUNTER
```

This prints an `id`. Open `worker/wrangler.toml` and paste it in place of
`REPLACE_WITH_KV_NAMESPACE_ID`.

## 3. Set the allowed origin

Edit `worker/wrangler.toml` and set `ALLOWED_ORIGIN` to your site's exact
origin, e.g. `https://YOUR-USERNAME.github.io` (no path, no trailing slash).
This only affects the CORS header the Worker sends back — it does not stop
someone from hitting the Worker URL directly and inflating the count. That's
a general limitation of any public hit counter, not something worth building
rate-limiting infrastructure around here.

## 4. Deploy

```bash
wrangler deploy
```

Wrangler prints the live URL, something like:

```
https://babywegweiser-counter.your-subdomain.workers.dev
```

## 5. Wire it into the site

Open `mk.py` at the project root and set:

```python
COUNTER_URL = "https://babywegweiser-counter.your-subdomain.workers.dev"
```

Rebuild and redeploy the site:

```bash
python3 mk.py --min
cp babywegweiser.min.html index.html
git add -A
git commit -m "Enable view counter"
git push
```

`mk.py` automatically adds that one origin to the page's `connect-src` CSP
directive — every other network destination stays blocked at
`default-src 'none'`. Leaving `COUNTER_URL` at its placeholder value keeps
`connect-src 'none'` and ships the site with the counter silently disabled,
exactly as before this feature existed.

## Updating the count display

The footer fetches the count once per page load and writes it into
`#viewCountN`. There's no polling, no websockets, and no counting of unique
visitors — it's a page-load counter, same as a classic hit counter.
