# AI Landscape Project

This project generates a self-updating AI industry landscape web page tracking key companies, leadership, products, financial health, and headcount over time.

## Key files
- `data/ai-landscape.json` — the source of truth. **Never delete historical data. Only append.**
- `docs/index.html` — GENERATED FILE. Do not edit by hand; always regenerate via the `/ai-landscape` skill.
- `/Users/groser/.claude/commands/ai-landscape.md` — the update skill.

## Company sections
1. Frontier AI — OpenAI, Anthropic, xAI, Google DeepMind, Meta AI
2. Foundation Model Labs — Mistral AI, Cohere
3. Big Tech AI — Microsoft AI, Amazon/AWS AI
4. AI Applications — Perplexity AI, Hugging Face, Stability AI
5. AI Infrastructure — Nvidia, Scale AI, Together AI
6. AI Startups — ElevenLabs, Runway, Luma AI, Reka AI, Cognition AI, Thinking Machines Lab, Sierra, Cursor, Harvey, Glean, Cerebras, Groq

## Design system (matches GPS all-hands site)
- Primary: #0070D2 (Salesforce blue)
- Accent: #00A1E0
- Background: #F4F6F9
- Text: #16325C
- Font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif

## Data rules
- All HTML is self-contained (no external CDN, no external images, no runtime fetch)
- All charts are inline SVG built from embedded data
- Date format: YYYY-MM-DD throughout the JSON
- All dollar amounts in USD
- Never delete historical snapshot entries — only append
- Carry forward last known value when data unavailable (confidence: "carried_forward")

## Running the skill
```
/ai-landscape              → full weekly update for today's date
/ai-landscape 2026-06-25  → update for a specific date
/ai-landscape --init       → first run: seed from training knowledge (no web search)
/ai-landscape --dry-run    → research and show draft, do not write files
/ai-landscape --companies openai,anthropic  → limit scope
```

## Confidence levels
- high — verified from official source or SEC filing
- medium — credible press report or LinkedIn estimate
- low — inference or unverified
- carried_forward — no new data; using prior week's value

## News event types
model_release, product_launch, funding, partnership, leadership, business, regulatory, research
