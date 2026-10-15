// Read-only public mirror of the Neuron Jury monitor.
// GET  /api/experiment -> latest snapshot (stored gzipped in KV, served as-is)
// POST /api/push       -> replace the snapshot; requires the x-nj-token secret
// There are deliberately no control endpoints: the experiment can only be paused from the owner's machine.
const EMPTY = JSON.stringify({ status: { stages: {}, counters: {}, events: [] }, modal: { jobs: {} }, spend: {}, caps: {}, history: {}, paused: false });

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname === "/api/experiment") {
      const body = await env.LIVE.get("snapshot", "arrayBuffer");
      if (!body) return new Response(EMPTY, { headers: { "content-type": "application/json", "cache-control": "no-store" } });
      return new Response(body, {
        headers: { "content-type": "application/json", "content-encoding": "gzip", "cache-control": "no-store" },
        encodeBody: "manual",
      });
    }
    if (url.pathname === "/api/push") {
      if (req.method !== "POST") return new Response("method not allowed", { status: 405 });
      if (!env.NJ_PUSH_TOKEN || req.headers.get("x-nj-token") !== env.NJ_PUSH_TOKEN) return new Response("forbidden", { status: 403 });
      const body = await req.arrayBuffer();
      if (body.byteLength > 4_000_000) return new Response("too large", { status: 413 });
      await env.LIVE.put("snapshot", body);
      return new Response("ok");
    }
    if (url.pathname.startsWith("/api/")) return new Response("not found", { status: 404 });
    return env.ASSETS.fetch(req);
  },
};
