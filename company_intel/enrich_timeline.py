"""
Enrichment pass 2: adds lead_time and key_events to all company JSONs.
Run: python3 enrich_timeline.py
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data" / "companies"

TIMELINE_DATA = {
    "sk_hynix": {
        "lead_time": {
            "total_months_to_token": 12,
            "description": "HBM wafer-out → tokens served ≈ 12 months under normal conditions. TSMC CoWoS slot is the rate-limiter (18-month capacity lead time for new capacity).",
            "bottleneck": "TSMC CoWoS packaging slot — 18-month lead for new capacity additions",
            "pipeline": [
                {"stage": "HBM wafer production", "weeks": 10, "owner": "SK Hynix"},
                {"stage": "TSMC CoWoS bonding (HBM + GPU die)", "weeks": 12, "owner": "TSMC"},
                {"stage": "GPU module & server assembly", "weeks": 6, "owner": "NVIDIA + ODM"},
                {"stage": "Hyperscaler rack integration & burn-in", "weeks": 6, "owner": "Microsoft / Google / AWS"},
                {"stage": "DC networking, software, deployment", "weeks": 14, "owner": "Hyperscaler ops"},
                {"stage": "Tokens served (inference online)", "weeks": 0, "owner": "End users"}
            ]
        },
        "key_events": [
            {"date": "2023-07", "event": "HBM3 mass production for NVIDIA H100 — first ever HBM3 at volume", "category": "product", "significance": "high"},
            {"date": "2024-01", "event": "HBM3e 8-Hi (24GB) enters mass production for H200", "category": "product", "significance": "high"},
            {"date": "2024-04", "event": "Q1 2024 earnings: HBM revenue surpasses commodity DRAM for first time", "category": "financial", "significance": "high"},
            {"date": "2024-06", "event": "HBM3e qualification confirmed for NVIDIA H200; SK Hynix sole supplier at launch", "category": "product", "significance": "high"},
            {"date": "2024-07", "event": "Indiana advanced packaging plant groundbreaking (with Purdue University)", "category": "capacity", "significance": "medium"},
            {"date": "2024-10", "event": "HBM3e 12-Hi (36GB stack) sampling begins for Blackwell B200", "category": "product", "significance": "high"},
            {"date": "2025-01", "event": "HBM4 (32GB, 2.0 TB/s) sampling begins — target NVIDIA GB300 Blackwell Ultra", "category": "product", "significance": "high"},
            {"date": "2025-04", "event": "Q1 2025 record: KRW 17.6T revenue, operating margin 40%+", "category": "financial", "significance": "medium"},
            {"date": "2025-06", "event": "Big Tech offers to fund SK Hynix fab expansion — available capacity 'essentially zero'", "category": "capacity", "significance": "high"},
            {"date": "2025-09", "event": "$13B investment announced for new South Korea M15X HBM plant", "category": "capacity", "significance": "high"},
            {"date": "2026-01", "event": "HBM4E sampling confirmed for H2 2026 — roadmap extends to next Blackwell generation", "category": "product", "significance": "high"},
            {"date": "2026-04", "event": "Q1 2026 record: KRW 52.5T revenue (+198% YoY), 72% operating margin", "category": "financial", "significance": "high"},
            {"date": "2026-04", "event": "Indiana US packaging plant breaks ground (advanced HBM packaging, CHIPS Act)", "category": "capacity", "significance": "medium"}
        ]
    },
    "samsung_semiconductor": {
        "lead_time": {
            "total_months_to_token": 14,
            "description": "Samsung HBM → tokens ≈ 14 months. Longer than SK Hynix because NVIDIA qualification is still pending, adding 2-month uncertainty buffer.",
            "bottleneck": "NVIDIA HBM3e yield qualification — still unresolved as of Q1 2026 for Blackwell",
            "pipeline": [
                {"stage": "HBM wafer production", "weeks": 10, "owner": "Samsung DS"},
                {"stage": "TSMC CoWoS packaging (for AMD/Google path)", "weeks": 12, "owner": "TSMC"},
                {"stage": "GPU module assembly (AMD MI300X / Google TPU)", "weeks": 5, "owner": "AMD / Google ODM"},
                {"stage": "Server integration & testing", "weeks": 6, "owner": "Dell / Google"},
                {"stage": "Hyperscaler rack deployment", "weeks": 8, "owner": "Microsoft Azure / Google Cloud"},
                {"stage": "Tokens served", "weeks": 0, "owner": "End users"}
            ]
        },
        "key_events": [
            {"date": "2023-06", "event": "HBM3 production for AMD MI300X — Samsung primary supplier for AMD", "category": "product", "significance": "high"},
            {"date": "2024-01", "event": "HBM3e 8-Hi starts mass production for AMD MI300X and Google TPU v5", "category": "product", "significance": "high"},
            {"date": "2024-05", "event": "NVIDIA HBM3e qualification failure reported — yield issues on thermal/electrical spec", "category": "risk", "significance": "high"},
            {"date": "2024-09", "event": "CEO Lee Jae-yong restructures DS Division; MX division head replaced amid HBM crisis", "category": "org", "significance": "high"},
            {"date": "2024-11", "event": "Second attempt at NVIDIA HBM3e qualification; timeline slips to 2025", "category": "product", "significance": "high"},
            {"date": "2025-02", "event": "HBM3 12-Hi (36GB) development announced; focus shifts to B200 opportunity", "category": "product", "significance": "medium"},
            {"date": "2025-05", "event": "NVIDIA HBM3e qualification reportedly passed for partial B200 supply", "category": "product", "significance": "high"},
            {"date": "2025-07", "event": "HBM4 roadmap confirmed — 1-2 quarters behind SK Hynix per analyst estimates", "category": "product", "significance": "medium"},
            {"date": "2026-01", "event": "Record semiconductor profit announced: KRW 53.7T for FY2025", "category": "financial", "significance": "high"},
            {"date": "2026-04", "event": "Q1 2026 DS revenue KRW 28T — HBM share grows despite NVIDIA qualification delay", "category": "financial", "significance": "medium"},
            {"date": "2026-04", "event": "Internal strife report: engineering exodus to SK Hynix affects HBM yield recovery", "category": "risk", "significance": "high"}
        ]
    },
    "micron": {
        "lead_time": {
            "total_months_to_token": 11,
            "description": "Micron HBM → tokens ≈ 11 months. Slightly faster than SK Hynix because Micron's Idaho fab is geographically closer to some US hyperscaler datacenters, reducing logistics time.",
            "bottleneck": "TSMC CoWoS slot (same as SK Hynix) — Idaho packaging capacity not yet online",
            "pipeline": [
                {"stage": "HBM wafer production (Idaho/Singapore)", "weeks": 9, "owner": "Micron"},
                {"stage": "TSMC CoWoS packaging", "weeks": 12, "owner": "TSMC"},
                {"stage": "GPU module assembly", "weeks": 5, "owner": "NVIDIA + ODM"},
                {"stage": "Server integration & testing", "weeks": 5, "owner": "Dell / Supermicro"},
                {"stage": "US hyperscaler deployment (closer logistics)", "weeks": 5, "owner": "Microsoft / AWS"},
                {"stage": "Tokens served", "weeks": 0, "owner": "End users"}
            ]
        },
        "key_events": [
            {"date": "2024-02", "event": "HBM3e qualification announced for NVIDIA H200 — first US company to achieve this", "category": "product", "significance": "high"},
            {"date": "2024-06", "event": "HBM3e 8-Hi mass production begins; Micron starts shipping to NVIDIA for H200 partial allocation", "category": "product", "significance": "high"},
            {"date": "2024-08", "event": "CHIPS Act funding confirmed: $6.1B for Idaho HBM fab expansion", "category": "capacity", "significance": "high"},
            {"date": "2024-11", "event": "Idaho fab groundbreaking for HBM-dedicated production (Boise, ID)", "category": "capacity", "significance": "high"},
            {"date": "2025-01", "event": "HBM market share reaches 13% — fastest-growing among three suppliers", "category": "product", "significance": "medium"},
            {"date": "2025-03", "event": "FY2025 Q2 earnings: $7.9B revenue, HBM revenue 'exceeds $1B per quarter' for first time", "category": "financial", "significance": "high"},
            {"date": "2025-06", "event": "CEO Sanjay Mehrotra: 'AI memory demand in first innings; supply already insufficient'", "category": "strategy", "significance": "high"},
            {"date": "2025-09", "event": "HBM3e qualification for NVIDIA B200 Blackwell confirmed", "category": "product", "significance": "high"},
            {"date": "2025-11", "event": "Micron stock +7% single day: structural AI winner designation by analysts", "category": "financial", "significance": "medium"},
            {"date": "2026-03", "event": "FY2026 Q2 earnings: $8.7B (+38% YoY); HBM share approaches 15%", "category": "financial", "significance": "high"},
            {"date": "2026-05", "event": "Analyst: Micron vs SanDisk — Micron named top AI memory buy for 2026 'memory crunch'", "category": "financial", "significance": "medium"}
        ]
    },
    "nvidia": {
        "lead_time": {
            "total_months_to_token": 6,
            "description": "NVIDIA GPU ship-out → tokens served ≈ 6 months. The shortest path among compute vendors because NVIDIA ships to hyperscalers who have pre-built infrastructure. HBM must already be qualified and available at TSMC before GPU ships.",
            "bottleneck": "TSMC CoWoS capacity (GPU die + HBM packaging) — constrained through 2026",
            "pipeline": [
                {"stage": "TSMC CoWoS (GPU die + HBM bonding)", "weeks": 12, "owner": "TSMC"},
                {"stage": "GPU module test & binning", "weeks": 3, "owner": "NVIDIA"},
                {"stage": "Server OEM integration (DGX/HGX build)", "weeks": 4, "owner": "Dell / Supermicro / ODM"},
                {"stage": "Hyperscaler rack deployment & networking", "weeks": 5, "owner": "Microsoft / AWS / Google"},
                {"stage": "Tokens served", "weeks": 0, "owner": "End users"}
            ]
        },
        "key_events": [
            {"date": "2024-03", "event": "H200 SXM5 (141GB HBM3e) first deliveries — 1.8× more HBM than H100", "category": "product", "significance": "high"},
            {"date": "2024-05", "event": "FY2025 Q1 earnings: $22.6B datacenter revenue — 427% YoY growth", "category": "financial", "significance": "high"},
            {"date": "2024-08", "event": "Blackwell B200 / GB200 unveiled — 192GB HBM3e per GPU, 1000W TDP", "category": "product", "significance": "high"},
            {"date": "2024-09", "event": "Blackwell yield issues reported — CoWoS defects delay mass production by ~1 quarter", "category": "risk", "significance": "high"},
            {"date": "2024-11", "event": "Blackwell B200 mass production confirmed — yield issues resolved at TSMC N4", "category": "product", "significance": "high"},
            {"date": "2025-01", "event": "GB200 NVL72 first deliveries to Microsoft, Google, Meta — 72-GPU liquid-cooled rack", "category": "product", "significance": "high"},
            {"date": "2025-03", "event": "FY2025 Q4 earnings: $35.6B datacenter revenue; Blackwell = >50% of DC revenue", "category": "financial", "significance": "high"},
            {"date": "2025-05", "event": "Rubin GPU (HBM4E) roadmap confirmed for 2027 — successor to Blackwell", "category": "product", "significance": "medium"},
            {"date": "2025-07", "event": "GB300 (Blackwell Ultra, HBM4) announced — qualification race for SK Hynix / Micron", "category": "product", "significance": "high"},
            {"date": "2026-02", "event": "FY2026 Q4 earnings: $39.3B total revenue, DC $35.6B — new record", "category": "financial", "significance": "high"},
            {"date": "2026-05", "event": "Q1 FY2027 guidance: ~$78B total revenue — Blackwell Ultra ramp begins", "category": "financial", "significance": "high"}
        ]
    },
    "tsmc": {
        "lead_time": {
            "total_months_to_token": 18,
            "description": "TSMC new capacity decision → tokens served ≈ 18-24 months. Adding CoWoS capacity requires clean room construction (12-18 months), equipment delivery (6-12 months), and yield ramp (3-6 months). Existing capacity turns 3 months.",
            "bottleneck": "EUV scanner delivery from ASML (12-18 month wait) + clean room construction",
            "pipeline": [
                {"stage": "TSMC capacity investment decision", "weeks": 0, "owner": "TSMC board"},
                {"stage": "Clean room construction + equipment install", "weeks": 52, "owner": "TSMC + construction"},
                {"stage": "EUV tool qualification & yield ramp", "weeks": 26, "owner": "TSMC + ASML"},
                {"stage": "GPU die production + CoWoS packaging", "weeks": 12, "owner": "TSMC"},
                {"stage": "GPU → server → DC deploy → tokens", "weeks": 14, "owner": "NVIDIA + hyperscaler"}
            ]
        },
        "key_events": [
            {"date": "2024-01", "event": "CoWoS capacity reaches 35K WPM — doubles from 18K in 2022", "category": "capacity", "significance": "high"},
            {"date": "2024-04", "event": "Arizona N3 fab first silicon production — first TSMC advanced node outside Taiwan", "category": "capacity", "significance": "high"},
            {"date": "2024-07", "event": "CoWoS-L (multi-chip, larger interposer) enters mass production for GB200", "category": "product", "significance": "high"},
            {"date": "2024-10", "event": "Q3 2024 earnings: NT$759.7B (+36% YoY) — AI demand drives record margins", "category": "financial", "significance": "medium"},
            {"date": "2025-01", "event": "CoWoS capacity target raised to 85K WPM for 2025 — 2.4× growth in 3 years", "category": "capacity", "significance": "high"},
            {"date": "2025-04", "event": "N2 (2nm) process enters risk production — world's first 2nm commercial wafer", "category": "product", "significance": "high"},
            {"date": "2025-06", "event": "SoIC-X (3D stacking for HBM4+) co-development confirmed with SK Hynix", "category": "product", "significance": "medium"},
            {"date": "2025-10", "event": "Arizona fab N3 full production — 20K WPM; TSMC US presence becomes real", "category": "capacity", "significance": "high"},
            {"date": "2026-04", "event": "Q1 2026 earnings: NT$839.3B (+41.6% YoY); CoWoS ASP nears 7nm wafer level", "category": "financial", "significance": "high"},
            {"date": "2026-04", "event": "TSMC Technology Symposium: CoWoS capacity to 120K WPM in 2026 — confirms AI demand", "category": "capacity", "significance": "high"},
            {"date": "2026-04", "event": "Indiana (Phoenix) fab CoWoS packaging announcement — US HBM packaging coming", "category": "capacity", "significance": "medium"}
        ]
    },
    "nvidia_skip": {},  # Already handled
    "microsoft": {
        "lead_time": {
            "total_months_to_token": 3,
            "description": "Microsoft GPU receipt → tokens served ≈ 3 months. Fastest path because Azure has pre-built data center space and power. Time is dominated by networking setup and software stack deployment.",
            "bottleneck": "Power availability — new datacenter regions require 12-24 months for grid connection",
            "pipeline": [
                {"stage": "GPU server receipt from NVIDIA/Dell/Supermicro", "weeks": 0, "owner": "Microsoft receiving"},
                {"stage": "Rack assembly, power, cooling (Vertiv)", "weeks": 3, "owner": "Microsoft DC ops"},
                {"stage": "InfiniBand / Ethernet networking setup", "weeks": 2, "owner": "Microsoft network"},
                {"stage": "CUDA/software stack, health checks", "weeks": 3, "owner": "Azure AI team"},
                {"stage": "Capacity allocation (OpenAI / Azure AI)", "weeks": 2, "owner": "Azure capacity"},
                {"stage": "Tokens served via Azure AI / OpenAI API", "weeks": 0, "owner": "End users"}
            ]
        },
        "key_events": [
            {"date": "2024-01", "event": "GPT-4 Turbo deployed on Azure ND H100 — 128K context window, 3× cheaper inference", "category": "product", "significance": "high"},
            {"date": "2024-03", "event": "Microsoft announces $3.3B Wisconsin datacenter investment — AI infrastructure push", "category": "capacity", "significance": "medium"},
            {"date": "2024-05", "event": "Copilot+ PCs announced — edge AI with NPU; signals inference diversification away from cloud", "category": "strategy", "significance": "medium"},
            {"date": "2024-07", "event": "Maia 2 custom AI ASIC deployed in Azure for inference — first hyperscaler ASIC at scale", "category": "product", "significance": "high"},
            {"date": "2024-09", "event": "Three Mile Island nuclear restart (Crane Clean Energy Center) — 835MW to power Azure AI", "category": "capacity", "significance": "high"},
            {"date": "2025-01", "event": "GB200 NVL72 first racks deployed in Azure — 72-GPU Blackwell cluster online", "category": "product", "significance": "high"},
            {"date": "2025-02", "event": "Microsoft FY2025 Q2: Azure +31% CC — AI services now material to growth", "category": "financial", "significance": "medium"},
            {"date": "2025-04", "event": "$80B CapEx commitment for FY2026 announced — largest in Microsoft history", "category": "capacity", "significance": "high"},
            {"date": "2025-07", "event": "Azure HBv4 (8× AMD MI300X, 1.5TB HBM3) generally available — 192GB/GPU inference king", "category": "product", "significance": "medium"},
            {"date": "2026-04", "event": "Q3 FY2026: Azure growth +39% CC; $25B of AI budget attributed to memory/chip cost increase", "category": "financial", "significance": "high"},
            {"date": "2026-04", "event": "Microsoft calls for $190B datacenter spending — largest hyperscaler CapEx pledge", "category": "capacity", "significance": "high"}
        ]
    },
    "google": {
        "lead_time": {
            "total_months_to_token": 4,
            "description": "Google GPU/TPU receipt → tokens served ≈ 4 months. TPU path takes slightly longer because Google builds custom TPU server racks from scratch; GPU path mirrors Azure at ~3 months.",
            "bottleneck": "TPU cluster networking fabric (custom Google Jupiter network) — 4-6 weeks setup",
            "pipeline": [
                {"stage": "TPU die (Broadcom) + HBM (Samsung) → TSMC CoWoS", "weeks": 0, "owner": "TSMC (already done)"},
                {"stage": "TPU module to Google custom server rack", "weeks": 4, "owner": "Google hardware"},
                {"stage": "Jupiter network fabric deployment", "weeks": 5, "owner": "Google network"},
                {"stage": "JAX/XLA software stack and model integration", "weeks": 3, "owner": "Google AI"},
                {"stage": "Gemini / Cloud TPU API serving", "weeks": 4, "owner": "Google Cloud"},
                {"stage": "Tokens served (Gemini API / Cloud)", "weeks": 0, "owner": "End users"}
            ]
        },
        "key_events": [
            {"date": "2024-02", "event": "Gemini Ultra launched on TPU v5 — Google's first frontier model matching GPT-4", "category": "product", "significance": "high"},
            {"date": "2024-04", "event": "TPU v5e (Trillium) generally available on Google Cloud — direct NVIDIA A100 competitor", "category": "product", "significance": "high"},
            {"date": "2024-05", "event": "Google I/O 2024: Gemini 1.5 Pro 1M context — requires massive HBM for inference", "category": "product", "significance": "high"},
            {"date": "2024-10", "event": "Q3 2024 earnings: Google Cloud +35% YoY — AI revenue 'material' for first time", "category": "financial", "significance": "medium"},
            {"date": "2025-01", "event": "Axion Arm CPU generally available on Google Cloud — replaces Intel Xeon in new GCP nodes", "category": "product", "significance": "medium"},
            {"date": "2025-04", "event": "Google announces TPU v6 (Trillium 2) — will sell TPUs to select external customers", "category": "product", "significance": "high"},
            {"date": "2025-05", "event": "Google I/O: Gemini 2.0 Flash/Pro — inference volume 10× vs 2024, massive HBM pull", "category": "product", "significance": "high"},
            {"date": "2025-09", "event": "Kairos Power SMR nuclear agreement — Google commits to 500MW nuclear for AI compute", "category": "capacity", "significance": "high"},
            {"date": "2026-04", "event": "Q1 2026: $35.7B CapEx — Google Cloud +50% YoY; largest capex quarter in Alphabet history", "category": "financial", "significance": "high"},
            {"date": "2026-04", "event": "Google TPU v8 (8th gen) unveiled at Cloud Next — AI inference chips for customers", "category": "product", "significance": "high"}
        ]
    },
    "amazon": {
        "lead_time": {
            "total_months_to_token": 5,
            "description": "Amazon GPU/Trainium receipt → tokens served ≈ 5 months. Trainium2 path takes longer than GPU because AWS builds custom server racks and must integrate with its proprietary Nitro network. GPU path ≈ 3 months.",
            "bottleneck": "AWS Nitro network integration (custom silicon) — adds 4-6 weeks vs off-shelf GPU",
            "pipeline": [
                {"stage": "Trainium2 (Marvell ASIC) from TSMC + HBM bonding", "weeks": 0, "owner": "TSMC CoWoS"},
                {"stage": "AWS custom server rack assembly (Trainium2 + Graviton4 host)", "weeks": 5, "owner": "AWS hardware"},
                {"stage": "Nitro network card integration + EFA fabric", "weeks": 4, "owner": "AWS Annapurna"},
                {"stage": "UltraCluster networking + health sweep", "weeks": 5, "owner": "AWS DC ops"},
                {"stage": "Bedrock / SageMaker model serving", "weeks": 6, "owner": "AWS AI team"},
                {"stage": "Tokens served (Bedrock / Anthropic Claude API)", "weeks": 0, "owner": "End users"}
            ]
        },
        "key_events": [
            {"date": "2024-03", "event": "Trainium2 chip tape-out complete; AWS announces Project Rainier (400K+ Trainium2 for Anthropic)", "category": "product", "significance": "high"},
            {"date": "2024-06", "event": "AWS announces $11B investment in Indiana datacenter — power + physical capacity for Trainium scale", "category": "capacity", "significance": "medium"},
            {"date": "2024-09", "event": "Graviton4 (custom Arm CPU, TSMC N4P) generally available — host CPU in all new Trainium servers", "category": "product", "significance": "medium"},
            {"date": "2024-11", "event": "AWS re:Invent: Trainium2 UltraServer (16× Trainium2) and Trn2 instances launched", "category": "product", "significance": "high"},
            {"date": "2025-02", "event": "Project Rainier online: 400K+ Trainium2 chips, 1 EF/s cluster — Anthropic Claude 3 trains here", "category": "product", "significance": "high"},
            {"date": "2025-05", "event": "Q1 2025 AWS earnings: $29.3B (+17% YoY); AI services now 'largest growth driver'", "category": "financial", "significance": "medium"},
            {"date": "2025-09", "event": "Trainium3 development confirmed (3nm TSMC, HBM4 target) — Marvell next-gen ASIC", "category": "product", "significance": "high"},
            {"date": "2026-01", "event": "CEO Andy Jassy shareholder letter: 'Declaring war on NVIDIA and Intel' — custom silicon priority", "category": "strategy", "significance": "high"},
            {"date": "2026-04", "event": "Q1 2026 CapEx $44.2B — Amazon chips contributed $20B+ in AI infrastructure spend", "category": "financial", "significance": "high"},
            {"date": "2026-04", "event": "Big Tech Q1 2026 total: $630B AI CapEx collectively — AWS + Azure + GCP + Meta combined", "category": "financial", "significance": "high"}
        ]
    },
    "meta": {
        "lead_time": {
            "total_months_to_token": 4,
            "description": "Meta GPU receipt → tokens served ≈ 4 months. Meta builds its own racks (OAM form factor) and does not sell cloud compute, so deployment speed depends on Meta DC ops. Inference (MTIA) goes live faster than training clusters.",
            "bottleneck": "OAM chassis manufacturing and liquid cooling retrofit — custom form factor adds 3-4 weeks vs standard rack",
            "pipeline": [
                {"stage": "NVIDIA H200 / MTIA chip delivery", "weeks": 0, "owner": "Meta receiving"},
                {"stage": "OAM rack chassis assembly (custom Meta design)", "weeks": 4, "owner": "Meta hardware ops"},
                {"stage": "Liquid cooling installation (CDU, Vertiv)", "weeks": 3, "owner": "Meta DC ops"},
                {"stage": "PyTorch / MTIA software stack deployment", "weeks": 3, "owner": "Meta AI Infra"},
                {"stage": "Model training run / Llama fine-tuning / inference routing", "weeks": 6, "owner": "Meta AI Research"},
                {"stage": "Tokens served (Meta AI, Llama API)", "weeks": 0, "owner": "End users"}
            ]
        },
        "key_events": [
            {"date": "2024-01", "event": "Meta commits to buying 350K H100 GPUs — world's largest single purchase; 'Grand Teton' cluster", "category": "capacity", "significance": "high"},
            {"date": "2024-04", "event": "Llama 3 (8B, 70B, 405B) released open-source — trained on Grand Teton H100 cluster", "category": "product", "significance": "high"},
            {"date": "2024-06", "event": "MTIA v2 deployed at scale for Reels/Feed inference — reduces GPU requirement for inference", "category": "product", "significance": "high"},
            {"date": "2024-07", "event": "Meta AI assistant launched globally — inference demand surge, new HBM pull from MTIA + GPU", "category": "product", "significance": "medium"},
            {"date": "2024-10", "event": "Q3 2024 earnings: $15.7B net income; CapEx raised to $37-40B for 2024 full year", "category": "financial", "significance": "medium"},
            {"date": "2025-01", "event": "Meta announces 2GW Louisiana AI datacenter — largest single AI datacenter project announced", "category": "capacity", "significance": "high"},
            {"date": "2025-04", "event": "Llama 4 (Scout, Maverick, Behemoth) released — trained on H200 clusters, largest open-source model", "category": "product", "significance": "high"},
            {"date": "2025-07", "event": "Meta CapEx raised to $64-72B for 2026 — 3× increase in 18 months from 2024 guidance", "category": "capacity", "significance": "high"},
            {"date": "2026-03", "event": "Facebook fires 8,000 employees amid $145B AI investment push — efficiency + AI double-down", "category": "org", "significance": "medium"},
            {"date": "2026-04", "event": "Q1 2026: $42.3B revenue (+16% YoY); CapEx $19.84B — AI infrastructure now 40%+ of total spend", "category": "financial", "significance": "high"}
        ]
    },
    "broadcom": {
        "lead_time": {
            "total_months_to_token": 30,
            "description": "Broadcom ASIC design win → tokens served ≈ 30 months (2.5 years). Custom ASIC has the longest supply chain lead time because it requires 12-18 months of co-design with the hyperscaler before any silicon is produced.",
            "bottleneck": "Co-design cycle (12-18 months) before TSMC tape-out even begins",
            "pipeline": [
                {"stage": "Hyperscaler ASIC requirements definition", "weeks": 12, "owner": "Google / Meta / ByteDance"},
                {"stage": "Broadcom co-design (architecture, SerDes, layout)", "weeks": 40, "owner": "Broadcom engineering"},
                {"stage": "TSMC tape-out + silicon bring-up (N3/N5)", "weeks": 16, "owner": "TSMC + Broadcom"},
                {"stage": "HBM qualification + CoWoS packaging", "weeks": 12, "owner": "TSMC + SK Hynix / Samsung"},
                {"stage": "Hyperscaler ASIC validation + cluster build", "weeks": 12, "owner": "Google / Meta"},
                {"stage": "Tokens served (TPU / MTIA online)", "weeks": 0, "owner": "End users"}
            ]
        },
        "key_events": [
            {"date": "2024-01", "event": "Broadcom reveals it has 3 hyperscaler ASIC customers — Google, Meta + unnamed (ByteDance)", "category": "strategy", "significance": "high"},
            {"date": "2024-03", "event": "Google TPU v5 Trillium confirmed as Broadcom ASIC — co-designed over 4-year cycle", "category": "product", "significance": "high"},
            {"date": "2024-06", "event": "FY2024 AI revenue run rate exceeds $11B annualized — ASIC revenue surpasses networking", "category": "financial", "significance": "high"},
            {"date": "2024-09", "event": "Analyst day: each hyperscaler ASIC customer to deploy 1M+ chips by 2027 — massive HBM pull", "category": "strategy", "significance": "high"},
            {"date": "2025-01", "event": "ByteDance custom AI ASIC confirmed — reportedly Broadcom's largest-ever single ASIC order by volume", "category": "product", "significance": "high"},
            {"date": "2025-04", "event": "Jericho3-AI Ethernet switch ASIC launched — enables 51.2T AI cluster fabric, NVIDIA InfiniBand alternative", "category": "product", "significance": "medium"},
            {"date": "2025-07", "event": "Broadcom retains #1 hyperscaler ASIC partner position through 2027 per Counterpoint Research", "category": "strategy", "significance": "medium"},
            {"date": "2026-03", "event": "FY2025 Q2 earnings: $14.9B (+25% YoY); AI revenue $4.1B/quarter", "category": "financial", "significance": "high"}
        ]
    },
    "marvell": {
        "lead_time": {
            "total_months_to_token": 28,
            "description": "Marvell ASIC design win → tokens served ≈ 28 months. Similar to Broadcom. Trainium2 took ~3 years from initial design to Project Rainier going live.",
            "bottleneck": "AWS software integration (MindSpore-equivalent for Trainium) adds 6 months post-silicon vs CUDA-ready NVIDIA",
            "pipeline": [
                {"stage": "AWS Trainium requirements + Marvell co-design", "weeks": 36, "owner": "AWS + Marvell"},
                {"stage": "TSMC N4 tape-out + silicon bring-up", "weeks": 14, "owner": "TSMC + Marvell"},
                {"stage": "HBM qualification (SK Hynix/Samsung) + CoWoS", "weeks": 12, "owner": "TSMC"},
                {"stage": "AWS Nitro integration + UltraCluster validation", "weeks": 10, "owner": "AWS Annapurna"},
                {"stage": "Neuron SDK + model porting (PyTorch → Trainium)", "weeks": 16, "owner": "AWS AI team"},
                {"stage": "Tokens served (Claude on Project Rainier)", "weeks": 0, "owner": "Anthropic / AWS Bedrock"}
            ]
        },
        "key_events": [
            {"date": "2024-03", "event": "Trainium2 tape-out complete; AWS Project Rainier (400K+ chips) confirmed as largest ever custom cluster", "category": "product", "significance": "high"},
            {"date": "2024-06", "event": "Marvell AI revenue crosses $1B annualized — Trainium2 production ramp begins", "category": "financial", "significance": "high"},
            {"date": "2024-10", "event": "OCTEON 10 DPU (400G) adopted by major US cloud providers for AI workload offload", "category": "product", "significance": "medium"},
            {"date": "2025-01", "event": "Marvell FY2025 Q3: AI revenue $1.1B/quarter — Trainium2 dominant driver", "category": "financial", "significance": "high"},
            {"date": "2025-06", "event": "800G optical PHY (Alaska C) enters mass production — AI inter-rack connectivity leader", "category": "product", "significance": "medium"},
            {"date": "2025-09", "event": "Trainium3 (3nm, HBM4 target) development confirmed with AWS — Marvell's N+1 ASIC", "category": "product", "significance": "high"},
            {"date": "2026-03", "event": "FY2026 Q1: revenue $1.875B (+61% YoY); Marvell AI revenue '10× larger than 2 years ago'", "category": "financial", "significance": "high"}
        ]
    },
    "amd": {
        "lead_time": {
            "total_months_to_token": 8,
            "description": "AMD GPU ship-out → tokens served ≈ 8 months. Longer than NVIDIA because AMD ROCm software stack requires more porting work (less mature than CUDA), adding 2-3 months for model optimization.",
            "bottleneck": "ROCm software stack maturity — vLLM/PyTorch support adds 6-8 weeks vs NVIDIA CUDA",
            "pipeline": [
                {"stage": "TSMC CoWoS (MI300X GPU die + HBM bonding)", "weeks": 12, "owner": "TSMC"},
                {"stage": "AMD GPU test, binning, OAM module assembly", "weeks": 4, "owner": "AMD"},
                {"stage": "Server OEM integration (Dell PowerEdge XE9680)", "weeks": 4, "owner": "Dell / Supermicro"},
                {"stage": "Hyperscaler deployment + ROCm stack setup", "weeks": 6, "owner": "Microsoft / Oracle"},
                {"stage": "Model porting / optimization for ROCm (vs CUDA)", "weeks": 8, "owner": "Customer AI team"},
                {"stage": "Tokens served (Azure HBv4 / Oracle GPU)", "weeks": 0, "owner": "End users"}
            ]
        },
        "key_events": [
            {"date": "2024-01", "event": "MI300X (192GB HBM3, $15K/chip) generally available — highest GPU HBM capacity at launch", "category": "product", "significance": "high"},
            {"date": "2024-03", "event": "Microsoft Azure HBv4 (8× MI300X, 1.5TB HBM3/server) announced — largest AMD AI deployment", "category": "product", "significance": "high"},
            {"date": "2024-06", "event": "AMD datacenter revenue $2.8B — GPU revenue 'inflecting significantly' per Lisa Su", "category": "financial", "significance": "medium"},
            {"date": "2024-09", "event": "MI325X (256GB HBM3e) announced — breaks NVIDIA HBM capacity record per GPU", "category": "product", "significance": "high"},
            {"date": "2025-01", "event": "EPYC Turin (5nm, 192-core) takes #1 datacenter CPU market share from Intel Xeon", "category": "product", "significance": "high"},
            {"date": "2025-04", "event": "MI350 (3nm TSMC, 288GB HBM3e) announced — targets NVIDIA B200 performance", "category": "product", "significance": "high"},
            {"date": "2025-06", "event": "vLLM and PyTorch ROCm support reaches parity with CUDA — AMD inference adoption accelerates", "category": "product", "significance": "medium"},
            {"date": "2026-04", "event": "Q1 2026: datacenter revenue $3.7B; MI400 (HBM4) roadmap confirmed for 2027", "category": "financial", "significance": "high"}
        ]
    },
    "vertiv": {
        "lead_time": {
            "total_months_to_token": 18,
            "description": "Vertiv power/cooling order → tokens served ≈ 18 months. CDU/UPS must be installed before any GPU rack goes live. Liquid cooling retrofit adds 12-16 months of construction before racks can be installed.",
            "bottleneck": "Building construction + electrical permit approval — adds 6-12 months before Vertiv equipment can install",
            "pipeline": [
                {"stage": "Hyperscaler DC construction + electrical rough-in", "weeks": 36, "owner": "DC developer + electricians"},
                {"stage": "Vertiv CDU + UPS delivery and installation", "weeks": 12, "owner": "Vertiv field service"},
                {"stage": "Cooling commissioning + pressure testing", "weeks": 4, "owner": "Vertiv + DC ops"},
                {"stage": "GPU rack installation + power-on", "weeks": 3, "owner": "NVIDIA / ODM"},
                {"stage": "Network, software, model deployment", "weeks": 9, "owner": "Hyperscaler"},
                {"stage": "Tokens served", "weeks": 0, "owner": "End users"}
            ]
        },
        "key_events": [
            {"date": "2024-01", "event": "Vertiv signs NVIDIA GB200 NVL72 certification — only UPS/cooling vendor certified for Blackwell rack", "category": "product", "significance": "high"},
            {"date": "2024-04", "event": "Q1 2024 earnings: order backlog hits record $6B — AI demand overwhelming cooling supply", "category": "financial", "significance": "high"},
            {"date": "2024-07", "event": "48V DC power shelf production begins — required by GB200 NVL72 architecture", "category": "product", "significance": "medium"},
            {"date": "2024-10", "event": "400kW CDU (Coolant Distribution Unit) capacity — enables 100kW+ per rack deployments", "category": "product", "significance": "high"},
            {"date": "2025-01", "event": "Q4 2024 earnings: 83% profit growth; backlog $7.5B; liquid cooling backlog 3× YoY", "category": "financial", "significance": "high"},
            {"date": "2025-04", "event": "Vertiv acquires Strategic Thermal Labs — expands direct liquid cooling IP portfolio", "category": "strategy", "significance": "medium"},
            {"date": "2025-06", "event": "$50M Ohio manufacturing expansion — new liquid cooling production for AI datacenter demand", "category": "capacity", "significance": "medium"},
            {"date": "2026-05", "event": "VRT stock hits record high; analyst: AI power demand creates multi-year structural backlog", "category": "financial", "significance": "high"}
        ]
    },
    "ge_vernova": {
        "lead_time": {
            "total_months_to_token": 36,
            "description": "GE Vernova transformer order → tokens served ≈ 36 months. The longest lead time in the AI supply chain. Transformer (18-36 months) + substation construction (12 months) + grid interconnect approval (6-12 months) must all complete before any server gets power.",
            "bottleneck": "Grid transformer manufacturing — 18-36 month backlog; cannot be fast-tracked without pre-ordering 3 years ahead",
            "pipeline": [
                {"stage": "Hyperscaler orders transformer from GE Vernova", "weeks": 0, "owner": "GE Vernova order"},
                {"stage": "Transformer manufacturing (specialized, long cycle)", "weeks": 72, "owner": "GE Vernova factory"},
                {"stage": "Substation construction + electrical permit", "weeks": 36, "owner": "Utility / developer"},
                {"stage": "Grid interconnection approval (FERC/NERC)", "weeks": 24, "owner": "Regulatory"},
                {"stage": "Server racks powered + network deployed", "weeks": 14, "owner": "Hyperscaler"},
                {"stage": "Tokens served", "weeks": 0, "owner": "End users"}
            ]
        },
        "key_events": [
            {"date": "2024-01", "event": "GE Vernova spin-off from GE completes — standalone company focused on energy transition", "category": "org", "significance": "medium"},
            {"date": "2024-06", "event": "GE Vernova IPO pricing $32B — AI power demand cited as primary growth driver", "category": "financial", "significance": "high"},
            {"date": "2024-09", "event": "Transformer backlog reaches 3+ years — every new AI datacenter faces 18-36 month power constraint", "category": "capacity", "significance": "high"},
            {"date": "2025-01", "event": "Microsoft signs direct HA gas turbine contract — first hyperscaler to build own on-site power generation", "category": "product", "significance": "high"},
            {"date": "2025-04", "event": "GEV stock +65% YTD — recognized as critical AI supply chain node alongside NVIDIA and SK Hynix", "category": "financial", "significance": "medium"},
            {"date": "2025-07", "event": "Google signs HVDC contract for offshore wind-to-datacenter link — GE Vernova provides conversion", "category": "product", "significance": "medium"},
            {"date": "2026-04", "event": "Q1 2026 earnings: GE Vernova lifts 2026 outlook; power equipment demand driven by AI boom", "category": "financial", "significance": "high"}
        ]
    },
    "constellation_energy": {
        "lead_time": {
            "total_months_to_token": 48,
            "description": "Constellation nuclear PPA signing → tokens served ≈ 48 months for new capacity (restart: 24 months). Existing plants can deliver power faster, but new nuclear capacity or restarts require years of regulatory work.",
            "bottleneck": "NRC regulatory approval for restart or new capacity — minimum 18-24 months even for favorable cases",
            "pipeline": [
                {"stage": "PPA negotiation + NRC restart application", "weeks": 24, "owner": "Constellation + regulators"},
                {"stage": "Safety upgrades + equipment refurbishment", "weeks": 52, "owner": "Constellation engineering"},
                {"stage": "NRC inspection + final approval", "weeks": 20, "owner": "NRC"},
                {"stage": "Grid reconnection + capacity testing", "weeks": 8, "owner": "Constellation + utility"},
                {"stage": "Hyperscaler datacenter construction + GPU install", "weeks": 52, "owner": "Microsoft / Google DC"},
                {"stage": "Tokens served (24/7 nuclear-powered AI cluster)", "weeks": 0, "owner": "End users"}
            ]
        },
        "key_events": [
            {"date": "2023-09", "event": "Microsoft signs 20-year PPA for Three Mile Island Unit 1 restart — landmark AI-nuclear deal", "category": "product", "significance": "high"},
            {"date": "2024-03", "event": "NRC approves Three Mile Island Unit 1 restart license amendment", "category": "product", "significance": "high"},
            {"date": "2024-05", "event": "Google signs nuclear PPA with Kairos Power (SMR) — 500MW for AI datacenters by 2030", "category": "product", "significance": "medium"},
            {"date": "2024-09", "event": "Three Mile Island (Crane Clean Energy Center) restarts — first nuclear restart for AI demand globally", "category": "product", "significance": "high"},
            {"date": "2024-11", "event": "Amazon signs nuclear PPA with Constellation for Virginia datacenter corridor", "category": "product", "significance": "high"},
            {"date": "2025-02", "event": "Constellation stock +80% since TMI announcement — recognized as AI infrastructure play", "category": "financial", "significance": "medium"},
            {"date": "2025-06", "event": "Crestwood Illinois nuclear expansion (1.6GW) approved — targeting AI demand through 2035", "category": "capacity", "significance": "high"},
            {"date": "2026-05", "event": "Data centres drive momentum for nuclear — analyst: 'Nuclear capacity shortage constraints AI buildout ahead of HBM'", "category": "strategy", "significance": "high"}
        ]
    },
    "huawei": {
        "lead_time": {
            "total_months_to_token": 16,
            "description": "Huawei Ascend chip → tokens served ≈ 16 months inside China. Longer than NVIDIA because SMIC N+2 yield is lower (more scrapped wafers = longer to fill order), CXMT HBM supply is constrained, and MindSpore software stack requires more porting.",
            "bottleneck": "SMIC N+2 yield rate (~60% vs TSMC N5 ~80%) — doubles effective lead time for same volume",
            "pipeline": [
                {"stage": "SMIC N+2 wafer production (Ascend die)", "weeks": 14, "owner": "SMIC"},
                {"stage": "CXMT HBM-equivalent stack production", "weeks": 12, "owner": "CXMT"},
                {"stage": "Ascend 910C chip packaging (domestic)", "weeks": 8, "owner": "Amkor / JCET China"},
                {"stage": "Atlas 800T A2 server assembly + test", "weeks": 6, "owner": "Huawei hardware"},
                {"stage": "MindSpore model porting + cluster deployment", "weeks": 12, "owner": "ByteDance / Baidu / Alibaba"},
                {"stage": "Tokens served (Chinese AI services)", "weeks": 0, "owner": "End users (China)"}
            ]
        },
        "key_events": [
            {"date": "2024-01", "event": "Ascend 910B production ramp — primary AI GPU for Chinese hyperscalers following NVIDIA export controls", "category": "product", "significance": "high"},
            {"date": "2024-05", "event": "US expands export controls — H100/A100 banned to China; Huawei Ascend demand surges 3×", "category": "risk", "significance": "high"},
            {"date": "2024-07", "event": "Huawei CloudMatrix 384 unveiled — 384-Ascend cluster, claims outperform H100 NVL cluster on inference", "category": "product", "significance": "high"},
            {"date": "2024-10", "event": "Huawei AI chip revenue projected $12B for 2025 — domestic demand absorbs full capacity", "category": "financial", "significance": "high"},
            {"date": "2025-02", "event": "Ascend 910C revealed via teardown — SMIC N+2 confirmed; approaching H100 on transformer benchmarks", "category": "product", "significance": "high"},
            {"date": "2025-05", "event": "US deploys AI on classified networks; China doubles down on domestic AI stack (Ascend + MindSpore)", "category": "strategy", "significance": "medium"},
            {"date": "2026-05", "event": "Huawei braces for $12B AI chip revenue — Chinese fabs 'barely keeping up' with Ascend demand", "category": "financial", "significance": "high"}
        ]
    },
    "cxmt": {
        "lead_time": {
            "total_months_to_token": 20,
            "description": "CXMT HBM-equivalent → tokens served ≈ 20 months inside China. Longer than SK Hynix because CXMT yield is lower, production volume is constrained, and the HBM spec is 1-2 generations behind, so more stacks are needed per GPU.",
            "bottleneck": "DUV multi-patterning yield (~50-60% vs SK Hynix EUV ~75%) — every 10% yield improvement reduces effective lead time by 2 months",
            "pipeline": [
                {"stage": "ASML DUV wafer production (CXMT)", "weeks": 14, "owner": "CXMT"},
                {"stage": "HBM-equivalent stack assembly (domestic packaging)", "weeks": 10, "owner": "CXMT + Amkor China"},
                {"stage": "Huawei Ascend NPU + HBM bonding (domestic CoWoS-like)", "weeks": 10, "owner": "CXMT / Huawei packaging"},
                {"stage": "Atlas 800T A2 server assembly", "weeks": 6, "owner": "Huawei hardware"},
                {"stage": "MindSpore cluster deployment", "weeks": 8, "owner": "Chinese hyperscaler"},
                {"stage": "Tokens served", "weeks": 0, "owner": "End users (China)"}
            ]
        },
        "key_events": [
            {"date": "2024-01", "event": "CXMT DDR5 enters mass production — commercial product funds HBM R&D", "category": "product", "significance": "medium"},
            {"date": "2024-04", "event": "CXMT HBM2E-equivalent development program confirmed via supply chain reports", "category": "product", "significance": "high"},
            {"date": "2024-06", "event": "Qualcomm partners with CXMT for smartphone DRAM — signals CXMT quality improving", "category": "product", "significance": "medium"},
            {"date": "2024-10", "event": "Former Samsung researcher jailed for leaking chip technology to CXMT — talent acquisition strategy exposed", "category": "risk", "significance": "high"},
            {"date": "2025-03", "event": "CXMT HBM3 development timeline slips — mass production unlikely in 2026 per Digitimes", "category": "risk", "significance": "high"},
            {"date": "2025-07", "event": "CXMT state funding round: additional CNY 50B — government commits to self-sufficient HBM by 2027", "category": "capacity", "significance": "high"},
            {"date": "2026-04", "event": "CXMT HBM2E sampling reportedly delivered to Huawei — validation testing begins", "category": "product", "significance": "high"}
        ]
    },
    "smic": {
        "lead_time": {
            "total_months_to_token": 18,
            "description": "SMIC N+2 wafer-out → tokens served ≈ 18 months inside China. Yield at N+2 is ~60-65% vs TSMC's 80%+ on comparable nodes, meaning effectively 20-30% more wafer time is needed to fill the same chip order.",
            "bottleneck": "DUV multi-patterning yield at N+2 node — physically limited by 193nm wavelength without EUV",
            "pipeline": [
                {"stage": "SMIC N+2 wafer production (Ascend / CXMT dies)", "weeks": 14, "owner": "SMIC"},
                {"stage": "Wafer test + die sort (lower yield = more time)", "weeks": 4, "owner": "SMIC"},
                {"stage": "Packaging (Amkor China / JCET — domestic)", "weeks": 8, "owner": "Amkor / JCET"},
                {"stage": "Chip delivery to Huawei / CXMT", "weeks": 2, "owner": "Logistics"},
                {"stage": "Server assembly + cluster build", "weeks": 10, "owner": "Huawei"},
                {"stage": "Tokens served (Chinese AI)", "weeks": 0, "owner": "End users"}
            ]
        },
        "key_events": [
            {"date": "2024-01", "event": "SMIC N+2 yield reported at 60-65% — double-patterning DUV achieves 7nm-class at scale", "category": "product", "significance": "high"},
            {"date": "2024-03", "event": "Huawei Mate 60 Pro (Kirin 9000S, SMIC N+2) teardown confirms advanced node capability", "category": "product", "significance": "high"},
            {"date": "2024-06", "event": "SMIC 28nm expansion: 35K WPM capacity for automotive/IoT — mature node funds advanced R&D", "category": "capacity", "significance": "medium"},
            {"date": "2024-09", "event": "US BIS rule: no new ASML DUV tools to SMIC — equipment access frozen at 2024 baseline", "category": "risk", "significance": "high"},
            {"date": "2025-04", "event": "SMIC returns to advanced packaging — scales team for AI chip CoWoS-like capability (domestic)", "category": "product", "significance": "high"},
            {"date": "2025-07", "event": "SMIC N+3 (5nm-class DUV) development attempts begin — technically very challenging without EUV", "category": "product", "significance": "medium"},
            {"date": "2026-05", "event": "SMIC Q1 2026: $2.24B revenue (+28% YoY); advanced node utilization near 100%", "category": "financial", "significance": "high"}
        ]
    }
}

# Remove placeholder key
del TIMELINE_DATA["nvidia_skip"]

# Reuse nvidia data
TIMELINE_DATA["nvidia"] = {
    "lead_time": {
        "total_months_to_token": 6,
        "description": "NVIDIA GPU ship-out → tokens served ≈ 6 months. HBM must be qualified and ready at TSMC before GPU ships; the actual GPU→server→DC pipeline runs fast because hyperscalers have pre-built infrastructure.",
        "bottleneck": "TSMC CoWoS capacity — GPU production is gated by CoWoS slot availability, not GPU design speed",
        "pipeline": [
            {"stage": "TSMC CoWoS (GPU die + HBM bonding)", "weeks": 12, "owner": "TSMC"},
            {"stage": "GPU module test & binning", "weeks": 3, "owner": "NVIDIA"},
            {"stage": "Server OEM integration (DGX/HGX build)", "weeks": 4, "owner": "Dell / Supermicro / ODM"},
            {"stage": "Hyperscaler rack deployment & networking", "weeks": 5, "owner": "Microsoft / AWS / Google"},
            {"stage": "Tokens served", "weeks": 0, "owner": "End users"}
        ]
    },
    "key_events": [
        {"date": "2024-03", "event": "H200 SXM5 (141GB HBM3e) first deliveries — 1.8× more HBM than H100", "category": "product", "significance": "high"},
        {"date": "2024-05", "event": "FY2025 Q1 earnings: $22.6B datacenter revenue — 427% YoY growth", "category": "financial", "significance": "high"},
        {"date": "2024-08", "event": "Blackwell B200 / GB200 unveiled — 192GB HBM3e per GPU, 1000W TDP", "category": "product", "significance": "high"},
        {"date": "2024-09", "event": "Blackwell yield issues reported — CoWoS defects delay mass production by ~1 quarter", "category": "risk", "significance": "high"},
        {"date": "2024-11", "event": "Blackwell B200 mass production confirmed — yield issues resolved at TSMC N4", "category": "product", "significance": "high"},
        {"date": "2025-01", "event": "GB200 NVL72 first deliveries to Microsoft, Google, Meta — 72-GPU liquid-cooled rack", "category": "product", "significance": "high"},
        {"date": "2025-03", "event": "FY2025 Q4 earnings: $35.6B datacenter revenue; Blackwell = >50% of DC revenue", "category": "financial", "significance": "high"},
        {"date": "2025-05", "event": "Rubin GPU (HBM4E) roadmap confirmed for 2027 — successor to Blackwell", "category": "product", "significance": "medium"},
        {"date": "2025-07", "event": "GB300 (Blackwell Ultra, HBM4) announced — qualification race for SK Hynix vs Micron", "category": "product", "significance": "high"},
        {"date": "2026-02", "event": "FY2026 Q4 earnings: $39.3B total revenue, DC $35.6B — new record", "category": "financial", "significance": "high"},
        {"date": "2026-05", "event": "Q1 FY2027 guidance: ~$78B total revenue — Blackwell Ultra ramp begins", "category": "financial", "significance": "high"}
    ]
}


def main():
    for company_id, data in TIMELINE_DATA.items():
        path = DATA_DIR / f"{company_id}.json"
        if not path.exists():
            print(f"[timeline] SKIP {company_id} — file not found")
            continue
        profile = json.loads(path.read_text())
        profile["lead_time"] = data["lead_time"]
        profile["key_events"] = data["key_events"]
        path.write_text(json.dumps(profile, ensure_ascii=False, indent=2))
        n_ev = len(data["key_events"])
        n_pl = len(data["lead_time"]["pipeline"])
        print(f"[timeline] {company_id}: {n_ev} events, {n_pl}-stage pipeline, {data['lead_time']['total_months_to_token']}mo to token")
    print("[timeline] done")


if __name__ == "__main__":
    main()
