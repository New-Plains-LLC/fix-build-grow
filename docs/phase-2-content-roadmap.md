# Phase 2 Content Roadmap

_Last updated: 2026-04-18_

## Objective

Build the next 20 pages for the DIY home repair site around practical, high-trust homeowner help. Phase 2 should expand the existing tutorial, comparison, estimator, gallery, and blog formats into a tighter topical library that answers beginner and budget-conscious repair questions clearly.

## Current site audit

### Existing content types
- **Tutorials:** 1 hands-on project guide (`weekend-mudroom-upgrade`)
- **Comparisons:** 1 tool buying guide (`best-cordless-drills-for-first-time-homeowners`)
- **Estimators:** 1 budget-planning page (`deck-repair-cost-estimator`)
- **Galleries:** 1 visual project story (`backyard-fire-pit-refresh`)
- **Blog:** 1 seasonal support article (`spring-home-maintenance-checklist`)

### What is working
- Clear section structure already exists in Hugo.
- Content model supports practical metadata like time, difficulty, tools, materials, and FAQs.
- Current pages fit a useful-first homeowner voice.
- The format mix is good for both search intent coverage and internal linking.

### Biggest gaps
- Too little topical depth in any one home-repair cluster.
- No linked page sets around one problem area like drywall, caulking, decks, doors, or leaks.
- No foundational "how to diagnose" pages for repair intent.
- No cost pages for common interior repairs like drywall patching, fence repair, or subfloor fixes.
- No comparison pages for repair materials, patch products, sealants, or beginner tool kits.

## Phase 2 strategy

Focus on **repair-first topical clusters** instead of broad lifestyle content. The first 20 pages should make the site feel credible in a few practical lanes:

1. **Drywall and wall repair**
2. **Door, trim, and interior finish fixes**
3. **Deck, fence, and exterior wood maintenance**
4. **Leak sealing, caulk, and weatherproofing**
5. **Starter tools and repair materials**

## First 20 pages in priority order

### Cluster A: Repair tutorials
1. **How to Patch Drywall Holes the Right Way**  
   Format: tutorial. Intent: fix common wall damage with clear beginner steps.
2. **How to Fix Peeling Caulk Around a Bathtub or Shower**  
   Format: tutorial. Intent: solve a high-frequency bathroom repair problem.
3. **How to Repair a Sagging Fence Gate**  
   Format: tutorial. Intent: exterior repair with strong seasonal demand.
4. **How to Replace a Broken Interior Door Knob or Latch**  
   Format: tutorial. Intent: fast, low-risk homeowner repair.
5. **How to Repair Squeaky Floors From Above**  
   Format: tutorial. Intent: solve a frustrating symptom without opening ceilings.
6. **How to Fix Cracks in Exterior Wood Trim Before Painting**  
   Format: tutorial. Intent: repair plus prep for seasonal maintenance.
7. **How to Reseal Drafty Windows Without Replacing Them**  
   Format: tutorial. Intent: energy-saving repair help for budget-conscious owners.
8. **How to Repair Loose Deck Boards and Popped Fasteners**  
   Format: tutorial. Intent: safety-driven outdoor repair content.

### Cluster B: Estimators and cost planning
9. **Drywall Repair Cost Estimator**  
   Format: estimator. Intent: price small patch vs medium repair vs larger replacement.
10. **Fence Repair Cost Estimator**  
   Format: estimator. Intent: compare DIY repair ranges vs likely contractor scope.
11. **Bathroom Re-Caulking Cost Estimator**  
   Format: estimator. Intent: help readers decide whether to tackle sealing work now.
12. **Deck Board Replacement Cost Estimator**  
   Format: estimator. Intent: budget planning for partial deck repair.

### Cluster C: Comparisons and buying guides
13. **Best Drywall Patch Kits for Small and Medium Wall Repairs**  
   Format: comparison. Intent: choose the right kit by hole size and finish quality.
14. **Best Caulk for Bathrooms, Windows, and Exterior Trim**  
   Format: comparison. Intent: match sealant type to repair job.
15. **Best Oscillating Multi-Tools for Common Home Repairs**  
   Format: comparison. Intent: tool research tied to repair use cases.
16. **Joint Compound vs Spackle vs Patch Kits: What to Use and When**  
   Format: comparison. Intent: material selection before a drywall repair.

### Cluster D: Supporting blog and visual proof content
17. **What to Fix First After Buying an Older House**  
   Format: blog. Intent: broad early-funnel entry page that routes to repair clusters.
18. **Signs a Small Water Leak Is Turning Into Wall Damage**  
   Format: blog/diagnostic. Intent: symptom-driven support content linking to caulk and drywall pages.
19. **Before-and-After: Small Deck Repair That Added Another Season of Life**  
   Format: gallery. Intent: visual proof and internal links into deck repair pages.
20. **DIY Wall Repair Mistakes That Make Paint Touch-Ups Obvious**  
   Format: blog. Intent: trust-building support content for drywall cluster.

## Recommended publishing sequence

### Wave 1: Build the first strong cluster
- Patch drywall tutorial
- Drywall repair cost estimator
- Drywall patch kit comparison
- Joint compound vs spackle comparison
- DIY wall repair mistakes article

### Wave 2: Bathroom and weather-sealing cluster
- Re-caulking tutorial
- Bathroom re-caulking estimator
- Best caulk comparison
- Leak-to-wall-damage diagnostic article
- Drafty window resealing tutorial

### Wave 3: Exterior repair cluster
- Loose deck boards tutorial
- Deck board replacement estimator
- Small deck repair gallery
- Sagging fence gate tutorial
- Fence repair cost estimator

### Wave 4: Fast homeowner fixes cluster
- Door knob or latch tutorial
- Squeaky floors tutorial
- Exterior trim crack repair tutorial
- Best oscillating multi-tool comparison
- What to fix first after buying an older house

## Internal linking rules
- Every tutorial should link to at least 1 estimator, 1 comparison, and 1 related support article.
- Every estimator should link back to the matching tutorial and a "should you DIY this" section.
- Every comparison should link to the jobs each product category helps solve.
- Every support article should route readers into one of the repair clusters above.

## Production workflow using subagents

### Recommended roles
1. **Orchestrator subagent**
   - Owns backlog, assigns page batches, and reviews cluster completeness.
2. **Content-writing subagent**
   - Must read and follow the `seo-fundamentals` skill before drafting pages.
   - Produces search-intent-aware outlines, metadata, FAQs, and draft copy.
3. **Content-formatting/coder subagent**
   - Converts approved drafts into Hugo markdown with valid front matter and internal links.
4. **Image subagent**
   - Uses **`Gemini-3-pro-image-preview`** for featured visuals and step-image concepts.
   - Keeps imagery practical, tool-accurate, and homeowner-friendly.
5. **QA/review subagent**
   - Checks factual clarity, duplicate intent, metadata consistency, and link completeness.

### Suggested page workflow
1. Orchestrator assigns a 3 to 5 page cluster batch.
2. Content-writing subagent drafts outlines and copy using `seo-fundamentals`.
3. Image subagent creates a featured image brief and generates visuals with `Gemini-3-pro-image-preview`.
4. Formatting/coder subagent adds markdown files, front matter, and section placement.
5. QA subagent validates links, headings, consistency, and search-intent alignment.
6. Orchestrator merges, commits, and ships the batch.

## Guardrails
- Keep the site focused on repair help, diagnosis, safety, budgeting, and realistic DIY scope.
- Do not add visible monetization language to page copy or page planning.
- Prefer specific repair intent over generic inspiration topics.
- Favor clusters that can earn trust through practical detail, not fluff.

## Definition of done for each new page
- Clear primary homeowner problem and search intent
- Strong intro with direct answer
- Helpful steps, tools, materials, and safety notes where relevant
- FAQ section matching likely search follow-ups
- At least 3 internal links into the cluster
- Image plan ready for `Gemini-3-pro-image-preview`
- Hugo front matter complete and section-appropriate
