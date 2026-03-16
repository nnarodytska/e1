# Provider


## Overview

A cluster is operationally a collection of ESXi hosts. As a result, the basic counters of CPU, memory, disk and network are basically the sum of the member host.

### vSphere Cluster

What makes a cluster more complex than the sum of its hosts is the various cluster-level features and configuration. I see vSphere Cluster as the smallest logical building block. From operations management, it’s basically a single computer. It’s a huge and complex machine, much more than just a group of ESXi hosts sharing a common network and storage.
Let’s start by looking its 2 most basic features:

| Features | Impact | Impacts |
| --- | --- | --- |
| HA | Capacity | The various options of HA complicate usable capacity calculation. |
| HA | Availability | HA results in 2 metrics: actual availability and operational availability. HA event requires VM availability to be verified as application dependency could be affected. The order of booting needs to be kept up to date. HA event needs to be reported and investigated. This typically requires log analysis to find the root cause. |
| HA | Configuration | ESXi hosts in the cluster should have identical hardware & software configuration.  Customers typically have multiple clusters, and need them to be consistently configured. |
| HA | Inventory | Actual needs to match plan. Not only the amount, but also the movement and their status. |
| DRS | Performance | Degradation of vMotion stunned time could give a clue to overall ESXi performance. vMotion may impact latency-sensitive application. Rate of vMotion should be measured against expectation. |
| DRS | Configuration | Various DRS settings such as automation level should match plan and standard. VM-level exception can get buried in large environment. Customers typically have multiple clusters, and need them to be consistently configured. |

You can see that the above complicate operations, especially in a very large environment with hundreds of clusters. If you add these features on top, you further increase complexity of your operations.

| Features | Impact | Impacts |
| --- | --- | --- |
| Affinity | Configuration | The settings of affinity and anti-affinity should match plan. In large environment with hundreds of clusters this can get buried and hence overlooked. |
| Resource Pool | Capacity | Shares, Limit, Reservation done at resource pool level need to be compatible with those at its children VM.  Resource Pool should not be peer of VM. |
| Resource Pool | Performance | Shares, Limit, Reservation done at resource pool level need to be compatible with those at its children VM.  Resource Pool should not be peer of VM. |
| Resource Pool | Configuration | Complication from cascading resource pools. Need to ensure VMs are not siblings of resource pool |
| DPM | Capacity | DPM impacts capacity as it changes total capacity. |
|  | Performance | DPM is only considering the ESXi utilization metrics. It does not check the VM contention metric. |
|  | Configuration | DPM settings need to match plan. |

The above cover the standard vSphere cluster. There are 2 other variants, which take the operational complexity higher.

| Features | Impact | Impacts |
| --- | --- | --- |
| Stretched Cluster | Configuration | The configuration of each site needs to be checked so VMs always accessed local storage |
| Stretched Cluster | Capacity | The utilization of the 2 physical sites may be intentionally unbalanced, because one acts as primary site while the other as DR site. |
| Stretched Cluster | Performance | Horse-shoe traffic between VMs on the same site. Traffic ping pong between VMs on different sites. |
| Stretched Cluster | Availability | The whole purpose of a stretched cluster is they protect one another. This shall be tested at least once a year. |
| vSAN Cluster |  | vSAN impacts all aspects of operations management. It impacts Day 0, Day 1, and Day 2. |

In addition, there are complication simply because there are multiple members in the cluster. For example, is cluster utilization simply the average of all its hosts? What if there is imbalanced? It will get buried if the cluster has many hosts.
While a cluster focuses on compute, it is where VM runs and consumes network and storage. This means network and storage counters must be considered as appropriate. If you’re using vSAN, then it’s mandatory.

#### Base Metrics

vSphere Client only displays basic set of metrics. They are grouped into 4, as shown in the following screenshot:

[Image: The image shows the CPU metrics selection interface in vSphere Client, displaying three available counters: **Total** (MHz, totalmhz), **Usage** (%, usage), and **Usage in MHz** (usagemhz) — all using Average rollup and Rate stat type. Only the **Usage** counter (percentage-based) is selected/checked. This screenshot illustrates the basic/limited set of CPU metrics available in the vSphere Client interface, which the surrounding text refers to as the "base metrics" grouped into four categories (CPU, Cluster Services, Memory, and Virtual Machine Operations).]

For each of the group, there is basic set of metrics. Here it is for memory:

[Image: The image shows the **Memory metrics group** selected in vSphere Client's chart configuration interface, displaying 5 available counters: **Ballooned memory** (vmmemctl), **Consumed** (consumed), **Host consumed %** (usage), **Overhead consumed** (overhead), and **Total** (totalmb). All counters use **Average rollup** and **Absolute stat type**, with units in KB or MB except Host consumed % which uses percentage. This screenshot illustrates the basic/limited set of memory metrics available natively in vSphere Client for cluster-level monitoring, as referenced in the surrounding text discussing base metrics.]

The group Cluster Services only provides 3 metrics:

[Image: The image shows a counter selection table for vSphere Cluster Services metrics, displaying three counters: **Current Failover Level** (Latest rollup, numeric, Absolute — tracking HA fault tolerance capacity), **Effective CPU Resources** (Average, MHz, Rate — aggregate CPU across cluster hosts), and **Effective Memory Resources** (Average, MB, Absolute — total available memory across cluster hosts). This screenshot illustrates the limited set of only 3 metrics available under the Cluster Services group in vSphere Client, as referenced in the surrounding text. The table confirms these are the foundational cluster-level health and capacity metrics for monitoring HA and resource availability.]


#### VM Operations

vSphere Cluster, being the main object where VM runs, has a set of event metrics. They count the number of times an event, such as a VM gets deleted, happens. This provides insight into the dynamics of the environment.

[Image: ## Image Description

This screenshot shows the **VMware vSphere performance chart configuration interface** for the **Virtual Machine Operations** metric group within a vSphere Cluster object. It displays 10 available counters including Storage vMotion count, VM clone count, VM create count, VM delete count, VM guest reboot/shutdown counts, and VM host/datastore change counts — all using **Latest rollup, num (number) units, and Absolute stat type**. This illustrates the event-based operational metrics available for tracking VM lifecycle activities (migrations, clones, deletions, reboots) at the cluster level, as referenced in the surrounding text about VM Operations metrics.]

Take note that the metric is accumulative. So it starts since the day the cluster was created. VCF Operations converts into rate, and also make them available at higher level objects (Data Center, vCenter and vSphere World).

| Category | Metric Name | Description |
| --- | --- | --- |
| Change of State | VM guest reboot count | Only a reboot. The underlying VM is not powered off. |
| Change of State | VM guest shutdown count | I think this triggers VM Power Off too. |
| Change of State | VM standby guest count | My guess this also power off the VM |
| Change of State | VM power off count | I think this is direct, abrupt power off. It does not include proper shut down from Guest OS. |
| Change of State | VM power on count |  |
| Change of State | VM reset count | Power cycle, different to Guest OS restart as the VM is momentarily powered off. |
| Change of State | VM suspend count | Deeper than Guest OS Standby. Is this like hibernate in Windows? |
| Change of Inventory | VM create count | All creation, be it from template, direct, or cloning. So this is the total amount. |
| Change of Inventory | VM clone count | Creation via cloning only. |
| Change of Inventory | VM template deploy count | Counted separately to separate those VMs not deployed from template. |
| Change of Inventory | VM reconfigure count | Log Insight tracks the actual changes. |
| Change of Inventory | VM register count | Add into vSphere inventory |
| Change of Inventory | VM unregister count | Take note the VM file can still exist in datastore and LUN |
| Change of Inventory | VM delete count | All deletion, be it API or UI. |
| Change of Location | vMotion count | Change of ESXi host only |
| Change of Location | Storage Motion count | Change of datastore only. |
| Change of Location | VM host and datastore change count | Both change in one event. Powered-on VMs only |
| Change of Location | VM datastore change count | Only for powered-off VMs |
| Change of Location | VM host and datastore change count | Only for powered-off VMs |
| Change of Location | VM host change count | Only for powered-off VMs |

You certainly have some expectation on the dynamics of your environment. Does the reality match your expectation?
In production environment, these numbers should be low. Some numbers such as shutdown should also match the change request and happens during the green zone. Some exceptions apply, such as your VDI design includes scheduled reboot on the weekend.

## Performance

Operationally, you manage at cluster level, not at Resource Pool, ESXi host, or data center level. It’s the sweet spot for starting your monitoring and troubleshooting. As usual, we start with the contention metric, followed by the utilization metric.
By definition, the metrics are average numbers. So be careful as there can be VM that has issue but obscured in the cluster wide average. Even the so-called total or summation is mathematically an average. For example, the Total CPU Wait counter is the sum of all ESXi CPU Wait metrics, which in turn is the sum of all the VMs. At the end you get a large number, which you need to normalize and convert into average. Since you divide it against the cluster total, you get average.

### Utilization vs Contention

There is a common misconception that you cannot have performance issue when cluster has low utilization. We introduced that problem as a story earlier here.
Is there corelation between cluster utilization and cluster contention?
I’ll show 2 opposite examples.

#### Example showing Correlation

If every VM is given the same treatment by the cluster, then yes.
Here is a cluster experiencing regular high utilization in the last 7 days. You can clearly see the peak. The cluster has 14 ESXi Hosts.

[Image: ## Image Description

The chart displays **CPU Demand (%)** for a VMware vSphere cluster over a 7-day period (May 11–18), showing a clear **recurring daily spike pattern** with peaks reaching the high value of **H: 125.72%** and a low of **L: 38.06%**. The baseline utilization sits around **~50%**, with sharp, regular spikes climbing to approximately **110–125%** each day, indicating consistent scheduled workload bursts (likely daily batch jobs or backups). This demonstrates the **correlation example** referenced in the text — the cluster experiences predictable high utilization peaks across all 7 days, setting up the subsequent discussion of how these utilization spikes directly correspond to VM-level CPU contention metrics.]

A logical question here would be what’s the impact on VM performance? Are they getting the CPU they asked? The cluster has 550 running VM.
This is where the contention metrics come in. One tracks the depth of the problem, the other the breadth of the problem.
The counter Percentage of VMs facing CPU Ready > 1% shows a nearly identical pattern. We can see that a big percentage of the VM population is affected.

[Image: ## Image Description

The chart displays **"CPU | Percentage of VMs facing CPU Ready (%)"** for a VMware cluster over approximately 7 days (May 11–17), showing values ranging from a **low of 2.26%** to a **high of 59.68%**. The metric exhibits a **consistent daily spike pattern**, with sharp peaks reaching ~50-60% occurring roughly once per day (likely during business hours or scheduled workloads), followed by rapid drops back to near-baseline (~2-5%). This demonstrates the **breadth of CPU contention** — at peak, nearly 60% of the 550 running VMs in the 14-host cluster simultaneously experienced CPU Ready values exceeding 1%, confirming that the utilization spikes visible in the preceding charts translate directly into widespread VM-level performance degradation.]

The second counter tracks the depth, giving the absolute worst CPU Ready value experienced by any VM in the cluster.

[Image: ## Image Description

The chart displays **CPU | Worst VM CPU Ready (%)** for a VMware cluster over approximately one week (May 11–17), showing the single highest CPU Ready value experienced by any VM in the cluster at any given time. The metric peaks **daily around midday**, reaching a maximum of **H: 50.7%** (marked on May 16) with most daily spikes ranging between **30–45%**, while baseline values remain low at **L: 1.54%**. This demonstrates the **depth of CPU contention** — even if only one VM is severely affected, this counter captures it, complementing the breadth metric (% of VMs facing CPU Ready >1%) to provide a complete picture of cluster-wide CPU contention during what appears to be a recurring daily workload pattern.]


#### Example showing no Correlation

Performance is unmet demand. VM 007 can face very high contention when all other VMs on the same cluster face no contention.
It is possible for VMs in the cluster to suffer from poor performance, while the cluster utilization is low. One main reason is cluster utilization looks at the provider layer (ESXi), while performance looks at individual consumer (VM).
The following cluster has 32 ESXi supporting 2357 VM. The average demand across the cluster is <40%. Since it has 32 ESXi and 2357 VM, we can retire 8 ESXi or add 1K VM.

[Image: ## Image Description

The chart displays **CPU Demand (%)** for a VM named **us04vcore2vc1c1** over approximately 48 hours (March 12–13), with values ranging between **~25–40%**. The metric shows consistent oscillating demand with a notable **peak near 40% around 12:00–4:00 PM on March 12**, followed by a dip to ~25% on March 13 morning before recovering to ~32–35%. In the context of the surrounding text, this chart illustrates how an **individual VM can show meaningful CPU demand** even when cluster-level utilization appears low, supporting the argument that cluster-level metrics can mask individual VM performance issues.]

And yet the VMs in the clusters are facing contention. Both VM CPU Ready and CPU Co-stop are high.

[Image: ## Image Description

The chart displays two VM-level CPU contention metrics for **us04vcore2vc1c1** over March 12-13: **Max VM CPU Ready (%)** (pink) and **Max VM CPU Co-Stop (%)** (teal), both fluctuating between approximately **0-20%**. Both metrics show consistently elevated values throughout the period, with notable spikes reaching **~20%**, and CPU Co-Stop appearing relatively stable around **15%** during midday on March 12. This demonstrates the core thesis of the surrounding text: despite the cluster showing low average utilization (<40%), individual VMs are experiencing significant CPU contention (Ready and Co-Stop well above acceptable thresholds), illustrating that cluster-level utilization metrics can mask VM-level performance problems.]

Let me take another example, where you can see the corelation between cluster utilization and VM contention in the cluster. My apology that the picture is not sharp. You can see the cluster has 774 running VM at the start. One month later it has dropped to 629, a drop of 145 VM or 19%. The second line chart reveals the number of running vCPU dropped from 3019 to 1980, a whopping 1039 vCPU or 34%. That indicates the big VMs were moved out.
This cluster was running mission critical VMs. What’s going on?! What caused the mass evacuation.
Notice the mass evacuation happened multiple times, so it’s not accidental.
Looking at the last chart. It has 2 line. Maroon showing utilization, blue showing contention. Can you figure out what happened?

[Image: The image shows three time-series charts spanning October 9 to November 7, tracking a VMware cluster's health: (1) Running VMs dropping from a high of 774 to a low of 629, (2) vCPUs on powered-on VMs declining from 3,019 to 1,980, and (3) a dual-metric chart showing CPU Demand (pink/maroon, ~50% average) alongside Max VM CPU Contention (blue), which spiked repeatedly above 75%. The data illustrates that despite relatively stable ~50% cluster utilization, recurring CPU contention spikes — reaching into the 75-100% range — triggered multiple forced VM evacuations, explaining the stepwise VM and vCPU count reductions visible in the upper two charts. The tooltip highlights a specific data point on November 1 at 03:00 AM showing CPU Contention at 1.801% and CPU Demand at 38.478%, capturing a relatively calm moment between contention events.]

The cluster utilization was hovering around 50%. In that entire month, it barely moved. This cluster was probably 16 nodes, so 50% utilization means you can easily take out a few ESXi hosts actually.
The Max VM CPU Contention told a different story. Notice it spiked well above 75%. That impacted at least 1 VM. There were multiple spikes, leading to multiple complaints, and eventually infrastructure was forced to evacuate the cluster to fix the performance problem. Notice the counter dropped gradually in November, despite utilization remains fairly stable.

#### Example for Memory

We covered 2 examples for CPU. What about memory, since it’s a form storage. It’s just a disk space basically, so can VM experience contention when Cluster consume metric is not high?
I’d zoom into ESXi, so it’s easier to see. What do you deduce from this ESXi? This chart shows 1 month worth of data.

[Image: ## Image Description

This is a time-series chart from VMware vSphere/VCF Operations displaying **ESXi host memory metrics** over approximately one month (Aug 14 – Sep 13). At the tooltip point of **Thursday, Aug 26, 11:00 PM**, three metrics are shown: **Memory|Usable Memory = 759.39 GB** (blue, flat line near 700), **Memory|Allocated on all Powered On Consumers = 444 GB** (pink, ~450 GB), and **Memory|Consumed = 413.371 GB** (green, ~410-420 GB). The chart demonstrates that the ESXi host has substantial free memory headroom (~315 GB unallocated), with allocated and consumed memory remaining relatively stable throughout the period, supporting the conclusion that there is **no memory pressure** at the host level.]

It has 759 GB of usable memory. All the powered on VM has 444 GB configured, out of which only 413 GB is mapped to physical DIMM. So there is plenty of memory left.
To confirm that it has plenty of memory, let’s plot Balloon. What do you expect?

[Image: ## Image Description

The chart displays **Memory|Balloon (KB)** metric for an ESXi host over approximately one month (August 14 – September 13), showing a **flat line at exactly 0 KB** throughout the entire period, with High (H) and Low (L) values both recorded as **0**.

This confirms the preceding text's assertion that the ESXi host experienced **zero memory pressure** — ballooning never activated, which is consistent with the host having 759 GB usable memory with only ~413 GB mapped by powered-on VMs.

The flat zero baseline serves as the **provider-level baseline** before the analysis shifts to consumer-level contention, setting up the paradox explained in the following text: despite no host-level memory pressure, individual VMs can still experience contention (e.g., via memory compression/swap).]

There is no ballooning. ESXi was under no memory pressure whatsoever.
So that’s the situation at provider level. How about consumer level?
VCF Operations has a metric that tracks the highest memory contention experienced by any VM in the host. This is a good leading indicator as all it takes is 1 VM, it matters not which VM.
As we can see here, there is a problem.

[Image: ## Chart Description

The chart displays **"Memory | Worst VM Memory Contention (%)"** over a period from August 14 to September 13, showing values that remain near **0% for most of the timeframe**. A sharp, isolated spike occurs around **September 5**, reaching the maximum recorded value of **H: 12.5%**, with the low recorded as **L: 0**. This metric tracks the highest memory contention experienced by any single VM on the host, and the prominent spike confirms the text's assertion that "there is a problem" — indicating at least one VM experienced significant memory contention (~12.5%) at that point, likely due to compressed or swapped pages being accessed.]

Can you explain why?
A VM experiences contention when the page is not in the DIMM. It was compressed or swapped out. Checking the compressed metric, it reveals that pages had to be brought it. Notice the swap metric lagged a bit, which makes sense.

[Image: ## Image Description

The image displays two time-series charts for an ESXi host (**esxi-04**) spanning **Aug 14 – Sep 13**. The **top chart** shows **Memory|Compressed (MB)** with a high of **138.754 MB** and a low of **133.855 MB**, featuring a notable **drop ~Sep 5** (green circle) where compressed memory decreases, and an unexplained earlier anomaly around **Aug 24** (red circle). The **bottom chart** shows **Memory|Worst VM Memory Contention (%)** with a high of **12.5%** and low of **0%**, showing a **sharp contention spike ~Sep 5** (green circle) that correlates directly with the compression drop above, demonstrating that when compressed pages were decompressed/recalled into DIMM, the VM experienced measurable memory contention.]

I am not able to explain the earlier dropped, the one in red circle. If you can drop me a note.
Let’s complete by plotting Swapped. I’m plotting all the way to the beginning of tracking.
It’s all 0. What happened?
That means all the pages could be compressed, so ESXi decided to compress instead of putting them into swapped file.
Now that we know it’s due to compression, we know the contention on 5 September was caused by compression. When was that page compressed, no one knows. Plotting back, the compression started around 2 August.

[Image: ## Chart Description

This chart displays **Memory|Compressed (MB)** for a VM over the period of **August 2–12**, with a high value of **342.63 MB** and a low of **0 MB**. The data shows a sharp spike beginning around **August 2–3**, peaking near 342 MB, followed by a sudden drop around **August 4**, then stabilizing at a consistently low (near-zero) level through August 12. This chart supports the surrounding text's explanation that memory compression began around August 2 and reached only ~342 MB — a negligible fraction of total consumed memory — yet was sufficient to cause performance contention for the affected VM.]

The compression was only 342 MB. Not even 0.1% of consumed memory. But if you are unlucky, it was the active VM that got hit, as in the case here.
The past is harder to debug, as we lack the ability to travel back in time and see the environment as it was. My guess here is the VM had limit, be it indirectly via resource pool or directly.

### Cluster Performance (%)

We’ve covered in the VM chapter how we quantify the KPI of a single VM. How would you represent all the VMs in the cluster? Do you simply average the VM KPI (%)?
The answer is no. A cluster has a different purpose to a VM, so we need to see it from cluster point of view. For examples:
- Contention inside a VM (this means Windows or Linux) is not that relevant to the cluster performance.
- ESXi physical network is relevant to the cluster performance, but not to the VM performance.
A cluster is more of a group of ESXi hosts serving a VM.

[Image: ## VMware vSphere Cluster KPI Thresholds Table

This table defines color-coded performance thresholds (Green/Yellow/Orange/Red) for **10 cluster-level metrics** split into two categories: **"How Deep?"** (worst-case VM contention: vCPU Ready 0-4%/4-8%/8-16%/16-32%, Co-Stop, Memory Latency, ESXi network packet loss) and **"How Broad?"** (average cluster-wide metrics: vCPU Ready, Co-Stop, Memory Latency, vMotion percentage, swapped+zipped memory, and Balloon memory). In context, the table operationalizes the cluster-level KPI framework described in the surrounding text, distinguishing between **depth** (worst single-VM contention, e.g., Memory Latency red threshold: >4%) and **breadth** (average across all VMs, with notably tighter thresholds, e.g., Average Memory Latency red threshold: >2%). The dual-dimension approach addresses the limitation that simple VM-level averaging would obscure both severe individual outliers and widespread moderate contention across the cluster.]

The metrics are grouped into 2:
- Breadth
- Depth.
We cover why we need both dimensions in VCF Operations Management book.
The metrics are using the 20-second peak so it does not miss short bursts. The limitation of this metric is outlier. A large cluster with thousands of VMs can easily have 1 VM having contention due to limit. One way to minimize the false positive is to set a higher threshold.
For the breadth, we use average. Ideally, we use 75th percentile instead of average. Average tends to be too late. On the other than, 95th percentile suffers from cluster imbalance. I’ve adjusted the threshold downward since I’m using average.
In a cluster with many hosts, there can be imbalance. It is not possible to aggregate at the host level first. This 2-level aggregation can result in suboptimal number. The drilling down to specific host can be facilitated with the host level metric.

#### Metrics

vMotion is included as it does impact the VM performance (although the end users may not notice in most cases) and it’s a leading indicator that the cluster is struggling to serve the load hence it has to shuffle the VMs around.
Take a look at this cluster. It has 488 running VMs on 16 ESXi host. Notice the percentage of VM being vMotion jumped to 5.3%, as 26 VMs were vMotion.

[Image: ## Image Description

The chart displays **"Super Metrics | Cluster vMotion Percentage (%)"** for cluster **wdc-06-vc02c01** over a ~29-hour period. The metric remains at **0% (Low: 0)** for nearly the entire timeframe, with a single sharp spike reaching **5.33% (High: 5.33)** occurring around **04:30–05:00 AM on August 24**. This spike represents the moment when 26 VMs out of 488 were vMotioned simultaneously, illustrating how cluster vMotion activity is typically near-zero but can briefly surge when the cluster needs to rebalance VM workloads under load pressure.]

What do you think will happen to the VM CPU Ready and CPU Co-stop?

[Image: The image shows two time-series charts for cluster **wdc-06-vc02c01** displaying **CPU Co-Stop** (top, H: 0.043, L: 0.000116) and **CPU Ready %** (bottom, H: 0.11, L: 0.0726) over a ~24-hour period spanning Aug 23–24. Both metrics show a prominent spike highlighted in yellow at approximately **04:30–05:00 AM**, corresponding to the vMotion event described in the preceding text. This confirms the assertion that CPU Ready and Co-Stop rose during the vMotion activity, though the increase was minimal (values remain low overall), consistent with only ~5% of VMs being affected.]

They rose. Since only 5% was impacted, the rise will be minimal.
The threshold should reflect reality. For examples:
- While the impact on VMs is the same with Ready, using the same range for CPU Co-stop, CPU Overlap and CPU Other Wait will elevate the KPI score, as practically these 3 have lower score.
- Dropped packet and error packets are very rare. Instead of summing them up, which will result in an average, I took the worst among ESXi host. Since many ESXi sports 25 Gb NIC, I set the threshold to be very low. On the other hand, I did not set green = 0, so the KPI does tolerate some issue.
- Ballooning does not actually impact performance. That’s why it’s given 4x the threshold of zipped + swapped. I may change to 6x, but will have to consider large cluster. A cluster with 20 TB of RAM means 4% ballooned translates into 800 GB.
- Ballooned, swapped, and zipped are given higher threshold as they could have happened in the past. These metrics are “sticky”. They also may not impact performance. But since many clusters sport >4 TB of RAM, I need to balance the absolute size.

#### Metrics Not Used

The following metrics are not included:
- “Percentage of VM population experience CPU Ready > 1%” and “Percentage of VM population experience Memory Contention > 0%” as they measure the same purpose with the average.
- VM utilization. They are irrelevant. Use the metrics at ESXi level instead.
- ESXi Consumed. The higher the consumed, the better the performance. We use balloon, swapped and compressed metrics instead. Since they do not directly impact performance, we put as secondary KPI.
- ESXi CPU Utilization. They do not actually impact performance. If you include them, take the highest among ESXi instead of cluster wide average, as average is too late.
- VM DRS Score. It’s using metrics that are already included in the KPI, so it’s double counting.
- Disk latency. Storage troubleshooting differs to compute troubleshooting. The exception here is Hyperconverged Infrastructure, as the compute and storage are integrated.
- Percentage of VMs facing Disk Latency. It should be part of datastore KPI, not the cluster. The reason is if there is a population problem, you troubleshoot the datastore not the cluster(s) mounting it.
- CPU Other Wait. There is a false positive. I’ve seen it hence decided to exclude.
- CPU Overlap. I find their values to be very low that they might mask out other problems.
Future enhancements:
- There are metrics that are only available in esxtop. They are not available in vCenter REST API, so they are not retrievable. Example is Local:Remote memory ratio for VM.
- 2 level roll up. This means that the cluster metrics take from its hosts instead VMs. In this way, every host is represented. Need to model the difference scenarios before we decide this solution meets the requirement better.

#### Implementation

The above is implemented using super metrics.

[Image: ## Image Description

This image shows a **VMware Aria Operations (vROps) super metric formula** using a `sum([...])` function that aggregates **10 cluster-level performance metrics** into a single composite score. The metrics included are: CPU Ready, CPU Co-Stop, Memory Contention, Worst VM CPU Ready, Worst VM CPU Co-Stop, Worst VM Memory Contention, Worst ESXi Bad Network Packets, vMotions, Memory Stressed, and Memory Ballooned — each aliased with short variable names (e.g., `Ready`, `coStop`, `MemLatc`). This demonstrates the implementation referenced in the surrounding text, where super metrics collect individual ESXi/VM performance indicators at the cluster level to enable consolidated health monitoring.]

All the super metrics are fairly simple. They are simply taking the average or the maximum of either ESXi or VM in the cluster.
Something a little trickier is Ballooned (%). The formula is below.

[Image: The image shows a super metric formula for calculating **Ballooned Memory (%)** in VMware vSphere. The formula divides `mem|vmmemctl_average` (balloon memory) by the sum of `mem|vmmemctl_average` + `mem|consumed_average` - `mem|sysUsage_average`, then multiplies by 100 to express it as a percentage. This demonstrates how ballooned memory is calculated as a proportion of effective total memory consumption, excluding kernel/system usage from the denominator.]

Why did I exclude kernel usage, but include ballooned?
Answer is in the Memory chapter.

### Troubleshooting

At any given moment, a running VM always resides on an ESXi Host. Due to DRS and HA, it’s easier to monitor at cluster level. Since a cluster can have hundreds of VMs, you need consolidated metrics that can represent the experience of all the running VMs in the cluster. VCF Operations 8.2 provides the following metrics:

| Problem | Optimize or Remediate |
| --- | --- |
| Worst VM CPU Ready.  Worst VM RAM Contention | These are the highest value among all the running VMs. It shows you the depth of the problem. Check how many VMs are affected to see pattern. |
| % VMs experienced CPU Ready % VMs experienced RAM Contention | Since it’s impacting many VMs, the problem is likely not at VM setting, but at ESXi or cluster level. Some possibilities: There is 1 or more sibling VM to Resource Pool, causing VMs in the pool to suffer. Imbalance shares. 1 or more VM has relatively large shares. High ESXi utilization. However, Cluster utilization is unlikely to be high, due to HA and Buffer. So check for imbalance among hosts, which is common in large clusters.  Imbalance could be due to  DRS settings VM – Host affinity, or VM – VM affinity Resource Pool Cluster inconsistent configuration (e.g. storage or network not available to all hosts) |
| vSAN CPU Ready | It’s not something you can change, unless via ESXi advanced settings to modify the kernel scheduler behaviour? |
| ESXi Error Packets | Check the vmnic driver and firmware |


### Service Level Metrics

These metrics require the understanding of how SLA, SLI and KPI differ. They are covered in-depth in Part 1 of VMware Operations Transformation book. Their implementation require VCF Operations super metrics and custom dashboard.

#### Cluster SLA

How to roll up the VM SLA into total SLA for the whole environment? Your CIO likely wants to see this number over time.
Calculating SLA per vSphere cluster also makes management easier. You know which cluster to attend to. The problem is SLA is a lagging indicator. It is based on the last 30 days or the last month.
Cluster SLA is derived from the VM SLA. It is simply the percentage of VMs that fail the SLA. How bad each VM fails the SLA, or how comfortable it exceeds the SLA, is irrelevant at this stage. At the cluster level, you care about pass/fail first.
That means the Cluster SLA is not the average of its VM SLA. Doing an average can be too late unless your SLA is 100%.
Once you know how many VM fails, you want to know who the VMs are and troubleshoot if there is a common reason.

#### Cluster SLI

SLA is a 30-day counter. You can’t wait that long before you do something. This is where SLI comes in. It’s an indicator, and not mentioned in the SLA contract.
Let’s take an example of a cluster with 500 VM. Each VM consumes 4 IaaS resource (CPU, Memory, Disk, Network). It must pass all else it’s counted as 1 SLI fails.
The Cluster SLI (%) is simply the percentage of VM that fails the SLI. As a recap, this is the single threshold we use for all classes of service:

[Image: ## Image Description

The table defines **four IaaS resource thresholds** used to determine VM SLI (Service Level Indicator) failures across CPU, RAM, Disk, and Network layers. The specific threshold values are: **CPU Ready ≤ 2.5%**, **RAM Contention ≤ 1%**, **Disk Latency ≤ 10ms**, and **Network TX Dropped Packets = 0%**. In context, these represent the single normalized pass/fail criteria applied uniformly across all VM classes of service when calculating the Cluster SLI percentage.]

It’s a normalized average of the VM SLI, taking into account the actual SLI failures. That means it will give a lower number if the VMs are experiencing worse SLI individually. 1 VM experiencing 4 SLI failure will result in the same value as 4 VM experiencing 1 SLI value each.
The formula is
100 –
(
( Sum([VM]Performance|Number of KPIs Breached) + Sum([Pod]Performance|Number of KPIs Breached ) )
/
( Summary|Number of Running VMs + Summary|Number of Pods )    * 100 / 4
)

## Capacity

Now that you’ve reviewed the raw metrics, let’s apply them into capacity management.
The following diagram shows that capacity uses a smaller subset of the resource than performance.

[Image: ## Image Description

The diagram illustrates the relationship between **Performance Management** and **Capacity Management** within total ESXi resource allocation (scaled 0–100%). The total resource is divided into three layers: **Hypervisor** (bottom overhead), **Usable Capacity** (middle, 0–100% for Capacity Management), and **Buffer** (top reserve), with Performance Management spanning the full 0–100% range. This visually demonstrates that capacity management operates within a **smaller subset** of the total resource than performance management, as the usable capacity excludes both the hypervisor overhead and the buffer zone.]

ESXi capacity is often misunderstood, as there are multiple considerations.
- On the supply side, you have total capacity and usable capacity. Both have nuances.
- On the demand side, you have utilization, reservation, allocation, and unmet demand.
- The kernel impacts both the supply side and demand side. Be careful of double counting!
- Lastly, CPU, memory and network have different natures.
From the first principle, the total capacity and usable capacity should not be a variable as it makes capacity management impractical. Your 100% should always be a constant so you have a stable anchor. This makes cost accounting less debatable too.

| Usable Capacity | Usable Capacity = Total Capacity – Hypervisor – Buffer. |
| --- | --- |
| Usable Capacity | Hypervisor = VMkernel + vSAN + NSX + vSphere Replication |

So what amount should we put for the hypervisor?
It turns out that it’s not an easy answer. So let’s dive in.
BTW, extracting the hypervisor portion as a separate value has a bonus as it can be used use cases involving 2 different ESXi hosts, such as migration from non VCF cluster to a cluster running both vSAN and NSX

### Hypervisor


| Why Hypervisor? | Why not use the word kernel or VMkernel? |
| --- | --- |
| Why Hypervisor? | The hypervisor is more than kernel. There are user-level or application that is runs on top of the kernel. |
| Why Hypervisor? | The word kernel is often mistaken with VMkernel. VMkernel does not include vSAN & NSX as they are not traditionally considered part of kernel. vSAN for example has processes parked under /opt resource group |
| Capacity or Performance? | Why do I put hypervisor under capacity, and not performance? |
| Capacity or Performance? | Because operationally, the metrics impact capacity management. Since the hypervisor gets the highest priority, you do not monitor the metrics from performance viewpoint. If you need to see the ready time for each of the kernel process, see esxtop. |

Kernel does not have allocation as it’s an OS process.
The hypervisor has 3 types of metrics:
- Reservation
- Limit
- Utilization.
Which one do you use?
- Utilization is not feasible as it changes by the seconds. Just like total capacity cannot be volatile, the same goes with usable capacity.
- Limit does not even make sense as certain features of hypervisor impacts all VM, hence should take higher priority.
- Reservation tends to be too low if you run vSAN and NSX, and too high if you only run ESXi. It also fluctuates over time, giving you unstable usable capacity.
The last option is to manually include a static value when calculating the usable capacity. This means we need to know the amount.

#### Metric Type

ESXi scheduler uses share, limit and reservation to manage its worlds. Broadly speaking, there are 2 types of worlds:
- VM
- Non VM
You will see 3 types of metrics in the vCenter UI:

| Type | Analysis |
| --- | --- |
| Utilization | This is the actual, visible, consumption.  It can be lower than reservation, but not higher than allocation. |
| Utilization | Since you’ve already paid for the hardware, you want to drive ESXi utilization as high as possible so long there is no contention. Since the hypervisor has higher priority than VM, we can safely assume we can use VM contention as the proxy for overall contention (assuming manual VM Limit is not set). The ESXi utilization metric considers both the hypervisor and VM. There is no need to separate the hypervisor in this case. The only time we need to separate is when we’re migrating the VMs into another architecture. |
| Reservation | For the hypervisor processes, the maximum amount is taken care of by allocation, while the minimum amount is by reservation. This is a safety mechanism to ensure the hypervisor can still run when all the VMs want 100% resource.  Processes that run at hypervisor level does not get its reserved memory up front. It’s granted on demand. CPU, being an instruction in nature, does not use the reserved amount unless it needs to run. If you plot in vSphere Client UI, you will see the value of utilization can be lower than reservation. |
| Allocation | For VM, allocation is useful as there is overcommit between virtual and physical. For the non VM, it is not useful since there is no overcommit because there is no virtual part. You notice that some hypervisor processes have no limit. If you plot them in vSphere Client UI, you will find their limits are either blank or 0. |

The above 3 values vary over time. Why is it hard to determine the size of the above 3 values up front?
Taking from page 258 of Frank Denneman and Niels Hagoort’s book, with some changes:
- Some services have static values (allocation and reservation) regardless of the host configuration. Ok, this is the easy part.
- Some services have relative values. It scales with the memory configuration of the host. Ok, that means you need to know the percentage for each.
- Some services have relative values that are tied to the number of active VMs. Ok, that means you need to know how many VMs are active.
- Some services consume more when they do more work. Example is storage and networking stack.
- Some services consume more depending on the configuration. For example, vSAN consumes more when you turn on dedupe and compression.
Since an ESXi host has many services, it is impossible to predict the overall values of the above 3 metrics.

#### Grouping

All the processes that run in the hypervisor belong to one these 5 top-level resource groups:

| System | host/system resource pool for low-level hypervisor services and drivers. You will find world such as minfree, kernel, helper, fault tolerant, vmotion, storage vmotion, vmk API mod, idle, and drivers.  Doing multiple vMotion simulaneously will increase the consumption of vmotion resource.  The data plane portion of vSAN is reported here, although there is no separate counter for it. |
| --- | --- |
| VIM | VIM = virtual infrastructure manager.  vmvisor = hypervisor. This include NSX, and vSAN management plane. host/vim resource pool for host management process such as HA (aam), vCenter agent vpxa, hostd, VIM user (the group for DCUI, shell, SSH, Tools), authd, tmp, envoy, GPU Manager, ESX tokend, healthd |
| User | host/user resource pool All the running VMs are children of the User resource pool. This includes the VM overhead as it’s part of the VM. There is no breakdown for this pool. The only metric is host/user. vSphere Client UI does not display the CPU or memory reservation metrics. |
| Opt | Mostly vSAN. You will see it as opt/vsan. An example of process will be vsan/vsanperfsvc for the performance monitoring. Added in vSphere 8.0.1 |
| IO Filter | host/iofilter resource pool The IO Filter processes are grouped here. The generic framework allows 3rd party partner software to intercept and process network and storage IO. More about it at vSphere manual. Just search for “About I/O Filters”. If you are unsure, read this by Ken Werneburg.  Note: vSphere Client UI does not display the CPU or memory reservation metrics. |

In the older version of vCenter, you could see the structure. The dialog box is no longer available in the present vCenter UI. I’ve made the screenshot smaller as the details has changed, so this is just to show the idea.

[Image: The image shows the **System Resource Allocation** panel from an older vCenter UI, displaying a hierarchical tree structure of **ESXi host resource pools**. The tree is organized under a root "host" node, branching into major groups: **system** (containing minfree, retiredmem, kernel, helper, drivers, ft, vmotion, svmotion, vmkapimod) and **vim** (containing vmci, vmvisor sub-groups with processes like aam, dcui, dhclient, hostd with child processes rhttpproxy.20862, hostd.20921, nssquery.20926). This screenshot demonstrates the internal ESXi resource pool hierarchy referenced in the surrounding text, illustrating how system and VIM resource groups are structurally organized — the same groups whose CPU and memory consumption patterns are contrasted in the table that follows.]


##### Relative Comparison

You will notice major differences in the way the resource groups consume resources.

|  | CPU | Memory |
| --- | --- | --- |
| System | Surprisingly low. It can be well below 1 GHz. | Relatively high. It’s ~20 – 30 GB depending on the ESXi |
| VIM | Relatively high. It’s around 4 – 12 GHz depending on the ESXi. | Surprisingly low. It could be even 0 GB. |


[Image: This image displays two tables showing **ESXi host resource group metrics**: the top table shows CPU resource pools (vmgid 0-5) with parameters including `amin`, `amax`, `minLimit`, `units`, and `shares`, while the bottom table shows corresponding memory allocations in MB (`min`, `max`, `minLimit`, `shares`). Key highlights (marked in green/orange) show the **system group has amin=110% CPU** and **14,720 MB memory min**, while the **vim group has amin=342% CPU** but **0 MB memory min** — directly illustrating the contrasting resource consumption patterns described in the surrounding text (VIM consumes relatively high CPU, system consumes relatively high memory). The host root group shows total values of 3200-3300% CPU and 391,428 MB memory across 5 child resource groups.]


##### Metrics

In the vSphere Client UI, you will see the list of resource grouping in the Target Objects section in the performance chart.
I’ve highlighted them in the following screenshot:

[Image: The image shows the VMware vSphere performance chart configuration interface, with **"Resource memory consumed"** (in KB) selected as the counter, measuring memory consumed by the system resource group. The **Target Objects** section (highlighted in green) displays a hierarchical list of ESXi resource groups — including `host`, `host/iofilters`, `host/system`, `host/vim`, and their sub-components — all checked for inclusion in the chart. The timespan is set to **Real-time (Last 1 Hour)** with a **Line Graph** chart type, demonstrating how to select specific resource group objects to monitor kernel-level memory consumption across ESXi subsystems.]

To see the kernel consumption, select only these 3 from the list above:
- host/iofilters
- host/system
- host/vim.
The rest of the items are part of them, so no need to plot them. More importantly, they are fairly small, well below 0.5 GHz. The following screenshot shows their highest 20-second average in the last 1 hour.

[Image: This image shows a performance metrics table from vCenter listing **Resource CPU usage (in MHz)** for various ESXi host system objects/processes, sorted by Maximum value in descending order. The top consumers are **host/system (3,456 MHz)**, **host/vim/vmvisor (3,121 MHz)**, and **host/vim/vmvisor/esximage (1,677 MHz)**, with most other processes consuming well under 500 MHz. The highlighted entries (vsan, hostd, vpxa, healthd, aam, dcui, vmtoolsd) identify specific VMware kernel and management processes, demonstrating that while a few top-level resource groups dominate CPU consumption, the majority of individual vmvisor processes consume minimal CPU (under 100 MHz).]

To see their total, plot their values in vCenter by stacking up their values, as shown below.

[Image: ## Image Description

This stacked area chart displays **Resource CPU usage (Average) in MHz** for three ESXi kernel components — `host/iofilters`, `host/system`, and `host/vim` — over a ~1-hour real-time window on 03/27/2021. The stacked visualization shows combined kernel CPU consumption ranging roughly **250–700 MHz baseline** with periodic spikes reaching up to **~1,900 MHz**, with `host/vim` (green, max 1,481 MHz, avg 471.7 MHz) dominating over `host/system` (black, max 732 MHz, avg 348.9 MHz) and the negligible `host/iofilters` (avg 0.667 MHz). This demonstrates the **total ESXi kernel CPU overhead** by stacking the three primary kernel consumers, illustrating that VMkernel itself consumes a non-trivial but bounded amount of CPU capacity that must be accounted for in capacity planning.]


### CPU

When you buy a CPU, what exactly is the capacity that you actually get?
To recap, this is what vSphere uses for ESXi.

[Image: ## Image Description

This screenshot shows the **Summary tab of an ESXi host (192.168.233.149)** in VMware vCenter, running **VMware ESXi 6.7.0** on a **Dell EMC PowerEdge R620** with dual Intel Xeon E5-2660 processors (32 logical processors). The resource utilization metrics show **CPU at 11.3 GHz used out of 35.18 GHz capacity** (Free: 23.89 GHz), **Memory at 178.9 GB used out of 255.96 GB**, and **Storage at 2.85 TB used out of 3.88 TB**. In the context of the surrounding text, this image illustrates how vSphere calculates **CPU capacity as base frequency × number of cores** (2.20 GHz × 16 cores = 35.18 GHz), explicitly excluding turbo boost and hyperthreading from the reported capacity figure.]

vSphere simply takes the base frequency x number of cores.
- It does not include turbo boost
- It does not include hyper threading.
The above is great for mission critical, where you need to be conservative and performance takes priority. For the rest of the workload, you can actually squeeze more. However, you need to set expectation as as the CPU speed depends on the model you buy.
I recommend you optimize the above answer. You can get more while keeping the trade off low. How?
Let’s answer with a simple example. You have 2 ESXi servers:

[Image: The image compares two ESXi host configurations: **ESXi 01** has 20 cores/40 threads at 1 GHz nominal (1.25 GHz turbo), while **ESXi 02** has 10 cores/20 threads at 2 GHz nominal (2.5 GHz turbo). Despite having identical total nominal capacity (20 GHz each: 20×1 GHz vs 10×2 GHz), the hosts differ significantly in core count and per-core frequency. This illustrates how vCenter's core-based capacity model can mask performance trade-offs between fewer fast cores versus more slower cores when sizing VM workloads.]

Using the model provided by vCenter, what’s the total capacity of each server?
Answer:
- ESXi 1 capacity = 20 cores x 1 GHz = 20 GHz.
- ESXi 2 capacity = 10 cores x 2 GHz = 20 GHz.
The above is a good answer, but can we improve it?
On ESXi 2, VM will run 2x faster, but you can only run half as many VMs. If you run the same number of vCPU as you do on ESXi 1, the VMs on ESXi 2 will compete and incur ~50% CPU Ready time. Workload performance likely becomes unpredictable. CPU context switch will be very high.
That means ESXi 2 has 2x the performance, but 0.5x the capacity. The 200% performance only happens when you run at 50% capacity of ESXi 1. When you load ESXi 2 with 1x the capacity of ESXi 1, its performance could drop below 1x of ESXi 1.
The above shows the imperfect correlation between performance and capacity. This is why you cannot use a single number to measure both.
You need 2 answers:
- Space: Do I have enough capacity to run the VM?
- Speed: When I run it, what is the CPU frequency during the run?

|  | ESXi 01 | ESXi 02 |
| --- | --- | --- |
| Space | 40 threads | 20 threads |
| Speed | 31.25 GHz | 31.25 GHz |

Not what you expect?
Okay, let’s dive in.

#### Capacity Metrics

The CPU capacity is in thread, not in Hertz.
Capacity does not consider performance or speed. It simply looks at the part of the CPU where a VM can run. Since a thread can run in parallel with partner thread in a core, it is as simple as counting the physical threads.
ESXi 01 can run 40 vCPU worth of VMs concurrently. By that definition, that means you do not overcommit when you run 40 vCPU, if we set aside hypervisor overhead for now. This is true as the VMs do not experience CPU Ready. Sure, they will run slower but that’s a performance, and not capacity question. The effect would be the same as having a slower hardware. Capacity is not performance. Think of capacity as space, while performance as speed.
Using highway analogy, the number of lanes is fixed, but the allowed speed typically vary depends on the segment of the highway.
BTW, this is consistent with AWS. It counts the threads, not physical core. AWS market it as no overcommit. Yes, they use allocation model and not utilization model.

| Metric | Allocation Model | Demand Model |
| --- | --- | --- |
| Total Capacity | Total physical threads in the box | Core utilization and thread utilization. Do not use CPU Cycles (GHz). |
| Hypervisor Overhead | No of physical threads you manually assigned | Not applicable, as it’s included in total ESXi counters |
| Consumption | Sum of all running VM vCPU | Core utilization and thread utilization. Usage (GHz) tends to over report. |
| Consumption | Performance is not applicable. | Ready + CoStop. Swap Wait and Other Wait are not CPU related. |


##### Hyper Threading

What should we do with HT?
I recommend enabling it, but set your customers expectation on the CPU speed.
HT technology may change in the future. New Intel Xeon no longer has HT, but uses small core and big core instead.

##### CPU Cycles

Do not express an ESXi capacity in MHz, as the total “capacity” becomes volatile.
- If you enable hyper threading, the total capacity only goes up by 1.25x. However, the speed reduction experienced by VM is significant. It’s 37.5% slower.
- All Cores Turbo brings up the total capacity. This number varies per CPU model.
The usage of GHz as the unit complicates calculation as it’s mixing performance and capacity.

###### All Cores Turbo

I highly recommend you review this article by IOFLOOD. I’ve highlighted in green a key point stating your CPU is actually operating at a higher speed.

[Image: The image displays a text excerpt explaining that **All Cores Turbo** is the true operational speed of a CPU when all cores are actively processing, noting that neither Intel nor AMD prominently advertises this specification. The highlighted phrase "this is the true speed of the CPU" emphasizes the key point referenced in the surrounding text — that All Cores Turbo represents the actual sustained clock speed rather than the marketed base or single-core boost frequency. This supports the book's calculation formula where a **1.25x All Cores Turbo multiplier** is applied to derive total ESXi host capacity (e.g., 31.25 GHz).]

While it’s a good news that you have more capacity, the issue is this number is not always exposed via API.
Now you know why the answer is 31.25 GHz.
Here is the formula:
- ESXi 01: 20 cores * 1 GHz Base Speed * 1.25x HT * 1.25 All Cores Turbo
- ESXi 02: 10 cores * 2 GHz Base Speed * 1.25x HT * 1.25 All Cores Turbo

##### Hypervisor Overhead

In the planning stage, we need a single number for usable capacity.
In the monitoring stage, we should be mindful that our estimate may be too aggressive or conservative. This is why tracking contention is paramount.
What number do I recommend?
Based on the profiling documented in the kernel section later on, I’d use the following at 2.5 GHz clock speed:
- 12 threads if you use NSX and vSAN.
- 4 threads if you use ESXi only.
NSX EDP adds 2-4 cores as it regularly polls the network card.
vSphere Replication and HCX need to be sized separately.
vSAN File Services needs 2 vCPU as it's a VM. Set reservation.

##### Consumption

For allocation-based model, the consumption is simply the configured vCPU for all the running VM.
For demand-based model, the consumption is the maximum of CPU Usage and CPU Reservation for all the running VMs.
Do not include VM CPU contention, but make sure performance is tracked explicitly.

#### Hypervisor Metrics

I’ve given recommendations on the number to provide as part of the planning process. Now let’s dive into how the numbers are derived.
The following screenshot shows the CPU counter names used by vSphere Client UI. What do you notice?

[Image: The image displays a table of VMware vSphere CPU-related performance counters for the system resource group, showing 10 metrics including **Resource CPU active**, **running**, **maximum limited**, **allocation shares/min/max**, and **CPU usage**. Most counters use a **"Latest"** rollup type measured in **%** or **MHz**, except "Resource CPU usage ({rollupType})" which uses **"Average"** rollup in **MHz**. This table contextualizes the surrounding text's point about rollup types — specifically how "Latest" versus "Average" rollups produce significantly different values, and why the **CPU Usage** counter (with its Average rollup and coverage of all 4 resource groups) is preferred for utilization tracking over Running or Active counters.]

Yes, the roll up of the counter.
In general, when you take the latest value of something, you tend to get a much higher value than averaging the entire period.

##### Utilization

There are 3 counters provided to track the actual utilization.
- Usage
- Running
- Active
Usage is what you should use as it has the 4 resource groups and their sub pools.
Running and Active counters only has these 3 objects, hence they are less useful. You lose host/user, host/opt so you won’t get complete picture.

[Image: The image shows a **target object selection interface** for a vSphere performance chart, listing three selectable objects: **host/system**, **host/system/vmotion**, and **host/vim**. This corresponds to the surrounding text's explanation that the **Running and Active counters only expose these 3 resource group objects**, in contrast to the Usage counter which includes all 4 resource groups (including host/user and host/opt). The limited object set visible here illustrates why Running and Active counters provide an incomplete picture of memory/resource utilization.]

Plus, Active uses “latest” as its rollup.
If you still need to know about Active and Running, reach out to me and happy to share more details.

###### Usage

Now that we know which counters to use, what do you expect the values of the 4 groups?
Here is a sample from ~400 ESXi hosts, where I sort the top 7 from highest System usage.

[Image: ## Image Description

This table displays CPU resource metrics for ~400 ESXi hosts, showing the **top 7 hosts by highest System usage**, with columns for **Host (total), system, vim, iofilters, user, Usage, and Demand** (all in GHz). The data demonstrates that **host/system values (2.28–3.66 GHz) are significantly lower than host/user values (5.93–24.86 GHz)**, confirming that the CPU Usage metric primarily reflects VM workloads rather than kernel overhead. The bottom two bold rows show the **cluster average (12.21 GHz usage, 0.69 GHz system)** and **peak values (91.65 GHz usage, 3.66 GHz system)**, with Usage matching the Host column exactly — validating that `CPU \ Usage (MHz)` equals `System \ Resource CPU Usage (Average) (MHz)`.]

The bottom two rows show the summary. The first summary is the average among all the hosts, while the last row is the highest value.
Usage maps to the ESXi CPU Usage metrics under CPU group.

[Image: ## Image Description

This screenshot shows the **vSphere performance chart configuration interface** for selecting the **"Resource CPU Usage (Average)"** metric (measured in MHz, counter: `resourceCpuUsage`, Rate type), with the timespan set to **Real-time (last 1 hour)** between 11/11/2023–11/12/2023, displayed as a **Line Graph**. The target object selected is **"host"** from a hierarchy that includes host/iofilters, host/system, and other sub-components. This demonstrates the configuration used to validate that the **CPU \ Usage (MHz)** metric equals **System \ Resource CPU Usage (Average) (MHz)** at the host level, as referenced in the surrounding text.]

The value at host matches the value of CPU Usage. This means the metric CPU \ Usage (MHz) is the same with System \ Resource CPU Usage (Average) (MHz).
As the value contains VM metrics, the value is much higher than the kernel. You can see the host/system is far lower.

[Image: ## Image Description

The chart displays **Resource CPU Usage (Average) in MHz** for two objects over a ~1-hour period (7:30–8:27 PM): the **host** (blue line, averaging ~22,611 MHz, ranging 20,331–28,129 MHz) and **host/system/kernel** (black line, nearly flat near zero, averaging ~377 MHz, ranging 213–598 MHz). This demonstrates that the **ESXi kernel (host/system) CPU consumption is negligibly small** (~287 MHz latest) compared to total host CPU usage (~23,097 MHz latest), visually confirming that the vast majority of CPU utilization is attributable to VM workloads rather than the ESXi hypervisor kernel itself.]


###### Real World Samples

I plotted 364 ESXi hosts running production workload. All of them are doing at least 100 GHz and are running vSAN and NSX. For vSAN, they are a mixed of OSA and ESA architecture.
The line below shows the kernel relative to the total CPU Usage.

[Image: ## Image Description

The chart displays the **ESXi kernel CPU utilization as a percentage of total CPU usage** across 364 production ESXi hosts (all running ≥100 GHz, vSAN, and NSX), sorted in descending order from position 1 to 364. Values range from approximately **34% at the highest (host #1) down to ~2% at the lowest (host ~361)**, following a steep power-curve decline in the first ~30 hosts before gradually tapering. This demonstrates that while a small number of hosts exhibit relatively high kernel overhead (>20%), the **majority of hosts fall between roughly 10–15%**, illustrating the variable but generally moderate kernel CPU cost imposed by vSAN and NSX workloads.]

In terms of absolute utilization, the actual utilization has a wide range. This is despite all these ESXi were running at least 100 GHz.

[Image: ## Image Description

The chart displays **Kernel Utilization in GHz** across **364 ESXi hosts**, ranked in descending order (x-axis: hosts 1–364, y-axis: 0–45 GHz). The curve shows a steep decline from ~44 GHz for the highest-utilized host down to ~2–3 GHz for the lowest, with the majority of hosts clustered between **10–20 GHz**. This demonstrates the wide absolute range of kernel CPU utilization across production ESXi hosts running vSAN and NSX, even though all hosts share a common baseline of at least 100 GHz total CPU usage.]

Take note there is no perfect correlation between kernel utilization and VM utilization. This is especially true when the kernel has NSX and vSAN. All these 364 ESXi were running vSAN (mixed of OSA and ESA) and NSX.
The following chart shows that a great majority were below 10%. There is no strong correlation between the relative overhead and the absolute overhead.

[Image: ## Image Description

This scatter plot displays **CPU kernel (hypervisor) utilization percentage (Y-axis, 0–50%) vs. total CPU load in GHz (X-axis, 100–170 GHz)** across 364 ESXi hosts running vSAN and NSX. The majority of data points cluster between **10–20%** kernel utilization regardless of absolute CPU load, with a **red reference line at ~19–20%** and two **red outlier points** at ~113 GHz/39% and ~153 GHz/45%. The chart demonstrates **no strong correlation** between higher absolute CPU utilization (GHz) and kernel overhead percentage, with most hosts remaining below the 20% threshold across the entire frequency range.]

Another measurement, taken at a different time. This time there were 557 ESXi with CPU Usage > 100 GHz, with 2 of them clocking > 170 GHz.

[Image: ## Chart Description

This scatter plot displays **Hypervisor CPU Usage (GHz) vs Total CPU Usage (GHz)** across 558 ESXi hosts, with total CPU usage on the X-axis (100–180 GHz) and hypervisor CPU overhead on the Y-axis (0–60 GHz). The data demonstrates **no meaningful correlation** between total CPU load and hypervisor overhead — the majority of hosts cluster below 25 GHz of hypervisor overhead regardless of total CPU usage, with threshold annotations showing only **5.6% above 25 GHz, 2.0% above 30 GHz, and 0.7% above 35 GHz**. Three red-highlighted outliers exceed 35 GHz of hypervisor overhead, while green-highlighted clusters at ~3–6 GHz represent the lowest overhead values, confirming that vSAN/NSX hypervisor overhead remains relatively flat and independent of total workload intensity.]

There were 2 outliers at > 40 GHz, highlighted in orange. The hypervisor overhead remains steady at 100 GHz vs > 150 GHz. I drew a red line at 25 GHz to show that majority of the numbers are below this.
Plot the values across all your ESXi hosts. If you take enough hosts, you will notice the values vary. The following chart shows 558 ESXi hosts. Almost all are running both vSAN and NSX. They are all running at least 100 GHz. What do you notice?
Yes, there is hardly any correlation between total CPU Usage and hypervisor CPU Usage.
I drew the following illustration to show the lack of predictable relationship between hypervisor CPU reservation, hypervisor CPU usage and total CPU usage.

[Image: ## Image Description

The chart illustrates the relationship between **Total CPU Usage**, **Hypervisor CPU Usage**, and **Hypervisor CPU Reservation** (MHz/GHz) over time on an ESXi host. As VMs are added (marked by "0 VM" and "Few VM" annotations), Total CPU Usage rises dramatically and unpredictably, while Hypervisor CPU Usage (red line) remains consistently low and relatively flat — staying near or below the Hypervisor Reservation threshold (dotted gray line). This demonstrates that **hypervisor CPU overhead has no predictable correlation with total workload CPU consumption**, regardless of VM density.]


###### Network Impact

What’s the kernel overhead to do network packet processing?
The following ESXi was doing > 40 Gigabit per second multiple times. It was processing > 3 million packets.

[Image: ## Image Description

The image shows two time-series charts for a single ESXi host spanning **April 28 – May 5**, displaying **Network Usage Rate (Gbps)** peaking at **41.75 Gbps** and **Network Aggregate Packets per Second** peaking at **3,134,645.5 pps (~3 million packets/sec)**. Both metrics show sustained high activity with frequent spikes throughout the period, with minimum values near zero (0.042 Gbps / 2,107 pps). This demonstrates that even under extreme network load (>40 Gbps, >3M pps), the kernel CPU overhead remained minimal (<8 GHz), illustrating the efficiency of ESXi's network packet processing in the hypervisor.]

Hardly any impact on the kernel. The kernel was less than 8 GHz.

[Image: ## Image Description

The chart displays three metrics over approximately one week (April 27 – May 5): **ESXi kernel CPU usage** (teal/cyan, highly volatile, ranging from ~0 to 7.5 GHz), **CPU reservation** (orange, relatively flat near ~0.2–0.4 GHz), and a third near-zero metric (blue, essentially 0). The teal kernel CPU line oscillates dramatically with frequent spikes throughout the period, while the orange reservation line remains largely stable and low. This illustrates the **lack of predictable relationship** between CPU reservation and actual kernel CPU usage — high kernel activity occurs independently of the reservation value, confirming the surrounding text's assertion that these metrics do not correlate reliably.]


###### Storage Impact

Storage IO processing can require more kernel if the IOPS and throughput are high. The following ESXi hit > 200K IOPS two times.

[Image: ## Image Description

The image displays three performance charts from a VMware ESXi host covering approximately a 24-hour period (May 3–4): **Disk Total Throughput** (peaking at **1,456.75 MBps**), **Disk Aggregate Total IOPS** (peaking at **251,917.86 IOPS**), and **Network Usage Rate** (peaking at **11.3 Gbps**). Two significant spike events are visible — one around 9:00 PM and a larger one around **10:00 AM** — where both disk throughput and IOPS simultaneously exceeded ~1,000 MBps and ~200K IOPS respectively. In the context of the surrounding text, this image demonstrates the storage I/O load on the ESXi host that caused a corresponding kernel CPU overhead spike (referenced as exceeding **10 GHz** in the following text), illustrating how high IOPS (>200K) drives measurable kernel processing costs unlike network packet processing.]

You can see a corresponding spike in the kernel. It went above 10 GHz.
The red dot is because of network.

[Image: ## Image Description

This time-series chart displays **CPU kernel utilization (GHz)** for an ESXi host over approximately 24 hours (May 3–4), with the y-axis scaled to 10 GHz. The **teal/cyan line** shows kernel CPU usage with two prominent spikes exceeding **10 GHz** — one around **9:00–10:00 PM** and a larger one near **10:00–11:00 AM** — corresponding to the >200K IOPS storage events mentioned in the text. A **red dot** near **12:00 PM** marks a secondary spike attributed to **network activity**, while the **orange and blue lines** (likely ready or other CPU metrics) remain nearly flat at ~0 throughout.]


##### Reservation

Utilization is relatively more volatile or dynamic, while reservation is logically more stable. The following screenshot shows CPU Usage fluctuates every 20 seconds, while reservation remains perfectly constant. Expect Usage to be higher reservation at high utilization.

[Image: ## Image Description

This VMware vSphere performance chart displays **CPU metrics for host/system** over approximately one hour (8:38–9:37 AM on 08/05/2022), showing **Resource CPU Usage (Average)** fluctuating dynamically between **115–294 MHz** (green line), while the **Resource CPU allocation minimum/reservation remains perfectly flat at 220 MHz** (orange horizontal line). The tooltip highlights a specific data point at 9:04 AM showing 120 MHz of CPU used by the Service Console. This demonstrates the text's point that **utilization is volatile while reservation remains constant**, with the legend confirming CPU maximum limited values (1 min and 5 min) are both zero, indicating no CPU limits are applied to kernel processes.]

Notice the maximum limited value is perfectly flat. That’s what you want as kernel processes should not have a limit.
The above is for host/system. The reservation is surprisingly low.
Now let’s look at host/vim. What do you notice from the following screenshot?

[Image: ## Image Description

The screenshot shows a VMware vSphere performance chart for **host/vim** over a 1-hour period (08/05/2022, 8:39–9:39 AM), displaying four metrics: **Resource CPU allocation minimum (6,651 MHz, perfectly flat blue line)**, **Resource CPU usage average (ranging 169–994 MHz, orange line with a spike near 8:55 AM)**, and two **Resource CPU maximum limited** metrics (both at 0%). The tooltip highlights the CPU allocation reservation at **6,651 MHz** at 8:55 AM, confirming the reservation is consistently ~6.6 GHz throughout the observation window. This contrasts with the host/system resource group discussed previously, demonstrating that host/vim carries a surprisingly high and stable CPU reservation (~6.6 GHz) compared to the relatively low actual CPU usage.]

Surprisingly the reservation is not low. It’s around 6.6 GHz.

###### Real World Samples

The above is from 1 ESXi. We need to plot for many to get a better understanding. The following diagram shows the distribution of the kernel overhead based on a sample of almost 400 ESXi in production environment.

[Image: ## Image Description

This histogram displays the distribution of VMware ESXi kernel overhead (in GHz) across approximately 400 production ESXi hosts, with frequency counts on the Y-axis and overhead frequency bands on the X-axis. The distribution is heavily concentrated in the **6–8 GHz range (~197 counts)** and **8–10 GHz range (~155 counts)**, together accounting for the vast majority of observations. This confirms the preceding text's assertion that kernel overhead reservations cluster around 6–10 GHz, with very few hosts falling outside this range (bins 0–6, 10–16 GHz all show counts below ~10).]

By far the majority of the values lie in 6 – 10 GHz.
Their values tend to be stable over days, although from time to time I see fluctuating metrics, which is reasonable as there are multiple factors impacting the reservation.
The following chart shows both the fluctuating pattern and steady pattern (most common). They are from 2 ESXi hosts.

[Image: The chart displays CPU Overhead (GHz) metrics for two ESXi hosts over a ~24-hour period on March 26, with values ranging between approximately 7–8.5 GHz. The purple line shows a **fluctuating pattern** with frequent spikes reaching ~8+ GHz, while the pink/red line remains nearly **flat at ~5 GHz**, representing the steady/stable pattern. This illustrates the two behavioral archetypes described in the text: most ESXi hosts maintain stable CPU overhead values day-over-day, while some exhibit intermittent fluctuation due to varying factors affecting the hypervisor reservation.]


### Memory

Memory is simpler than CPU as there is only “space” dimension. There is no “speed”.
Memory is more complex than CPU as Guest OS and VM are 2 different realms. None is perfect as an input.

#### Capacity Metrics

There are

| Metric | Allocation Model | Demand Model |
| --- | --- | --- |
| Total Capacity | Total physical memory in the box. This is the same for either model | Total physical memory in the box. This is the same for either model |
| Hypervisor Overhead | No of GB you manually assigned | Not applicable, as it’s included in total ESXi counters |
| Consumption | Sum of all running VM configured RAM. | ESXi Consumed |
| Consumption | Performance is not applicable. | ESXi Swapped + Zipped + Guest OS Ballooned. |


##### Hypervisor Overhead

In the planning stage, we need a single number for usable capacity.
In the monitoring stage, we should be mindful that our estimate may be too aggressive or conservative. This is why tracking contention is paramount.
What number do I recommend?
Based on the profiling documented in the kernel section later on, I’d say:
- 64 GB if you use NSX and vSAN
- ~20 GB if you use ESXi only. I don’t have real world numbers to back this up as the environment I have is NSX and vSAN.

##### Demand Metric

Unlike allocation, demand is tricky as different layers in virtualization has their own perspective. ESXi applies multiple memory management techniques, which makes it harder to determine the total demand:
- TPS results in less actual usage.
- Balloon means ESXi is under memory pressure, or the VM hit a limit.
- Compress means the pages are still in DIMM, albeit occupying less space. How much less depends on the zipped result and if the remaining page is fully used or not.
- Swapped and compressed share the same input. When a page cannot be compressed, it got swapped.
- Host cache.
- Memory tiering such as Intel Optane.
- We exclude VM overhead as it’s negligible.
Because of the above, it is better not to mix metrics from Guest OS and VM.
ESXi Demand = Kernel Consumed + Sum of (Running VM Demand)
where VM Demand = Min (Limit, Consumed + Ballooned + Zipped + Swapped)
Limitation of VM counters:
- Consumed metric is mostly inactive pages. So adding ballooned, zipped, swapped will make it even more conservative.
- The Guest OS counter is more accurate as it’s closer to application. It tends to be smaller. However, Guest OS is unaware of ESXi memory management techniques.

#### Hypervisor Metrics

The following screenshot shows the counter names used by vSphere Client UI

[Image: This image displays a table of **VMware vSphere system resource group memory metrics**, listing 11 counters including allocation maximum/minimum, consumed, mapped, overhead, share saved, shared, swapped, touched, and zero — all measured in **KB** except "Resource memory allocation shares" (num). The table defines each metric's description, mapping hypervisor-level memory management counters to their functional meaning within the system resource group context. In the surrounding text, this serves as a reference for the hypervisor memory metrics visible in the vSphere Client UI, preceding a discussion of their rollup type (Latest) and stat type (Absolute).]

Unlike CPU, the Rollups column values are all Latest. This makes sense as memory is measure storage space. You want to know the last value, not the average over collection period.
The Stat Types column values are all Absolute.

| Allocation maximum | As per CPU, this is the limit. |
| --- | --- |
| Allocation minimum | As per CPU, this is reservation. |
| Shares | Relative shares of each the kernel world. This is the kernel internal metric, not something vSphere Administrator should change |
| Consumed | The actual consumption. Just like CPU, this can be lower than the reservation. The host/vim world has no reservation. |
| Mapped | I’m unsure what mapped means. Regardless, there seems to be no use case for customer operations.  The rest of the metrics are fairly similar with the associated metric at VM and ESXi level. |
| Overhead | I’m unsure what mapped means. Regardless, there seems to be no use case for customer operations.  The rest of the metrics are fairly similar with the associated metric at VM and ESXi level. |
| Share Saved | I’m unsure what mapped means. Regardless, there seems to be no use case for customer operations.  The rest of the metrics are fairly similar with the associated metric at VM and ESXi level. |
| Shared | I’m unsure what mapped means. Regardless, there seems to be no use case for customer operations.  The rest of the metrics are fairly similar with the associated metric at VM and ESXi level. |
| Swapped | I’m unsure what mapped means. Regardless, there seems to be no use case for customer operations.  The rest of the metrics are fairly similar with the associated metric at VM and ESXi level. |
| Touched | I’m unsure what mapped means. Regardless, there seems to be no use case for customer operations.  The rest of the metrics are fairly similar with the associated metric at VM and ESXi level. |
| Zero | The entire block contains just a series of 0. |


##### Utilization

I plotted 607 production ESXi running vSAN and NSX. The hosts have Consumed memory between 650 GB and 1450 GB. As expected, the kernel overhead decreases relatively as total memory grow.

[Image: ## Chart Description

This scatter plot displays **hypervisor overhead percentage (Y-axis, 4%–12%) relative to ESXi Consumed memory in GB (X-axis, 600–1500 GB)** across 607 production ESXi hosts running vSAN and NSX. The chart demonstrates a clear **inverse relationship**: overhead decreases from ~10–12% at 650–700 GB consumed memory to ~4–5% at 1400+ GB. Notably, the data points form **approximately 5 distinct horizontal bands/clusters**, suggesting discrete groupings likely tied to vSAN configuration differences, as referenced in the surrounding text.]

The number dropped to well below 10% once Consumed passed 800 GB. This means that the absolute amount plateau at a certain level. We can validate that by plotting the absolute utilization.

[Image: ## Chart Description

This scatter plot displays **Hypervisor overhead (GB) vs ESXi Consumed Memory (GB)** across 607 production ESXi hosts running vSAN and NSX, with Consumed memory ranging from **650–1450 GB** on the X-axis and overhead values spanning approximately **33–77 GB** on the Y-axis. The data reveals **5 distinct horizontal band clusters** (highlighted in yellow) at roughly **35, 47, 63, 70, and 76 GB** of overhead, suggesting discrete groupings likely tied to vSAN configuration differences. Notably, the overhead values plateau at fixed absolute levels rather than scaling with consumed memory, confirming the text's assertion that hypervisor overhead stabilizes as a constant absolute amount rather than growing proportionally with total memory.]

Interestingly, there are levels. From the preceding chart, you can see there are 5 groups of similar number range. I think it’s because of vSAN configuration.

##### Reservation

The metric name is Memory \ ESX System Usage (KB).
It is a raw counter from vCenter. Just in case you’re wondering, the name ESX System Usage is a legacy name.

[Image: ## Image Description

This VMware vSphere performance chart displays **system memory metrics** for a one-hour window (08/05/2022, 8:36–9:35 AM), showing four counters: **host/system Resource Memory Allocation Minimum** (~26.5 GB, blue line), **host/system Resource Memory Consumed** (~22.3 GB, green line), **host/vim Resource Memory Allocation Minimum** (0 KB, black), and **host/vim Resource Memory Consumed** (~703 MB, orange line near zero). All four metrics remain **essentially flat/constant** throughout the entire monitoring period with negligible variation (e.g., allocation minimum ranges only from 26,481,736 to 26,514,472 KB). This flatness validates the preceding text's assertion that ESXi kernel/system memory reservations plateau at a stable level, as these values represent **reservations rather than dynamic consumption**.]

The following is an ESXi 6.7 U3 host with 1.5 TB of memory. Notice the kernel values remains constant over a long period. The number of running VM eventually dropped to 0. While the Granted counter drops to 1.5 GB (not sure what it is since there is no running VM), the kernel did not drop. This makes sense as they are reservation and not the actual usage.

[Image: ## Image Description

This time-series chart (Sep 13 – Feb 28) displays four VMware ESXi memory metrics for a **1.5 TB host**: **Memory Consumed (67.13 GB)**, **VMkernel Usage (55.49 GB)**, **Memory Granted (9.53 GB)**, and **Memory Allocated on all Powered On Consumers (8 GB)**, with a tooltip captured on **Tuesday, Jan 4, 04:00–11:59 PM**. The chart demonstrates that the **VMkernel reservation (cyan line, ~60 GB)** remains essentially flat throughout the entire period, even as VM workloads (pink/blue lines) drop sharply from ~20 GB to near **0 around Jan 3** when running VMs reached zero. This illustrates the core concept that **kernel memory reservations are static allocations**, independent of actual VM utilization, consistent with the surrounding text's explanation that these are reservations, not actual usage.]

Based on a sample of 500+ ESXi hosts, the range varies from 6 GB to 88 GB. In an ultra large ESXi with 12 TB RAM running vSAN and NSX, the reservation went up to 300 GB.

##### Utilization vs Reservation

Logically, utilization does not always correspond to the reserved amount. The following chart shows the reservation remains steady when the utilization drops by 90%, from 40 GB to single digit.

[Image: ## Image Description

The chart displays two ESXi host memory metrics over a ~4-week period (Mar 4–28): **Memory|ESX System Usage (KB)** (purple, ~59,611,356 KB / ~57 GB) and **Memory|VMkernel Usage (KB)** (pink, ~40,286,652 KB / ~38 GB at peak). The pink VMkernel usage line shows a **dramatic ~90% drop around Mar 17–18**, falling from ~40 GB to near 0 GB, while the purple ESX System Usage remains virtually unchanged at ~57–60 GB throughout. This demonstrates the book's key point that **reservation remains steady even when utilization drops sharply**, illustrating that VMkernel usage is a utilization metric while ESX System Usage reflects reserved memory that does not fluctuate with actual consumption.]

To see the actual usage, choose the metric Resource Memory Consumed metric from vSphere Client. Stack them, and you see something like this. The system part typically dwarfs the other 2 resources.

[Image: ## Image Description

The chart displays **Resource Memory Consumed** (in KB) for three host resources — `host/iofilters`, `host/system`, and `host/vim` — over a ~1-hour real-time period on 06/10/2021. The dominant component is `host/system` (gray, ~3.68 GB average), dwarfing `host/vim` (green, ~299 MB average) and `host/iofilters` (blue, ~6.8 MB), which are barely visible at this scale. This stacked chart demonstrates that the **system resource consumes the vast majority** of host memory, validating the text's claim that "the system part typically dwarfs the other 2 resources" when visualizing actual memory utilization.]

Do not take the value from Memory \ VMkernel consumed counter. That’s only the system resource. You can verify by plotting this and compare against host/system resource. You will get identical charts.

[Image: ## Image Description

This screenshot shows the **vSphere Client performance chart counter selection interface**, specifically under the **Memory** category. The counter **"VMkernel consumed"** is selected (checked, highlighted in blue), displaying its properties: **Average rollup, KB units, internal name "sysUsage," Absolute stat type**, described as "Amount of host physical memory..."

In context, this image illustrates the warning from the surrounding text — that the **Memory › VMkernel consumed counter represents only the system/kernel resource portion** of memory usage, not total host memory consumption, and should not be used as a proxy for overall memory capacity planning.]

This value is for vSphere kernel modules. It does not include vSAN.

### Implementation

Download the Capacity Planning spreadsheet from here. It combines both models, and apply 3 class of services.

[Image: The image shows a Broadcom Box.com shared folder (`broadcom.ent.box.com/v/OpsYourWorld`) titled **"Private Cloud Operations"** containing four directories: **Books**, **Presentation Slides**, **VCAP Exam Study Guide**, and **Spreadsheet**. In the context of the surrounding text, this is the download location for the **Capacity Planning spreadsheet** referenced by the author, which combines multiple capacity models and applies three classes of service for vSphere memory planning.]


##### Total Capacity

The first thing you need to confirm is the size of the host. The spreadsheet comes with default values that I think provides a good balance between cost and size.

[Image: ## Image Description

This spreadsheet shows **host hardware configuration inputs** for a VMware vSphere capacity planning model, with six parameters: **CPU Speed (2.5 GHz)**, **Cores (64)**, **Threads (128)**, **All Core Turbo (1.25x base frequency)**, **RAM (768 GB)**, and **NVMe (768 GB)**. The green-highlighted cells indicate user-editable input fields where actual hardware specifications should be entered. In context, this represents the first step of the capacity planning spreadsheet — defining physical host size before calculating total usable capacity across CPU, memory, and storage tiers.]


##### Aria Operations metrics


| Memory \ Total Capacity (KB) | The capacity as seen by the kernel, which is essentially the physical size. |
| --- | --- |
| Memory \ Utilization (KB) | Sum of demand from all running VM (see below) + ESXi kernel reservation. Demand is the maximum of VM reservation and Guest OS needed memory + total page-in in the collection cycle (default is 5 minutes). Page in = page in rate x memory block size.  If Guest OS is missing, it falls back to consumed.  The amount also includes the VM memory overhead. |
| Memory \ Workload (%) | Utilization / Total Capacity. Likely this is usable. |
| Memory \ Memory Allocated on all Powered On Consumers | Sum of all running VM configured memory.  This is used in allocation model. |

At the vSphere Cluster level, here are the metrics:

| Cluster Configuration \vSphere HA \ HA Memory Failover (%) | Cluster HA failover for memory. |
| --- | --- |
| Memory\|Demand\|Usable Capacity after HA and Buffer (GB) | Total Capacity minus HA above and buffer (not shown as property) |
| Memory\|ESX System Usage (GB) | Kernel reservation |
| Memory \ Utilization (KB) | Sum of all ESXi |
| Memory\|Demand\|Workload (%) | Utilization / Usable |
| Memory \ Memory Allocated on all Powered On Consumers | Sum of all ESXi |
| Memory\|Workload (%) | Normalized average of all ESXi? |


### Cluster Capacity

Cluster capacity is more complex than ESXi capacity due to the following cluster-level property

| Total Capacity | Unlike ESXi, this could be dynamic due to reasons such as maintenance mode and DPM. Hybrid cloud such as VM sports on-demand host that is added dynamically. Dynamic cluster size increases complexity significantly. As a best practice, avoid removing hosts from the cluster if the cluster has < 5 ESXi hosts as your availability overhead becomes higher. |
| --- | --- |
| Buffer | For most cases, this is 10% for CPU and 0% memory.  For stretched cluster, this is 50% for CPU and memory. For DR, this depends on the DR workload. |
| HA | This impacts usable capacity. For example, if it’s 9+1, then cluster average utilization at 100% means each host is averaging 90%. |
| Stretched Cluster | The 2 sites have their own capacity calculation, yet they impact each other. |
| Host-VM Affinity | The group of hosts have their own capacity, operating like a subcluster. |
| Resource Pool | Each pool has their own capacity. |
| DR | A cluster may participate in disaster recovery by providing destination during DR dry run and actual. This is why you need to specify buffer, so that usable capacity reflect this rarely happens workload. BTW, the buffer default value is 0% in VCF Operations. |


#### Total vs Usable


[Image: ## Image Description

The diagram illustrates the capacity breakdown of a **vSphere cluster with 4 nodes**, showing how **Total Capacity** is partitioned into distinct layers: **VMkernel overhead** (bottom), **Usable Capacity** (middle, highlighted with dashed border), **Capacity Buffer** (top), and **HA** reservation (right node, shown as a full-height dedicated block).

The image demonstrates that **Usable Capacity** represents only a subset of total cluster resources — specifically the 3 non-HA nodes minus VMkernel overhead and the buffer — while one entire node is reserved exclusively for **High Availability (HA)** failover capacity.

This visually supports the surrounding text's explanation that in an N+1 HA configuration, one host's worth of capacity is set aside, reducing the operationally usable capacity denominator used for capacity calculations.]

Let’s take an example.
Assuming 10 hosts in a cluster, with N+1 HA setting, and Buffer is set to 0%.
Usable Capacity is 9 hosts, so 9 is the 100% operationally.
From here, if a host is out, the calculation depends on what actually caused it. There are 3 different scenarios:

|  | Intentional? | Desired? | Impact |
| --- | --- | --- | --- |
| vSphere DPM | Yes | Yes | Total Capacity |
| Maintenance Mode | Yes | No | Usable Capacity |
| HA happen | No | No! | Usable Capacity |

Intentional means it’s something you knowingly execute. In the case of vSphere DPM, it’s also something you want to happen. In the case of Maintenance Mode, you intentionally do it but it’s not something you want. So the 2 have different impact. vSphere DPM does not impact your HA as you still want HA even though you take out host(s). The length of DPM can be as long as there is no request for extra host. The length of maintenance mode should be as short as possible, hence the name maintenance.
HA events is an outage. It is obviously not something desired.
Undesired event impacts usable capacity and not total capacity.

|  | DPM Event | Maintenance Mode | HA Event |
| --- | --- | --- | --- |
| Total Capacity | 9 | 10 | 10 |
| Usable Capacity | 8 | 9 | 9 |
| Actual Availability | 9/9 = 100% | 9 / 10 = 90% | 9 / 10 = 90% |
| Operational Availability | 9 / 8 = 100%  (capped) | 9 / 9 = 100% | 9 / 9 = 100% |

The actual availability drops to reflect reality. The operational availability remains at 100% due to N+1 HA design.
For completeness, let’s follow with a 2nd host out:

|  | DPM Event | Maintenance Mode | HA Event |
| --- | --- | --- | --- |
| Total Capacity | 8 | 10 | 10 |
| Usable Capacity | 7 | 8 | 8 |
| Actual Availability | 8 / 8 = 100% | 8 / 10 = 80% | 8 / 10 = 80% |
| Operational Availability | 8 / 7 = 100% | 8 / 9 = 89% | 8 / 9 = 89% |

BTW, the metric Total Capacity only counts those ESXi hosts that are connected to vCenter. If a host is connection state = disconnected, its value becomes blank, so the Total Capacity is affected.

[Image: The image shows two time-series charts for **SiteO2-Cluster-O2** spanning from ~4:00 PM on Jan 23 to ~2:00 AM on Dec 24. The top chart displays **Memory|Total Capacity (TB)**, dropping from a high of **1.5 TB to a low of 1 TB** around 10:00 PM, while the bottom chart shows **Summary|Number of Running Hosts**, dropping from a high of **6 to a low of 5 hosts** at the same timestamp (~10:00 PM). This corroborates the surrounding text's explanation that Total Capacity is directly affected when a host becomes disconnected or removed — both metrics decline simultaneously, confirming that losing one host reduces the cluster's reported memory capacity from 1.5 TB to approximately 1.25 TB (i.e., 5/6 of original capacity).]


## Other Metrics


### Availability

The availability of a complex system such as an ESXi host is not a simple binary. There is degradation, which is important to distinguish to help manage in large farm.

[Image: ## Image Description

The image defines a **5-tier availability scoring model for ESXi hosts** in VMware vSphere, mapping operational states to percentage values: **Fully Functioning = 100%**, **Not on maintenance but on quarantine = 75%**, **Connected to vCenter but on maintenance mode = 50%**, **Powered-on but not connected to vCenter = 25%**, and **Powered Off = 0%**. The tiers are color-coded (green for 100%, yellow for 75%/50%, red for 25%/0%), visually represented as stacked horizontal bands on a 0–100% scale. This model demonstrates that ESXi host availability is a **graduated metric rather than binary**, enabling nuanced health tracking across large host farms in VCF Operations super metrics.]

Implementation using VCF Operations super metric:

[Image: ## Image Description

This image shows a **VCF Operations super metric formula** that calculates ESXi host availability as a score out of 100 (multiplied by 25). The formula uses a `sum` of four binary conditions: whether the host is powered on (`sys|poweredOn`), connected (`runtime|connectionState` contains 'connected'), not in maintenance mode (`runtime|maintenanceState` contains 'notInMaintenance'), and not in quarantine (`runtime|quarantineState` contains 'notInQuarantine'). Each condition contributes 25 points, producing a **graduated availability score (0, 25, 50, 75, or 100)** rather than a simple binary up/down metric.]

What are the limitations of the above?
Yes, it does not recognise the sub-degradation in a fully functioning ESXi. VMs running on an ESXi are unlikely to experience any performance degradation as the hardware has redundancy on network card, storage HBA, local disks, fan, and power supply. ESXi can also lose the iLO network as it’s a separate network.

## esxtop

Now that we have covered many of the metrics, the esxtop output would be easier to understand. This documentation is not about how to use esxtop, but about what the metrics mean and their relevance in operations management.

### Overview

While the manual uses the term Guest, esxtop does not actually have any Guest OS metrics. Distinguish between Guest OS and VM as they are 2 different realms.
The view from a VM (consumer) and the view from ESXi (provider) are of opposite nature. vCPU is a construct of a VM, while core and thread are constructs seen by ESXi. I hope future version of esxtop segregates this better. You get to see both VM level and ESXi level objects at the same time. It is confusing for newbie, but convenient for power user, and if you’re looking at esxtop, you are a power user 😊
The nature of esxtop means it is excellent for performance troubleshooting, especially real time and live situation where you know the specific ESXi Host. The tool is not so suitable for capacity management, where you need to look at long term (often weeks or months). As a result, I cover the contention metrics first, followed by consumption.
I have not had the need to use some of the metrics, hence I don’t have much guidance on them. If you do, let’s collaborate.

#### Grouping

The esxtop screen groups the metrics into 10 screen panels, as shown below:

[Image: The image shows the **esxtop command-line tool's display switch menu**, listing the 10 available screen panels accessible via single-key shortcuts: **c:cpu, d:disk adapter, r:rdma device, x:vsan, i:interrupt, u:disk device, m:memory, v:disk VM, n:network, and p:power mgmt**. This screenshot directly illustrates the "10 screen panels" referenced in the surrounding text, which subsequently explains that these panels will be reorganized into 4 logical groups for better understanding. The prompt "Hit any key to continue" indicates this is a transitional/help screen within the esxtop interface.]

There are relationships among some of the 10 panels, but they are not obvious as the UI simply presents them as a list. To facilitate understanding of the metrics, we need to group them differently.
So instead of documenting the 10 panels, I’d group the panels into 4.

| Group | Consumer | Provider | Remarks |
| --- | --- | --- | --- |
| CPU | Yes | Sort of | The CPU panel has a 4 line summary that provides the provider’s viewpoint.  I moved Power Management panel here as it only covers CPU. It does not cover memory, disk, network and other parts of the box (e.g. fan, motherboard). It complements the CPU panel as it covers the provider’s viewpoint. Take note that it does not show at socket level. And if you enable HT, it does not show at core level. I moved interrupt panel here as it’s about CPU. |
| Memory | 1 shared panel for both | 1 shared panel for both | Provider and Consumer are shown in 1 panel. The panel has a summary at the top, which cover the provider’s viewpoint |
| Storage | Yes | Almost | The Disk VM panel covers from consumer’s viewpoint. The Disk Adapter panel and Disk Device panel cover from provider’s viewpoint, and are best to be analyzed together.  BTW, notice the Path panel is missing. I moved vSAN panel here as all the metrics are disk metrics. There is no vSAN network and CPU counter, but you can see them in the respective network and CPU panel. |
| Network | 1 shared panel for both | 1 shared panel for both | Provider and Consumer are shown in 1 panel I moved RDMA device here as it’s about network card |


#### Export


[Image: ## Image Description

The screenshot shows an Excel spreadsheet (Book1) with **16,384 rows of VMware vSphere metrics**, displaying the last visible rows (16373–16384). Column A contains the metric source identifier **"Vcpu(1:system:2098091:vmknvmeGeneralHelper)"** repeated for each row, while Column B lists specific vCPU performance counters including **% VmWait, % Ready, % Idle, % Overlap, % CoStop, % Max Limited, % Swap Wait, Switches/sec, Migrates/sec, Quantum Expires/sec, Wakeups/sec, and Alloc Min**.

This image directly supports the surrounding text's warning about CSV exports, visually demonstrating that a full vSphere metrics collection yields **over 16,000 individual metrics** — confirming the stated ">10K metrics" threshold that makes CSV exports impractical due to file size exceeding 100 MB.]

Avoid exporting to CSV file. If you need to do it, limit to specific metrics and keep the time short. If you collect everything, you end up with a large file (easily > 100 MB) with >10K metrics. The following shows 16384 metrics being collected.

### CPU

The CPU panel consists of 2 parts:
- Summary
- Detail. It shows a table.
Here is the summary section. It has 4 lines.

[Image: This is a VMware ESXi host CPU summary display showing system uptime (20 days), 892 worlds, 2 VMs, and 6 vCPUs, with CPU load averages of 0.03, 0.03, and 0.02 over 1/5/15 minutes. The output displays per-PCPU metrics across three rows: **PCPU USED(%)** averaging 0.7, **PCPU UTIL(%)** averaging 1.1, and **CORE UTIL(%)** averaging 2.5 (NUMA averages shown on the right). The image demonstrates the four-line CPU summary format described in the text, with notably low utilization values across all 20 PCPUs, illustrating the distinction between the Used, Utilization, and Core Utilization counters referenced in the surrounding content.]

The first line shows the summary of the physical load average in the last 1 minute, 5 minute and 15 minutes, respectively.
The next 3 lines covers Used (%), Utilization (%) and Core Utilization (%). The reason why I swapped the order in the book is Used (%) is built upon Utilization, and it’s a more complex counter. You can see in the following screenshot that Used (%) hit 131% while Util (%) maxed at 100%.
Note that their values are in percentage, meaning you need to know what they use for 100%.

[Image: The screenshot shows **esxtop output** from an ESXi host running 2 VMs with 8 vCPUs, highlighting the distinction between **PCPU USED(%)** and **PCPU UTIL(%)** across individual physical CPU threads. The red boxes highlight specific PCPUs where **USED% reaches 131%** while **UTIL% caps at 100%**, demonstrating that Used can exceed 100% due to CPU ready/co-stop accounting, whereas Utilization is bounded by physical execution capacity. The VM table below confirms the load source: **Test-ESX-test-v** VMs show **%USED of 545% and 534%** with **%RUN at 400%**, indicating significant CPU contention and scheduling overhead (**%WAIT ~800%**).]

If you guess that Used (%) and Utilization (%) eventually map into vSphere Client metrics Usage (%) and Utilization (%), respectively, you are right. However, you need to know how they map.
PCPU means a physical, hardware execution context. That means it is a physical core if CPU SMT is disabled, or a physical thread inside a core if SMT is enabled. It does not mean CPU socket. A single socket with 10 cores and 20 threads will have 20 PCPU metrics.
The white vertical line shows where I cut the screenshot, as the text became too small and unreadable if I were to include all of them. Anyway, it’s just repeating for each CPU physical thread.
At the end of each 3 lines (after the white line in preceding screenshot), there are NUMA information. It shows the average value across each NUMA node (hence there are 2 numbers as my ESXi has 2 NUMA nodes). The number after AVG is the whole box, system wide average. The per NUMA node metric values are useful to easily identify if a particular NUMA node is overloaded.
The detail section takes a consumer view. It is different to the physical view above.
Take a look at the panel below. Notice something interesting?

[Image: This is an **esxtop CPU panel** showing process-level metrics including ID, GID, LWID, NAME, NWLD (number of worlds), %USED, %RUN, %SYS, %WAIT, %VMWAIT, and %RDY columns. The table mixes VM processes (e.g., `blr01m01win01`, `vsanmgmtd`) with non-VM system processes (e.g., `system`, `hostd`, `vpxa`), where the `system` process (ID=1) shows notably high %WAIT (54513.72) and %RDY (42.93, highlighted in red), indicating CPU ready pressure. Non-VM processes lack a %VMWAIT value (shown as "–"), demonstrating the distinction between VM and non-VM world scheduling metrics within esxtop's consumer view.]

It mixes VM and non VM processes in a single table. The non-VM also has Ready time. What it does not have is VM Wait, which is expected.
If you want to only show VMs, just type the capital letter V.
- Name based filtering allows regular expression based filtering for groups and worlds.
- Type the capital letter G to only show groups that match given string. This is useful when a host has large number of VMs and you want to focus on a single or set of interesting VMs.
- Once a group is expanded you can type the small letter g to show only the worlds that match the given string. This is useful when running a VM with many vCPUs and you want to focus on specific worlds like storage worlds or network worlds.
If you want to see all, how to tell which ones are VM? I use %VMWAIT column. This tracks the various waits that VM world gets, so it does not apply to non VM.
Notice the red dot in the picture. Why the Ready time is so high for system process?
Because this group includes the idle thread. Expand the GID and you will see Idle listed.
There are many columns, as shown below. The most useful one is the %State Times, which you get by pressing F.

[Image: This image shows the **esxtop field selection menu** for CPU metrics, listing options A through K that can be toggled on/off by pressing the corresponding letter key. The currently active field is **F: %STATE TIMES = CPU State Times** (indicated by the asterisk `*`), which the surrounding text identifies as the most useful column for VM performance analysis. The menu demonstrates the breadth of available CPU metrics in esxtop, including Group ID, Leader World ID, CPU Allocations, Summary Stats, Power Stats, and Physical CPU Summary.]

The rest of the information are relatively static or do not require sub-20 second granularity.
You know that only Utilization (%) and Used (%) exist at the thread level because they are the only one you see at, as shown below.

#### CPU State

We covered earlier in the CPU Metric that there are only 4 states. But esxtop shows a lot more metrics.

[Image: ## Image Description

This is an **esxtop screenshot** displaying VM-level CPU metrics, showing columns including **%USED, %RUN, %SYS, %WAIT, %VMWAIT, %RDY, %IDLE, %OVRLP, %CSTP, %MLMTD, and %SWPWT** for several VMs/processes. Notable values include the **system** process showing an extreme **%WAIT of 53,618.23%** and **%RUN of 4,722.03%**, while **VMware vCenter** shows **%WAIT of 2,655.50%**, and **blr1m01win01** shows **%VMWAIT of 12.90%**. This image demonstrates the multiple CPU state columns available in esxtop's **%State Times view (accessed via F key)**, which is the context for the surrounding text's discussion about how these states relate to — and overlap with — the four fundamental CPU states, particularly highlighting **%USED** as a metric that doesn't purely represent a CPU state due to its influence by power management and hyperthreading.]

So what does it mean? How come there are more than 4 states?
The answer is below. Some of these metrics are included in the other metrics.

[Image: ## Image Description

The image displays a **vCPU state taxonomy diagram** showing the mutually exclusive CPU states that sum to exactly 100% of a vCPU's time. The top row shows the four primary states: **Ready** (red), **Run** (green), **Costop** (yellow/amber), and **Wait** (gray), while the bottom row shows sub-components: **Max Limited** and **Overlap** (both red, nested within Ready/Run), and **Swap Wait** and **VM Wait** (red) plus **Idle** (gray), nested within Wait.

This diagram contextualizes why esxtop shows more metrics than the four base CPU states — the additional metrics (**Max Limited**, **Overlap**, **Swap Wait**, **VM Wait**, **Idle**) are **sub-components included within the parent states**, not independent states, explaining the apparent discrepancy between the four-state model and esxtop's extended metric list.]

Review the metrics below, starting with %USED.
Which one does not actually belong to a CPU state, meaning it’s not something you mix with the rest?

[Image: This is an **esxtop screenshot** displaying CPU metrics for various VMware processes/groups, including VMware vCenter (GID 59801), system (GID 1), hostd, vpxa, and others. Key columns shown include **%USED, %RUN, %SYS, %WAIT, %VMWAIT, %RDY, %IDLE, %OVRLP, %CSTP, %MLMTD, and %SWPWT**. The image contextually illustrates that **%USED** stands apart from true CPU state metrics (like %RUN, %WAIT, %RDY, %IDLE), as evidenced by VMware vCenter showing an anomalous **%WAIT of 2666.43** and **%IDLE of 378.74**, values exceeding 100% that highlight why %USED is distorted by hyperthreading and power management.]

That’s right, it’s %USED.

| %USED | It should be excluded from this panel as it is influenced by power management and hyperthreading. We explained the reason why in CPU Metric chapter. That’s why it’s necessary to review the VM CPU states before reading each esxtop metric. |
| --- | --- |
| %RUN | Run is covered in-depth under VM CPU Metrics. |
| %SYS | System time is covered in-depth under VM CPU Metrics. |
| %WAIT | The wait counter and its components are covered in-depth under VM CPU Metrics. VMWAIT includes SWPWT. VCF Operations does not show VM Wait and uses a new counter that excludes Swap Wait. The reason is the remediation action is different. You’re welcome. |
| %VMWAIT | The wait counter and its components are covered in-depth under VM CPU Metrics. VMWAIT includes SWPWT. VCF Operations does not show VM Wait and uses a new counter that excludes Swap Wait. The reason is the remediation action is different. You’re welcome. |
| %SWPWT | The wait counter and its components are covered in-depth under VM CPU Metrics. VMWAIT includes SWPWT. VCF Operations does not show VM Wait and uses a new counter that excludes Swap Wait. The reason is the remediation action is different. You’re welcome. |
| %IDLE | The wait counter and its components are covered in-depth under VM CPU Metrics. VMWAIT includes SWPWT. VCF Operations does not show VM Wait and uses a new counter that excludes Swap Wait. The reason is the remediation action is different. You’re welcome. |
| %RDY | Ready is covered in-depth under VM CPU Metrics. As discussed in the CPU scheduling, each vCPU has its own ready time. In the case of esxtop, the metric is simply summed up, so it can go >100% in theory. |
| %CSTP | Co-Stop is covered in-depth under VM CPU Metrics. This is also 100% per vCPU. |
| %OVRLP | Overlap is covered in-depth under VM CPU Metrics. |
| %MLMTD | MLMTD is Max Limited, not some Multi-Level Marketing scam 😊. It measures the time the VM was halted due to manual limit, as opposed to the kernel has no CPU resource. This is more of an event as you should not be setting limit in the first place. |


#### CPU Event Count


[Image: ## Image Description

This is a terminal/CLI output displaying **CPU event count metrics** for several VMware vSphere worlds/processes, showing four metrics: **SWTCH/s** (world switches per second), **MIG/s** (NUMA/core migrations per second), **QEXP/s** (queue expansions per second), and **WAKE/s** (world wake-ups per second). The **system** world dominates with the highest values across all metrics (139.62 SWTCH/s, 8.20 MIG/s, 3950.31 WAKE/s), followed by **VMware vCenter** (69.05 SWTCH/s, 1670.27 WAKE/s) and **vRealize-Operat** (23.46 SWTCH/s, 807.00 WAKE/s). Notably, **QEXP/s is 0.00 for all worlds**, and **vmotion shows near-zero activity**, suggesting no active vMotion operations at the time of capture.]


| SWTCH/s | Number of world switches per second, the lower the better. I guess this number correlates with the overcommit ratio, the number of VM and how busy they are.  What number will be a good threshold and why? |
| --- | --- |
| MIG/s | Number of NUMA and core migrations per second.  It will be interesting to compare 2 VM, where 1 is the size of a single socket, and the other is just a bit larger. Would the larger one experience a lot more switches? |
| WAKE/s | Number of time the world wakeups per second. A world wakes up when its state is changes from WAIT to READY. A high number can impact performance. |

The metric QEXP/s (Quantum Expirations per second) has been deprecated from ESXi 6.5 in an effort to improve vCPU switch time.
In rare case where the application has a lot of micro bursts, CPU Ready can be relatively higher to its CPU Run. This is due to the CPU scheduling cost. While each scheduling is negligible, having too many of them may register on the counter. If you suspect that, check esxtop, as shown below:

[Image: The image shows an **esxtop screenshot** displaying CPU scheduling metrics for two VMs (`someVMblafoobar` and `someVMblabarfoo`), with the **WAKE/s (Wakeups per second)** column highlighted in pink. The two VMs show dramatically different WAKE/s values — **3,309.71** and **6,309.71** respectively — while both share identical SWTCH/s (9.78), MIG/s (0.00), and QEXP/s (0.00) values across 27 worlds each. The red arrow emphasizes the WAKE/s column, illustrating the context of high wakeup rates that can contribute to elevated CPU Ready in micro-burst workload scenarios described in the surrounding text.]


#### Summary Stats


[Image: ## Image Description

This is an **esxtop screenshot** displaying CPU scheduling metrics for several VMware worlds/processes, including `system`, `drivers`, `ft`, `hostd-probe.210`, `VMware vCenter`, and `vRealize-Operat`. The key columns shown are `%LAT_C`, `%LAT_M`, `%DMD`, `EMIN`, `TIMER/s`, `AFFINITY_BIT_MASK`, `CPU`, and `EXC_AF`. Notable values include **VMware vCenter** showing `%DMD` of 29, `EMIN` of 29046, and `TIMER/s` of 817.00, while **vRealize-Operat** shows `%DMD` of 49, `EMIN` of 11597, and `TIMER/s` of 957.00, demonstrating the scheduling metrics referenced in the surrounding text for diagnosing micro-burst CPU scheduling behavior.]

Other than the first 3 (which I’m unsure why they are duplicated here as they are shown in the CPU State already), the other metrics do not exist in vSphere Client UI and VCF Operations.

| %LAT_C | This is covered in-depth in CPU Contention |
| --- | --- |
| %LAT_M | This is covered in-depth in Memory contention |
| %DMD | This is covered in-depth in CPU Demand |
| EMIN | This is the minimum amount of CPU in MHz that the world will get when there is not enough for everyone. |
| TIMER/s | Timer rate for this world |
| AFFINITY BIT MASK | Bit mask showing the current scheduling affinity for the world. Not set for Latency Sensitive = High VMs |
| CPU | The physical or logical processor on which the world was running when esxtop obtained this information. BTW, I’m not 100% sure as this is always blank for me |
| EXC_AF | Yes means the VM has exclusive affinity. This happens when you enabled the Latency Sensitivity setting. Use this feature very carefully. |

The column HTQ is no longer shown in ESXi 7.0. In earlier release, this indicates whether the world is quarantined or not. ‘N’ means no and ‘Y’ means yes.

#### CPU Allocation


[Image: ## CPU Allocation Metrics (esxtop)

The image displays the **CPU Allocation panel in esxtop**, showing allocation metrics for system resources, kernel modules (system, drivers), and VMs (VMware vCenter, vRealize-Operat, blr01m01win01, sh.2098629). Key observations include: **AMAX is -1 for all entries** (meaning no CPU limit is set), **ASHRS shows -3 for the VMs** (indicating default/relative shares), and **AUNITS differentiates between MHz (VMs) and pct/percentage (kernel modules)**. The `sh.2098629` entry notably has **AMLMT of 0** rather than -1, suggesting a max limit condition may be applied to that resource pool/world.]


| AMIN | Allocation Minimum. Basically, the reservation |
| --- | --- |
| AMAX | Allocation Maximum. Basically, the limit. |
| ASHRS | Allocation shares |
| AMLMT | Max Limited. I’m unsure if this is when it’s applied or not. |
| AUNITS | Units. For VM, this is in MHz. For the kernel module, this is in percentage. |


#### Power Stats

This complements the power management panel as it lists per VM and kernel module, while the power panel lists per ESXi physical treads (logical CPU).

[Image: ## Image Description

This screenshot displays a **per-process/VM CPU power consumption table** from ESXtop, showing columns for **ID**, **NAME**, and **POWER** (in Watts). Notable entries include **VMware vCenter** (ID 59801) and **esxtop.2328582** (ID 1334633) each consuming **9W**, **vRealize-Operat** (ID 64652) consuming **6W**, while most kernel modules (system, drivers, ft, sh, dcui, getty, hostd-probe) show **0W**. This table demonstrates the per-VM/process granularity of CPU power metrics, complementing the physical thread-level power panel described in the surrounding text.]


| POWER | Current CPU Power consumption in Watts. So it does not include memory, disk, etc. |
| --- | --- |


#### Power Consumption

Power management is given its own panel. This measures the power consumption of each physical thread. If you disable hyper-threading, then it measures at physical core

[Image: This screenshot shows **ESXi `esxtop` CPU power management output**, displaying system-level stats (150W power usage, no power cap, 0.02/0.03/0.03 load average, 2 VMs, 6 vCPUs) followed by a per-physical-thread table with metrics including **%USED, %UTIL, %C0, %C1, %C2, %T0, and %A/MPERF** for CPUs 0–11. CPU 0 shows notably higher utilization (19.1% used, 18.4% util) with a %A/MPERF of 105.3, while most other CPUs are near-idle with ~99-100% in C2 sleep state. This demonstrates the per-physical-thread power state granularity referenced in the surrounding text, illustrating how C-states (C0=active, C1/C2=idle sleep depths) and frequency scaling metrics reveal actual CPU power consumption patterns across threads.]

The Power Usage line tracks the current total power usage (in Watts). Compare this with what the hardware specification. Power Cap shows the limit applied. You only do this hard limit when there is insufficient power supply from the rack.
The PSTATE MHZ line tracks the CPU clock frequency for each state.
Now let’s go into the table. It lists all the physical core (or thread if you enable HT). Note it does not group them by socket.

| %USED | Used (%) metric is covered in-depth in ESXi CPU metric sub-chapter. |
| --- | --- |
| %UTIL | Utilization (%) metric is covered in-depth in ESXi CPU metric sub-chapter. |
| %CState | Percentage of time spent in a C-State, P-State and T-State. Power management is covered in System Architecture sub-chapter. |
| %TState | Percentage of time spent in a C-State, P-State and T-State. Power management is covered in System Architecture sub-chapter. |
| %A/Mperf | Actual / Measured Performance, expressed in percentage. The word measured in this case means the nominal or static value. So a value above 100% means Turbo, while a value below 100% means power saving kicked in. If this number is not what you are expecting, check the power policy settings in BIOS and ESXi. Notice this is not on a vCPU. This means you do not know the boost per VM. This counter is only applicable when the core is on %C0 state. In the preceding example, ignore the values from CPU 1 – CPU 11. |

The following screenshot shows ESXi with 14 P-States, where P0 is represented as 2401 MHz. Each row is a physical thread as HT is enabled.
See PCPU 10 and 11 (they share core 6). What do you notice?

[Image: This screenshot shows ESXi `esxtop` CPU metrics for physical threads (PCPUs), displaying columns including %USED, %UTIL, C-states (%C0, %C1, %C2), P-states (%P0–%P13), and %A/MPERF. PCPUs 10 and 11 (highlighted in red boxes) are the critical data points: both show **63.0%/62.9% Used**, **100% Utilization**, **100% C0 state**, **100% P0 state**, and **%A/MPERF of 130.2/130.1**, indicating the shared core is fully saturated with both HT threads competing while running at ~30% above nominal frequency via Turbo Boost. The remaining PCPUs show typical idle-to-lightly-loaded behavior with low %USED, predominantly C1/C2 sleep states, and lower %A/MPERF values.]

Utilization (%) shows 100% for both. This means both threads run, hence competing.
The core is in Turbo Boost. The %A/MPERF shows frequency increase of 30% above nominal. The core is in C0 state and P0 state. This counter was introduced in ESXi 6.5. It is not available via vSphere Client UI.
Why is Used (%) for PCPU 10 and 11 are showing 63.0% and 62.9%?
Unlike Utilization (%) which adds up to 200%, Used (%) adds up to 100%. So each thread maxes out at 50%. But Used (%) considers frequency scaling. Since there is a turbo boost at 130%, you get 50% x 130% = 65%. Pretty close to the numbers shown there.

#### Interrupt

This panel captures the interrupt vectors. In the following screenshot, I’ve added 2 vertical white lines to show where I cropped the screenshot. It’s showing the value of each CPU thread, so the column became too wide.

[Image: The screenshot displays VMware vSphere interrupt vector metrics from what appears to be **esxtop** or a similar VMware monitoring tool, showing interrupt cookies (0x0 through 0xa) with associated devices including **VMK dmar**, **VMK ACPI Interrupt**, and **VMK hpet**. All COUNT/s, TIME/int, COUNT_0/1, and TIME_0/1/2 values are **0.0** across all interrupt vectors, indicating no active interrupt activity at the time of capture. The system header shows **2 VMs, 6 vCPUs** with a very low CPU load average of **0.03**, consistent with the idle interrupt counters.]


| COUNT/s | Total number of interrupts per second. This value is cumulative of the count for every CPU. |
| --- | --- |
| COUNT_x | Count 0, Count 1, etc. Interrupts per second on CPU x. My guess is CPU 0 is the first thread in the first core in the first socket. |
| TIME/int | Average processing time per interrupt (in microseconds). It will be interesting to profile this for each type of interrupt. |
| TIME_x | Time 0, Time 2, etc.  Average processing time per interrupt on CPU x (in microseconds). |
| DEVICES | Devices that use the interrupt vector. If the interrupt vector is not enabled for the device, its name is enclosed in angle brackets (< and >). |

To see the list of devices, issue the command at ESXi console: sched-stats -t sys-service-stats. You will get something like this:
service      count       time maxElapsed maxService   name
32   98973493    171.267      0.000      0.000   VMK-lsi_msgpt3_0
33   93243036    153.993      0.000      0.000   VMK-lsi_msgpt3_0
34 1783955246   1841.025      0.000      0.000   VMK-igbn-rxq0
36          4      0.000      0.000      0.000   VMK-Event
37  167025903    418.733      0.000      0.000   VMK-xhci0-intr
51  242318260    792.014      0.000      0.000   VMK-0000:19:00.1-TxRx-0
60   21281764     80.125      0.000      0.000   VMK-vmw_ahci_00003b000
244     176227      0.090      0.000      0.000   VMK-timer-ipi
245    1250405      0.163      0.000      0.000   VMK-monitor
246 1868139923    340.709      0.000      0.000   VMK-resched
248  414047027    189.255      0.000      0.000   VMK-tlb
4096 3193917027   1321.416      0.000      0.000   0_2nd-level-intr-handler
4097  304258696    193.711      0.000      0.000   1_smpcall
4099        246      0.003      0.000      0.000   3_VOB-Wakeup
4100   35706272      6.186      0.000      0.000   4_TimerBH
4101  399313616  10339.744      0.000      0.000   5_fastSlab
4104     859208      7.851      0.000      0.000   8_logEvent
4105  109560008    158.914      0.000      0.000   9_netTxComp
4106         26      0.197      0.196      0.196   10_keyboard
4107         56      0.001      0.000      0.000   11_SMIEnableCountPCPU-bh
4165  365305096   2433.530      0.001      0.001   TCPIPRX
4167   54024607     55.359      0.000      0.000   SCSI
4171   54520415    124.983      0.000      0.000   START-PATH-CMDS
4173   55109136    254.927      0.000      0.000   COMPL.-ADAPTER-CMD
4174   55102189     85.804      0.000      0.000   START-ADAPTER-CMDS
4180 5254928064  13877.461      0.001      0.001   Netpoll
BTW, some services maybe combined and reported under VMK-timer. For example, IOChain from vSphere Distributed Switch does not appear on its own.

### Memory

The top part of the screen provides summary at ESXi level. They are handy in seeing overall picture, before diving into each VM or the kernel modules.

[Image: This image shows the **ESXi `esxtop` memory statistics header**, displaying system-level memory metrics for a host that has been running for 20 days with 892 worlds, 2 VMs, and 6 vCPUs. Key values include **130,692 MB total physical memory** with 100,223 MB free, **MEM overcommit avg of 0.00** across all three intervals (1/5/15 min), and NUMA distribution of 65,155 MB / 65,536 MB across two nodes. All memory pressure indicators (SWAP, ZIP, MEMCTL) are at **0**, indicating no memory reclamation activity, while VMKMEM shows 121,735 MB unreserved with a **"high state"** designation — demonstrating a healthy, non-overcommitted memory environment used as context for explaining the overcommit avg metric described in the surrounding text.]


| MEM overcommit avg | Average memory overcommit level in the last 1-minute, 5-minute, and 15-minute, respectively. Calculation is done with Exponentially Weighted Moving Average.  Memory overcommit is the ratio of total requested memory and the "managed memory" minus 1. According to this, the kernel computes the total requested memory as a sum of the following components:  VM configured memory (or memory limit setting if set),  the user world memory,  the reserved overhead memory.  If the ratio is > 1, it means that total requested VM memory is more than the physical memory available. This is fine, because ballooning and page sharing allows memory overcommit. I’m puzzled why we mix allocation and utilization. No 1 and no 3 make sense, but what exactly is no 2? My recommendation is you simply take the configured VM memory and ignore everything else. While it’s less accurate, since the purpose is capacity and not performance, it’s more than good enough and it’s easier to explain to management. There is no need to get other details. |
| --- | --- |
| PMEM | Physical Memory.  Total = vmk + Other + Free Total is what is reported by BIOS.  vmk is ESXi the kernel consumption. This includes kernel code section, kernel data and heap, and other the kernel management memory. Other is memory consumed by VM and non VM (user-level process that runs directly on the kernel) |
| VMKMEM | The kernel memory. The following metrics are shown: Managed. The memory space that ESXi manage. Typically this is slightly smaller than the total physical memory, as it does not contain all the components of vmk metric. It can be allocated to VM, non VM user world, or the kernel itself.  Minfree. The minimum amount of machine memory that the kernel would like to keep free. The kernel needs to keep some amount of free memory for critical uses. Note that minfree is included in Free memory, but the value tends to be negligible. Reserved. The sum of the reservation setting of the groups + the overhead reservation of the groups + minfree. I think by group it means the world or resource pool. Unreserved. It is the memory available for reservation. I have not found a practical use case for the above 4 metrics. If you do, let me know! State is the memory state. You want this to be on high state. |
| NUMA | In the preceding screenshot, there are 2 NUMA nodes.  For each node there are 2 metrics: the total amount and the free amount. Note that the sum of all NUMA nodes will again be slightly smaller than total, for the same reason why the kernel managed is less than total. If you enable Cluster-on-Die feature in Intel Xeon, you will see 2x the number of nodes. For details, see this by Frank Denneman. |
| PSHARE | shared: the amount of VM physical memory that is being shared. common: the amount of machine memory that is common across Worlds. saving: the amount of machine memory that is saved due to page-sharing. |
| SWAP | Swapped counter is covered under VM memory. What “cannot” be zipped is swapped. What you see on this line is sum of all the VMs. The metric rclmtgt shows the target size in MB that ESXi aims to swap. |
| ZIP | Zipped counter is covered under VM memory. What you see on this line is sum of all the VMs. |
| MEMCTL | Memory Control, also known as ballooning, is covered here under VM memory. What you see on this line is sum of all the VMs. |

There are a lot of metrics in many panels. It’s easier to understand if we group them functionally.

#### Contention

As usual, we start with the contention-type of metrics.

##### Balloon

I start with Balloon as this is the first level of warning. Technically, this is not a contention. Operationally, you want to start watching as Balloon only happens at 99% utilization. So it’s high considering you have HA enabled in the cluster.

[Image: ## Image Description

This screenshot displays a **balloon memory metrics table** (likely from `esxtop` or similar VMware diagnostic tool) showing five processes/VMs with columns **MCTL?**, **MCTLSZ**, **MCTLTGT**, and **MCTLMAX**. Two entries — **VMware vCenter** and **vRealize-Operat** — are flagged as VMs (MCTL? = Y) with MCTLMAX values of **12384.16 MB** and **5184.59 MB** respectively, while all MCTLSZ and MCTLTGT values are **0.00** across all entries. This demonstrates a healthy baseline state where no active ballooning is occurring (MCTLSZ = 0), though the non-zero MCTLMAX values indicate these VMs have balloon driver capacity configured.]


| MCTL? | ‘Y’ means the line is a VM, as the kernel processes is not subjected to ballooning. |
| --- | --- |
| MCTLSZ (MB) | Memory Control Size is the present size of memory control (balloon driver). If larger than 0 hosts is forcing VMs to inflate balloon driver to reclaim memory as host is overcommitted |
| MCTLTGT (MB) | Amount of physical memory the ESXi system attempts to reclaim from the resource pool or VM by way of ballooning. If this is not 0 that means the VM can experience ballooning. |
| MCTLMAX (MB) | Maximum amount of physical memory the ESXi system can reclaim from the resource pool or VM by way of ballooning. This maximum depends on the type of Guest OS. |


##### Compressed & Swapped

I think that Swap and Compressed should be shown together as what can’t be compressed is swapped.
Why am I showing Compressed first?
Because it’s faster than swapped.

[Image: The image displays a terminal/CLI output showing memory compression metrics for several VMware processes and VMs: **hostd.2099383**, **vsanmgmtd.22914**, **VMware vCenter**, **blr01m01win01**, and **vRealize-Operat**. All four metrics — **CACHESZ**, **CACHEUSD**, **ZIP/s**, and **UNZIP/s** — show values of **0.00** across all listed processes/VMs. This demonstrates an ideal, healthy state where no memory compression activity is occurring, consistent with the surrounding text's guidance that ZIP/s should be kept at 0 to avoid memory contention.]


| CACHESZ (MB) | Compression memory cache size. |
| --- | --- |
| CACHEUSD (MB) | Used compression memory cache |
| ZIP/s (MB/s) | The rate at which memory pages are being zipped. Once zipped, it’s not immediately available for the VM. This is a capacity problem. Your ESXi needs more RAM. If the pages being zipped is unused, the VMs will not experience memory contention. Keep this number 0. See Capacity chapter for details. |
| UNZIP/s (MB/s) | The rate at which memory pages are being unzipped so it can be used by VM. This is a performance problem. The pages are being asked. The VM CPU is waiting for the data. If you check the VM memory contention counter, it will not be 0%. Make sure that number is within your SLA or KPI. |


##### Swapped


[Image: This screenshot displays a VMware ESXi **swap memory metrics table** showing six processes (dcui.2100802, getty.2100827, hostd-probe.210, VMware vCenter, ioFilterVPServe, and sh.2098515) with six columns: **SWCUR, SWTGT, SWR/s, SWW/s, LLSWR/s, and LLSWW/s**. All values across every process and metric are **0.00**, indicating no active swapping activity on this ESXi host. This represents an **ideal/healthy state**, as zero swap activity means no memory contention-driven disk swapping is occurring for any of these processes.]


| SWCUR (MB) | Swapped Current is the present size of memory on swapped. It typically contains inactive pages. |
| --- | --- |
| SWTGT (MB) | The target size the ESXi host expects the swap usage by the resource pool or VM to be. This is an estimate. |
| SWR/s (MB) | Swapped Read per second and Swapped Write per second. The amount of memory in megabyte that is being brought back to memory or being moved to disk |
| SWW/s (MB) | Swapped Read per second and Swapped Write per second. The amount of memory in megabyte that is being brought back to memory or being moved to disk |
| LLSWR/s (MB) | These are similar to SWR/s but is about host cache instead of disk. It is the rate at which memory is read from the host cache. The reads and writes are attributed to the VMM group only, so they are not displayed for VM.  LL stands for Low Latency as host cache is meant to be faster (lower latency) than physical disk.  Memory to host cache can be written from both the physical DIMM and disk. So the counter LLSWW/s covers all these sources, and not just from physical DIMM. |
| LLSWW/s (MB) | These are similar to SWR/s but is about host cache instead of disk. It is the rate at which memory is read from the host cache. The reads and writes are attributed to the VMM group only, so they are not displayed for VM.  LL stands for Low Latency as host cache is meant to be faster (lower latency) than physical disk.  Memory to host cache can be written from both the physical DIMM and disk. So the counter LLSWW/s covers all these sources, and not just from physical DIMM. |


##### NUMA

Logically, this statistic is applicable only on NUMA systems.

[Image: This image shows an **esxtop NUMA statistics table** displaying memory metrics for several VMware vSphere workloads/processes. Key visible processes include **VMware vCenter** (27 worlds, NHN=1, NMIG=16, NRMEM=0.00, NLMEM=19456.00, N%L=100, GST_ND0=0.00, OVD_ND0=19.87) and **vRealize-Operat** (13 worlds, NHN=0, NMIG=16, NRMEM=0.00, NLMEM=8192.00, N%L=100, NLMEM=8192.00, OVD_ND0=24.12, OVD_ND1=8.75), while other processes (dcui, getty, hostd-probe, rhttpproxy) show dashes indicating no NUMA home node assignment. The table illustrates NUMA home node assignments, migration counts, and memory locality metrics (N%L=100 indicating 100% local memory access for active VMs), contextualizing the surrounding text's discussion of NHN and NMIG counters.]


| NHN | The count of NUMA Home Node for the resource pool or VM. If the VM has no home node, a dash (-) appears. You want to see the number 1VM. If you see the number 2, that means the VM is split into multiple nodes, which could impact performance. When you enable CPU Hot Add, esxtop will report multiple home nodes as NUMA is disabled. It also does not distinguish remote and local memory as memory is interleaved. For more information, see this by Frank. |
| --- | --- |
| NMIG | Number of NUMA migrations. It gets reset upon VM power cycle, meaning this counter is accumulative. Be careful as you could be looking at past data. Use Log Insight to plot the event over time.  Migration is costly as all pages need to be remapped. Local memory starts at 0% again and grow overtime. Copying memory pages across NUMA boundaries cost memory bandwidth. |
| NRMEM (MB) | Current amount of remote memory allocated to the VM or resource pool. Ideally this amount is 0 or a tiny percentage. You decrease the chance by decreasing the VM configured RAM. A VM whose configured memory is larger than the ESXi RAM attached to a single CPU socket have higher chance of having remote memory. |
| N%L | Current percentage of memory allocated to the VM or resource pool that is local.  Anything less than 100% is not ideal. |
| GST_NDx (MB) | Guest memory allocated for a resource pool on NUMA node x, where GST_ND0 means the first node. The following screenshot shows the VMware vCenter VM runs on node 2 while the vRealize-Operat VM runs on node 1. |
| OVD_NDx (MB) | VMM overhead memory allocated for a resource pool on NUMA node x, where x starts with 0 for the first node. |


#### Consumption

I group metrics such as consumed, granted, and overhead under consumption as they measure how much the VM or the kernel module consumes.

##### Consumed


[Image: ## Image Description

This is a terminal/CLI output displaying VMware ESXi memory metrics for six VMs/processes: **VMware vCenter**, **vRealize-Operat**, **blr01m01win01**, **hostd.2099383**, **vsanmgmtd.22914**, and **vpxa.2099926**. The columns shown are **MEMSZ**, **GRANT**, **CNSM** (Consumed), **SZTGT**, **TCHD**, and **TCHD W**, all in MB. The data illustrates the relationship between key consumption metrics, notably that **VMware vCenter** has the largest footprint (MEMSZ: 19606.73 MB, CNSM: 19456.00 MB), while smaller processes like **vpxa** consume significantly less (MEMSZ: 42.83 MB, CNSM: 33.90 MB), demonstrating how MEMSZ, GRANT, and CNSM values correlate across workloads of varying sizes.]


| MEMSZ (MB) | Amount of physical memory allocated to a resource pool or VM. The values are the same for the VMM and VMX groups.  MEMSZ = GRANT + MCTLSZ + SWCUR + "never touched"  I’m unsure where the compressed page goes. It’s still occupying space but 50% or 25%. |
| --- | --- |
| GRANT (MB) | Do not confuse it with Consumed 😊 |
| CNSM | Yup, this is that legendary Consumed metric. |
| SZTGT (MB) | Size Target in MB. Amount of machine memory the ESXi kernel wants to allocate to a resource pool or VM. The values are the same for the VMM and VMX groups. |
| TCHD (MB) | The size of touched pages in MB Working set estimate for the resource pool or VM. The values are the same for the VMM and VMX groups. |
| TCHD_W | As per above, but only for the write operations. A relatively much lower value compared to TCHD means the activities are mostly read. |


##### Overhead

I find overhead is a small amount that is practically negligible, considering ESXi nowadays sports a large amount of RAM. Let me know the use case where you find otherwise.

[Image: The image displays a table of VMware overhead memory metrics (OVHDUW, OVHD, OVHDMAX) for five system components. VMware vCenter shows the highest overhead values (98.14 MB current, 153.53 MB maximum), followed by vRealize-Operations (58.55 MB / 82.69 MB) and blr01m01win01 (41.57 MB / 65.15 MB), while hostd and vsanmgmtd show zero overhead. This illustrates that management VMs/services like vCenter and vRealize incur the most memory overhead, while system processes (hostd, vsanmgmtd) have negligible overhead, supporting the author's claim that overhead is practically negligible in modern ESXi environments.]


| OVHD (MB) | Current space overhead for resource pool. |
| --- | --- |
| OVHDMAX (MB) | Maximum space overhead that might be incurred by resource pool or VM. |
| OVHDUW (MB) | Current space overhead for a user world. It is intended for VMware use only. |


##### Shared


[Image: This image shows a table of VMware memory sharing metrics for several processes/VMs, displaying columns for ID, GID, NAME, ZERO, SHRD, SHRDSVD, and COWH (in MB). Notable data points include **VMware vCenter** with a significant COWH value of **17,503.53 MB** and **vRealize-Operat** with **6,436.82 MB**, indicating substantial Copy-on-Write Hint (TPS candidate) memory, while most other processes show negligible or zero values across all metrics. The table contextually demonstrates the SHRD, SHRDSVD, and COWH memory sharing counters described in the surrounding text, highlighting that vCenter and vRealize Operations are the primary consumers with meaningful sharing-related overhead.]


| ZERO (MB) | Resource pool or VM physical pages that are zeroed. |
| --- | --- |
| SHRD (MB) | Total amount that is shared. |
| SHRDSVD (MB) | Machine pages that are saved because of sharing.  Notice this counter does not exist in vSphere Client UI. |
| COWH (MB) | Copy on Write Hint. An estimate of the amount of Guest OS pages for TPS purpose. |


##### Active

The manual uses the word Guest to refer to VM. I distinguish between VM and Guest. Guest is an OS, while a VM is just a collection of processes. Guest has its own memory management that is completely invisible to the hypervisor.

[Image: The image displays a table of VMware memory activity metrics (%ACTV, %ACTVS, %ACTVF, %ACTVN) for five entities: VMware vCenter, vRealize-Operat, blr01m01win01, hostd.2099383, and vsanmgmtd.22914. VMware vCenter shows consistent values of 4% across %ACTV, %ACTVS, and %ACTVF with 2% for %ACTVN, while vRealize-Operat shows the highest activity with values of 6, 8, 7, and 10 respectively. The remaining three processes (blr01m01win01, hostd, vsanmgmtd) show zero activity across all metrics, demonstrating the contrast between active and idle VM/process memory utilization.]


| %ACTV | Active is covered in-depth in Active metric |
| --- | --- |
| %ACTVS | Percentage Active Slow and Percentage Active Fast. Slow is the slow moving average, taking longer period. Longer is more accurate. I don’t have a use case for the fast moving average. |
| %ACTVF | Percentage Active Slow and Percentage Active Fast. Slow is the slow moving average, taking longer period. Longer is more accurate. I don’t have a use case for the fast moving average. |
| %ACTVN | Percentage Active Next. It predicts of what %ACTVF will be at next sample estimation. It is intended for VMware use only. |


##### Committed

Committed page means the page has been reserved for that process. Commit is a counter for utilization but it’s not really used, especially for VM.
Note: none of these metrics exist in vSphere Client and VCF Operations, as they are meant for internal use.

[Image: ## Image Description

The image displays a table of **VMware memory commitment metrics** for several processes/VMs, including VMware vCenter, vRealize-Operations, blr01m01win01, hostd, vsanmgmtd, and vpxa. The columns show **MCMTTGT** (all 0.00), **CMTTGT** (ranging from 31.73 MB to 19,476.33 MB), **CMTCHRG** (all 0.00), and **CMTPPS** (all -1). The data demonstrates that **CMTTGT is the primary active metric** among the committed memory counters, with VMware vCenter showing the highest commit target at **19,476.33 MB**, while MCMTTGT and CMTCHRG remain at zero across all processes.]


| MCMTTGT | Minimum Commit Target in MB. I think this value is not 0 when there is reservation, but I’m not sure. |
| --- | --- |
| CMTTGT | Commit Target in MB. |
| CMTCHRG | Commit Charged in MB. I think this is the actual committed page. |
| CMTPPS | Commit Pages Per Share in MB |


##### Allocation & Reservation


[Image: ## Image Description

This is an **esxtop memory allocation table** showing 8 VMware kernel processes/modules with their allocation and reservation metrics. The key columns display **NWLD** (workloads), **AMIN** (allocation minimum/reservation), **AMAX** (allocation maximum/limit), **ASHRS**, **AMLMT**, and **AUNITS** (kilobytes).

All processes show **AMIN = 0** (no reservation) and **AMAX = -1** (unlimited), with `vpxa.2099926` having the highest workload count of **38** and `rhttpproxy.2099` showing **21**, demonstrating the allocation and limit settings for internal VMware kernel modules that are not exposed in vSphere Client or VCF Operations.]


| AMIN | Allocation minimum. This is the term esxtop uses for memory reservation for this resource pool or VM. A value of 0 means no reservation, which is what you should set for most VM. Reservation for the kernel modules should be left as it is. |
| --- | --- |
| AMAX | Allocation maximum. This is the term esxtop uses for memory limit for this resource pool or VM. A value of -1 means Unlimited.  Limit for the kernel modules should be left as it is. |
| AMLMT | Limit. You should expect the value -1, means no limit assigned. I’m not sure how this differs to AMAX. |
| ASHRS | Memory shares for this resource pool or VM. |
| AUNITS | This is just displaying the units of allocations counters |


#### Checkpoint

Checkpoint is required in snapshot or VM suspension. You can convert a VM checkpoint into a core dump file, to debug the Guest OS and applications.

| CPTRD (MB) | Checkpoint Read. Amount of data read from checkpoint file. A large amount can impact the VM performance. |
| --- | --- |
| CPTTGT (MB) | Checkpoint Target. The target size of checkpoint file that the kernel is aiming for. I’m unsure why it needs to have a target, unless this is just an estimate of the final size and not a limit. |


### Storage

The Storage monitoring sports 3 panels:
- VM
- Adapter
- Device
We covered in Part 2 that an ESXi host has adapter, path and devices. I’m unsure why esxtop does not have a panel for path. It would be convenient to check dead path or inactive path as the value will be all 0. If your design is active/active, it can be useful to compare if their throughput is not lopsided.
Datastore is also missing. While VMFS can be covered with Device (if you do 1:1 mapping and not using extent), NFS is not covered.
On the other hand, esxtop does provide metrics that vSphere Client does not. I will highlight those.
ESXi uses adapter to connect to device. As a result, their main contention and utilization metrics are largely similar. I’ve put them side by side here, and highlight the similar metric groups with vertical green bar. I highlighted the word group, as the group name may be identical, but the actual metrics within the group differ.

[Image: ## Image Description

The image displays a side-by-side comparison of **esxtop metric groups** for two object types: **Adapter metrics groups** (left) and **Device metrics groups** (right). Both share several identical metric group names — **QSTATS, IOSTATS, RESVSTATS, LATSTATS, ERRSTATS, PAESTATS, and SPLTSTATS** — highlighted with **vertical green bars** to indicate commonality, while Device metrics groups include additional unique entries: **ID, NUM, SHARES, BLKSZ, VAAISTATS, and VAAILATSTATS**. This visual demonstrates that while adapter and device metrics overlap significantly in structure, device-level metrics extend further with VAAI (vStorage APIs for Array Integration) specific statistics not present at the adapter level.]


#### VM

We begin with VM as that’s the most important one. It complements vSphere Client by providing unmap and IO Filter metrics.
You can see at VM level, or virtual disk level. In the following screenshot, I’ve expanded one of the VM. The VM shown as vRealize-Operat has 3 virtual devices.

[Image: This screenshot displays VM-level virtual disk I/O metrics from a VMware monitoring tool, showing columns for **CMDS/s, READS/s, WRITES/s, MBREAD/s, MBWRTN/s, LAT/rd, and LAT/wr** across four VMs (GIDs: 59801, 64652, 1120181). The VM **vRealize-Operat (GID 64652)** is expanded to show three virtual devices (scsi0:0, scsi0:1, scsi0:2), with scsi0:1 showing the highest write activity (0.95 WRITES/s, 0.01 MBWRTN/s, 0.131ms write latency). This demonstrates the tool's ability to display metrics at both the **VM aggregate level and individual virtual disk level**, complementing vSphere Client with granular per-VMDK visibility.]


##### Contention


| LAT/rd | Average latency (in milliseconds) per read. |
| --- | --- |
| LAT/wr | Average latency (in milliseconds) per write. |


##### Consumption


[Image: ## Image Description

This is a **esxtop/vscsiStats output table** displaying disk I/O consumption metrics for three VMs: **VMware vCenter**, **vRealize-Operat**, and **blr01m01win01**. The table shows **CMDS/s, READS/s, WRITES/s, MBREAD/s, and MBWRTN/s** columns, with vRealize-Operat showing the highest activity (**46.16 CMDS/s, 38.34 READS/s, 1.65 MBREAD/s**), while blr01m01win01 shows **zero activity across all metrics**. This image illustrates the **consumption-tier disk metrics** described in the surrounding text, specifically demonstrating how IOPS (READS/s, WRITES/s) and throughput (MBREAD/s, MBWRTN/s) are represented per VM in a live vSphere monitoring context.]


| CMDS/s | Count of disk IO commands issued per second. This is basically IOPS. Both the Read IOPS and Write IOPS are provided. |
| --- | --- |
| READS/s | Count of disk IO commands issued per second. This is basically IOPS. Both the Read IOPS and Write IOPS are provided. |
| WRITES/s | Count of disk IO commands issued per second. This is basically IOPS. Both the Read IOPS and Write IOPS are provided. |
| MBREAD/s | Total disk amount transferred per second in MB. This is basically throughput. Both the read throughput and write throughput are provided. |
| MBWRTN/s | Total disk amount transferred per second in MB. This is basically throughput. Both the read throughput and write throughput are provided. |


##### Unmap

It has unmap statistics. This can be useful that there is no such information at vSphere Client. In the UI, you can only see at ESXi level.

[Image: ## Image Description

The image shows a tabular output displaying **Unmap (UMP) statistics** for three VMs: VMware vCenter (GID 59801, 16 NVDisks), vRealize-Operat (GID 64652, 3 NVDisks), and blr01m01win01 (GID 1120181, 1 NVDisk). The metrics displayed include **SC_UMP/s, FL_UMP/s, UMP/s, SC_UMP_MBS/s, and FL_UMP_MBS/s**, all showing values of **0.00** across all VMs, indicating no unmap activity is currently occurring. This screenshot demonstrates the unmap statistics visibility at the VM level, which the surrounding text notes is not available through the vSphere Client UI and can only be seen at the ESXi level natively.]


| SC_UMP/s | Successful, Failed and Total Unmaps per second.  Unmap can fail for a variety of reason. One example that was addressed in vSphere 6.7 Patch ESXi670-202008001 and documented in in KB is Guest OS does not refresh unmap granularities and keep sending unmap based on older value. Eventually limit is reached and the operation fail. |
| --- | --- |
| FL_UMP/s | Successful, Failed and Total Unmaps per second.  Unmap can fail for a variety of reason. One example that was addressed in vSphere 6.7 Patch ESXi670-202008001 and documented in in KB is Guest OS does not refresh unmap granularities and keep sending unmap based on older value. Eventually limit is reached and the operation fail. |
| UMP/s | Successful, Failed and Total Unmaps per second.  Unmap can fail for a variety of reason. One example that was addressed in vSphere 6.7 Patch ESXi670-202008001 and documented in in KB is Guest OS does not refresh unmap granularities and keep sending unmap based on older value. Eventually limit is reached and the operation fail. |
| SC_UMP_MBS/s | As above, but in MB/second. |
| FL_UMP_MBS/s | As above, but in MB/second. |


##### IO Filter

I/O Filter in ESXi enable the kernel to manipulate the IO sent by Guest OS before processing it. This obviously opens up many use cases, such as replication, caching, Quality of Service, encryption.
There is no such metric at vSphere Client. You will not find IO Filter metrics at both VM object and ESXi object.

[Image: The image shows a command-line output displaying IO Filter metrics for three VMs: **VMware vCenter**, **vRealize-Operat**, and **blr01m01win01**. All three VMs show **NUMIOFILTERS = 0**, **IOFILTERCLASS = "-"**, and **FAILEDIO, TOTALIO, and LATENCY all at 0**, indicating no IO Filters are configured or active on any of these virtual machines. This output demonstrates the esxcli/command-line method of retrieving IO Filter metrics that are otherwise unavailable in the vSphere Client UI.]


| NUMIOFILTERS | Number of IO Filters |
| --- | --- |
| IOFILTERCLASS | Type of IO Filter Class |
| FAILEDIO | I think Failed IO should be 0 at all times. |
| TOTALIO | I think Failed IO should be 0 at all times. |
| LATENCY | I’m unsure if this latency measures the additional overhead introduced by IO Filter, or the total latency as seen by the VM. |


##### Configuration


[Image: ## Image Description

The image displays a tabular output showing **VM disk/VSCSI configuration data** with four columns: **ID, GID, VMNAME, VDEVNAME, and NVDISK**. Three VMs are listed: **VMware vCenter** (ID 59801, 16 virtual disks), **vRealize-Operat** (ID 64652, 3 virtual disks), and **blr01m01win01** (ID 1120181, 1 virtual disk). The VDEVNAME column shows dashes for all entries, indicating no specific VSCSI device filter is applied, and **NVDISK** represents the number of virtual disks per VM — consistent with the surrounding context describing VSCSI device metrics.]


| ID | Resource pool ID or VSCSI ID of VSCSI device. |
| --- | --- |
| GID | Resource pool ID. |
| VMNAME | Name of the resource pool. |
| VSCSINAME | Name of the VSCSI device. |
| NDK | Number of VSCSI devices |


#### Disk Adapter

ESXi uses adapter to connect to device, so let’s begin with adapter, then device.
The panel has a lot of metrics and properties, so let’s group them for ease of understanding.

##### Errors

Since you check availability before performance, let’s check the errors first. This type of problem is best monitored as accumulation within the reporting period as any value other than 0 should be investigated.
BTW, none of these metrics are available at vSphere Client UI.

| FCMDS/s | Number of failed commands issued per second. How does this differ to Reset and Aborted?  Number of failed read commands issued per second. Number of failed write commands issued per second. |
| --- | --- |
| FREAD/s | Number of failed commands issued per second. How does this differ to Reset and Aborted?  Number of failed read commands issued per second. Number of failed write commands issued per second. |
| FWRITE/s | Number of failed commands issued per second. How does this differ to Reset and Aborted?  Number of failed read commands issued per second. Number of failed write commands issued per second. |
| FMBRD/s | Megabytes of failed read operations per second. Megabytes of failed write operations per second. |
| FMBWR/s | Megabytes of failed read operations per second. Megabytes of failed write operations per second. |
| CONS/s | Number of SCSI reservation conflicts per second. This number should stay 0?  Number of failed SCSI reservations per second, if the conflict can’t be solved timely. Number of SCSI reservations per second. This number should stay within the limit, but how to know what the limit is? |
| FRESV/s | Number of SCSI reservation conflicts per second. This number should stay 0?  Number of failed SCSI reservations per second, if the conflict can’t be solved timely. Number of SCSI reservations per second. This number should stay within the limit, but how to know what the limit is? |
| RESV/s | Number of SCSI reservation conflicts per second. This number should stay 0?  Number of failed SCSI reservations per second, if the conflict can’t be solved timely. Number of SCSI reservations per second. This number should stay within the limit, but how to know what the limit is? |
| ABRTS/s | Number of commands cancelled per second. |
| RESETS/s | Count of disk commands reset per second. |


##### Queue

For storage, the queue gives insight into performance problem. It’s an important counter so I was hoping there will be more, such as the actual queue.

| AQLEN | Current queue depth of the storage adapter. This is the maximum number of kernel active commands that the adapter driver is configured to support. This counter is not available in vSphere Client UI |
| --- | --- |


##### Contention

You expect to get 4 sets (Device, Kernel, Guest, Queue). For each set, you expect read, write, and total. 12 metrics, and that’s exactly what you got below.

| DAVG/cmd | Average latency per command in milliseconds. It’s an average number, not the last number in the reporting period. If you have 1000 IOPS, that means 5K IOPS over the 5 second reporting period. It’s a weighted average between read and write. If the IO commands are mostly read, then high latency from write could be masked out. |
| --- | --- |
| KAVG/cmd | Average latency per command in milliseconds. It’s an average number, not the last number in the reporting period. If you have 1000 IOPS, that means 5K IOPS over the 5 second reporting period. It’s a weighted average between read and write. If the IO commands are mostly read, then high latency from write could be masked out. |
| GAVG/cmd | Average latency per command in milliseconds. It’s an average number, not the last number in the reporting period. If you have 1000 IOPS, that means 5K IOPS over the 5 second reporting period. It’s a weighted average between read and write. If the IO commands are mostly read, then high latency from write could be masked out. |
| QAVG/cmd | Average latency per command in milliseconds. It’s an average number, not the last number in the reporting period. If you have 1000 IOPS, that means 5K IOPS over the 5 second reporting period. It’s a weighted average between read and write. If the IO commands are mostly read, then high latency from write could be masked out. |
| DAVG/rd | Average read latency per read operation in milliseconds. The same set of metrics as above, except it only counts the reads.  It’s useful to see read and write separately as the numbers tend to be different. More importantly, the remediation action is different. |
| KAVG/rd | Average read latency per read operation in milliseconds. The same set of metrics as above, except it only counts the reads.  It’s useful to see read and write separately as the numbers tend to be different. More importantly, the remediation action is different. |
| GAVG/rd | Average read latency per read operation in milliseconds. The same set of metrics as above, except it only counts the reads.  It’s useful to see read and write separately as the numbers tend to be different. More importantly, the remediation action is different. |
| QAVG/rd | Average read latency per read operation in milliseconds. The same set of metrics as above, except it only counts the reads.  It’s useful to see read and write separately as the numbers tend to be different. More importantly, the remediation action is different. |
| DAVG/wr | The same set of metrics as above, except it only counts the writes. |
| KAVG/wr | The same set of metrics as above, except it only counts the writes. |
| AVG/wr | The same set of metrics as above, except it only counts the writes. |
| QAVG/wr | The same set of metrics as above, except it only counts the writes. |


##### Consumption

Now that we get the more important metrics (errors, queue, and contention) done, you then check utilization counter. In this way you have better context.

| ACTV | The definition is “Number of commands that are currently active”. I don’t know how it differs to IOPS as I’m unsure what the word “active” exactly mean here. |
| --- | --- |
| CMDS/s | I combine these 3 metrics as they are basically IOPS.  Total IOPS, read IOPS and write IOPS. |
| READS/s | I combine these 3 metrics as they are basically IOPS.  Total IOPS, read IOPS and write IOPS. |
| WRITES/s | I combine these 3 metrics as they are basically IOPS.  Total IOPS, read IOPS and write IOPS. |
| MBREAD/s | I combine them as they measure throughput. Interestingly, there is no total throughput metric, but you can simply sum them up. Read the string MBWRTN as MB Written. |
| MBWRTN/s | I combine them as they measure throughput. Interestingly, there is no total throughput metric, but you can simply sum them up. Read the string MBWRTN as MB Written. |


##### PAE and Split


| PAECMD/s | PAE Command per second and PAE Copy per second. PAE (Physical Address Extension) no longer applicable in 64-bit and modern drivers/firmware/OS, as the size is big enough. Copy operations here refer to the kernel copies the data from high region (beyond what the adapter can reach) to low region. This statistic applies to only paths. |
| --- | --- |
| PAECP/s | PAE Command per second and PAE Copy per second. PAE (Physical Address Extension) no longer applicable in 64-bit and modern drivers/firmware/OS, as the size is big enough. Copy operations here refer to the kernel copies the data from high region (beyond what the adapter can reach) to low region. This statistic applies to only paths. |
| SPLTCMD/s | Split Commands per second.  Disk IO commands with large block size have to be split by the kernel. This can impact the performance as experiences by the Guest OS. |
| SPLTCP/s | Number of split copies per second. A higher number means lower performance |


##### Configuration

The panel provides basic configuration. I use vSphere Client as it provides a lot more information, and I can take action on them. The following is just some of the settings available.

[Image: ## Storage Adapters Configuration Panel

The image shows the **Storage Adapters** configuration panel in vSphere Client, displaying two physical HBA adapters: a **Dell BOSS-S1 Adapter** (vmhba3, Block SCSI type) and a **Dell HBA330 Mini** (vmhba0, SAS type). Both adapters show **Status: Unknown**, with identical metrics of **2 Targets, 2 Devices, and 2 Paths** each. This screenshot illustrates the configuration view referenced in the surrounding text, demonstrating the richer detail available in vSphere Client compared to esxtop, including adapter model, type, and path count information.]

Compare the above with what esxtop provides, which is the following:

[Image: This is an **esxtop output** showing storage adapter (HBA) path information, displaying four adapters: **vmhba0, vmhba1, vmhba2, and vmhba3**. vmhba0 and vmhba3 each show two active paths (C0:T0:L0 and C0:T2:L0), while vmhba1 and vmhba2 show **0 paths (NPTH=0)**, indicating no connected storage paths. The image demonstrates the ADAPTR and PATH columns in esxtop's disk adapter view, contrasting with vSphere Client's configuration panel shown previously, and contextualizes the **NPTH (Number of Paths)** metric discussed in the surrounding text.]


| NPTH | Number of path. This should match your design. An adapter typically has more than 1 path, which is why I said it would be awesome to have a panel for path |
| --- | --- |


#### Disk Device

The device panel has a lot of metrics and properties, so let’s group them for ease of understanding.

##### Errors

I’m always interested in errors first, before I check for contention and utilization.

| ABRTS/s | Number of commands cancelled per second. Expect this to be 0 at all times. |
| --- | --- |
| RESETS/s | Number of commands reset per second. Expect this to be 0 at all times. |


##### Queue

You’ve seen that there is only 1 counter for queue in Disk Adapter. How many do you expect for Disk Device?
Interestingly, there are 6 metrics for queue, as shown below.

[Image: ## Image Description

This screenshot displays **esxtop/vscsiStats output** showing storage device queue metrics for four devices: one NVMe (`eui.`), two NAS/iSCSI (`naa.`), and one local SATA SSD (`t10.ATA____SSDSCKKB240G8R`). The visible columns include **DQLEN** (device queue depth: 31 or 254), **WQLEN**, **ACTV**, **QUED**, **%USD**, and **LOAD** — with all activity counters showing **zero values (0, 0.00)**, indicating no I/O load at the time of capture. This idle baseline demonstrates the queue metrics described in the surrounding text, specifically illustrating how **LOAD, QUED, and %USD** appear under no-contention conditions.]


| LOAD | The formula is (active commands + ESXi kernel queued commands) / queue depth.  If LOAD > 1, check the value of the QUED counter. |
| --- | --- |
| QUED | Number of commands in the kernel that are currently queued. You want this to be as low as possible, well below the queue depth. |
| %USD | USD (%) = ACTV / QLEN For world stats, QLEN is WQLEN. For LUN (aka device) stats, QLEN is DQLEN. Percentage of the queue depth used by ESXi kernel active commands.  So this does not include the queued command? Does it mean that if this number is not 100%, then there is nothing in the queue, as queue should only develop when it’s 100% used?  Obviously when Used = 100% it means the queue is full. That will introduce outstanding IO, which in turn will increase latency |
| DQLEN | I combine this together as a device can have 1 or more world, and there is a per-device maximum. DQLEN is the device configured queue length. The corresponding counter for adapter is called AQLEN WQLEN is the world queue depth. The manual states “This is the maximum number of ESXi kernel active commands that the world is allowed to have”. So it does not look like the queue at present.  So we show maximum value for each world, and the present value for each device. |
| WQLEN | I combine this together as a device can have 1 or more world, and there is a per-device maximum. DQLEN is the device configured queue length. The corresponding counter for adapter is called AQLEN WQLEN is the world queue depth. The manual states “This is the maximum number of ESXi kernel active commands that the world is allowed to have”. So it does not look like the queue at present.  So we show maximum value for each world, and the present value for each device. |
| ACTV | The definition is “Number of commands that are currently active”. I think this means the IO in flight. This is worth profiling and I expect it to be small most of the time. |


##### Contention

See Disk Adapter as both sport the same 12 metrics.

##### Consumption

See Disk Adapter as both sport the same 5 metrics.

##### PAE and Split

See Disk Adapter as both sport the same 4 metrics.

##### Configuration

As you can expect, esxtop provides minimal configuration information. They are shown below.

[Image: This is an **esxtop screenshot** showing disk device metrics for a VMware vSphere host running for 103 days with 933 worlds, 3 VMs, and 8 vCPUs. Four storage devices are listed (`eui.0050430000000000`, `naa.500056b323e140fd`, `naa.5002538b00145ad0`, and `t10.ATA_SSDSCKKB240G8R`) with configuration columns **NPH, NWD, NPN, SHARES, BLKSZ, and NUMBLKS**. Notable values include `naa.5002538b00145ad0` with 7 NWD, 1 NPN, 512 BLKSZ, and 1,875,385K NUMBLKS, and the SSD device with 7 NWD, 5 NPN, 512 BLKSZ, and 468,862K NUMBLKS, illustrating the configuration metrics available per disk device in esxtop.]


###### Path/World/Partition

They are grouped as 1 column, and you can only see one at a time.
By default, none of them is shown. To bring up one of them, type the corresponding code. In the following screenshot, I’ve type the letter e, which them prompted me to enter one of the device.

[Image: The screenshot shows the **esxtop disk device selection interface**, where a user has typed `naa.5002538b00145ad0` in response to the "Device to expand/rollup" prompt. The device list displays four storage devices: `eui.005043000000000`, `naa.500056b323e140fd`, `naa.5002538b00145ad0`, and `t10.ATA____SSDSCKKB240G8R_`, with the **PATH/WORLD/PARTITION** column visible but showing no values (dashes) by default. This demonstrates the process of selecting a specific device to reveal the Path, World, or Partition sub-column in esxtop's disk metrics view.]

Path is obviously the path name, such as vmhba0:C0:T0:L0.
A disk device can have >1 world, which I’m unsure why. You can see each world ID, and you get the statistics per world.

[Image: The image shows the **esxtop storage device view** displaying disk device metrics including NPH (Number of Paths), NWD (Number of Worlds), and NPN (Number of Partitions) for multiple storage devices. The device `naa.5002538b00145ad0` appears multiple times with different PATH/WORLD/PARTITION IDs (e.g., 2097209, 2099383, 2106123), each showing **1 path, 6 worlds, and 1 partition**. The view demonstrates the "World" sub-view (activated by pressing **e**), showing per-world statistics for each LUN, with the system running 3 VMs across 933 worlds on an ESXi host with 103 days uptime.]

Partition shows the partition ID. Typically this is a simple number, such as 1 for the first partition. vSphere Client provides the following, which is more details yet easier.

[Image: This image shows the **Partition Details tab** in vSphere Client for a disk device using **GPT partition format**, listing 5 partitions — four "Legacy MBR" primary partitions (101 MB, 4 GB, 4 GB, and 119.9 GB) and one **VMFS primary partition (2 GB)**. In the context of the surrounding text, this screenshot illustrates the partition information referenced by the **NPN (Number of Partitions)** metric in esxtop, providing a more readable GUI-based view of partition data. The presence of a single VMFS partition aligns with the author's note that NPN should typically be 1 for VMFS datastores.]


###### Others

Let’s cover the rest of the metrics.

| NPH | Number of paths. This should not be 1 as that means a single point of failure. |
| --- | --- |
| NWD | Number of worlds. If you know the significance of this in troubleshooting, let me know. |
| NPN | Number of partitions. Expect this to be 1 for VMFS |
| SHARES | Number of shares. This statistic is applicable only to worlds.  This is interesting, as that means each world can have their own share? Where do we set them then? |
| BLKSZ | Block size in bytes.  I prefer to call this sector format. International Disk Drive Equipment and Materials Association (IDEMA) increased the sector size from 512 bytes to 4096 bytes (4 KB).  This is important, and you want them to be in 4K (Advanced Format) or at least 512e (e stands for emulation). Microsoft provides additional information here. |
| NUMBLKS | Number of blocks of the device. Multiply this with the block size and you get the total capacity. In vSphere UI, you get the capacity, which I think it’s more relevant. |

For configuration, I use vSphere Client as it provides a lot more information, and I can take action on them. The following is just some of the settings available.

[Image: ## Storage Devices Panel Description

The image shows the **vSphere Client Storage Devices configuration panel** for a host, listing four storage devices with key attributes including LUN number, device type, capacity, datastore assignment, hardware acceleration (VAAI) support, drive type, and adapter. Two disk devices are visible: a **Local SAMSUNG Disk (894.25 GB, Flash, vmhba0)** assigned to *datastore1* and a selected **Local ATA Disk (223.57 GB, Flash, vmhba3)** assigned to *datastore2*. Notably, all devices show **"Not supported"** under Hardware Acceleration, directly contextualizing the subsequent discussion about VAAI offloading capabilities and their vendor-dependent nature.]


##### VAAI

VMware vSphere Storage APIs - Array Integration (VAAI) offloads storage processing to the array, hence improving performance or reducing overhead. This is obviously vendor-dependant. There is no VAAI counter at adapter level or path level, as the implementation is at back-end array.
The VAAI has a lot of metrics. There are essentially 2 types of metrics: non latency and latency metrics.
As with metrics, check for contention type of metrics first. There are metrics that track failed operations, such as CLONE_F, ATSF and ZERO_F.
In this book, I’m grouping them by function as it’s easier to understand.
I saw this note from VMware vSphere Storage APIs – Array Integration (VAAI) document by Cormac Hogan, which I think it’s worth mentioning. Because the nature of VAAI as an offloads, you will see higher latency value of KAVG metric. Other latency metrics are not affected, so there is no issue unless there are other symptoms present.
At this moment, I have not found the need to document them further. So what you get here is mostly from the KB article above. Andreas Lesslhumer also has useful information in this blog article. Other references are this blog by Cormac and this this KB article.

###### Extended Copy

Hardware Accelerated Move (the SCSI opcode for XCOPY is 0x83)

| Clone_RD | RD stands for reader.  The number of CLONE commands successfully completed where this device was a source. WR stands for writer. The number of CLONE commands successfully completed where this device was a destination The number of failed CLONE commands |
| --- | --- |
| Clone_WR | RD stands for reader.  The number of CLONE commands successfully completed where this device was a source. WR stands for writer. The number of CLONE commands successfully completed where this device was a destination The number of failed CLONE commands |
| Clone_F | RD stands for reader.  The number of CLONE commands successfully completed where this device was a source. WR stands for writer. The number of CLONE commands successfully completed where this device was a destination The number of failed CLONE commands |
| LCLONE_RD | The same set of 3 metrics, except for Linked Clone. |
| LCLONE_WR | The same set of 3 metrics, except for Linked Clone. |
| LCLONE_F | The same set of 3 metrics, except for Linked Clone. |
| MBC_RD/s | MBC = megabytes of clone data. RD/s is read per second, and WR/s is written per second |
| MBC_WR/s | MBC = megabytes of clone data. RD/s is read per second, and WR/s is written per second |
| AVAG/suc | The average clone latency per successful command The average clone latency per failed command |
| AVAG/f | The average clone latency per successful command The average clone latency per failed command |


###### Atomic Test & Set

Hardware Accelerated Locking on Single Extent Datastore or on Multi Extent Datastore (SCSI code 0x89).

| ATS | The number of Atomic Test & Set (ATS) commands successfully completed |
| --- | --- |
| ATSF | The number of ATS commands failed. Expect this to be 0? |
| AAVG/suc | The Average ATS latency per successful command |
| AAVG/f | The Average ATS latency per failed command |


###### Write Same

Hardware Accelerated disk space initialization by writing 0s on all the blocks for faster future operations. The SCSI code for WRITE SAME operations is 0x93 or 0x41.

| ZERO | The number of ZERO commands successfully completed |
| --- | --- |
| ZERO_F | The number of ZERO commands failed |
| MBZERO/s | The megabytes zeroed per second |
| ZAVG/suc | The average zero latency per successful command |
| ZAVG/f | The average zero latency per failed command |


###### Unmapped

Unmapped block deletion (SCSI code 0x42). We discussed unmapped block (TRIM) in earlier chapter.

| DELETE | The number of successful DELETE commands |
| --- | --- |
| DELETE_F | The number of failed UNMAP commands, this value should be 0 |
| MBDEL/s (MB/s) | The rate at which the DELETE command getting processed. Measured in Megabytes per second |


###### Others


| RESSPACE | Reservation Space. The number of commands which were successful while doing space reservation for a VMDK file in thick Provisioning format. RESSPACE_F captures the failure. |
| --- | --- |
| RESSPACE_F | Reservation Space. The number of commands which were successful while doing space reservation for a VMDK file in thick Provisioning format. RESSPACE_F captures the failure. |
| EXTSTATS | Extended Statistics The number of commands which were successful in reporting extended statistics of a clone after the cloning process had been completed. EXTSTATS_F captures the failure |
| EXTSTATS_F | Extended Statistics The number of commands which were successful in reporting extended statistics of a clone after the cloning process had been completed. EXTSTATS_F captures the failure |
| CAVG/suc | The average clone latency per successful command. Unit is millisecond per clone.  CAVG/f captures the failures. |
| CAVG/f | The average clone latency per successful command. Unit is millisecond per clone.  CAVG/f captures the failures. |
| LCAVG/suc | As per above, but for Linked Clone. |
| LCAVG/f | As per above, but for Linked Clone. |
| RAVG/suc | The average latency (in ms) per successful VAAI Space Reservation command. RAVG/f captures the failures |
| RAVG/f | The average latency (in ms) per successful VAAI Space Reservation command. RAVG/f captures the failures |
| ESAVG/suc | As per above, but for Extended Statistics |
| ESAVG/f | As per above, but for Extended Statistics |


#### vSAN

I group the vSAN panel under Disk as esxtop only covers storage related information. There is no network or compute (vSAN kernel modules).

[Image: The image shows a legend/key for an **esxtop vSAN panel**, defining six column categories (A–F) used to interpret vSAN DOM (Distributed Object Manager) performance metrics. Column A represents the DOM role name, while columns B–F define statistics (IOPS, bandwidth, average latency, and standard deviation latency in ms) for five IO operation types: **READ, WRITE, RECOVERY WRITE, UNMAP, and RECOVERY UNMAP**. This legend provides the framework for interpreting the vSAN performance data described in the surrounding text.]

The panel provides visibility into 5 types of IO operations:
- Read
- Write
- Recovery Write
- Unmap
- Recovery Unmap
For each, it provides the IOPS, bandwidth, average latency (ms) and standard deviation latency (ms). Take note that some use MB, while others use GB.

| ROLE | The Distributed Object Manager (DOM) role of that component, such as client, owner, and component manager. |
| --- | --- |
| READS/s    MBREAD/s  AVGLAT SDLAT | Reads/second is the number of reads operations. This is IOPS. MBReads/s is read throughput in Megabytes/second.  AvgLat is the average latency. Standard deviation of latency, when above 10ms latency. |
| WRITES/s   MBWRITE/s  AVGLAT  SDLAT | Same set of metrics, like above, but for write |
| RECOWR/s  MBRECOWR/s  AVGLAT  SDLAT | Same set of metrics, like above, but for Recovery Write. Recovery covers component rebuild task (e.g. from disk failure). Read the string MBRECOWR as MB Reco Wr. |
| UNMAPS/s   GBUNMAP/s  AVGLAT  SDLAT | Same set of metrics, like above, but for unmap operations. I think this number should be within your expectation, as excessive unmap can impact performance.  GBUNMAP/s = Unmapped rates in Gigabytes/second Read the string GBUNMAP as GB Unmap |
| RECOUN/s  GBRECOUN/s  AVGLAT  SDLAT | Same set of metrics, but for Recovery Unmap operations.  Read the string GBRECOUN as GB Reco Un.  RecoUn/s is the number of recovery unmapped operations per second.  GBRecoUn/s is the amount of disk space in GB/second by Recovery Unmapped. |


### Network

Take note that the network panels mix the virtual and physical networks.
Focus on the virtual network first as that’s closer to the VM and kernel.

#### Contention

As usual, we check contention first. There are no network latency and packet retransmit metrics.

[Image: This screenshot shows ESXi network port statistics with **PORT-ID**, **USED-BY**, **%DRPTX** (percentage dropped transmit packets), and **%DRPRX** (percentage dropped receive packets) columns. The ports include management interfaces, vmnic physical adapters (vmnic0, vmnic1), vmk0 kernel adapter, and virtual ports for VMs including vCenter Server (2106123) and vRealize Operations (2106767). All **%DRPTX and %DRPRX values are 0.00%** across all ports, demonstrating a healthy network with no dropped packets on either transmit or receive paths.]


| %DRPTX | Percentage of Dropped Packet. Expressed in percentage, which makes it easier as you expect this not to exceed 0.x%. In dedicated network such as vSAN and vMotion, this should be flat 0% non-stop for every single ESXi. Transmit and Receive have different nature. A high drop in transmit means your physical NIC card or uplink switch is unable to cope. A high drop in receive means your ESXi or VM may not have enough CPU to process the packet, or the ring buffer size is too small.  : The screen output show dropped receive packets at the virtual switch port. They are actually dropped between the virtual switch and the guest OS driver. The dropped packets can be reduced by increasing the Rx buffers for the virtual network driver. |
| --- | --- |
| %DRPRX | Percentage of Dropped Packet. Expressed in percentage, which makes it easier as you expect this not to exceed 0.x%. In dedicated network such as vSAN and vMotion, this should be flat 0% non-stop for every single ESXi. Transmit and Receive have different nature. A high drop in transmit means your physical NIC card or uplink switch is unable to cope. A high drop in receive means your ESXi or VM may not have enough CPU to process the packet, or the ring buffer size is too small.  : The screen output show dropped receive packets at the virtual switch port. They are actually dropped between the virtual switch and the guest OS driver. The dropped packets can be reduced by increasing the Rx buffers for the virtual network driver. |


#### Consumption

As usual, check the non-unicast packets first and make sure they match the expectation at that time.

##### Non-Unicast Packets


| PKTTXMUL/s | Number of multicast packets transmitted or received per second.  Read the string PKTTXMUL as Pkt Tx Mul, which is Packet TX Multicast. Same with PKTRXMUL. |
| --- | --- |
| PKTRXMUL/s | Number of multicast packets transmitted or received per second.  Read the string PKTTXMUL as Pkt Tx Mul, which is Packet TX Multicast. Same with PKTRXMUL. |
| PKTTXBRD/s | Number of broadcast packets transmitted or received per second.  Read the string PKTTXBRD as Pkt Tx Brd, which is Packet TX Broadcast. Same with PKTRXBRD |
| PKTRXBRD/s | Number of broadcast packets transmitted or received per second.  Read the string PKTTXBRD as Pkt Tx Brd, which is Packet TX Broadcast. Same with PKTRXBRD |


##### All Packets


[Image: ## Image Description

This is a VMware vSphere **virtual switch port statistics table** displaying network metrics for multiple ports, including management interfaces, shadow ports, VMkernel (vmk0), VMs (vCenter Server, vRealize Operations, a Windows VM), and physical NICs (vmnic0/vmnic1). The key metrics shown are **PKTTX/s, MbTX/s, PSZTX, PKTRX/s, MbRX/s, and PSZRX** (packet rates, throughput in Mbps, and packet sizes for both TX and RX directions). Notably, **vmk0 and vmnic0 show a PSZTX of 402.00 bytes**, vmnic1 shows **PSZRX of 62.00** and vmnic0 **60.00**, while all packet rate and throughput values (PKTTX/s, MbTX/s, PKTRX/s, MbRX/s) are **0.00** across all ports, indicating a near-idle network state during this capture.]


| PKTTX/s | This is the total packets, so it includes multicast packet and broadcast packet. Multicast packet and broadcast packet are listed separately. This is handy as they are supposed to low most of the time. |
| --- | --- |
| PKTRX/s | This is the total packets, so it includes multicast packet and broadcast packet. Multicast packet and broadcast packet are listed separately. This is handy as they are supposed to low most of the time. |
| MbTX/s | This is measured in bit, unlike vCenter Client UI which shows in byte.  Packet length is typically measured in bytes. A standard packet is 1500 bytes, so a 10 Gb NIC would theoretically max out at 833,333 packets on each direction.  Compare this with your ESXi physical network card. |
| MbRX/s | This is measured in bit, unlike vCenter Client UI which shows in byte.  Packet length is typically measured in bytes. A standard packet is 1500 bytes, so a 10 Gb NIC would theoretically max out at 833,333 packets on each direction.  Compare this with your ESXi physical network card. |
| PSZTX | This is convenient. If you see a number far lower than 1500, it’s worth discussing with network team. |
| PSZRX | This is convenient. If you see a number far lower than 1500, it’s worth discussing with network team. |

There is another metric ACTN/s, which is the number of actions per second. The actions here are the kernel actions. It is an internal counter, not relevant to day to day operations.

#### Configuration

This panel mixes physical and virtual. For virtual, it shows both the kernel network and VM network. I find it easier to use the information in vSphere Client.

[Image: This image shows the output of a VMware vSwitch port configuration command, displaying **8 ports** on **vSwitch0** with their associated metadata. Key data points include two active uplink ports (**vmnic0 and vmnic1**) operating at **10,000 Mbps full duplex (FDUPLX: Y)**, while the remaining ports (PORT-IDs 67108870–67108880) are non-uplink virtual ports (UPLINK: N) used by VMs and kernel components including **vmk0, vCenter Server (VM 2106123), vRealize Operations (VM 2106767), and a Windows VM (VM 2291223)**. The image demonstrates the mixed physical/virtual nature of vSwitch port configuration referenced in the surrounding text, showing how uplinks (physical NICs) and virtual device ports coexist within the same virtual switch.]


| PORT-ID | Virtual network device port ID. |
| --- | --- |
| UPLINK | ‘Y’ means that the corresponding port is an uplink. ‘N’ means it is not. The physical NIC cards (vmnic0, vmnic1, etc.) serve as the uplink |
| UP | ‘Y’ means that the corresponding link is up. ‘N’ means it is not. |
| SPEED | Link speed in Megabits per second. |
| FDUPLX | ‘Y’ means the corresponding link is operating at full duplex. ‘N’ means it is not, which is a problem. |
| USED-BY | Virtual network device port user. |
| DNAME | Virtual network device name. |

The metric DTYP (Virtual network device type, where H means Hub and S means switch) does not seem to be available anymore.
vSphere Client separates the components. You can see the virtual switches, the kernel network and physical cards. The level of details is more comprehensive.

[Image: The image shows the **Physical Adapters** view in the VMware vSphere Client, displaying four network interface cards (vmnic0–vmnic3) with their associated metrics. vmnic0 and vmnic1 are in a **Down** state with no switch assignment and no observed networks, while vmnic2 (10 Gbit/s, vSwitch0, MAC: 3c:fd:fe:ac:f5:5c) and vmnic3 (10 Gbit/s, SC2-dSwitch-1, MAC: 3c:fd:fe:ac:f5:5d) are active and associated with IP ranges including VLAN1536 (10.173.22.1–10.173.22.254). This screenshot demonstrates how vSphere Client provides a more comprehensive, component-separated view of physical adapter metrics compared to the CLI-based esxtop metrics described in the surrounding text.]


#### RDMA Device

Remote Direct Memory Access (RDMA) enable direct access to the physical network card, bypassing the OS overhead. The following screenshot, taken from here, shows 2 types of access from application (that lives inside a VM. The VMs are not shown).

[Image: ## Image Description

This architectural diagram illustrates two distinct network access paths from user-space applications to physical network hardware: a **traditional Sockets API path** (left) that traverses the full kernel stack — Sockets → TCP → IPv4/IPv6 → Network Device → Device Driver — and an **RDMA Kernel Bypass path** (right) that uses the RDMA Verbs API to route directly to the Device Driver, bypassing OS networking layers entirely. Both paths terminate at a **Host Channel Adapter (HCA)**, which supports three underlying transport protocols: **InfiniBand**, **RoCE** (highlighted in orange), and **iWARP**. In the context of the surrounding text, the diagram explains why RDMA metrics (TX/RX packet drops via `%PKTDTX`/`%PKTDRX`) differ from standard network metrics — since the kernel bypass eliminates retransmit and latency visibility, only packet drop counters are available for contention monitoring.]


##### Usage

Since it’s about network, you get both the TX (transmit or sent) and RX (received or incoming).
For contention, there is only packet dropped. There is no packet retransmit or latency. The metrics are:

| %PKTDTX | Percentage of packet dropped relative to number of packets sent. |
| --- | --- |
| %PKTDRX | Percentage of packet dropped relative to number of packets sent. |

For utilization, you get them in both amount of data, and number of packets. Both are important metrics. There is no breakdown on the type of packets (broadcast, multicast, unicast).

| PKTTX/s | Packets per second.  Check the limit for packet per second in your specific card. |
| --- | --- |
| PKTRX/s | Packets per second.  Check the limit for packet per second in your specific card. |
| MbTX/s | Network throughput in Megabit/second. |
| MbRX/s | Network throughput in Megabit/second. |

There is no packet size. This can be handy to determine if they are much smaller or larger than you expect. For example, if you expect jumbo frame but the reality is much smaller.
These metrics are not available in vSphere Client UI, so you need to use esxtop to get the visibility. Just in case you’re wondering where I got the following screenshot from, they are courtesy of Shoby Cherian and Aditya Kiran Pentyala.

[Image: ## ESXtop RDMA Network Metrics Screenshot

The image shows an **esxtop output** displaying RDMA network interface statistics for two adapters: **vmrdma0** (on vmnic2) and **vmrdma1** (on vmnic3). Key metrics include packet and throughput rates in both directions — notably, vmrdma1 shows significantly higher TX traffic (**4,876,380 pkts/s at 40,700 Mb/s**) while vmrdma0 shows much higher RX traffic (**1,951,328 pkts/s at 16,286 Mb/s**). Both interfaces have **2 Queue Pairs (QP)** and **4 Memory Regions (MR)** allocated, demonstrating the RDMA-specific metrics only visible via esxtop (not the vSphere Client UI).]

You also get the queue usage information.

| QP | Number of Queue Pairs Allocated and Completion Queue Pairs Allocated. RDMA uses these queues for communication. |
| --- | --- |
| CQ | Number of Queue Pairs Allocated and Completion Queue Pairs Allocated. RDMA uses these queues for communication. |
| SRQ | Number of Shared Receive Queues Allocated I think this is required in virtualization as the physical NIC card can be shared. |
| MR | Memory Regions Allocated. Check that this is inline with your expectation. |

For more reading on RDMA, I found this academic paper, title “Understanding the concepts and mechanisms of RDMA” useful.

##### Configuration

vSphere Client provides the following information. You get the first 4 columns in esxtop.

[Image: ## RDMA Adapters Configuration Screenshot

The image displays the **RDMA adapters panel** in vSphere Client, showing two adapters (**vmrdma0** and **vmrdma1**) both using the **nmlx5_rdma** driver, paired with **vmnic4** and **vmnic5** respectively, where vmrdma0 is **Active** and vmrdma1 is **Down**. Both adapters have **RoCE v1 and RoCE v2 enabled (Yes)** but **iWARP disabled (No)**. The detail pane for vmrdma0 shows it is a **ConnectX-5 PCIe 3.0** device with an MTU of **1024** and a speed of **100 Gbit/s**, illustrating the configuration data available in vSphere Client beyond what esxtop provides.]

The information you get in esxtop covers the first 4 columns in the preceding screenshot. They are:

| NAME | Name of the device |
| --- | --- |
| DRIVER | Name of the driver |
| STATE | Active or down |
| TEAM-PNIC | The physical Network Interface Card that the RDMA adapter is paired with. |

Chapter 8