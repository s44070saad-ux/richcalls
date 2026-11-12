import siteHtml from "../../content/site.html";

export const dynamic = "force-dynamic";

const TRADES = new Set([
  "plumbing",
  "electrical",
  "hvac",
  "roofing",
  "windows",
  "solar",
  "siding",
  "landscaping",
  "pest-control",
]);

function render(view: string, trade = ""): Response {
  let html = siteHtml as unknown as string;
  html = html
    .replaceAll("__SUPABASE_URL__", process.env.NEXT_PUBLIC_SUPABASE_URL ?? "")
    .replaceAll("__SUPABASE_ANON_KEY__", process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? "")
    .replaceAll("__RC_VIEW__", view)
    .replaceAll("__RC_TRADE__", trade);
  return new Response(html, {
    headers: { "Content-Type": "text/html; charset=utf-8" },
  });
}

export async function GET(
  _req: Request,
  { params }: { params: { path?: string[] } }
) {
  const parts = params.path ?? [];
  if (parts.length === 0) return render("home");
  if (parts.length === 1 && parts[0] === "home-services") return render("home-services");
  if (parts.length === 2 && parts[0] === "trades" && TRADES.has(parts[1]))
    return render("trade", parts[1]);
  return new Response("Not found", { status: 404 });
}
