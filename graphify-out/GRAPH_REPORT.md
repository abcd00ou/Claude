# Graph Report - AI_SCM + ssd_ai_potential  (2026-04-29)

## Corpus Check
- 170 files · ~394,652 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 721 nodes · 1084 edges · 47 communities detected
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 62 edges (avg confidence: 0.8)
- Token cost: 22,200 input · 5,300 output

## Community Hubs (Navigation)
- [[_COMMUNITY_SSD Demand Signals & Communities|SSD Demand Signals & Communities]]
- [[_COMMUNITY_AI Supply Chain Companies|AI Supply Chain Companies]]
- [[_COMMUNITY_AI SCM Intelligence & Analysis|AI SCM Intelligence & Analysis]]
- [[_COMMUNITY_Database Agent & Historical Data|Database Agent & Historical Data]]
- [[_COMMUNITY_Daily Content Pipeline|Daily Content Pipeline]]
- [[_COMMUNITY_SSD Demand Analyzer (Code)|SSD Demand Analyzer (Code)]]
- [[_COMMUNITY_Study Email & Content Generation|Study Email & Content Generation]]
- [[_COMMUNITY_Report & Visualization Agent|Report & Visualization Agent]]
- [[_COMMUNITY_Modeling Agent (Token→GPU→HBM)|Modeling Agent (Token→GPU→HBM)]]
- [[_COMMUNITY_Final Report Generation (PPTXDOCX)|Final Report Generation (PPTX/DOCX)]]
- [[_COMMUNITY_Bottleneck Detection Agent|Bottleneck Detection Agent]]
- [[_COMMUNITY_Study Runner & Progress Agent|Study Runner & Progress Agent]]
- [[_COMMUNITY_Demand Mapper & Gap Engine|Demand Mapper & Gap Engine]]
- [[_COMMUNITY_HBM Supply Chain|HBM Supply Chain]]
- [[_COMMUNITY_Power Infrastructure|Power Infrastructure]]
- [[_COMMUNITY_Sovereign AI & Geopolitics|Sovereign AI & Geopolitics]]
- [[_COMMUNITY_CoWoS Packaging|CoWoS Packaging]]
- [[_COMMUNITY_AI Networking (InfiniBandEthernet)|AI Networking (InfiniBand/Ethernet)]]
- [[_COMMUNITY_Investment Framework|Investment Framework]]
- [[_COMMUNITY_Token Demand & LLM Services|Token Demand & LLM Services]]
- [[_COMMUNITY_Hyperscaler CapEx|Hyperscaler CapEx]]
- [[_COMMUNITY_Earnings Data (MicronSK Hynix)|Earnings Data (Micron/SK Hynix)]]
- [[_COMMUNITY_SSD Product Positioning|SSD Product Positioning]]
- [[_COMMUNITY_Edge AI & Physical AI|Edge AI & Physical AI]]
- [[_COMMUNITY_Strategy Agent|Strategy Agent]]
- [[_COMMUNITY_NVIDIA GPU Platform|NVIDIA GPU Platform]]
- [[_COMMUNITY_SSD Community Reddit Data|SSD Community Reddit Data]]
- [[_COMMUNITY_Data Collection & Crawling|Data Collection & Crawling]]
- [[_COMMUNITY_Semiconductor Process (TSMC)|Semiconductor Process (TSMC)]]
- [[_COMMUNITY_xAI & New Entrants|xAI & New Entrants]]
- [[_COMMUNITY_AI Model Deployment (Local LLM)|AI Model Deployment (Local LLM)]]
- [[_COMMUNITY_CHIPS Act & Policy|CHIPS Act & Policy]]
- [[_COMMUNITY_SSD Technical Drivers|SSD Technical Drivers]]
- [[_COMMUNITY_WDSanDisk Products|WD/SanDisk Products]]
- [[_COMMUNITY_Cost & Pricing Models|Cost & Pricing Models]]
- [[_COMMUNITY_NVMe Speed & VRAM Offload|NVMe Speed & VRAM Offload]]
- [[_COMMUNITY_Scaling Laws & Theory|Scaling Laws & Theory]]
- [[_COMMUNITY_Data Center Infrastructure|Data Center Infrastructure]]
- [[_COMMUNITY_Config & Pipeline Orchestration|Config & Pipeline Orchestration]]
- [[_COMMUNITY_AI Cluster Networking|AI Cluster Networking]]
- [[_COMMUNITY_Study Content Levels (Lv1-3)|Study Content Levels (Lv1-3)]]
- [[_COMMUNITY_Market Analysis Reports|Market Analysis Reports]]
- [[_COMMUNITY_Supply Gap Analysis|Supply Gap Analysis]]
- [[_COMMUNITY_Prompt & Agent Definitions|Prompt & Agent Definitions]]
- [[_COMMUNITY_Crawling & Data Ingestion|Crawling & Data Ingestion]]
- [[_COMMUNITY_Misc Utilities|Misc Utilities]]
- [[_COMMUNITY_Output Artifacts|Output Artifacts]]

## God Nodes (most connected - your core abstractions)
1. `SSD × Local AI Demand Analysis Report Series (Mar-Apr 2026)` - 29 edges
2. `NVIDIA` - 17 edges
3. `run_full_pipeline()` - 14 edges
4. `HBM (High Bandwidth Memory)` - 14 edges
5. `model_hardware_demand()` - 11 edges
6. `Power/DC Infrastructure Bottleneck` - 11 edges
7. `generate_html_report()` - 10 edges
8. `build_gap_report()` - 10 edges
9. `build()` - 10 edges
10. `build()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `make_docx()` --calls--> `set_cell_bg()`  [INFERRED]
  AI_SCM/generate_final_report.py → ssd_ai_potential/outputs/build_pptx.py
- `main()` --calls--> `send_study_email()`  [INFERRED]
  AI_SCM/run_study.py → AI_SCM/agents/daily/study_email_agent.py
- `run_full_pipeline()` --calls--> `load_gap_report()`  [INFERRED]
  AI_SCM/run.py → AI_SCM/agents/gap_engine.py
- `cmd_status()` --calls--> `print_status()`  [INFERRED]
  AI_SCM/run_daily.py → AI_SCM/agents/daily/progress_agent.py
- `main()` --calls--> `build()`  [INFERRED]
  AI_SCM/run_newsletter.py → AI_SCM/agents/newsletter/newsletter_builder.py

## Communities

### Community 0 - "SSD Demand Signals & Communities"
Cohesion: 0.03
Nodes (82): Linux Page Cache Hidden Write Latency on ARM64 (Jetson Orin) — SSD I/O bottleneck in edge AI inference, 용량 전략: 7B~70B 모델 복수 보유 트렌드 → 2TB/4TB 대용량 SKU 강조 (Apr-05 이후 등장), r/buildapc — highest demand signal volume: ~14-14.4% demand rate, 1,460–1,686 posts, HackerNews — 0% SSD demand rate in monitored posts, r/homelab — highest demand rate: 18.3-18.5%; 951–1,045 posts, r/LocalLLaMA — 2.7-2.9% demand rate; 1,869–2,258 posts (largest community by volume), 커뮤니티: reddit/r/buildapc - 수요율 약 15.1%, 커뮤니티: reddit/r/homelab - 수요율 약 19.9% (가장 높은 수요 신호율) (+74 more)

### Community 1 - "AI Supply Chain Companies"
Cohesion: 0.04
Nodes (60): Amazon (AWS), AMD, Arista Networks, Broadcom, Micron Technology, NVIDIA, Samsung Electronics, SK Hynix (+52 more)

### Community 2 - "AI SCM Intelligence & Analysis"
Cohesion: 0.07
Nodes (44): AI SCM Final Report 20260409, AI SCM Study Report 20260411, Amazon (AWS), Anthropic, Bottleneck Cascade (GPU→HBM→Power→Network), Broadcom, CHIPS and Science Act (2022), CoWoS Packaging Bottleneck (+36 more)

### Community 3 - "Database Agent & Historical Data"
Cohesion: 0.07
Nodes (40): _connect(), init_db(), load_historical_data(), DB Agent — PostgreSQL ai_scm 데이터베이스 연동 psycopg2 없거나 DB 연결 실패 시 조용히 fallback 시계열, seed_data.json의 과거 시계열 데이터를 DB에 bulk insert., run(), save_all(), load_demand_state() (+32 more)

### Community 4 - "Daily Content Pipeline"
Cohesion: 0.08
Nodes (35): cmd_evening(), cmd_morning(), cmd_preview(), cmd_reset(), cmd_status(), main(), load_comment(), main() (+27 more)

### Community 5 - "SSD Demand Analyzer (Code)"
Cohesion: 0.07
Nodes (26): aggregate(), AnalyzerAgent, classify_by_keywords(), classify_with_claude(), extract_technical_factors(), has_portable_ssd(), analyzer_agent.py — 수요 신호 분류 + 기술 근거 추출 Claude API 사용 가능 시: AI 분류 / 없을 시: 키워드 기반, Claude API로 20개씩 배치 분류 (+18 more)

### Community 6 - "Study Email & Content Generation"
Cohesion: 0.13
Nodes (25): get_topic_news(), build_email_html(), _capex_bar_html(), _cat_color(), _compact_recap_html(), _content_cowos(), _content_hbm(), _content_hyperscaler() (+17 more)

### Community 7 - "Report & Visualization Agent"
Cohesion: 0.12
Nodes (23): _build_bottleneck_section(), _build_capex_section(), _build_demand_table(), _build_forecast_section(), _build_network_graph_section(), _build_signals_section(), _build_value_chain_section(), generate_html_report() (+15 more)

### Community 8 - "Modeling Agent (Token→GPU→HBM)"
Cohesion: 0.13
Nodes (23): build_scenario_table(), compute_current_snapshot(), compute_total_token_demand(), gpu_capex(), gpu_to_hbm(), memory_pressure(), model_hardware_demand(), power_demand() (+15 more)

### Community 9 - "Final Report Generation (PPTX/DOCX)"
Cohesion: 0.28
Nodes (19): make_docx(), add_footer(), add_hyperlink_to_cell(), add_textbox(), main(), make_table(), new_prs(), SSD Demand Analysis PPT 생성 스크립트 (+11 more)

### Community 10 - "Bottleneck Detection Agent"
Cohesion: 0.16
Nodes (17): analyze_cascade_risk(), compute_bottleneck_scores(), compute_supply_demand_gap(), find_primary_bottleneck(), load_gap_report(), predict_cascade(), Bottleneck Detection Agent - Calculate demand/capacity ratio per layer - Score c, gap_engine이 생성한 gap_report.json을 로드합니다. (+9 more)

### Community 11 - "Study Runner & Progress Agent"
Cohesion: 0.21
Nodes (15): main(), advance(), _do_advance(), get_current_topic(), _get_previous_context(), is_duplicate(), _last_sent_entry(), load_state() (+7 more)

### Community 12 - "Demand Mapper & Gap Engine"
Cohesion: 0.2
Nodes (14): _capex_to_hbm_demand(), collect_demand_state(), compute_tier1_demand(), compute_tier2_demand(), compute_tier3_demand(), compute_tier4_demand(), demand_mapper.py — 고객 수요 역산 에이전트  공개 데이터(CapEx 공시, GPU 출하 가이던스, DC 착공 공시)를 조합해 고, Tier 1 — 하이퍼스케일러 수요 역산. (+6 more)

### Community 13 - "HBM Supply Chain"
Cohesion: 0.13
Nodes (15): AI Supply Chain Study Agent System (prompt.md), AI SCM Python Requirements, AI SCM Intelligence System, Bottleneck Detection Agent, Daily Learning System (Email Automation), Demand Mapper Agent (CapEx Reverse Calc), Earnings Agent (SEC/IR Parser), Intelligence Pipeline (Supply-Demand Engine) (+7 more)

### Community 14 - "Power Infrastructure"
Cohesion: 0.2
Nodes (13): build_market_events(), build_timeseries_summary(), classify_headline(), load_seed_data(), Data Intelligence Agent - Loads seed data - Attempts web scraping for latest mar, Build structured market events from seed data., 과거 시계열 데이터 요약 — 시계열 분석용., Run the data agent and return market state. (+5 more)

### Community 15 - "Sovereign AI & Geopolitics"
Cohesion: 0.3
Nodes (13): _add_heading(), _add_refs(), _add_table(), _box(), build(), _concept(), _marketing(), _quant() (+5 more)

### Community 16 - "CoWoS Packaging"
Cohesion: 0.3
Nodes (13): _add_heading(), _add_refs(), _add_table(), _box(), build(), _concept(), _marketing(), _quant() (+5 more)

### Community 17 - "AI Networking (InfiniBand/Ethernet)"
Cohesion: 0.3
Nodes (13): _add_heading(), _add_refs(), _add_table(), _box(), build(), _concept(), _marketing(), _quant() (+5 more)

### Community 18 - "Investment Framework"
Cohesion: 0.33
Nodes (12): _add_heading(), _add_refs(), _add_table(), _box(), build(), _concept(), _marketing(), _quant() (+4 more)

### Community 19 - "Token Demand & LLM Services"
Cohesion: 0.33
Nodes (12): _add_heading(), _add_refs(), _add_table(), _box(), build(), _concept(), _marketing(), _quant() (+4 more)

### Community 20 - "Hyperscaler CapEx"
Cohesion: 0.33
Nodes (12): _add_heading(), _add_refs(), _add_table(), _box(), build(), _concept(), _marketing(), _quant() (+4 more)

### Community 21 - "Earnings Data (Micron/SK Hynix)"
Cohesion: 0.31
Nodes (12): _add_heading(), _add_refs(), _add_table(), _box(), build(), _concept(), _marketing(), _quant() (+4 more)

### Community 22 - "SSD Product Positioning"
Cohesion: 0.31
Nodes (12): _add_heading(), _add_refs(), _add_table(), _box(), build(), _concept(), _marketing(), _quant() (+4 more)

### Community 23 - "Edge AI & Physical AI"
Cohesion: 0.37
Nodes (12): build(), _chg_color(), _chg_str(), _fmt(), _price_cell(), Newsletter Builder 실시간 데이터 + 분석 → 종합 HTML 뉴스레터 섹션: Executive Summary / Layer Sco, _section_company_table(), _section_executive() (+4 more)

### Community 24 - "Strategy Agent"
Cohesion: 0.23
Nodes (11): build_company_graph(), build_network_graph(), get_bottleneck_companies(), get_layer_summary(), Supply Chain Mapping Agent - Builds knowledge graph from VALUE_CHAIN config - Ma, Build complete company-to-supply-chain knowledge graph., Get companies in critical/high bottleneck layers., Summarize companies per layer. (+3 more)

### Community 25 - "NVIDIA GPU Platform"
Cohesion: 0.23
Nodes (11): analyze_key_themes(), analyze_risks(), determine_phase_position(), generate_signals_from_bottlenecks(), Strategy / Investment Agent - Maps bottleneck analysis to investment phases - Ge, Determine current investment cycle phase based on bottleneck., Generate investment signals based on bottleneck analysis., Identify key investment themes. (+3 more)

### Community 26 - "SSD Community Reddit Data"
Cohesion: 0.24
Nodes (10): Email Agent - Gmail SMTP로 학습 문서 자동 발송 - App Password 인증 - DOCX 첨부 지원, send_study_doc(), find_latest_docx(), load_state(), Study Scheduler - 학습 커리큘럼 관리 (8개 주제 × 3 라운드) - 각 에이전트 실행 → DOCX 생성 → Gmail 발송 -, 에이전트 실행 — level 파라미터 전달., run_agent(), run_next() (+2 more)

### Community 27 - "Data Collection & Crawling"
Cohesion: 0.17
Nodes (12): GE Vernova, AI Supply Chain Bottleneck Cascade, ChatGPT Launch (Nov 2022) as AI Supply Chain Trigger, AI Supply Chain Investment Wave Framework (Phase 1-5), Phase 5: Physical AI / Robotics Investment Wave, AI Data Center Power Infrastructure Bottleneck, Power Transformer Supply Bottleneck (30-month lead time), [Study] AI Supply Chain Intelligence Report (Apr 2026 v2) (+4 more)

### Community 28 - "Semiconductor Process (TSMC)"
Cohesion: 0.27
Nodes (10): collect_supply_state(), get_next_earnings(), parse_pdf_with_claude(), parse_sec_press_release(), earnings_agent.py — 공급 수치 수집 에이전트  실적발표 PDF/텍스트를 Claude API로 파싱해 공급 수치를 구조화합니다., SEC EDGAR press release HTML을 정규식으로 파싱해 공급 수치를 추출합니다.     Claude API 없이 동작 — 1차, 실적발표 PDF를 Claude API로 파싱해 공급 수치를 추출합니다.      사용 방법:         1. earnings_pdfs/ 디렉, 공급 수치를 수집합니다.      순서:     1. earnings_pdfs/ 에 PDF가 있으면 Claude API로 파싱     2. 없으 (+2 more)

### Community 29 - "xAI & New Entrants"
Cohesion: 0.29
Nodes (10): _add_heading(), _add_methodology_box(), _add_ref_table(), _add_table(), build(), _load_state(), Word Agent — 한국어 학습용 Word 보고서 생성 주제별 8장 구성, 50+ 참고자료, 상세 방법론 설명 포함 출력: outputs/r, ALL_REFERENCES에서 키를 조회하여 참고자료 표 추가. (+2 more)

### Community 30 - "AI Model Deployment (Local LLM)"
Cohesion: 0.39
Nodes (7): _classify_category(), fetch_news(), _fetch_rss(), _is_scm_relevant(), _parse_date(), News Agent - AI SCM 뉴스 수집 RSS 실시간 수집 + 정확한 seed 뉴스 fallback 기준: 2026년 4월 현재 시장 상, 실시간 RSS 수집 → 실패 시 seed 뉴스 반환

### Community 31 - "CHIPS Act & Policy"
Cohesion: 0.4
Nodes (5): Capacity Strategy: 2TB/4TB Large SKU Emphasis — driven by trend of users owning multiple 7B-70B models simultaneously, Early Report Insight (Mar 13): Portable Use was Priority #1 Driver (110 mentions) before Model File Size took over by Mar 18, MoE Runtime Achieving 3,324 tok/s Prefill on Single RTX 5080 — Hybrid MoE runtime with specific SSD loading patterns, Qwen3.5-35B-A3B Quantization Benchmarks on RTX 5080 16GB (Q8_0) — large quantized model requiring substantial SSD storage, Top SSD Demand Driver: Model File Capacity (314 mentions by Apr 21) — LLM weights require large storage

### Community 32 - "SSD Technical Drivers"
Cohesion: 0.5
Nodes (4): 48-Core 128GB 2.5G Homelab Build (score 815) — high-end homelab AI servers as SSD demand vector, 9-Slot SSD Backplane (homelab community viral post, score 2069) — multi-SSD homelab AI server build, r/homelab Highest SSD Demand Rate: 17.4% (202 of 1,164 posts) — homelabbers most active SSD buyers, HackerNews SSD Demand Signal: ~0% despite 9 posts collected — developer/tech community less focused on hardware purchasing

### Community 33 - "WD/SanDisk Products"
Cohesion: 0.67
Nodes (3): r/StableDiffusion SSD Demand Rate: 2.2-3.0% — AI image generation creating SSD wear risk via swap usage, Risk: Using SSD as Virtual Memory for AI Generation Damages SSDs — StableDiffusion community warning, zRAM as Swap Alternative to SSD — Linux community recommending RAM-based swap to preserve SSD lifespan during AI workloads

### Community 34 - "Cost & Pricing Models"
Cohesion: 1.0
Nodes (1): AI Supply Chain Intelligence System - Configuration All constants, parameters, a

### Community 35 - "NVMe Speed & VRAM Offload"
Cohesion: 1.0
Nodes (1): AI Supply Chain Intelligence System - Agents Package

### Community 36 - "Scaling Laws & Theory"
Cohesion: 1.0
Nodes (1): AI SCM 커버리지 유니버스 — 전 레이어 30개+ 기업

### Community 37 - "Data Center Infrastructure"
Cohesion: 1.0
Nodes (1): SSD × AI 수요 조사 에이전트 — 설정

### Community 38 - "Config & Pipeline Orchestration"
Cohesion: 1.0
Nodes (2): Microsoft, OpenAI

### Community 39 - "AI Cluster Networking"
Cohesion: 1.0
Nodes (2): Google, Google TPU

### Community 40 - "Study Content Levels (Lv1-3)"
Cohesion: 1.0
Nodes (2): r/SelfHosted SSD Demand Rate: 11.8% (103 of 876 posts) — self-hosters show strong AI-SSD correlation, LM Studio Malware Concern Post (r/LocalLLaMA, score 1048) — security risk drives users toward self-hosted alternatives requiring local SSD storage

### Community 41 - "Market Analysis Reports"
Cohesion: 1.0
Nodes (2): r/LocalLLaMA Low Demand Rate: 2.5% (66 of 2,661 posts) — LLM community focused on model quality not hardware purchasing, Recommended Marketing Channels: r/LocalLLaMA, r/OllamaAI, r/SelfHosted — direct community engagement possible

### Community 44 - "Supply Gap Analysis"
Cohesion: 1.0
Nodes (1): AI SCM Study Report 20260325

### Community 45 - "Prompt & Agent Definitions"
Cohesion: 1.0
Nodes (1): AI SCM Study Report 20260324

### Community 46 - "Crawling & Data Ingestion"
Cohesion: 1.0
Nodes (1): Meta

### Community 47 - "Misc Utilities"
Cohesion: 1.0
Nodes (1): [Study] NVIDIA Supply Chain

### Community 48 - "Output Artifacts"
Cohesion: 1.0
Nodes (1): r/buildapc SSD Demand Rate: 13.9% (266 of 1,919 posts) — PC builders second largest SSD demand community

## Knowledge Gaps
- **255 isolated node(s):** `AI Supply Chain Intelligence System - Main Orchestrator  Usage:     python run.p`, `agents/ 디렉토리에서 에이전트 모듈을 동적으로 임포트.`, `Load previous run state if available.`, `Save current run state.`, `Load market state from previous data agent run.` (+250 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Cost & Pricing Models`** (2 nodes): `config.py`, `AI Supply Chain Intelligence System - Configuration All constants, parameters, a`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `NVMe Speed & VRAM Offload`** (2 nodes): `AI Supply Chain Intelligence System - Agents Package`, `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scaling Laws & Theory`** (2 nodes): `universe.py`, `AI SCM 커버리지 유니버스 — 전 레이어 30개+ 기업`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Data Center Infrastructure`** (2 nodes): `config.py`, `SSD × AI 수요 조사 에이전트 — 설정`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Config & Pipeline Orchestration`** (2 nodes): `Microsoft`, `OpenAI`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `AI Cluster Networking`** (2 nodes): `Google`, `Google TPU`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Study Content Levels (Lv1-3)`** (2 nodes): `r/SelfHosted SSD Demand Rate: 11.8% (103 of 876 posts) — self-hosters show strong AI-SSD correlation`, `LM Studio Malware Concern Post (r/LocalLLaMA, score 1048) — security risk drives users toward self-hosted alternatives requiring local SSD storage`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Market Analysis Reports`** (2 nodes): `r/LocalLLaMA Low Demand Rate: 2.5% (66 of 2,661 posts) — LLM community focused on model quality not hardware purchasing`, `Recommended Marketing Channels: r/LocalLLaMA, r/OllamaAI, r/SelfHosted — direct community engagement possible`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Supply Gap Analysis`** (1 nodes): `AI SCM Study Report 20260325`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Prompt & Agent Definitions`** (1 nodes): `AI SCM Study Report 20260324`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Crawling & Data Ingestion`** (1 nodes): `Meta`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Misc Utilities`** (1 nodes): `[Study] NVIDIA Supply Chain`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Output Artifacts`** (1 nodes): `r/buildapc SSD Demand Rate: 13.9% (266 of 1,919 posts) — PC builders second largest SSD demand community`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_full_pipeline()` connect `Database Agent & Historical Data` to `SSD Demand Analyzer (Code)`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `main()` connect `Study Runner & Progress Agent` to `SSD Demand Analyzer (Code)`, `Study Email & Content Generation`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `send_study_email()` connect `Study Email & Content Generation` to `Study Runner & Progress Agent`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `run_full_pipeline()` (e.g. with `init_db()` and `save_all()`) actually correct?**
  _`run_full_pipeline()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `AI Supply Chain Intelligence System - Main Orchestrator  Usage:     python run.p`, `agents/ 디렉토리에서 에이전트 모듈을 동적으로 임포트.`, `Load previous run state if available.` to the rest of the system?**
  _255 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `SSD Demand Signals & Communities` be split into smaller, more focused modules?**
  _Cohesion score 0.03 - nodes in this community are weakly interconnected._
- **Should `AI Supply Chain Companies` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._