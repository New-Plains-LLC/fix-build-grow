# Vercel Hosting Documentation

## Current status
- Hugo site scaffold is ready.
- Repository is live at `https://github.com/New-Plains-LLC/fix-build-grow`.
- Production domain for this project is `https://firsthomefix.com/`.

## Vercel deployment
1. Vercel auto-deploys from the `main` branch of `New-Plains-LLC/fix-build-grow`.
2. Build command: `npx hugo --gc --minify`
3. Output directory: `public`
4. The `package.json` build script is: `hugo --gc --minify`

## Environment variables (set in Vercel dashboard)
- `HUGO_VERSION=0.149.2`
- `HUGO_ENV=production`
- `HUGO_ENABLEGITINFO=true`

## Domain mapping
- **Primary domain:** `firsthomefix.com`
- **WWW redirect:** `www.firsthomefix.com` -> `firsthomefix.com`
- **DNS:** nsone.net (original Netlify DNS — Vercel serves the site)

## Post-deploy checks
- Confirm homepage renders hero art and featured cards
- Verify `/tutorials/`, `/galleries/`, `/estimators/`, and `/comparisons/`
- Add form capture or newsletter once lead gen is ready