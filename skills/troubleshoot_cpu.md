### Skill: CPU Performance Troubleshooting Wizard

**Diagram source:** `diagrams/vSphere Performance Troubleshooting.drawio` — page "VM CPU"

**When to activate:** When the user describes a VM CPU performance problem, reports CPU contention symptoms (slow VM, high CPU Ready, co-stop, spin lock), or uploads a CPU metrics screenshot. Also activate when diagnosing Guest OS CPU issues (run queue, context switch, interrupt time).

**How to use this diagram:**
- Follow arrows in the direction of "COULD BE CAUSED BY OR IMPACTED BY"
- Start from the symptom (contention metric) and trace outward to find root causes
- The diagram has two realms separated by a horizontal line:
  - **Guest OS Realm** (above the line): Queue, Context Switch, Interrupt Time, Spin Lock, Thread Migration, Power Management
  - **VM and ESXi Realm** (below the line): all VM and ESXi metrics

> Ignore `CPU Latency` counter — that is for the VMkernel CPU scheduler, not human operators.
> Do not pin VMs to ESXi hosts.

---

**Starting points — VM CPU contention metrics (red nodes):**

```
VM CPU "contention"
├── CPU Ready
│   ├── VM Limit → Resource Pool (Limit | Share | Rsvp) → ESXi CPU Reservation
│   │                                                    → ESXi CPU Overcommit
│   ├── VM Shares → Resource Pool (Limit | Share | Rsvp) → Configured CPU
│   ├── Configured CPU → vNUMA → ESXi CPU Utilization → Hyperthreading
│   │                         → Physical NUMA ↔ ESXi CPU Usage
│   ├── Usage Disparity [green: consumption indicator — shows vCPU usage imbalance across sockets/cores]
│   │   → VM Shares / Configured CPU / ESXi CPU Utilization
│   ├── vMotion [green: consumption event — transient Ready spike during migration]
│   │   → VM-Host Affinity / Resource Pool
│   ├── Power Management → VMware Tools → VM Hardware / ESXi Power Management
│   │                                                  → BIOS Power Management
│   ├── ESXi CPU Utilization / ESXi CPU Overcommit
│   └── ↔ CPU Co-stop (bidirectional impact)
│
├── CPU Co-stop
│   ├── VM Shares
│   ├── Usage Disparity → Configured CPU → vNUMA → ESXi CPU Utilization
│   ├── Configured CPU → vNUMA
│   ├── Thread Migration (impact) → Configured CPU / ESXi CPU Utilization
│   └── ↔ CPU Ready (bidirectional)
│
├── CPU Other Wait
│   ├── Memory Contention → ESXi Memory Consumed → Physical NUMA / ESXi CPU Utilization
│   │                    → Configured Memory → vNUMA
│   │                    → See Memory Troubleshooting Flow
│   ├── Disk Latency → See Storage Troubleshooting Flow
│   └── Snapshot → See Storage Troubleshooting Flow
│
└── CPU Overlap
    ├── Disk IOPS → See Storage Troubleshooting Flow / VMkernel CPU Usage
    ├── Network Packets/s → See Network Troubleshooting Flow / VMkernel CPU Usage
    ├── ESXi CPU Utilization
    └── VMkernel CPU Usage → ESXi CPU Usage → ESXi Power Management → BIOS Power Management
                          → vSAN, NSX, VR
```

**Guest OS realm (above the horizontal line):**

```
Guest OS Realm
├── Queue (CPU Run Queue)
│   ├── Process Priority
│   ├── Run (not 1:1 relationship)
│   │   ├── Context Switch (not 1:1)
│   │   ├── Spin Lock (high run → spin lock)
│   │   ├── Thread Migration (cause)
│   │   ├── Power Management (impacted by)
│   │   └── Container Share → Container Control Group
│   └── Interrupt Time
│
├── Context Switch (standalone contention metric, not 1:1 with Queue)
│
├── Interrupt Time
│
├── Thread Migration
│   ├── NUMA Migration (impact)
│   ├── Configured CPU (impact)
│   └── Memory Consumed (impact)
│
├── Spin Lock (from high Run queue)
│
└── Power Management
    ├── VMware Tools (ensure compatibility → ESXi Power Management)
    ├── ESXi Power Management → BIOS Power Management
    └── Windows State Transitions
        └── Windows DPC
```

**Key root causes (terminal nodes):**
- ESXi CPU Reservation
- ESXi CPU Overcommit
- Hyperthreading
- Physical NUMA / vNUMA misconfiguration
- ESXi Power Management / BIOS Power Management
- VM Hardware version
- VM-Host Affinity / CPU Pinning (avoid pinning)
- Guest OS Spin Lock
- vSAN, NSX, VR overhead
- Container Control Group / Container Share

**Consumption metrics to check (green nodes):**
- ESXi CPU Utilization, ESXi CPU Usage
- VMkernel CPU Usage
- ESXi Memory Consumed
- Usage Disparity (imbalance indicator — not a root cause itself)
- vMotion (transient event — not a root cause itself)
- ESXi Drivers & Firmware (green: ESXi-layer health indicator — outdated drivers can cause erratic CPU behaviour; check version/compatibility)

**Context / settings (grey nodes):**
- VM Shares, VM Limit, Configured CPU, Configured Memory
- Resource Pool (Limit | Share | Rsvp)
- vNUMA, Physical NUMA, VM Hardware, VMware Tools
- ESXi Power Management, BIOS Power Management
- VM-Host Affinity, CPU Pinning
- Container Control Group, Container Share
- Windows DPC, Windows State Transitions, Process Priority
