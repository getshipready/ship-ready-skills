import { withSupabase } from 'npm:@supabase/server@1'
export default { fetch: withSupabase({ auth: 'publishable:web' }, async (_req, ctx) => Response.json({ok:1})) }
