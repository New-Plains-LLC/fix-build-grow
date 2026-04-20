# firsthomefix.com

Home Improvement & DIY site scaffolded for Netlify + Hugo, built around visual tutorials, project galleries, cost estimators, and tool comparisons.

## Project domain
- **Production domain:** `https://firsthomefix.com/`
- **Note:** `firsthomefix.com` is the live domain for this project.

## Stack
- **Static site generator:** Hugo
- **Hosting:** Netlify
- **Source control:** GitHub
- **Build command:** `npx hugo --gc --minify`

## Why Hugo
Hugo is the better fit here than Jekyll because it is faster, easier to model with front matter, and better suited to image-heavy evergreen content that will eventually scale to hundreds of pages.

## Content structure
- `content/tutorials/` for step-by-step DIY guides
- `content/galleries/` for before-and-after project showcases
- `content/estimators/` for budget-planning pages
- `content/comparisons/` for affiliate-ready tool and material guides
- `content/blog/` for seasonal and editorial support content

## Local development
```bash
npm install
npm run dev
```

## Netlify settings
- **Base directory:** `automated-revenue-website` if deploying from the workspace monorepo, otherwise repo root
- **Build command:** `npx hugo --gc --minify`
- **Publish directory:** `public`

## Included starter templates
- Visual homepage with niche-specific CTA blocks
- Generic list and single layouts
- Comparison page template with structured product table
- Estimator page template with range breakdowns and assumptions
- Front matter fields for cost, time, difficulty, tools, materials, and CTA

## Next recommended moves
1. Replace SVG placeholders with original project imagery
2. Add Netlify Forms for quote requests or newsletter capture
3. Connect affiliate modules into comparison and tutorial templates
4. Add search, schema markup, and internal-link automation
