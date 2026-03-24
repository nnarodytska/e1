### Skill: Performance vs Capacity Distinction

**When to activate:** When comparing performance management vs capacity management, questions about utilization and throughput, or "choose all correct" questions about what high/low utilization means.

---

#### Core distinction

| | Performance | Capacity |
|---|---|---|
| Measured at | Consumer (VM) — contention metrics | Provider (ESXi/Cluster) — utilization metrics |
| High utilization means | ??? — depends on queue | Efficient use of investment (good!) |
| Low utilization means | May signal a bottleneck elsewhere | Wastage / over-provisioned |
| 100% utilization | Risky — creates contention risk | Only bad if it exceeds **Usable Capacity** |
| Key metric | CPU Ready, Co-stop, Memory Latency | Usage %, Thread Util, Consumed |

---

#### Why statement A ("high utilization = perfect performance, equals more throughput") is WRONG

Utilization ≠ throughput. The book shows clusters at **50% utilization** where VMs had **50%+ CPU Ready** — meaning the cluster was half-empty yet VMs were being starved. Conversely, a fully utilized cluster with no contention delivers good throughput.

The key flaw: "higher utilization equals more throughput" implies utilization and throughput correlate, which the book explicitly disproves. You must look at contention metrics (Ready, Co-stop), not utilization, to judge performance.

> "There is a common misconception that you cannot have performance issue when cluster has low utilization." — Provider > Performance > Utilization vs Contention

**Statement A is wrong** — the correlation between utilization and throughput does not hold.

---

#### Why statement B ("100% utilization is bad news for capacity") is WRONG

The book says high utilization is **desirable** from a capacity/economics standpoint:
> *"You want to maximize its use, ideally at 100%. After all, you pay for the whole box."*

B frames high utilization as "bad news" — this inverts the book's position. Capacity is only a concern when utilization breaches **Usable Capacity** (Total − Hypervisor − Buffer). Raw 100% utilization before that threshold = efficient use, not bad news.

**Statement B is wrong** — high utilization is the goal; only Usable Capacity breach triggers action.

---

#### The two correct insights

**C — Low utilization may mean bad news for performance.** A resource bottleneck (storage, network, limit) can cause artificially low CPU utilization. Low utilization ≠ healthy VMs. Always check contention metrics alongside consumption.

**D — ESXi capacity ≠ VM performance.** Capacity is a provider-layer metric (how full is the ESXi?). Performance is a consumer-layer metric (are VMs getting what they asked for?). A cluster at 50% utilization can have VMs with 50% CPU Ready — shown in real book examples.

**See:** Provider > Cluster > Performance > Utilization vs Contention
