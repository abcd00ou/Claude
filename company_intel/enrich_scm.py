"""
One-time enrichment: adds scm_engagement block to every company JSON.
Run: python3 enrich_scm.py
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data" / "companies"

SCM_DATA = {
    "sk_hynix": {
        "scm_role": "World's #1 HBM supplier. Manufactures the high-bandwidth memory stacks that are bonded directly onto NVIDIA/AMD AI GPU dies via TSMC CoWoS packaging. Without SK Hynix HBM, NVIDIA cannot ship H200 or B200 GPUs.",
        "server_products": [
            {
                "name": "HBM3e 24GB Stack (8-Hi)",
                "type": "Memory stack",
                "used_in": "NVIDIA H200 SXM5, AMD MI325X",
                "bandwidth": "1.23 TB/s per stack",
                "note": "12 stacks per H200 GPU (141GB total). SK Hynix supplies ~52% of all HBM to NVIDIA."
            },
            {
                "name": "HBM3e 24GB Stack (12-Hi)",
                "type": "Memory stack",
                "used_in": "NVIDIA B200, GB200 NVL72",
                "bandwidth": "1.23 TB/s per stack",
                "note": "16 stacks per B200 GPU (192GB total). GB200 NVL72 rack = 72 GPUs = 13.8TB HBM."
            },
            {
                "name": "HBM4 32GB Stack (target)",
                "type": "Next-gen memory stack",
                "used_in": "NVIDIA GB300 Blackwell Ultra (target)",
                "bandwidth": "2.0 TB/s per stack (target)",
                "note": "Mass production expected H2 2026. Qualification race with Micron."
            },
            {
                "name": "DDR5 Server DRAM",
                "type": "CPU memory module",
                "used_in": "AI server CPU DRAM slots (Intel Xeon, AMD EPYC hosts)",
                "bandwidth": "~89 GB/s per module",
                "note": "All AI servers need host DRAM for OS, data pipelines, model orchestration."
            }
        ],
        "upstream_from": ["ASML (EUV lithography)", "Tokyo Electron (deposition equipment)", "Silicon wafer suppliers (Shin-Etsu)"],
        "downstream_to": ["TSMC (CoWoS packaging of HBM+GPU)", "NVIDIA", "AMD", "Google (TPU)", "Amazon (Trainium direct)"],
        "scm_position": "Memory tier — bonded onto GPU die at TSMC CoWoS"
    },
    "samsung_semiconductor": {
        "scm_role": "HBM supplier (#2 globally) and the only company supplying both HBM (for AI GPUs) and DDR5/LPDDR5 DRAM (for AI server hosts). Also supplies HBM directly to Google TPU and Amazon Trainium custom silicon, bypassing NVIDIA.",
        "server_products": [
            {
                "name": "HBM3e 24GB Stack",
                "type": "Memory stack",
                "used_in": "AMD MI300X (primary), Google TPU v5",
                "bandwidth": "1.23 TB/s per stack",
                "note": "NVIDIA HBM3e qualification still pending Q1 2026. AMD MI300X uses 8 stacks (192GB)."
            },
            {
                "name": "DDR5-6400 RDIMM (64GB/128GB)",
                "type": "CPU memory module",
                "used_in": "Intel Xeon and AMD EPYC host CPU slots in all AI servers",
                "bandwidth": "~100 GB/s per channel",
                "note": "Every AI server has 12-24 DDR5 DIMMs in the CPU host. Samsung is #1 DDR5 supplier."
            },
            {
                "name": "CXL Memory Expander",
                "type": "Memory expansion",
                "used_in": "Next-gen AI inference servers (CXL 2.0)",
                "bandwidth": "PCIe Gen5 ~64 GB/s",
                "note": "CXL memory pooling for LLM inference; reduces per-server HBM requirement."
            },
            {
                "name": "UFS 4.0 / eMMC",
                "type": "Storage",
                "used_in": "Edge AI devices, smartphones with on-device AI",
                "bandwidth": "—",
                "note": "Samsung's NAND/UFS also feeds the edge AI tier."
            }
        ],
        "upstream_from": ["ASML (EUV, DUV)", "Applied Materials", "Lam Research", "Silicon wafers (ShinEtsu, Sumco)"],
        "downstream_to": ["TSMC (HBM packaging)", "AMD", "Google", "Amazon Trainium (direct)", "OEM server makers (Dell, HPE, Supermicro)"],
        "scm_position": "Memory tier — HBM on GPU die + DDR5 in server host slots"
    },
    "micron": {
        "scm_role": "Only US-headquartered HBM supplier. Fastest growing HBM share (10% → 15%). Supplies HBM3e to NVIDIA H200 (partial allocation) and is in qualification race for Blackwell Ultra HBM4. Also the largest US DRAM supplier for server host memory.",
        "server_products": [
            {
                "name": "HBM3e 24GB Stack",
                "type": "Memory stack",
                "used_in": "NVIDIA H200 (partial), Microsoft Azure AI servers",
                "bandwidth": "1.23 TB/s per stack",
                "note": "Qualified for NVIDIA H200 in 2024. Growing from ~10% to 15%+ share of total HBM."
            },
            {
                "name": "DDR5-6400 RDIMM",
                "type": "CPU memory module",
                "used_in": "Intel Xeon / AMD EPYC host slots in AI servers",
                "bandwidth": "~100 GB/s per channel",
                "note": "Micron is #1 DRAM supplier in North America; strong in US hyperscaler supply chains."
            },
            {
                "name": "LPCAMM2 (Compression-Attached Memory Module)",
                "type": "Low-power server/edge DRAM",
                "used_in": "Next-gen AI laptops, edge inference servers",
                "bandwidth": "LPDDR5X speeds",
                "note": "New form factor; first to production. Apple M4 MacBook Pro uses Micron LPCAMM2."
            },
            {
                "name": "232-layer NAND (QLC/TLC)",
                "type": "Storage",
                "used_in": "AI server NVMe SSDs (training dataset storage)",
                "bandwidth": "7+ GB/s sequential read",
                "note": "AI training clusters need petabytes of fast storage. Micron's 232L NAND is industry-leading density."
            }
        ],
        "upstream_from": ["ASML (EUV, DUV)", "Applied Materials", "US CHIPS Act DOE funding ($6.1B)", "Boise/Idaho fabs (domestic)"],
        "downstream_to": ["TSMC (HBM packaging)", "NVIDIA", "Microsoft Azure (direct HBM allocation)", "OEM server makers"],
        "scm_position": "Memory tier — HBM on GPU die + DRAM/NAND in AI server host"
    },
    "nvidia": {
        "scm_role": "Designs the AI GPUs that are the primary compute engine in every major AI training server. NVIDIA is the central node of the entire AI supply chain: it dictates which HBM supplier qualifies, which foundry (TSMC) packages the chips, and which server OEM integrates the systems.",
        "server_products": [
            {
                "name": "H100 SXM5 GPU",
                "type": "AI training GPU (SXM form factor)",
                "used_in": "DGX H100, HGX H100 (8-GPU server board), cloud GPU instances",
                "hbm": "80GB HBM3 (SK Hynix), 6 stacks",
                "note": "~$30K/chip street price at peak. Still the most deployed AI training GPU in 2025."
            },
            {
                "name": "H200 SXM5 GPU",
                "type": "AI training GPU (SXM form factor)",
                "used_in": "DGX H200, HGX H200, Azure ND H200 v5, AWS P5e",
                "hbm": "141GB HBM3e (SK Hynix primary, Micron partial), 8 stacks",
                "note": "141GB is 1.8x more HBM than H100. Memory bandwidth 4.8 TB/s."
            },
            {
                "name": "B200 SXM GPU",
                "type": "AI training/inference GPU (Blackwell)",
                "used_in": "GB200 NVL72 rack unit, DGX B200",
                "hbm": "192GB HBM3e (SK Hynix), 8 stacks × 24GB",
                "note": "Performance: 20 petaFLOPS FP4. TDP 1000W. Requires liquid cooling."
            },
            {
                "name": "GB200 NVL72 Rack Unit",
                "type": "AI supercomputer rack (72 GPUs)",
                "used_in": "Hyperscaler AI training clusters (Microsoft, Google, Meta, Amazon)",
                "hbm": "13.8TB HBM3e total per rack (72 × 192GB)",
                "note": "72 B200 GPUs + 36 Grace CPUs in one 19-inch rack. Requires Vertiv/Schneider liquid cooling."
            },
            {
                "name": "NVSwitch 4.0",
                "type": "GPU interconnect switch",
                "used_in": "Inside DGX/HGX servers, NVL72 rack backplane",
                "bandwidth": "3.2 TB/s per switch, NVLink 4.0",
                "note": "Connects all 72 B200 GPUs inside GB200 NVL72 at full bandwidth. TSMC N4 process."
            },
            {
                "name": "ConnectX-7 / BlueField-3 (Mellanox)",
                "type": "InfiniBand / Ethernet NIC + DPU",
                "used_in": "AI server cluster networking (all NVIDIA-based AI clusters)",
                "bandwidth": "400Gb/s HDR InfiniBand",
                "note": "InfiniBand connects servers in a training cluster. BlueField-3 handles offloaded networking."
            }
        ],
        "upstream_from": ["SK Hynix (HBM)", "Micron (HBM partial)", "TSMC (GPU die + CoWoS packaging)", "Synopsys/Cadence (EDA)", "ASML (via TSMC)"],
        "downstream_to": ["Microsoft Azure", "Google Cloud", "Amazon AWS", "Meta", "Dell EMC (DGX/HGX OEM)", "Supermicro", "HPE"],
        "scm_position": "GPU tier — central integrator of HBM + GPU die at TSMC; sold to hyperscalers and server OEMs"
    },
    "tsmc": {
        "scm_role": "Manufactures all advanced AI GPU/ASIC dies AND performs CoWoS advanced packaging (bonding HBM stacks to GPU dies). TSMC is the only supplier capable of both steps at volume, making it the single most critical chokepoint in the AI hardware supply chain.",
        "server_products": [
            {
                "name": "CoWoS-S (GPU + HBM interposer)",
                "type": "Advanced packaging (wafer-on-substrate)",
                "used_in": "NVIDIA H100/H200/B200, AMD MI300X/MI325X, Google TPU v5",
                "note": "Bonds GPU die + HBM stacks on a silicon interposer. 50K+ WPM capacity in 2025. 18-month lead time."
            },
            {
                "name": "CoWoS-L (multi-die, large interposer)",
                "type": "Advanced packaging (multi-chiplet)",
                "used_in": "NVIDIA GB200 (Grace CPU + Blackwell GPU + NVLink chiplets)",
                "note": "Larger interposer for multi-chip modules. Required for Grace Blackwell Superchip (GB200)."
            },
            {
                "name": "N3E/N3P Die (3nm GPU wafer)",
                "type": "Foundry wafer production",
                "used_in": "NVIDIA Blackwell GPU die, Apple M4",
                "note": "NVIDIA Blackwell uses TSMC N4 for compute die, N3 for components. Highest-demand node in 2025-2026."
            },
            {
                "name": "N4P Die (4nm GPU wafer)",
                "type": "Foundry wafer production",
                "used_in": "NVIDIA Hopper (H100/H200), AMD MI300X",
                "note": "Most H100/H200 GPU dies produced on N4P. ~$17K per wafer for N4."
            },
            {
                "name": "SoIC-X (3D stacking, next-gen)",
                "type": "3D IC integration",
                "used_in": "HBM4+ integration (2026-2027)",
                "note": "Enables direct die-to-die bonding of HBM4 on logic. Co-developed with SK Hynix."
            }
        ],
        "upstream_from": ["ASML (EUV scanners — only supplier)", "Applied Materials (deposition)", "Lam Research (etch)", "SK Hynix/Samsung/Micron (HBM for CoWoS)"],
        "downstream_to": ["NVIDIA (GPU dies + CoWoS packaging)", "AMD (GPU dies + CoWoS)", "Apple (M-series)", "Broadcom (ASIC dies)", "Marvell (ASIC dies)", "Google (TPU dies)"],
        "scm_position": "Foundry + packaging tier — manufactures GPU dies AND bonds HBM to GPU (CoWoS)"
    },
    "microsoft": {
        "scm_role": "Largest AI compute buyer globally. Procures GPU servers (NVIDIA H200/B200) for Azure AI, deploys them as cloud services, and also designs custom AI ASICs (Maia 2) for inference. Consumes HBM indirectly via NVIDIA and directly via Maia chip procurement.",
        "server_products": [
            {
                "name": "Azure ND H100 v5 (8× H100 SXM)",
                "type": "AI training VM / bare-metal server",
                "used_in": "Azure AI compute; OpenAI GPT training",
                "hbm": "640GB HBM3 per server (8 × 80GB)",
                "note": "Microsoft is NVIDIA's largest single customer for H100. GPT-4 trained on Azure ND H100."
            },
            {
                "name": "Azure ND H200 v5 (8× H200 SXM)",
                "type": "AI training VM",
                "used_in": "Azure AI; OpenAI GPT-4o/5 training",
                "hbm": "1.13TB HBM3e per server (8 × 141GB)",
                "note": "Deployed in 2025. 40% more memory than H100 server; critical for larger model context."
            },
            {
                "name": "Azure GB200 NVL72 cluster",
                "type": "AI supercomputing rack",
                "used_in": "Azure Maia + NVIDIA Blackwell deployments",
                "hbm": "13.8TB HBM3e per rack",
                "note": "Deployed for OpenAI Orion/GPT-5 training. Requires Vertiv liquid cooling."
            },
            {
                "name": "Maia 2 (custom AI ASIC)",
                "type": "AI inference accelerator",
                "used_in": "Azure internal inference (Bing, Copilot, Office 365 AI)",
                "hbm": "HBM (supplier TBD, likely SK Hynix or Micron via Broadcom ASIC)",
                "note": "Replaces GPU for ~30% of inference workloads. Lowers per-token cost for Copilot."
            },
            {
                "name": "Azure HBv4 (8× AMD MI300X)",
                "type": "AI inference VM",
                "used_in": "Azure AI inference; large context models",
                "hbm": "1.5TB HBM3 per server (8 × 192GB)",
                "note": "MI300X's 192GB HBM makes it the best for inference on 70B+ parameter models."
            }
        ],
        "upstream_from": ["NVIDIA (H100/H200/B200 GPUs)", "AMD (MI300X GPUs)", "Broadcom (Maia 2 ASIC)", "TSMC (via chip vendors)", "Vertiv/Schneider (power/cooling)", "Constellation Energy (nuclear PPA)"],
        "downstream_to": ["Enterprise customers (Azure AI services)", "OpenAI (dedicated compute)", "Developers (Azure ML, AI Studio)"],
        "scm_position": "Demand tier — largest HBM consumer (via NVIDIA GPU procurement)"
    },
    "google": {
        "scm_role": "Unique dual-path AI compute buyer: purchases NVIDIA GPUs for Google Cloud AND designs its own TPU ASICs (manufactured by Broadcom/TSMC), which use HBM directly without NVIDIA intermediary. Google is both a major HBM demand source and a direct Samsung/SK Hynix customer.",
        "server_products": [
            {
                "name": "TPU v5 (Trillium) Pod",
                "type": "Custom AI training/inference accelerator",
                "used_in": "Google internal AI (Gemini Ultra training), Google Cloud TPU v5e",
                "hbm": "HBM3 (Samsung primary), 16GB–32GB per chip",
                "note": "Broadcom ASIC + Samsung HBM + TSMC CoWoS. Google's TPU bypasses NVIDIA completely."
            },
            {
                "name": "TPU v6 (Trillium 2)",
                "type": "Next-gen AI accelerator",
                "used_in": "Gemini 2.0/2.5 training, Google Cloud",
                "hbm": "HBM4 (target, supplier TBD)",
                "note": "Announced 2025. Google announced selling TPUs to select external customers."
            },
            {
                "name": "Google Cloud A3 Ultra (8× H200)",
                "type": "GPU cloud instance",
                "used_in": "Google Cloud AI compute for external customers",
                "hbm": "1.13TB HBM3e per server",
                "note": "Google resells NVIDIA GPU compute via A3/A3 Ultra instances."
            },
            {
                "name": "Axion CPU (custom Arm server CPU)",
                "type": "Custom server CPU",
                "used_in": "Google Cloud general compute, AI inference host",
                "note": "Google's own Arm-based server CPU (TSMC N5). Replaces Intel Xeon in some Google datacenters."
            }
        ],
        "upstream_from": ["Broadcom (TPU ASIC design/fab)", "TSMC (TPU die + CoWoS)", "Samsung (HBM for TPU)", "SK Hynix (HBM for Cloud GPU)", "NVIDIA (A3 GPU instances)"],
        "downstream_to": ["Google Cloud customers", "Internal AI teams (DeepMind, Google Brain)", "Enterprise (Workspace AI, Gemini API)"],
        "scm_position": "Demand tier — dual-path: TPU (direct Samsung HBM) + GPU cloud (via NVIDIA)"
    },
    "amazon": {
        "scm_role": "Largest cloud infrastructure provider. Procures NVIDIA GPUs for AWS GPU cloud AND operates the most advanced hyperscaler custom silicon program (Trainium for training, Inferentia for inference), both sourcing HBM directly. Project Rainier is the largest-ever single custom silicon cluster.",
        "server_products": [
            {
                "name": "AWS P5 / P5e Instance (8× H100/H200 SXM)",
                "type": "GPU cloud instance",
                "used_in": "AWS AI training (Anthropic Claude, third-party AI)",
                "hbm": "640GB (P5) / 1.13TB (P5e) per server",
                "note": "AWS resells NVIDIA GPU compute. Used by Anthropic, Stability AI, Cohere."
            },
            {
                "name": "Trainium2 Chip (custom AI training ASIC)",
                "type": "Custom AI training accelerator",
                "used_in": "Project Rainier (Anthropic Claude training), AWS UltraServer",
                "hbm": "HBM3 (SK Hynix / Samsung direct), 96GB per chip",
                "note": "Marvell ASIC design, TSMC N4 fab, SK Hynix/Samsung HBM. 400K+ chips in Project Rainier cluster."
            },
            {
                "name": "Inferentia3 Chip (custom AI inference ASIC)",
                "type": "Custom AI inference accelerator",
                "used_in": "AWS internal inference (Alexa, AWS Bedrock), Inf2 instances",
                "hbm": "HBM (Samsung, lower bandwidth config)",
                "note": "Handles ~40% of AWS inference workloads. 4× better price-performance than GPU for inference."
            },
            {
                "name": "Graviton4 (custom Arm server CPU)",
                "type": "Custom Arm server CPU",
                "used_in": "AWS general compute, AI inference host",
                "note": "TSMC N4P. Accompanies Trainium/Inferentia in AI server racks as the host CPU."
            },
            {
                "name": "Nitro System (custom network + security chip)",
                "type": "Data center offload chip",
                "used_in": "All AWS EC2 instances including AI GPU instances",
                "note": "Offloads networking/storage/security from host CPU. Required in all AWS AI servers."
            }
        ],
        "upstream_from": ["Marvell (Trainium2 ASIC design)", "TSMC (all custom chip fabrication)", "SK Hynix/Samsung (HBM for Trainium)", "NVIDIA (GPU instances)", "Vertiv (power/cooling)", "Constellation/GE Vernova (power)"],
        "downstream_to": ["AWS cloud customers", "Anthropic (dedicated Rainier cluster)", "Enterprise (Bedrock AI services)", "Third-party AI startups"],
        "scm_position": "Demand tier — dual-path GPU cloud (NVIDIA HBM) + custom silicon (direct HBM from SKH/Samsung)"
    },
    "meta": {
        "scm_role": "Largest non-cloud-provider AI compute buyer. Builds and operates its own AI training clusters (not selling cloud services), making HBM procurement a direct cost with no revenue offset. Drives AI chip demand through open-source Llama model releases, which indirectly multiplies HBM demand across thousands of Llama fine-tuners.",
        "server_products": [
            {
                "name": "Grand Teton AI Training Server (H100 OAM)",
                "type": "Custom AI training server (Open Rack 3.0)",
                "used_in": "Meta's 350K-GPU H100 cluster; Llama 3/4 training",
                "hbm": "640GB HBM3 per server (8× H100 80GB)",
                "note": "Meta designed custom OAM (Open Accelerator Module) form factor. 350K H100 cluster is world's largest single-tenant cluster."
            },
            {
                "name": "Grand Teton v2 (H200 OAM)",
                "type": "Custom AI training server",
                "used_in": "Llama 4 / next-gen model training",
                "hbm": "1.13TB HBM3e per server",
                "note": "Upgrade of Grand Teton with H200. Meta buying large H200 allocations from NVIDIA in 2025."
            },
            {
                "name": "MTIA v2 (Meta Training & Inference Accelerator)",
                "type": "Custom AI inference ASIC",
                "used_in": "Reels/Feed ranking inference, content recommendation (3B+ daily users)",
                "hbm": "HBM3 (direct, Broadcom ASIC + TSMC fab)",
                "note": "Handles prediction/ranking inference without NVIDIA. Deployed at scale in Meta datacenters."
            },
            {
                "name": "RSC (Research SuperCluster) — Llama training",
                "type": "AI supercomputer cluster",
                "used_in": "Foundation model pre-training (Llama 3 70B, 405B)",
                "hbm": "~28TB HBM3 total (35K H100 GPUs × 80GB)",
                "note": "Meta RSC = 35K H100 + 4 Exaflop/s compute. One of the largest AI training systems globally."
            }
        ],
        "upstream_from": ["NVIDIA (H100/H200 GPUs)", "Broadcom (MTIA v2 ASIC)", "TSMC (via NVIDIA + Broadcom)", "SK Hynix (HBM via NVIDIA)", "Vertiv (liquid cooling for H100/H200 racks)"],
        "downstream_to": ["Meta internal AI (Instagram, Facebook, WhatsApp AI)", "Open-source community (Llama models)", "Meta AI assistant (external product)"],
        "scm_position": "Demand tier — direct HBM consumer via NVIDIA GPU purchases + MTIA direct path"
    },
    "broadcom": {
        "scm_role": "Designs the custom AI ASIC dies that hyperscalers use instead of NVIDIA GPUs (Google TPU, Meta MTIA, ByteDance custom chip). Also makes the high-speed SerDes (signal integrity IP) and Ethernet/InfiniBand switch ASICs that connect AI servers in a cluster. Broadcom is the 'behind-the-scenes' chip designer for the entire AI ASIC economy.",
        "server_products": [
            {
                "name": "Google TPU v5 Trillium ASIC die",
                "type": "AI accelerator ASIC (custom for Google)",
                "used_in": "Google TPU pods, Google Cloud TPU v5e instances",
                "hbm": "Samsung HBM3 (bonded at TSMC CoWoS)",
                "note": "Broadcom designs the compute die; TSMC fabricates; Samsung supplies HBM; TSMC packages all together."
            },
            {
                "name": "Meta MTIA v2 ASIC die",
                "type": "AI inference ASIC (custom for Meta)",
                "used_in": "Meta Reels/Feed/Ads inference at global scale",
                "hbm": "HBM3 (direct procurement, supplier TBD)",
                "note": "Deployed across Meta's inference fleet. Reduces GPU purchase from NVIDIA by ~30% for inference."
            },
            {
                "name": "Jericho3-AI Ethernet Switch ASIC",
                "type": "AI cluster networking switch chip",
                "used_in": "AI datacenter spine-leaf switches (Arista, Cisco)",
                "bandwidth": "51.2 Tbps per chip",
                "note": "AI clusters need ultra-low-latency switching. Jericho3-AI is purpose-built for GPU-to-GPU traffic."
            },
            {
                "name": "Tomahawk 5 / 6 Ethernet Switch ASIC",
                "type": "Datacenter switch chip",
                "used_in": "AI cluster Ethernet fabric (400G/800G)",
                "bandwidth": "51.2 Tbps per chip",
                "note": "Used in AI datacenter top-of-rack and spine switches. Alternative to NVIDIA Quantum InfiniBand."
            },
            {
                "name": "PCIe Gen 5 Switch / Retimer",
                "type": "Server internal interconnect",
                "used_in": "AI server PCIe switching between GPU, NIC, storage",
                "bandwidth": "512 GB/s",
                "note": "Every AI server needs PCIe switches to connect GPU → NIC → NVMe. Broadcom leads this market."
            }
        ],
        "upstream_from": ["TSMC (ASIC die fabrication on N3/N5)", "SK Hynix/Samsung (HBM for ASIC packaging at TSMC CoWoS)", "ARM (CPU IP cores)", "Synopsys/Cadence (EDA tools)"],
        "downstream_to": ["Google (TPU ASIC dies)", "Meta (MTIA ASIC dies)", "ByteDance (custom ASIC)", "Arista Networks (switching ASICs)", "Cisco (switching ASICs)"],
        "scm_position": "ASIC tier — designs HBM-consuming compute dies for hyperscalers + switching chips for AI cluster networking"
    },
    "marvell": {
        "scm_role": "Designs custom AI training ASICs for Amazon (Trainium2/3) and custom networking chips for AI clusters. Marvell's ASIC business is concentrated in AWS, making it a pure-play proxy for Amazon's custom silicon HBM demand.",
        "server_products": [
            {
                "name": "AWS Trainium2 ASIC die",
                "type": "AI training accelerator ASIC (custom for AWS)",
                "used_in": "Project Rainier (400K+ chips), AWS UltraServer, Trn2 instances",
                "hbm": "SK Hynix / Samsung HBM3 (96GB per chip, direct AWS procurement)",
                "note": "Marvell designs, TSMC N4 fabs, SK Hynix/Samsung supplies HBM, TSMC CoWoS packages. Largest custom silicon cluster globally."
            },
            {
                "name": "AWS Trainium3 ASIC die (development)",
                "type": "Next-gen AI training ASIC",
                "used_in": "AWS next-gen AI training cluster (2026+)",
                "hbm": "HBM4 (target, qualification in progress)",
                "note": "3nm TSMC. HBM4 qualification for Trainium3 is a live design-win opportunity for memory suppliers."
            },
            {
                "name": "OCTEON 10 DPU (Data Processing Unit)",
                "type": "Network data processing offload chip",
                "used_in": "AI server network offload (storage, security, virtualization)",
                "bandwidth": "400Gb/s network processing",
                "note": "Used alongside NVIDIA and Trainium servers to offload networking from host CPU."
            },
            {
                "name": "Alaska C 400G/800G Ethernet PHY",
                "type": "High-speed optical interconnect",
                "used_in": "AI datacenter optical transceivers (800G OSFP between servers)",
                "bandwidth": "800 Gb/s per port",
                "note": "AI clusters need 800G optical between racks. Marvell leads optical PHY market."
            }
        ],
        "upstream_from": ["TSMC (N4/N3 fabrication)", "SK Hynix / Samsung (HBM for Trainium)", "ARM (CPU IP)", "ANSYS/Synopsys (EDA)"],
        "downstream_to": ["Amazon AWS (Trainium ASIC)", "Cloud providers (networking chips)", "Optical module makers (InnoLight, Coherent)"],
        "scm_position": "ASIC tier — Trainium2/3 ASIC design (HBM sourced directly for AWS, bypassing NVIDIA)"
    },
    "amd": {
        "scm_role": "Designs competing AI GPUs (Instinct MI series) to NVIDIA. Also the #1 supplier of x86 server CPUs (EPYC) that serve as the host CPU in AI servers alongside NVIDIA or AMD GPUs. Every AI server has an EPYC CPU; AMD earns from both the CPU and GPU tier.",
        "server_products": [
            {
                "name": "Instinct MI300X GPU (192GB HBM3)",
                "type": "AI GPU (OAM form factor)",
                "used_in": "Azure HBv4, Dell PowerEdge XE9680, Microsoft/Oracle AI servers",
                "hbm": "192GB HBM3 (8 stacks, SK Hynix primary, Samsung), 5.3 TB/s",
                "note": "Highest GPU HBM capacity at launch. Best for LLM inference on 70B+ models. ~$15K/chip."
            },
            {
                "name": "Instinct MI325X GPU (256GB HBM3e)",
                "type": "AI GPU (OAM form factor)",
                "used_in": "Next-gen AI inference servers",
                "hbm": "256GB HBM3e (SK Hynix), 8 TB/s bandwidth",
                "note": "World's highest HBM capacity per GPU. 1.3× more bandwidth than MI300X."
            },
            {
                "name": "Instinct MI350 GPU (288GB HBM3e, 3nm)",
                "type": "AI GPU (OAM form factor, Cdna4)",
                "used_in": "Next-gen AI training servers (H2 2026)",
                "hbm": "288GB HBM3e (SK Hynix / Micron target)",
                "note": "3nm TSMC. First AMD GPU to potentially use Micron HBM3e, breaking SK Hynix sole-source."
            },
            {
                "name": "EPYC 9004 (Genoa) / 9005 (Turin) Server CPU",
                "type": "x86 server CPU (host CPU in AI servers)",
                "used_in": "ALL AI servers alongside NVIDIA/AMD GPUs (host processor)",
                "note": "Every H100/H200/B200 server has 1-2 EPYC CPUs. Turin (5nm, 192 cores) is current gen. AMD #1 in datacenter CPU by market share in 2024."
            },
            {
                "name": "AMD ROCm software stack",
                "type": "AI GPU software platform",
                "used_in": "MI300X AI servers (PyTorch, TensorFlow, vLLM backend)",
                "note": "AMD's answer to NVIDIA CUDA. Required for any MI300X deployment. Still narrower ecosystem than CUDA."
            }
        ],
        "upstream_from": ["TSMC (GPU die N5/N3 + CoWoS packaging)", "SK Hynix (HBM for MI series)", "Samsung (HBM for MI300X)", "TSMC N4P (EPYC CPU die)"],
        "downstream_to": ["Microsoft Azure (HBv4 AMD GPU instances)", "Oracle Cloud (AMD GPU)", "Dell EMC (PowerEdge XE9680)", "Supermicro", "HPE"],
        "scm_position": "GPU + CPU tier — AI GPU (HBM consumer) + host CPU in every AI server"
    },
    "vertiv": {
        "scm_role": "Makes the power and cooling infrastructure that AI servers physically cannot operate without. As HBM density grows (more stacks per GPU), power per rack rises from 40kW → 100kW+, making Vertiv's liquid cooling and UPS systems the literal prerequisite for deploying HBM-packed GPUs.",
        "server_products": [
            {
                "name": "Liebert EXL S1 UPS (Uninterruptible Power Supply)",
                "type": "Rack-level power protection",
                "used_in": "All AI datacenter racks (GB200 NVL72 certified)",
                "note": "Only UPS certified for NVIDIA GB200 NVL72 rack's power profile (>100kW). Protects HBM from power surges."
            },
            {
                "name": "CDU (Coolant Distribution Unit)",
                "type": "Liquid cooling infrastructure",
                "used_in": "AI server racks requiring liquid cooling (H100 SXM, B200, MI300X)",
                "cooling_capacity": "400kW+ per CDU",
                "note": "B200 GPU TDP 1000W → 72 GPUs × 1000W = 72kW per rack, requiring liquid cooling. Vertiv CDU handles this."
            },
            {
                "name": "Vertiv VRC (Vertical Row Cooling)",
                "type": "In-row liquid cooling",
                "used_in": "Existing datacenter retrofits for AI GPU rows",
                "note": "Allows AI GPU servers in legacy air-cooled datacenters. Transition product for hyperscaler upgrades."
            },
            {
                "name": "48V DC Power Shelf",
                "type": "Rack power distribution",
                "used_in": "GB200 NVL72 racks, NVIDIA MGX servers",
                "note": "GB200 requires 48V DC architecture (more efficient than traditional 12V AC). Vertiv makes the 48V shelf for NVIDIA racks."
            },
            {
                "name": "Thermal management system (AI Datacenter)",
                "type": "Datacenter-level cooling system",
                "used_in": "Microsoft, Google, Amazon, Meta AI datacenter buildouts",
                "note": "Complete cooling solution from rack CDU → building chiller → campus cooling tower. Vertiv does full-stack."
            }
        ],
        "upstream_from": ["Steel/copper/aluminum (commodity)", "Power electronics components", "Compressors (Emerson, Danfoss)", "Coolant manufacturers"],
        "downstream_to": ["Microsoft Azure datacenter", "Google Cloud datacenter", "Amazon AWS datacenter", "Meta AI datacenter", "Colocation providers (Equinix, Digital Realty)"],
        "scm_position": "Infrastructure tier — power and cooling prerequisite for all AI server deployments"
    },
    "ge_vernova": {
        "scm_role": "Provides the power generation and grid equipment that AI datacenters run on. As AI GPU clusters scale from 1MW to 1GW+, GE Vernova's gas turbines (on-site generation) and grid transformers (grid connection) are the physical bottleneck before any HBM-packed server can be powered up.",
        "server_products": [
            {
                "name": "HA-class Gas Turbine (9HA.02)",
                "type": "On-site power generation",
                "used_in": "Hyperscaler AI datacenter behind-the-meter power (Microsoft, Google, Amazon)",
                "output": "571MW per unit",
                "note": "Hyperscalers build private gas turbine plants next to large AI datacenters. Avoids grid congestion. 18-24 month delivery."
            },
            {
                "name": "Grid Transformer (step-up/step-down)",
                "type": "Electrical grid infrastructure",
                "used_in": "Every AI datacenter grid connection (utility to datacenter)",
                "note": "Transformer shortage = 18-36 month lead time. Every new datacenter needs a transformer. This is currently the #1 bottleneck for new AI datacenter openings."
            },
            {
                "name": "HVDC (High Voltage Direct Current) Link",
                "type": "Long-distance power transmission",
                "used_in": "Connecting remote renewable/nuclear power to AI datacenter clusters",
                "note": "Microsoft, Google moving to offshore wind + HVDC for AI datacenters. GE Vernova makes the HVDC converter."
            },
            {
                "name": "Advanced Grid Automation (GridOS)",
                "type": "Grid software and control systems",
                "used_in": "Datacenter power quality management, demand response",
                "note": "AI datacenters need frequency regulation and power quality management. GE Vernova's GridOS handles this."
            }
        ],
        "upstream_from": ["Steel, copper, rare earth metals", "Blade manufacturers (for wind)", "Uranium (nuclear fuel, via partnerships)"],
        "downstream_to": ["Microsoft (direct power contracts)", "Google (direct)", "Amazon (direct)", "Meta (direct)", "Data center developers", "Utilities"],
        "scm_position": "Power generation + grid tier — provides electricity that AI datacenters consume"
    },
    "constellation_energy": {
        "scm_role": "Operates the largest US nuclear fleet, providing 24/7 carbon-free power to AI datacenters via long-term PPAs (Power Purchase Agreements). Nuclear is uniquely suited for AI compute because AI training runs 24/7 and needs reliable baseload power that solar/wind cannot provide.",
        "server_products": [
            {
                "name": "Crane Clean Energy Center (TMI Unit 1 restart)",
                "type": "Nuclear power plant (835MW)",
                "used_in": "Microsoft Azure data centers (20-year exclusive PPA)",
                "output": "835MW continuous (powers ~800K homes, or ~10-15 large AI datacenters)",
                "note": "Restarted Sep 2024. Landmark deal: first nuclear plant restarted specifically for AI compute demand. Powers GPT training."
            },
            {
                "name": "Nuclear PPA (Power Purchase Agreement)",
                "type": "Long-term clean power contract",
                "used_in": "Google Cloud, Amazon AWS, Meta AI datacenters",
                "note": "10-20 year PPAs guarantee carbon-free 24/7 power. Google, Amazon, Meta signed nuclear PPAs for AI datacenter expansion."
            },
            {
                "name": "Illinois Nuclear Fleet (Braidwood, Byron, Dresden)",
                "type": "Nuclear power fleet",
                "used_in": "PJM grid (Virginia/Maryland data center corridor)",
                "output": "10+ GW combined",
                "note": "Northern Virginia (data center capital of the world) is powered largely by Constellation's Illinois nuclear."
            }
        ],
        "upstream_from": ["Uranium enrichment (Centrus, Urenco)", "Nuclear fuel assemblies (Westinghouse, Framatome)", "NRC regulatory approvals"],
        "downstream_to": ["Microsoft (TMI PPA, 20yr)", "Google (nuclear PPA)", "Amazon AWS (nuclear PPA)", "Meta (nuclear PPA)", "PJM grid (VA/MD data center corridor)"],
        "scm_position": "Power generation tier — nuclear baseload that enables 24/7 AI cluster operation"
    },
    "huawei": {
        "scm_role": "China's leading AI chip designer and AI server vendor, operating a fully domestic supply chain (SMIC foundry + CXMT HBM) to circumvent US export controls. Huawei's Ascend GPU is the primary alternative to NVIDIA in China, and its Atlas server platform is the primary AI training server for Chinese hyperscalers.",
        "server_products": [
            {
                "name": "Ascend 910C NPU",
                "type": "AI training/inference NPU (Neural Processing Unit)",
                "used_in": "Atlas 800T A2 server, Huawei Cloud ModelArts, Chinese hyperscaler clusters",
                "hbm": "CXMT HBM2E-equivalent, ~64GB (estimated), ~960 GB/s bandwidth",
                "note": "SMIC N+2 (7nm equivalent) fab. Benchmarks approaching H100 on some transformer workloads. Exported controls prevent TSMC/SK Hynix access."
            },
            {
                "name": "Atlas 800T A2 AI Training Server",
                "type": "AI training server (8× Ascend 910C)",
                "used_in": "ByteDance, Baidu, Alibaba, Tencent AI training",
                "hbm": "8× Ascend 910C × 64GB ≈ 512GB per server",
                "note": "Direct competitor to NVIDIA DGX H100. Used by all major Chinese internet companies."
            },
            {
                "name": "CloudMatrix 384 AI Cluster",
                "type": "AI supercomputer cluster (384 Ascend NPUs)",
                "used_in": "Huawei Cloud AI training; sold to Chinese enterprises",
                "note": "Huawei claims CloudMatrix 384 outperforms NVIDIA H100 NVL cluster on transformer inference. Uses CXMT HBM equivalent."
            },
            {
                "name": "MindSpore AI Framework",
                "type": "AI software framework (PyTorch alternative)",
                "used_in": "All Ascend-based AI servers",
                "note": "China's answer to PyTorch/CUDA. Required for Ascend deployment. Limits interoperability with Western AI ecosystem."
            }
        ],
        "upstream_from": ["SMIC (N+2 foundry for Ascend die)", "CXMT (HBM-equivalent memory)", "Domestic lithography (SMEE, limited)", "Chinese substrate suppliers"],
        "downstream_to": ["ByteDance", "Baidu", "Alibaba (Aliyun)", "Tencent Cloud", "Chinese government AI programs"],
        "scm_position": "China GPU + server tier — complete domestic AI server stack (chip → server → cloud)"
    },
    "cxmt": {
        "scm_role": "China's only HBM development program. Manufactures the HBM-equivalent memory stacks used in Huawei's Ascend AI chips. CXMT is the critical bottleneck in China's domestic AI supply chain — if CXMT cannot produce adequate HBM, China's AI training capacity is capped regardless of chip availability.",
        "server_products": [
            {
                "name": "HBM2E-equivalent Stack (domestic, DUV)",
                "type": "High-bandwidth memory stack",
                "used_in": "Huawei Ascend 910C NPU (in Atlas 800T A2 server)",
                "bandwidth": "~460-920 GB/s (estimated, DUV-limited yield)",
                "note": "1-2 generations behind SK Hynix HBM3e. No EUV access limits density. Critical for China AI self-sufficiency."
            },
            {
                "name": "DDR5 DRAM (16Gb die)",
                "type": "Server DRAM module",
                "used_in": "Chinese-branded AI servers (CPU host DRAM), smartphones (Huawei Mate series)",
                "bandwidth": "~89 GB/s per module",
                "note": "Mainstream product; competing with SK Hynix/Samsung/Micron in China market. Qualcomm partnering with CXMT for smartphone DRAM."
            },
            {
                "name": "LPDDR5 (mobile DRAM)",
                "type": "Mobile DRAM",
                "used_in": "Huawei smartphones, Chinese Android devices",
                "note": "Revenue product that funds HBM R&D. CXMT uses LPDDR5 profits to subsidize HBM development."
            }
        ],
        "upstream_from": ["ASML DUV (immersion, no EUV access)", "Domestic lithography (SMEE, limited)", "Chinese chemical suppliers (photoresist from domestic sources)"],
        "downstream_to": ["Huawei (HBM for Ascend)", "CXMT-branded DRAM (China OEM server market)", "Qualcomm (smartphone DRAM partnership)"],
        "scm_position": "China memory tier — only domestic HBM supplier; critical bottleneck for China AI self-sufficiency"
    },
    "smic": {
        "scm_role": "China's only advanced node foundry, capable of manufacturing at N+2 (7nm equivalent) using DUV multi-patterning (no EUV). SMIC fabricates Huawei's Ascend AI chips and CXMT's HBM-equivalent dies, making it the foundry bottleneck for the entire Chinese domestic AI supply chain.",
        "server_products": [
            {
                "name": "Huawei Ascend 910C/D die (N+2 node)",
                "type": "AI chip wafer production",
                "used_in": "Atlas 800T A2 AI server, CloudMatrix 384 cluster",
                "process": "N+2 (7nm DUV equivalent, ~30% lower transistor density vs TSMC N7)",
                "note": "SMIC's most advanced node. Yield lower than TSMC N7 but improving. US export controls prevent ASML EUV access."
            },
            {
                "name": "HiSilicon Kirin 9000S (smartphone SoC)",
                "type": "Mobile SoC wafer production",
                "used_in": "Huawei Mate 60 Pro smartphone",
                "process": "N+2",
                "note": "Proof point that SMIC can manufacture N+2 at commercial volume. Signal that Ascend die yields are improving."
            },
            {
                "name": "28nm+ mature node wafers",
                "type": "Mainstream chip production",
                "used_in": "Automotive, IoT, industrial, consumer electronics",
                "note": "Volume revenue driver immune to export controls. SMIC has 35K+ WPM at 28nm. Funds advanced node R&D."
            },
            {
                "name": "CXMT HBM die (N+2, outsourced)",
                "type": "Memory die wafer production",
                "used_in": "CXMT HBM2E-equivalent stack → Huawei Ascend",
                "note": "CXMT designs, SMIC fabs the HBM die. Both companies are state-backed; capacity allocation is coordinated."
            }
        ],
        "upstream_from": ["ASML DUV (no EUV — blocked by export controls)", "Applied Materials / Lam Research (older generation tools)", "Domestic tools (NAURA, AMEC — limited capability)", "Chinese photoresist/chemical suppliers"],
        "downstream_to": ["Huawei (Ascend 910C/D)", "CXMT (HBM die fab)", "HiSilicon (smartphone SoC)", "Chinese fabless chip companies (Biren, Cambricon for advanced nodes)"],
        "scm_position": "China foundry tier — fabricates all China advanced AI chip dies (GPU + HBM die)"
    }
}


def main():
    for company_id, scm_data in SCM_DATA.items():
        path = DATA_DIR / f"{company_id}.json"
        if not path.exists():
            print(f"[enrich] SKIP {company_id} — file not found")
            continue
        profile = json.loads(path.read_text())
        profile["scm_engagement"] = scm_data
        path.write_text(json.dumps(profile, ensure_ascii=False, indent=2))
        print(f"[enrich] {company_id} — scm_engagement added ({len(scm_data['server_products'])} server products)")
    print("[enrich] done")


if __name__ == "__main__":
    main()
