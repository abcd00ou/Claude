# Shared Record Schema — the canonical contract

**Created:** 2026-06-22 · **Applies to:** every role agent in `salesmarketing 2.0`

Every role writes ONE flat record shape. It splits into two parts:

```
  record  =  ENVELOPE  (provenance + trust — identical for every role)
          +  PAYLOAD   (what THIS role tracks — declared per role spec)
```

Flat (not nested) on purpose: a flat record diffs cleanly cycle-over-cycle and serializes
deterministically, so two runs over the same frozen sources produce byte-identical output.
That determinism is what the diff and the eval harness depend on.

## Envelope fields (every role, every record)

| Field | Meaning |
|---|---|
| `schema_version` | contract version; consumers branch on it |
| `run_id` | which cycle/run produced this record |
| `retrieved_at` | ISO 8601, when the source was fetched |
| `source` | human label (e.g. "NVIDIA Q4 FY25 earnings call") |
| `source_url` | link to the source |
| `content_hash` | hash of the frozen snapshot the value came from |
| `snapshot_path` | path to the frozen snapshot (versioned evidence) |
| `quote` | verbatim source sentence the value came from |
| `locator` | filing item / transcript speaker-turn; best-effort |
| `source_tier` | `official` \| `analyst` \| `other` |
| `normalization_method` | how the raw value was normalized |
| `extractor_version` | which extractor produced it (for debugging drift) |
| `confidence` | 0–1, `min` of the deterministic subscores |
| `status` | `verified` \| `reconciled` \| `unverified-needs-human` |
| `status_reason` | reason code; required iff `status = unverified-needs-human` |

See [`trust_model.md`](trust_model.md) for `status` / `confidence` / `status_reason` rules.

## Payload (declared per role)

Each role spec lists its own payload fields. Examples of how the SAME envelope carries
different payloads:

- **Market Intelligence** → `{category, entity, period, period_type, fiscal_calendar, as_of_date, raw_value, raw_unit, normalized_value, currency}`
- **Price & Promotion** → `{metric, product_family, region, channel, as_of_date, raw_value, raw_unit, normalized_value, currency}`
- **Customer Tech** → `{signal_type, customer, product_family, stage, as_of_date, detail}`

## Validation rules (what a valid record must satisfy)

1. Exactly the envelope fields + the role's payload fields — no missing, no unknown.
2. `schema_version` matches the current contract.
3. `status`, `source_tier`, `status_reason` are known enum values.
4. `status_reason` is present iff `status = unverified-needs-human`; null otherwise.
5. `confidence` is a number in `[0, 1]`.
6. Numeric-payload roles (MI, Price & Promotion): a usable (`verified`/`reconciled`) record
   must carry a non-null `normalized_value`. A flagged record may have it null.

## Serialization (deterministic)

The pack is serialized with sorted keys, stable separators, and a `schema_version`-tagged
envelope, so re-running on the same frozen inputs yields byte-identical output. This is a
precondition for trustworthy diffs and for the eval harness to hash output.
