import { auth } from "@clerk/nextjs/server";
async function requireUser() { const { userId } = await auth(); if (!userId) throw new Response("no", {status:401}); return userId; }
export async function GET() { await requireUser(); return Response.json([]); }
export async function DELETE(req: Request) { await requireUser(); await db.items.delete({ where: { id: "1" } }); return Response.json({ok:true}); }
