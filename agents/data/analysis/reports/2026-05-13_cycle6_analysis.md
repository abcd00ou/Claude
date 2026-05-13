# Cycle 6 Analysis Report — AI Supply Chain

**Date:** 2026-05-13  
**Source cycle:** Orchestrator Cycle 6  
**Purpose:** Derived interpretation only. Facts belong in section update logs.

---

## Demand Model Implications

### 1. Heterogeneous AI Factories Become the Default Planning Unit

Rubin, Trainium3, Ironwood, Maia, and NVLink Fusion show that demand should be modeled at rack/factory level, not only GPU unit level. Future demand models should separate:

- Merchant GPU racks: NVIDIA Rubin / Blackwell, AMD Instinct.
- Custom ASIC racks: AWS Trainium, Google TPU, Microsoft Maia, Meta MTIA.
- Hybrid racks: custom XPUs or CPUs integrated through NVIDIA NVLink Fusion / Spectrum-X.

### 2. Capex-To-Chip Conversion Needs A Physical Deployment Discount

Microsoft, Meta, Amazon, and Google-level capex signals are large enough to support demand, but transformer and grid equipment lead times mean booked capex does not convert into live compute immediately. Add a deployment discount to capex-derived accelerator demand:

```text
Live Compute Capacity = Ordered Compute Capacity × Power/Grid Availability Factor
```

Initial default: use a qualitative `grid_constrained` flag until transformer, switchgear, substation, and utility interconnection evidence is quantified.

### 3. Custom Silicon Is Additive To HBM / Foundry Pressure

Trainium3 and Ironwood use high-capacity HBM and advanced-node silicon. Treat custom ASICs as incremental demand on HBM and foundry capacity, not as a clean subtraction from NVIDIA demand.

### 4. Packaging Relief Timing

Amkor Arizona advanced packaging production starts in early 2028, based on company guidance. For 2026–2027 bottleneck modeling, do not count U.S. OSAT capacity as available relief unless explicit qualification and production timing are confirmed.

---

## Model Updates To Consider

- Add a `rack_scale_platform` demand category for Rubin NVL72, Trainium3 UltraServer, Ironwood pod, and NVLink Fusion systems.
- Add `grid_equipment_lead_time_weeks` as a physical deployment risk variable.
- Add `custom_asic_hbm_load` to HBM demand estimates.
- Keep `osat_cowos_relief` at `unconfirmed_before_2028` until Amkor/TSMC qualification details are public.

---

## Evidence Quality Notes

- High confidence: NVIDIA, AWS, Google, Microsoft, Meta, Samsung, Amkor, Wolfspeed, DOE, and NREL official materials.
- Medium confidence: Wood Mackenzie lead-time figures via POWER executive summary; use as benchmark until primary Wood Mackenzie dataset is licensed or obtained.
- Unresolved: Samsung NVIDIA HBM qualification, Google Ironwood process node, Amkor CoWoS-class production qualification, and Trainium4 NVLink Fusion implementation details.
