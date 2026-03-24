### Skill: CPU Frequency, Turbo Boost & Power Management

**When to activate:** When a question asks about actual CPU speed a vCPU will receive, what frequency a core runs at, the effect of Turbo Boost, the difference between Balanced vs High Performance power policy, or any question involving nominal / All-Cores Turbo / Single-Core Turbo speeds.

---

#### The three CPU speed numbers — know which one applies

| Speed | What it is | When it applies |
|---|---|---|
| **Nominal (Base)** | The rated clock frequency. What vSphere uses as total capacity baseline. | The CPU *rarely* runs at this speed in practice — it runs above it. |
| **All Cores Turbo** | Max speed when *all* cores are simultaneously active. | Under heavy full-cluster load. This is the practical ceiling for a busy cluster. The book says: "This is what you should pay attention to." |
| **Single Core Turbo** | Max speed when only *one* (or very few) cores are active. | When most cores are idle and the socket power budget can be concentrated on one core. |

---

#### BIOS Power Setting: OS Controlled

- **OS Controlled** means ESXi has full authority over P-states (performance states) and C-states (idle states) via ACPI.
- ESXi can actively put idle cores into deep C-states and redirect that power budget into Turbo on active cores.
- This is the **prerequisite** for Balanced policy to fully exploit Turbo Boost.
- With BIOS set to static High Performance, ESXi loses C-state flexibility — all cores are pinned at a fixed high P-state (~130% of nominal). Note: Turbo can still kick in to some degree even with BIOS static High Performance (verified in the book via esxtop %A/MPERF showing 129%), but the dynamic range is narrower.

---

#### Balanced vs High Performance policy — the key insight

The book's chart (CPU > CPU Frequency > High Performance vs Balanced) shows:

- **High Performance** keeps all cores at a constant elevated frequency (~130% of nominal). No C-states. Static.
- **Balanced** puts idle cores into deep C-states and uses the saved power budget to push active cores to **higher Turbo states** — up to ~151% of nominal in the book's example.
- **Balanced can deliver higher per-vCPU frequency than High Performance**, especially at low-to-medium host utilisation.
- At HIGH host utilisation (all cores busy), the advantage narrows but Balanced still reaches All Cores Turbo.

> Key quote from the book: *"Balanced was running higher than High Performance... it can boost the running cores to 151% as other cores are idle."*

---

#### What speed does a vCPU actually get? — Decision logic

Use this logic when asked "what speed will a vCPU get?":

1. **Is the cluster idle or lightly loaded?**
   - Balanced + OS Controlled → many cores in C-state → active cores can reach **Single Core Turbo** territory (highest possible speed).

2. **Is the cluster busy (many demanding VMs)?**
   - "Busy cluster" does NOT mean every single core is simultaneously pegged at 100%. In practice, even a heavily loaded cluster has some cores more active than others at any instant.
   - With BIOS **OS Controlled** + ESXi **Balanced**: ESXi manages P-states and C-states, pushing active cores toward Single Core Turbo by exploiting the per-socket power envelope. Balanced reaches ~151% of nominal in the book's chart.
   - Balanced policy's design is precisely to concentrate the socket power budget on whichever cores are actively running — reaching **Single Core Turbo** for those cores.
   - **All Cores Turbo** would only be the ceiling if truly *every* core on every socket were simultaneously maxed with zero power headroom — the true worst case.
   - With BIOS **High Performance** (static): All cores run at a fixed ~130% of nominal. No dynamic boost possible.

3. **Is the exact frequency predictable?**
   - The book is explicit: *"Within a core, it is impossible to predict the core frequency. It all depends on the instructions and what other cores are doing."*
   - However, if a question gives a Balanced + OS Controlled scenario and asks for the *most realistic* speed, the answer is the **Single Core Turbo** value — because Balanced policy's design goal is to reach that ceiling by concentrating the socket power budget on active cores.
   - Only answer "it depends / not enough info" if the power policy or BIOS setting is missing or ambiguous.

---

#### All-Core Turbo and TDP — power envelope

- Intel's **All-Core Turbo** frequency is the maximum all-core speed *within* the CPU's TDP (Thermal Design Power).
- Example: a 24-core CPU at 2.4 GHz nominal with 3.4 GHz All-Core Turbo and 210W TDP — the 3.4 GHz is achievable across all cores while staying within 210W.
- The book: *"The overall power envelope within the socket remains the same"* — applies to the Turbo mechanism generally.
- **Single-Core Turbo** concentrates the full TDP budget on one core (others sleeping) → highest per-core speed, same total power.
- Saying "All-Core Turbo uses the same power as base frequency" is a simplification: both operate within TDP, but All-Core Turbo uses the full TDP ceiling while base may use less.
- **High Performance setting does NOT cause the CPU to exceed TDP** — that is not why it's sometimes not recommended. The reason is it prevents Balanced from exploiting C-states to reach higher single-core Turbo.

---

#### HT does NOT reduce clock speed

- HyperThreading is a **metric accounting factor** (credited as 0.625x throughput per thread when both threads share a core).
- The physical clock frequency of the core is **not changed** by HT being ON or by both threads being active.
- Never apply the HT 0.625x factor to clock frequency — they are completely separate.

---

#### Quick reference — worked example from the book

CPU: 1 GHz nominal, 1.3x All Cores Turbo, 1.7x Single Core Turbo, HT ON, Balanced, OS Controlled.

| Scenario | Expected vCPU speed |
|---|---|
| All cores busy, single vCPU VM | ~1.3 GHz (All Cores Turbo) |
| Single core active, rest idle | ~1.7 GHz (Single Core Turbo) |
| Balanced policy, busy cluster | Up to Single Core Turbo (~1.7 GHz) because Balanced exploits power headroom |

To apply the ratios: multiply the nominal speed by 1.3x for All Cores Turbo and 1.7x for Single Core Turbo, then match the result to the given frequency options.
