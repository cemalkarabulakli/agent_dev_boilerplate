# V4 Research Sources

Each source has its own config, raw storage, processed storage, and reports.

Rules:

- Raw source output is saved under `research/sources/{source}/raw/`.
- Processed source-linked insights are saved under `research/sources/{source}/processed/`.
- Human-readable source reports are saved under `research/sources/{source}/reports/`.
- Every raw signal gets a reference entry in `research/index/collected_references.jsonl`.
- Raw dumps must not be injected directly into agent context.
- Only processed, scored, source-linked insights can be considered for compacted context.
- Human review is required before insights update business strategy.
