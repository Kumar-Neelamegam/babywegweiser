/**
 * BabyWegweiser view counter — a Cloudflare Worker you deploy and own.
 *
 * It does exactly one thing: increments a number in KV and returns it.
 * No IP addresses, user agents, or request metadata are read or stored.
 * This is the only server-side component in the whole project — everything
 * else in the site is static and runs entirely in the visitor's browser.
 *
 * Bindings expected (see ../wrangler.toml):
 *   COUNTER        KV namespace, holds a single key "views"
 *   ALLOWED_ORIGIN env var, the exact origin the counter accepts requests
 *                  from (e.g. "https://your-user.github.io")
 */
export default {
  async fetch(request, env) {
    const headers = {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": env.ALLOWED_ORIGIN || "",
      "Cache-Control": "no-store",
      "Vary": "Origin",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers });
    }
    if (request.method !== "GET") {
      return new Response(JSON.stringify({ error: "method not allowed" }), {
        status: 405,
        headers,
      });
    }

    const current = parseInt((await env.COUNTER.get("views")) || "0", 10);
    const count = current + 1;
    await env.COUNTER.put("views", String(count));

    return new Response(JSON.stringify({ count }), { headers });
  },
};
