### Skill: Troubleshooting Wizard

**When to activate:** Automatically when the user describes a performance problem, reports symptoms (slow VM, high latency, contention), or asks for help diagnosing an issue. Also activate when the user uploads a screenshot showing problematic metric values.

Run an interactive guided diagnosis using the decision trees below. These are the EXACT troubleshooting flows from the official vSphere CPU Performance Troubleshooting diagrams.

**How to run the wizard:**
1. Identify which tree to use (VM, Guest OS, or Cluster) based on the symptom
2. Start at the root node and ask the user to check the first branching metric
3. At each step, ask for 1-2 specific metric values, then follow the tree branch
4. Keep each step SHORT — 2-3 sentences + what to check next
5. End with: root cause, evidence, recommended action
6. If a branch says "See Storage/Memory/Network Flow", tell the user the problem is in that domain

**DECISION TREE 1: VM CPU Troubleshooting**

Root: VM CPU "contention" — check these 4 primary metrics first:

```
VM CPU "contention"
├── CPU Ready
│   ├── VM Limit → Resource Pool (Limit|Share|Rsvp) → ESXi CPU Reservation / ESXi CPU Overcommit
│   ├── VM Shares → Resource Pool (Limit|Share|Rsvp) → Configured CPU
│   ├── Configured CPU → vNUMA → ESXi CPU Utilization → Hyperthreading
│   │                        └── Physical NUMA ↔ ESXi CPU Usage
│   ├── Usage Disparity → VM Shares / Configured CPU / ESXi CPU Utilization
│   ├── vMotion → Resource Pool / VM-Host Affinity
│   ├── Guest OS Power Management → VMware Tools → VM Hardware / ESXi Power Management
│   ├── ESXi CPU Utilization / ESXi CPU Overcommit
│   └── ↔ CPU Co-stop (bidirectional)
├── CPU Co-stop
│   ├── VM Shares
│   ├── Usage Disparity → Configured CPU → vNUMA → ESXi CPU Utilization
│   ├── Configured CPU → vNUMA
│   ├── Guest OS CPU Ping Pong → Configured CPU / Configured Memory → vNUMA
│   └── ↔ CPU Ready (bidirectional)
├── CPU Other Wait
│   ├── Memory Contention → ESXi Memory Consumed → Physical NUMA / ESXi CPU Utilization
│   │                   └── Configured Memory → vNUMA
│   │                   └── → See Memory Troubleshooting Flow
│   ├── Snapshot → See Storage Troubleshooting Flow
│   └── Disk Latency → See Storage Troubleshooting Flow
└── CPU Overlap
    ├── Disk IOPS → See Storage Flow / VMkernel CPU Usage
    ├── Network Packets/s → See Network Flow / VMkernel CPU Usage
    ├── ESXi CPU Utilization
    └── VMkernel CPU Usage → ESXi CPU Usage → ESXi Power Management → BIOS Power Management
                         └── vSAN, NSX, VR
```

Terminal nodes (root causes to check): ESXi CPU Reservation, ESXi CPU Overcommit, Hyperthreading, ESXi/BIOS Power Management, VM Hardware version, VM-Host Affinity, CPU Pinning, Guest OS Spin Lock, ESXi Drivers & Firmware, vSAN/NSX/VR overhead.

**DECISION TREE 2: Guest OS + VM (extends Tree 1)**

Adds Guest OS realm above the VM layer:
```
Guest OS Realm:
├── Guest OS CPU Context Switch (standalone indicator)
├── Guest OS CPU Queue → Guest OS CPU Priority
├── Guest OS Spin Lock (linked from VM realm)
└── Guest OS Power Management → VMware Tools → VM Hardware / ESXi Power Management
```

**DECISION TREE 3: Cluster Troubleshooting**

Split by scope of impact:
```
Narrow Problem (few VMs affected):
├── vMotion → DRS Settings / Cascading Resource Pools → Cluster Reservation
├── HA Event → Host-VM Affinity → vMotion / Cascading Resource Pools
├── ESXi Imbalance → Cluster Reservation / DRS Settings / Inconsistent Settings
│                └── Cascading Resource Pools / Monster VM → Physical NUMA
├── Share / Limit → Cascading Resource Pools
└── Port Group

Wide Problem (many VMs affected):
├── ESXi Utilization → vSAN/NSX/VR / ESXi Power Management → BIOS Power Management
│                  └── ESXi Overcommit → Cluster Overcommit
│                  └── Monster VM → Physical NUMA / VAAI
├── ESXi Storage Issue → See Storage Flow
└── ESXi Network Issue → See Network Flow
```
