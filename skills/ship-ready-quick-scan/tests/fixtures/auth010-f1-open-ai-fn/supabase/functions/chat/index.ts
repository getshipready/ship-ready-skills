Deno.serve(async (req) => {
  const { prompt } = await req.json();
  const r = await fetch("https://api.openai.com/v1/chat/completions", { method: "POST", headers: { Authorization: `Bearer ${Deno.env.get("OPENAI_API_KEY")}` }, body: JSON.stringify({ model: "gpt-4o-mini", messages: [{ role: "user", content: prompt }] }) });
  return new Response(await r.text());
});
