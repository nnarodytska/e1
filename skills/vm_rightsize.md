### Skill: VM CPU Right-Sizing

**When to activate:** When the question involves:
- Which metric to use for VM CPU right-sizing
- Guest OS sizing vs VM Footprint sizing
- Whether Demand, Usage, Net Run, or Run is the correct right-sizing metric
- Why CPU Usage or Demand is not suitable for right-sizing

---

#### Two distinct right-sizing formulas

| Purpose | Method | Metrics to use |
|---------|--------|----------------|
| **Guest OS Sizing** | Size what Windows/Linux actually needs | CPU Run (or Net Run), Guest OS Run Queue |
| **VM Footprint** | Size the VM's claim on ESXi infrastructure | CPU Used + Overlap + Ready + Co-stop + Other Wait + Swap Wait |

The hint "size the Guest OS, not the VM" → use the **Guest OS Sizing** formula → use **Net Run (CPU Run − Overlap)**.

---

#### Why Demand and Usage are EXCLUDED for Guest OS sizing

The book is explicit (Consumer chapter, CPU Sizing > Exclusion table):

> *"The VM CPU Demand and VM CPU Usage metrics are not suitable as their values are affected by CPU Frequency and HT."*

> *"The VM CPU Used, Demand, Usage counter include system time at VM level, hence they are not appropriate."*

Specifically excluded:
- **HT penalty** — Guest OS is unaware of HT. When running on a shared core, Windows/Linux just runs slower (37.5% throughput drop). Demand and Usage reflect this speed change; the Guest OS doesn't know it happened.
- **CPU Frequency** — Turbo Boost inflates Demand/Usage. A VM running at 125% Turbo will show higher Demand than it actually needs. This caused a real example: 16 vCPU at 90% usage inflated to 18 vCPU due to Turbo, then bumped to 20 vCPU → NUMA effect.
- **System/overhead time** — VM overhead (MKS, VMX) is in Demand/Used. Guest OS does not use these cycles.

---

#### Why Net Run IS suitable for Guest OS sizing

`Net Run = CPU Run − Overlap`

- **CPU Run**: time the vCPU is executing Guest OS instructions (unhalted, on a physical thread). Not aware of CPU frequency or HT speed — just time.
- **Overlap subtracted**: removes the portion where the vCPU ran but was interrupted by the kernel (the kernel "borrowed" those cycles back). This gives the net time the Guest OS actually ran.
- Result: frequency-agnostic, HT-agnostic count of vCPU execution time — exactly what Guest OS sizing needs.

Book (CPU chapter, Thread Utilization section): *"Net Run = Run – Overlap... it is suitable as input to size the Guest OS."*

---

#### Guest OS CPU sizing formula (from the book)

```
Guest OS CPU Needed = Configured vCPU − Idle vCPU + CPU Run Queue factor
```

Where:
- `Idle vCPU` = vCPUs spending time in the idle state (not running, not contended — just idle). Derived from CPU Run: Idle = Configured − Run-based active equivalent.
- `CPU Run Queue factor` = additional vCPUs needed to drain the Guest OS process backlog (Run Queue / acceptable threshold per vCPU)
- Result is in **vCPU count**, then rounded to NUMA-aligned even numbers
- Contention time (Ready, Co-stop, Other Wait, Swap Wait) is *included* because the Guest OS was trying to run during those periods

See: Consumer chapter > Capacity > VM > Guest OS Sizing > CPU Sizing

---

#### CPU Reclamation — common quiz traps

**"Reclaiming vCPU frees allocation in GHz"** — Correct. In the allocation model, reclaimed vCPU × nominal frequency = freed allocation. For example: reclaim 20 vCPU on a 2 GHz ESXi = 40 GHz freed in the allocation model. This accounting statement is **correct**.

**"But freed allocation ≠ guaranteed active capacity"** — Also correct. An idle vCPU consumes near-zero physical threads. The freed allocation reduces the *allocation footprint*, but you cannot assume those freed slots can directly support a heavily active new VM without checking physical thread headroom. Idle CPU ≠ active CPU capacity.

**These two statements are simultaneously correct and complementary, not contradictory.** B (allocation freed in GHz) and C (caveat: not the same as active capacity) both describe different aspects of the same reclamation. Accept both.

**"Power off also frees memory"** — Correct and valid. Powering off a VM releases both its CPU allocation AND its physical memory pages. This is a legitimate reclamation action. Don't exclude it just because right-sizing (vCPU reduction) is the less disruptive alternative.

**Conservative reclamation** — When a VM is idle with no metrics to guide the exact reduction, the correct first step is to reclaim **up to 50%** of the configured vCPU count. The reasoning: idle means the VM is using less than half its configured vCPUs, so reducing by up to half is the safe conservative approach before doing deeper analysis. This is not just defensible — it is the right call.

See: Consumer chapter > Capacity > VM Footprint > CPU Sizing
