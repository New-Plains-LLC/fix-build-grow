#!/usr/bin/env python3
"""FirstHomeFix lead-gen factory.

Scores boring local-service opportunities and generates Hugo landing pages for
validated service + city pairs. This is intentionally API-light so it can run in
cron without paid dependencies; replace seed scores with live Ahrefs/Maps/CPC
feeds later without changing the page generator.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "leadgen_markets.json"
OUT_DIR = ROOT / "content" / "lead-gen"
REPORT_DIR = ROOT / "reports" / "leadgen"


@dataclass
class Opportunity:
    city: str
    state: str
    service_slug: str
    service_name: str
    score: float
    lead_value: int
    monthly_value: int
    rationale: str
    example_jobs: list[str]

    @property
    def city_slug(self) -> str:
        return slugify(self.city)

    @property
    def page_slug(self) -> str:
        return f"{self.service_slug}-{self.city_slug}-{self.state.lower()}"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def load_data(path: Path = DATA_FILE) -> dict:
    return json.loads(path.read_text())


def score_opportunities(data: dict) -> list[Opportunity]:
    rows: list[Opportunity] = []
    for metro in data["metros"]:
        for svc in data["services"]:
            demand = (
                metro["population_score"] * 1.4
                + metro["home_age_score"] * 1.1
                + metro["affluence_score"] * 0.8
                + svc["urgency_score"] * 1.5
                + svc["ticket_score"] * 1.4
                + svc["diy_risk_score"] * 1.2
                + svc["buyer_demand_score"] * 1.5
            )
            # Higher competition score means harder to rank; subtract it, but do not
            # over-penalize big markets because their lead volume is worth fighting for.
            score = round(demand - metro["competition_score"] * 0.9 + svc["repeat_score"] * 0.4, 1)
            monthly_value = int(svc["lead_value"] * max(8, round(score / 5)))
            rationale = (
                f"{svc['name']} in {metro['city']} has urgent intent, contractor buyer demand, "
                f"and enough ticket size to support paid lead/rental monetization."
            )
            rows.append(
                Opportunity(
                    city=metro["city"],
                    state=metro["state"],
                    service_slug=svc["slug"],
                    service_name=svc["name"],
                    score=score,
                    lead_value=svc["lead_value"],
                    monthly_value=monthly_value,
                    rationale=rationale,
                    example_jobs=svc["example_jobs"],
                )
            )
    return sorted(rows, key=lambda r: (r.score, r.monthly_value), reverse=True)


def today_ct() -> str:
    return datetime.now(ZoneInfo("America/Chicago")).date().isoformat()


def write_score_report(rows: list[Opportunity]) -> tuple[Path, Path]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = REPORT_DIR / "leadgen-opportunity-scores.csv"
    md_path = REPORT_DIR / "leadgen-opportunity-scores.md"
    generated_date = today_ct()
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rank", "service", "city", "state", "score", "lead_value", "estimated_monthly_value", "rationale"])
        for i, r in enumerate(rows, 1):
            w.writerow([i, r.service_name, r.city, r.state, r.score, r.lead_value, r.monthly_value, r.rationale])
    lines = [
        "# FirstHomeFix Lead-Gen Opportunity Scores",
        "",
        f"Generated: {generated_date}",
        "",
        "Scoring favors urgent, high-ticket, contractor-buyable jobs in Oklahoma metros where firsthomefix can publish city/service pages and route quote requests.",
        "",
        "| Rank | Service | City | Score | Lead value | Est. monthly value |",
        "|---:|---|---|---:|---:|---:|",
    ]
    for i, r in enumerate(rows[:25], 1):
        lines.append(f"| {i} | {r.service_name} | {r.city}, {r.state} | {r.score} | ${r.lead_value} | ${r.monthly_value} |")
    md_path.write_text("\n".join(lines) + "\n")
    return csv_path, md_path


def ensure_index() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    index = OUT_DIR / "_index.md"
    if not index.exists():
        index.write_text(
            "---\n"
            "title: \"Local Repair Help\"\n"
            "description: \"City-specific repair guides and quote request pages for Oklahoma homeowners.\"\n"
            "summary: \"Find practical repair guidance and request help from local pros when a job is too risky or time-sensitive to DIY.\"\n"
            "---\n\n"
            "FirstHomeFix is building practical city-specific repair resources for homeowners. "
            "Start with the guide, avoid dangerous DIY mistakes, and request a referral when the job needs a pro.\n"
        )


def page_markdown(o: Opportunity) -> str:
    jobs = ", ".join(o.example_jobs[:-1]) + f", and {o.example_jobs[-1]}"
    title = f"{o.service_name} in {o.city}, {o.state}: Costs, Warning Signs, and When to Call a Pro"
    description = f"A practical homeowner guide to {o.service_name.lower()} in {o.city}, {o.state} — common problems, cost ranges, safety warnings, and quote-request checklist."
    summary = f"Know what to check before hiring a {o.service_name.lower()} pro in {o.city}, and what details to collect before requesting quotes."
    body = f"""---
title: \"{title}\"
date: {today_ct()}
draft: false
description: \"{description}\"
summary: \"{summary}\"
categories: [\"local repair\"]
tags: [\"{o.service_name.lower()}\", \"{o.city.lower()}\", \"local repair\", \"contractor quotes\"]
difficulty: \"homeowner screening\"
project_type: \"local lead guide\"
estimated_cost: \"varies by job\"
estimated_time: \"6 minute read\"
leadgen:
  service: \"{o.service_name}\"
  city: \"{o.city}\"
  state: \"{o.state}\"
  opportunity_score: {o.score}
  estimated_lead_value: {o.lead_value}
---

If you need **{o.service_name.lower()} in {o.city}**, the goal is not to hire the first company that answers the phone. The goal is to describe the problem clearly, avoid dangerous DIY work, and compare quotes from contractors who actually handle this kind of repair.

This page is built for homeowners dealing with jobs like **{jobs}**.

## Quick triage before you call

Use this checklist before requesting a quote:

1. Take 3 photos: the full area, a close-up of the failure, and anything showing water, movement, cracking, or electrical/mechanical parts.
2. Write down when the problem started and whether it is getting worse.
3. Note anything you already tried.
4. Decide whether the issue is urgent, unsafe, or just annoying.
5. Ask each contractor the same questions so the quotes are comparable.

{{{{< warning >}}}}
Do not turn a contractor lead into a hospital bill. If the repair involves high-tension springs, structural movement, electrical work, gas lines, sewage, major water damage, or work above your safe ladder height, stop and call a pro.
{{{{< /warning >}}}}

## What this usually costs in {o.city}

Actual pricing depends on access, parts, severity, and whether the job is an emergency. For lead-gen qualification, the useful question is not \"what is the cheapest possible fix?\" It is \"is this job valuable enough that a real contractor will answer quickly and do good work?\"

For {o.service_name.lower()}, this is a strong lead category because one booked job can be worth enough for a contractor to pay for qualified calls. That is why FirstHomeFix tracks this category separately from basic DIY repairs.

## Questions to ask before hiring

- Are you licensed or insured for this type of repair?
- Do you charge a diagnostic/trip fee?
- Can you give a written scope before work starts?
- What parts or materials are included?
- What would make the price go up after arrival?
- Do you warranty labor and parts?

## When DIY is reasonable

DIY is reasonable when the job is inspection, cleaning, tightening, basic maintenance, or documenting the issue for a contractor. DIY is not reasonable when the failure can hurt you, damage the home, or create a code problem.

{{{{< callout >}}}}
**FirstHomeFix rule:** Do the safe diagnosis yourself. Pay for the dangerous repair. That saves money without pretending every repair is a weekend project.
{{{{< /callout >}}}}

## Want help finding a local pro?

FirstHomeFix is building a vetted local repair network for Oklahoma homeowners. If you want help with **{o.service_name.lower()} in {o.city}**, use the contact page and include your city, photos, and a short description of the issue.

[Request repair help](/contact/)
"""
    return body


def generate_pages(rows: Iterable[Opportunity], service: str | None, limit: int) -> list[Path]:
    ensure_index()
    selected = [r for r in rows if service is None or r.service_slug == service][:limit]
    written: list[Path] = []
    for o in selected:
        service_dir = OUT_DIR / o.service_slug
        service_dir.mkdir(parents=True, exist_ok=True)
        service_index = service_dir / "_index.md"
        if not service_index.exists():
            service_index.write_text(
                f"---\ntitle: \"{o.service_name}\"\ndescription: \"City-specific {o.service_name.lower()} guides for Oklahoma homeowners.\"\n---\n\nCompare repair warning signs, quote questions, and when to call a pro.\n"
            )
        page = service_dir / f"{o.city_slug}-{o.state.lower()}.md"
        page.write_text(page_markdown(o))
        written.append(page)
    return written


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["score", "generate", "all"])
    ap.add_argument("--service", default=None, help="Service slug to generate, e.g. garage-door-repair")
    ap.add_argument("--limit", type=int, default=6)
    args = ap.parse_args()

    rows = score_opportunities(load_data())
    if args.command in {"score", "all"}:
        csv_path, md_path = write_score_report(rows)
        print(f"score_report_csv={csv_path}")
        print(f"score_report_md={md_path}")
        print("top_5=")
        for i, r in enumerate(rows[:5], 1):
            print(f"{i}. {r.service_name} — {r.city}, {r.state} — score {r.score} — est monthly ${r.monthly_value}")
    if args.command in {"generate", "all"}:
        written = generate_pages(rows, args.service, args.limit)
        print(f"pages_written={len(written)}")
        for p in written:
            print(p.relative_to(ROOT))


if __name__ == "__main__":
    main()
