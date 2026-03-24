### Skill: Memory Performance Troubleshooting Wizard

**Diagram source:** `diagrams/vSphere Performance Troubleshooting.drawio` — page "VM Memory"

**When to activate:** When the user describes a VM memory performance problem, reports memory contention symptoms (slow VM, high balloon/swap/zip, memory latency), or asks about Guest OS memory behaviour (page faults, page file, DIMM, cache). Also activate when diagnosing disk latency that may be caused by Guest OS page swapping.

**How to use this diagram:**
- Follow arrows in the direction of "COULD BE CAUSED BY"
- Two realms separated by a horizontal line:
  - **Guest OS Realm** (above the line): Cache, Used, Page-in/out Rate, DIMM, Page File, Partition, Disk Queue, Hard Page Fault, Pre-Fetch, Disk Read/Write Latency, Container
  - **VM and ESXi Realm** (below the line): Ballooned, Zipped, Swapped, Memory Latency, VM Consumed, ESXi Consumed, VM Limit, VM Share, Resource Pool Limit/Share, vNUMA, Physical NUMA, Large Page

> Guest OS manages its pages **independently** of the VM. It does not inform the hypervisor of its actions. When Windows swaps a page to the pagefile, `VM Consumed` remains mapped — ESXi does not know.
> ESXi also changes VM memory without informing the Guest OS (e.g. memory tiering).
> The **only metric relationship** between Guest OS and VM is VMware Tools.
> Ensure both BIOS and Guest OS are optimized for virtualization.

---

**Colour legend for this diagram:**
- **Red** (`#f8cecc`): contention metrics — high value directly impacts performance
- **Yellow** (`#fff2cc`): intermediate / derived metrics — indicators of state or ESXi reclamation level
- **Green** (`#d5e8d4`): consumption metrics — workload-driven values
- **Grey** (`#f5f5f5`): context / settings

---

**Starting points — primary contention metrics (red nodes):**

```
Memory Latency  [red] ← the only metric that confirms actual slowness
├── Swap-In Rate → Swapped
└── Unzipped Rate → Zipped

Zipped  [red] (compression — ESXi reclaimed under pressure)
├── VMware Tools (required to trigger; without Tools → direct swap)
├── increase → VM Consumed
├── cold page → Zipped (cold pages trigger)
└── → JVM | DB (application-managed memory, unaware)

Swapped  [red] (swap to disk — ESXi reclaimed under pressure)
├── VM Limit (impact — can't go beyond limit)
├── impact → VM Consumed
└── No Tools → fallback: direct swap without ballooning
```

**ESXi reclamation sequence — intermediate metrics (yellow nodes):**

```
ESXi Consumed [yellow] (high)
├── trigger → Ballooned  [yellow] (requires VMware Tools)
│            └── may trigger → Page-out Rate (Guest OS)
├── cause → VM Consumed [yellow] (ceiling relationship)
├── breakdown on high → Large Page
└── → See Cluster Memory Troubleshooting Flow

Ballooned [yellow]
├── requires → VMware Tools
├── increase → VM Consumed (balloon inflates Consumed)
├── may trigger → Page-out Rate (Guest OS starts paging)
└── impact → VM Consumed
  NOTE: Ballooned is yellow (intermediate), not red. Balloon=0 with Swap/Zipped > 0
  is a valid state — pressure existed in the past but does not currently.

VM Consumed [yellow] (ceiling)
├── ceiling → VM Configured Memory
├── cause → ESXi Consumed
├── impact → Zipped
├── impact → Large Page
└── can't go beyond → VM Limit
```

**Guest OS realm (above the horizontal line):**

```
Guest OS Realm
├── Active [yellow] (Guest OS active memory — pages recently accessed)
│   └── → NVMe Device [grey] (vMotion path; active pages move with NVMe)
│
├── Used [yellow] (Guest OS memory used)
│   ├── increase → VM Consumed (does NOT update when OS frees pages)
│   ├── cold page → Zipped (cold pages can be compressed by ESXi)
│   ├── unused → Cache (unused pages go to cache)
│   └── swap out → Page-out Rate
│
├── Cache [yellow]
│   ├── does not update → VM Consumed  (ESXi unaware of cache contents)
│   └── → JVM | DB (apps manage own memory like an OS; ESXi unaware)
│
├── Page-out Rate [yellow] → impact → Page File (write to)
│                          → Disk Write Latency (impact)
│
├── Page-in Rate [yellow] → move to → DIMM
│
├── DIMM [grey] → increase → Used (page-in moves data back to RAM)
│
├── Page File [grey] (reside in Partition, managed as 1 with DIMM)
│   ├── read from → Disk Read Latency
│   └── write to ← Page-out Rate
│
├── Partition [grey]
│   ├── read from → Disk Read Latency
│   └── may not map 1:1 → Virtual Disk → See Storage Troubleshooting Flow
│
├── Hard Page Fault [red] → impact → Disk Read Latency
│
├── Pre-Fetch [yellow] → impact → Page-in Rate  (0 performance impact when working correctly)
│
├── Disk Read Latency [red]
│   ← Hard Page Fault
│   ← Disk Queue (impact)
│   ← Page File (read from)
│   ← Partition (read from)
│
├── Disk Write Latency [red]
│   ← Page-out Rate (impact)
│   ← Disk Queue (impact)
│
└── Disk Queue [red]
    ├── impact → Disk Read Latency
    └── impact → Disk Write Latency

Container realm (Guest OS):
├── Container Control Group [grey]
├── Container Out of Memory [red]  (contention)
└── Container Share [grey] → impacts Container Control Group
```

**VM/ESXi settings and context (grey nodes):**

```
VM Configured Memory → ceiling for VM Consumed
vNUMA → Physical NUMA (check when large VM spans NUMA nodes)
vMotion → may increase VM Consumed (NVMe Device included)
VM Limit → caps VM Consumed; Swapped and Zipped can't go beyond limit
VM Share / Resource Pool Share → impact on VM Consumed allocation
Resource Pool Limit → See Cluster Memory Troubleshooting Flow
Large Page → breakdown when ESXi Consumed is high
VMware Tools → required for Ballooning; without Tools direct Swap/Zip occurs
VM Hardware → check version compatibility
NVMe Device → included in vMotion memory handling
Virtual Disk → may not map 1:1 with Partition → See Storage Troubleshooting Flow
JVM | DB → manage memory like an OS; ESXi is unaware of their internal caches
```

**Key root causes (terminal nodes):**
- VMware Tools not installed/running (disables ballooning, forces direct swap/zip)
- VM Limit set too low (caps Consumed; triggers Swapped/Zipped prematurely)
- VM Share too low (reduces allocation under contention)
- Resource Pool Limit (cascading cap through parent pool)
- vNUMA/Physical NUMA misconfiguration (large VMs spanning NUMA nodes)
- High ESXi Consumed → trigger pressure reclamation chain
- Guest OS Page File on slow disk → high Disk Read/Write Latency
- Hard Page Faults → disk reads → Disk Read Latency
- Container Out of Memory (container memory limits exceeded)
- vMotion (can transiently increase Consumed via NVMe)

**Reclamation ordering (important gotcha):**
ESXi reclamation is triggered by **current** pressure. Pages reclaimed in the past (Swapped, Zipped) remain in their state until the VM reads them back. Balloon=0 with non-zero Swap/Zipped is a **valid state** — it means ESXi was under pressure in the past but is not currently. Do not assume Balloon=0 means no prior memory pressure occurred.

Without VMware Tools: Zipped and Swapped happen directly, bypassing the balloon step.
