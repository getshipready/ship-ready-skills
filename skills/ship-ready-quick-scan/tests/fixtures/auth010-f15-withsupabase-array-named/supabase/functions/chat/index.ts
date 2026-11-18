import { withSupabase } from 'npm:@supabase/server@1'
export default { fetch: withSupabase({ auth: ['user', 'secret:automations'] }, async (req, ctx) => Response.json({ok:1})) }
