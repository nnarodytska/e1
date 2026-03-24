### Skill: ESXi CPU Capacity Metrics

**When to activate:** When the question involves:
- Which ESXi CPU metric shows "true utilisation" or "real utilization"
- Multiple ESXi metrics (Usage, Core Utilization, Utilization/Thread Utilization) showing different values simultaneously
- Whether an ESXi host has capacity remaining to deploy more VMs
- The hint or context says "think ESXi capacity, not VM performance"
- Comparing Usage vs Core Utilization vs Thread Utilization at the ESXi level
- Calculating or comparing ESXi host total CPU capacity in GHz

---

#### The three ESXi CPU utilization metrics

| Metric | vSphere counter | What it measures | HT penalty? | Turbo effect? | Sensitivity |
|--------|----------------|-----------------|-------------|---------------|-------------|
| **Usage (%)** | `cpu.usage.average` | Cycles completed vs nominal frequency (NHCC hardware counter) | Yes — HT sharing penalizes to 62.5% per thread | Yes — inflates above 100% with Turbo; deflates with power-saving | **Highest** |
| **Core Utilization (%)** | `cpu.coreUtilization.average` | Whether a physical core is active — reports 100% if **either or both** threads run | Partial — doesn't reflect the 62.5% per-thread penalty | No | Medium |
| **Thread Utilization (%)** | `cpu.utilization.average` | Fraction of physical threads that are unhalted — binary per thread | No — treats each thread as independent, full 100% | No | **Lowest** |

**Sensitivity order: Usage > Core Utilization > Thread Utilization**

All three values are simultaneously correct — they measure different things and answer different questions.

---

#### Which metric to use — by purpose

**Capacity consumption: "is this ESXi host full?"**
→ **Usage (%)**
- Usage = 100% means the host has consumed its full nominal CPU budget (base frequency × core count)
- In older vCenter, Usage was **capped at 100%** — hitting that cap is the definitive "no more capacity" signal
- In newer vCenter / Aria Operations 8.18+, Usage can exceed 100% due to Turbo Boost — this is normal and desirable
- When asked "what is the ESXi true utilisation" from a capacity standpoint: **Usage is the answer**

**Physical capacity planning: "when do I need more hosts?"**
→ **Core Utilization (%) + Thread Utilization (%) together**
- Book rule: *"If Core Utilization is not yet 100% or Thread Utilization is not yet 50%, there is still physical capacity available."*
- Recommended threshold: keep Thread Utilization ≤ 80–90% per ESXi host (lower at cluster level to preserve HA reserve)
- Core Utilization = 100%: all cores have at least one active thread
- Thread Utilization = 50%: the capacity planning threshold — at this point, on average, half of all HT threads are active

**VM performance throughput: "how fast are VMs running?"**
→ **Usage (MHz)** — not %
- MHz captures actual CPU work per second, accounting for frequency variation over time
- This is the performance complement; it tells you throughput delivered, not how full the host is

---

#### Why Usage beats Thread Utilization as the "true utilization" capacity signal

Thread Utilization is the most basic counter — the ESXi equivalent of VM CPU Run. It tracks only **time** (thread unhalted or not). It ignores two factors that Usage accounts for:

1. **HT efficiency penalty** — when two threads share a core, each gets only 62.5% throughput. Usage reflects this reduction; Thread Utilization does not.
2. **CPU clock speed** — Usage is based on the NHCC hardware counter (Non-Halted Core Cycles), so Turbo Boost and power-saving both affect it. Thread Utilization never reflects speed.

Result: on a host where all cores have both threads running, Thread Utilization reads 50% while Usage reads ~100% (or above). Thread Utilization "under-reports" because it counts threads as fully independent and speed-agnostic.

> "Thread Utilization is not considering CPU Frequency nor HT." — book, ESXi > Consumption > Thread Utilization

---

#### Reading the 3-metric chart — the common quiz pattern

When you see three lines on an ESXi chart with values like:
- Blue (Usage): ~100%
- Green (Core Utilization): ~70%
- Black (Thread Utilization): ~50%

All three are correct simultaneously. Interpretation:
- **Usage = 100%**: the host has consumed its nominal capacity budget → **at capacity**
- **Core Utilization = 70%**: 70% of cores have at least one thread running; 30% of cores are fully idle
- **Thread Utilization = 50%**: half of all physical threads are active

The hint *"think ESXi capacity, not VM performance"* points to **Usage** as the answer for capacity questions. The 100% cap on the blue line is the signal — not the lower, more conservative thread-counting metric.

---

#### HT balance quiz: Thread Util = Core Util = 50%

**How Thread Util is calculated at ESXi level:** It is the **average of all individual HT thread utilizations** (each thread measured independently, 0–100%). This is NOT simply "fraction of active threads."

**When Thread Util = Core Util = 50%:**

The book states: *"Core Utilization (%) will tend to be consistently higher than Thread Utilization."* Equal values are the exception — they occur when HT sharing is absent (no-HT host, or ideal scheduling where no core runs both threads simultaneously).

- **Scenario B (ideal):** Each active core runs exactly one thread. No HT throughput penalty. The metrics converge toward equality in this case — as seen in the book's no-HT example where Core Util = Thread Util identically.
- The combination is **ambiguous** — without additional context you cannot confirm which specific scheduling arrangement produced it.

**Answer for the quiz:** Both **B** (ideal — 1 thread per core) AND **C** (ambiguous — not enough info) are correct. Equal metrics at 50% is consistent with ideal single-threading, but cannot be confirmed from numbers alone.

See: CPU > ESXi > Consumption Metrics > Thread Utilization > Core vs Thread

---

#### ESXi total CPU capacity — the formula

**vSphere formula: `Nominal Speed × Physical Cores`**

HyperThreading and Turbo Boost are both **excluded** from the capacity baseline.
> *"vSphere calculates CPU capacity as base frequency × number of cores, explicitly excluding turbo boost and hyperthreading."* — book, ESXi > Usage

Examples:
- 8 cores × 3.0 GHz = **24 GHz**
- 12 cores × 2.0 GHz = **24 GHz** ← same capacity despite different specs

**Critical insight — do not assume different specs mean different capacity:**
Two hosts with different core counts and speeds can have identical total capacity if `Cores × Nominal` is the same. If the calculation gives the same answer for two hosts, that **is** the correct answer — do not change it because the specs look different. Always calculate, never assume. The surprising result (same capacity despite different specs) is often the intended teaching point.

**The book's 1.25× HT factor** (`Cores × Nominal × 1.25`) is used when discussing the *true* throughput benefit of HT-enabled hosts, but vSphere UI reports capacity as `Nominal × Cores` only. Use the simpler formula unless the question explicitly asks about HT-adjusted capacity.

---

#### CPU reservation is capped at nominal capacity — Turbo cannot be reserved

**Key fact:** The total CPU reservation at ESXi level is capped at `Nominal Speed × Physical Cores` — the same formula as total capacity. This means you **cannot** reserve Turbo Boost capacity.

> *"Total capacity is based on base clock speed."* — book, CPU > VM > Consumption Metrics

Because vSphere defines total capacity as `Nominal × Cores`, and reservation cannot exceed total capacity, the maximum reservable amount equals the nominal baseline only. Turbo Boost pushes actual throughput *above* this nominal baseline, but that headroom above nominal cannot be reserved.

Consequence: even if all VMs run at full Turbo, the total possible throughput exceeds the total that can be reserved. This is correct and expected behavior — it is not a bug or misconfiguration. Any statement saying "reservation is capped at nominal, so Turbo capacity cannot be fully reserved" is **correct**.
