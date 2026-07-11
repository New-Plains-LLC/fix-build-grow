# FirstHomeFix Lead-Gen Automation Blueprint

## Goal
Turn FirstHomeFix from a pure content site into a local repair lead-gen asset.

The machine is:

```text
City/service page -> call/form -> n8n -> lead score -> contractor match -> weekly report -> recurring rental/sold-lead offer
```

## Current implementation

- `data/leadgen_markets.json` stores seed service + metro scores.
- `tools/leadgen_factory.py score` ranks service/geo opportunities.
- `tools/leadgen_factory.py generate --service SERVICE --limit N` creates Hugo landing pages.
- Generated pages live under `content/lead-gen/<service>/<city>-ok.md`.
- Reports live under `reports/leadgen/`.

## n8n workflow to build next

### Trigger
Webhook path:

```text
POST /webhook/firsthomefix-lead
```

Expected payload:

```json
{
  "name": "Jane Homeowner",
  "phone": "+14055551212",
  "email": "jane@example.com",
  "city": "Oklahoma City",
  "service": "Garage Door Repair",
  "problem": "Door starts closing then reverses",
  "page_url": "https://firsthomefix.com/lead-gen/garage-door-repair/oklahoma-city-ok/",
  "source": "firsthomefix"
}
```

### Lead scoring

Score 0-100:

| Signal | Points |
|---|---:|
| Phone present | 20 |
| City present | 10 |
| Service present | 10 |
| Problem length > 40 chars | 15 |
| Emergency words: leaking, broken, stuck, no hot water, spring, sewage, smoke, sparking | 20 |
| High-value service category | 15 |
| Photos attached | 10 |

### Routing

1. If score >= 70: alert contractor/owner immediately.
2. If score 40-69: store in review queue.
3. If score < 40: send confirmation only, do not sell as qualified.

### Storage
Use a Google Sheet or Airtable table with:

- timestamp
- lead_id
- name
- phone
- email
- city
- service
- problem
- score
- page_url
- status
- assigned_contractor
- sold_amount
- notes

### Contractor sales report
Every Monday:

- leads received by service/city
- qualified leads
- booked/unknown
- estimated lead value
- suggested contractor offer

## Offer to contractors

Do not sell "SEO." Sell calls.

Starter offer:

> We have homeowner repair requests coming in for {service} in {city}. You can take the next 10 qualified leads for $X, or rent the category for $Y/month if the calls are good.

## Non-negotiable rule
No outbound emails/SMS/calls are sent automatically. Drafts only until Shawn approves.
