import Stripe from "npm:stripe";
const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY")!);
Deno.serve(async (req) => {
  const body = await req.text();
  const event = await stripe.webhooks.constructEventAsync(body, req.headers.get("stripe-signature")!, Deno.env.get("STRIPE_WEBHOOK_SECRET")!);
  return new Response(JSON.stringify({ received: event.id }));
});
