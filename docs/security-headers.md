# Security headers — server-side companion to the in-page CSP

The HTML file already carries a strict Content Security Policy in a `<meta>` tag, so it
is protected even when opened straight from disk. Three headers **cannot** be delivered
via `<meta>` and must come from the server. Drop the matching file next to the HTML.

---

## Cloudflare Pages / Netlify — `_headers`

```
/*
  Content-Security-Policy: default-src 'none'; script-src 'self'; style-src 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'none'; object-src 'none'; frame-src 'none'; worker-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: no-referrer
  Permissions-Policy: geolocation=(), camera=(), microphone=(), payment=(), usb=(), interest-cohort=()
  Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
  Cross-Origin-Opener-Policy: same-origin
  Cross-Origin-Resource-Policy: same-origin
  Cache-Control: public, max-age=0, must-revalidate
```

> Note: the header CSP above intentionally omits the script hashes — the `<meta>` CSP in
> the file already carries them, and the browser enforces **both** policies, taking the
> strictest of each directive. If you prefer a single source of truth, copy the exact
> `script-src 'sha256-…'` list out of the file's `<meta>` tag into the header and delete
> the meta tag.

## Apache — `.htaccess`

```apache
<IfModule mod_headers.c>
  Header always set X-Frame-Options "DENY"
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "no-referrer"
  Header always set Permissions-Policy "geolocation=(), camera=(), microphone=(), payment=()"
  Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
  Header always set Cross-Origin-Opener-Policy "same-origin"
</IfModule>
```

## nginx

```nginx
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer" always;
add_header Permissions-Policy "geolocation=(), camera=(), microphone=(), payment=()" always;
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header Cross-Origin-Opener-Policy "same-origin" always;
```

---

## What each one buys you

| Header | Protects against |
|---|---|
| `Content-Security-Policy` | Injected or third-party scripts. With `default-src 'none'` the page may not call, fetch or embed **anything** external. |
| `frame-ancestors` / `X-Frame-Options` | Clickjacking — nobody can put your site in an invisible iframe over their own buttons. |
| `X-Content-Type-Options: nosniff` | The browser guessing a file is a script when it isn't. |
| `Referrer-Policy: no-referrer` | Leaking which page a visitor came from to gesundheit.gv.at and the other outbound links. Fits the privacy promise. |
| `Permissions-Policy` | Silently claiming camera, microphone or location. The site needs none of them. |
| `Strict-Transport-Security` | Downgrade to plain HTTP. Also a precondition for notifications, which need a secure context. |
| `Cross-Origin-Opener-Policy` | Another window keeping a handle on yours after `window.open`. |

## Verify after deploying

- <https://securityheaders.com> — should grade A or A+
- <https://csp-evaluator.withgoogle.com> — paste the policy from the `<meta>` tag
- Open DevTools → Console on the live site: any CSP violation prints there. It should be silent.
