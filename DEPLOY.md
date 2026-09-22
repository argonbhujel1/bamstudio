# BAM Studio — Vercel Deploy

## Entrypoint
- `api/index.py` exports Flask `app` (required by Vercel Python runtime)
- `vercel.json` rewrites all traffic to `/api`

## Env vars (Production + Preview)
| Name | Required | Notes |
|------|----------|--------|
| DATABASE_URL | Yes | Neon: `postgresql://...@ep-xxx.region.aws.neon.tech/neondb?sslmode=require` |
| SECRET_KEY | Yes | Random long string |
| SETUP_SECRET | Recommended | Token for `/api/setup` |
| ADMIN_EMAIL | For seed | |
| ADMIN_PASSWORD | For seed | |

**Never use** `@host` in DATABASE_URL.

## After deploy
1. `https://YOUR.app/api/setup?token=SETUP_SECRET` — create tables  
2. Local: `DATABASE_URL=... python seed.py`  
3. `https://YOUR.app/api/health` — must show database ok  

## Redeploy after env change
Settings → Environment Variables → Save → Deployments → Redeploy
