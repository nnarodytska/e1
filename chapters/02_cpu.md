# CPU


## Architecture

What used to be Windows or Linux running on a server has transformed into Guest OS  VM  ESXi. There 3 distinct layers resulted in complexity documented in Part 2 Chapter 1. This is not as complex as memory, where you have 4 layers as process running inside a Guest OS represents another layer.
The following infographic shows how the nature of CPU metrics changes as a result of virtualization.

[Image: The image is an architectural diagram showing the layered hierarchy of CPU metric measurement in a VMware vSphere environment, with four stacked horizontal bars labeled **Guest OS CPU 1**, **VM-1 vCPU-1**, **VM-1**, and **VM-X vCPU-Y**. It visually illustrates the three key measurement complexities described in the accompanying text: Guest OS and VMkernel independently calculating CPU metrics, VM-level overhead (MKS, VMX, VMM worlds) not attributed to individual vCPUs, and multiple VMs competing on the same ESXi physical thread. The diagram contextualizes why CPU metrics differ across layers and cannot be directly compared between Guest OS and hypervisor perspectives.]

Specifically for CPU, we need to be aware of dynamic metric. This means their values fluctuates depending on CPU clock speed and HT effect. As a result, the values are harder to figure out due to lack of observability on the fluctuation. This is not an issue if the range is negligible. It is not. For example, HT can increase the value of CPU Latency anywhere from 0% to 37.5%.

### Guest OS vs VM

CPU metrics for a VM differ greatly from those in the Guest OS. For example, vCenter provides 5 metrics to account for the utilization of VM CPU, yet none directly maps to Windows/Linux CPU utilization.
The following diagram shows some of the differences.

[Image: The diagram categorizes CPU performance metrics into three layers: **Guest OS-level counters** (Context Switch, Run Queue, Utilization, IO Wait — invisible to the VM), **VM-level counters caused by the VM** (Run, Idle), and **VM-level counters caused by the Hypervisor** (System, Overlap, Ready, Co-Stop, VMX, Other Wait — invisible to the Guest OS). It illustrates the observability gap between the Guest OS and ESXi hypervisor layers, where neither has full visibility into the other's metrics. This directly supports the surrounding text's argument that vCenter VM CPU metrics do not map directly to Guest OS metrics (e.g., Windows/Linux utilization), requiring practitioners to use layer-appropriate metrics for accurate performance analysis.]

When the kernel de-schedules a VM to process something else (e.g. other VM, kernel interrupt) on the same physical thread or core, the Guest OS does not know why it is interrupted. In fact, it experiences frozen time for that particular vCPU running on the physical core. Time jumps when it’s scheduled again. Because of this unique visibility, it’s important to use the correct metrics at the correct layers.
On the other hand, ESXi cannot see how the Guest OS schedules its processes. ESXi can only see what’s being sent out by the Guest.
Difference in the CPU Utilization metrics:

| Guest OS | Depending on the version of Guest OS, some may not be aware of CPU scaling. The real time frequency has to be obtained from the BIOS or VMM layer. I’m unsure how frequent this gets updated by ESXi to the VM, as it varies per core and over time. |
| --- | --- |
| Guest OS | It’s unaware of the hyper-threading, because the information is not being supplied by ESXi VMM module. |
| VM | When the vCPU shares a physical core, the CPU Usage will drop by 37.5%. |
| VM | Includes IO processing done on behalf of the hypervisor. In heavy databases or NSX Edge, this is significant. This increases VM CPU Usage. |

Both layers need to be monitored, as each measure different performance problems. Hence it’s imperative to install VMware Tools. It reports the statistics about Guest OS to the ESXi host every 20 seconds by default.
The following example summarizes that mapping between Guest and VM is not possible.

| Type | Windows Metric | VM Metric |
| --- | --- | --- |
| Contention | Run Queue | None.  All these are internal operations of Windows or Linux. |
| Contention | DPC Time | None.  All these are internal operations of Windows or Linux. |
| Contention | Context Switch | None.  All these are internal operations of Windows or Linux. |
| Contention | C1 Time C2 Time C3 Time | None. ESXi does not break down per VM as it focuses on the physical core. |
| Contention | None | CPU Ready CPU Co-Stop CPU System |
| Utilization | Usage | Run – Overlap – VMX – System. In Linux, the usage counters shown by the commands top, htop, or vmstat measures the time spent. It does not include the speed during the run. |

I put Linux separately as Windows and Linux have different approaches. The metrics are:

| User | This means non kernel. Applications typically run here. |
| --- | --- |
| System | This is the kernel or privileged ring, where core operating systems function run. |
| Idle | Not running. This should correlate with the CPU run queue. |
| Wait | The time spent waiting for IO (disk or network) |
| Stolen | I think this is only applicable in virtual machine, not physical. This is the time it’s frozen because underlying hypervisor does not have physical thread to run the VM vCPU. |

The following diagram shows the difference between Guest OS and VM.

[Image: The table maps the relationship between **Guest OS states** and **VM states** from CPU[0]'s perspective, showing how the same condition appears differently at each layer. Key mappings include: Guest OS "Run (productive/Context X)" = VM "Run"; Guest OS "Run (wants to run)" = VM "Ready" or "Co-Stop"; and Guest OS "Wait" = VM either "Run (Guest OS IO)" or "Wait (VM IO)" — illustrating the **Double IO Processing** phenomenon. This demonstrates that VM-level metrics do not directly correspond to Guest OS metrics, as the hypervisor layer introduces additional states (notably Co-Stop and the IO processing split) that have no direct Guest OS equivalent.]

We will explain the above diagram after we cover the counters.

### ESXi ≠ VM + Kernel

Let’s use an example to drive the point. Can you explain the following?

[Image: ## Image Description

The chart displays **VM CPU Usage (GHz)** versus **Total Capacity (GHz)** for ESXi host `wdc-10-r13esx05.oc.vmware.com` from January 5–13. The key anomaly occurs on **Tuesday, Jan 9 at 10:30–10:59 AM**, where VM CPU Usage spikes to **159.03 GHz** — significantly exceeding the host's Total Capacity flat line of **111.74 GHz** (shown in pink). This directly illustrates the surrounding text's point that **VM CPU usage can exceed ESXi physical capacity**, demonstrating that these metrics measure fundamentally different things due to differing vantage points (consumer vs. provider perspective).]

Yes, the sum of VM CPU Usage is greater than the ESXi total capacity! How could it be?
The answer is different perspective.
Just like Guest OS and VM have different vantage points, the same complexity happens between VM and ESXi.
The complexity comes from the different vantage points. The metrics at ESXi and VM level measure different things. As a result, the counter at ESXi level cannot be the sum of its VMs + kernel.

[Image: ## Image Description

The diagram illustrates the **dual-viewpoint architecture** of VMware vSphere metrics, showing how VM ABC maps its two virtual components (**vcpu-0** and **mks**) across a virtual/physical boundary (red line) to two physical **threads (Thread 1, Thread 2)** running on a single **Core 1**.

The diagram explicitly annotates that **Memory Consumed** counter operates in the virtual viewpoint realm (while **Granted** does), and **CPU Demand** counter operates in the virtual viewpoint realm (while **Usage** does not — **Usage** measures the physical realm).

This directly supports the surrounding text's explanation that VM-level and ESXi-level metrics measure fundamentally different layers, which is why aggregating VM CPU Usage counters cannot simply equal ESXi total capacity — the counters reflect different vantage points (consumer/virtual vs. provider/physical).]

VM takes the consumer view, meaning it sees the virtual layer. It sees 2 virtual CPUs, unaware of HT. A VM may compete with other VMs, but they are always unaware of one another.
ESXi takes the provider view, meaning it sees the physical layer. It sees 1 core with 2 threads, fully aware of HT. Concept such as Ready and Wait are not applicable as a core is either runs or idle. The kernel practically does not experience contention as it has the highest priority.

[Image: ## Image Description

The diagram illustrates the relationship between three measurement perspectives in VMware vSphere — **VM vCPU**, **ESXi Thread**, and **ESXi Core** — across a shared timeline, showing how the same workload appears differently at each layer. It demonstrates that when one vCPU transitions through states (Co-stop → Ready → Wait → Run), its corresponding thread moves inversely (Idle → Thread Utilisation), while the paired HT thread moves in the opposite direction, and the core-level view aggregates both threads into a single utilisation metric reported every **20,000 milliseconds** in vCenter UI. The key technical point illustrated is that two threads on the same core each report independently up to **100%** utilisation, but the core itself only totals **100%**, which can cause confusion when interpreting CPU metrics without understanding the HT thread/core distinction.]

The preceeding diagram shows that there are actualy 3 levels of measurements:

| VM vCPU | Since a vCPU is a consumer, when it does not get what it wants, it needs to account for it. This is why you see counters such as ready and co stop. |
| --- | --- |
| ESXi Thread | Since a thread is consumer, it never experiences contention. It either runs or not. |
| ESXi Thread | Since each thread runs in parallel, each gets their own 100%. Now, do not total them and conclude the core can run at 200%. Yes, I know esxtop shows that. It is not wrong, but there is a simpler way. Simply look at it from core perspective. |
| ESXi Core | The core is the one doing the actual work, not the thread. So the one that is running is actually the core. That’s why it’s correct that a core registers 100% and not 50% when it only runs one of its threads. |

Now, there is a complication.
When a core is running, it can run at different frequency and efficiency.
This is where the Usage (MHz) counter comes in.
If the word Usage is confusing, think of the word throughput or cycles completed.

[Image: ## Image Description

The diagram illustrates CPU metrics across three perspectives — **VM vCPU**, **Thread**, and **Core** — mapped across three time columns, showing how **Usage (%)** and **Usage (MHz)** counters differ at each layer. The middle section highlights a key complexity with **Hyper-Threading**: two physical threads sharing a core both report **Usage (MHz)** simultaneously while the core itself consolidates this into a single **Usage (MHz)** value, with leftover capacity appearing as **Ready + Co Stop + Wait** or **Idle** on the thread not scheduled. This demonstrates why thread-level percentage metrics cause confusion (each thread adds to 100% independently, but the core only totals 100%), establishing that **Usage (MHz)** reflects performance/throughput while **Usage (%)** reflects capacity consumption.]

Let’s apply the above into the 2 pillars of operations management:
- performance
- capacity
Review the following infographic. Go through it vertically, then horizontally.
What’s your take on the metrics?

[Image: ## Image Description

This infographic contrasts **Capacity Management vs. Performance Management** metrics across three CPU hierarchy levels: **vCPU, Physical Core (HT1/HT2), and Physical Socket (C1-C6)**. For capacity, key formulas are shown: at the vCPU level, `Running + cannot run + idling = 100%` with a 2-vCPU VM summing to **40,000ms**; at the physical core level, utilization reports **200%** when both hyperthreads are active; at the ESXi level, `ESXi Utilization (%) = Average(thread utilization)`. For performance management, the unit is **GHz (not %)** at both vCPU and socket levels, with nominal speed noted as insufficient as a 100% baseline, while physical core performance is explicitly marked **"Not applicable"** — managed at the ESXi level instead. The infographic directly supports the surrounding text's argument that capacity uses static percentage-based counters while performance requires frequency (GHz/MHz) metrics to capture variable CPU speed.]

Capacity is always based on a static counter. That’s why it can use percentage as the unit.
- For VM, it’s about consuming the given vCPU.
- For ESXi, it’s about the utilization of the threads.
The CPU frequency is about performance, not capacity. That’s why metrics such as Usage and Demand are not used in capacity.
Performance is about speed, not space. That’s why CPU frequency, a key indicator of speed, has to be included.
- The capability of today’s CPU means the CPU speed varies over time and varies among its cores. As such, there is no 100% as the upper limit cannot be determined. Even if it is possible, there is no API to access this information.
- This means we can’t use percentage as unit.
- Since the upper limit is not known, we need to complement with contention counters (e.g. ready and overlap) so we can proactively manage.

### CPU vs vCPU

One major difference is there is no hyperthreading at vCPU level. vSphere only expose vSocket and vCore. Within a vCore, there is no hyperthreading.

[Image: ## VMware vSphere VM CPU Configuration Screenshot

This screenshot shows the **Virtual Hardware settings** for a VMware vSphere VM, specifically the CPU configuration panel. The VM is configured with **4 vCPUs**, set as **4 sockets × 1 core per socket**, with CPU Reservation at **0 MHz**, Limit set to **Unlimited**, and Shares at **Normal (4000)**.

In the context of the surrounding text, this image illustrates the **vSocket/vCore abstraction** in vSphere — demonstrating that vCPU configuration exposes only virtual sockets and cores (no hyperthreading visibility), which directly supports the discussion about why CPU utilization cannot use percentage-based metrics with a known upper limit.]


#### System on a Chip

As CPU architecture moves towards System on a Chip design, it’s important not to assume that a CPU socket is a simple and linear collection of cores. Take a 64-core AMD EPYC for example. It’s actually made of 8 Core Complex Dies. Each CCD has their own L3 cache. Within a CCD, there are 8 Zen 3 cores, each having their own L2 cache.
The following diagram (taken from page 5 on the AMD link above) shows there its locality effect within a single socket. A thread is closer to another thread on the same CCD. You can see an example of the performance impact on this blog here by Todd Muirhead.

[Image: ## Image Description

The diagram illustrates the **hierarchical die architecture of an AMD EPYC processor in a Multi-Chip Module (MCM) package**, showing 8x **7nm Core Complex Dies (CCDs)** connected to a central **14nm I/O Die** (with DDR memory controllers and I/O fabric). The zoomed-in CCD detail shows **8 Zen 3 cores**, each with its own **L2 cache**, all sharing a single **32MB L3 cache**. In the context of the surrounding text, this demonstrates the **locality effects within a single socket** — threads on the same CCD share L3 cache and are "closer" to each other than threads on different CCDs, which is critical for understanding NUMA sub-topology and workload placement in vSphere.]

Another consideration is NUMA. NUMA Node = Socket / Package, as 1 socket can have >1 package (if you enable Cluster-on-Die feature of Intel Xeon).
The whitepaper from AMD on EPYC 9005 Series processors shows that you can divide the socket into 4 NUMA domain. It shows the following diagram, where each domain has 6 memory DIMMS and 3 memory controllers.

[Image: ## Image Description

This diagram illustrates the **AMD EPYC 9005 Series processor's quad-NUMA domain architecture**, showing a single socket divided into 4 NUMA nodes (labeled 1–4), each with its own **GMI (Global Memory Interconnect)** controller and **6x DDR5 memory channels** (shared via a unified left/right memory bus). Each NUMA domain connects to **3 Z5 memory DIMMs stacks** and **3 D5 DIMM slots**, with inter-domain communication facilitated through GMI links. The diagram demonstrates how enabling AMD's NUMA partitioning divides one physical socket into 4 independent memory domains, directly impacting VM scheduling decisions in vSphere due to increased NUMA locality sensitivity.]

Review the NUMA effect in this KB.
From workload perspective, the situation is similar in Intel CPU. The paper from SAP below shows that SAP recommends Intel Sub-NUMA Cluster (SNC) to be enabled:

[Image: The image presents a technical explanation from an SAP document about **Intel Sub-NUMA Clustering (SNC)** support in SAP HANA, covering three key concepts: (1) increased CPU density causes longer data transfer times between different parts of the CPU chip, (2) Uniform Memory Access (UMA) domains lack optimization for nearest-resource data flow, creating risk of processors accessing memory controllers on the **opposite side** of the CPU chip, and (3) half-socket vSphere VM deployments on **Sapphire Rapids CPUs require Intel SNC** to mitigate performance fluctuations when running multiple SAP HANA VMs on a single socket. This directly supports the surrounding text's context that SAP recommends enabling Intel SNC to optimize NUMA locality and reduce cross-chip memory access latency.]

In terms of latency, this site showed the test result of Xeon 6 cache. The latency went up from 33 ns for local L3 cache to 80 ms to an L3 that is further away.

### State of a VM vCPU

ESXi Scheduler keeps in mind the following goals:
- To balance load across physical cores.
- To preserve cache state, minimize migration cost.
- To avoid contention from hardware (hyperthreading, low level cache, etc.) and sibling vCPUs (from the same VM).
- To keep VMs or threads that have frequent communications close to each other.
With the above understanding, now look at the life of a single vCPU of a VM.
At the most basic level, a VM CPU is either being utilized or not being utilized by the Guest OS. At any given moment, it either runs or it does not, there is no “walk” state.

| Being used | The hypervisor must schedule the vCPU. A multi vCPU VM has multiple schedules, 1 for each vCPU. For each vCPU: If the kernel has the physical CPUs to run it, then the vCPU gets to Run. The Run counter is increased to track this. If the kernel has no physical CPUs to run it, then the vCPU is placed into Ready State. The VM is ready, but the hypervisor is not. The Ready counter tracks this. If the kernel has resource, but other vCPU of the VM is far behind, then the vCPUis placed into Co Stop state. |
| --- | --- |
| Not being used | There are 2 possible reasons why it’s used: The CPU is truly idle. It’s not doing any work. The Idle Wait counter accounts for it. The CPU is waiting for IO. CPU, being faster than RAM, waits for IO to be brought in. There are 3 sub cases here (Co-stop, VM Wait and memory wait), and they will be covered later. |

With the above understanding, we’re ready to examine the following state diagram. The diagram shows a single schedule (1 vCPU, not the whole VM). It’s showing the view from hypervisor (not from inside the Guest OS):

[Image: ## vCPU State Diagram Description

This state diagram illustrates the four mutually exclusive vCPU scheduling states in ESXi (**Run**, **Ready**, **Wait**, **Costop**) plus the **Zombie** and **New** lifecycle states, with labeled transitions between them including **Dispatch**, **Deschedule**, **Wakeup**, **Costart**, **Wait**, **Add**, and **Remove/Die**. The **Wait** state contains a nested **Idle** sub-state, and the **Ready** state shows a **Limit** sub-label, indicating throttling conditions. In context, the diagram demonstrates how the ESXi hypervisor tracks a single vCPU's lifecycle transitions — the foundation for understanding CPU metrics like `%Ready`, `%CoStop`, and `%Wait`, which are measured in milliseconds of time spent per state rather than frequency.]

ESXi places each vCPU of the VM in one of the 4 above states. A vCPU cannot be in 2 states at the same time. This is fundamental in understanding the formula behind CPU metrics.
- Run does not check how fast it runs (frequency) or how efficient it runs (hyperthreading). Run measures how long it runs, hence the counter is in milliseconds, not GHz.
- Ready and Co-stop. 
They are mutually exclusive as they have opposite reason. 
Co-stop is “caused by” the VM, while Ready is caused by the ESXi. You can reduce Co-stop by reducing the VM size, especially relative to the NUMA boundary. You can’t do the same on Ready.
- Wait handles both Idle and Wait. The reason is the hypervisor cannot tell whether the Guest OS is waiting for IO or idle. As far as the hypervisor concern, it’s not doing anything. This also measures the state where the wait is due to hypervisor IO.
Regardless of the cause of the pause, a freeze is a freeze. The impact to Windows or Linux is the same.
Back to the kernel 4 possible states, you can conclude that:
- Run + Ready + Co-stop + Wait = 100%
- VM 2 can run when VM 1 is on Co-stop state, Ready state, or Wait state. This is because the physical thread becomes available.
Those of you familiar with Operating Systems kernel will notice that the diagram is similar with a physical OS scheduler state diagram. I’m taking  as an example as it’s a new OS and it’s designed for a range of device.

[Image: ## Image Description

This is a **process state transition diagram** for a modern OS (likely Fuchsia, given the context of "new OS designed for a range of devices"), showing five states: **Init → Ready ↔ Running → Zombies**, with **Running → Pending → Ready** as the blocking/unblocking cycle.

The diagram illustrates how OS-level process states map to **VMware vSphere kernel scheduler states**, specifically: Init=New, Ready=Ready, Running=Run, Pending=Wait, and Zombies=Zombies.

This visual supports the text's argument that vSphere's VM scheduling model (Run/Ready/Co-stop/Wait) is architecturally analogous to a physical OS process scheduler, helping readers understand vSphere metrics through familiar OS concepts.]


| Init | The process is being created.  Maps to New in the kernel |
| --- | --- |
| Ready | The process is in the ready list and waits for being scheduled by the CPU.  Maps to Ready in the kernel |
| Running | Maps to Run in the kernel |
| Pending | The process is blocked and suspended. When all threads in a process are blocked, the process is blocked and suspended. Maps to Wait in the kernel. Notice they also include Idle here in their Wait state. |
| Zombies | Maps to Zombies in the kernel |
| “none” | Our Co-stop is unique as VM is a multi-process scheduled entity |


#### Limitation

What is the ramification of above?
None of the counters above know about hyperthreading and CPU speed.
Ready, Co-stop, Wait are unaware of contention due to hyperthreading. The vCPU is not placed in ready state because both threads can execute at the same time. The contention for shared resources happens at low level hardware and essentially transparent to ESXi scheduler. If you are concerned about this certain degradation in throughput when two worlds execute at the same time on the same core, what counter should you use?
You’re right. It’s CPU Latency. Different purpose, different counter.

#### State Across Time

The above is at any given moment. To measure over time and report it (say every 20 seconds), we need to add a time dimension. The following example shows the above state diagram repeated over time, where each block is 1 second. In reality, the scheduler checks every 2- 30 milliseconds.

[Image: The image shows a time-series diagram of vCPU scheduler states (Run, Wait, CoStop, Ready) across four 1000ms blocks totaling a 4-second reporting window, visually demonstrating how each state accumulates milliseconds over time. It illustrates the conversion methodology where accumulated milliseconds are divided by total window duration (e.g., 787ms Run ÷ 4000ms = 19.7%), which scales to vCenter's actual 20,000ms (20-second) reporting cycle. The diagram contextualizes why percentage-based CPU metrics like Ready and CoStop must be interpreted relative to the Run percentage, as the proportional relationships between states reveal true VM scheduling contention.]

vCenter happens to use 20000 milliseconds as the reporting cycle, hence 20000 milliseconds = 100%.
The above visually shows why Ready (%) + Co-stop (%) needs to be seen in context of Run. Ready at 5% is low when Run is at 95%. Ready at 2% is very high when Run is only 10%, because 20% of the time when the VM wanted to run it couldn’t.
The above is per vCPU. A VM with 24 vCPU will have 480,000 as the total. It matters not if the VM is configured with 1 vCPU 24 vCores or 24 vCPU with 1 vCore each.
You can prove the above by stacking up the 4 metrics over time. In this VM, the total is exactly 80000 ms as it has 4 vCPU. If you wonder why CPU Ready is so high, it’s a test VM where we artificially placed a limit.

[Image: ## Image Description

This stacked area chart displays four vCPU scheduling metrics (Co-stop, Ready, Run, and Wait) for VM **VROPS-86** over approximately one hour on 4/5/2022 (8:00–9:00 AM), with the Y-axis in milliseconds. The chart visually demonstrates that the four metrics sum to exactly **80,000 ms** (4 vCPUs × 20,000 ms/vCPU), with Wait (orange, avg ~49,930 ms) dominating most of the period, then a dramatic shift around 8:30 AM where Ready (black, max 67,873 ms) and Co-stop (blue, max 59,243 ms) spike massively due to an artificially applied CPU limit. This illustrates why millisecond counters are problematic — the raw summed values scale with vCPU count and are not normalized, making percentage-based counters preferable for meaningful performance analysis.]

The formula for the millisecond metrics in VCF Operations are also not normalized by the number of vCPU. The following shows the total adds up to 80000 as the VM has 4 vCPU.

[Image: ## Image Description

The chart displays four CPU metrics for `_AutoRemTestVm_0_(111)` over approximately 24 hours (May 9–10), showing CPU|Ready at **77,227 ms**, CPU|Idle at **1,493.73 ms**, CPU|Co-stop at **1,151.6 ms**, and CPU|Run at **130.67 ms** at the tooltip timestamp of **05:07:11 PM**. CPU|Ready dominates the chart (reaching ~80K ms), visually dwarfing the other three metrics which remain nearly flat near zero. This demonstrates the surrounding text's point that these millisecond counters are **not normalized by vCPU count**, and the four metrics stack to exactly **80,000 ms** (4 vCPU × 20,000 ms/vCPU per collection interval), confirming the VM has 4 vCPUs while also illustrating why the artificially imposed limit causes extreme CPU Ready values.]

This is why you should avoid using the millisecond counter. Use the % version instead. They have been normalized.

#### State Across Multiple vCPU


[Image: ## Image Description

The diagram illustrates the relationship between **CPU Ready** and **Co-Stop** states across two vCPUs over time intervals A through G. vCPU 1 experiences a **Ready** state during interval C-D (waiting for a physical CPU), while vCPU 2 simultaneously experiences a **Co-Stop** state — meaning vCPU 2 is artificially halted to wait for vCPU 1 to be co-scheduled together. Both vCPUs show **Run** states during A-B and E-F, and both enter **Ready** state at interval G. This demonstrates why Co-Stop occurs in multi-vCPU VMs: when one vCPU cannot be scheduled, the hypervisor stops the other vCPU(s) to keep them synchronized, which is why VMs with more vCPUs tend to accumulate higher combined CPU contention metrics.]


[Image: The table illustrates the possible **co-scheduling states** for a 2-vCPU VM in ESXi, showing seven scenarios (A through G) where each vCPU can be in **Run, Ready, Co-Stop, or Idle** states. It demonstrates how ESXi manages vCPU synchronization, particularly the **Co-Stop mechanism** (states C and D), where an ahead-running vCPU is deliberately halted to keep virtual clocks synchronized across vCPUs. The table contextualizes why CPU Ready metrics can be affected by co-scheduling overhead in multi-vCPU VMs, with state G showing contention where both vCPUs are Ready but lack available physical CPU threads.]


### 2 Metrics Not 1

When you order a taxi, you expect 2 numbers on your mobile phone.
- The first number shows time. It tells you how long you have to wait.
- The second number show distance. It tells you how far the car is.
For example, the application tells you the car will reach in 3:50 minutes and it’s 2.8 kilometres away.
What metric you don’t need, hence it’s not provided?
The progress is 78%. A relative metric like this has no purpose as the 100% is undeterministic. The car may experience traffic jam, diversion, or simply makes a wrong turn.
The same thing in CPU, although it’s not obvious to us.
Review the following diagram. What do you observe?

[Image: ## Image Description

The chart displays **CPU clock frequency (MHz) over time (seconds)**, showing two "Run" periods separated by "Idle" periods. During active workloads, the frequency fluctuates dynamically between **Base Clock Speed**, **All-Cores Turbo Speed**, and **1-Core Turbo Speed** (the three labeled red dotted reference lines), while dropping to near-zero during idle phases.

In context, this illustrates that **CPU frequency is variable and non-constant**, analogous to the "distance traveled" metaphor — the actual work completed (CPU cycles) fluctuates based on turbo boost states, meaning a simple utilization percentage metric is insufficient to measure real throughput.]

Yes, the amount of CPU cycles completed varies. This is the equivalent of distance travelled.
The following table provides the comparison.

[Image: The image presents a side-by-side analogy comparing a **car's travel metrics** to **CPU performance metrics**, using two key dimensions: **CPU Run %** (utilization — the percentage of time active, illustrated as 90% in both cases: 9 of 10 minutes running/moving) and **CPU Throughput in MHz** (the speed/rate when active — 60 km/h for the car, 3 GHz for the CPU). It demonstrates that CPU utilization percentage alone is insufficient, as it must be paired with throughput (MHz) to understand actual work completed, since CPU speed varies due to power management just as a car's speed varies due to traffic. This directly supports the surrounding text's argument that CPU cycle completion is the meaningful metric, not just run percentage.]


### Frequency | Efficiency

There are 2 factors (speed of the run, and efficiency of pipeline) that get mixed into a single counter that measure the amount of work completed.

| Frequency | impacted by clock speed | All else being equal, a 2 GHz CPU does 2x more cycles than 1 GHz CPU |
| --- | --- | --- |
| Efficiency | impacted by Hyperthreading | All else being equal, a core running 2 threads completes 1.25x more cycles at the expense of each thread gets only 0.625x. Note these numbers are hardcoded for ease of reporting |


#### CPU Frequency

What is your CPU Speed?
There are 3 main numbers that defines the speed:

| Base | This is what vSphere uses as the total capacity. It is the nominal frequency and most commonly shown. The CPU rarely runs at this speed. It runs above it, giving you extra performance for free. |
| --- | --- |
| Single-Core Turbo | This is what marketing will show you. Benchmarking of single thread app is done with this frequency.  This is typically much higher. Using AMD EPYC 9000 series family, it ranges from 7% - 64% additional speed gain. Using Intel Xeon Platinum 8593Q, the gain is 77%. |
| All Cores Turbo | This is what you should pay attention to. AMD shares the All Core Boost speed, while Intel no longer does that. Since Intel does not provide the All Core Boost via API, we can’t use it as part of capacity. Using AMD EPYC 9000 series family, the gain ranges from 1% - 48%. |

Intel has a page called What is CPU Clock Speed. Below is an extract, with relevant highlight from me:
Intel Turbo Boost Technology enhances clock speed dynamically to deal with heavy workloads. It works without requiring any installation or configuration by the user. The technology judges the amount of heat the system can tolerate, as well as the number of cores in use, and then boosts clock speed to the maximum safe level.
Base Processor Frequency and Max Turbo Frequency are two core performance metrics that refer to different usage scenarios. For high-intensity gaming, the turbo frequency is the more important metric. Given adequate cooling, this is the speed your CPU will operate at when dealing with heavy gaming workloads such as traveling through a highly detailed environment, or calculating AI behavior on an enemy turn in a strategy game in the most CPU-intensive titles.
Recent features like the Intel Thread Director allow the latest gen Intel processors to intelligently distribute workloads to multiple cores. That’s one reason why newer processors often outperform older ones on benchmark tests even when they have similar clock speeds.
Each core can have its own frequency. This makes rolling up the number to ESXi level more complex. You can’t derive one throughput counter from the other. Each has to be calculated independently at core level.
The above brings an interesting question: what is your CPU Total Capacity?
The higher the frequency (GHz), the faster the CPU run. Ceteris paribus, a CPU that run at 1 GHz is 50% slower than when it runs at 2 GHz. On the other hand, Turbo Mode can kick in and the CPU clock speed becomes higher than stated frequency. Turbo Boost normally happens together with power saving on the same CPU socket. Some cores are put to sleep mode, and the power saving is used to turbo mode other cores. The overall power envelope within the socket remains the same.

##### Power States

There are 2 types of power states as defined by ACPI standard.

[Image: ## Image Description

The diagram illustrates the **ACPI CPU power states**, showing both **P-states (performance states)** and **C-states (idle states)** on a frequency/performance axis. In the **C0 state** (all components active), P-states range from **P0 (Turbo Mode, above nominal frequency) through P1 (nominal frequency) down to P13**, representing progressively slower clock speeds while the CPU remains running. Beyond C0, **C1, C2, through Cn** represent increasingly deep idle/halt states where the CPU is no longer executing instructions, corresponding to greater power savings but longer wake latency.]


| C-State | When a core is idle, ESXi applies deep halt states, also known as C-states. The deeper the C-state, the less power the CPU uses, but the longer it takes for the CPU to start running again. ESXi predicts the idle state duration and chooses an appropriate C-state to enter. There are 3 possible sub-states in C-state: |
| --- | --- |
| P-State | There are 14 grades of CPU performance, measured by its frequency. You can see all the frequencies in esxtop if your hardware supports it. P0 state where Turbo Boost happens.  P1 is where it runs at Nominal Frequency (NF). P13 is the lowest CPU frequency. |

For details on P-State and C-State, see Valentin Bondzio and Mark Achtemichuk, VMworld 2017, Extreme Performance Series.
BTW, we

##### Turbo

How high can Turbo/Boost go?
It turns out that it is high enough that both performance and capacity need to account for it.
Because speed is the primary attribute for performance, and an important contributor to capacity, the upper limit of CPU performance and capacity become harder to manage.
- Within a core, it impossible to predict the core frequency. It all depends on the instructions and what other cores are doing. Likely, there is no pattern at all.
- Within a socket, it’s impossible to predict which cores will run faster at the expense of others. A socket with 20 cores will run at >1 frequency in real world.
The following diagram is taken from page 12 of “Host Power Management in VMware vSphere 7.0” whitepaper by Ranjan Hebbar and Praveen Yedlapalli. It shows that Intel Xeon Platinum 8260 can increase its speed by 1.29x (from 2.4 GHz to 3.1 GHz). If it only needs to increase 1 core, that single core can go up by 1.62x. This will be noticeable by application that is CPU intensive. Consider this benefit before you decide to disable power management. The high performance is static, it runs at the same frequency throughout. [e1: review this diagram. TDP should be higher than 165W in the following diagram]

[Image: The diagram illustrates the CPU P-state frequency scaling for the **Intel Xeon Platinum 8260**, showing frequency levels from **1.00 GHz (P15, 57W)** at the lowest operating frequency up to **3.90 GHz (P0, 165W)** at 1-core max turbo, with the nominal frequency at **2.40 GHz (P1, 165W)**. The "Boost range" (P0) spans from 2.41 GHz to 3.90 GHz and is not directly OS-visible, while P1–P15 represent the OS-visible operating range. This demonstrates Intel Turbo Boost's ability to scale all-core frequency to **3.10 GHz** (1.29x over nominal) and single-core frequency to **3.90 GHz** (1.62x over nominal), directly supporting the surrounding text's argument for keeping power management enabled rather than forcing static high-performance mode.]

Let’s take a more recent example. The following is Intel Xeon 6520P. It can run at 3.4 GHz, which is 42% higher than the base speed.

[Image: The image displays CPU specifications for the **Intel Xeon 6520P** processor, showing 24 cores, 48 threads, a Max Turbo Frequency of **4 GHz**, an All Core Turbo Frequency of **3.4 GHz**, and a Processor Base Frequency of **2.4 GHz**. In context, this data supports the surrounding text's claim that the All Core Turbo frequency (3.4 GHz) is **42% higher** than the base frequency (2.4 GHz), illustrating the performance benefit of Turbo Boost under power management settings. The gap between base (2.4 GHz) and single-core max turbo (4 GHz) also demonstrates the **1.62x** uplift potential referenced in the preceding text.]

BTW, there is no setting in ESXi to disable or enable Turbo Boost directly. Yes, I’m aware Windows has it. In the case of ESXi, it’s enabled by default and all you have to do is set the power management.
Thanks to Sushil Kavi, I learned Turbo can still kick in despite the BIOS setting to static high power management. We verified that the value of %A/MPERF in esxtop showing all cores running at 129%.

##### Impacts on ESXi

The following table shows the difference in value if All Core Turbo is 20%.

[Image: ## Table Description

This table illustrates the impact of **20% All-Core Turbo Boost** on ESXi CPU metrics across six utilization scenarios, comparing three values: **Core Utilization** (actual physical usage), **Usage %** (what vSphere Client displays, inflated by Turbo), and the author's **recommended threshold** (conservative baseline excluding Turbo overhead).

Key data points show that at **67% core utilization**, vSphere reports **80% usage** (highlighted as a warning threshold), while the recommended cap is **54%** — demonstrating a ~26% reporting gap caused by Turbo Boost. At **100% core utilization**, vSphere shows **120% usage** with an 80% recommended limit (highlighted green), and at **125% utilization** (HT/hyperthreading territory), usage hits **150%** where actual **performance degradation from Hyper-Threading begins**.

The table demonstrates that vSphere's reported CPU usage figures are significantly inflated relative to true core utilization when Turbo Boost is active, meaning administrators risk over-provisioning or misreading capacity if they rely solely on the UI percentage without accounting for the Turbo multiplier.]

Usage (%) is what vSphere Client UI shows.

##### High Performance vs Balance

Should you always set power management to maximum?
No. ESXi uses power management to save power without impacting performance. A VM running on lower clock speed does not mean it gets less done. You only set it to high performance on latency sensitive applications, where sub-seconds performance matters. VDI, VoIP, video calling, Telco NFV are some examples that are best experienced with low latency.
Review the vSphere 9 performance best practices paper. I’ve copied the part you need to focus below:

[Image: The image displays a text excerpt from a VMware ESX documentation covering **Power Policy Options**, specifically describing two policies: **High Performance** (no power saving, maximizes performance for fully-loaded cores, but may underperform when cores are idle) and **Balanced** (default policy, reduces power consumption while maintaining flexibility, and can actually **increase performance** on systems with idle CPUs by enabling active CPUs to reach faster **Turbo Boost states**).

In the context of the surrounding text, this excerpt supports the argument that **High Performance mode is not always optimal** — on clusters with low core utilization (common in mission-critical or HA configurations), the Balanced policy may deliver better performance by leveraging Turbo Boost on active cores rather than keeping all cores at a fixed high frequency.]

In mission critical cluster, the overcommit ratio is lower and the VMs tend to be over-provisioned. Or you have 2 hosts for HA as you worry about availability. The end result is your ESXi actual core utilization is not high.

###### Impact on Oversized VM

One downside of an oversized VM is higher risk of some vCPU becoming idle. When the VM becomes idle, the power enters C1 State, but does not go deeper to C2. This enables the VM to quickly spike, which is evident on the spikes at the end.
The following diagram is taken from page 24 of “Host Power Management in VMware vSphere 7.0” whitepaper by Ranjan Hebbar and Praveen Yedlapalli.

[Image: ## Chart Description

The chart displays **CPU frequency** (vertical axis, scaled to ~60–160% of nominal frequency where 100 = nominal) comparing two ESXi power management modes: **High Performance** (red) and **Balanced** (blue). Initially, Balanced mode runs significantly higher (~150) than High Performance (~129), but Balanced degrades more steeply over the horizontal axis (representing CPU utilization/busyness), dropping as low as ~65, while High Performance remains relatively stable around 125 until both lines show volatile spikes at the far right. This demonstrates the counterintuitive finding that **Balanced power management delivers higher CPU frequency than High Performance at low-to-moderate utilization levels**, due to Turbo Boost exploitation, though it becomes more erratic under certain load conditions.]

I cut out the chart so we can explain how balanced power management delivers higher performance than high performance setting.
The vertical axis is the CPU Frequency, where the 100 is the nominal frequency. Yes, at the start the CPU was running well above the nominal frequency. Balanced was running higher than High Performance.
The red line is the VM CPU frequency when ESXi power management was set to High Performance. The blue line is Balanced.
The horizontal axis is not time. It’s how busy the core is. It starts with 100% busy and steadily goes down to 0, meaning the VM was idle. The VM was not powered off at the end.
The red line is fairly constant until the VM becomes idle. This makes sense as the entire CPU socket is kept on high, so all the cores are equal. As the result, the CPU boost only goes to 130% mark.
The blue line starts at much higher throughput. This makes sense as the CPU has flexibility. It can boost the running cores to 151% as other cores are idle. This is why balanced performance can deliver higher performance on low to medium load ESXi.
As the core gets less busy, the CPU reduces its clock speed. Notice it is still higher than 100 until it became idle. When the VM is idle, the CPU entered the deep C2 State. Notice there was no spike and the frequency dropped deeper.

#### CPU Efficiency

CPU SMT (Hyper Threading as Intel calls it) impacts CPU accounting as it delivers higher overall throughput. It increases the overall CPU cycles completed of the core, but at the expense of individual thread throughput. The increase varies depending on the load.
Accounting wise, it is expensive to measure as the core speed is not affected. It is still running at the same frequency. ESXi records this overall boost at 1.25x regardless of the actual increase, which may be less or more than 1.25x. Your application may experience 2.x or 1.x, the counter will simply report 1.25x.
If both threads are running at the same time, the core records 1.25x overall throughput but each thread only gets 62.5% of the shared physical core. This is a significant drop from the perspective of each VM. From the perspective of each VM, it is better that the second thread is not being used, because the VM could then get 100% performance instead of 62.5%. Because the drop could be significant, enabling the latency sensitivity setting will result in a full core reservation. The CPU scheduler will not run any task on the second HT.
The following diagram shows 2 VMs sharing a single physical core. Each run on a thread of the shared core. There are 4 possible combinations of Run and Idle that can happen:

[Image: ## Image Description

The diagram shows **two VMs (VM A on HT #1 and VM B on HT #2) sharing a single physical core** over a 100% time window, illustrating their respective **Run and Idle states**. VM A runs for approximately the first half then goes idle, while VM B runs briefly, goes idle in the middle, then resumes running. This demonstrates one of the four possible **Run/Idle combinations** — specifically a scenario where both VMs are simultaneously running (contending for the shared core) and periods where only one VM is running — which directly explains why the **CPU Run counter (50%) overstates actual performance** and necessitates the CPU Used counter to reflect the HT penalty (62.5% vs 100%).]

Each VM runs for half the time. The CPU Run counter = 50%, because it’s not aware of HT. But is that really what each VM gets, since they have to fight for the same core?
The answer is obviously no. Hence the need for another counter that accounts for this. The diagram below shows what VM A actually gets. The allocation is fixed.

[Image: ## Image Description

The diagram illustrates **CPU Used calculation for VM A** across four time segments, showing how HyperThreading (HT) contention affects CPU metrics. When both VM A (HT #1) and VM B (HT #2) are running simultaneously, VM A receives only **62.5%** of the core; when VM A runs alone (VM B idle), it receives **100%**; and when VM A is idle, it reports **0%** regardless of VM B's state. This demonstrates why **CPU Used** (which accounts for HT co-scheduling penalties) differs from **CPU Run** — producing a blended result of **40.625%** versus the naive **50%** reported by CPU Run.]

The CPU Used counter takes this into account. In the first part, VM A only gets 62.5% as VM B is also running. In the second part, VM A gets the full 100%. The total for the entire duration is 40.625%. CPU Used will report this number, while CPU Run will report 50%.
If both threads are running all the time, guest what CPU Used and CPU Run will report?
62.5% and 100% respectively.

#### CPU Throughput

The CPU efficiency and frequency have the same final effect. Both impacts the number of CPU productive cycles processed attributed to a particular thread of vCPU. This is why I prefer to call the metric CPU Throughput instead of CPU Usage and CPU Used. The word usage and used are confusing as it’s a general English word.
A CPU is always running. A CPU could be running many cycles while waiting for data from memory or a disk, and those cycles are effectively "wasted" from the perspective of completing the task. I hope the word throughput conveys that it refers to the useful cycles, and not idle loop.

#### Impacts on VM

Let’s take an example to quantify the impact of both CPU frequency and CPU efficiency on a VM vCPU.

|  | The CPU can run all its 20 cores at 30% higher speed. When only a single core is used, it runs up to 70% faster. An example of CPU capable of such performance boost is AMD EPYC 9634.  For ease of calculation, this sample CPU has a nominal clock speed of 1 GHz. This is what you see in vSphere Client UI, and what you consider as 100%. The number is shown in red as using this number as total capacity leaves money on the table. |
| --- | --- |

Now let’s look at what the experience that Windows or Linux receive as a result.
You will see that a VM can run 100% flat out for hours yet the amount of work completed varies wildly by the second. This is why VM performance feels unpredictable.
We consider 2 extreme scenarios. In typical data center, you’re fluctuating between these 2 edges.

[Image: The image shows two bar charts comparing CPU frequency performance for 1 vCPU vs 2 vCPU configurations under two conditions: **single core active** (left) and **all cores active** (right). When only 1 core runs, 1 vCPU achieves **1.7 GHz** while 2 vCPU drops to **1.06 GHz** due to hyperthreading penalty; when all cores run, 1 vCPU gets **~1.3 GHz** and 2 vCPU drops further to **812 MHz**. The 2 vCPU configuration uses a **1.25x wider scheduling unit**, illustrating how adding vCPUs paradoxically reduces per-vCPU clock frequency and overall performance due to hyperthreading contention and scheduling constraints.]

One 1 extreme, the entire CPU only runs 1 core out of 20 cores. If a vCPU runs at 100% and has 0% contention, it will get 1.7 GHz cycles. This is 70% higher than the nominal speed. VM CPU counter such as Demand will report 170%. If you’re not careful, you will think you need more vCPU. In this case, adding more vCPU will make the situation worse.
Let’s say you add a second vCPU. For simplicity, let’s assume they run on the same core. What happens is hyperthreading penalty kicks in. Each only gets 62.5%. So now both vCPU gets 1.06 GHz. So instead of getting 3.4 GHz total, you get 2.12 GHz.
Now let’s look at the other extreme. All the cores are running at the same time. A VM with 1 vCPU will run at 1.3 GHz. Again, since VM CPU Demand is based on 1 GHz, it will report 130%. You then add another vCPU. Now, since all the cores are busy, there is a real chance that the VM 2 vCPU will end up on the same core. In this case, each will run at 812 GHz. You will now be confused, as both runs at 81% yet it seems to have maxed out.
The flow over time in the preceding example is 1.7 GHz  1.3 GHz  1.06 GHz  0.81 GHz, as ESXi CPU scheduler will maximize throughput. The problem is CPU Usage (%) metric mask out this degradation. Couple with the fact that it happens over time as VMs get added into the clusters, it becomes complex to figure out.

[Image: ## Image Description

The diagram illustrates CPU frequency throttling over time across three phases of VM workload, showing how frequency degrades from **1.7 GHz** (Single Core Boost) → **1.3 GHz** (All Cores Boost) → **0.8 GHz** (below Nominal 1.0 GHz), while CPU Run percentage remains constant at **100%** throughout all three phases. This demonstrates the core problem discussed in the surrounding text: the CPU Usage (%) metric masks frequency degradation because utilization reads 100% regardless of whether the processor is running at 1.7 GHz or 0.8 GHz. The red arrow in the final phase extending below nominal frequency visually emphasizes the thermal/power throttling condition where actual throughput is significantly degraded despite misleading utilization metrics.]


## VM

Take note that some metrics are for the kernel internal consumption, and not for vSphere administrators. Just because they are available in the UI and have names that sound useful do not mean it’s for your operations. Their name is written from CPU scheduler viewpoint.
I will use the vSphere Client as the source of metrics in the following screenshots.
vSphere provides 6 metrics to track contention.

[Image: The image displays a table of **6 VM CPU contention metrics** available in vSphere, listing their Counter name, Rollup method, Units, Stat Type, and Description. The metrics shown are **Latency** (Average, %, Rate), **Max Limited** (Summation, ms, Delta), **Overlap** (Summation, ms, Delta), **Readiness** (Average, %, Rate), **Ready** (Summation, ms, Delta), and **Co-stop** (Summation, ms, Delta). This table directly supports the surrounding text's claim that vSphere provides 6 metrics to track CPU contention, illustrating how each metric captures a different aspect of a VM's inability to access physical CPU resources.]

You get 9 metrics for consumption.

[Image: The image shows a table of **9 VM CPU consumption metrics** available in vSphere, including: **Demand, Demand-to-entitlement ratio, Entitlement, System, Usage, Usage in MHz, Used, VCPU Usage, and Run**. Each metric is defined by its rollup type (Average, Latest, or Summation), units (MHz, %, or ms), stat type (Absolute, Rate, or Delta), and a description. This table supports the surrounding text's claim that vSphere provides 9 metrics for CPU consumption tracking, distinguishing between scheduler-internal metrics and those relevant for vSphere administrators.]

I group Wait metrics separately as it mixes both contention and consumption.

[Image: The table displays three CPU "Wait" metrics in vSphere: **Swap Wait** (CPU time waiting for swap-in), **Idle** (total CPU idle state time), and **Wait** (total CPU wait state time) — all using Summation rollup, milliseconds units, and Delta stat type. This image illustrates the author's point that these metrics occupy a hybrid category, mixing both **contention and consumption** characteristics, which is why they are grouped separately from the pure contention and pure consumption metric sets. The context indicates these 3 Wait metrics supplement the 6 contention metrics and 9 consumption metrics previously described.]


### Contention Metrics

Let’s dive into each counter. As usual, we start with contention type of metrics, then utilization.
Contention has to be judged within the context of consumption. A 2% CPU Ready relative to a 10% CPU Run is “not good”, while 2% Ready on 98% Run is “good”. What I meant is the application may not feel the later, as 98% Run means the application gets a lot of work done. On the other hand, if you have an oversized VM, and it only needs 10% CPU power because business is bad, a 2% CPU Ready means 20% of that business transactions were delayed.
The main 2 counters are Ready and Co-stop. The other 2 counters (Overlap and Other Wait) tend to show much lower value, hence less important operationally. The following shows a typical observation, where both are very high, yet CPU Overlap is near 0.

[Image: ## Chart Description

The graph displays three vCPU metrics over time (roughly 2:00 AM to 2:00 PM) for a VM: **Peak vCPU Co-Stop (25.26%)**, **Peak vCPU Ready (17.87%)**, and **Peak vCPU Overlap (0.0069%)**, captured at the 20-second peak interval at the vCPU level. Both Co-Stop and Ready exhibit sharp spikes between ~3:00–7:00 AM followed by sustained elevated levels beginning around 8:00 AM, while Overlap remains essentially flat near zero throughout. This illustrates the text's point that Co-Stop and Ready can simultaneously reach high values while Overlap remains negligible, representing significant CPU scheduling contention where the guest OS is unaware of the frozen time.]

The preceding showed the 20-second peak metric, taken at vCPU level. Taking at the VM level (it has 8 vCPU) shows a similar pattern.
Guest OS is not aware of both Co-stop and Ready. The vCPU freezes. “What happens to you when time is frozen?” is a great way to put it. As far as the Guest OS is concerned, time is frozen when it is not scheduled. Time jumps when it’s scheduled again.
The time it spends under Co-stop or Ready should be included in the Guest OS CPU sizing formula as the vCPU wants to run actually.
If VM utilization is not high, reduce its vCPU while following NUMA best practice.
High CPU Ready can happen at low CPU Co-stop. This means everytime the VM vCPU wants to run, there is enough physical CPU threads to run all the vCPU at the same time. So it’s an all or nothing situation.
The following shows an 8 vCPU VM with ready hit 7.5% multiple times, while Co-stop remains near 0% for days.

[Image: The chart displays two metrics for an 8-vCPU VM (`h_eight_core-se-mpcus`) over approximately November 14–16: **CPU Peak vCPU Ready** (blue line) and **CPU Peak vCPU Co-Stop** (pink line, near 0%). The Ready metric repeatedly spikes to **7.5–17.57%** throughout the monitoring period, while Co-Stop remains consistently near **0.14%** or below. This visually demonstrates the described "all or nothing" scenario where high CPU Ready occurs without corresponding Co-Stop elevation, meaning each time the VM's vCPUs want to run, sufficient physical threads are available to schedule all vCPUs simultaneously — eliminating the need for co-scheduling waits.]


#### Ready

Ready tracks the time when a VM vCPU wants to run, but ESXi does not have a physical thread (not core) to run it. This could be due to the VM itself (e.g. it has insufficient shares relative to other VMs, it was vMotion) or the ESXi (e.g. it is highly utilized. A sign of ESXi struggling is other VMs are affected too).
When the above happens, ESXi CPU Scheduler places the VM vCPU into Ready state.
Ready also accounts when Limit is applied, as the impact to the vCPU is the same (albeit for a different reason altogether). When a VM is unable to run due to Limit, it accumulates limbo time when sitting in the limbo queue. Be careful when using a Resource Pool, as it can unintentionally cause limits.
Take a look at the high spikes on CPU Ready value. It hits 40%!

[Image: The image displays three time-series charts for a VMware VM over March 1-2, showing **CPU Ready (%)**, **CPU Usage (GHz)**, and **CPU Demand (GHz)**. Key peaks are highlighted in yellow around 4:00 PM on March 2, where CPU Ready spikes to **40.69%**, CPU Usage peaks at **3.95 GHz**, and CPU Demand reaches **6.6 GHz**. The divergence between Usage (capped near 4 GHz) and Demand (6.6 GHz) visually demonstrates the effect of a **4 GHz CPU limit** on the VM, causing excessive CPU Ready time as the vCPU is forced to wait despite having unmet demand.]

Notice the overall pattern of the line chart correlates very well with CPU Usage and CPU Demand. The CPU Usage hit 3.95 GHz but the Demand shot to 6.6 GHz. This is a 4 vCPU VM running on a 2.7 GHz CPU, so its total capacity is 10.77 GHz. Why did Usage stop at 3.95 GHz?
What’s causing it?
If your guess is Limit you are right. This VM had a limit set at 4 GHz.
Ready also includes the CPU scheduling cost (normally completed in microseconds), hence the value is not a flat 0 on idle VM. You will notice a very small number. Ready goes down when Guest OS is continually busy, versus when a process keeps waking up and going to sleep, causing the total scheduling overhead to be higher. The following shows Ready is below 0.2% on an idle VM (running at only 0.8%). Notice Co-stop is basically flat 0.

[Image: ## Image Description

The chart displays three CPU metrics for a VM (`stage-web-1`) over approximately 26 hours (Feb 23 ~12PM to Feb 24 ~11AM): **CPU Usage (~0.8%)**, **CPU Ready (<0.2%)**, and **CPU Co-stop (~0%)**. CPU Usage (pink) remains relatively stable around 0.8%, while CPU Ready (purple) stays consistently below 0.2%, and Co-stop (teal) is essentially flat at zero throughout the entire period. This demonstrates the text's assertion that on an idle/lightly loaded VM, Ready overhead remains non-zero due to scheduling costs but stays very low, and Co-stop is negligible — with a notable brief spike in both Usage and Ready around 2:00 AM Feb 24.]

CPU Ready tends to be higher, ceteris paribus, in larger VMs. The reason is the chance of running more vCPU at the same time is lower in a busy ESXi host.
Instead of thinking of CPU ready in 2D (as shown in the first chart below), think in 3D where each vCPU moves across time. Each needs to be scheduled, and ideally they run together. The 2nd chart below shows how the 8 vCPUs move across time better.

[Image: The image shows two charts displaying **CPU Ready Time (%)** across 8 vCPUs (vcpu0–vcpu7) over 9 samples. The left 2D stacked area chart shows a peak of ~24% total ready time at sample 3, while the right 3D line chart separates each vCPU's individual ready time trajectory (peaking around ~8% for the highest vCPU at sample 5). Together, these charts illustrate the book's point that visualizing CPU Ready in 3D better demonstrates how individual vCPUs must each be independently scheduled, explaining why larger VMs experience higher CPU Ready — the probability of co-scheduling all vCPUs simultaneously decreases as the ESXi host becomes busier.]


##### Best Practice

I sample 3937 VMs from production environment. For each of them, I took the 20-second peak and not the 5-minute peak.
Why do I take the 20-second?
Unless the performance issue is chronic, CPU Ready tends to last in seconds instead of minutes. The following is one such example.

[Image: ## Image Description

The chart displays two CPU Ready metrics for VM **vrho-CS2** over a ~9-hour period (12:00 PM – 9:00 PM, July 25): **Peak vCPU Ready within collection cycle (%)** (pink) and **CPU Ready (%)** (purple), with values ranging from ~0–15%. A sharp spike occurs around **4:43 PM**, where the peak metric reaches **17.17%** while the average CPU Ready is only **3.63%** — demonstrating a ratio of nearly **5x** between the two. This illustrates the book's argument for using 20-second peak sampling rather than 5-minute averages, as the brief CPU Ready spike would be significantly **underrepresented** by the averaged metric alone.]

The following shows a different behaviour. Notice initially both metrics are bad, indicating severe CPU ready. However, the gap is not even 2x. I think partly because the value is already very high. Going beyond 50% CPU Ready when CPU Usage is high will result in poor performance. This VM has 16 vCPU.

[Image: The chart displays two CPU Ready metrics for a VM ("CPU|Peak vCPU Ready within collection cycle (%)" in pink and "CPU|Ready (%)" in purple) over a ~24-hour period on September 28-29. At the tooltip marker (05:35:25 PM), Peak vCPU Ready reached **47.69%** while average CPU Ready was **26.84%**, demonstrating a near **2x gap** between the two metrics during the high-contention period. Around 06:00 PM, both metrics drop sharply to near zero and remain flat, illustrating the text's point that after the severe CPU ready event resolved, both values converged and stayed in a healthy range.]

Subsequently, the performance improved, and both values became very similar and remained in a healthy range.
I collected 4 months’ worth of data, so it’s around 35K metrics per VM.
The following screenshot was my result. What do you expect to get in your environment?

[Image: ## Image Description

This screenshot displays a VMware vSphere CPU performance table showing **3,937 VMs** sorted by **20-second worst CPU Ready %** over a 4-month period (~35K data points per VM). The top entries show alarming worst-case values (HSS-P at **40.24%**, RPA-P entries ranging **22-33%**, cp-mic at **22.8%**), yet the **99th percentile column** reveals most VMs have healthy values (majority **<5%**, with cp-mic at **14.33%** and control… at **8.81%** being notable exceptions). The average row (**0.97% worst, 0.37% 99th percentile, 5.37 vCPU**) demonstrates the core statistical argument: while absolute worst-case metrics appear alarming, they are outliers, and the environment's overall CPU Ready health is excellent when evaluated with percentile-based analysis across 137 million data points.]

The first column takes the highest value from ~35K data points. The table is sorted by this column, so you can see the absolute worst from 35040 x 3937 = 137 million data points. Unsurprisingly, the number is bad. Going down the table, it’s also not surprising as the worst 10 are bad.
But notice the average of these “worst metrics”. It’s just 0.97%, which is a great number.
The 2nd column complements the first one. I eliminate the worst 1% of the data, then took the highest. So I took out 350 datapoints. Since VCF Operations collects every 5 minutes, that eliminates the worst 29 hours in 4 months. As you can expect, for most VMs the values improve dramatically. The 2nd column is mostly green.

##### Ready | Readiness

There are 2 metrics provided: Ready (ms) and Readiness (%).
I plotted both of them. They show identical pattern. This is a 4 vCPU VM, hence the total is 80000 ms.

[Image: ## Chart Description

The chart displays two metrics for **VROPS-86**: **Ready (ms)** with Summation rollup (left Y-axis, 0–80k ms) and **Readiness (%)** with Average rollup (right Y-axis, 0–100%), both plotted over approximately one hour on **4/5/2022 from 7:45–8:40 AM**. Both metrics show **near-zero values until ~8:30 AM**, when they spike dramatically — Ready peaks at **67,443 ms maximum** and Readiness reaches **84.3% maximum** — before exhibiting high volatility through 8:40 AM. This illustrates the text's point that Ready (ms) and Readiness (%) show **identical patterns**, with the 80,000 ms scale ceiling corresponding to 100% Readiness for this 4-vCPU VM, confirming the normalization relationship described.]

The Readiness (%) has been normalized, taking into account the number of vCPU. Notice 80000 ms matches with 100%. If it is not normalized, you will see 80000 as 400%.

#### Co-stop

Co-stop is a different state than Ready because the cause is different. The effect to the VM is the same. A pause is a pause. The Guest OS is unaware of the cause and experience the same contention.
Co-stop only happens on Simultaneous Multi Processor (SMP) VMs. SMP means that the OS kernel executes parallel threads. This means Co-stop does not apply to 1 vCPU VMs, as there is only 1 active process at any given time. It is always 0 on single vCPU VM.
In a VM with multiple vCPUs, ESXi kernel is intelligent enough to run some of the VM vCPUs when it does not have all physical threads to satisfy all the vCPU. At some point, it needs to stop the running vCPU, as it’s too far ahead of its sibling vCPU (which it cannot serve, meaning they were in ready state). This prevents the Guest OS from crashing. The Co-stop metrics track the time when the vCPU is paused due to this reason. This explains why Co-stop tends to be higher on a VM with more vCPUs.
Say one vCPU is in ready state. The remaining vCPU will eventually be co-stopped, until all the vCPUs are co-started. The following diagram show vCPU 0 hit a ready state first. Subsequently, the remaining 7 vCPU hit a co-stop, even though there were actually physical thread to run them.

[Image: ## Image Description

This 3D line chart displays **vCPU Co-stop metrics (in %)** across 8 vCPUs (vcpu0–vcpu7) over 10 samples (0–9). **vcpu0** (dark navy) peaks at ~2.75% around sample 3 then drops sharply to 0% at sample 5, while **vcpu1–vcpu7** (lighter blue shades) peak later at ~4.3% around sample 6 before declining to ~1% by sample 9. This illustrates the described cascading behavior: vcpu0 enters a ready state first, causing the remaining 7 vCPUs to subsequently hit co-stop, staggered in time, even though physical threads were available to run them.]

One reason for Co-stop is snapshot. Refer to this KB article for details.

##### Best Practice

The value of Co-stop should be <1% in high performing environment. This is based on 64 million datapoints, as shown on the following pie chart.

[Image: ## Image Description

The pie chart displays the distribution of **Co-stop metric values** across **2,429 production VMs**, using each VM's maximum Co-stop value over the last 3 months (26,298 datapoints per VM). The vast majority — **97.69%** — fall in the **0–0.5% range**, with only **0.82% (20/2429 VMs)** in the 0.5–1% range and **1.48%** in the 1–10% range. This validates the best practice threshold of **<1% Co-stop** in high-performing environments, demonstrating that Co-stop issues are rare in production VMware vSphere deployments.]

The value of Co-stop tends to be smaller than Ready, as shown below. Ready and Co-stop may or may not corelate with Usage. In the following chart you can see both the correlation and lack of correlation.

[Image: ## Chart Description

The chart displays three CPU metrics for a VMware vSphere VM (`ora***-s**g-w2`) over approximately 5 days (Feb 1–5): **CPU Ready (%)** in purple, **CPU Usage (%)** in pink, and **CPU Co-stop (%)** in teal. CPU Usage fluctuates between roughly **5–12.5%** throughout the period, while CPU Ready remains consistently low (~0–1%), and Co-stop stays near **0%** (essentially flat/teal line barely visible). A notable spike in CPU Ready (~8) occurs around **Feb 3 at ~06:00 AM**, coinciding with a corresponding spike in CPU Usage, demonstrating the text's point that Ready and Co-stop **may or may not correlate** with Usage — in most of the timeframe they don't correlate, but the Feb 3 spike shows a momentary correlation.]


#### Overlap

When ESXi is running a VM, this activity might get interrupted with IO processing (e.g. incoming network packets). If there is no other available cores in ESXi, the kernel has to schedule the work on a busy core. If that core happens to be running VM, the work on that VM is interrupted. The counter Overlap accounts for this, hence it’s useful metric just like Ready and Co-stop counter.
The interrupt is to run a system service, and it could be on behalf of the interrupted VM itself or other VM.
Notice the word system services, a process that is part of the kernel. This means it is not for non-system services, such as vCPU world. That’s why the value in general is lower than CPU Ready or even Co-Stop. The value is generally affected by disk or network IO.
Some documentation in VMware may refer to Overlap as Stolen. Linux Guest OS tracks this as Stolen time.
When a vCPU in a VM was interrupted, the vCPU Run counter is unaware of this and continues tracking. To the Guest OS, it experiences freeze. Time stops for this vCPU, as everything is paused. The clock on motherboard does not tick for this vCPU. Used and Demand do account for this interruption, making them useful in accounting the actual demand on the hypervisor. When the VM runs again, the Guest OS experiences a time jump.
Review the following charts. It shows CPU Usage, CPU Overlap and CPU Run. See the green highlights and yellow highlights. What do you notice?

[Image: The image displays three time-series charts for **UAG-167** showing **CPU Usage (%)**, **CPU Overlap (ms)**, and **CPU Run (ms)** between approximately **06:00–07:30 AM**. Green highlights mark two peaks (~06:15 AM and ~06:40 AM) visible in both CPU Usage and CPU Run, while yellow highlights mark periods of **elevated CPU Overlap** (~06:20–06:35 AM and ~06:45–07:15 AM). The charts demonstrate that during the yellow-highlighted overlap periods, **CPU Run remains unchanged** (unaware of overlap) while **CPU Usage decreases correspondingly**, proving that Usage accounts for overlap contention whereas Run does not.]

The above prove that Run is not aware of overlap. Notice when overlap went up, Run did not go lower. CPU Usage however, did go down as it’s aware of overlap.
The correlation is not perfect as Usage is also aware of hyperthreading and CPU frequency.
The Overlap counter is useful to troubleshoot performance problem, complementing Ready, Co-stop, Other Wait and Swap Wait. Ready does not include Overlap as the VM remains on the Run State (see the CPU State Diagram).
The unit is millisecond, and it’s the summation of the entire 20 seconds. VCF Operations averages over 300 seconds. So the amount at 300 seconds is max 20000 (this is 100%), and must be multiplied by 15 if we want to see the actual average in the 300 second period.
The amount is the sum of all vCPU, so you need to divide by the number of running vCPU if you are converting into a percentage. Divide over 20000 ms x 100%. When I did that, and plot the highest 5 among ~3K production VMs, I get this.

| Overlap (ms) | vCPU | Overlap (%) |
| --- | --- | --- |
| 6,169 | 30 | 1.03% |
| 284 | 2 | 0.71% |
| 509 | 4 | 0.64% |
| 484 | 4 | 0.61% |
| 237 | 2 | 0.59% |

The above indicates the VMs only experienced minimal interruption by the kernel.
Let’s dive into a single VM. The following is a 68 vCPU VM running Splunk. In the last 7 days, it experienced a low but sizeable CPU overlap. 10K is relatively low for a 68 vCPU VM, but it still represents half a vCPU worth of interruption.

[Image: ## Image Description

The chart displays **CPU|Overlap (ms)** and **CPU|Ready (ms)** metrics for a 68 vCPU Splunk VM over a 7-day period (Feb 18–25), with both metrics tracking closely together. Several distinct spikes are visible, with the most notable being **15,600.27 ms Overlap** and **10,092.6 ms Ready** on Thursday, Feb 18 at 10:30–10:44 AM, and additional spikes reaching ~14K–20K ms around Feb 22 and Feb 24. The chart demonstrates that while baseline values hover around 0–2,500 ms, periodic bursts of CPU contention occur, with Overlap consistently slightly exceeding Ready, illustrating the ESXi kernel's IO-driven interruptions on this VM as described in the surrounding text.]

Overlap should be included in Guest OS sizing as the Guest OS wants to run actually. The effect is the same with an unmet Demand.
A high overlap indicates the ESXi host is doing heavy IO (Storage or Network). Look at your NSX Edge clusters, and you will see the host has relatively higher Overlap value versus non IO-intensive VM.

#### Contention

This is a value add by Aria Operations in July 2024. Before that, it’s mapped to the CPU Latency metric.
The formula is.
Contention (%) = Overlap + CoStop + Ready + Other Wait (if less than 1%)
Contention means the vCPU is not getting the CPU time. Using this logic, the CPU frequency is not even applicable as the vCPU is not even running.

[Image: ## Image Description

The diagram illustrates the components of **CPU Contention** as a timeline of vCPU states, showing six distinct states: **Run**, **Overlap**, **CoStop**, **Ready** (with a **Limit** sub-component highlighted in orange), **Other Wait**, **Swap Wait**, and **Idle**. The states are color-coded with red gradients indicating contention-impacting states, and a curly brace labels **Overlap, CoStop, Ready, and Other Wait** as comprising **CPU "Contention"**, while **Swap Wait** is separately identified as **"Part of Memory Contention."** This visual contextualizes the contention formula described in the surrounding text — `Contention (%) = Overlap + CoStop + Ready + Other Wait` — by showing exactly which vCPU time states contribute to the metric and distinguishing them from memory-related wait states and idle time.]

In most situations, the value will be mostly coming from CPU Ready. The following screenshot shows the CPU Contention is basically identical to CPU Ready

[Image: ## Image Description

The chart displays three CPU metrics for **Secondary-App50-06** over Friday, Oct 4 (approximately 7:00 AM–8:00 PM): **Peak vCPU Ready** (blue, ranging ~10–23%), **CPU Contention** (cyan, ~4–7%), and **CPU Ready** (pink, ~4–7%). The key observation is that **CPU Contention (6.341%) and CPU Ready (6.16%) are nearly identical**, with their trend lines closely overlapping throughout the day, while Peak vCPU Ready shows a notable spike of **23.19%** at 4:22 PM. This visually demonstrates the surrounding text's assertion that in most situations, CPU Contention value is predominantly driven by CPU Ready, as the two metrics track almost in lockstep.]

Why does the counter include Ready by Limit?
Because we need to separate the what and the why. The fact is the VM faces contention. Whether that is because of VM Limit, insufficient VM Shares, or high ESXi utilization is a different issue.
What is the limitation for including Ready by Limit?
You cannot use the counter to define ESXi or cluster performance. The limit has nothing to do with the cluster.

#### Latency

CPU Latency tracks the “stolen time”, which measures the CPU cycle that could have been given to the VM in ideal scenario. It maps to %LAT_C counter in esxtop.
The diagram shows what it includes. Latency excludes Max Limited in Ready, but it includes Co-stop even if the Co-stop was the result of Limit. It also excludes Other Wait.
Notice that HT and CPU Frequency are effect and not metrics. You can see the impact of CPU Frequency in esxtop %A/MPERF counter.

[Image: The diagram illustrates the components of **CPU Latency** across a timeline, showing which thread states are **included** (Overlap, CoStop, Ready, Swap Wait — shown in red) versus **excluded** (Other Wait, Idle) from the CPU Latency metric. It also depicts CPU frequency effects — **Turbo Boost** and **Power Saving** — as influences on the "Used" time, along with **HT effect**, which are noted as effects rather than tracked metrics. The visual maps directly to the `%LAT_C` esxtop counter, clarifying that Max Limited in Ready and Other Wait are excluded from Latency calculations, while CoStop is included even when caused by a Limit configuration.]

Latency also includes 37.5% impact from Hyper Threading. In ESXi CPU accounting, Hyper Threading is recorded as giving 1.25x throughput, regardless of actual outcome. That means when both threads are running, each thread is recorded as only getting 62.5%. This will increase the CPU Latency value to 37.5%. All else being equal, VM CPU Contention will be 37.5% when the other HT is running. This is done so Used + Latency = 100%, as Used will report 62.5% when the vCPU has a competing thread running.
In the above scenario, what’s the value of CPU Ready?
Yup, it’s 0%.
CPU Latency also accounts for power management. When the clock speed falls below nominal frequency, CPU Latency goes up accordingly.
Because of these 2 factors, its value is more volatile, making it less suitable as a formal Performance SLA. Use CPU Ready for Performance SLA, and CPU Contention for performance troubleshooting.
The following table only shows 5 VM out of 2500 that I analyzed. These 2 metrics do not have good correlation, as they are created for different purpose.

[Image: ## Image Description

The table displays **CPU Ready (Max Contention) and CPU Latency (Max Ready)** metrics for 5 VMs out of 2,500 analyzed, showing four columns: Max Contention, Ready at CPU Contention maximum, Max Ready, and Contention at CPU Ready maximum. Values range from **27.16%–33.12% for Max Contention** and **0.54%–2.32% for Max Ready**, with the highest contention VM (33.12%) showing identical Ready and Contention peaks of 2.32%, while others show significant divergence (e.g., 29.75% contention but only 1.2% Max Ready). This directly supports the surrounding text's assertion that **CPU Ready and CPU Latency/Contention have poor correlation** because they measure fundamentally different aspects of CPU performance.]

In many cases, the impact of both threads running is not felt by the application running on each thread. If you use CPU Latency as formal SLA, you may be spending time troubleshooting when the business does not even notice the performance degradation.
The following screenshot shows CPU Latency went down when both Ready and Co-stop went up.

[Image: The image shows three performance charts for **vatc-web01** displaying **CPU Co-stop (%)**, **CPU Ready (%)**, and **CPU Contention (%)** over a time period from ~9:00 PM to 3:45 AM. The green highlighted regions (around 1:15–2:00 AM) mark a period where CPU Co-stop peaked at **H: 8.78%** and CPU Ready peaked at **H: 19.2%**, while CPU Contention shows a notably **lower/declining trend** during that same highlighted interval (H: 6.83%, L: 0.074%). This demonstrates the book's assertion that CPU Latency (Contention) and CPU Ready/Co-stop lack strong correlation — Contention actually **decreases** while Ready and Co-stop simultaneously **increase**, visually proving these metrics serve different purposes and don't reliably track each other.]

How about another scenario, where Latency is near 0% but Ready is very high? Take a look at this web server. Both CPU Demand and CPU Usage are similar identical. At around 1:40 am mark, both Demand and Usage showed 72.55%, Contention at 0.29%, but Ready at above 15%. What’s causing it?

[Image: The image shows four CPU metrics for **vxta-web01** over a ~1-hour window (1:10–2:00 AM, May 31): **CPU Ready** (H: 19.2%, L: 0.051%), **CPU Contention** (H: 5.84%, L: 0.081%, with a tooltip showing 0.29% at 1:41:59 AM), **CPU Demand** (H: 72.55%, L: 3%), and **CPU Usage** (H: 72.55%, L: 2.9%). The key observation is that at ~1:40 AM, Demand and Usage are nearly identical at 72.55% while Contention is only 0.29%, yet CPU Ready peaks above 15–19%, which appears contradictory. This demonstrates the scenario described in the text: high Ready without corresponding Contention indicates a **CPU Limit** constraint rather than inter-VM contention, since Ready does not exclude limit-induced wait time but Contention does.]

The answer is Limit. Unlike CPU Ready, it does not account for Limit (Max Limited) because that’s an intentional constraint placed upon the VM. The VM is not contending with other VMs. VMware Cloud Director sets limit on VM so this counter will not be appropriate if you aim to track VM performance using Contention (%) metric.
Here is a clearer example showing latency consistently lower than Ready due to limit.

[Image: The image shows two time-series charts for VM **odm-test-app-a3-LM4A** from approximately 2:15 PM to 7:15 PM, displaying **CPU Contention (%)** (top, H: 11.79%, L: 0.105%) and **CPU Ready (%)** (bottom, H: 17.82%, L: 0.0522%). Both metrics follow identical cyclical patterns with regular peaks and troughs, but CPU Ready consistently peaks higher (~17.82%) than CPU Contention (~11.79%), visually demonstrating the surrounding text's point that **CPU Contention does not account for VM CPU Limits**, causing it to report lower values than CPU Ready when a limit is applied — making Contention an unreliable standalone metric in limit-constrained environments like VMware Cloud Director.]

A better and more stable metric to track the contention that a VM experience is Ready + Co-stop + Overlap + VM Wait + Swap Wait. Note that the raw metric for all these are millisecond, not GHz.
Where do you use CPU Contention then?
Performance troubleshooting for CPU-sensitive VM.
If the value is low, then you don’t need to check CPU Ready, Co-stop, Power Management and CPU overcommit. The reason is they are all accounted for in CPU Contention.
If the value is high ( > 37.5%), then follow these steps:
- Check CPU Run Queue, CPU Context Switch, “Guest OS CPU Usage“, CPU Ready and CPU Co-stop. Ensure all the CPU metrics are good. If they are all low, then it’s Frequency Scaling and HT. If they are not low, check VM CPU Limit and CPU Share.
- Check ESXi power management. If they are set to Maximum correctly, then Frequency Scaling is out (you are left with HT as the factor), else HT could be at play. A simple solution for applications who are sensitive to frequency scaling is to set power management to max.
- Check CPU Overcommit at the time of issue. If there is more vCPU than pCore on that ESXi, then HT could be impacting, else HT not impacting. IMHO, it is rare that an application does not tolerate HT as it’s transparent to it. Simplistically speaking, while HT reduces the CPU time by 37.5%, a CPU that is 37.5% faster will logically make up for it.
There is a corner case accounting issue in %LAT_C that was resolved in ESXi 6.7. VMs with Latency Sensitive = High on ESXi 6.5 or older, will show any “guest idle” time of vCPUs as LAT_C, for those VMs the counter should not be relied on. This is a corner case because majority of VM should not be set with this, as it impacts performance of other VMs.

### Wait Metrics

CPU is the fastest component among infrastructure resources, so there are times it must wait for data. The data comes from memory, disk or network.
There are also times when there is nothing to do, so the CPU is idle. Whether the upper-layer (Guest OS vCPU) is truly idle or blocked by pending IO, the kernel does not have the visibility. It can only see that Windows or Linux is not doing any work.
There are 3 sub-metrics that make up Wait.
- Idle. Waiting for work.
- Swap Wait. Waiting for memory.
- Other Wait. Waiting for other things.

[Image: ## Image Description

The table displays four CPU wait sub-metrics across 10 rows: **CPU|Wait (%)**, **CPU|Idle (%)**, **CPU|Other Wait (%)**, and **CPU|Swap Wait (%)**. CPU|Wait values are consistently high (98.56–99.99%), CPU|Idle dominates at 93.78–97.71%, CPU|Other Wait ranges from 1.79–6.21% (sorted descending), and **CPU|Swap Wait is 0% across all rows**. This demonstrates that the overwhelming majority of CPU Wait time is attributable to Idle (doing nothing) rather than actionable contention, supporting the surrounding text's argument that Idle should be **excluded from VM sizing calculations** since it does not represent genuine workload demand.]

Guest OS isn’t aware of both Other Wait and Swap Wait. Just like other type of contention, it experiences freeze. The time it spends under Other Wait and Swap Wait should be included in the Guest OS CPU sizing formula as the VM wants to run actually.
Idle counter tracks when VM is not running. Regardless of the reason in the upper-layer, VM Idle should not be included in both VM sizing, and definitely not in Guest OS sizing. The reason is the vCPU is not running and you can’t predict what the usage would be. You should address the IO and memory bottleneck in Guest OS level, using Windows and Linus metrics.
Swap Wait tracks the time CPU is waiting for Memory page to come in from ESXi swap. Adding more RAM or faster RAM may result in lower CPU Wait, hence higher CPU Run. This metric was superseded by Memory Contention metric.

#### Other Wait

It tracks the time CPU is being blocked by things other than memory. This can be disk IO, network IO, or vMotion. For example, the VMM layer is trying to do something and it’s blocked. The number of reasons vary and it’s hard to pinpoint exactly which one, as you need low level debug logs such as stats vmx, schedtraces, and custom vprobes. You’re better off removing the common reasons. Snapshot is a common reason here, that it was mistakenly named as IO Wait.
The formula is:
Other Wait = Wait – Idle – Swap Wait
The above is a formula at VCF Operations.
Actions you can do to reduce Other Wait:
- vMotion the VM.
- Remove Snapshot
- Update to the latest build of ESXi (incl. physical device drivers), virtual HW and VMware Tools (virtual device drivers).
If this happens to multiple VMs, find commonality. If the above is not helping in your case, file a Support Request with VMware GSS and tag me. Please mention that you get it from here, so I have a context.
I plotted Other Wait for 4000 production VMs. Surprisingly, the value is not low.

[Image: ## Pie Chart: Other Wait Distribution Across ~4000 Production VMs

The pie chart displays the distribution of **Other Wait (%)** values across approximately 4000 production VMs, segmented into 8 ranges. The dominant segment is **0–0.5%** at **40.16%**, followed by **0.5–1%** at **20.25%** and **1–2%** at **17.21%**, with progressively smaller portions for higher ranges (2–3%: 7.88%, 3–5%: 6.32%, 5–7.5%: 2.53%, 7.5–10%: 1.53%, 10–100%: 4.12%).

In context, this chart demonstrates that while the majority (~77%) of VMs have low Other Wait values below 1%, a **surprisingly non-trivial portion (~20%)** exhibit elevated Other Wait above 1%, with 4.12% reaching as high as the 10–100% range — supporting the author's statement that the value is "not low" across production environments.]

I was curious if the value corelates with CPU Ready or Co-stop. From around 4000 production VM in the last 1 month, the answer is a no.

[Image: ## Image Description

This table displays **CPU performance metrics** for ~10 VMs, showing **Worst Ready**, **Worst Co-stop**, **Worst VM Wait**, and **99th percentile VM Wait** percentages. The VMs (mostly named RP...) show high CPU Ready values (9–27%) and Co-stop values (7–29%), yet their **Worst VM Wait values remain relatively low** (0.22–10.4%) and **99p VM Wait values are very low** (0.004–2.33%). This data supports the surrounding text's claim that **VM Wait (Other Wait) does not correlate with CPU Ready or Co-stop**, as VMs with the highest Ready/Co-stop values do not consistently show proportionally high VM Wait percentages.]

Since snapshot is another potential culprit, let’s compare with disk latency and outstanding IO.
What do you expect?

[Image: ## Image Description

This table displays VM Wait metrics for 10 production VMs, showing **99th percentile VM Wait**, **Worst VM Wait**, **Worst Outstanding IO**, **Worst Read Latency**, and **Worst Write Latency**. VM Wait values range from **12.75% to 20.02%** (highlighted in red), while Outstanding IO values are extremely low (0 to 1.55 OIOs) and latency values are minimal for most VMs. This demonstrates the **negative correlation** referenced in the surrounding text — VMs exhibiting high sustained VM Wait percentages are **not experiencing significant disk latency or IO pressure**, ruling out storage/snapshot as the root cause.]

Again, negative corelation. None of the VMs with high VM Wait is experiencing latency. Notice I put a 99th percentile, as I wanted to rule out a one-time outlier. I’m plotting the first VM as the value at 99th is very near to the max, indicating sustained problem.

[Image: ## CPU I/O Wait (%) Chart

This chart displays **CPU I/O Wait percentage** over a **7-day period (Sep 23–Sep 30)**, showing a consistently elevated pattern oscillating roughly between **~8–15%**, with a recorded **high of 16.86%** and a **low of 4.07%**. The metric exhibits a sustained, rhythmic fluctuation pattern throughout the entire week with no significant downward trend. In the context of the surrounding text, this chart demonstrates the **sustained ~15% VM Wait** value referenced by the author, confirming that the high VM Wait is not a one-time anomaly but a persistent condition — while simultaneously ruling out disk I/O latency as the root cause since the pattern is consistent rather than spike-driven.]

It turned out to be true. It has sustained VM Wait value around 15% (above is zoomed into 1 week so you can see the pattern).
I’m curious why it’s so high. First thing is to plot utilization. I checked Run, Usage and Demand. They are all low.

[Image: ## Image Description

This is a time-series chart displaying **CPU Usage (%)** for a VMware VM named "cpms-prd-[redacted]-2" over approximately **one week (Sep 23–Sep 30)**. The metric shows consistently **near-zero CPU utilization** with only occasional sharp spikes reaching approximately **5–6.47%** (highlighted max value "H: 6.47" and low value "L: 0.0207"). This chart contextually demonstrates that despite the VM exhibiting high **VM Wait** values (~15%), its CPU utilization remains extremely low — supporting the text's investigation into why VM Wait is elevated when Run/Usage/Demand metrics are all minimal.]

Using VCF Operations correlation feature, I checked if it correlates with any other metric. The only metric it founds is Idle, which is logical they basically add up to 100% when Run is low.
Take note of a  that wrongly inflates the value of Other Wait and esxtop %VMWait.

### Consumption Metrics

Consumption metric covers only utilization. Reservation and Allocation are properties, not metrics.
The following table shows the 5 VM utilization metrics.

| Counter | Unit | Source | Observability |
| --- | --- | --- | --- |
| Run | Millisecond | ESXi | vCPU level |
| Used | Millisecond | ESXi | vCPU level VM level |
| Usage | MHz | vCenter | vCPU level VM level |
| Usage | % | vCenter | VM level |
| Demand | MHz | ESXi | VM level |

Note: CPU Used and Usage at the VM level includes the system time and other charges that is not associated with a particular vCPU. If you sum up the vCPU amounts, you will notice a small gap to the amount at VM level. You can verify by comparing the values show on the vCenter performance chart legend.

[Image: This Performance Chart Legend from vCenter shows **CPU Usage in MHz** metrics for a VM (`vidb-node-cm9pk`) and its individual vCPUs (0, 13, 14), all using Average rollup. The VM-level total shows a latest value of **8,624 MHz** with a maximum of **38,051 MHz** and average of **8,613.9 MHz**, while the three vCPUs show latest values of 406, 393, and 384 MHz respectively — demonstrating the discrepancy mentioned in the surrounding text where **summing vCPU values (~1,183 MHz) does not equal the VM-level total**, due to system time and other charges not attributable to specific vCPUs.]


#### Run | Net Run

Run is when the Guest OS gets to run and process instruction. It is the most basic counter among the CPU consumption metrics. It’s the only counter not affected by CPU frequency scaling and hyper threading. It does not check how fast it runs (frequency) or how efficient it runs (SMT).
Run at VM level = Sum of Run at vCPU levels
Since the unit is millisecond, this means the value of CPU Run at VM level can exceed 20000 ms in vCenter.
The following screenshot shows CPU Run higher than CPU Used. We can’t tell if the difference is caused by power management or hyperthreading, or mix of both.

[Image: ## Image Description

The chart displays **CPU Run vs. CPU Used** metrics for vROps over a ~1-hour real-time period (1:04 PM – 2:03 PM, 03/08/2021), both measured in milliseconds using Summation rollup. CPU Run (blue) consistently exceeds CPU Used (black) throughout the monitoring window, with Run peaking at **44,664 ms** (average: 10,709 ms) versus Used peaking at **41,077 ms** (average: 7,101 ms). This visually demonstrates the key concept from the surrounding text — that the gap between Run and Used reflects the combined effect of **power management (CPU frequency scaling) and/or Hyper-Threading (SMT)**, neither of which CPU Run accounts for.]

CPU Run does not account for the following:
- Interrupt
- System time. IO performed by hypervisor has to be charged back to the VM.
- Power Management or CPU Frequency Scaling
- Simultaneous Multithreading (Hyper Threading as Intel calls it)
Because CPU Run does not take into account this external work, and not aware of CPU speed and HT, it is suitable as input to size the Guest OS and not the VM. The portion that needs to be removed is Overlap. VCF Operations added a new counter in July 2024 called Net Run.
The formula is:
Net Run = Run – Overlap
As you can guess, Net Run cannot hit 100%.
What do you notice on the following chat?

[Image: ## Chart Description

The chart displays two CPU metrics for **Centos8-DontTouch** over approximately 24 hours (Mar 29 6PM – Mar 30 ~5PM): **CPU|Usage (%)** in pink/purple and **CPU|Net Run (%)** in blue. CPU Usage fluctuates wildly between ~115% and ~144%, while CPU Net Run remains essentially flat at **~100%** throughout the entire period, with only minor dips. This demonstrates the key point from the surrounding text: Net Run is capped at 100% and stays consistently near that ceiling, while Usage (which accounts for CPU frequency scaling and other factors) reports values well above 100% with high variability — illustrating that the two metrics measure fundamentally different aspects of CPU consumption.]

Yes, Net Run was basically flat out at 100% for 24 hours. The value did not exceed 100%. Usage on the other hand, was wildly fluctuating. By now you should know why

#### Used | Usage

The scope of CPU Run metric means it can’t answer 2 important questions. When a vCPU is running,

| How fast is the “run”? | All else being equal, a 5 GHz CPU is 5x faster than a 1 GHz CPU.  The faster it can complete a task, the shorter it has to work. That’s why you see some metrics in MHz, because they account for this speed. |
| --- | --- |
| How efficient is the “run”? | If there is competing thread running in the same core, the 2 threads have to share the core resource. Both threads do not drop their CPU frequency, but the cycles that each thread receives is 37.5% less. This is where it’s better to think in terms of cycles and not frequency |

This is where Used comes in. vCenter then adds Usage (MHz) and Usage (%) metrics.
BTW, if the English word usage confuse you, think of CPU Cycles Completed or CPU Throughput instead.
By covering the above 3, CPU Used covers uses cases that CPU Run does not.
- Amount of work done.
- VM Migration. Moving VM to another ESXi requires that you know the actual footprint of the VM, because that’s what the destination ESXi needs to deal with.
- VM Chargeback. You should charge the full cost of the VM, and not just what’s consumed inside the VM. In fairness, you should also charge the actual utilization, and not rated clock speed.

##### Used

Here is how Used differs to Run:

[Image: The image is a timeline diagram comparing **CPU Used vs CPU Run** metrics across two VMs (VM 1 CPU 0 and VM 2 CPU 0). It illustrates that **Run accumulates fixed clock-time continuously** (including during overlap with VM 2's execution), while **Used accounts for Overlap, HyperThreading (HT), and Frequency Scaling** adjustments — shown by the "Used (consider HT & Frequency Scaling)" bar being wider/different than the base "Used" bar. The **Overlap** segment explicitly notes that "Run continues to accumulate, but Overlap accounts for it," demonstrating why Used provides a more accurate representation of actual CPU consumption than Run alone.]

Based on the above, you can work out the formula for VM level Used, which is:
VM level Used      = Run - Overlap +/- E + System + VMX
VM vCPU level Used = Run - Overlap +/- E
Where E is the combination of
- efficiency gained from CPU Turbo Boost. This is significant, could be 50% more when other physical cores in the socket are idle.
- efficiency loss from power savings. This is also significant. If the frequency is dropped to 40% of the nominal frequency, we consider 60% of the CPU time was stolen.
- 37.5% efficiency loss from CPU SMT. ESXi accounting records HT as 1.25x overall gain, hence each thread drops to 62.5% only. This is a significant drop that should be accounted.
VMX is typically negligible. It accounts for CPU cycles spent on things like consoling to the VM. In esxtop, System time is charged to the VM VMX world.
Because Used accounts for the actual frequency, you may expect it to be measured in GHz and not millisecond. The “conversion” from GHz to millisecond was based on static frequency. I know it requires a bit of mental mathematics 😊
Quiz:
- Why does the formula state VM level, and not individual vCPU level. What’s the reason? 
Answer: CPU Used has a different formula at VM level and vCPU level. At vCPU level, it does not include System Time. At VM level, it includes the work done by the kernel that is charged at VM level, such as System and other worlds.
- How will Used compare with Run in general? Do you expect it to be higher or lower? If it’s higher, what can cause it?
For example, a physical chip comes with 2 GHz as its standard speed. ESXi may increase or decrease this speed dynamically, resulting in turbo boost or power saving. If ESXi increases the clock speed to 3 GHz, Used counter will be 50% higher than the Run counter. Older Guest OS (e.g. Windows or Linux) version was not aware of this performance boost. It reported a value based on the standard clock speed, just like Run does. On the other hand, if ESXi decreases the clock speed to 1.5 GHz, then Used will report a value that is 25% lower than what Run reports.

##### Usage

Usage is Used + work done by kernel on behalf of the VM. This is why you see a gap on VM that processes a lot of network packets or storage commands.
There are two metrics:
- Usage (MHz)
- Usage (%)
Usage (%) is only available at VM level. Usage (MHz) is available at both vCPU and VM level.
Usage (%) = ( Usage MHz for each vCPU + VM level load ) / VM Static CPU Speed
These 2 metrics do not exist in ESXi, meaning they only exist in vCenter.
The reason is Usage (%) is not available on a per vCPU basis, while Usage MHz is. The 2 charts are also very similar but not 100% identical. Notice in the following screenshot there is time where they are 100% identical, and there is time they are not. My guess is Usage (%) contains VMX load as it’s not available on a per vCPU basis.

[Image: ## Image Description

The image shows a VMware vCenter performance chart for VM **awsvtl01** displaying two CPU metrics over approximately one hour (12:57 PM – 1:56 PM): **Usage (%)** in blue (left Y-axis, 0–110%) and **Usage in MHz** in black (right Y-axis, 0–11k MHz). The chart demonstrates that while the two metrics track very closely, they are **not perfectly identical** — particularly visible during the sustained high-activity period after ~1:48 PM where the lines diverge slightly, supporting the author's assertion that Usage (%) includes additional VMX-level load not captured in Usage MHz. Key statistics from the legend show a **maximum of 100%** and **9,185 MHz**, with averages of **14.079%** and **1,239.306 MHz** respectively.]


###### Usage (MHz)

Turbo Boost’s impact on Usage is real. In the following, you can see the value exceeds the total capacity by a sizable amount.

[Image: ## Image Description

The chart displays CPU Usage (MHz) versus CPU Total Capacity (MHz) for host **esx-01a-CEjR** over a ~12-hour period on March 17. The pink horizontal line represents the **Total Capacity at 16,800 MHz**, while the teal line shows **CPU Usage fluctuating between ~8,000–17,500 MHz** for most of the period. The key demonstration is the spike at ~10:00 PM where **CPU Usage reaches 20,435.4 MHz — exceeding the rated total capacity by ~3,635 MHz (~21.6%)**, directly illustrating the real-world impact of **Intel Turbo Boost** allowing actual CPU frequency to surpass the nominal/rated capacity ceiling.]

Let’s do a calculation so you can quantify the impact of power management.
Review the following example. This is a single VM occupying an entire ESXi.
The ESXi has 12 cores with nominal frequency of 2.4 GHz. The number of sockets does not matter in this case.
Since HT is enabled, the biggest VM you can run is a 24 vCPU. The 24 vCPU will certainly have to share 12 cores, but that’s not what we’re interested here.
What do you expect the VM CPU Usage (GHz) when you run the VM at basically 100%?

[Image: The chart displays CPU performance (MHz) over time for a single VM, showing two distinct phases separated by marker "1": a **Turbo Boost** phase running at approximately **~38,500-39,000 MHz** and a subsequent **Hyper-Threading** phase dropping to approximately **~35,500-36,000 MHz**. The sharp step-down transition at marker 1 illustrates the performance cliff when Turbo Boost is no longer sustained and the workload operates at base frequency with HT overhead. This visually quantifies the text's calculation — the ~39 GHz result with Turbo Boost versus the expected ~36 GHz baseline (12 cores × 2.4 GHz × 1.25 HT multiplier) without it.]

Well, that depends on the all-core turbo boost of the CPU.
The result above is slightly less than 39 GHz.
If there is no turbo boost, the answer will be 36 GHz.
Why not 57.6 GHz, because it’s 24 vCPU x 2.4 GHz?
Because HT does not yield 2x. It yields 1.25x only. At the end of the day, the one that does the computation is the core not the thread.
12 cores x 2.4 GHz 1.25 HT = 36 GHz total capacity with hyperthreading enabled.
In the preceding example, power management was enabled. Naturally Turbo Boost kicked in, albeit not so dramatic as all the physical cores were turbo at the same time.
You got around 39 GHz, a small increase over 36 GHz. Formula is 2.4 GHz x 12 cores x 1.25 HT x 1.08x Turbo Boost.
What happens when we disable turbo boost? That’s what we did at point 1 in the diagram above.
CPU Usage drops to slightly below 36 GHz.

###### Usage (%)

The following is a single vCPU production Windows Server. Both CPU Usage (MHz) and Demand jump to over 100%. Their values are identical for almost 30 days. The VM had near 0% Contention (not shown in chart), hence the 2 values are identical.

[Image: ## Image Description

The chart displays **CPU Demand (MHz)** and **CPU Usage (MHz)** for a single vCPU Windows Server VM over approximately **May 12 – June 11**, with the Y-axis scaled to **~3K MHz**. Both metrics track nearly identically throughout the period, showing several spikes reaching **~3,200 MHz** (around May 12–15, May 18–19, June 3–4, June 5–7), with baseline values near **0 MHz** during idle periods. The near-perfect overlap of Demand and Usage confirms near-zero contention for most of the period, with a brief divergence visible around **May 12** where Demand slightly exceeded Usage — consistent with the surrounding text's explanation that minor contention caused the two values to separate.]

Around 12 May, the VM experienced some contention. That’s why Demand was higher than Usage.

###### Usage vs Net Run

Usage is greatly affected by CPU speed and power management.
As a result, it’s more volatile than CPU Run. What do you notice on the following chart?

[Image: ## Image Description

The chart displays three CPU metrics for **S360-Trial-UAT** over approximately 21 hours (from ~5:00 PM on Mar 17 to ~3:00 PM on Mar 18): **CPU Usage (%)** (blue), **CPU Net Run (%)** (pink/mauve), and **CPU Ready (%)** (gray, nearly invisible). CPU Usage fluctuates more volatilely between **~32.5–45%**, while CPU Net Run oscillates more smoothly in a tighter band around **~39–43%**, with the two lines alternately crossing each other. This demonstrates the surrounding text's point that **CPU Usage is both higher and lower than CPU Net Run** due to turbo boost causing over-reporting at high utilization and power management causing under-reporting at low utilization.]

CPU Usage is both higher and lower than CPU Net Run. CPU Net Run is CPU Run minus CPU Overlap, so it’s closer to Usage. I hide CPU Ready as the value was basically 0%.
Generally speaking, during high utilization, Usage (%) will over-report due to CPU turbo boost.

[Image: ## Image Description

The chart displays two CPU metrics for **8.17.1_GA_for_EUC_upgrade_node_1** over time: **CPU Net Run (%)** (blue line, ~80-85%) and **CPU Usage (%)** (pink/magenta line, ~90-100%). At the tooltip timestamp of **Saturday, May 25, 10:44:02 PM**, Net Run reads **83.01%** and Usage reads **79.93%**. This demonstrates the text's assertion that during **high utilization, CPU Usage over-reports due to turbo boost** (pink line consistently higher) but can also occasionally dip below Net Run, while both metrics show periodic sharp drops representing brief low-utilization periods where Usage under-reports.]

During low utilization, Usage (%) will under report due to power savings

[Image: ## Image Description

The chart displays two CPU metrics for **VC-8.0.3.23503093-vIDB-Primary**: **CPU Net Run (%) at 12.156%** and **CPU Usage (%) at 10.11%** at the tooltip timestamp of **Sunday, May 26, 05:30:50 PM**. Both metrics show consistently low baseline values (well below 20%) with a **single sharp spike** visible earlier in the timeline reaching approximately 60-65%. This demonstrates the text's point that during **low utilization periods, CPU Usage (%) under-reports** compared to CPU Net Run, as evidenced by Usage (10.11%) reading lower than Net Run (12.156%) at this low-utilization moment.]


#### CPU Usage Disparity

This metric is required to convince the owners of the VM to downsize their large VMs. It’s very common for owners to refuse sizing it down even though utilization is low, because they have already paid for it or cost is not an issue.
Let’s an example. This VM has 104 vCPU. In the last 90 days, it’s utilization is consistently low. The Usage (%) counter never touch 40%. Demand is only marginally higher. Idle (%) is consistently ~20%.

[Image: ## Image Description

The chart displays three metrics for **secsplunk-sc2-es1** over approximately one week (April 30 – May 7): **CPU Usage (%)** (purple, ~10-15%), **CPU Idle (%)** (pink, consistently ~80-85%), and **Guest CPU Queue** (teal, near zero). A notable anomaly appears around **May 6**, where CPU Idle briefly drops to ~60% and CPU Usage spikes to ~25-30%, before returning to baseline. This visualization supports the surrounding text's argument that the VM's CPU resources are chronically underutilized, with Idle consistently near 80% and the Guest OS CPU Run Queue remaining consistently low throughout the observation period.]

All the key performance metrics such as Guest OS CPU Run Queue are low.
Obviously the VM does not need 104 vCPU. How to convince the owner if he is not interested in refund? The only angle left is performance. But then we’re faced with the following:
- CPU Run Queue inside the Guest OS is low. Decreasing CPU will in fact increase it, which is worse for performance.
- CPU Context Switch is high from time to time.
- CPU Co-Stop is very low (max of 0.006% in the last 90 days). Decreasing CPU may or may not make it lower. Regardless, it’s irrelevant. Same goes with VM Wait and Swap Wait.
- CPU Ready is very low (max of 0.14% in the last 90 days).
The only hope we have here to convince VM owner is to give insight on how the 104 vCPU are used. There are 2 ends of the spectrum:

| At one end, all 104 are balanced | All are running at that low 20%. This triggers an interesting discussion on why the application is unable to even consume a single vCPU. Is this inefficiency the reason why the application vendor is asking for so many vCPU? Commercially, it’s wasting a lot of software license |
| --- | --- |
| Imbalance | Some are saturated, while others are not. The Peak among vCPU metric will capture if any of them is saturated. This is good insight.  The Min among vCPU is not useful as there is bound to be 1 vCPU among 104 that is running near 0%. The delta between Max and Min will provide insight on the degree of the usage disparity. Does it fluctuate over time? This type of analysis helps the application team. Without it they have to plot 104 vCPU one by one. |

In reality, there could be many combinations in between the 2 extremes. Other insights into the behaviour of the 104 vCPU are:
- Jumping process. Each vCPU takes turn to be extreme high and low, as if they are taking turn to run. This could indicate process ping pong, where processes either do frequent start/stop, or they jump around from one vCPU to another. Each jump will certainly create context switch, like the cache needs to be warm up. If the target CPU is busy, then the running process was interrupted.
- CPU affinity. For example, the first 10 vCPU is always much busier than the last 10 vCPU. This makes you think why, as it’s not normal.
Naming wise, vCPU Usage Disparity is a better name than Imbalance vCPU Usage. Imbalance implies that they should be balanced, which is not the case. It’s not an indication that there is a problem in the guest OS because VCF Operations lacks the necessary visibility inside the guest OS

##### Quiz!

Review the following. How can the average utilization is only 12.% yet the Usage Disparity is >100%

[Image: ## Image Description

The chart displays two metrics for **wvRNI--6.14--Platform** over a ~9-hour period (9:00 AM – 6:00 PM on Sunday, Dec 8): **CPU|vCPU Usage Disparity (%)** at **131.829%** (blue line, hovering near ~125) and **CPU|Net Run (%)** at **12.49562%** (pink/purple line, flat near ~12.5). 

This directly illustrates the quiz scenario: despite an average CPU utilization of only ~12.5%, the vCPU Usage Disparity exceeds **100%**, demonstrating that while most vCPUs are nearly idle, at least one vCPU is heavily loaded (and boosted above 100% via CPU frequency/Turbo), creating extreme imbalance across the vCPU set.]

To answer, we need to plot each vCPU one by one.
Below is what we get.

[Image: ## Image Description

This chart displays per-vCPU Usage (MHz) for a VM named **wvRNI--6.14--Platform** at Sunday, Dec 8, 05:38:16 PM, showing 8 vCPUs (CPU:0 through CPU:7). **CPU:0 shows 2,636.4 MHz** (exceeding 2,500 MHz, indicating turbo boost), while **CPUs 1–7 all show 0 MHz**, with two flat lines visible — one near ~2,500 MHz and one near 0.

This demonstrates the "Usage Disparity" concept from the surrounding text: despite an average utilization of only ~12% across all 8 vCPUs, CPU:0 is running at full/boosted frequency while all other vCPUs are completely idle — consistent with the author's conclusion of a **uniprocessor (non-SMP) kernel** that can only utilize a single vCPU. The value exceeding 2,500 MHz confirms CPU frequency scaling (turbo boost) is active.]

Why only the first vCPU?
My take is uniprocessor kernel. It was compiled without SMP support.
Why did it go above 100%?
That’s CPU Frequency. Turbo has kicked in.

#### Demand

Demand is similar to Usage. It differs to Usage as it assumes the VM does not share the physical core. It’s what the VM utilization would be had it not experienced any issue, including hyper-threading.
Demand is not what Usage would be had the VM got everything it demanded. This metric is for the kernel resource scheduler. Ignore it.
Just to assure you, get a VM with high CPU Ready and Co-Stop that was intentionally caused. Set a limit. I did that, and here is what I got:
Co-Stop: 8.78%
Ready:  15.91%
Wait:   13.16%
Run:    62.15%
Total of the 4 = 100%.
This is expected. So far so good
But then here is what I got for Demand (%) and Usage (%):

[Image: The image shows four CPU metrics for VM **vatc-web01** over a time window on May 31: **CPU Ready** (H: 19.2%), **CPU Contention** (H: 5.84%, tooltip showing 0.29% at 01:41:59 AM), **CPU Demand** (H: 72.55%, L: 3%), and **CPU Usage** (H: 72.55%, L: 2.9%). The key observation is that **CPU Demand and CPU Usage are nearly identical** in both their peak values (72.55%) and curve shapes, despite CPU Contention being near zero. This demonstrates the author's point that Demand mirrors Usage when a CPU limit is applied, because from the kernel scheduler's perspective the VM never "demanded" more than the limit allowed.]

Demand is identical to Usage, despite Contention (%) being near 0%.
The reason is Demand is a kernel internal metric. From the kernel perspective, the VM did not demand as limit is intentionally set.
In the event the VM vCPU is running on a core where both threads are busy, the value of Usage will be 37.5% lower, reflecting the fact that the VM only gets 62.5% of the core. This makes sense as the HT throughput benefit is fixed at 1.25x.
If there is no competition for resource, Demand and Usage will be similar.
Take a look at the following screenshot from vCenter. It’s comparing Demand (thick line) and Usage (grey line)
What do you notice?

[Image: ## Image Description

The chart displays **CPU Demand (purple/thick line) vs. CPU Usage in MHz (grey/thin line)** for a VM over a real-time period on 01/27/2023, showing metrics with a maximum Demand of **1,343 MHz** (avg: 719.889 MHz) and maximum Usage of **1,501 MHz** (avg: 672.933 MHz). The key observation is that **Usage (grey line) frequently spikes higher and more sharply than Demand** (e.g., Usage peaks at 1,501 MHz vs. Demand's 1,343 MHz), while Demand appears smoother and wider at its peaks. This demonstrates how **Demand is averaged over a longer sampling interval**, producing a steadier, lower-peak value, whereas Usage captures instantaneous spikes — explaining why Usage can momentarily exceed Demand despite Demand having a higher overall average (719 vs. 672 MHz).]

How can Usage be higher than Demand at some of the point?
The reason is Demand is averaged over a longer time, giving it a steadier value. That’s why the peak is shorter but wider. Notice the average over 1 hour is higher for Demand.
Due to Turbo Boost, Demand (MHz) and Usage (MHz) can exceed 100%. The following is a 32-vCPU Hadoop worker node. Notice it exceeds the total capacity multiple times, as total capacity is based on base clock speed. Demand and Usage are identical as it’s the only VM running and the host has more than 32 cores, hence there is 0 issue.

[Image: ## Image Description

The chart displays CPU metrics for a 32-vCPU Hadoop worker node on March 24, showing **CPU Usage (104,949.4 MHz)**, **CPU Demand (104,089.13 MHz)**, and **CPU Total Capacity (86,197.48 MHz)** at the 08:30:37 AM timestamp. The pink lines for Usage and Demand are nearly identical and **repeatedly spike above the 100K MHz mark**, significantly exceeding the total capacity baseline (green horizontal line at ~86,197 MHz). This demonstrates the Turbo Boost effect described in the surrounding text, where both Demand and Usage can exceed 100% of nominal capacity, with the metrics tracking closely together because the VM is the sole workload on a host with sufficient physical cores to satisfy all CPU requests (zero contention).]

Okay, now that you have some knowledge, let’s test it 😊
Quiz Time! Looking at the chart below, what could be causing it?

[Image: ## Chart Analysis

The chart displays three VMware vSphere CPU metrics for a VM over approximately 4 days (Jan 11–14): **CPU Contention (%)** (purple), **CPU Demand (%)** (pink), and **CPU Usage (%)** (teal).

Around **Jan 12 ~06:00 AM**, a significant state change occurs: CPU Demand jumps from ~1% to ~19%, CPU Contention spikes sharply to ~19–20%, while CPU Usage **drops** from ~19% to ~14–15% — creating a clear divergence between all three metrics that persists for the remainder of the observation window.

This chart demonstrates a scenario where increased VM CPU Demand cannot be fulfilled (likely due to hyperthreading contention or insufficient physical CPU resources), causing Usage to fall below Demand while Contention rises disproportionately — notably **exceeding the Demand-Usage delta**, indicating hyperthreading tax is a contributing factor.]

Why did Demand jump while Usage dropped? VM CPU Contention (%) jumped even more. What is going on?
And why is that Contention is much more than Demand – Usage?
The reason why Demand metric jumps is the VM wanted more vCPU. That’s the only explanation.
Usage drops because the additional demand could not be met.
The VM experiences contention, which includes hyperthreading sharing. I did not include CPU Ready, Co-stop, Overlap, VM Wait and Swap Wait, as they do not matter in this case.
From the chart you can see that the formula for VM CPU Contention > Demand – Usage. Contention (%) is around 20% when Demand is 25% and Usage is 15%. The reason is Contention accounts for both CPU frequency and hyper threading, while the difference between Demand and Usage is only hyper-threading.
VCF Operations provides a percentage metric for Demand. The formula is
Demand (%) = Demand (MHz) / Total Capacity (MHz) x 100
Source wise, the metric in VCF Operations simply maps to vCenter counter cpu.demand.average.

#### System

A VM may execute a privilege instruction, or issue IO commands. These 2 activities are performed by the hypervisor, on behalf of the VM.
IO processing differs to non-IO processing as it has to be executed twice. It’s first processed inside the Guest OS, and then in the hypervisor storage subsystems, because each OS has their own storage subsystem. For ESXi, its network stack also has to do processing if it’s a IP-based storage.

[Image: ## Image Description

The diagram illustrates the **dual-processing of IO operations** across three layers: Guest OS vCPU 1, VM 1 vCPU 1, and VM 1 (hypervisor level). During **1st Processing**, the Guest OS vCPU shows "Utilization" while VM 1 vCPU 1 shows "Run" state; during **2nd Processing**, VM 1 vCPU 1 enters **"Other Wait"** (waiting for IO) while the VM-level (VMkernel) incurs a **"System"** charge as the hypervisor processes the IO independently. This visually demonstrates why the `cpu.system` counter is charged at the **VM level** (not vCPU 1) and why IO latency appears inflated to the Guest OS — it must wait for both processing phases to complete.]

ESXi typically uses another core for this work instead of the VM vCPU, and put that that VM vCPU in wait state. This work has to be accounted for and then charged back to the associated VM. The System counter tracks this. System counter is part of VMX world of the VM.
Guest OS isn’t aware of the 2nd processing. It thinks the disk is slower as it has to wait longer.
If there is snapshot, then the kernel has to do even more work as it has to traverse the snapshot.
The work has to be charged back to the VM since CPU Run does not account for it. Since this work is not performed by any of the VM CPU, this is charged to the VM CPU 0. The system services are accounted to CPU 0. You may see higher Used on CPU 0 than others, although the CPU Run are balanced for all the VCPUs. So this is not a problem for CPU scheduling. It’s just the way the kernel does the CPU accounting.
The System counter is not available per vCPU. Reason is the underlying physical core that does the IO work on behalf of the VM may be doing it for more than 1 vCPU. There is no way to break it down for each vCPU. The following vCenter screenshot shows the individual vCPU is not shown when System metric is selected.

[Image: ## Image Description

This is a VMware vCenter **Chart Options dialog** for a VM named "ARC," showing CPU performance counter configuration. The **"System" counter is selected** (highlighted in blue, checked) with Summation rollup, milliseconds unit, Delta stat type — while the individual vCPU breakdown options are not visible/available for this metric. The timespan is set to **Real-time (Last 1 Hour)** with a Line Graph chart type, demonstrating the text's point that the CPU System counter cannot be broken down per vCPU (unlike Run, Ready, or Swap Wait counters which appear above it unchecked).]

ESXi is also performing IOs on behalf of all VMs that are issuing IOs on that same time, not just VM 1. The kernel may serialize multiple random IO into sequential for higher efficiency.
Note that I wrote to CPU accounting, not Storage accounting. For example, vSphere 6.5 no longer charges the Storage vMotion effort to the VM being vMotion-ed.
Majority of VMs will have System value less than 0.5 vCPU most of the time. The following is the result from 2431 VMs.

[Image: The pie chart displays the distribution of maximum CPU System time values across 2,431 production VMs over a 4-month period, with **95.89% (2,331/2,431 VMs)** having a peak System time of **0–5 seconds**, and the remaining ~4% distributed across higher ranges (5–10s at 1.97%, 10–20s at 0.99%, 20–40s at 0.58%, and 40–1,000s at ~0.58%). The data demonstrates that nearly **98% of VMs never exceed 10 seconds of CPU System time** at their worst recorded peak, which equates to less than half a vCPU of kernel-level overhead. This supports the surrounding text's claim that ESXi System CPU consumption is negligible for the vast majority of VMs, validating that kernel I/O processing on behalf of VMs rarely becomes a significant performance concern.]

On IO intensive VM like NSX Edge, the System time will be noticeable, as reported by this KB article. In this case, adding more vCPU will make performance worse. The counter inside Linux will differ to the counter in vSphere. The following table shows high system time.

[Image: ## Image Description

The table displays CPU System time (in milliseconds) across VMs provisioned with different vCPU counts (2, 4, and 32 vCPUs), sorted in descending order by System time. Notably, the highest System times belong to the **32 vCPU VMs** (74,124 ms and 68,004 ms), significantly exceeding the 4 vCPU entries (33,230–39,645 ms) and the 2 vCPU entry (27,066 ms). This demonstrates the counterintuitive behavior described in the surrounding text: **adding more vCPUs increases System CPU time** on IO-intensive workloads (such as NSX Edge), making performance worse rather than better.]


#### Reservation


[Image: ## Image Description

This screenshot shows the **CPU configuration panel** for a VMware vSphere Virtual Machine, displaying:

- **CPU count**: 2 vCPUs
- **Reservation**: **888 MHz** (a specific non-default value)
- **Limit**: Unlimited (in GHz)
- **Shares**: Normal / 1000

In the context of the surrounding text about **CPU Reservations**, this image illustrates that reservations are configured in **MHz/GHz units rather than vCPUs**, which is the key point being made — that when a VM is migrated via vMotion to an ESXi host with a different CPU frequency, the reservation value (888 MHz in this example) must be **manually adjusted** to maintain the intended resource guarantee.]

The number is only available in MHz or GHz, not in vCPU. That means when you move the VM to an ESXi of different frequency, you need to adjust the number manually.

### Quiz!

By now I hope you vrealize that the various “utilization” metrics in the 4 key objects (Guest OS, VM, ESXi and Cluster) varies. Each has their own unique behaviour. Because of this, you are right to assume that they do not map nicely across the stack. Let’s test your knowledge 😊

#### VM vs ESXi

Review the following chart carefully. Zoom in if necessary.

[Image: ## Image Description

The VMware vCenter Advanced Performance chart displays three CPU metrics for **ISTAv2_host-sized** VM over ~1 hour (4:33–5:33 PM, 8/16/2020): **Used** (blue, summation in ms, avg 247K ms), **Run** (black, summation in ms, avg 330K ms, max 479K ms), and **Usage** (green, average %, max 62.44%, avg 51.46%). 

The chart demonstrates a **stepped ramp-up pattern** where CPU Run and Used times increase incrementally from ~240K ms to ~480K ms, while Usage (%) rises from ~45% to ~62%, before all metrics drop sharply at 5:30 PM. 

This illustrates the **divergence between VM-level CPU metrics** (Run/Used in ms) and the percentage-based Usage metric, which is central to the quiz about why utilization values don't map cleanly across the stack — notably, Usage plateaus near 60% rather than reaching 100% despite the VM consuming nearly all available CPU cycles on the 12-core/24-thread host.]

The vCenter chart above shows a VM utilization metrics from a single VM. The VM is a large VM with 24 vCPUs running controlled CPU test. The power management is fixed so it runs at nominal clock speed. This eliminates CPU frequency scaling factor.
The ESXi only has 12 cores. Hyper threading is enabled, so it has 24 threads.
The VM starts at 50% “utilization”, with each vCPU pinned to a different physical core. It then slowly ramps up over time until it reaches 100%.
Can you figure out why the three metrics moved up differently? What do they measure?
Now let’s look at the impact on the parent ESXi. It only has a single VM, but the VM vCPU matches the ESXi physical cores. The ESXi starts at 50% “consumption”, then slowly ramp up over time until it reached 100%.

[Image: ## Advanced Performance Chart Analysis

The chart displays three CPU metrics for ESXi host **cs-tse-d93.csl.vmware.com** over a ~1-hour real-time window (4:33–5:33 PM, 8/16/2020): **Usage** (blue, average 91.63%), **Core Utilization** (green, average 91.681%), and **Utilization** (black, average 69.03%). All three metrics start near 50% around 4:38 PM and steadily climb to 100%, but **Utilization lags significantly behind** the other two metrics throughout the ramp-up. This divergence demonstrates that Core Utilization and Usage move in tandem (both reflecting actual physical core consumption), while Utilization accounts for hyperthreading threads — since the VM's vCPUs are pinned one-per-core with HT enabled, Utilization normalizes against the full 24-thread capacity rather than just 12 physical cores, producing a lower reported value (~69% average vs ~91%).]

Can you figure out why Usage moves in tandem with Core Utilization, but Utilization moved up differently? What do they measure?
Let’s break it down…

##### At the start of the test

The VM runs 12 vCPU, but each vCPU was pinned to each ESXi core. So all cores are 100% utilized, but each running 1 thread.
VM CPU Run (ms) is 240K milliseconds, which is 20K milliseconds x 12 (half of its 24 vCPU).
VM CPU Used (ms) is also at 240K milliseconds. There is no loss from overlap, the VM does not do much IO, and no efficiency loss/gain due to HT.
VM CPU Usage is 50%.
So at this point, all 3 metrics of VM CPU are 50%.
The counter at ESXi tells a different story. The ESXi Core Utilization (%) immediately went up to 100% while Utilization went up to only 50%. The reason is Core Utilization measures whether the core is used or not. It takes a different perspective.
Usage (%) is identical to Core Utilization in this case, because CPU frequency is static.
On the other hand, ESXi Utilization (%) looks at if each thread HT is running or not. It does not care about the fact that the 2 threads share a core, and simply roll up to ESXi level directly from thread level. This is why it’s showing 50% as it only cares whether a thread is running or not, at any point in time.

##### During Ramp Up period

VM is being ramped up steadily. You can see all 3 metrics went up in steps.
VM CPU Run (ms) ramps up from 240K to 480K. All 24 vCPU has 20K ms value, which equals to 100%.
VM CPU Used (ms) barely moved. From 240K to 300K. That’s 1.25x, demonstrating that Used understands HT only delivers 1.25x throughput.
VM CPU Usage (%) ramp up from 50% to 62.5%, also demonstrating awareness of contention due to HT.
Used (ms) = Usage (%)
ESXi CPU Usage (%) counter stayed flat at 100%. The reason is all 12 cores were already busy and the metric is capped at 100%. That means VM CPU Usage (%) is aware of HT, but ESXi CPU Usage (%) is not.
ESXi CPU Core Utilization (%) matches VM Run. Both went 2x.

##### Towards the end of the run

VM CPU Run is at 480K ms. This counter is suitable for VM Capacity sizing, as it correctly accounts that each vCPU is used by Guest OS.
VM CPU Used is at 300K milliseconds, which is 62.5%.
VM CPU Usage (%) is at 62.5%. On average, each of the VM vCPU only gets 62.5%. If you use this for your VM capacity, you will get the wrong conclusion as it’s already running 100%
ESXi CPU Usage (%) is at 100%. This makes it suitable from Capacity viewpoint, albeit too conservative. It is not suitable from Performance, as you cannot tell if there is still room.
ESXi CPU Utilization (%) is at 100%. Because it tracks the ramp correctly, it can be used from Performance. You can use it for capacity, but take note that 100% means you get performance hit from. In fact, at 50% the HT effect will kick in.

#### When Run is lower than Used

Take a look at this VM. It’s a single vCPU, so co-stop is not applicable.
The ESXi clock speed is 2.095 GHz, so the VM has a capacity of 2.095 GHz. A limit is imposed at 2 GHz.
What’s your conclusion on the Demand and Usage counters?
They are basically identical, hovering around 1.96 GHz. If you use the 2.095 GHz as the 100%, basically both counters are flat around 94%.
Why are they similar? Shouldn’t Demand be higher?

[Image: ## Image Description

The chart displays four CPU metrics for **avi-poc-dops1-N7eV** over approximately 24 hours (Jan 5 3:00 PM to Jan 6 3:00 PM), captured at 10:42:51 AM. The metrics shown are:

- **Total Capacity: 2.1 GHz** (flat blue line at top)
- **Effective Limit: 2 GHz** (flat pink line)
- **CPU Usage: 1.9574 GHz** and **CPU Demand: 1.95693 GHz** (both nearly identical, fluctuating ~1.95 GHz)

This demonstrates a scenario where a **2 GHz CPU limit is imposed** on a VM with 2.1 GHz total capacity, causing Usage and Demand to converge at ~1.96 GHz (~93% of capacity), with Demand not significantly exceeding Usage — contrary to typical expectations — because the limit prevents the VM from consuming more CPU, effectively suppressing Demand to match Usage.]

Now let’s see the Used (ms) metric.
It’s also flat, around 18600 ms. Using the 20000 as the 100%, it’s around 93%. This is fairly expected, as I think Usage (MHz) contains non vCPU worlds (e.g. MKS)
Now let’s plot Run (ms) alongside. Why is it much lower?

[Image: The chart displays two CPU metrics for **avi-poc-dops1-N7eV** over a ~24-hour period: **CPU|Used (ms)** hovering consistently near **18,621 ms** (~18K) and **CPU|Run (ms)** significantly lower at ~**13,217 ms** (~13K). The tooltip captured at Saturday, Jan 6, 09:02:47 AM highlights the gap between the two metrics. This visualization demonstrates the ~41% differential between Used and Run counters, which the surrounding text attributes to **CPU Ready time** — since Used ≈ Run + Ready + Overlap + Idle = 20,000 ms (the total for a 2-vCPU VM over a 20-second sampling interval).]

Why is Used consistently 41% higher than Run?
Answer is CPU Ready.
If you sum up Run + Ready  + Overlap + Idle, it will be 20000.

[Image: ## Image Description

The chart displays CPU metrics for VM **avi-poc-dops1-N7eV** on Saturday, Jan 6 at 03:38:01 PM, showing a stacked area graph with four metrics: **CPU|Run (ms) at 13,196.6**, **CPU|Ready (ms) at 6,802.47**, **CPU|Overlap (ms) at 2.87**, and **CPU|Idle (ms) at 0.13**. The data shows a dramatic spike beginning around 3:00 PM where both Run and Ready metrics surge significantly — Run (pink) reaching ~13K ms and Ready (teal) reaching ~6.8K ms. This demonstrates the surrounding text's claim that **Run + Ready + Overlap + Idle ≈ 20,000 ms** (the total vCPU time budget), and specifically illustrates why Used is higher than Run — the substantial CPU Ready time (~6,802 ms, or ~34% of the 20,000 ms budget) represents time the VM was waiting for physical CPU resources.]


#### When Run is higher than Used

Now let’s look at the opposite scenario.
This VM is a 64-bit Ubuntu running 4 vCPU. Used (ms) is around 44% of Run (ms). The VM had minimal System Time (ms) and Overlap (ms), so Used is basically lowered by both power savings and CPU SMT.

[Image: ## Image Description

The chart displays two CPU metrics for a VM named "atl-se-g\*\*b-cat-2" over a ~7-day period (Feb 20–27): **CPU|Run (ms)** in purple hovering consistently around **24,000–25,000 ms** and **CPU|Used (ms)** in pink consistently around **11,000–12,000 ms**. This demonstrates the scenario where **Run is significantly higher than Used** (~44% ratio), illustrating the impact of **power management and CPU SMT (Simultaneous Multi-Threading)** reducing the effective Used time relative to actual Run time, with minimal CPU Ready or contention metrics present.]

In this example, if Run is far from 100% and the application team want faster performance, your answer is not to add vCPU. You should check the power management and CPU SMT, assuming the contention metrics are low.

## ESXi

Throughout this book, I always cover the contention metrics first, then consumption. Why is it that I swap the order for ESXi Host?
Because in the provider layer there is no contention. The one that faces contention is the consumer (VM).

### Consumption Metrics

vSphere Client UI provides 6 counters to track ESXi CPU “consumption” and 1 to track reservation.

[Image: ## Image Description

The image displays a table of **6 ESXi CPU consumption counters** from vSphere, listing: **Core Utilization, Demand, Usage, Usage in MHz, Used, and Utilization**. Each counter specifies its rollup method (Average or Summation), units (%, MHz, or ms), stat type (Rate, Absolute, or Delta), and a brief description. The table contextualizes why multiple distinct metrics exist — they measure CPU consumption differently (e.g., **Usage** tracks percentage during interval, **Demand** tracks MHz as Absolute, **Used** tracks total CPU in ms as Delta), setting up the subsequent quiz about why the same host can simultaneously report ~50%, 75%, and 100% utilization depending on which counter is observed.]

Why 6?
Let’s dive into the utilization metrics with a quiz.

#### Quiz: 50% or 75% or 100%?!

Hope you like the tour of VM CPU accounting. Can you apply that knowledge into ESXi and explain the following?

[Image: ## Image Description

The image shows a **VMware vSphere CPU performance chart** for an ESXi host over a 1-hour window (11/26/2020, 2:23–3:23 PM), displaying three CPU metrics: **Usage** (blue, peaks at 100%, average 78.4%), **Utilization** (black, latest 54.38%, average 35.77%), and **Core Utilization** (green, latest 84.94%, average 58.8%). All three metrics start near zero, spike sharply around the midpoint, then stabilize at divergent steady-state values — blue saturates at 100%, green settles ~70–75%, and black stabilizes ~50%. This demonstrates the quiz premise: three different consumption metrics report dramatically different utilization values simultaneously for the same ESXi host, illustrating why metric selection is critical and how **Usage can hit its 100% cap** while other metrics still show available headroom.]

The above is an ESXi host, showing 3 types of utilization metrics.
- One shows ~50%, indicating you have capacity.
- The second one shows 100%, indicating you do not have capacity. BTW, this was the old version, where the metric was capped at 100%.
- The 3rd shows ~70%.
Which metrics do you take for the ESXi CPU “consumption” then?
They also do not move in tandem. Towards the end, both the black line and green line fluctuate, but the blue one was flat at 100%. Why?
Since the graph is a bit small, let’s zoom in:

[Image: ## Image Description

The chart displays three CPU metrics for an ESXi host (eldwc910010n.ldn.swissbank.com) over time on 11/26: **Usage** (blue, ~100% at peak), **Utilization** (black, ~47-50% at peak), and **Core Utilization** (green, ~70% at peak). All three metrics show a similar pattern — low/idle in the middle period, a spike early, then a sharp sustained climb toward the end — but with significantly different magnitudes. This image demonstrates the **divergence between CPU metrics under high load**, specifically illustrating why Usage can be saturated at 100% while Utilization remains ~47%, raising questions about which metric accurately reflects true CPU consumption capacity.]

Notice they have similar pattern, but their sensitivity differs.
- Why is Usage (%) = 100% when Utilization (%) is around 47%? The gap is more than double. What could be causing it?
- Why is Utilization (%) fluctuating yet Usage (%) remains constant? Notice both Utilization varies between 45% and 55% while Usage remains flat at 100%
- Why is Core Utilization (%) in the “middle”? What does it actually measure then?

##### High Load Example

The preceding example shows Utilization (%) mostly below 50%. Let’s pick the opposite example, where at least half the threads are utilized. What do you expect the value of Usage (%) and Core Utilization (%)?

[Image: The chart displays three CPU metrics over a ~42-hour period (Dec 4–5): **CPU Usage (%)** (teal, ~125%), **CPU Core Utilization (%)** (blue/purple, ~97–98%), and **CPU Utilization (%)** (pink/lavender, trending upward from ~75–80% to ~88–90%). The pink highlights (drawn annotations) mark two periods where CPU Utilization (%) was relatively stable at ~75–78% early on, then elevated at ~88–90% later on Dec 5. This demonstrates the high-load scenario described in the text: as Utilization (%) rises toward 90%, Core Utilization (%) approaches 100%, while Usage (%) remains consistently above 100% (indicating sustained above-nominal clock speeds).]

Notice the Utilization (%) metric went up from ~80% to 90%.
At around 80%, not all cores are running all the tiem. This means a few cores were idle, despite most cores running both threads. Yes, that indicate imbalance.
As Utilization (%) reach 90%, the Core Utilization got closer to 100%, which is the limit.
Usage (%) was constantly above 100%, as it’s compared with the base frequency. This indicates the CPU was constantly running above the nomimal speed. Notice the pattern of Usage is not as volatile as Utilization (%). The reason is hyperthreading only gains 1.25%.

##### Analysis

Unlike RAM, CPU performance varies widely among different CPU models. Speed matters in CPU, whereas in RAM we can generally ignore it. DDR5 RAM is faster than DDR4 but for general monitoring reason it can be ignored. Because of this significant difference in CPU, we need to have metrics to account for:
- How often it runs. 
How much the CPU runs in a time period. E.g. if it runs 60% of the time in the last 100 seconds, that means it runs for 60 seconds accumulatively in that period. That’s why you see many metrics in millisecond. They track the consumption over time.
- When it is running, how fast is the run. 
All else being equal, a 5 GHz CPU is 5x faster than a 1 GHz CPU. Throughput impacts utilization. The faster it can complete a task, the shorter it has to work. That’s why you see some metrics in MHz.
- When it is running, how efficient is the run. 
CPU SMP impacts the core efficiency. This efficiency is then translated into MHz, for ease of accounting. Unfortunately, this simplification creates confusion as HT and Power Management are not the same thing.
These 3 dimensions of run are the reason why CPU consumption is hard to measure. It becomes “it depends on what you consider”. It can’t be a single number. Insisting that the CPU has a single, static, total capacity and use this as the only 100% for all use cases will result in confusion in “consumption” numbers.

#### Thread Utilization

It’s easier to think the metric Utilization (%) as Thread Utilization (%), so I’m going to refer to it as such.
You’re welcome.

| At a thread level | This is the most basic counter. It’s the ESXi equivalent of VM CPU Run.  It tracks at a single physical thread level. At any given moment, a thread is either running (unhalted) or not (halted). So it’s binary (0% or 100%). Using a human analogy, think of it as a person who is either running or standing, and never walking. It’s not considering CPU Frequency nor HT. Over a time period, the value is averaged. So when you see the number as 50%, it does not mean it’s running 100% at half the “speed”. It means it’s running half the time, which is why the original counter is in millisecond and not percentage.  This metric is only relevant when hyper-threading is enabled. |
| --- | --- |
| At a core level | Core Utilization, as the name implies, rolls up at the core level. It is a simple metric.  If one of the threads is running, then this metrics reports 100%. This is logical as the core is indeed running. If both are running, this metrics also reports 100%. I agree that reporting the same number on 2 different scenarios will certainly cause confusion. |

Let’s apply the above into an example. We start with a single core of a physical socket. The socket may have many cores; we are just interested on 1 core only. The core has 2 threads as it supports CPU SMT.
In a time period of say 20 seconds, this core had the following consumption:

[Image: The image illustrates CPU utilization behavior on a single physical core with two hyperthreads (HT 0 and HT 1) over a total elapsed time window. It shows that HT 0 runs during the first and last segments while HT 1 runs during the second and last segments, with a gap in the middle where neither thread runs (Core runs 0%), and three segments where the core runs at 100%. The diagram emphasizes that CPU utilization is binary at any given instant (a thread either runs or does not), and that percentage metrics are derived by converting active milliseconds across a measurement window — contextualizing how thread-level and core-level utilization percentages are calculated in the surrounding example (50% per thread, 75% overall core utilization).]

Going back to our example, here are metrics reported:
- Thread Utilization (%) for HT 0 = 10 seconds / 20 seconds = 50%
- Thread Utilization (%) for HT 1 = 10 seconds / 20 seconds = 50%
- Core Utilization (%) for entire core = 15 seconds / 20 seconds = 75%
BTW, in vSphere Client performance tab, you can’t select a core if you enable HT. You can only choose PCPU, which is a thread. So what happens on the Core Utilization counter at thread level?
Does it get split into half?
As you can see below, no. The value is duplicated.

[Image: The chart displays **Core Utilization (%)** for two objects (Object 0 and Object 1) over approximately 55 minutes on 10/26/2021, with values fluctuating between ~30% and ~91%. Both objects show **identical statistics**: Latest = 68.96%, Maximum = 90.67%, Minimum = 30.47%, and Average = 64.279%. This demonstrates the book's point that Core Utilization is **duplicated across both HT threads** rather than split, meaning both logical CPUs (threads) on the same physical core report the same core-level utilization value.]

Notice in the above chart, the 2 have identical value.
Thread Utilization (%), on the other hand, will be different. Each thread has different value.

[Image: The chart displays **CPU Utilization (%)** for two objects (Object 0 and Object 1) measured as Thread Utilization over approximately one hour on 10/26/2021 from 12:00–12:55 PM. Object 0 (purple) shows Latest: 42.34%, Maximum: 72.48%, Minimum: 22.15%, Average: 44.762%, while Object 1 (blue-gray) shows Latest: 24.93%, Maximum: 61.97%, Minimum: 12.4%, Average: 36.857%. This demonstrates that **Thread Utilization differs between the two HT threads** on the same core — contrasting with Core Utilization, which was shown previously to be duplicated identically across both threads.]

If you simply sum them up, you get more than 100%, so don’t! Their context is a single thread.

[Image: ## Image Description

The chart displays **Thread Utilization (%)** for two CPU threads (Object 0 and Object 1) on 10/26/2021 between 12:05 PM and 1:00 PM, showing that the two threads have **distinctly different values** — Thread 0 averages **44.749%** (max 72.48%) shown in purple, while Thread 1 averages **36.937%** (max 61.97%) shown in blue-gray. This contrasts with the preceding Core Utilization chart where values were duplicated/identical across threads, demonstrating that **Thread Utilization is measured independently per thread**, reflecting actual per-thread workload differences. The key point illustrated is that summing these two thread utilization values would exceed the meaningful 100% boundary, as both threads share the same physical core context.]

Now let’s roll this up to the ESXi level. The following shows a tiny ESXi with 2 cores, where each core has 2 threads.

[Image: The image illustrates CPU utilization metrics for a 2-core ESXi host, where each core contains 2 PCPUs (hyperthreads). Core 0 shows PCPU 0 and PCPU 1 each at 50% utilization but a Core Utilization of 75% (due to overlapping active periods), while Core 1 shows PCPU 0 at 100%, PCPU 1 at 0%, and Core Utilization at 100%. This demonstrates how Core Utilization (%) differs from and typically exceeds Thread Utilization (%) because it accounts for the physical core being active whenever *either* thread is running, rather than averaging independent thread activity.]

The metrics at ESXi level is
- CPU Thread Utilization (%) = (50% + 50% + 100% + 0% ) / 4 = 50%.
- CPU Core Utilization (%) = (75% + 100% ) / 2 = 87.5%
Thread Utilization = 50% because each thread is counted independently. There are 4 threads in the preceding ESXi, each runs 50%, so the average at ESXi level is 50%. This counter basically disregards that HT does not deliver 2x the throughput.
This is why the Core Utilization (%) will tend to be consistently higher than Thread Utilization (%). The following chart demonstrate that.

[Image: ## Performance Chart: CPU Utilization vs. Core Utilization

The chart displays two metrics for host **192.168.233.149** over a ~55-minute window on 10/26/2021: **Thread Utilization** (purple, averaging **42.525%**, max **61.61%**) and **Core Utilization** (blue-gray, averaging **65.37%**, max **83.43%**).

The data visually demonstrates the key concept from the surrounding text: **Core Utilization consistently runs higher than Thread Utilization** — in this case by roughly **20-23 percentage points** on average — because Core Utilization accounts for the reduced throughput efficiency of Hyper-Threading, while Thread Utilization treats each logical thread as a fully independent unit, effectively underreporting actual CPU demand.]

Now let’s go back to the chart shown earlier. Can you now explain Thread Utilization (%) and Core Utilization (%)?
Great! Let’s move to the next one.
In the following example, this ESXi has no hyper-threading. What do you notice?

[Image: ## Image Description

This VMware vSphere Advanced Performance chart displays **CPU Core Utilization and Thread Utilization** for host **192.168.233.80** over a 1-hour real-time period (2:56 PM – 3:56 PM on 3/19/2021). Both metrics show nearly **identical values** — Latest: ~10.66-10.67%, Maximum: 16.28%, Minimum: 5.48-5.49%, Average: 9.998% — with the line graph showing consistent low utilization fluctuating primarily between 5-20%.

In context, this chart demonstrates an **ESXi host with Hyper-Threading disabled**, which is why Core Utilization and Thread Utilization are **essentially identical** — there is no HT multiplier effect to cause divergence between the two counters, confirming the expected behavior stated in the surrounding text.]

Yup, the Core Utilization is identical with Thread Utilization.

#### Core vs Thread


[Image: ## Image Description

The chart illustrates the relationship between **Core Utilization (%)** and **Thread Utilization (%)** on a system **with Hyper-Threading enabled**, where the two metrics diverge. Core Utilization (marked with a green star at **100%**) peaks earlier and higher than Thread Utilization, which only reaches 100% at the far right endpoint — demonstrating that Core Utilization consistently exceeds Thread Utilization under HT. The red shaded region between the two lines visually represents the **gap/delta** between the metrics, with a notable inflection point at approximately **50% Thread Utilization**, after which the dotted line shows Core Utilization declining toward convergence.]


[Image: This image displays a **legend/key** for a Core vs Thread utilization matrix or heatmap used in VMware vSphere performance analysis. It defines five color-coded states: a **green star** (all cores fully utilized, idle cores existed before this point), **light pink** (≥1 core running 2 threads while ≥1 core remains idle — suboptimal scheduling), **salmon/red** (≥1 cores running 2 threads — HT contention, performance risk), **gray** (impossible/non-existent metric combinations), and **black** (Cluster HA buffer zone — reaching this causes availability-driven performance degradation). In context, this legend supports the explanation of how HT (hyper-threading) thread-to-core rollup creates complexity when interpreting Core Utilization vs Thread Utilization counters.]

HT and power management is done at core level. This creates complexity in rolling up the counters at thread level to core level.
Let’s start. The basic unit is time, expressed in 20000 ms.
20000 ms = 100% at the core level. This means the value remains 20000 if you disable HT.
Since there are 2 threads, what happens when both are idle?
You assigned Idle = 10000 ms for each.
When one of the threads is running hot, the highest the Used value of the thread can go is 20000. This means the CPU frequency doubles. What happens to the paired thread then? Does it show 0 ms? I am yet to test here.
At thread level, 100% Used = 20000 ms, while 100% Idle = 10000 ms. This creates confusion when you work at thread level.

#### Idle

Before we cover more advance consumption metrics, we need to cover Idle. The reason is idle + non idle should add up to 100%. Knowing what defines 100% is crucial.
If HT is enabled, Idle is capped at 10000 ms at a thread level. The following example shows an ESXi with 64 threads that is basically idle. Notice none of the threads passes 10000 ms. The table shows maximum value of 9998, not exactly 10000. I suppose the 2 ms is the kernel just humming along.

[Image: ## Image Description

The chart displays **CPU Idle metrics (in milliseconds) at the thread level** for multiple ESXi threads (Objects 22, 23, 44, 58, 59) over approximately one hour on 12/19/2023 (12:25 PM – 1:20 PM). All threads consistently hover near the **10,000 ms ceiling**, with periodic sharp dips reaching as low as **~7,458 ms minimum**, and a maximum of **9,998 ms** across all objects. This demonstrates that when HT is enabled, idle time is capped at ~10,000 ms per thread, confirming the host is in a near-idle state, with the 2 ms deficit from 10,000 representing minimal kernel overhead.]

The above translates that the total per core should be 20000, since there are 2 threads per core.
You can confirm the above ESXi is idle by plotting idle at the host level. The sum is near 640000 ms.

[Image: The chart displays the **CPU Idle time (Summation) in milliseconds** for ESXi host `w2-hs4-r1207.eng.vmware.com` over approximately one hour on 12/19/2023 (12:25 PM – 1:25 PM), showing values oscillating between ~631,128 ms (minimum) and ~638,205 ms (maximum), with a latest value of 637,631 ms. The metric hovers near **640,000 ms**, which confirms the host is essentially idle, as the aggregate idle time across all threads approaches the theoretical maximum (64 threads × 10,000 ms = 640,000 ms). The regular periodic dips in the chart represent brief intervals of CPU activity but the values quickly return near the maximum, reinforcing the idle state described in the surrounding text.]

If HT is not available, then there is no counter at thread level. The counter at the core level adds up to 20000 ms.

[Image: ## Image Description

The chart displays **CPU Idle and Used metrics (in milliseconds) for a single core** over approximately one hour (8:40–9:35 AM on 05/04/2025), with the legend showing Idle averaging **13,973 ms** (max 16,725, min 1,399) and Used averaging **6,027 ms** (max 18,606, min 3,276), both using Summation rollup. The two metrics together consistently approach the **20,000 ms ceiling** (confirming 2 threads × 10,000 ms per interval), with Idle dominating the area chart in purple and Used shown in blue-gray above it. This confirms the surrounding text's assertion that a 2-thread (HT-enabled) core has a total capacity of 20,000 ms, and illustrates the inverse relationship between Idle and Used time.]


#### Used | Usage

You are now ready to tackle the next metrics, which are Used (ms), Used (%), Usage (%) and Usage (MHz). Used (%) is used in esxtop, while vSphere Client UI uses the other 3 metrics.
vSphere Client uses the name Used instead of Usage. But in the metrics chart page, it uses Usage. As a result, I’m going to assume that Used (MHz) = Usage (MHz) as vSphere Client UI uses them interchangeably. While I’ve found differences in rare cases, it is safe to take as Usage = Used.
I only see the use case for Usage (MHz). The other 2 units (second and percentage) are not needed. Using millisecond is hard to account for “how fast you run” and “how efficient you run”. With MHz, we gain an additional dimension, which is speed. We can plot the speed across time.
If you have a specific need on Used (ms), Used (%) and Usage (%), reach out to me with the reason and happy to provide the documentation on these 3 metrics.
Usage (MHz) relates to Utilization in a similar way that VM Usage metric relates to VM Run metric. The difference is a physical thread does not experience overlap, and system is not applicable as it’s run in the kernel.
Here is how Utilization and Usage are related at PCPU level:

[Image: The diagram illustrates the relationship between **CPU Utilization (%)** and **CPU Used** metrics at the physical CPU (PCPU) level over time, showing that `CPU Used = Utilization (%) + Efficiency`. It depicts a physical thread's lifecycle across three states — **Halted** (idle, shown in orange/purple), **Execution** (active, shown in green/teal) — where CPU Utilization measures only the active execution window, while the broader "CPU Used" metric also incorporates efficiency factors including **Power Saving** (reduced clock speed) and **Turbo Boost** (elevated clock speed) during execution. This contextualizes why the Usage (MHz) metric captures more than raw utilization, accounting for clock speed variations via hardware counters like Non-Halted Core Cycles (NHCC).]

Used is calculated based on a hardware counter called Non-Halted Core Cycle (NHCC). Logically, the higher the CPU clock speed, the more cycles you complete. That’s why the value gets higher in turbo boost.
From the diagram above, you can see that Usage accounts for 2 factors that Utilization does not:
- A physical thread is either executing (running) or halted (idle). Its execution will be less efficient if its paired thread is also running at the same time.
- While it’s running, it can run at lower/higher CPU clock speed due to power management.

##### Usage

vCenter adds this counter, meaning it does not exist at ESXi level.
You see both the Capacity of 35.18 GHz and Used of 11.3 GHz. There is no concept of Usable Capacity in vSphere, so the Free amount is basically Capacity – Used.

[Image: ## Image Description

This screenshot shows the **Summary tab of an ESXi host (192.168.233.149)** in VMware vCenter, running **VMware ESXi 6.7.0** on a **Dell EMC PowerEdge R620** with dual Intel Xeon E5-2660 processors (32 logical processors). The resource utilization metrics show **CPU at 11.3 GHz used out of 35.18 GHz capacity** (Free: 23.89 GHz), **Memory at 178.9 GB used out of 255.96 GB**, and **Storage at 2.85 TB used out of 3.88 TB**. In the context of the surrounding text, this image illustrates how vSphere calculates **CPU capacity as base frequency × number of cores** (2.20 GHz × 16 cores = 35.18 GHz), explicitly excluding turbo boost and hyperthreading from the reported capacity figure.]

The Used CPU is summary.quickStats.overallCpuUsage.
The value above is likely some average of say 5 minutes as it remains static for a while, and it does not exactly match the number below as the roll up period is not the same.

##### Usage and 100%

Usage no longer capped at 100% of total capacity at the nominal frequency. This was fixed in Aria Operations 8.18. In a highly utilized host, you will see Usage exceed it. This is indeed a desirable situation as you bought the host to be used as much as possible.

[Image: ## Image Description

The chart displays three CPU metrics for ESXi hosts over a ~6-hour period (4:30 PM–10:00 PM on Monday, Dec 15): **CPU|Usage (%)** at **124.54%** (blue), **CPU|Core Utilization (%)** at **97.09%** (teal), and **CPU|Utilization (%)** at **81.26%** (purple), captured at the 6:54 PM tooltip. All three metrics show a sharp decline beginning around **9:00–9:15 PM**, dropping from their sustained levels (~120, ~90, ~75 respectively) to significantly lower values. This directly illustrates the surrounding text's point that **CPU Usage is no longer capped at 100%**, with the blue Usage line clearly exceeding 100% throughout the monitored period, demonstrating that highly utilized hosts can and should report Usage values above 100% since vSphere 8.18.]


#### Consumed

When vSphere UI lists ESXi Hosts, it typically includes the present utilization. It lists the metrics as Consumed CPU (%) and Consumed Memory (%).

[Image: The image shows the **vSphere UI Hosts view** for cluster **sc2c01**, listing three ESXi hosts (b1613, b1612, b1608) all in Connected/Normal state with 643 days uptime. Key metrics displayed are **Consumed CPU%** (19%, 10%, 9%) and **Consumed Memory%** (51%, 60%, 45%), alongside HA State (one Running Master, two Connected Slaves). This screenshot directly illustrates the context that vSphere UI presents current host utilization using the "Consumed CPU %" and "Consumed Memory %" column labels referenced in the surrounding text.]

Consumed CPU maps to CPU Usage (%). Consumed Memory (%) maps to Memory Consumed (KB).
To confirm it, simply plot CPU Usage value. The last value is what you see at the table.

[Image: This image shows a **VMware vSphere real-time CPU performance chart** for host **sc2-hs2-b1613.eng.vmware.com** over a ~1-hour window (7:39–8:38 AM on 09/30/2021), displaying CPU Usage (%) with an Average rollup. The CPU utilization remains consistently low and stable at approximately **19–20%**, with brief spikes reaching a maximum of **26.45%** around 8:03–8:08 AM, and an overall average of **19.913%**. This chart demonstrates how CPU Usage (%) corresponds to the "Consumed CPU (%)" metric visible in the vSphere UI, with the latest value of **19.35%** confirming the real-time correlation between the chart and the host listing table.]

You also see them in vSphere Host Client.

[Image: The image shows the **VMware ESXi Host Client** displaying the **Performance > CPU monitor** for host `blrcolo-hs1-h0808.eng.vmware.com`, plotting **Consumed host CPU (%)** over the **last hour** (15:35–16:00). CPU utilization remains consistently near **0%** throughout the entire period, with only minor periodic spikes barely above zero. This screenshot demonstrates the CPU Usage (%) metric as viewed in the vSphere Host Client, with 6 VMs registered and the breakdown visible per CPU package, contextualizing the "Consumed" metric discussion.]

As a bonus, you get the breakdown by CPU package.

#### Demand


[Image: This screenshot shows the **vSphere performance chart configuration interface** for CPU metrics, with the **Demand counter selected** (checked in blue). The Demand metric is configured with Average rollup, MHz units, internal name "demand," and Absolute stat type, displayed in Real-time timespan for the host **sc2-hs2-b1613.eng.vmware.com**. This image contextually introduces the Demand counter within the CPU metrics section, illustrating how it differs from Usage/Utilization — measured in absolute MHz rather than percentage, and representing the consumer (VM) perspective rather than the provider (physical thread) perspective.]

This is an internal counter. It’s for the kernel CPU scheduler to optimize the running of VM as the kernel is aware that hyper-threading has performance impact. As a result, demand looks at different context than Utilization/Used. The value you see at ESXi is the summation of all the VMs, not physical threads.
Demand is consumer-view, while Usage is provider view. Now you know why Demand is not available on a per-core or thread basis. If a host has no VM, Demand will show flat 0. Usage will not show 0 as it includes the kernel.

[Image: ## Image Description

This VMware vSphere Advanced Performance chart displays **CPU Usage in MHz** for ESXi host `shd-e2e-esx22.vcfops.lvn.broadcom.net` over a one-hour real-time period (15/12/2025, 21:18–22:17). The purple line shows **Usage (MHz)** fluctuating between ~2,000–6,727 MHz with an average of **2,945 MHz**, while the **Demand metric shows a flat 0** across the entire period (Latest: 0, Maximum: 0, Minimum: 0, Average: 0). This directly illustrates the surrounding text's point that **Demand = 0 when no VMs are running**, while Usage remains non-zero because it includes kernel/hypervisor utilization — demonstrating the fundamental difference between the consumer-view (Demand) and provider-view (Usage) metrics.]

Demand includes the reservation by VM.
Usage includes kernel actual utilization. The following shows Demand remains perfectly flat at 10.21% for weeks. The ESXi has 0 running VM. The only explanation is the kernel reservation.

[Image: ## Image Description

The chart displays four CPU metrics for ESXi host **10.78.206.172** over approximately three weeks (Aug 16 – Sep 7): **CPU Demand (%)**, **CPU Usage (%)**, **CPU Contention (%)**, and **vCPUs Allocated**. The tooltip captured at **Friday, Aug 30, 07:00 PM** shows **Demand at a perfectly flat 10.21%** (the straight blue horizontal line), while **Usage fluctuates around 1-2%** (the noisy pink line) with a brief spike near Aug 30. This demonstrates the key concept from the surrounding text: **Demand remains artificially flat due to the ESXi kernel reservation**, even with no running VMs, while Usage reflects actual kernel utilization — explaining why Demand can exceed Usage when no workload is present.]

The following chart shows the same ESXi, where the Demand (MHz) = Overhead (MHz). Overhead tracks the kernel reservation.

[Image: ## Image Description

The chart displays CPU metrics for ESXi host **10.78.206.172** on Friday, Sep 6 at 02:00 AM, showing **CPU Demand (MHz) = CPU Overhead (MHz) = 3,257.99 MHz**, while CPU Contention, Reserved Capacity, and vCPUs Allocated on Powered On Consumers all equal **0**. The flat orange line near the 3K mark runs consistently from Aug 24 through Sep 7. This demonstrates the book's assertion that when no VMs are running (0 vCPUs allocated), Demand exactly equals Overhead, confirming that the Overhead metric tracks the ESXi kernel reservation, which accounts for the non-zero Demand value despite no active VM workloads.]

If the kernel reservation is lower than the kernel utilization, then Demand could be lower than Usage. The following example shows that.

[Image: ## Image Description

This VMware vSphere Advanced Performance chart displays **CPU Usage in MHz (blue line) vs. CPU Demand in MHz (black line)** for ESXi host **192.168.233.82** over a one-hour real-time period on 3/17/2021 (7:36–8:36 AM). The legend shows Usage averaging **1,587 MHz** (max 3,839 MHz) while Demand averages **803 MHz** (max 1,100 MHz), with Usage consistently and significantly **higher than Demand** throughout the monitoring window. This demonstrates the scenario described in the surrounding text where **Demand is lower than Usage** due to kernel utilization being higher than the kernel reservation, with insufficient VM co-scheduling contention to drive Demand above Usage.]

Once there is enough utilization, defined as some VMs are sharing the same cores, Demand will be higher than Usage. The following screenshot shows Demand being consistently higher

[Image: ## Image Description

The chart displays two CPU metrics for `sc2-hs3-i0724.eng.vmware.com` over approximately 4 days (Jun 28 – Jul 2): **CPU Demand (%)** in pink/magenta and **CPU Usage (%)** in blue. At the tooltip timestamp (Saturday, Jun 29, 02:04:56 PM), Demand reads **66.48%** and Usage reads **56.45%**, with both metrics showing a notable spike at that point reaching ~65%. 

This screenshot demonstrates the scenario described in the surrounding text where **Demand is consistently higher than Usage** (~55% vs ~45% baseline), indicating sufficient VM co-scheduling contention on shared cores — the opposite of the previous example where Demand was lower than Usage.]


#### Summary


[Image: ## Image Description

This diagram illustrates the relationship between CPU **"Time Taken"** metrics (VM vCPU Run %, ESXi Thread Utilization %, ESXi Core Utilization %) and **"Distance Travelled"** metrics (VM vCPU Usage MHz, ESXi Thread Usage MHz, ESXi Core Usage MHz), explaining that the Usage metric incorporates three factors: running time, efficiency, and speed. Using a 1 GHz base speed example, it demonstrates how Hyper-Threading efficiency works — where two VM vCPUs each consuming **625 MHz** map to two ESXi threads each at **625 MHz**, summing to **1250 MHz** at the ESXi Core level. It also notes that all five counters are volatile, typically **15-40% higher** due to Turbo Boost frequency scaling.]


##### Comparison

Let’s evaluate all the possible scenarios so you can compare the values returned by the metrics. We will use a simple ESXi with 2 cores. Each core has 2 threads. In each of the scenario, a thread is either running or not running. There is no partial run within a thread as that’s mathematically covered in our scenarios.
I will also use 20000 ms as that’s more familiar. The following table shows an ESXi with 2 cores. There are 6 possible permutations in their utilization.

[Image: ## Image Description

The table compares **CPU Utilization vs. CPU Used metrics** across 6 scenarios for a 2-core, 4-thread (HT) ESXi host, using 20,000ms as the measurement unit. Each scenario represents a different permutation of thread activity (100% or 0% utilization), showing raw millisecond values alongside percentage representations for both metrics. The key insight demonstrated is that **Used splits the Utilization value in half (10,000ms, highlighted in red) when both hyperthreads on a core are simultaneously active** (Scenarios 1, 2, and 4), while Utilization maintains the full 20,000ms per thread — illustrating the HT co-scheduling penalty that the Used metric accounts for.]

The table shows clearly that Used splits the Utilization into 2 when both threads are running.
Look at scenario 1. While Utilization charges 20000 ms to each thread, Used charges 10000. This is not intuitive as ESXi considers HT to deliver 1.25x. Personally I find 12500 easier to understand. The good news is this number is normalized back when it is rolled up to the ESXi host level.
How will those scenarios roll up at the ESXi level?
The following table shows the 4 metrics (Utilization, Used, Core Utilization, Usage). I have expressed each in % so it’s easier to compare.
There are 6 different scenarios, so logically there should be 6 different values. But they are not, so I added my personal take on what I like them to show. I’m keen to hear your thought.

[Image: ## Image Description

The table displays **6 scenarios comparing four VMware vSphere CPU metrics** (Utilization, Core Utilization, and Usage expressed as percentages) at the ESXi host level, alongside a custom "My Recommendation" formula. The scenarios range from full utilization (100%/100%/100%) down to idle (0%/0%/0%), with scenarios highlighted in green representing cases where **Hyper-Threading (HT) is active**. The "My Recommendation" column applies a formula averaging a HT-adjusted value (125%) with a base value, yielding results like **125.0% for Scenario 1** and **62.5% for Scenario 4**, demonstrating how standard vSphere metrics fail to consistently represent HT's **1.25x throughput bonus** across mixed utilization scenarios.]

What’s causing the difference?
Yup. Hyper Threading.
Why do I choose 125% instead of 100%?
To me, the 1.25x bonus factor has to be shown. Without HT, it’s 100%. HT is a bonus. While it provides 1.25x overall throughput, each thread pays an expensive price, as each suffers 37.5% penalty.

| Scenario | Analysis |
| --- | --- |
| 1 | Do you notice something strange with the value of Usage (%)? Yes, it’s no longer 50%. It’s 100%. The average of 50% is 100%. The reason is the accounting does not count each thread as 20000. Each core has 20000 and not 40000. If you say that is similar behaviour to Core Utilization, you’re right. |
| 3 | Utilization is only showing 50% when both cores are in fact already utilized. I prefer this to show 80% as HT only delivers 1.25x, not 2x. |
| 5 | Utilization is again showing too low a value. |

Now let’s add CPU clock speed. What happens when there is power management?
I’d focus on just Used and Usage to highlight the difference.
What do you notice from the table below?

[Image: ## Image Description

The image displays two comparison tables showing CPU **Frequency**, **Usage**, and a proposed metric **E1** across two frequency scenarios: **0.6x** (left table) and **1.3x** (right table). At 0.6x frequency, Usage ranges from 0–60% while E1 values align proportionally (0–75%), and at 1.3x frequency, Usage is **capped at 100%** in three rows (shown in red) while E1 correctly reflects values of **130–163%** (shown in blue). This demonstrates the core argument from the surrounding text: the standard **Usage metric artificially caps at 100%** and fails to represent true CPU utilization when clock speeds exceed baseline, whereas the proposed E1 metric remains uncapped and provides accurate capacity/demand insight.]

Usage is capped at 100%. I prefer this not to be capped, so you know its actual value. The good part is Demand metric is not.
For comparison, I put forth what I think the value should be.

##### Recommendation

The answer depends on the purpose: performance (VM-centric) or capacity (ESXi-centric)? Performance is about giving VM the highest quality resource (no HT), but capacity is about using all the resources (including HT).
Here is how the counters stack up in terms of sensitivity:

| Metric | Analysis |
| --- | --- |
| Utilization | The value shows 50% when it should report 80% |
| Core Utilization | The value goes up to 100% when it should report 80% |
| Usage | These 3 metrics are essentially the same.  The value is affected by CPU frequency. During low utilization it under-reports due to power savings, while during high utilization it over-reports due to turbo-boost. |
| Used | These 3 metrics are essentially the same.  The value is affected by CPU frequency. During low utilization it under-reports due to power savings, while during high utilization it over-reports due to turbo-boost. |
| Consumed | These 3 metrics are essentially the same.  The value is affected by CPU frequency. During low utilization it under-reports due to power savings, while during high utilization it over-reports due to turbo-boost. |
| Demand | The value is even higher than Usage. |

I’d use Core Utilization (%) and Thread Utilization (%) as the primary counters. Yes, 2 counters.
I’d complement with Usage (MHz) for performance.
If Core Utilization is not yet 100% or Thread Utilization is not yet 50% then there is still physical cores available. You can go ahead deploy new VMs.
If Core Utilization = 100% (meaning Thread Utilization is at least 50%) then review Thread Utilization and ensure it’s not passing your threshold. I’d keep it around 80% - 90% per ESXi, meaning the level at cluster level will be lower as we have HA host. Also, check contention.
Regardless of what counters you use, As Mark Achtemichuk said it best: “drive by contention”.

##### Real World Samples

How do these values compare in production environment? The following table shows 297 ESXi hosts. It shows the various possibilities covered earlier.

[Image: ## Image Description

The table displays CPU performance metrics for 297 ESXi hosts (showing 8 rows plus averages), with columns for **CPU Demand, Usage, Core Utilization, Utilization, CPU Used (Seconds), and Configured Cores**. The top hosts show notably elevated metrics, particularly the third row (**wdc-08-r0...**) with **65.77% Demand, 60.63% Usage, 46.04% Core Utilization, and 24.31% CPU Utilization** across 40 cores. The table demonstrates the real-world variance between different CPU metrics on the same hosts, with **wdc-08** hosts (40 cores) generally showing higher demand/usage than **wdc-10** hosts (56 cores), while the fleet-wide averages remain moderate at **33.39% Demand and 13.54% Utilization**.]

Let’s zoom on an ESXi with a very high utilization.
Take a look at the 4 numbers below. Demand is consistently around 130%.
With such a high demand value, it’s no surprise that Usage is 100% flat out.
Do we have a performance problem? What can you deduce from the other 3 numbers?

[Image: ## Image Description

This time-series chart displays four CPU metrics for ESXi host **wdc-08-r03esx23.oc.vmware.com** over approximately 6 hours (2PM–9PM on Dec 31). At the tooltip timestamp of 6:30 PM, the values are: **CPU Demand = 134.76%** (pink, consistently ~130%), **CPU Usage = 100%** (dark blue, perfectly flat line), **CPU Core Utilization = 85.55%** (light blue, ~83-86% range), and **CPU Utilization = 62.66%** (teal, ~58-65% range).

This chart demonstrates the critical distinction between these four metrics: despite Demand exceeding 100% and Usage being fully saturated, Core Utilization (~85%) and raw Utilization (~62%) reveal that the host still has available physical CPU capacity — indicating that hyper-threading and scheduling headroom exist, suggesting the performance impact may be less severe than Demand/Usage alone would imply.]

Core Utilization at 85% is not very high. The box still has 15% of the cores not running. The box has 40 cores 80 threads. Unless there is limit, there are still 6 cores available.
Utilization at 62% is moderate. This means ~38% x 80 threads, or 30 threads are available.
Based on the raw utilization above, I expect the CPU ready to be low.
Let’s check. What’s your conclusion from below?

[Image: The image shows two time-series charts for ESXi host **wdc-08-r03esx23.oc.vmware.com** over a ~7-hour window (1:00 PM–8:30 PM). The top chart displays **CPU Ready in seconds**, ranging from ~76.7 to a peak of **128.53 seconds** around 6:30 PM, with a minimum near **76.7** around 4:30 PM. The bottom chart shows **CPU vCPUs Allocated on all Powered On Consumers**, ranging from a minimum of **214** at 1:00 PM to a peak of ~**250** around 6:30 PM, stabilizing near **225** by end of period. Together, these charts contextualize the CPU Ready values — the peak of 128.53 seconds divided across ~250 vCPUs yields only ~514ms per vCPU (~2.5% ready), demonstrating that despite the high absolute ready value, per-vCPU contention remains low.]

The value peaks at 128 seconds.
But that’s for the entire box. There are 250 vCPU at that time.
Dividing the value, it’s only 514 ms per vCPU. This translates into 2.5%, a relatively low number.
Let’s validate this further by going into each VM.
I took the average of the entire 7 hour period, and got around 2% for Ready and less than 0.1% for Co-Stop. This is pretty good considering these VMs are large. They are 15.29 vCPU on average. Some of them also have limit, which could contribute to the CPU read.

[Image: ## Image Description

This is a VMware vSphere VM CPU performance table displaying **Ready %**, **Co-stop %**, **Limit (GHz)**, and **vCPU count** for 8 virtual machines, along with Highest, Average, and Summary rows. Ready values range from **1.69% to 4.79%**, with Co-stop values remaining very low (**0.0003% to 0.26%**), and the average Ready is **1.98%** with average Co-stop at **0.06%**. The table validates the preceding analysis that despite large VM sizes (avg 15.29 vCPU, 214 total vCPUs in summary), CPU contention metrics are within acceptable thresholds, with some VMs showing CPU limits (notably **esx-hcx-setup-1-1S1V at 72 GHz/36 vCPU**) that may contribute to elevated Ready percentages.]

Now let’s pick the opposite example.
The following chart shows an ESXi with low utilization. What do you notice?

[Image: ## Image Description

The chart displays four CPU metrics for **wdc-10-r13esx01.oc.vmware.com** over a ~6-hour period (3:00 PM–9:00 PM): **CPU Demand (50.49%)**, **CPU Core Utilization (48.13%)**, **CPU Usage (31.72%)**, and **CPU Utilization (28.56%)**, captured at the tooltip timestamp of **Sunday, Dec 31, 07:03:35 PM**. A notable **sharp drop** occurs around 7:00 PM across all four metrics, after which values stabilize at lower levels (~42-44% for the upper pair, ~25-27% for the lower pair). This demonstrates the key finding described in the surrounding text: **Usage is lower than Core Utilization**, indicating the ESXi host is below 50% utilized and the CPU is being **clocked down** by the kernel to conserve power.]

This time around, Usage is lower than Core Utilization.
This ESXi is not even 50% utilized, as the core utilization shows 48%. The kernel decides that it could complete the job with less power, and clocks down the core.

#### Reservation

There is only 1 metric provided, which is Reserved Capacity (MHz). Compare this with memory, which provides 3 counters. Why is that so?
Review the System Architecture section. In short, it is not applicable to CPU as due to its highly transient nature. When the VM is not running, the reserved capacity can be used by other VM. This differs to memory, which is “sticky” as it’s a form of storage.
The metric does not include hypervisor reservation.

[Image: The image shows a VMware vSphere Advanced Performance chart displaying **Reserved Capacity (MHz)** for host **w1-hs2-f0309.eng.vmware.com** over a ~1-hour real-time period on 02/28/2024. The metric flatlines at **0 MHz** throughout the entire period, with all statistical values (Latest, Maximum, Minimum, Average) showing **0**, and a tooltip at 9:49:20 PM confirming "Total CPU capacity reserved by virtual machines: 0." This demonstrates the text's explanation that CPU reservation is highly transient — unlike memory, reserved CPU capacity returns to the pool when VMs are not actively running, resulting in consistently zero reserved capacity.]


#### Peak Core CPU Usage

An ESXi with 72 CPU cores will have 144 threads. You will not be able to see when a single core peak at ESXi Host level as it’s the average of 144 metrics. If you are concerned that any of them is running hot, you need to track the peak among them.
Imbalance among the cores happen because when a VM runs, it runs on as few core as possible, not spread out to all ESXi cores. It’s more efficient to schedule that way, as will requires less context switches.
The following shows an ESXi where 3 of the threads hit >90%

[Image: The image shows a **Performance Chart Legend** table displaying CPU Utilization metrics for 6 ESXi objects (IDs 31, 37, 38, 43, 46, 50), all measured as Average rollup in percentage. Three objects show maximum utilization values exceeding 90% (object 38: 99.96%, object 43: 97.11%, object 50: 91.03%), while their average values remain relatively low (9.57%–22.47%), demonstrating the core imbalance described in the text. This illustrates how individual CPU threads can spike to near 100% utilization while the host-level average remains low (~20%), which would be masked when viewing only aggregate ESXi host metrics.]

The average, however, is low. The total usage can hit 5600% as there are 56 threads, hence the total is only hovering 1100%, which translates into 20%.

[Image: ## Image Description

This is a stacked area chart displaying **CPU thread utilization (%)** across all 56 threads of an ESXi host, spanning approximately **12:40 PM to 1:37 PM**. The Y-axis reaches up to **1000%+**, with the total aggregate hovering around **1100%** — representing only ~20% average utilization across all 56 threads (max possible: 5600%). The chart visually demonstrates the **imbalance between cores**: while the aggregate average appears low, individual threads spike sharply, illustrating that a small subset of cores carry disproportionate load rather than workload being evenly distributed across all available threads.]

Peak CPU Core Usage (%) tracks the highest CPU Usage among the CPU cores. A constantly high number indicates that one or more of the physical cores has high utilization. So long the highest among any cores at any given time is low, it does not matter which one at a specific point in time. They can take turn to be hot, it does not change the conclusion of troubleshooting. Max() is used instead of 95thpercentile as both result in the same remediation action, and Max() can give better early warning.
The imbalance value among the cores is not needed because it is expected when utilization is not high.

#### Metrics to Avoid

Do not use the following metrics. Use the recommended metric instead.

##### CPU Utilization for Resources

Under the System metric group, you will see 17 metrics with names starting with “CPU Utilization for Resources”.

[Image: The image shows the **Chart Options dialog in vSphere Client**, with the **System** metric group selected, displaying available counters including "File descriptors used," "Resource CPU active (1 min average)," "Resource CPU active (5 min average)," "Resource CPU allocation maximum (in MHz)," and "Resource CPU allocation minimum (in MHz)" — all with **Latest** rollup type. This screenshot contextually illustrates the location of the "CPU Utilization for Resources" metrics (prefixed as `rescpu.*`) within the System metric group that the surrounding text advises **avoiding**. The image serves as a visual reference for identifying these metrics in the vSphere Client UI before the text provides the full table of 17 metrics to avoid.]

Here is the full list.

| Name in VCF Operations | Name in vSphere Client |
| --- | --- |
| CPU Utilization for Resources\|CPU Active (1 min. average) | rescpu.actav1.latest |
| CPU Utilization for Resources\|CPU Active (5 min. average) | rescpu.actav5.latest |
| CPU Utilization for Resources\|CPU Active (15 min. average) | rescpu.actav15.latest |
| CPU Utilization for Resources\|CPU Active (1 min. peak) | rescpu.actpk1.latest |
| CPU Utilization for Resources\|CPU Active (5 min. peak) | rescpu.actpk5.latest |
| CPU Utilization for Resources\|CPU Active (15 min. peak) | rescpu.actpk15.latest |
| CPU Utilization for Resources\|CPU Running (1 min. average) | rescpu.runav1.latest |
| CPU Utilization for Resources\|CPU Running (5 min. average) | rescpu.runav5.latest |
| CPU Utilization for Resources\|CPU Running (15 min. average) | rescpu.runav15.latest |
| CPU Utilization for Resources\|CPU Running (1 min. peak) | rescpu.runpk1.latest |
| CPU Utilization for Resources\|CPU Running (5 min. peak) | rescpu.runpk5.latest |
| CPU Utilization for Resources\|CPU Running (15 min. peak) | rescpu.runpk15.latest |
| CPU Utilization for Resources\|CPU Throttled (1 min. average) | rescpu.maxLimited1.latest |
| CPU Utilization for Resources\|CPU Throttled (5 min. average) | rescpu.maxLimited5.latest |
| CPU Utilization for Resources\|CPU Throttled (15 min. average) | rescpu.maxLimited15.latest |
| CPU Utilization for Resources\|Group CPU Sample Count | rescpu.sampleCount.latest |
| CPU Utilization for Resources\|Group CPU Sample Period | rescpu.samplePeriod.latest |

Do not use them. They are legacy metrics.
Instead, use the following:
- For CPU Active, use CPU Demand as they are the same. The 1-minute average results in the same value as the 20-second metric and the 5-minute metric, as VCF Operations averages all of them into a 5-minute value (or whatever default interval you set). So there is no need for a separate 1-minute. The 15-minute does not have a use case as you already have the 5-minute and can always roll up.
- For CPU Running, use CPU Usage.
- For CPU Throttled, use Effective Limit.

### Wait Metric

You can ignore it as it’s the sum of the VM Wait, which mixes idle time.
The following ESXi host has 2 VM. You can see the Wait metric is the sum of the 2 VM wait metrics.

[Image: ## Image Description

The image shows an **Advanced Performance chart** from VMware vROps displaying **CPU Wait metrics** (in milliseconds, Summation rollup) for an ESXi host and two NSX VMs over a ~1-hour real-time period on 29/11/2025 (11:50–12:49).

The legend table reveals three series: **vcfops-arm-m01-esx04** (ESXi host Wait, average **75,947 ms**, max **118,469 ms**) and two VMs — **vcfops-arm-w01-nsx01a** (average **9,562 ms**) and **vcfops-arm-m01-nsx01a** (average **66,385 ms**) — with the green annotations highlighting that **75,947 ≈ 9,562 + 66,385**, i.e., the ESXi host's Wait metric is the **mathematical sum of its two VMs' Wait values**.

This directly illustrates the book's point that the **ESXi Wait metric should be ignored** because it merely aggregates VM-level Wait values (which include idle time), making it misleading as a standalone host contention indicator.]


### Contention Metrics

The nature of average is also one reason why ESXi “consumption” does not correlate to ESXi “contention”. The 4 highlighted area are examples where the metrics don’t correlate, even go the opposite way in some of them. Can you guess why?

[Image: ## Image Description

The image shows two time-series charts for VMware ESXi/vSAN infrastructure spanning **February 12–19**, displaying:

1. **Top chart**: `sc2-prod11-esxi-04` host metrics including **CPU Demand (%)**, **CPU Usage (%)**, and **CPU Utilization (%)**, fluctuating roughly between **40–80%**
2. **Bottom chart**: `sc2-vsan-prod1-02` VM metrics showing **CPU Co-stop (ms)** and **CPU Ready (ms)**, with CPU Ready spiking significantly to **~15K–20K ms** after February 17

Four **red dashed boxes** highlight specific time periods where ESXi consumption metrics (top) and contention metrics (bottom) **fail to correlate or move inversely** — for example, around **Feb 16**, host CPU metrics drop while contention remains visible, and after **Feb 17**, CPU Ready spikes dramatically while host utilization metrics don't show a proportional increase. This directly illustrates the book's point that ESXi consumption and contention metrics don't reliably correlate due to hyperthreading, power management, and the physical vs. virtual CPU measurement distinction.]

The above picture is a little too small. The following ESXi has total capacity of 111 GHz. So Demand hit 315%! Sum of VM CPU Usage also unbelievably high at 143%. Sure, Ready + CoStop were high at that moment, but how do you explain these 2 exceed Total Capacity?

[Image: ## Image Description

The image displays three time-series charts for **wdc-10-r13esx05.oc.vmware.com** spanning January 2–10, showing: **CPU|VM CPU Usage** (peak 159.03 GHz, min 9.51 GHz), **CPU|Demand** (peak 350.34 GHz, min 19.36 GHz), and **CPU|Contention %** (peak 60.65%, min 0.077%). 

The charts illustrate the disconnect between consumption and contention metrics — notably around **January 9**, where CPU Demand spikes dramatically (~350 GHz, exceeding the host's 111 GHz total capacity at ~315%) while the contention chart doesn't show a proportionally correlated spike, and conversely, the contention chart shows significant spikes (e.g., Jan 4 ~60%) where consumption metrics appear relatively flat.

This demonstrates the core argument in the surrounding text: **VM CPU Usage and ESXi Demand can paradoxically exceed physical capacity** due to hyperthreading, power management, and vCPU/pCPU measurement differences, while contention metrics operate independently on a different measurement basis.]

These are the reasons why they don’t match:
- One looks at physical CPU, the other the virtual CPU. One looks at ESXi, while the other looks at VM.
- Hyperthreading and Power Management.
- Imbalance utilization. There are many VMs in this host. Their experience will not be identical.
- Limit may impact the VM, either directly or via resource pool.
- CPU pinning, although this rarely happens.
So what metrics should you use?
Here are the latency metrics provided by vSphere Client.

[Image: The image displays a table of **VMware vSphere CPU latency metrics** available in vSphere Client, listing 7 counters: **Co-stop, Ready, Latency, Readiness, Wait, Swap wait, and Idle**. Each counter includes its rollup method (Summation or Average), unit (ms or %), and a technical description of what it measures — primarily focusing on CPU scheduling delays, contention, and wait states at the VM level. In context, this table represents the **lagging indicators** the author references, explaining why these metrics (averaged across running VMs) are insufficient for proactive performance management compared to the leading indicators discussed in the vSphere Cluster chapter.]

For Co-stop and Ready, the counter does not include contention faced by non VM worlds.
Your operations can’t wait until problem become serious. All the built-in metrics are averaged of all the running VMs. So by the time they are high, it’s time to prepare your resume, not start troubleshooting 😉.
I’d provide a set of leading indicators to replace these lagging indicators. As performance management is best done holistically, I’d cover it as a whole. Find them under vSphere Cluster chapter as an ESXi is typically part of a cluster.
Chapter 3