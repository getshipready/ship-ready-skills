import { auth } from "@clerk/nextjs/server";
export async function GET() { const { userId } = await auth(); if (!userId) return new Response("no", {status:401}); return Response.json([]); }
export async function DELETE(req: Request) { const id = new URL(req.url).searchParams.get("id"); await db.items.delete({ where: { id } }); return Response.json({ok:true}); }
