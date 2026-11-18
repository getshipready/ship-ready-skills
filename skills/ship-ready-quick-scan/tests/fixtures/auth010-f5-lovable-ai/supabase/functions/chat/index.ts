Deno.serve(async (req) => {
  const { messages } = await req.json();
  const r = await fetch("https://ai.gateway.lovable.dev/v1/chat/completions", { method: "POST", headers: { Authorization: `Bearer ${Deno.env.get("LOVABLE_API_KEY")}` }, body: JSON.stringify({ model: "google/gemini-2.5-flash", messages }) });
  return new Response(r.body);
});
