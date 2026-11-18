import { withSupabase } from 'npm:@supabase/server@1'
export default { fetch: withSupabase({ auth: 'none' }, async (_req, ctx) => Response.json({ok:1})) }
