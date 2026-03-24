### Skill: Guest OS CPU Behaviour

**When to activate:** Questions about Guest OS CPU awareness, Run Queue, Context Switch, or what Windows/Linux can/cannot see in a virtual environment.

---

#### Guest OS HT awareness — the book is explicit

> *"It's unaware of the hyper-threading, because the information is not being supplied by ESXi VMM module."* — CPU chapter, line 26

> *"VM takes the consumer view... It sees 2 virtual CPUs, unaware of HT."* — CPU chapter, line 78

**Guest OS does NOT know it is running on hyperthreaded hardware.** ESXi presents virtual CPUs to the Guest OS as independent logical processors. The Guest OS schedules its threads against vCPUs, not against physical cores or HT threads. It cannot tell whether two of its vCPUs share a physical core.

Any quiz option saying "Guest OS IS aware of HT and will schedule accordingly" is **wrong** per the book.

---

#### Run Queue and Context Switch — do they impact performance?

Yes, both impact application performance:

- **Run Queue:** Tracks processes waiting to execute. A sustained queue longer than 2–3 per vCPU means processes are delayed — the Guest OS cannot serve all requests in time. The book includes this in the Guest OS CPU sizing formula as an additional vCPU demand signal.

- **Context Switch:** Expensive operation — the CPU must save/restore state, flush TLB, and warm instruction caches. The book notes context switches represent wasted CPU cycles: *"the CPU can complete many instructions within the time taken to switch context."* High context switch rates degrade throughput even at moderate utilization.

Both are **internal Guest OS operations** with no direct corresponding vSphere counter (hence "None" in the VM metrics mapping table). That doesn't mean they don't affect performance — it means you must use Guest OS tools (Windows Task Manager/PerfMon, Linux top/vmstat) to see them.

---

#### Co-stop and Other Wait — are they "complete stops"?

Yes. From the book:

> *"Co-stop is a different state than Ready because the cause is different. The effect to the VM is the same. A pause is a pause. The Guest OS is unaware of the cause and experiences the same contention."* — CPU chapter

> *"Guest OS isn't aware of both Other Wait and Swap Wait. Just like other type of contention, it experiences freeze."* — CPU chapter

Ready, Co-stop, and Other Wait ALL cause the vCPU to completely stop. The Guest OS cannot distinguish between them — it just experiences frozen time.

See: CPU > VM > Contention Metrics > Ready, Co-stop, Other Wait
