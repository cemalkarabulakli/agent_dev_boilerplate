You are generating deterministic eval cases for a local-first agent.

Rules:
- Test the configured role, guardrails, memory behavior, and citation policy.
- Prefer cases that can be checked with required and forbidden terms.
- Do not require external APIs.
- Do not encode private or business-specific data.

Output:
- id
- input
- expected_behavior
- required_terms
- forbidden_terms
