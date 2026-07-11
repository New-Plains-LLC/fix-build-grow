#!/usr/bin/env python3
"""Lead-gen site factory — upgraded with Luke Vander's niche selection framework.

Scoring dimensions based on the Luke Vander / Koerner Office model:
- Maps competition weakness (reviews <10, no website, no exact-match domain)
- Organic competition weakness (inner pages vs dedicated sites)
- Owner reachability (does the decision-maker answer the phone?)
- Ticket size vs effort ratio
- Exact-match domain availability
- Red flag detection (long-term contracts, middleman risk)

Usage:
  python3 leadgen_factory.py score              # Rank opportunities
  python3 leadgen_factory.py lookup             # Generate manual research prompts
  python3 leadgen_factory.py generate --service X --limit N  # Build pages
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "leadgen_markets.json"
OUT_DIR = ROOT / "content" / "lead-gen"
REPORT_DIR = ROOT / "reports" / "leadgen"

# ── Luke's red-flag niches — don't waste time here ──────────────────────────
RED_FLAG_NICHES = {
    "elevator-repair":    "long-term service contracts, can't break them",
    "elevator-maintenance": "same as elevator repair",
    "jet-rental":         "middleman on top of middleman, no direct buyer",
    "jet-charter":        "same as jet rental",
}

# ── Owner reachability ranking (Luke's framework) ───────────────────────────
# How likely you are to reach the decision-maker directly
OWNER_REACHABILITY = {
    "towing": 10,
    "tree-removal": 9,
    "tree-service": 9,
    "pest-control": 8,
    "concrete": 8,
    "lawn-care": 7,
    "landscaping": 7,
    "roofing": 6,
    "painting": 6,
    "fencing": 6,
    "mold-remediation": 6,
    "asbestos-testing": 6,
    "radon-mitigation": 6,
    "carpet-cleaning": 7,
    "window-cleaning": 7,
    "power-washing": 7,
    "garage-door-repair": 7,
    "septic-repair": 8,
    "foundation-repair": 6,
    "water-heater-repair": 5,
    "hvac-repair": 4,
    "hvac-installation": 4,
    "plumbing": 4,
    "electrical": 4,
    "dentistry": 2,
}

# ── Ticket/value tiers (Luke's sweet spot: high ticket + owner reachable) ───
TICKET_TIER = {
    "towing": 200,
    "tree-removal": 500,
    "tree-service": 350,
    "pest-control": 300,
    "concrete": 800,
    "lawn-care": 50,
    "landscaping": 400,
    "roofing": 1000,
    "painting": 400,
    "fencing": 600,
    "mold-remediation": 600,
    "asbestos-testing": 500,
    "radon-mitigation": 600,
    "carpet-cleaning": 150,
    "window-cleaning": 200,
    "power-washing": 250,
    "garage-door-repair": 350,
    "septic-repair": 700,
    "foundation-repair": 1500,
    "water-heater-repair": 400,
    "hvac-repair": 300,
    "hvac-installation": 2000,
    "plumbing": 350,
    "electrical": 300,
    "dentistry": 2000,
}


@dataclass
class ServiceProfile:
    slug: str
    name: str
    urgency_score: int
    repeat_score: int
    diy_risk_score: int
    buyer_demand_score: int
    lead_value: int
    owner_reachability: int
    ticket_size: int
    example_jobs: list[str]
    notes: str = ""

    @property
    def luke_score(self) -> float:
        """Luke's sweet spot: high ticket + reachable owner."""
        a = self.ticket_size * 0.4
        b = self.owner_reachability * 10 * 0.3
        c = self.urgency_score * 3 * 0.2
        d = self.buyer_demand_score * 4 * 0.1
        return round(a + b + c + d, 1)

    @property
    def competition_field_score(self) -> int:
        """How likely competition is weak (subjective, 1-10).

        Luke looks for: <10 reviews on maps, no website, no exact-match domain.
        Higher = more likely to find weak competition.
        """
        base = 5  # default neutral
        # Niche-specific heuristics from Luke's transcript
        niche_hints = {
            "asbestos-testing": 8,
            "radon-mitigation": 9,
            "mold-remediation": 7,
            "towing": 6,
            "pest-control": 6,
            "concrete": 5,
            "tree-removal": 6,
            "tree-service": 6,
        }
        return niche_hints.get(self.slug, base)

    @property
    def monthly_rental_estimate(self) -> int:
        """Flat fee Luke would charge for a ranked site in this niche."""
        base = 300
        multiplier = max(1, self.luke_score / 30)
        return int(base * multiplier)


@dataclass
class MetroProfile:
    city: str
    state: str
    population_score: int
    home_age_score: int
    affluence_score: int
    competition_score: int


@dataclass
class Opportunity:
    metro: MetroProfile
    service: ServiceProfile

    @property
    def slug(self) -> str:
        return f"{self.service.slug}-{self.metro.city.lower()}-{self.metro.state.lower()}"

    @property
    def city_slug(self) -> str:
        text = self.metro.city.lower().strip()
        text = re.sub(r"[^a-z0-9]+", "-", text)
        return text.strip("-")

    @property
    def service_slug(self) -> str:
        return self.service.slug

    @property
    def luke_viability_score(self) -> float:
        """0-100. Luke's combined niche + city viability.

        Blends: niche sweet spot, competition weakness, city size fit, affluence.
        """
        m = self.metro
        s = self.service

        # Luke's sweet spot: high ticket × reachable owner
        sweet = s.luke_score

        # City fit: 60-400k population is ideal (Luke says 60k-500k)
        pop = m.population_score
        pop_fit = 5 - abs(pop - 6)  # peaks at score 6 (ideal range)

        # Competition: lower = better for ranking ease
        comp_factor = max(0, 10 - m.competition_score)

        # Affluence: higher = more likely to pay for services
        affluence = m.affluence_score

        # Home age: older = more repair needs
        home_age = m.home_age_score

        # Red flag check
        if s.slug in RED_FLAG_NICHES:
            return 0.0

        score = (
            sweet * 0.35
            + s.competition_field_score * 10 * 0.20
            + pop_fit * 8 * 0.15
            + comp_factor * 5 * 0.10
            + affluence * 3 * 0.10
            + home_age * 3 * 0.05
            + s.repeat_score * 3 * 0.05
        )
        return round(score, 1)

    @property
    def estimated_monthly_rental(self) -> int:
        return self.service.monthly_rental_estimate

    @property
    def research_prompt(self) -> str:
        """Instructions for manually Googling to validate this opportunity (Luke's method)."""
        m = self.metro
        s = self.service
        return (
            f"## Research: {s.name} in {m.city}, {m.state}\n"
            f"\n"
            f"1. **Google Maps:** Search `{s.name.lower()} {m.city}`\n"
            f"   - How many results? _____\n"
            f"   - How many have <10 reviews? _____ / 3 shown\n"
            f"   - How many have NO website (just FB/Twitter)? _____\n"
            f"   - Do any have an exact-match domain name? Y / N\n"
            f"   - If you registered `{m.city.lower()}{s.slug.replace('-','')}.com`, would it match?\n"
            f"\n"
            f"2. **Google Organic:** Check the top 5 results\n"
            f"   - Dedicated sites (Y): _____\n"
            f"   - Inner pages on bigger sites: _____\n"
            f"   - Yelp/aggregators: _____\n"
            f"   - Verdict: {'Likely easy to beat' if s.competition_field_score >= 7 else 'Mixed — dig deeper'}\n"
            f"\n"
            f"3. **Thumbtack:** Search `{s.name}` → how many providers in area? _____\n"
            f"\n"
            f"4. **Owner reachability:** Call one random provider in {m.city}. Does the owner answer? Y / N\n"
            f"\n"
            f"5. **Verdict:** {'GOOD — ' + ('niche is strong' if s.luke_score >= 60 else 'city needs checking')}\n"
        )

    def to_csv_row(self) -> list:
        return [
            self.service.name,
            self.metro.city,
            self.metro.state,
            self.luke_viability_score,
            self.service.luke_score,
            self.service.competition_field_score,
            self.estimated_monthly_rental,
            self.service.owner_reachability,
            self.service.ticket_size,
            f"vet this" if self.luke_viability_score >= 60 else "marginal",
            "RED FLAG: " + RED_FLAG_NICHES.get(self.service.slug, "") if self.service.slug in RED_FLAG_NICHES else "",
        ]


def load_data(path: Path = DATA_FILE) -> dict:
    return json.loads(path.read_text())


def score_opportunities(data: dict) -> list[Opportunity]:
    rows: list[Opportunity] = []
    for m in data["metros"]:
        metro = MetroProfile(**m)
        for svc in data["services"]:
            profile = ServiceProfile(
                slug=svc["slug"],
                name=svc["name"],
                urgency_score=svc.get("urgency_score", 5),
                repeat_score=svc.get("repeat_score", 3),
                diy_risk_score=svc.get("diy_risk_score", 5),
                buyer_demand_score=svc.get("buyer_demand_score", 5),
                lead_value=svc.get("lead_value", 50),
                owner_reachability=OWNER_REACHABILITY.get(svc["slug"], 5),
                ticket_size=TICKET_TIER.get(svc["slug"], 200),
                example_jobs=svc.get("example_jobs", []),
            )
            rows.append(Opportunity(metro=metro, service=profile))
    return sorted(rows, key=lambda r: r.luke_viability_score, reverse=True)


def today_ct() -> str:
    return datetime.now(ZoneInfo("America/Chicago")).date().isoformat()


def write_score_report(rows: list[Opportunity]) -> tuple[Path, Path]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = REPORT_DIR / "leadgen-opportunity-scores.csv"
    md_path = REPORT_DIR / "leadgen-opportunity-scores.md"

    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "rank", "service", "city", "state", "luke_score", "niche_sweet_spot",
            "comp_field_score", "est_monthly_rental", "owner_reachability",
            "avg_ticket", "verdict", "red_flag"
        ])
        for i, r in enumerate(rows, 1):
            w.writerow(r.to_csv_row())

    lines = [
        "# Lead-Gen Opportunity Scores (Luke Vander Framework)",
        "",
        f"Generated: {today_ct()}",
        "",
        "Scoring blends: niche sweet spot (high ticket × reachable owner), ",
        "competition weakness (maps & organic), city fit (60k-500k ideal), affluence, home age.",
        "",
        "| Rank | Service | City | Score | Niche Sweet | Comp Field | Est Rental | Owner | Ticket | Verdict |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for i, r in enumerate(rows[:30], 1):
        crow = r.to_csv_row()
        lines.append(
            f"| {i} | {crow[0]} | {crow[1]} | {crow[3]} | {crow[4]} | {crow[5]} | ${crow[6]} | {crow[7]} | ${crow[8]} | {crow[9]} |"
        )
    if any(r.service.slug in RED_FLAG_NICHES for r in rows):
        lines.append("")
        lines.append("### ⛔ Red-flag niches (automatically excluded)")
        lines.append("")
        for slug, reason in RED_FLAG_NICHES.items():
            name = next((s["name"] for s in json.loads(DATA_FILE.read_text())["services"] if s["slug"] == slug), slug)
            lines.append(f"- **{name}**: {reason}")

    md_path.write_text("\n".join(lines) + "\n")
    return csv_path, md_path


def write_lookup_sheet(rows: list[Opportunity], limit: int = 10) -> Path:
    """Generate a manual research sheet (Luke's Google + Maps method)."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / f"manual-research-prompt-{today_ct()}.md"
    selected = [r for r in rows if r.luke_viability_score >= 50][:limit]
    parts = [
        f"# Manual Niche Research — {today_ct()}",
        "",
        f"Top {len(selected)} opportunities to Google-validate (Luke Vander method).",
        "For each, open Google Maps + organic results and check the signals below.",
        "",
        "---",
        "",
    ]
    for i, r in enumerate(selected, 1):
        parts.append(f"## {i}. {r.service.name} in {r.metro.city}")
        parts.append("")
        parts.append(r.research_prompt)
        parts.append("---")
        parts.append("")

    path.write_text("\n".join(parts))
    return path


def generate_pages(rows: list[Opportunity], service: str | None, limit: int) -> list[Path]:
    """Generate Hugo landing pages for validated opportunities."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    selected = [r for r in rows if service is None or r.service_slug == service][:limit]
    written: list[Path] = []

    # Ensure service index pages exist
    for o in selected:
        sdir = OUT_DIR / o.service_slug
        sdir.mkdir(parents=True, exist_ok=True)
        idx = sdir / "_index.md"
        if not idx.exists():
            idx.write_text(
                f"---\ntitle: \"{o.service.name}\"\ndescription: \"City-specific {o.service.name.lower()} guides.\"\n---\n\n"
            )

        page = sdir / f"{o.city_slug}-{o.metro.state.lower()}.md"
        if not page.exists():
            page.write_text(build_page_markdown(o))
            written.append(page)
    return written


def build_page_markdown(o: Opportunity) -> str:
    jobs = o.service.example_jobs
    job_str = ", ".join(jobs[:-1]) + f", and {jobs[-1]}" if len(jobs) > 1 else jobs[0]
    svc_name = o.service.name
    city = o.metro.city
    state = o.metro.state
    title = f"{svc_name} in {city}, {state} — Get Local Help"
    desc = f"Need {svc_name.lower()} in {city}? This page connects you with local pros."
    return f"""---
title: "{title}"
date: {today_ct()}
draft: false
description: "{desc}"
summary: "Local {svc_name.lower()} service information for {city}."
categories: ["local service"]
tags: ["{svc_name.lower()}", "{city.lower()}", "home service"]
leadgen:
  service: "{svc_name}"
  city: "{city}"
  state: "{state}"
  luke_score: {o.luke_viability_score}
  est_rental: {o.estimated_monthly_rental}
---

# {title}

If you need **{svc_name.lower()} in {city}**, the right approach is to describe the problem clearly, avoid dangerous DIY work, and compare quotes from licensed providers.

Common jobs: **{job_str}**.

## Quick checklist before you call

1. Take photos of the problem area.
2. Note when it started and whether it is getting worse.
3. Decide if it is urgent or can wait for multiple quotes.
4. Ask each provider the same questions.

<div class="contact-form-card card">
  <div class="contact-form-body">
    <h2>Request help with {svc_name.lower()} in {city}</h2>
    <form name="local-lead" class="contact-form" action="https://n8n.newplains.cloud/webhook/firsthomefix-lead" method="POST">
      <input type="hidden" name="source" value="firsthomefix">
      <input type="hidden" name="service" value="{svc_name}">
      <input type="hidden" name="city" value="{city}">
      <input type="text" name="name" required placeholder="Your name">
      <input type="tel" name="phone" required placeholder="Phone">
      <input type="email" name="email" placeholder="Email">
      <textarea name="problem" rows="4" required placeholder="Describe the issue..."></textarea>
      <label><input type="checkbox" name="consent" value="yes" required> I consent to being contacted about this request.</label>
      <button type="submit">Send request</button>
    </form>
  </div>
</div>
"""


def main() -> None:
    ap = argparse.ArgumentParser(description="Lead-gen site factory (Luke Vander framework)")
    ap.add_argument("command", choices=["score", "lookup", "generate", "all"])
    ap.add_argument("--service", default=None, help="Service slug to generate pages for")
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()

    data = load_data()
    rows = score_opportunities(data)

    if args.command in {"score", "all"}:
        csv_path, md_path = write_score_report(rows)
        print(f"SCORE_CSV={csv_path}")
        print(f"SCORE_MD={md_path}")
        print("--- Top 10 ---")
        for i, r in enumerate(rows[:10], 1):
            crow = r.to_csv_row()
            print(f"{i}. {crow[0]} — {crow[1]} — score {crow[3]} — est ${crow[6]}/mo [{crow[9]}]")

    if args.command == "lookup":
        path = write_lookup_sheet(rows, args.limit)
        print(f"LOOKUP_SHEET={path}")

    if args.command in {"generate", "all"}:
        written = generate_pages(rows, args.service, args.limit)
        print(f"PAGES_WRITTEN={len(written)}")
        for p in written:
            print(p.relative_to(ROOT))


if __name__ == "__main__":
    main()