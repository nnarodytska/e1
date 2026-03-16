### Skill: Metric Explorer

**When to activate:** Automatically when the user asks about a specific metric — what it means, how it works, where it's available, or how it differs across levels (VM vs ESXi vs Cluster). Also activate when the user seems confused about why a metric shows different values at different levels.

Produce a level-by-level breakdown:

1. **Metric Overview** — one sentence on what this metric measures

2. **Level Map** — a table showing for EACH level where the metric exists:

| Level | Available? | Formula / How calculated | Unit | Key difference at this level |
|-------|-----------|--------------------------|------|------------------------------|
| vCPU | | | | |
| VM | | | | |
| ESXi Host | | | | |
| Cluster | | | | |
| Datastore | | | | |
| Resource Pool | | | | |

Only include levels where the metric exists or where its absence is noteworthy.

3. **Cross-level gotchas** — Specific warnings about how the metric changes meaning or formula across levels. The book emphasizes these heavily (e.g., "VM CPU Used includes System time at VM level but NOT at vCPU level").

4. **Related metrics** — Other metrics that are often confused with this one or that should be checked alongside it, with a brief note on why.

5. **Practical guidance** — Which level should the user look at for performance troubleshooting vs capacity planning?
