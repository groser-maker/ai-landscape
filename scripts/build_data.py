#!/usr/bin/env python3
"""
Rebuild data/ai-landscape.json with full model history, funding rounds,
acquisitions, and investor data. Run: python3 scripts/build_data.py
"""
import json, sys, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(BASE, "data", "ai-landscape.json")

# ── Helpers ────────────────────────────────────────────────────────────────
def model(name, date, params_b, params_estimated, mtype, purpose,
          context_k=None, notable=False, notes="", params_note="",
          elo=None, elo_est=True):
    return dict(name=name, date=date,
                parameters_billions=params_b,
                parameters_estimated=params_estimated,
                parameters_note=params_note,
                type=mtype, purpose=purpose,
                context_length_k=context_k,
                notable=notable, notes=notes,
                elo_score=elo,
                elo_estimated=elo_est)

def round_(date, amount, rtype, lead, valuation=None, investors=None):
    return dict(date=date, amount_usd_billions=amount, type=rtype,
                lead_investor=lead, valuation_usd_billions=valuation,
                investors=investors or [])

def acq(name, date, amount_note, description):
    return dict(name=name, date=date, amount_note=amount_note,
                description=description)

# ── COMPANY DEFINITIONS ────────────────────────────────────────────────────
COMPANIES = [

# ═══════════════════════════════════════════════════════
# FRONTIER AI
# ═══════════════════════════════════════════════════════

{
  "id": "openai", "name": "OpenAI", "section": "Frontier AI",
  "founded": 2015, "hq": "San Francisco, CA",
  "color": "#10A37F", "emoji": "🟢",
  "description": "Developer of GPT and o-series models. ChatGPT is the world's most-used AI product. Restructured from nonprofit to capped-profit in 2019; IPO filing confidentially submitted Jun 2026.",
  "leadership": [
    {"name": "Sam Altman", "title": "CEO", "since": "2019-03"},
    {"name": "Greg Brockman", "title": "President (on leave)", "since": "2015-01"},
    {"name": "Brad Lightcap", "title": "COO", "since": "2023-01"}
  ],
  "products": [
    {"name": "GPT-4o", "type": "LLM API", "flagship": True, "description": "Omni model — text, vision, audio natively", "launched": "2024-05"},
    {"name": "ChatGPT", "type": "Consumer app", "flagship": False, "description": "100M+ weekly active users", "launched": "2022-11"},
    {"name": "o3", "type": "Reasoning model", "flagship": False, "description": "Advanced chain-of-thought reasoning", "launched": "2025-01"},
    {"name": "Sora", "type": "Video generation", "flagship": False, "description": "Text-to-video model", "launched": "2024-12"},
    {"name": "DALL-E 3", "type": "Image generation", "flagship": False, "description": "Text-to-image, integrated in ChatGPT", "launched": "2023-10"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 17.9, "valuation_usd_billions": 157.0,
    "valuation_as_of": "2024-10", "public": False, "ticker": None,
    "last_round_date": "2024-10", "last_round_amount_usd_billions": 6.6,
    "last_round_type": "Series F", "last_round_investors": ["SoftBank","Microsoft","Tiger Global"]
  },
  "funding_rounds_history": [
    round_("2023-01", 10.0, "Strategic Investment", "Microsoft", None, ["Microsoft"]),
    round_("2024-05", 0.87, "Secondary", "Thrive Capital", 80.0, ["Thrive Capital","Khosla Ventures","a16z"]),
    round_("2024-10", 6.6, "Series F", "SoftBank", 157.0, ["SoftBank","Microsoft","Tiger Global","Khosla Ventures"]),
  ],
  "model_history": [
    model("ChatGPT (GPT-3.5)","2022-11",175,False,"LLM","Conversational assistant that sparked the AI consumer revolution",8,True,"First model to reach 100M users in 2 months",elo=1111,elo_est=False),
    model("GPT-4","2023-03",None,True,"Multimodal LLM","Advanced reasoning and vision; first GPT with image understanding",32,True,"Params undisclosed; widely estimated ~1.8T MoE","~1.8T MoE (estimated)",elo=1207,elo_est=False),
    model("GPT-4 Turbo","2023-11",None,True,"LLM","Extended 128K context window; lower cost than GPT-4",128,False,"Introduced 128K context and updated knowledge",elo=1254,elo_est=False),
    model("GPT-4o","2024-05",None,True,"Multimodal","Native omni-modal: text, audio, and vision in one model",128,True,"First model to process audio natively end-to-end",elo=1285,elo_est=False),
    model("GPT-4o mini","2024-07",None,True,"LLM","Small, fast, cheap — replaced GPT-3.5 Turbo in most use cases",128,False,elo=1272,elo_est=False),
    model("o1","2024-09",None,True,"Reasoning","Chain-of-thought reasoning model; top USAMO math performance",128,True,"First in the o-series; thinks before answering",elo=1321,elo_est=False),
    model("o1 Pro","2024-12",None,True,"Reasoning","Higher-compute version of o1 for hardest problems",128,False,elo=1362,elo_est=True),
    model("o3","2025-01",None,True,"Reasoning","Major reasoning leap; near-human on ARC-AGI benchmark",200,True,"Scored 87.5% on ARC-AGI; considered milestone toward AGI",elo=1402,elo_est=False),
    model("GPT-4.5","2025-02",None,True,"LLM","Improved instruction following and reduced hallucinations",128,False,elo=1295,elo_est=True),
    model("GPT-5","2026-01",None,True,"Multimodal LLM","Flagship next-generation model with native agentic capabilities",256,True,"Released alongside ChatGPT agent mode expansion",elo=1460,elo_est=True),
  ],
  "acquisitions": [
    acq("Global Illumination","2023-08","undisclosed","Creative tools team; talent and tech for consumer product design"),
    acq("Rockset","2024-06","undisclosed","Real-time analytics database; strengthens enterprise data infrastructure"),
    acq("Multi","2025-02","undisclosed","Collaborative AI workspace startup"),
  ],
  "notable_investors": ["Microsoft","SoftBank","Thrive Capital","Khosla Ventures","Tiger Global","Sequoia Capital","Andreessen Horowitz","Founders Fund"],
  "tags": ["llm","consumer","enterprise","multimodal","reasoning","ipo-candidate"]
},

{
  "id": "anthropic", "name": "Anthropic", "section": "Frontier AI",
  "founded": 2021, "hq": "San Francisco, CA",
  "color": "#CC785C", "emoji": "🟤",
  "description": "Safety-focused AI lab founded by former OpenAI researchers. Pioneered Constitutional AI. Claude Mythos deployed to critical infrastructure globally. IPO filed Jun 2026.",
  "leadership": [
    {"name": "Dario Amodei", "title": "CEO & Co-founder", "since": "2021-01"},
    {"name": "Daniela Amodei", "title": "President & Co-founder", "since": "2021-01"},
    {"name": "John Jumper", "title": "VP Research (joining)", "since": "2026-06"},
    {"name": "Tom Brown", "title": "VP Research", "since": "2021-01"}
  ],
  "products": [
    {"name": "Claude Mythos", "type": "LLM API", "flagship": True, "description": "Most powerful Claude; in critical infrastructure 15+ countries", "launched": "2026-01"},
    {"name": "Claude Fable 5", "type": "LLM", "flagship": False, "description": "Accessible model capable of generating playable video games", "launched": "2026-06"},
    {"name": "Claude.ai", "type": "Consumer app", "flagship": False, "description": "Web and mobile chat interface", "launched": "2023-07"},
    {"name": "Claude API", "type": "API", "flagship": False, "description": "Developer API with tool use, vision, extended context", "launched": "2023-03"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 9.45, "valuation_usd_billions": 18.0,
    "valuation_as_of": "2024-11", "public": False, "ticker": None,
    "last_round_date": "2024-11", "last_round_amount_usd_billions": 4.0,
    "last_round_type": "Series E", "last_round_investors": ["Amazon","Google","Spark Capital"]
  },
  "funding_rounds_history": [
    round_("2023-04", 0.45, "Series C", "Spark Capital", 4.1, ["Spark Capital","Google","Salesforce"]),
    round_("2023-05", 1.25, "Strategic", "Google", None, ["Google"]),
    round_("2023-09", 1.25, "Strategic", "Amazon", None, ["Amazon"]),
    round_("2024-03", 2.75, "Series C Ext.", "Spark Capital", 18.0, ["Spark Capital","Google","Salesforce","Menlo Ventures"]),
    round_("2024-11", 4.0, "Series E", "Amazon", 18.0, ["Amazon","Google","Spark Capital"]),
  ],
  "model_history": [
    model("Claude 1","2023-03",52,True,"LLM","Constitutional AI-aligned assistant; first Claude release",9,True,"Trained using Constitutional AI; focused on harmlessness",elo=1052,elo_est=True),
    model("Claude 2","2023-07",137,True,"LLM","Major upgrade; 100K context window for long documents",100,True,"First model with 100K token context",elo=1118,elo_est=True),
    model("Claude 3 Haiku","2024-03",20,True,"LLM","Fastest, smallest Claude 3; edge and high-volume use",200,False,elo=1179,elo_est=False),
    model("Claude 3 Sonnet","2024-03",70,True,"LLM","Balanced performance-speed model in the Claude 3 family",200,False,elo=1202,elo_est=False),
    model("Claude 3 Opus","2024-03",None,True,"LLM","Flagship Claude 3; outperformed GPT-4 on most benchmarks",200,True,"First Claude to beat GPT-4 on MMLU","~2T MoE (estimated)",elo=1248,elo_est=False),
    model("Claude 3.5 Sonnet","2024-06",None,True,"LLM","Best coding model at launch; new computer-use capability",200,True,"Introduced Computer Use (agentic GUI interaction)",elo=1298,elo_est=False),
    model("Claude 3.5 Haiku","2024-10",None,True,"LLM","Affordable, fast model competitive with Claude 3 Opus",200,False,elo=1241,elo_est=False),
    model("Claude 3.7 Sonnet","2025-02",None,True,"Reasoning","Extended thinking mode; hybrid instant + reasoning responses",200,True,"First Claude with controllable chain-of-thought depth",elo=1356,elo_est=False),
    model("Claude 4 Sonnet","2025-05",None,True,"LLM","Significant intelligence jump; best-in-class coding",200,True,"Claude 4 family launch alongside Opus 4",elo=1385,elo_est=True),
    model("Claude 4 Opus","2025-05",None,True,"LLM","Most intelligent Claude 4; excels at complex multi-step tasks",200,True,elo=1418,elo_est=True),
    model("Claude Mythos","2026-01",None,True,"LLM","Frontier model deployed to government and critical infrastructure",256,True,"Subject to US government access restrictions Jun 2026",elo=1475,elo_est=True),
    model("Claude Fable 5","2026-06",None,True,"LLM","Accessible model; can generate fully playable video games",200,False,"Based on Mythos architecture, tuned for creative generation",elo=1425,elo_est=True),
  ],
  "acquisitions": [],
  "notable_investors": ["Amazon","Google","Spark Capital","Salesforce Ventures","Menlo Ventures","SK Telecom","Factorial Capital"],
  "tags": ["safety","alignment","enterprise","coding","ipo-candidate","constitutional-ai"]
},

{
  "id": "xai", "name": "xAI", "section": "Frontier AI",
  "founded": 2023, "hq": "Memphis, TN / Austin, TX",
  "color": "#1A1A1A", "emoji": "⚫",
  "description": "AI startup founded by Elon Musk. Grok integrated into X (Twitter). Operates Colossus supercomputer cluster. Under DOJ scrutiny for unpermitted Memphis data center turbines.",
  "leadership": [
    {"name": "Elon Musk", "title": "CEO & Founder", "since": "2023-07"},
    {"name": "Igor Babuschkin", "title": "Chief Scientist", "since": "2023-07"}
  ],
  "products": [
    {"name": "Grok 3", "type": "LLM", "flagship": True, "description": "Frontier model with real-time web access and deep research mode", "launched": "2025-02"},
    {"name": "Aurora", "type": "Image generation", "flagship": False, "description": "Text-to-image model integrated in X", "launched": "2024-08"},
    {"name": "Grok (X integration)", "type": "Consumer AI", "flagship": False, "description": "AI assistant embedded in X/Twitter for all users", "launched": "2023-11"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 6.1, "valuation_usd_billions": 50.0,
    "valuation_as_of": "2024-05", "public": False, "ticker": None,
    "last_round_date": "2024-05", "last_round_amount_usd_billions": 6.0,
    "last_round_type": "Series B", "last_round_investors": ["Andreessen Horowitz","Sequoia","Kingdom Holdings"]
  },
  "funding_rounds_history": [
    round_("2023-12", 0.135, "Seed", "Elon Musk", None, ["Elon Musk","Sequoia Capital","Vy Capital"]),
    round_("2024-05", 6.0, "Series B", "Andreessen Horowitz", 18.0, ["Andreessen Horowitz","Sequoia Capital","Kingdom Holdings"]),
  ],
  "model_history": [
    model("Grok 1","2023-11",314,False,"LLM","Real-time web-connected assistant embedded in X Premium",8,True,"Open-sourced in Mar 2024; 314B MoE architecture confirmed",elo=1151,elo_est=True),
    model("Grok 1.5","2024-03",None,True,"LLM","Improved reasoning; 128K context window",128,False,elo=1213,elo_est=True),
    model("Grok 2","2024-08",None,True,"LLM","Flagship model with Aurora image generation integration",128,True,"Estimated ~540B+ params; released alongside Aurora",elo=1268,elo_est=False),
    model("Grok 3","2025-02",None,True,"LLM","Major capability jump; deep research mode; trained on Colossus",128,True,"Trained on 100K H100 Colossus cluster; competitive with GPT-4o",elo=1358,elo_est=False),
    model("Grok 3 Mini","2025-04",None,True,"Reasoning","Lightweight reasoning model for X integration",128,False,elo=1302,elo_est=True),
  ],
  "acquisitions": [],
  "notable_investors": ["Elon Musk","Andreessen Horowitz","Sequoia Capital","Kingdom Holdings","Vy Capital","Valor Equity Partners"],
  "tags": ["llm","social","real-time","supercomputing","regulatory-issues"]
},

{
  "id": "google_deepmind", "name": "Google DeepMind", "section": "Frontier AI",
  "founded": 2010, "hq": "London, UK / Mountain View, CA",
  "color": "#4285F4", "emoji": "🔷",
  "description": "Alphabet's consolidated AI division (DeepMind + Google Brain merged 2023). Leads Gemini frontier models, AlphaFold science, and AI integration across Google's 3B+ user products.",
  "leadership": [
    {"name": "Demis Hassabis", "title": "CEO, Google DeepMind", "since": "2023-04"},
    {"name": "Sundar Pichai", "title": "CEO, Alphabet", "since": "2019-12"},
    {"name": "Jeff Dean", "title": "Chief Scientist, Google", "since": "2023-04"}
  ],
  "products": [
    {"name": "Gemini 2.5 Pro", "type": "LLM API", "flagship": True, "description": "Top-ranked reasoning model; #1 on LMArena leaderboard mid-2025", "launched": "2025-06"},
    {"name": "Gemini (Google apps)", "type": "Consumer AI", "flagship": False, "description": "AI assistant in Search, Workspace, Android — 3B+ users", "launched": "2024-02"},
    {"name": "NotebookLM", "type": "Consumer app", "flagship": False, "description": "AI research notebook with Audio Overview podcast generation", "launched": "2023-07"},
    {"name": "AlphaFold 3", "type": "Research tool", "flagship": False, "description": "Protein and biomolecule structure prediction", "launched": "2024-05"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": None, "valuation_usd_billions": None,
    "valuation_as_of": None, "public": True, "ticker": "GOOG",
    "last_round_date": None, "last_round_amount_usd_billions": None,
    "last_round_type": None, "last_round_investors": []
  },
  "funding_rounds_history": [],
  "model_history": [
    model("Bard (PaLM 2)","2023-02",None,True,"LLM","Google's first public AI chatbot, powered by PaLM 2",8,False,"Initially limited; widely criticized vs ChatGPT",elo=1049,elo_est=True),
    model("PaLM 2","2023-05",340,True,"LLM","Multilingual reasoning model powering Bard and Workspace AI",8,False,"Powers Google Workspace AI features",elo=1090,elo_est=True),
    model("Gemini 1.0 Nano","2023-12",None,True,"LLM","On-device model for Pixel phones and edge deployments",8,False,elo=1062,elo_est=True),
    model("Gemini 1.0 Pro","2023-12",None,True,"LLM","Mid-tier Gemini for Bard and API; multimodal from launch",32,False,elo=1111,elo_est=True),
    model("Gemini 1.0 Ultra","2023-12",None,True,"Multimodal LLM","Flagship Gemini 1.0; first model to beat GPT-4 on MMLU",32,True,"Scored 90.0% on MMLU; first model to surpass human expert",elo=1220,elo_est=True),
    model("Gemini 1.5 Pro","2024-02",None,True,"Multimodal LLM","Breakthrough 1M token context window; video/audio understanding",1000,True,"1M context = ~11 hours of video or 30K lines of code",elo=1261,elo_est=False),
    model("Gemini 1.5 Flash","2024-05",None,True,"LLM","Fast, efficient Gemini 1.5; low-cost API access",1000,False,elo=1228,elo_est=False),
    model("Gemini 2.0 Flash","2024-12",None,True,"Multimodal LLM","Agentic capabilities; real-time streaming; native tool use",1000,True,"Introduced native agentic multimodal reasoning",elo=1322,elo_est=False),
    model("Gemini 2.5 Pro","2025-06",None,True,"Reasoning LLM","#1 on LMArena; deep thinking mode; coding and math SOTA",1000,True,"Topped every major benchmark at launch in mid-2025",elo=1448,elo_est=False),
  ],
  "acquisitions": [
    acq("DeepMind","2014-01","~$500M","Foundational acquisition; brought AlphaGo, AlphaFold, Gemini research team"),
    acq("Isomorphic Labs (spin-out)","2021-11","internal","Drug discovery spinout using AlphaFold; later merged back"),
  ],
  "notable_investors": ["Alphabet (Google)"],
  "tags": ["research","multimodal","science","consumer","cloud","public-company"]
},

{
  "id": "meta_ai", "name": "Meta AI", "section": "Frontier AI",
  "founded": 2013, "hq": "Menlo Park, CA",
  "color": "#0866FF", "emoji": "🌐",
  "description": "Meta's AI division. Llama open-source models are the most widely deployed in the world. AI integrated across Facebook, Instagram, WhatsApp. Building superintelligence lab (with Alexandr Wang from Scale AI).",
  "leadership": [
    {"name": "Mark Zuckerberg", "title": "CEO, Meta", "since": "2004-02"},
    {"name": "Yann LeCun", "title": "Chief AI Scientist", "since": "2013-12"},
    {"name": "Ahmad Al-Dahle", "title": "VP Generative AI", "since": "2023-01"}
  ],
  "products": [
    {"name": "Llama 4", "type": "Open model", "flagship": True, "description": "Multimodal open-source frontier model (Scout/Maverick variants)", "launched": "2025-04"},
    {"name": "Meta AI Assistant", "type": "Consumer AI", "flagship": False, "description": "AI assistant across FB/Instagram/WhatsApp/Ray-Ban — 1B+ user reach", "launched": "2023-09"},
    {"name": "Facebook AI Mode", "type": "Consumer AI", "flagship": False, "description": "AI mode on Facebook drawing from public platform data", "launched": "2026-06"},
    {"name": "WhatsApp Business AI Agent", "type": "Business tool", "flagship": False, "description": "Globally available AI agent for WhatsApp Business", "launched": "2026-06"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": None, "valuation_usd_billions": None,
    "valuation_as_of": None, "public": True, "ticker": "META",
    "last_round_date": None, "last_round_amount_usd_billions": None,
    "last_round_type": None, "last_round_investors": []
  },
  "funding_rounds_history": [],
  "model_history": [
    model("LLaMA 1","2023-02",65,False,"LLM","Open-source research model that ignited the open-weights movement",2,True,"Released with research paper; weights leaked publicly weeks later",elo=1003,elo_est=True),
    model("LLaMA 2","2023-07",70,False,"LLM","First commercially licensed open LLM from Meta; major ecosystem adoption",4,True,"Partnered with Microsoft for enterprise licensing",elo=1075,elo_est=True),
    model("Code Llama","2023-08",34,False,"LLM","Specialized code generation and explanation model",16,False,"Fine-tuned from Llama 2 on code datasets",elo=1050,elo_est=True),
    model("LLaMA 3 (8B/70B)","2024-04",70,False,"LLM","Significant quality jump over Llama 2; strong multilingual",8,False,elo=1192,elo_est=False),
    model("LLaMA 3.1 405B","2024-07",405,False,"LLM","First open model competitive with GPT-4 Turbo on most benchmarks",128,True,"Landmark: open-source matches closed frontier for first time",elo=1265,elo_est=False),
    model("LLaMA 3.2","2024-09",None,True,"Multimodal","Multimodal vision models (11B/90B) plus edge models (1B/3B)",128,False,"First Llama with vision capability",elo=1218,elo_est=False),
    model("LLaMA 3.3 70B","2024-12",70,False,"LLM","Efficient update; 405B-level performance at 70B params",128,False,elo=1255,elo_est=False),
    model("LLaMA 4 Scout","2025-04",None,True,"Multimodal LLM","17B active (MoE); extremely long 10M token context window",10000,True,"10M context is longest ever; MoE with 16 experts",elo=1309,elo_est=True),
    model("LLaMA 4 Maverick","2025-04",None,True,"Multimodal LLM","128 experts MoE; GPT-4o competitive at fraction of cost",1000,True,"Beats GPT-4o and Gemini 2.0 Flash on benchmarks",elo=1352,elo_est=True),
  ],
  "acquisitions": [
    acq("Scale AI (significant investment)","2025-06","undisclosed","Strategic investment alongside hiring Alexandr Wang for Meta superintelligence lab"),
  ],
  "notable_investors": ["Meta Platforms (internal)"],
  "tags": ["open-source","social","consumer","multimodal","llama","superintelligence-lab","public-company"]
},

# ═══════════════════════════════════════════════════════
# FOUNDATION MODEL LABS
# ═══════════════════════════════════════════════════════

{
  "id": "mistral", "name": "Mistral AI", "section": "Foundation Model Labs",
  "founded": 2023, "hq": "Paris, France",
  "color": "#FF7000", "emoji": "🟠",
  "description": "European open-weight model lab. Pioneer of efficient MoE architecture. Rumored €3B raise at €20B valuation (Jun 2026). Secured $830M debt for Paris data center. First acquisition: Koyeb.",
  "leadership": [
    {"name": "Arthur Mensch", "title": "CEO & Co-founder", "since": "2023-04"},
    {"name": "Timothée Lacroix", "title": "CTO & Co-founder", "since": "2023-04"},
    {"name": "Guillaume Lample", "title": "Chief Scientist & Co-founder", "since": "2023-04"}
  ],
  "products": [
    {"name": "Mistral Large 2", "type": "LLM API", "flagship": True, "description": "123B flagship; strong multilingual and code", "launched": "2024-07"},
    {"name": "Forge", "type": "Enterprise platform", "flagship": False, "description": "Enterprise AI deployment platform launched at NVIDIA GTC 2026", "launched": "2026-03"},
    {"name": "Le Chat", "type": "Consumer app", "flagship": False, "description": "Consumer chat interface; growing European user base", "launched": "2024-02"},
    {"name": "Mistral Speech", "type": "Open model", "flagship": False, "description": "Open-source speech generation model", "launched": "2026-03"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 1.1, "valuation_usd_billions": 22.0,
    "valuation_as_of": "2026-06", "public": False, "ticker": None,
    "last_round_date": "2026-06", "last_round_amount_usd_billions": 3.3,
    "last_round_type": "Series C (rumored)", "last_round_investors": ["Andreessen Horowitz","General Catalyst","Salesforce"]
  },
  "funding_rounds_history": [
    round_("2023-06", 0.113, "Seed", "Lightspeed", 0.26, ["Lightspeed Venture Partners","Xavier Niel","Eric Schmidt"]),
    round_("2023-12", 0.415, "Series A", "Andreessen Horowitz", 2.0, ["Andreessen Horowitz","Lightspeed","Salesforce Ventures","BNP Paribas"]),
    round_("2024-06", 0.645, "Series B", "General Catalyst", 6.0, ["General Catalyst","Andreessen Horowitz","Lightspeed","Salesforce"]),
    round_("2026-03", 0.830, "Debt Facility", "Undisclosed", None, ["Undisclosed banks"]),
    round_("2026-06", 3.3, "Series C (rumored)", "TBD", 22.0, ["TBD"]),
  ],
  "model_history": [
    model("Mistral 7B","2023-09",7.3,False,"LLM","Efficient open model that outperformed Llama 2 13B at 7B params",8,True,"Released with weights; proved smaller models could compete with larger ones",elo=1082,elo_est=True),
    model("Mixtral 8x7B","2023-12",46.7,False,"LLM","MoE architecture using 8 experts; best open model at launch",32,True,"~12B active params at inference; sparked MoE adoption across the industry",elo=1155,elo_est=False),
    model("Mistral Large","2024-02",None,True,"LLM","First closed frontier model from Mistral; via API and Azure",32,True,"Announced alongside Azure partnership; ~123B estimated",elo=1210,elo_est=True),
    model("Mixtral 8x22B","2024-04",141,False,"LLM","Larger MoE; 65K context; strong code and reasoning",64,False,"Active params ~39B; surpassed Llama 2 70B on most tasks",elo=1225,elo_est=False),
    model("Codestral","2024-06",22,False,"LLM","Specialized code completion model; 80+ programming languages",32,False,elo=1103,elo_est=True),
    model("Mistral Nemo","2024-07",12,False,"LLM","12B collaborative model with Nvidia; runs on consumer hardware",128,False,"Jointly developed with Nvidia; designed for local deployment",elo=1168,elo_est=True),
    model("Mistral Large 2","2024-07",123,False,"LLM","Flagship closed model; strong multilingual and 128K context",128,True,"Released same day as Llama 3.1 405B; competitive with GPT-4o",elo=1255,elo_est=False),
    model("Mistral Small 3","2025-01",24,False,"LLM","Updated small model; strong coding and instruction following",32,False,elo=1202,elo_est=True),
    model("Mistral Large 3","2025-06",None,True,"LLM","Updated flagship with improved reasoning and tool use",128,False,elo=1281,elo_est=True),
    model("Mistral Speech","2026-03",None,True,"Audio","Open-source speech synthesis and transcription model",None,False,elo=None,elo_est=True),
  ],
  "acquisitions": [
    acq("Koyeb","2026-02","undisclosed","Cloud infrastructure startup; enables managed Mistral model deployment"),
  ],
  "notable_investors": ["Andreessen Horowitz","General Catalyst","Lightspeed Venture Partners","Salesforce Ventures","BNP Paribas","Xavier Niel","Eric Schmidt"],
  "tags": ["open-source","european","efficient","moe","multilingual","enterprise"]
},

{
  "id": "cohere", "name": "Cohere", "section": "Foundation Model Labs",
  "founded": 2019, "hq": "Toronto, Canada / Berlin, Germany",
  "color": "#39579A", "emoji": "🔵",
  "description": "Enterprise NLP platform. Merged with Germany's Aleph Alpha (Apr 2026) creating a transatlantic AI powerhouse. $240M ARR. Joelle Pineau (ex-Meta AI research head) as Chief AI Officer. IPO candidate.",
  "leadership": [
    {"name": "Aidan Gomez", "title": "CEO & Co-founder", "since": "2019-01"},
    {"name": "Ivan Zhang", "title": "CTO & Co-founder", "since": "2019-01"},
    {"name": "Joelle Pineau", "title": "Chief AI Officer", "since": "2025-08"},
    {"name": "Nick Frosst", "title": "Co-founder", "since": "2019-01"}
  ],
  "products": [
    {"name": "North", "type": "Enterprise AI platform", "flagship": True, "description": "Enterprise AI agent platform launched Aug 2025", "launched": "2025-08"},
    {"name": "Command R+", "type": "LLM API", "flagship": False, "description": "104B enterprise RAG model with 128K context and tool use", "launched": "2024-04"},
    {"name": "Cohere Transcribe", "type": "Speech API", "flagship": False, "description": "Open-source voice transcription model", "launched": "2026-03"},
    {"name": "Embed", "type": "Embeddings API", "flagship": False, "description": "Multilingual embeddings for semantic search and RAG", "launched": "2022-11"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 0.97, "valuation_usd_billions": 7.0,
    "valuation_as_of": "2025-09", "public": False, "ticker": None,
    "last_round_date": "2025-09", "last_round_amount_usd_billions": None,
    "last_round_type": "Valuation update", "last_round_investors": ["PSP Investments","Nvidia","Oracle"]
  },
  "funding_rounds_history": [
    round_("2023-02", 0.270, "Series C", "Inovia Capital", 2.2, ["Inovia Capital","Index Ventures","Tiger Global","Salesforce Ventures"]),
    round_("2024-07", 0.500, "Series D", "PSP Investments", 5.5, ["PSP Investments","Nvidia","Oracle","Salesforce"]),
  ],
  "model_history": [
    model("Command","2022-11",52,True,"LLM","Enterprise instruction-following model; early RAG-focused design",4,False,"Cohere's first commercial model; launched same month as ChatGPT",elo=1020,elo_est=True),
    model("Command Light","2022-11",6,True,"LLM","Lightweight Command variant for high-throughput enterprise use",4,False,elo=990,elo_est=True),
    model("Command R","2024-03",35,False,"LLM","Optimized for retrieval-augmented generation with 128K context",128,True,"Purpose-built for RAG; introduced grounded generation",elo=1100,elo_est=False),
    model("Command R+","2024-04",104,False,"LLM","Enterprise flagship with multi-step tool use and 128K context",128,True,"Competes with GPT-4 Turbo for enterprise RAG workloads",elo=1170,elo_est=False),
    model("Command R (v2)","2025-01",35,False,"LLM","Updated Command R with improved accuracy and reduced hallucination",128,False,elo=1128,elo_est=True),
    model("Command R+ (v2)","2025-03",120,True,"LLM","Updated flagship with stronger reasoning; competitive with Claude 3.5",128,False,elo=1195,elo_est=True),
    model("Cohere Transcribe","2026-03",None,True,"Audio","Enterprise-grade open-source speech transcription",None,False,elo=None,elo_est=True),
  ],
  "acquisitions": [
    acq("Ottogrid","2025-05","undisclosed","AI-powered market research platform; expands enterprise analytics offering"),
    acq("Aleph Alpha (merger)","2026-04","undisclosed","German AI company; creates transatlantic enterprise AI leader with European sovereign AI capabilities"),
  ],
  "notable_investors": ["PSP Investments","Nvidia","Oracle","Salesforce Ventures","Inovia Capital","Index Ventures","Tiger Global","NVIDIA"],
  "tags": ["enterprise","rag","multilingual","search","ipo-candidate","aleph-alpha"]
},

# ═══════════════════════════════════════════════════════
# BIG TECH AI
# ═══════════════════════════════════════════════════════

{
  "id": "microsoft_ai", "name": "Microsoft AI", "section": "Big Tech AI",
  "founded": 1975, "hq": "Redmond, WA",
  "color": "#00BCF2", "emoji": "🪟",
  "description": "Microsoft's AI division. $13B+ invested in OpenAI. Copilot across all products. 20M+ paid Copilot users (Apr 2026). Azure OpenAI Service dominant enterprise AI platform.",
  "leadership": [
    {"name": "Satya Nadella", "title": "CEO, Microsoft", "since": "2014-02"},
    {"name": "Mustafa Suleyman", "title": "EVP & CEO, Microsoft AI", "since": "2024-03"},
    {"name": "Eric Boyd", "title": "CVP, Azure AI", "since": "2022-01"}
  ],
  "products": [
    {"name": "Copilot", "type": "AI assistant", "flagship": True, "description": "AI in Windows, Office 365, Edge, Bing — 20M+ paid users", "launched": "2023-11"},
    {"name": "Azure OpenAI Service", "type": "Cloud API", "flagship": False, "description": "Enterprise access to OpenAI models via Azure", "launched": "2023-01"},
    {"name": "GitHub Copilot", "type": "Developer tool", "flagship": False, "description": "AI code completion in IDEs — millions of developers", "launched": "2022-06"},
    {"name": "Scout", "type": "Personal AI assistant", "flagship": False, "description": "Personal AI assistant for consumer and professional use", "launched": "2026-06"},
    {"name": "Phi-3/Phi-4", "type": "Open model", "flagship": False, "description": "Small language model family for on-device AI", "launched": "2024-04"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": None, "valuation_usd_billions": None,
    "valuation_as_of": None, "public": True, "ticker": "MSFT",
    "last_round_date": None, "last_round_amount_usd_billions": None,
    "last_round_type": None, "last_round_investors": []
  },
  "funding_rounds_history": [],
  "model_history": [],
  "acquisitions": [
    acq("Activision Blizzard","2023-10","$68.7B","Largest gaming acquisition; AI used for procedural content generation and NPCs"),
    acq("Inflection AI (team)","2024-03","~$650M","Acquired most of Inflection team including Mustafa Suleyman; Inflection IP remained separate"),
  ],
  "notable_investors": ["Microsoft (public — MSFT)"],
  "tags": ["enterprise","developer","cloud","copilot","openai-partner","public-company"]
},

{
  "id": "amazon_aws_ai", "name": "Amazon / AWS AI", "section": "Big Tech AI",
  "founded": 1994, "hq": "Seattle, WA",
  "color": "#FF9900", "emoji": "📦",
  "description": "Amazon's AI portfolio: Bedrock (multi-model API), Q (enterprise assistant), Trainium/Inferentia chips. $4B strategic investment in Anthropic. Now selling Trainium chips externally to challenge Nvidia.",
  "leadership": [
    {"name": "Andy Jassy", "title": "CEO, Amazon", "since": "2021-07"},
    {"name": "Matt Garman", "title": "CEO, AWS", "since": "2024-06"},
    {"name": "Swami Sivasubramanian", "title": "VP AI & Data, AWS", "since": "2020-01"}
  ],
  "products": [
    {"name": "Amazon Bedrock", "type": "Cloud AI platform", "flagship": True, "description": "Multi-model managed API (Claude, Llama, Titan, Nova)", "launched": "2023-09"},
    {"name": "Amazon Q", "type": "Enterprise AI assistant", "flagship": False, "description": "Enterprise AI assistant for AWS and business apps", "launched": "2023-11"},
    {"name": "Trainium / Inferentia", "type": "AI chips", "flagship": False, "description": "Custom ML chips — now sold externally to challenge Nvidia", "launched": "2020-12"},
    {"name": "Alexa+", "type": "Consumer AI assistant", "flagship": False, "description": "Generative AI-powered Alexa", "launched": "2024-09"},
    {"name": "Nova (model family)", "type": "LLM", "flagship": False, "description": "Amazon's own foundation model family via Bedrock", "launched": "2024-12"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": None, "valuation_usd_billions": None,
    "valuation_as_of": None, "public": True, "ticker": "AMZN",
    "last_round_date": None, "last_round_amount_usd_billions": None,
    "last_round_type": None, "last_round_investors": []
  },
  "funding_rounds_history": [],
  "model_history": [],
  "acquisitions": [
    acq("Zoox","2020-06","$1.2B","Autonomous vehicle company; AI safety and robotics research"),
    acq("MGM","2021-05","$8.45B","Content library for Alexa and Prime Video AI personalization"),
  ],
  "notable_investors": ["Amazon (public — AMZN)"],
  "tags": ["cloud","enterprise","chips","consumer","anthropic-investor","public-company"]
},

# ═══════════════════════════════════════════════════════
# AI APPLICATIONS
# ═══════════════════════════════════════════════════════

{
  "id": "perplexity", "name": "Perplexity AI", "section": "AI Applications",
  "founded": 2022, "hq": "San Francisco, CA",
  "color": "#20808D", "emoji": "🔍",
  "description": "AI-powered search engine combining LLM answers with real-time web citations. Snap $400M search deal dissolved May 2026. Personal Computer app launched for Mac.",
  "leadership": [
    {"name": "Aravind Srinivas", "title": "CEO & Co-founder", "since": "2022-08"},
    {"name": "Denis Yarats", "title": "CTO & Co-founder", "since": "2022-08"},
    {"name": "Johnny Ho", "title": "President & Co-founder", "since": "2022-08"}
  ],
  "products": [
    {"name": "Perplexity Search", "type": "AI search", "flagship": True, "description": "Answer engine with cited web sources", "launched": "2022-12"},
    {"name": "Perplexity Pro", "type": "Subscription", "flagship": False, "description": "Premium tier — $20/month", "launched": "2024-01"},
    {"name": "Perplexity Personal Computer", "type": "Desktop app", "flagship": False, "description": "Mac app for AI-powered personal knowledge management", "launched": "2026-05"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 0.5, "valuation_usd_billions": 9.0,
    "valuation_as_of": "2024-06", "public": False, "ticker": None,
    "last_round_date": "2024-06", "last_round_amount_usd_billions": 0.25,
    "last_round_type": "Series C", "last_round_investors": ["Nvidia","Bezos Expeditions","IVP"]
  },
  "funding_rounds_history": [],
  "model_history": [],
  "acquisitions": [],
  "notable_investors": ["Nvidia","Bezos Expeditions","IVP","NEA","Databricks"],
  "tags": ["search","consumer","real-time","citations"]
},

{
  "id": "hugging_face", "name": "Hugging Face", "section": "AI Applications",
  "founded": 2016, "hq": "New York, NY / Paris, France",
  "color": "#B8860B", "emoji": "🤗",
  "description": "The 'GitHub of AI' — 500K+ models, 150K+ datasets. Pivoting into robotics with Reachy Mini robot and humanoid acquisitions.",
  "leadership": [
    {"name": "Clément Delangue", "title": "CEO & Co-founder", "since": "2016-01"},
    {"name": "Julien Chaumond", "title": "CTO & Co-founder", "since": "2016-01"},
    {"name": "Thomas Wolf", "title": "CSO & Co-founder", "since": "2016-01"}
  ],
  "products": [
    {"name": "Hub", "type": "Platform", "flagship": True, "description": "Host and discover 500K+ open models, datasets, and demos", "launched": "2019-01"},
    {"name": "Transformers", "type": "Open-source library", "flagship": False, "description": "Most widely used ML library — 130K+ GitHub stars", "launched": "2018-10"},
    {"name": "Spaces", "type": "Demo hosting", "flagship": False, "description": "Free hosting for Gradio/Streamlit AI demos", "launched": "2021-07"},
    {"name": "Reachy Mini", "type": "Robotics", "flagship": False, "description": "Desktop robot for AI interaction research", "launched": "2025-07"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 0.395, "valuation_usd_billions": 4.5,
    "valuation_as_of": "2023-08", "public": False, "ticker": None,
    "last_round_date": "2023-08", "last_round_amount_usd_billions": 0.235,
    "last_round_type": "Series D", "last_round_investors": ["Google","Amazon","Nvidia","Salesforce","AMD"]
  },
  "funding_rounds_history": [],
  "model_history": [],
  "acquisitions": [
    acq("Pollen Robotics","2025-04","undisclosed","French humanoid robotics startup; builds Reachy robot"),
  ],
  "notable_investors": ["Google","Amazon","Nvidia","Salesforce Ventures","AMD","Intel Capital","Lux Capital"],
  "tags": ["open-source","platform","community","models","datasets","robotics"]
},

{
  "id": "stability_ai", "name": "Stability AI", "section": "AI Applications",
  "founded": 2020, "hq": "London, UK",
  "color": "#7B2D8B", "emoji": "🎨",
  "description": "Pioneer of open-source image generation. Getty lawsuit largely dropped Jun 2025. New CEO Sean McClure stabilizing the company after Emad Mostaque's 2024 departure.",
  "leadership": [
    {"name": "Sean McClure", "title": "CEO", "since": "2024-07"},
    {"name": "Emad Mostaque", "title": "Founder (departed)", "since": "2020-01", "departed": "2024-03"}
  ],
  "products": [
    {"name": "Stable Diffusion 3", "type": "Image generation", "flagship": True, "description": "Open-weight text-to-image model", "launched": "2024-06"},
    {"name": "Stable Audio 2", "type": "Audio generation", "flagship": False, "description": "Songs up to 6 minutes; improved quality", "launched": "2026-05"},
    {"name": "Stable Video Diffusion", "type": "Video generation", "flagship": False, "description": "Image-to-video model", "launched": "2023-11"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 0.101, "valuation_usd_billions": 1.0,
    "valuation_as_of": "2024-06", "public": False, "ticker": None,
    "last_round_date": "2022-10", "last_round_amount_usd_billions": 0.101,
    "last_round_type": "Seed", "last_round_investors": ["Coatue","Lightspeed"]
  },
  "funding_rounds_history": [],
  "model_history": [],
  "acquisitions": [],
  "notable_investors": ["Coatue","Lightspeed Venture Partners","O'Shaughnessy Ventures"],
  "tags": ["image-generation","open-source","creative","distressed"]
},

# ═══════════════════════════════════════════════════════
# AI INFRASTRUCTURE
# ═══════════════════════════════════════════════════════

{
  "id": "nvidia", "name": "Nvidia", "section": "AI Infrastructure",
  "founded": 1993, "hq": "Santa Clara, CA",
  "color": "#76B900", "emoji": "🟩",
  "description": "Dominant AI chip maker. Blackwell GPUs shipping. Now targeting $200B CPU market with AI agent PCs. FY2025 revenue ~$130B. Amazon selling Trainium chips as direct competitor.",
  "leadership": [
    {"name": "Jensen Huang", "title": "CEO & Co-founder", "since": "1993-01"},
    {"name": "Colette Kress", "title": "CFO", "since": "2013-09"}
  ],
  "products": [
    {"name": "Blackwell (GB200)", "type": "AI training GPU", "flagship": True, "description": "Next-gen GPU: 30x inference vs H100; shipping 2025", "launched": "2024-03"},
    {"name": "H100 / H200", "type": "AI training GPU", "flagship": False, "description": "Dominant LLM training GPUs — ~80% market share", "launched": "2022-09"},
    {"name": "CUDA", "type": "Software platform", "flagship": False, "description": "GPU programming ecosystem — ~30M developers", "launched": "2007-06"},
    {"name": "NIM Microservices", "type": "AI inference software", "flagship": False, "description": "Containerized AI model deployment", "launched": "2024-03"},
    {"name": "Nvidia AI Agent PCs", "type": "PC platform", "flagship": False, "description": "AI agent PC platform with Microsoft, Dell, HP", "launched": "2026-06"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": None, "valuation_usd_billions": 3000.0,
    "valuation_as_of": "2024-06", "public": True, "ticker": "NVDA",
    "last_round_date": None, "last_round_amount_usd_billions": None,
    "last_round_type": None, "last_round_investors": []
  },
  "funding_rounds_history": [],
  "model_history": [],
  "acquisitions": [
    acq("Mellanox","2020-04","$6.9B","High-speed networking; critical for GPU cluster interconnects"),
    acq("Arm (attempted, blocked)","2022-02","$40B (blocked)","Attempted acquisition blocked by global regulators in Feb 2022"),
  ],
  "notable_investors": ["Nvidia (public — NVDA)"],
  "tags": ["chips","hardware","cuda","infrastructure","datacenter","public-company"]
},

{
  "id": "scale_ai", "name": "Scale AI", "section": "AI Infrastructure",
  "founded": 2016, "hq": "San Francisco, CA",
  "color": "#FF4500", "emoji": "⚖️",
  "description": "Data labeling and AI evaluation platform. CEO Alexandr Wang departed Jun 2025 to join Meta's superintelligence lab. Meta made significant investment. 14% layoff in Jul 2025.",
  "leadership": [
    {"name": "Alexandr Wang", "title": "Founder (departed to Meta)", "since": "2016-01", "departed": "2025-06"},
    {"name": "Lucy Guo", "title": "Co-founder (departed)", "since": "2016-01", "departed": "2017-01"}
  ],
  "products": [
    {"name": "Scale Data Engine", "type": "Data platform", "flagship": True, "description": "End-to-end data labeling, curation, and RLHF pipelines", "launched": "2016-01"},
    {"name": "Donovan", "type": "Defense AI", "flagship": False, "description": "AI decision-making platform for US DoD", "launched": "2023-09"},
    {"name": "SEAL Leaderboards", "type": "Evaluation", "flagship": False, "description": "Independent third-party LLM benchmarks", "launched": "2024-01"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 1.6, "valuation_usd_billions": 13.8,
    "valuation_as_of": "2024-05", "public": False, "ticker": None,
    "last_round_date": "2024-05", "last_round_amount_usd_billions": 1.0,
    "last_round_type": "Series F", "last_round_investors": ["Accel","Tiger Global","Meta"]
  },
  "funding_rounds_history": [],
  "model_history": [],
  "acquisitions": [],
  "notable_investors": ["Accel","Tiger Global","Meta (strategic)","Y Combinator","Founders Fund"],
  "tags": ["data-labeling","rlhf","evaluation","defense","enterprise","leadership-change"]
},

{
  "id": "together_ai", "name": "Together AI", "section": "AI Infrastructure",
  "founded": 2022, "hq": "San Francisco, CA",
  "color": "#6B21A8", "emoji": "🟣",
  "description": "Open-source AI inference and fine-tuning platform. Fast, cheap inference for Llama, Mistral, and other open models via custom GPU clusters.",
  "leadership": [
    {"name": "Vipul Ved Prakash", "title": "CEO & Co-founder", "since": "2022-06"},
    {"name": "Ce Zhang", "title": "Co-founder", "since": "2022-06"},
    {"name": "Christopher Ré", "title": "Co-founder", "since": "2022-06"}
  ],
  "products": [
    {"name": "Together Inference", "type": "Inference API", "flagship": True, "description": "Fast open-model inference API (Llama, Mistral, etc.)", "launched": "2023-06"},
    {"name": "Together Fine-tuning", "type": "Fine-tuning platform", "flagship": False, "description": "Custom model fine-tuning on proprietary data", "launched": "2023-09"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 0.228, "valuation_usd_billions": 1.25,
    "valuation_as_of": "2024-03", "public": False, "ticker": None,
    "last_round_date": "2024-03", "last_round_amount_usd_billions": 0.106,
    "last_round_type": "Series A", "last_round_investors": ["Salesforce Ventures","Nvidia","NEA"]
  },
  "funding_rounds_history": [],
  "model_history": [],
  "acquisitions": [],
  "notable_investors": ["Salesforce Ventures","Nvidia","NEA","Emergence Capital"],
  "tags": ["inference","open-source","fine-tuning","cloud","cost-efficient"]
},


# ═══════════════════════════════════════════════════════
# AI STARTUPS (raised $100M+ in 2025, per TechCrunch Jan 2026)
# ═══════════════════════════════════════════════════════

{
  "id": "elevenlabs", "name": "ElevenLabs", "section": "AI Startups",
  "founded": 2022, "hq": "New York, NY",
  "color": "#6C2BD9", "emoji": "🔊",
  "description": "Leading synthetic voice AI platform. 1,000+ apps integrated. $180M Series C at $3B+ valuation (Jan 2025). Rapidly expanding into audio production, dubbing, and real-time voice cloning.",
  "leadership": [
    {"name": "Mati Staniszewski", "title": "CEO & Co-founder", "since": "2022-01"},
    {"name": "Piotr Dabkowski", "title": "CTO & Co-founder", "since": "2022-01"}
  ],
  "products": [
    {"name": "ElevenLabs Voice AI", "type": "Speech synthesis API", "flagship": True, "description": "Real-time multilingual TTS with voice cloning — 1000+ app integrations", "launched": "2023-01"},
    {"name": "ElevenLabs Studio", "type": "Audio production", "flagship": False, "description": "AI-powered audio production suite for publishers and creators", "launched": "2024-01"},
    {"name": "ElevenReader", "type": "Consumer app", "flagship": False, "description": "App to listen to any text in any voice", "launched": "2024-06"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 0.381, "valuation_usd_billions": 3.3,
    "valuation_as_of": "2025-01", "public": False, "ticker": None,
    "last_round_date": "2025-01", "last_round_amount_usd_billions": 0.180,
    "last_round_type": "Series C", "last_round_investors": ["Iconiq","Andreessen Horowitz","Sequoia"]
  },
  "funding_rounds_history": [
    round_("2023-06", 0.019, "Series A", "Andreessen Horowitz", 0.1, ["Andreessen Horowitz","Nat Friedman","Daniel Gross"]),
    round_("2024-01", 0.080, "Series B", "Andreessen Horowitz", 1.1, ["Andreessen Horowitz","Sequoia","NEA","Salesforce Ventures"]),
    round_("2025-01", 0.180, "Series C", "Iconiq", 3.3, ["Iconiq","Andreessen Horowitz","Sequoia","NEA","Salesforce Ventures"]),
  ],
  "model_history": [
    model("ElevenLabs V1","2023-01",None,True,"TTS","Real-time text-to-speech with natural voices; first commercial product",None,True,"Launched publicly; early viral moment with voice cloning demos",elo=None,elo_est=True),
    model("ElevenLabs V2","2024-03",None,True,"TTS","Improved naturalness; 30+ language support; emotional expressiveness",None,False,"Multilingual expansion; powers major app integrations",elo=None,elo_est=True),
    model("ElevenLabs V3","2025-08",None,True,"TTS","Real-time streaming; <500ms latency; 1000+ voice library",None,True,"Streaming latency milestone; industry-leading quality",elo=None,elo_est=True),
  ],
  "acquisitions": [],
  "notable_investors": ["Iconiq","Andreessen Horowitz","Sequoia","NEA","Salesforce Ventures","Nat Friedman"],
  "tags": ["voice-ai","tts","voice-cloning","audio","consumer","enterprise"]
},

{
  "id": "runway", "name": "Runway", "section": "AI Startups",
  "founded": 2018, "hq": "New York, NY",
  "color": "#0EA5E9", "emoji": "🎬",
  "description": "Pioneer of AI video generation. Gen-3/Gen-4 models power professional media production. $308M Series D at $3B valuation (Apr 2025). Used by major film studios and content creators.",
  "leadership": [
    {"name": "Cristóbal Valenzuela", "title": "CEO & Co-founder", "since": "2018-01"},
    {"name": "Anastasis Germanidis", "title": "CTO & Co-founder", "since": "2018-01"},
    {"name": "Alejandro Matamala", "title": "CPO & Co-founder", "since": "2018-01"}
  ],
  "products": [
    {"name": "Gen-4", "type": "Video generation", "flagship": True, "description": "Cinematic AI video; 4K quality; used in professional film production", "launched": "2025-04"},
    {"name": "Runway Studio", "type": "Creative platform", "flagship": False, "description": "Professional AI creative suite — video, image, audio editing", "launched": "2023-09"},
    {"name": "Act-One", "type": "Character animation", "flagship": False, "description": "Facial expression and performance transfer for characters", "launched": "2024-10"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 0.836, "valuation_usd_billions": 3.0,
    "valuation_as_of": "2025-04", "public": False, "ticker": None,
    "last_round_date": "2025-04", "last_round_amount_usd_billions": 0.308,
    "last_round_type": "Series D", "last_round_investors": ["General Atlantic","SoftBank","Nvidia","Fidelity"]
  },
  "funding_rounds_history": [
    round_("2023-06", 0.141, "Series C", "Google", 1.5, ["Google","Salesforce","Nvidia","Coatue","Felicis"]),
    round_("2024-02", 0.100, "Series C Ext.", "Andreessen Horowitz", 1.5, ["Andreessen Horowitz"]),
    round_("2025-04", 0.308, "Series D", "General Atlantic", 3.0, ["General Atlantic","SoftBank","Nvidia","Fidelity"]),
  ],
  "model_history": [
    model("Gen-1","2023-02",None,True,"Video generation","Text/image-guided video synthesis; launched text-to-video era",None,True,"First Runway consumer model; viral with short clip demos",elo=None,elo_est=True),
    model("Gen-2","2023-06",None,True,"Video generation","Improved consistency and motion quality; multi-modal control",None,True,"First production text-to-video widely used by creators",elo=None,elo_est=True),
    model("Gen-3 Alpha","2024-06",None,True,"Video generation","Photorealistic 1080p; extended motion; competitive with Sora",None,True,"Major quality leap; adopted by film and advertising studios",elo=None,elo_est=True),
    model("Gen-4","2025-04",None,True,"Video generation","Cinematic 4K; consistent characters across scenes; director controls",None,True,"First AI video model used in commercial film production",elo=None,elo_est=True),
  ],
  "acquisitions": [],
  "notable_investors": ["General Atlantic","SoftBank","Nvidia","Fidelity","Google","Salesforce","Coatue","Andreessen Horowitz"],
  "tags": ["video-generation","creative-ai","film","multimodal","enterprise"]
},

{
  "id": "luma_ai", "name": "Luma AI", "section": "AI Startups",
  "founded": 2021, "hq": "San Francisco, CA",
  "color": "#EC4899", "emoji": "✨",
  "description": "AI video and 3D generation platform. Dream Machine and Ray2 models. $900M Series C at $4B valuation (Nov 2025) led by Humain and a16z. Strong developer API ecosystem.",
  "leadership": [
    {"name": "Amit Jain", "title": "CEO & Co-founder", "since": "2021-01"},
    {"name": "Jianing Liu", "title": "CTO & Co-founder", "since": "2021-01"}
  ],
  "products": [
    {"name": "Ray2", "type": "Video generation", "flagship": True, "description": "Advanced text-to-video model; improved realism and motion", "launched": "2025-02"},
    {"name": "Dream Machine", "type": "Video generation", "flagship": False, "description": "Fast text-to-video model; web and API access", "launched": "2024-06"},
    {"name": "Luma Photon", "type": "Image generation", "flagship": False, "description": "Fast, high-quality image generation API", "launched": "2024-10"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 1.05, "valuation_usd_billions": 4.0,
    "valuation_as_of": "2025-11", "public": False, "ticker": None,
    "last_round_date": "2025-11", "last_round_amount_usd_billions": 0.900,
    "last_round_type": "Series C", "last_round_investors": ["Humain","Andreessen Horowitz","AMD Ventures"]
  },
  "funding_rounds_history": [
    round_("2023-05", 0.043, "Series B", "Andreessen Horowitz", 0.2, ["Andreessen Horowitz","Kleiner Perkins","Nvidia"]),
    round_("2024-05", 0.043, "Series B Ext.", "Andreessen Horowitz", 0.4, ["Andreessen Horowitz"]),
    round_("2025-11", 0.900, "Series C", "Humain", 4.0, ["Humain","Andreessen Horowitz","AMD Ventures","Amplify Partners"]),
  ],
  "model_history": [
    model("Dream Machine","2024-06",None,True,"Video generation","Fast text-to-video with strong motion quality and 120s generations",None,True,"Launched same week as Sora; immediate developer adoption",elo=None,elo_est=True),
    model("Luma Photon","2024-10",None,True,"Image generation","High-quality image generation with strong prompt adherence",None,False,"Fast API-first model for developers",elo=None,elo_est=True),
    model("Ray2","2025-02",None,True,"Video generation","Improved temporal consistency and realistic physics over Dream Machine",None,True,"Significant quality improvement; introduced cinematic motion",elo=None,elo_est=True),
  ],
  "acquisitions": [],
  "notable_investors": ["Humain","Andreessen Horowitz","AMD Ventures","Kleiner Perkins","Nvidia","Amplify Partners"],
  "tags": ["video-generation","3d","image-generation","creative-ai","developer-api"]
},

{
  "id": "reka_ai", "name": "Reka AI", "section": "AI Startups",
  "founded": 2023, "hq": "San Francisco, CA",
  "color": "#14B8A6", "emoji": "🌊",
  "description": "Multimodal AI research lab. Reka Core, Flash, and Edge models cover frontier to edge deployment. $110M Series B at $1B valuation (Jul 2025), backed by Snowflake and Nvidia.",
  "leadership": [
    {"name": "Dani Yogatama", "title": "CEO & Co-founder", "since": "2023-01"},
    {"name": "Cyprien de Masson d'Autume", "title": "Co-founder", "since": "2023-01"},
    {"name": "Yi Tay", "title": "Chief Scientist", "since": "2023-01"}
  ],
  "products": [
    {"name": "Reka Core", "type": "Multimodal LLM API", "flagship": True, "description": "Flagship model; strong vision-language understanding; 128K context", "launched": "2024-11"},
    {"name": "Reka Flash", "type": "LLM API", "flagship": False, "description": "Fast, efficient model for production workloads", "launched": "2024-06"},
    {"name": "Reka Edge", "type": "On-device LLM", "flagship": False, "description": "7B model for edge deployment and low-latency inference", "launched": "2024-01"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 0.166, "valuation_usd_billions": 1.0,
    "valuation_as_of": "2025-07", "public": False, "ticker": None,
    "last_round_date": "2025-07", "last_round_amount_usd_billions": 0.110,
    "last_round_type": "Series B", "last_round_investors": ["Snowflake","Nvidia"]
  },
  "funding_rounds_history": [
    round_("2024-04", 0.058, "Series A", "DST Global", 0.5, ["DST Global","Radical Ventures","Snowflake"]),
    round_("2025-07", 0.110, "Series B", "Snowflake", 1.0, ["Snowflake","Nvidia"]),
  ],
  "model_history": [
    model("Reka Edge","2024-01",7,False,"Multimodal LLM","Efficient 7B model for on-device and low-latency deployment",32,False,"Optimized for edge; competitive with Mistral 7B",elo=1089,elo_est=True),
    model("Reka Flash","2024-06",21,False,"Multimodal LLM","Balanced performance-speed; vision and text understanding",128,False,"Fast inference; strong multimodal benchmarks",elo=1145,elo_est=True),
    model("Reka Core","2024-11",65,True,"Multimodal LLM","Flagship model; competitive with GPT-4V on vision-language tasks",128,True,"Competes with Claude 3 Opus on multimodal benchmarks",elo=1218,elo_est=False),
  ],
  "acquisitions": [],
  "notable_investors": ["Snowflake","Nvidia","DST Global","Radical Ventures"],
  "tags": ["multimodal","llm","edge","research","enterprise"]
},

{
  "id": "cognition_ai", "name": "Cognition AI", "section": "AI Startups",
  "founded": 2023, "hq": "San Francisco, CA",
  "color": "#F59E0B", "emoji": "🤖",
  "description": "Creator of Devin, the world's first AI software engineer. $400M Series C at $10.2B valuation (Sep 2025) led by Founders Fund. Devin autonomously writes and deploys production code.",
  "leadership": [
    {"name": "Scott Wu", "title": "CEO & Co-founder", "since": "2023-11"},
    {"name": "Steven Hao", "title": "Co-founder", "since": "2023-11"},
    {"name": "Walden Yan", "title": "Co-founder", "since": "2023-11"}
  ],
  "products": [
    {"name": "Devin 2.0", "type": "AI software engineer", "flagship": True, "description": "Autonomous AI agent that codes, debugs, and deploys full projects", "launched": "2025-09"},
    {"name": "Devin API", "type": "Developer API", "flagship": False, "description": "API access to Devin for CI/CD integration and enterprise workflows", "launched": "2024-09"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 0.421, "valuation_usd_billions": 10.2,
    "valuation_as_of": "2025-09", "public": False, "ticker": None,
    "last_round_date": "2025-09", "last_round_amount_usd_billions": 0.400,
    "last_round_type": "Series C", "last_round_investors": ["Founders Fund"]
  },
  "funding_rounds_history": [
    round_("2024-03", 0.021, "Series A", "Founders Fund", 2.0, ["Founders Fund","Peter Thiel","Elad Gil"]),
    round_("2025-09", 0.400, "Series C", "Founders Fund", 10.2, ["Founders Fund"]),
  ],
  "model_history": [
    model("Devin 1.0","2024-03",None,True,"Agentic LLM","AI software engineer; writes, runs, and debugs production code autonomously",None,True,"First demo went viral; scored 13.86% on SWE-bench vs 1.96% prior SOTA",elo=None,elo_est=True),
    model("Devin 2.0","2025-09",None,True,"Agentic LLM","Full project lifecycle — planning, coding, testing, and deployment",None,True,"10x capability improvement; handles multi-file repos end-to-end",elo=None,elo_est=True),
  ],
  "acquisitions": [],
  "notable_investors": ["Founders Fund","Peter Thiel","Elad Gil","SV Angel"],
  "tags": ["coding-agent","software-engineering","agentic","enterprise","developer"]
},

{
  "id": "thinking_machines", "name": "Thinking Machines Lab", "section": "AI Startups",
  "founded": 2025, "hq": "San Francisco, CA",
  "color": "#7C3AED", "emoji": "🧪",
  "description": "Stealth AI research lab founded by Mira Murati (ex-OpenAI CTO) in July 2025. $2B seed round at $12B valuation led by Andreessen Horowitz. Focus on reasoning and inference optimization. No public model releases yet.",
  "leadership": [
    {"name": "Mira Murati", "title": "CEO & Founder", "since": "2025-07"},
    {"name": "Jared Kaplan", "title": "Chief Scientist", "since": "2025-07"}
  ],
  "products": [
    {"name": "TML-1 (unreleased)", "type": "LLM (stealth)", "flagship": True, "description": "Frontier reasoning model in development; no public release yet", "launched": "2026-01"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 2.0, "valuation_usd_billions": 12.0,
    "valuation_as_of": "2025-07", "public": False, "ticker": None,
    "last_round_date": "2025-07", "last_round_amount_usd_billions": 2.0,
    "last_round_type": "Seed", "last_round_investors": ["Andreessen Horowitz","Nvidia","Accel","AMD"]
  },
  "funding_rounds_history": [
    round_("2025-07", 2.0, "Seed", "Andreessen Horowitz", 12.0, ["Andreessen Horowitz","Nvidia","Accel","AMD"]),
  ],
  "model_history": [],
  "acquisitions": [],
  "notable_investors": ["Andreessen Horowitz","Nvidia","Accel","AMD"],
  "tags": ["stealth","research","reasoning","frontier","mira-murati"]
},

{
  "id": "sierra_ai", "name": "Sierra", "section": "AI Startups",
  "founded": 2023, "hq": "San Francisco, CA",
  "color": "#10B981", "emoji": "🏔️",
  "description": "Enterprise AI customer service platform founded by Bret Taylor (ex-Salesforce co-CEO, OpenAI Chair) and Clay Bavor (ex-Google VP). $350M at $10B+ valuation (Sep 2025). Customers include Sonos, Weight Watchers.",
  "leadership": [
    {"name": "Bret Taylor", "title": "CEO & Co-founder", "since": "2023-01"},
    {"name": "Clay Bavor", "title": "Co-founder", "since": "2023-01"}
  ],
  "products": [
    {"name": "Sierra Platform", "type": "AI agent platform", "flagship": True, "description": "Conversational AI agents for customer service and business workflows", "launched": "2024-03"},
    {"name": "Sierra Nucleus", "type": "Orchestration layer", "flagship": False, "description": "Agent memory, reasoning, and escalation management", "launched": "2024-09"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 0.735, "valuation_usd_billions": 10.0,
    "valuation_as_of": "2025-09", "public": False, "ticker": None,
    "last_round_date": "2025-09", "last_round_amount_usd_billions": 0.350,
    "last_round_type": "Series C", "last_round_investors": ["Greenoaks Capital"]
  },
  "funding_rounds_history": [
    round_("2023-10", 0.110, "Series A", "Sequoia", 1.0, ["Sequoia","Benchmark"]),
    round_("2024-09", 0.175, "Series B", "Greenoaks Capital", 4.5, ["Greenoaks Capital","Sequoia","Benchmark"]),
    round_("2025-09", 0.350, "Series C", "Greenoaks Capital", 10.0, ["Greenoaks Capital"]),
  ],
  "model_history": [],
  "acquisitions": [],
  "notable_investors": ["Greenoaks Capital","Sequoia","Benchmark"],
  "tags": ["customer-service","enterprise","agents","bret-taylor","cx"]
},

{
  "id": "cursor", "name": "Cursor (Anysphere)", "section": "AI Startups",
  "founded": 2022, "hq": "San Francisco, CA",
  "color": "#2563EB", "emoji": "⌨️",
  "description": "Fastest-growing AI coding tool. $2.3B raised in 2025; $29.3B valuation by Nov 2025. Millions of developers using Cursor for AI-assisted coding. Pioneered 'vibe coding' — natural language to full applications.",
  "leadership": [
    {"name": "Michael Truell", "title": "CEO & Co-founder", "since": "2022-01"},
    {"name": "Sualeh Asif", "title": "Co-founder", "since": "2022-01"},
    {"name": "Aman Sanger", "title": "Co-founder", "since": "2022-01"},
    {"name": "Arvid Lunnemark", "title": "Co-founder", "since": "2022-01"}
  ],
  "products": [
    {"name": "Cursor IDE", "type": "AI code editor", "flagship": True, "description": "AI-first code editor with multi-model support (Claude, GPT-4, Gemini)", "launched": "2023-03"},
    {"name": "Cursor Agent", "type": "Agentic coding", "flagship": False, "description": "Autonomous coding agent for full-feature implementation", "launched": "2025-01"},
    {"name": "BugBot", "type": "Code review", "flagship": False, "description": "AI pull request reviewer that catches bugs before merge", "launched": "2025-06"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 3.3, "valuation_usd_billions": 29.3,
    "valuation_as_of": "2025-11", "public": False, "ticker": None,
    "last_round_date": "2025-11", "last_round_amount_usd_billions": 2.3,
    "last_round_type": "Series D", "last_round_investors": ["Thrive Capital","Andreessen Horowitz","Accel"]
  },
  "funding_rounds_history": [
    round_("2024-01", 0.060, "Series A", "Andreessen Horowitz", 0.4, ["Andreessen Horowitz","OpenAI Startup Fund"]),
    round_("2025-06", 0.900, "Series C", "Thrive Capital", 10.0, ["Thrive Capital","Andreessen Horowitz","Accel","DST Global"]),
    round_("2025-11", 2.3, "Series D", "Thrive Capital", 29.3, ["Thrive Capital","Andreessen Horowitz","Accel"]),
  ],
  "model_history": [],
  "acquisitions": [],
  "notable_investors": ["Thrive Capital","Andreessen Horowitz","Accel","DST Global","OpenAI Startup Fund"],
  "tags": ["coding","developer-tools","vibe-coding","ide","agentic"]
},

{
  "id": "harvey_ai", "name": "Harvey", "section": "AI Startups",
  "founded": 2022, "hq": "San Francisco, CA",
  "color": "#DC2626", "emoji": "⚖️",
  "description": "AI platform for the legal industry. Used by leading law firms including A&O Shearman, PwC, and Allen & Overy. $600M raised in 2025 alone; $5B valuation by mid-2025. Backed by OpenAI Startup Fund.",
  "leadership": [
    {"name": "Winston Weinberg", "title": "CEO & Co-founder", "since": "2022-11"},
    {"name": "Gabriel Pereyra", "title": "CTO & Co-founder", "since": "2022-11"}
  ],
  "products": [
    {"name": "Harvey Platform", "type": "Legal AI platform", "flagship": True, "description": "AI for legal research, drafting, due diligence, and contract analysis", "launched": "2023-03"},
    {"name": "Harvey Document Review", "type": "AI workflow", "flagship": False, "description": "Automated document review for M&A, litigation, and compliance", "launched": "2024-01"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 0.716, "valuation_usd_billions": 5.0,
    "valuation_as_of": "2025-06", "public": False, "ticker": None,
    "last_round_date": "2025-06", "last_round_amount_usd_billions": 0.300,
    "last_round_type": "Series E", "last_round_investors": ["Kleiner Perkins","Coatue"]
  },
  "funding_rounds_history": [
    round_("2023-04", 0.021, "Series A", "OpenAI Startup Fund", 0.1, ["OpenAI Startup Fund","Sequoia"]),
    round_("2024-05", 0.080, "Series B", "Sequoia", 0.7, ["Sequoia","Kleiner Perkins","Elad Gil"]),
    round_("2025-02", 0.300, "Series D", "Sequoia", 3.0, ["Sequoia","OpenAI Startup Fund","Kleiner Perkins","Elad Gil"]),
    round_("2025-06", 0.300, "Series E", "Kleiner Perkins", 5.0, ["Kleiner Perkins","Coatue"]),
  ],
  "model_history": [],
  "acquisitions": [],
  "notable_investors": ["Kleiner Perkins","Coatue","Sequoia","OpenAI Startup Fund","Elad Gil"],
  "tags": ["legal-ai","enterprise","legaltech","law-firms","document-review"]
},

{
  "id": "glean", "name": "Glean", "section": "AI Startups",
  "founded": 2019, "hq": "Palo Alto, CA",
  "color": "#0284C7", "emoji": "🔎",
  "description": "Enterprise AI search and knowledge platform. $150M Series F at $7.25B valuation (Jun 2025). Connects to 100+ enterprise SaaS tools. Used by Duolingo, Databricks, Okta.",
  "leadership": [
    {"name": "Arvind Jain", "title": "CEO & Co-founder", "since": "2019-01"},
    {"name": "T.R. Vishwanath", "title": "Co-founder", "since": "2019-01"}
  ],
  "products": [
    {"name": "Glean Work AI", "type": "Enterprise AI search", "flagship": True, "description": "AI search across all company tools — Slack, Drive, Jira, Salesforce, 100+ more", "launched": "2021-05"},
    {"name": "Glean Agents", "type": "AI agents", "flagship": False, "description": "Autonomous agents that take action across enterprise systems", "launched": "2025-03"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 0.615, "valuation_usd_billions": 7.25,
    "valuation_as_of": "2025-06", "public": False, "ticker": None,
    "last_round_date": "2025-06", "last_round_amount_usd_billions": 0.150,
    "last_round_type": "Series F", "last_round_investors": ["Wellington Management","Sequoia","Lightspeed","Kleiner Perkins"]
  },
  "funding_rounds_history": [
    round_("2022-05", 0.100, "Series C", "Sequoia", 1.0, ["Sequoia","Lightspeed","General Catalyst","Kleiner Perkins"]),
    round_("2023-02", 0.200, "Series D", "Kleiner Perkins", 2.2, ["Kleiner Perkins","Sequoia","Lightspeed","Coatue"]),
    round_("2024-02", 0.200, "Series E", "Coatue", 4.6, ["Coatue","Kleiner Perkins","Sequoia","Lightspeed"]),
    round_("2025-06", 0.150, "Series F", "Wellington Management", 7.25, ["Wellington Management","Sequoia","Lightspeed","Kleiner Perkins"]),
  ],
  "model_history": [],
  "acquisitions": [],
  "notable_investors": ["Wellington Management","Kleiner Perkins","Sequoia","Lightspeed","Coatue","General Catalyst"],
  "tags": ["enterprise-search","knowledge-management","rag","saas","enterprise"]
},

{
  "id": "cerebras", "name": "Cerebras Systems", "section": "AI Startups",
  "founded": 2016, "hq": "Sunnyvale, CA",
  "color": "#EA580C", "emoji": "🧠",
  "description": "AI hardware company building the world's largest chip — the Wafer Scale Engine (WSE-3). $1.1B Series G at $8.1B valuation (Sep 2025). IPO filed Oct 2024; withdrawn. Provides ultra-fast AI inference challenging Nvidia.",
  "leadership": [
    {"name": "Andrew Feldman", "title": "CEO & Co-founder", "since": "2016-01"},
    {"name": "Sean Lie", "title": "Chief Hardware Architect & Co-founder", "since": "2016-01"}
  ],
  "products": [
    {"name": "WSE-3 (Wafer Scale Engine)", "type": "AI chip", "flagship": True, "description": "4 trillion transistors; 44GB on-chip SRAM; world's largest chip", "launched": "2024-03"},
    {"name": "Cerebras Inference", "type": "Inference API", "flagship": False, "description": "Ultra-fast LLM inference — 1,000+ tokens/sec on Llama models", "launched": "2024-09"},
    {"name": "Cerebras Cloud", "type": "AI cloud", "flagship": False, "description": "Cloud access to WSE-powered AI compute", "launched": "2023-11"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 1.682, "valuation_usd_billions": 8.1,
    "valuation_as_of": "2025-09", "public": False, "ticker": None,
    "last_round_date": "2025-09", "last_round_amount_usd_billions": 1.1,
    "last_round_type": "Series G", "last_round_investors": ["Fidelity","Atreides Management"]
  },
  "funding_rounds_history": [
    round_("2021-11", 0.250, "Series F", "Alpha Wave", 4.0, ["Alpha Wave","Coatue","Benchmark"]),
    round_("2024-08", 0.100, "Series F Ext.", "Abu Dhabi Growth Fund", 4.0, ["Abu Dhabi Growth Fund"]),
    round_("2025-09", 1.100, "Series G", "Fidelity", 8.1, ["Fidelity","Atreides Management"]),
  ],
  "model_history": [
    model("Cerebras-GPT 1.3B","2023-03",1.3,False,"LLM","Open-weight model demonstrating linear scaling on Cerebras WSE",None,False,"Released open-weight; showed hardware efficiency advantages",elo=None,elo_est=True),
    model("Cerebras-GPT 6.7B","2023-03",6.7,False,"LLM","Medium-scale open model; trained on Pile dataset",None,False,"Part of the first suite of Cerebras open models",elo=None,elo_est=True),
    model("Cerebras-GPT 13B","2023-03",13,False,"LLM","Largest of original Cerebras open models; competitive with Llama 13B",None,True,"Trained in 50% fewer steps than comparable models on GPU clusters",elo=None,elo_est=True),
  ],
  "acquisitions": [],
  "notable_investors": ["Fidelity","Atreides Management","Alpha Wave","Coatue","Abu Dhabi Growth Fund","Benchmark"],
  "tags": ["ai-chips","hardware","inference","wse","infrastructure","ipo-withdrawn"]
},

{
  "id": "groq", "name": "Groq", "section": "AI Startups",
  "founded": 2016, "hq": "Mountain View, CA",
  "color": "#F97316", "emoji": "⚡",
  "description": "AI inference chip company (LPU — Language Processing Unit). $750M Series D at ~$6.9B valuation (Sep 2025). Provides the world's fastest public LLM inference API, serving open-source models at 1000+ tokens/sec.",
  "leadership": [
    {"name": "Jonathan Ross", "title": "CEO & Co-founder", "since": "2016-01"}
  ],
  "products": [
    {"name": "GroqCloud API", "type": "Inference API", "flagship": True, "description": "Fastest public LLM API — Llama, Mistral, Gemma at 800-1500 tok/sec", "launched": "2024-03"},
    {"name": "LPU Inference Engine", "type": "AI chip", "flagship": False, "description": "Language Processing Unit — deterministic, ultra-low-latency inference chip", "launched": "2023-01"},
    {"name": "GroqRack", "type": "On-prem hardware", "flagship": False, "description": "LPU-based on-premises inference server for enterprise", "launched": "2024-09"},
  ],
  "funding_summary": {
    "total_raised_usd_billions": 1.093, "valuation_usd_billions": 6.9,
    "valuation_as_of": "2025-09", "public": False, "ticker": None,
    "last_round_date": "2025-09", "last_round_amount_usd_billions": 0.750,
    "last_round_type": "Series D", "last_round_investors": ["Disruptive Technology Advisers"]
  },
  "funding_rounds_history": [
    round_("2021-04", 0.300, "Series C", "Tiger Global", 1.0, ["Tiger Global","TDK Ventures","Geodesic Capital"]),
    round_("2024-08", 0.640, "Series D-2", "BlackRock", 2.8, ["BlackRock","Neuberger Berman","Samsung Catalyst"]),
    round_("2025-09", 0.750, "Series D-3", "Disruptive Technology Advisers", 6.9, ["Disruptive Technology Advisers"]),
  ],
  "model_history": [],
  "acquisitions": [],
  "notable_investors": ["BlackRock","Tiger Global","Disruptive Technology Advisers","Neuberger Berman","Samsung Catalyst","TDK Ventures"],
  "tags": ["ai-chips","inference","lpu","hardware","developer-api","speed"]
},

] # end COMPANIES

# ── Load existing snapshots and merge ─────────────────────────────────────
with open(OUT) as f:
    old = json.load(f)

existing_snapshots = old.get("weekly_snapshots", [])

# ── Output ─────────────────────────────────────────────────────────────────
out = {
    "schema_version": "1.1",
    "last_updated": "2026-06-25",
    "companies": COMPANIES,
    "weekly_snapshots": existing_snapshots,
}

with open(OUT, "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print(f"Wrote {OUT}")
print(f"  Companies: {len(COMPANIES)}")
print(f"  Snapshots: {len(existing_snapshots)}")
total_models = sum(len(c.get("model_history",[]) or []) for c in COMPANIES)
print(f"  Model history entries: {total_models}")
