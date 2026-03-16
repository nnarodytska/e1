# Memory


## Architecture

The purpose of memory is to act as disk cache. So you want to utilize all the cache given to you. 100% usage results in faster performance than 99%, all else being equal.
Let's now take a trip down memory lane, pun intended.
Memory differs from CPU as it is a form of storage.
- CPU is transient in nature. Instructions enter and leave the execution pipelines in less than a nanosecond. That’s why CPU reservation becomes not applicable when the VM is not using it.
- Memory behaves more like disk space. Memory reservation could remain in place even if the VM has not read or written the page in days.
As a storage, memory is basically a collection of blocks in physical DIMM. Information is stored in memory in standard block sizes, typically 4 KB or 2 MB. Each block is called a page. At the lowest level, the memory pages are just a series of zeroes and ones. MS Windows initializes its pages with 0, hence there is a zero-page counter in ESXi.
Keeping this concept in mind is critical as you review the memory metrics. The storage nature of memory is the reason why memory monitoring is more challenging than CPU monitoring. Unlike CPU, memory has 2 dimensions:

| Speed | Nanoseconds | The only counter ESXi has is Memory Latency. This counter increases when the time to read from the RAM is longer than usual. The counter tracks the percentage of memory space that’s taking longer than expected. It’s not tracking the actual latency in nanosecond.  This is the opposite of Disk, where we track the actual latency, but not the percentage of amount of space that is facing latency.  Both are storage, but “server people” and “storage people” measure them differently 😊 |
| --- | --- | --- |
| Space | Bytes | This is the bulk of the metrics |
|  | Bytes | As storage, it’s relatively static. As a result, you can create a heat map that plots all your Guest OS or VMs memory consumption. You want it near 100% while making sure the page in and page out rate within normal expectation. |


### The 4 Layers

With virtualization, there are 2 additional layers added. This brings the total to 4 from Process à Guest OS à VM à ESXi.
The only layer that manages the actual physical memory is the last layer. This is why the term “Guest physical memory” is illogical.
Each layer has their own viewpoint. Understanding the vantage point is required to make sense of the metrics. It will prevent you from comparing metrics that are not comparable (e.g. granted vs consumed) as they have different context.
Each of these layers have their own address space. And that’s where the fun of performance troubleshooting begins 😉

#### Virtual Memory

Virtual memory is an integral part of memory management. The following shows how Windows or Linux masks the underlying physical memory from processes running on the OS.

[Image: ## Image Description

The diagram illustrates **virtual memory abstraction** in an OS, showing how multiple processes (Process 0 through Process n) each perceive a **256 TB virtual address space**, while the underlying physical resources consist of only **64 TB RAM** and **256 TB storage (pagefile/swap)**. The "Magic" block represents the OS memory manager that maps virtual addresses to physical memory and disk. This demonstrates the overcommitment principle — the sum of virtual address spaces (n × 256 TB) far exceeds actual physical RAM (64 TB), with the deficit backed by storage.]

From the process’ point of view, this technique provides a contiguous address space, which makes memory management easier. It also provides isolation, meaning process A can’t see the memory of process B. This isolation provides some level of security. The isolation is not as good as isolation by container, which in turn is inferior to isolation by VM.
Virtual memory abstraction provides the possibility to overcommit. Microsoft Windows may only have 16 GB of physical RAM, but by using pagefile the total memory available to its processes can exceed 16 GB. The process is unaware what is backing its virtual address. It does not know whether a page is backed by Physical Memory or Swap File. All it experiences is slowness, but it won’t know why as there is no counter at process level that can differentiate the memory source.
On the other hand, some applications manage its own memory and do not expose to the operating system. Example of such applications as are database and Java VM. Oleg Ulyanov shared in this blog SQL Server has its own operating system called SQLOS. It handles memory and buffer management without communicating back to underlying operating system.

[Image: ## Image Description

The diagram illustrates how multiple VMs (VM 0 through VM n), each with **6 TB of virtual memory**, connect through a "Magic" abstraction layer (representing VMware's memory management) to produce different logical memory outputs on the right side. The outputs include various storage/memory types with one concrete value visible (**16 TB** for a block storage resource) and several unknown values (marked as **\*\*\* TB**) representing shared, imported, database, and snapshot/clone memory pools. In the context of the surrounding text, this diagram demonstrates how ESXi abstracts and transforms VM memory address spaces — providing each VM with contiguous, isolated memory while the underlying physical pages are managed differently at the hypervisor layer.]

From the VMs point of view, it provides a contiguous address space and isolation (which is security). The underlying physical pages at ESXi layer may not be contiguous, as it’s managed differently.

| VM memory | Metrics tracks the VM Pages. There are 2 sets, one for each VM, and one a summation at ESXi level for all running VMs. Do not confuse the summation with ESXi memory metrics. Examples: Granted or Memory Shared |
| --- | --- |
| ESXi memory | Metrics tracks the ESXi Pages. There are also 2 sets, but the summation at ESXi level contains the kernel own memory and VM overhead Examples: Consumed or Memory Shared Common |

ESXi uses 3 levels to manage memory:

| TPS | Transparent Page Sharing (TPS) happens automatically even if ESXi has plenty of RAM as it makes sense to do so. It’s not an indicative of unmet demand. Sharing the same page is the right thing to do, and not something that should be started only when physical pages are running low.  See more here. |
| --- | --- |
| Tiered Memory | This also happens transparently to the VM. ESXi moves inactives pages to the NVMe device. |
| Balloon | The first sign of unmet demand. It happens proactively, before ESXi is unable to meet Demand. Ballooning reduces cache. It does not mean ESXi unable to meet Demand. Demand is not met when Contention happen. That’s the only time it is not met. |
| Compress/Swap | This happens proactively too.  It does not mean VMs were contending for RAM. It merely means ESXi Consumed is very high. That Consumed can contain a lot of cache |
| Compress/Swap | If there is a host cache, ESXi uses this first. |

This abstraction provides the possibility to overcommit, because the VM is unaware what is backing the physical address. It could be physical memory on DIMM, swap file, Copy-on-Write, zipped, or ballooned. The following is taken from VMware vSphere 6.5 Host Resources Deep Dive. I have highlighted in green the part you need to pay attention.

[Image: This image is a text excerpt from *VMware vSphere 6.5 Host Resources Deep Dive* explaining the **memory management abstraction** between the VMkernel and guest OS. It highlights (in green) the concept of **"mutual disconnect"** — the VMkernel manages physical memory **without** guest OS knowledge, while the guest OS manages its own memory space **without informing** the VMkernel. This bidirectional isolation is the foundational principle that enables ESXi's memory overcommitment, as VMs cannot directly observe what physically backs their memory addresses (DIMM, swap, balloon, compressed pages, etc.).]

Read further and you will see that the kernel large page setting contributes more to ESXi capacity and the VM performance.

#### Relationship

Let’s put the 4 layers in a diagram, showing how a page maps across the 4 layers.
What can we notice from the diagram?

[Image: ## Image Description

This diagram illustrates the **4-layer memory mapping hierarchy** in VMware vSphere, showing how memory pages map across: **Process → Guest OS → VM → ESXi Host (DIMM/Disk)**. Each layer's memory is color-coded by state: **red (active)**, **gray (passive/inactive)**, **yellow (balloon)**, **orange (VM overhead)**, **green (compressed)**, **purple (VMkernel)**, and **black (swapped to host cache/disk)**. Key memory reclamation mechanisms are labeled — **TPS** (Transparent Page Sharing, shown via green arrows consolidating VM pages to physical DIMM), **ballooning** (yellow blocks notably having **no downward arrow**, indicating they don't map to physical memory), and **compression** — demonstrating how ESXi manages physical memory contention across multiple abstraction layers.]

Yup, a few things:
- Balloon did not map to physical layer. Notice there is no arrow on the yellow blocks
- The physical memory is “shared” between VM and hypervisor own processes, meaning you need to manage them as one. Sum their utilization to form the total consumption.
- At the physical layer, there can be host cache and tiered memory, and not just DIMM.
- Just to be complete, the mapping may not be to the closest DIMM. You can have NUMA effect.
The VM Monitor for each VM maps the VM pages to the ESXi pages. This page mapping is not always 1:1. Multiple VM pages may point to the same ESXi pages due to transparent page sharing. On the other hand, VM page may not map to ESXi page due to balloon and swapped. The net effect is the VM pages and ESXi pages (for that VM) will not be the same, hence we need two sets of metrics.
Let’s zoom into the key metrics that form a single VM.

[Image: ## Image Description

The diagram illustrates three hierarchical memory perspective layers in VMware vSphere: **Guest OS View** (Windows/Linux perspective showing In-Use, Cache, and Free segments), **Virtual View** (VM perspective showing memory categorized as Granted, Zipped, Swapped, and Ballooned), and **Physical View** (ESXi perspective showing Consumed and Swapped metrics). The mapping arrows demonstrate that VM pages do not have a 1:1 relationship with physical ESXi pages — Granted memory maps to Consumed (with page sharing consolidation shown in black/blue arrows), Zipped/Swapped pages map to physical Swapped blocks (red arrows), and Ballooned pages (yellow) have **no corresponding physical mapping** at the ESXi layer. This visually explains why VM-level metrics and ESXi-level metrics diverge, as the VM reports input-side values while ESXi reports the resulting physical output, particularly highlighting how ballooning removes pages from the physical address space entirely.]

Take note the difference between the VM perspective and the ESXi perspective.
- The VM looks at the “input”, while ESXi looks at the “output”. For example, VM metrics will report 3 pages being shared, while ESXi will report 1 page of the result shared page.
- Balloon does not exist at physical view as the page has been removed. It’s not pointing to any block in the ESXi memory address space.
Further reading: vSphere Resource Management technical paper.

### Guest OS vs VM

Both come with dozens of metrics. Compared with Guest OS such as Windows, can you notice what’s missing and what’s added?
The following diagram compares the memory metrics between VM and Guest OS,

[Image: ## Image Description

The diagram compares memory metrics between two perspectives: **what the Hypervisor (ESXi) sees** (left side, ranging 0–8 GB) and **what the Guest OS sees** (right side), illustrating how the same physical memory is represented differently at each layer. The hypervisor-side metrics include **Consumed, Active, Granted, Reservation, Balloon, Swapped, Shared, Compressed, Overhead, and Swap File**, while the Guest OS side shows **Page File, Hardware Reserved, Guest Free, Guest Cache/Buffers, Windows "In Use," Windows Modified, Windows "Compressed," Balloon, and Linux "Used."** The diagram visually demonstrates the metric translation gap referenced in the surrounding text — key hypervisor metrics like **Consumed, Shared, and Reservation have no equivalent in the Guest OS view**, and contention indicators like swapping/ballooning appear differently (or not at all) across the two perspectives.]

Guest OS and VM metrics do not map to each other. Neither the kernel nor the Guest OS have full visibility into each other.
Right off the bat, you will notice that popular metrics such as Consumed, Shared, and Reservation do not even exist in Windows.

| Type | Guest OS Metric | VM Metrics |
| --- | --- | --- |
| Contention | Paging | None |
| Contention | None | Latency |
| Utilization | In Use | None |
| Utilization | Cache | None |
| Utilization | Free | None |
| Utilization | Compressed | None |
| Utilization | None | Swapped or Compressed |

ESXi Host cannot see how the Guest OS manages its memory pages, how it classifies the pages as Use, Modified, Cache and Free. ESXi also cannot see the virtual memory (page file).
ESXi can only see when the Guest OS performs reads or writes. That’s why vSphere VM main metrics are basically what is active recently and what has been active. The first one is called Active, the second is called Consumed. All other metrics are about ESXi memory management, and not about VM memory utilization. VM memory utilization impacts ESXi memory management, but they are clearly not the same thing.

#### Example: Guest OS More Accurate

Let’s take an example with a simple Microsoft Windows server running Active Directory. It has 4 GB of memory as it’s just serving a small number of objects in the Singapore office lab. Look at the following table, where I compared the counter from inside the Guest OS and the VM memory active counter.

[Image: ## Image Description

The chart displays two memory metrics over approximately 2.5 days (Oct 2–4): **vmsgdc001.vmsg.lab - UTILIZATION|Percent Used Memory (%)** (blue/dark, Guest OS metric via Telegraf agent) and **VMSG-DC-001 - Memory|Workload %** (pink/magenta, vCenter metric), divided into four labeled periods (A–D). During **Period A**, only the vCenter workload metric is visible at ~15-20%, while in **Period B** (post-agent installation), the Guest OS metric (blue) shows ~40-60% actual memory usage with regular 5-minute collection spikes, dramatically contrasting with the vCenter active memory metric. This demonstrates that vCenter's Active memory counter significantly **underreports** true Guest OS memory consumption compared to direct in-guest measurement.]

There are four periods above where I made changes inside Windows. Let’s step through them.

| Period | What happened |
| --- | --- |
| A | Microsoft AD server in normal running condition. vCenter is reporting low utilization, around 15-20%. Note vCenter users the Active metric, not Consumed. |
| B | I installed the VCF Operations agent, which is based on the open source Telegraf. This gives the Guest OS metric, which is shown in blue. The agent collects data every 5 minutes, hence the regular spike. So far so good. Notice the value from VM Active metric jumps to 100%. That’s fine, but then it stays at 100% for more than 12 hours. All I did was installing a small collection agent and that’s it.  I actually got an alarm in vCenter, even though the VM does not need the RAM obviously. What happened here prove that the Active counter is based on sampling, and that sampling could be wrong. |
| C | The next morning, I decided to generate some load as the pattern does not change at all. Since Windows has not been patched for a long time, I started Windows patch. The entire process is mostly downloading and installing, which last for several hours. The two metrics show no correlation at all. |
| D | After several hours, the entire Windows update process is completed. |


#### Example: VM More Accurate

Let’s now look inside the VM. I will use another VM to show a different example. This time around, I will take an idle VM so we can see how the metrics behave. An idle VM will have minimal or 0 activity.
You can see that this Windows Server 2016 VM has 16 GB, but 0 GB is active. It is expected as we know the Guest OS is idle as nothing is installed. vCenter is showing the data correctly. So far so good….

[Image: The image shows a VMware vCenter summary page for a VM named "WindowsTest" running Microsoft Windows Server 2016 (64-bit) with 8 vCPUs, 16 GB RAM, and a 40 GB hard disk. Key metrics displayed show **CPU Usage: 0 Hz**, **Memory Usage: 0 B**, and **Storage Usage: 52.11 GB**, with the Memory hardware detail confirming **"16 GB, 0 GB memory active."** This screenshot demonstrates vCenter's perspective of an idle VM — reporting 0 B memory usage — which contrasts with the subsequent point that Windows Task Manager will show approximately 7.2 GB "In Use," illustrating the discrepancy between hypervisor-level memory metrics and guest OS memory reporting.]

What do you think you will see inside Windows?
Will the Windows In Use counter show that it’s using 0 GB or somewhere near there? You know that it won’t show 0 GB as it’s impossible that any OS does not use any memory while it’s running. So what number will the In Use counter show?

[Image: ## Windows Task Manager Memory Metrics

The screenshot shows Windows Task Manager's Performance tab displaying **Memory usage of 7.2 GB (compressed 1.5 GB) out of 16.0 GB total (47%)**, with 8.5 GB available, on a system with 2 memory slots used in Chip form factor. The memory usage graph shows a **flat, consistent utilization line**, indicating steady consumption with no activity spikes. This demonstrates the discrepancy between ESXi's reported **~0 GB active memory** for the VM and Windows' internal view of **7.2 GB in use**, illustrating how the Guest OS memory counters do not reflect the hypervisor's balloon/compression activity.]

It’s showing 7.2 GB! That’s nowhere near 0%.
Look at the chart. What do you notice?
It portrays that it has been constantly or actively using that much of memory. In reality, we know it’s idle because ESXi is the one doing the actual reading and writing. The other proof that it is idle is Windows actually compressed 1.5 GB of this 7.2 GB.
One possible reason why Windows is showing high usage when there is none is applications that manage their own memory. These applications will ask for the memory upfront in 1 contiguous block. You can see in the example below:

|  | You can see that java.exe takes up 26 GB. JVM (Java Virtual Machine) manages that memory and Windows can’t see inside this block. Windows sees the entire block as used and committed, regardless of the application actually uses it or not. BTW, the above is taken from old blog article of Manny Sidhu. The blog no longer available, hence I could not provide the link. |
| --- | --- |


[Image: ## Windows Task Manager Performance Tab

The screenshot shows Windows Task Manager's Performance tab displaying **32% CPU usage** and **29.3 GB memory consumption** out of 32,767 MB (32 GB) total physical memory, with **91% memory utilization** and only 252 MB free. 

In the context of the surrounding text, this demonstrates how a JVM-based application (java.exe consuming ~26 GB) allocates memory as a single contiguous committed block, causing Windows to report nearly all physical memory as used (29.3 GB) regardless of the JVM's actual internal utilization — illustrating why Windows-level memory metrics can be misleading for virtualized or managed-runtime workloads.]

I hope the above simple experiments shows that you should use the right counter for the right purpose.

## VM

Just like the case for CPU, some metrics are for the kernel consumption, not your operations.

### Overview

For performance use case, the only counter tracking actual performance is Page-fault Latency.

[Image: The image displays a table of VMware vSphere VM memory counters, showing metrics including **Overhead Reserved** (Average, KB), **Page-fault Latency** (Average, %), **Shared** (Average, KB), and **Swap In** (Average, KB). A tooltip is visible highlighting the **Page-fault Latency** description: *"Percentage of time the virtual machine spent waiting to swap in or decompress guest physical memory."* In the context of the surrounding text, this table supports the assertion that **Page-fault Latency is the only counter tracking actual VM memory performance**, as opposed to other metrics which reflect kernel/ESXi-level consumption rather than operational performance.]

Next, check for swapping as it’s slower than compressed. You get 6 metrics for it

[Image: The image displays a table of **6 VM memory swap-related counters** in VMware vSphere, all using **Average rollups**. The metrics include **Swap in/out** (KB), **Swap in/out rate** (KBps), **Swap target** (KB), and **Swapped** (KB), each with descriptions explaining they measure guest physical memory movement to/from swap space. In context, this table identifies the available metrics for monitoring VM swapping activity, which the author notes should be checked after page-fault latency but before compressed memory metrics, as swapping is slower than compression.]

Next is compressed

[Image: ## Image Description

The image displays a table of **five VMware ESXi memory compression metrics**: Compressed (Average, KB), Compressed (Latest, KB), Compression rate (Average, KBps), Compression saved (Latest, KB), and Decompression rate (Average, KBps). These metrics track guest physical memory pages undergoing compression, the rate of compression/decompression by ESXi, and host physical memory reclaimed via compression. In context, this table represents the compression-related counters a vSphere administrator would monitor after ruling out swapping, as compression is a faster memory reclamation technique than swap but still indicates memory pressure on the host.]

Host Cache should be faster than disk (at least I assume you designed it with faster SSD), so you check it last.

[Image: The image displays a table of **3 Host Cache memory metrics** in VMware vSphere: **Host cache consumed** (Average, KB), **Host cache swap in rate** (Average, KBps), and **Host cache swap out rate** (Average, KBps). These metrics track storage space used on the host swap cache and the rates at which guest physical memory is swapped in/out from that cache. In context, this represents the fourth tier of memory reclamation to monitor for performance, positioned after swapping and compression checks, with the assumption that host cache (SSD-backed) performs faster than traditional disk swap.]

Lastly, there is the balloon.

[Image: The image displays two balloon memory metrics from VMware vSphere: **Balloon Target** and **Ballooned Memory**, both measured in KB as Average/Absolute values. Balloon Target represents the desired amount of guest physical memory the balloon driver needs to reclaim, while Ballooned Memory represents the actual amount reclaimed from the VM. These metrics appear in the context of memory reclamation techniques, positioned as the last (slowest/least preferred) reclamation method after swapping, compression, and host cache.]

Wait! Where is the Intel Optane memory metrics?
It does not exist yet, as that’s supposed to be transparent to ESXi.
Performance is essentially the only use case you have at VM level. For Capacity, you should look at Guest OS. The VM capacity metrics serve as input to the host capacity and are used in determining the VM memory footprint (e.g. when migrating to another ESXi).
You’ve got 5 metrics, with consume being the main one.

[Image: The image displays a table of **5 VM-level memory metrics** from VMware vSphere: **Consumed, Host Consumed %, Entitlement, Granted, and Shared**. All metrics use **Average** rollup, with four measured in **KB** and one in **%**. This table contextualizes the surrounding text's claim that there are "5 metrics, with consumed being the main one," showing each metric's unit and a brief description of what host or guest physical memory aspect it measures.]

I’m going to add Active next, although I don’t see any use case for it. It’s an internal counter used by the kernel memory management.

[Image: The image shows a metrics table displaying two VMware guest memory counters: **Active** and **Active write**, both measured as Average, in KB, with Absolute rollup type. Both metrics track guest physical memory activity — **Active** measures memory being read or written, while **Active write** specifically tracks memory being written by the guest. This table appears in the context of the author introducing these counters while noting they have limited practical use cases, serving primarily as internal kernel memory management counters.]

Lastly, you get the shared pages and 0 pages.

[Image: The image displays a table of four VM memory metrics from vSphere: **Overhead active**, **Overhead consumed**, **Overhead reserved**, and **Zero pages** — all measured as averages in KB. The table provides brief descriptions of each metric, noting that the overhead metrics relate to ESXi host physical memory used for its data structures to run virtual machines, while Zero pages tracks guest physical memory pages containing 0x00. This image appears in the context of concluding the overview of VM memory metrics, specifically covering the overhead-related counters and zero/shared pages mentioned in the preceding text.]

Now that we’ve got the overview, let’s dive into the first counter!

### “Contention” Metrics

I use quote because the only true contention counter is latency. The second reason is VCF Operations has a metric called Contention, which is actually vCenter counter called latency.

#### Latency

Memory Latency, aka "Page-fault latency" is tracking the amount of time a vCPU spends waiting on the completion of a page fault. Its value is mostly swap wait, with a bit of page decompression / copy-on-write-break. The counter is called %LAT_M in esxtop.
The latency metric is highly corelated with the swap-in rate.

[Image: ## Image Description

The image displays two time-series charts for host **ora-uat1-ebs-r2** spanning approximately 24 hours (Jan 13 12:00 PM to Jan 14 12:00 PM). The top chart shows **Memory Swap In Rate (KBps)** with a peak of **6,352.6 KBps** around 2:00 PM and a baseline of **1.73 KBps**, while the bottom chart shows **Memory Contention/Latency (%)** peaking at **2.11%** with a baseline of **0.001%**. The two charts demonstrate the strong correlation described in the surrounding text — the Swap In Rate spikes and the Contention (latency) spikes are nearly identical in shape and timing, visually confirming that memory latency is driven primarily by swap-in activity.]

This is the only performance counter for memory. Everything else does not actually measure latency. They measure utilization, because they measure the disk space occupied. None captures the performance, which is how fast that memory page is made available to the CPU.
Consider the hard disk space occupied. A 90% utilization of the space is not slower than 10%. It’s a capacity issue, not performance.
If a page is not in the physical DIMM, the VM has to wait longer. It could be in Host Cache, Swapped or Compressed. It will take longer than usual. vSphere tracks this in 2 metrics: CPU Swap Wait and RAM Latency.
- CPU Swap Wait tracks the time for Swapped In.
- RAM Latency tracks the percentage of time VM waiting for Decompressed and Swapped In. The RAM Latency is a superset of CPU Swap Wait as it caters for more scenarios where CPU has to wait. VCF Operations VM Memory Contention metric maps to this.
Latency is >1000x lower in memory compared to disk, as it's CPU basically next to the CPU on the motherboard. Time taken to access memory on the DIMM bank is only around 200 nanoseconds. Windows/Linux does not track memory latency. The closest counter is perhaps page fault. The question is does page fault includes prefetch? If you know, let me know please.
This counter has the effect of reduced value of the Compressed metric and/or Swapped metric, and increased the value of Consumed & Granted.
Latency does not include balloon as that’s a different context. In addition, the hypervisor is not aware of the Guest OS internal activity.
Actions you can do to address high value:
- Store vswp file on higher throughput, lower latency storage, such as using Host Swap Cache.
- Increase memory shares and/or reservation to decrease amount of swapping. If the VM belongs to a resource pool, ensure the resource pool has sufficient for all its VMs.
- Reduce assigned memory. By rightsizing, you reduce the size of memory reclamation, hence minimizing the risk.
- Remove VM Limit.
- Unswap the swapped memory. You cannot do this via API, but you can issue the command manually. Review this article by Duncan Epping and Valentin Bondzio.
- If possible, reboot the VM as part of regular maintenance. This will eliminate the swap file, hence avoiding future, unexpected swap wait on that swapped page. Note this does guarantee the same page to be swapped out again.

##### Best Practice

In an environment where you do not do memory overcommit and place limit, the chance of hitting memory contention will be basically 0. You can plot the highest VM Memory Contention counter in all clusters and you will basically see a flat line. That would be a lot of line charts, so I’m using a pie chart to analyze 2441 VM in the last 4 months. For each VM, I took the highest value in the last 4 months. Only 13 VM had its worst VM Contention above 1%.

[Image: ## Image Description

This pie chart displays **VM Memory Contention** distribution across **2,441 VMs** over a **4-month period** (relative date range), sourced from vSphere Hosts and Clusters. The dominant segment shows **99.47% of VMs (2,428/2,441)** experienced peak memory contention in the **0-1% range**, with only small fractions falling in higher ranges: **0.16%** (1-2%), **0.082%** (2-3%), and **0.29%** (5-100%). This demonstrates the best practice outcome of avoiding memory overcommit and limits — resulting in near-zero memory contention across the environment, with only **13 VMs** ever exceeding 1% contention at their worst point.]


#### Balloon

Balloon is an application (kernel driver to be precise) running inside the Guest OS, but it can take instruction from the kernel to inflate/deflate.
When it receives an instruction to inflate, it asks the Guest OS to allocate memory to it. This memory in the Guest OS is not backed up by physical memory in ESXi, hence it is available for other VMs. When ESXi is no longer under memory pressure, it will notify the Balloon to release its requested page inside Guest OS. This is a proactive mechanism to reduce the chance of the Guest OS doing paging. Balloon will release the page inside the Guest OS. The Balloon counter for the VM will come down to 0.
It is the Guest OS that initiates memory reallocation. Therefore, it is possible to have a balloon target value of 0 and present balloon value greater than 0. The counter Balloon Target tracks this target, so if you see a nonzero value in this counter, it means that the hypervisor has asked this VM to give back memory via the VM balloon driver.
Just because Balloon asks for 1 GB of RAM, does not mean ESXi gets 1 GB of RAM to be freed. It can be less if there is TPS.
Guest OS will start allocating from the Free Pages. If insufficient, it will take from Cache, then Modified, then In Use.
To use ballooning, Guest OS must be configured with sufficient swap space.
How much will be asked depends on Idle Memory Tax. I do not recommend playing with this setting.

##### Performance Impact

Balloon by itself does not cause performance problem. What will cause performance is when the ballooned page is requested by Windows or Linux. The following shows a VM that is heavily ballooned as limit was imposed on it. Notice the actual performance happens rarely.

[Image: The image shows two VMware memory metrics for a production VM over a week-long period (March 12–19): **Memory Balloon (%)** ranging from a low of 2.44% to a high of 32.65%, displaying consistently high, volatile balloon activity throughout the period; and **Memory Contention (%)** ranging from 0 to a peak of 0.95%, showing mostly near-zero values with only rare, brief spikes. This demonstrates the text's key point that heavy ballooning itself does not continuously cause performance problems — the Contention metric (which reflects actual performance impact) spikes only occasionally despite persistent high balloon values. The contrast between the continuously active balloon graph and the nearly flat contention graph visually validates the claim that "actual performance happens rarely" even under sustained ballooning conditions.]

The higher the value is for balloon, swapped, and compressed, the higher the chance of a performance hit happening in the future if the data is requested. The severity of the impact depends on the VM memory shares, reservation, and limit. It also depends upon the size of the VM's configured RAM. A 10-MB ballooning will likely have more impact on a VM with 4 GB of RAM than on one with 512 GB.
How high?
Let’s take a VM and plot its value over time. The VM is configured with 16 GB memory. As you can see, the value in the last 4 weeks is a constant 16 GB.

[Image: ## Image Description

The chart displays **Memory|Total Capacity (MB)** for a VM over approximately 3 weeks (September 12 – October 2), showing a **perfectly flat line at 16,384 MB** throughout the entire period. Both the Highest (H) and Lowest (L) values are identical at **16,384 MB**, confirming zero variance. This demonstrates that the VM's total configured memory remained completely constant at 16 GB, providing the baseline reference against which the 63.66% ballooning (10,430 MB reclaimed) discussed in the surrounding text can be contextualized.]

The line is a perfect flat. Both the Highest value and Lowest value show 16,384 MB.
The VM was heavily ballooned. 63.66% of its memory was reclaimed. That’s a whopping 10,430 MB!

[Image: ## Image Description

The chart displays the **Memory|Balloon (%)** metric for a VM over approximately 3 weeks (September 12 – October 2), showing a **perfectly flat line at a constant 63.66%**. Both the High (H) and Low (L) values are identical at **63.66%**, indicating zero variation across the entire period. This demonstrates the surrounding text's point that the VM's balloon driver reclaimed ~63.66% of its 16 GB RAM (~10,430 MB) and **never changed**, confirming the Guest OS was inactive and never needed to reclaim those ballooned pages.]

Notice something strange.
The Ballooned did not change at all for 4 weeks.
That likely means the Guest OS is not active. It never needs any of those 10+ GB that was ballooned out.
So Guest was playing with the remaining 6 GB. It never page in those pages.
So what do you expect if we plot Granted + Swapped + Compressed?
You got it. A flat line.

[Image: ## Image Description

The chart displays three VMware memory metrics for a MySQL VM over approximately 3 weeks (Sep 11 – Oct 2): **Memory Granted (3,131,119 KB ~3M)**, **Memory Swapped (2,947,087.75 KB ~3M)**, and **Memory Compressed (55,782.67 KB)**. The teal/green area (Granted) and pink area (Swapped) both remain as **nearly flat horizontal bands around the 3M KB mark** throughout the entire period, with minimal variation. This demonstrates the author's point that plotting Granted + Swapped + Compressed produces an essentially flat line, confirming the Guest OS was inactive and never paged back the ballooned memory over the 4-week observation window.]


##### Capacity Impact

Balloon is a memory request from ESXi. So it’s not part of the application. It should not be included in the Guest OS sizing, hence it’s not part of reclamation.
Balloon impacts the accuracy of Guest OS sizing. However, there is no way to measure it.
When Balloon driver asks for pages, Guest OS will allocate, resulting in In Use to go up. This is because the balloon driver is treated like any other processes.
If the balloon driver page comes from Free, then we need to deduct it from In Use.
If the page comes from In Use, then it gets tricky as the value of In Use does not change. The Guest OS pages out, so we need to add Page Out or Cache.

#### Swap + Compress

Swap and Compress go hand in hand as the block that cannot be compressed go into swapped. The size of a memory page or block is only 4 KB. When the compression does not result in savings below 2 KB, then it makes no sense to compressed and the page is moved to swapped file.
There are 2 levels of compression (4:1 and 2:1), so a 4 KB page may end up as 1 KB or 2 KB. The reason there is no 3:1 compression
If the compression result is less than that, the page will be swapped instead as that’s a cheaper operation. So it’s completely possible to have 0 swapped as all the pages were compressed instead.
Large page (2 MB) is not compressed directly. Instead, it will be split into 4 KB page first.
The following screenshot shows how the 2 counters moved in tandem.

[Image: ## Image Description

The image displays two time-series charts for a VM named **hnr-vs-8Zdo** covering November 30 – December 15, showing **Memory|Compressed (GB)** (ranging from ~19.06 GB dropping to ~17.52 GB) and **Memory|Swapped (GB)** (ranging from ~130.50 GB dropping to ~123.79 GB). Both metrics exhibit an identical sharp decline around **December 7-8**, after which they stabilize at lower values. This demonstrates the **tandem movement** of compressed and swapped memory counters referenced in the text — when memory pressure was relieved, both compression and swap usage decreased simultaneously and proportionally.]

The above are the main metrics that you should track. vSphere provides additional visibility as swap and compress are complex process.

##### Transition

Read the following carefully, as there will be a quiz after this.

| Input | This is the number of pages that will be subjected to compression and swapping.  It’s not the number of pages that was processed already.  The metric is called Swap Target. Think of it as Compress-Swap Target as the page that cannot be compressed is swapped. |
| --- | --- |
| Process | You need metrics to track the progress as it’s happening. This complements the result as it covers how much memory is compressed or swapped at any given period.  A 10 MB compressed in 1 second is different to 10 KB compressed over 1000 seconds. Both results in the same amount, but the problem is different. One is an acute but short fever; the other is low grade but persistent fever. You don’t want neither, but good to know what exactly you’re dealing with. This is the rate of  compression decompression swapping from DIMM into the swap file. swapping from the swap file into the DIMM The In and Out can happen at the same, as they typically involve different pages. You can have 10 MB being decompressed and another 10 MB being compressed. Your swap file size is unchanged but the content has changed. This is why Swapped is not Swapped In – Swapped Out.  Swap-out does not mean there is contention. If you are lucky, the page being swapped is not required. However, swap out means the ESXi was under memory pressure or the VM hit a limit. Swap-in means there is contention. The page was called for, hence it was brought in. Plot them together and you will see a high correlation. Swap-in doesn't happen because there's memory pressure on the host. Swap-in just means there was memory pressure in the past and now the guest OS wants some of that data. |
| Output | You need a metric to track the result and the savings.  For swap, 3 counters are provided Swapped  Swapped Out Swapped In For compress, the compressed-in and compressed-out are not provided. You do get the savings from compression. |


###### Example


[Image: ## Image Description

The image displays three time-series charts for **CP4** on **Thursday, Nov 28**, covering approximately 9:00 AM to 11:00 PM:

1. **Memory|Swap Out Rate (KBps)**: Shows near-zero activity until ~5:30 PM, where two sharp spikes occur, with a highlighted value of **5,026.4 KBps** at 05:36:34 PM, and a smaller spike near 8:00 PM.

2. **Memory|Consumed (MB)**: Starts at **~7,718.91 MB**, remains stable until ~5:00 PM, then drops sharply to approximately **2,850.68 MB**, stabilizing at that lower level — a reduction of ~4,868 MB.

3. **Memory|Swapped (KB)**: Remains at zero until ~5:15 PM, then rapidly increases to plateau at approximately **4,156,976 KB (~4,057 MB)**, with a tooltip showing **1,899,628 KB** at 05:21:30 PM.

These charts collectively demonstrate the **correlation between swap-out activity and memory pressure**: as the host swapped out ~4,057 MB of memory, Consumed memory dropped correspondingly, confirming that swap-out directly reduced]

Swapped Out Rate was 6331.93	+ 5026.4 + 1882.13 + 615.86. This gives a total of 13856. Since it’s sustained for 300 seconds, we multiply by 300 and then divide by 1024 to get the total of 4059 MB being swapped out. This is pretty close to the 4157 MB of Swapped.
There is no Swap In. The rate metric was showing 0 during the entire period.
Consumed drops by 4868 MB (7719 – 2851). There were other factors impacting it.

##### Quiz

Explain why swap and compress move in opposite direction in the following chart.
This VM is configured with 64 GB of memory. So it experienced high amount of swapping and compressed in the last 7 days. It peaked at 20 GB, which is really bad.

[Image: ## Image Description

The image displays two time-series charts for the VM **ora-uat1-ebs-r2** spanning **January 8–14**:

1. **Memory|Compressed (GB)**: Shows near-zero baseline (~0.00012 GB) with frequent sharp spikes peaking at **5.29 GB**, occurring roughly daily.
2. **Memory|Swapped (GB)**: Shows an inverse relationship, hovering around **14.73 GB** with sharp **downward** dips toward **10.17 GB** — notably the lowest dip occurs around January 9–10.

The charts visually demonstrate the **inverse/opposing relationship** between compression and swapping — when swapped memory drops (pages being swapped in or reclaimed), compressed memory spikes upward, illustrating how the hypervisor alternates between these two memory reclamation techniques as the VM operates under memory pressure.]

Let’s plot consumed and granted. What’s your conclusion?

[Image: The image shows two charts for VM **ora-uat1-ebs-r2** spanning January 8–14: **Memory|Consumed (GB)** (top) hovering nearly flat at ~40 GB with occasional sharp dips to ~34.55 GB, and **Memory|Granted (GB)** (bottom) fluctuating between ~40.5–44.04 GB with more visible variability. This illustrates the text's point that Consumed is artificially capped flat by a memory **Limit**, while Granted shows normal movement above Consumed, with the small gap representing hypervisor overhead.]

Why is consumed basically flat for 7 days?
Granted looks rather normal as it hovers above consumed, with some movement.
If you guess Limit, you’re right! Let’s plot all the counters together now.

[Image: ## Image Description

The chart displays six memory metrics for **ora-uat1-ebs-r2** from Jan 8–14, with a tooltip highlighting Jan 13, 3:00–3:29 PM values: **Granted: 42.73 GB**, **Effective Limit: 40.44 GB**, **Consumed: 39.58 GB**, **Swapped: 12.19 GB**, **Shared: 3.97 GB**, and **Compressed: 2.6 GB**. The key observation is that **Consumed remains nearly flat** (dark navy line) just below the Effective Limit line (cyan), confirming that a memory **limit is capping consumption** rather than actual workload behavior. This demonstrates how a configured memory limit forces the hypervisor into repeated swap/compress cycles despite granted memory being available above the limit.]

Because of Limit, Consumed can’t go above it. The tiny gap is the hypervisor overhead for this VM.
Now, because Guest OS is actively using pages, this results in movement in both directions. Some pages are brought in from swapped files. To make space, other pages are subjected to compression & swap decision.

##### Balloon

Compressed and Swapped are different from ballooning, as the hypervisor has no knowledge of the free memory inside the Guest OS. It will randomly compress or swap. As a result, any value in this counter indicates that the host is unable to satisfy the VM memory requirement. This can have potential impact on performance.
It is possible to have balloon showing a zero value while compressed or swapped are showing nonzero values—even though in the order of ESXi memory reclamation techniques, ballooning occurs before compression. This indicates that the VM did have memory pressure in the past that caused ballooning, compression, and swapping then, but it no longer has the memory pressure. These events could have happened at different time. Data that was compressed or swapped out is not retrieved unless requested, because doing so takes CPU cycles. The balloon driver, on the other hand, will be proactively deflated when memory pressure is relieved.

#### Limit

Does limit result in Balloon?
The answer is no. Why not?
Go back to the 4 layers of memory. They are at different level on memory management. Limit results in swapped or compressed.
Let’s take an example with a VM that is configured with 16 GB RAM. This is a My SQL database running on RHEL. You can see in the last 7 days, it’s using around 13.4 GB and increasing to 13.6 GB.

[Image: ## Image Description

The chart displays **Guest|Needed Memory (GB)** for a VM over approximately 7 days (Sep 26 – Oct 3), showing values ranging from a low of **13.403 GB** to a high of **13.63 GB**, with the metric hovering consistently around **13.4–13.5 GB** throughout the period. The data represents the Guest OS's actual memory demand from a MySQL/RHEL VM configured with 16 GB RAM, demonstrating that the workload requires roughly **13.4–13.6 GB** of memory. This establishes the baseline of genuine memory need before a **2 GB limit** is applied, which will subsequently prevent the VM from receiving the memory it actually requires.]

It’s given a bad limit of 2 GB.
In the last 7 days, we can see the limit is a perfectly flat line. It’s 2.12 GB as it includes the overhead value.

[Image: The chart displays the **Memory Effective Limit** metric for a MySQL VM (`mysql-2`) over a 7-day period (Sep 26 – Oct 3), showing a perfectly flat line at **2.12 GB** (High and Low both equal 2.12 GB). This constant value represents the configured memory limit of 2 GB plus overhead (~0.12 GB). The flat line visually confirms that the effective memory limit remained unchanged throughout the observation period, illustrating how an artificially low limit constrains the VM regardless of its actual memory demand.]

The VM, or rather the Guest OS, did ask for more. You can see the demand by looking at the Granted or Compressed or Swapped metrics. I’m only showing Granted here:

[Image: ## Memory|Granted (GB) Chart

The chart displays the **Memory Granted** metric (in GB) over a 7-day period from September 26 to October 3, with a high of **2.9617 GB** and a low of **2.7862 GB**. The metric fluctuates between approximately **2.78–2.96 GB**, consistently hovering in that range throughout the period. This demonstrates that despite a 2 GB limit being imposed, the Guest OS was continuously requesting more memory than allowed, as evidenced by the Granted value persistently exceeding 2 GB — confirming the VM's demand was constrained by the limit.]

Because of the limit, the Consumed counter did not past the 2 GB. It’s constantly hovering near it as the VM is asking more than that.

[Image: ## Image Description

This chart displays **Memory|Consumed (GB)** over a 7-day period (Sep 26 – Oct 3), showing values oscillating between a **high of ~1.9999 GB** and a **low of 1.84 GB**, with the metric consistently hovering near the **2 GB limit**. The line remains densely packed near the 2 GB ceiling with periodic sharp dips, but never exceeds it. This demonstrates that the configured **memory limit of 2 GB** is actively constraining consumption — the VM continuously demands more memory but is capped, causing the metric to persistently press against the limit rather than exhibiting natural usage patterns.]

What do you expect to see the Balloon value?
If Balloon has something to do with it, it would not stay a perfectly flat line.
But this is what you got. A perfectly flat line, proving Limit had nothing to do with Balloon.

[Image: The chart displays the **Memory|Balloon (%)** metric for the VM **oauth-stage-mysql-2** over the period of **Sep 26 – Oct 3**, showing a perfectly flat line at a constant value of **63.66%** (both High and Low values are identical at 63.66). This flat, unchanging line demonstrates that the Balloon driver remained completely static throughout the observation period, providing evidence that the memory **Limit** applied to the VM had no relationship to ballooning activity. The image supports the author's argument that memory limits do not trigger ballooning — if they did, the line would fluctuate rather than remain perfectly constant.]


### Consumption Metrics


[Image: ## Image Description

This diagram illustrates the **virtual vs. physical memory view** of a single VM in VMware ESXi, showing how configured memory is divided across multiple memory states: **Granted** (shared, zero, and active pages), **Before Zip/Swap Target** (compressed), **Swapped**, **Host Cache**, **Ballooned** (yellow), and **Free**, plus a **Overhead** region. The physical view beneath shows how virtual memory pages map down to actual consumed, swapped, and host cache physical memory, with shared pages consolidating to fewer physical blocks. This diagram contextualizes the consumption metrics table that follows by visually distinguishing **Granted** (active physical-backed pages minus ballooned/swapped/compressed) from other memory states, and explains why **Balloon** operates independently from memory **Limit** enforcement.]


| Configured | What the Guest OS can see is what is configured by vSphere.  Guest OS can’t see the hypervisor memory overhead. |
| --- | --- |
| Granted | This is page granted to the VM, minus Ballooned, Swapped, Compressed, and swapped to host cache.  Take note of the process of transitioning during swap. During this process, the value of granted includes them |
| Shared | The number of memory pages that are pointing to the same underlying block. Many of these pages are likely the 0000 page. |
| Compressed | These 2 are mutually exclusive and go together. What can’t be compressed will be swapped. Compressed is preferred as unzipping memory from DRAM is faster than bringing it from SSD disk. Notice Windows even compressed its In Use pages. Compressed is the output (result of compression), not the input (memory subjected to compressed as that contains swapped also) |
| Swapped | These 2 are mutually exclusive and go together. What can’t be compressed will be swapped. Compressed is preferred as unzipping memory from DRAM is faster than bringing it from SSD disk. Notice Windows even compressed its In Use pages. Compressed is the output (result of compression), not the input (memory subjected to compressed as that contains swapped also) |
| Entitlement | = Granted + Overhead.  Overhead is mostly negligible, as it’s just storing metadata or index information required by virtualization, such as the shadow page tables. Overhead value goes up as you configure more vCPUs and memory. My guess is this excludes limit as you’re not entitled beyond the limit. |
| Ballooned | The page was reclaimed by the balloon driver. It has not been asked back by the Guest OS, hence it’s just seating there collecting pixie dust. I colored the box yellow as that’s not a good (green) situation. The bigger the balloon size, the higher the chance a page will be required in the future. |
| Overhead | Virtualization overhead is operationally negligible. |
| “Free” | The VM never touches or uses the page since it’s powered on.  After a while, as Guest OS starts paging in and out, this value will grow to near 0. |


#### Granted

Granted and Consumed are not similar. The former looks at from consumer layer, while the later looks from provider layer.
The formula is
Granted = normal page + shared page + zero page + being swapped-in + tiered page
Normal page is single pages being backed by physical DIMM. This metric is not exposed on its own.
Being swapped in means a staging stage between unmapped and normal. Once the transition is complete, it becomes a normal page.
Tiered is the memory tiering. Unlike swapped, memory tiering is “in-line” hence it is considered as part of granted.
Granted does not care about page savings at physical layer its vantage point is the VM, not ESXi. The following shows Granted is perfectly flat. Consumed goes down as the amount of shared page goes up.

[Image: The image shows three time-series charts for host **sbi-qa3-d3-LYPt** between 2:20 PM and 3:15 PM, tracking **Memory|Granted** (flat at 1,475.67 GB), **Memory|Consumed** (declining from 642.68 GB to 630.3 GB), and **Memory|Shared** (increasing from 839.75 GB to 851.45 GB). This visually demonstrates the key concept described in the surrounding text: **Granted remains perfectly flat** while Consumed decreases inversely as Shared memory increases, proving that Granted reflects the VM's perspective and is unaffected by physical-layer page savings such as memory sharing. The inverse relationship between Consumed and Shared confirms that as more pages are deduplicated/shared, the host reclaims physical memory, reducing Consumed without impacting Granted.]

The same vantage point reason is why Limit impacts Consumed, but not Granted. The following is VM is a Windows 2016 server, configured with 12 GB of RAM, but was limited to 8 GB. Limit is shown as the flat line in cyan near the bottom, hovering just above the pink line).

[Image: ## Image Description

The chart displays four memory metrics for a VM configured with 12 GB RAM but limited to 8 GB, captured over approximately 13 hours (8 PM to 9 AM). **Memory|Granted (KB) peaks at ~12,188,907 KB** (purple fluctuating line), significantly exceeding the **Memory|Effective limit of 8,488,260 KB** (cyan flat line near bottom), while **Memory|Consumed (KB) at 8,385,908.5 KB** remains consistently **below the limit**, and **Total Capacity stays flat at 12,582,912 KB** (dark blue top line). This demonstrates the key concept that **Limit constrains Consumed but not Granted** — Granted freely fluctuates above the configured 8 GB limit, approaching the full 12 GB configured memory.]

The purple line jumping up and down is Granted. Granted ignores the limit completely and runs way above it.
Notice Consumed (KB) is consistently below Limit. Granted does not exceed 12 GB as it does not exceed configured.

##### Compressed + Swapped

Granted does not include Compressed + Swapped because the page is no longer directly accessible without some extra processing.
The following shows Granted move up while the other 2 metrics went down.

[Image: ## Image Description

The image displays three time-series charts for VM **hnr-vs-8Zdo** spanning from ~9:30 PM (Dec 25) to ~9:30 AM (Dec 26), showing **Memory|Compressed (GB)** declining from 17.447 to 17.4434, **Memory|Swapped (GB)** declining from 123.4397 to 123.426, and **Memory|Granted (GB)** increasing from 266.751 to 266.769. This inverse relationship directly illustrates the surrounding text's assertion that **Granted moves up while Compressed and Swapped go down**, since as memory pressure recedes (less compression/swapping needed), more memory becomes directly accessible and is reflected in the Granted metric. The correlated step-changes visible around 2:00 AM and 8:00 AM across all three charts confirm that Granted excludes Compressed and Swapped pages because they require additional processing before access.]

Summing up the above resulted in a delta of 0.7 MB.

##### Ballooned

Balloon driver removes page from the granted list. Granted does not include ballooned as the page is not functionally used. Technically, Guest OS memory counters include it so don’t forget to exclude it when working out the Guest OS utilization.

[Image: ## Image Description

The chart displays three VMware vSphere memory metrics for **uni-cp-in-vc1** over time on November 29 (midnight to ~09:00 AM): **Memory|Balloon (KB)**, **Memory|Granted (KB)**, and **Memory|Zero (KB)**. At approximately **02:00 AM**, a significant memory event occurs: Balloon drops sharply from ~21M KB to near zero, Granted drops from ~18M KB to ~10.8M KB, and Zero simultaneously spikes then stabilizes near zero. At the tooltip timestamp **06:32:22 AM**, values show Balloon at **21,361,328 KB**, Granted at **10,815,756 KB**, and Zero at **497,963.72 KB**. This demonstrates the balloon driver's behavior described in the surrounding text — as ballooning increases, Granted memory decreases because ballooned pages are excluded from the Granted counter, confirming that Granted does not include ballooned memory.]


#### Shared

Shared counts the amount subjected to sharing. It does not count the actual savings post sharing.
There are 2 types of sharing that can happen to a page:

| Intra-VM sharing | sharing within the same VM. By default, each page is 4 KB. If Guest OS uses the Large Page, then it’s 2 MB. The chance of sharing in 4 KB page is logically much higher than in 2 MB. |
| --- | --- |
| Inter-VM sharing | Due to security concern, this is by default disabled in vSphere |
| Inter-VM sharing | For accounting purpose, the Shared page is counted in full for each VM. This means if you sum the number from all VMs you’re going to get inflated value at the ESXi level |

Example:
- VM 001 has 1 GB private.
- The 100 MB is the amount that is being shared internally within the VM. If not shared, they would consume 100 MB.
- There is additional 10 MB that is subjected to sharing with other VMs. It could be shared with 1 VM or many VM; it does not matter as far this VM 001 concern. The Shared counter merely counts that this 10 MB is being shared.
Using the above, the shared page for VM 001 is 110 MB.

##### Savings

The calculation has to be done on each block that points to the same destination page. For example, if there are 10 pages pointing to the same physical DIMM, then the savings is 9 pages worth of memory.
The above process is repeated for all the shared page.
The result is some savings. But how much savings?
Here is a summary from 7500 VMs.

[Image: The table displays memory metrics (Granted, Shared, and Consumed) for 7,505 VMs, showing four individual vPodRouter VMs with memory values in the 223-226 MB granted range, alongside aggregate Average (14.09 GB granted, 4.07 GB shared, 10.86 GB consumed) and Sum (103.26 TB granted, 29.83 TB shared, 79.56 TB consumed) rows. The data demonstrates VMware's Transparent Page Sharing (TPS) savings at scale, where the difference between total Granted (103.26 TB) and Consumed (79.56 TB) memory, adjusted against Shared (29.83 TB), reveals approximately 6.13 TB of actual memory savings (~6%) across the environment.]

Review the last row. What are the total savings?
Granted – Consumed = (103.26 – 79.56) = 23.7 TB
Savings = 29.83 TB – 23.7 TB = 6.13 TB.
That’s around 6% saving.
Profile your own environment. What savings do you get?
Savings does not include compressed as that is not true saving. Zipped results in performance impact, while saving should not.

##### Zero

A commonly shared page is certainly the zero page. A common technique to initialize space is to simply write 0.
The following screenshot shows the 2 moved in tandem over several days.

[Image: ## Image Description

The image displays two time-series charts for **vRealize_Operations_Appliance-6arg** spanning **March 17–22**, showing **Memory|Zero (GB)** (top, ranging ~61–63 GB) and **Memory|Shared (GB)** (bottom, ranging ~65–75 GB). Both metrics exhibit **nearly identical patterns** — with a notable spike around **March 19 12:00 PM** and a secondary peak near **March 19–20** — with orange dots marking specific data points of interest. This demonstrates the tight correlation between Zero and Shared memory metrics, supporting the surrounding text's assertion that zero pages (memory initialized to 0) represent a significant component of shared memory savings in ESXi's memory management.]


#### Consumed

The formula is Granted – Savings.
Consumes tracks the ESXi Memory mapped to the VM. ESXi assigns large pages (2 MB) to VM whenever possible; it does this even if the Guest OS doesn’t request them. The use of large pages can significantly reduce TLB misses, improving the performance of most workloads, especially those with large active memory working sets. The drawback is VM consumes more memory than what Guest OS does.
Consumed does not include overhead memory, although this number is practically negligible. Think of the word consume as delivering benefit to the VM. Since overhead is transparent to Guest OS, it’s excluded.
Consumed does not include swapped memory, for the same reason above. The swapped pages are not readily available for use. As for compressed, I’m unsure if it includes the portion that is the DIMM. It does not include the portion that was subjected to compression. For example, a 4 KB page was compressed to 1 KB. The 0.75 KB is not in Consumed as it’s no longer in the DIMM.
Consumed includes memory that might be reserved.
Do not use the metric Guest \ Memory Usage. That’s the same as Consumed.

##### Guest OS

When a Guest OS frees up a memory page, it normally just updates its list of free memory, it does not actually update the content. This list is not exposed to the hypervisor, and so the physical page remains claimed by the VM. This is why the Consumed is higher than the Guest OS In Use, and it remains high when the Active counter has long dropped.
Consumed and Guest OS In Use are not related, as they are independently managed. Here is a screenshot comparing Windows 10 Task Manager memory metrics with VCF Operations Memory \ Non Zero Active (KB) and Memory \ Consumed (KB). As you can see, none of the metrics match.

[Image: ## Image Description

The image compares **Windows 10 Task Manager memory metrics** (left panel showing 4.0 GB total, 2.2 GB in use with 192 MB compressed, 1.8 GB available) against **VCF Operations metrics** (right panel) showing **Memory|Consumed = 4,194,304 KB (~4 GB)** and **Memory|Non Zero Active = 1,512,743.5 KB (~1.48 GB)** at a specific timestamp (Wednesday, Dec 19, 06:06:45 PM). The right panel's pink trend line shows highly volatile Non Zero Active memory fluctuating between ~0.5M–2.5M KB, while Consumed (purple line) remains flat near 4M KB. This demonstrates that **none of the three metrics align with each other** — Windows reports ~2.2 GB in use, vSphere Consumed reports the full ~4 GB, and Non Zero Active reports ~1.48 GB — illustrating that these counters are independently managed and measure fundamentally different things.]

When you see Consumed is lower than Guest OS Used, check if there are plenty of shared pages. Consumed does not include shared page.
The following screenshot shows Guest OS Used consistently higher. It’s also constant, around 156 GB throughout. Consumed was relatively more volatile, but never exceed 131 GB. The reason for it is Shared. Notice the value of page with all 0 is high, around 61 – 63 GB.

[Image: ## Image Description

The image displays three time-series charts for **vRealize_Operations_Appliance-6arg** spanning **March 17–21**, showing: **Memory|Consumed** (H: 130.77 GB, L: 119.26 GB), **Memory|Zero** (H: 63.2 GB, L: 61.38 GB), and **Guest|Used Memory** (H: 156.2929 GB, L: 156.2394 GB).

The charts demonstrate why **Guest OS Used (156 GB) consistently exceeds Consumed (~120–131 GB)** — the gap (~25–35 GB) is explained by the high **Zero page memory (61–63 GB)**, which represents shared all-zero pages that are deduplicated and therefore **not counted in Consumed**.

This illustrates the key concept that **Consumed excludes shared/zero pages**, making it appear significantly lower than Guest OS Used despite the VM actively referencing that memory.]


##### Ballooned

This 64-bit CentOS VM runs My SQL and is configured with 8 GB of RAM.
Linux was heavily ballooned out (default limit is around 63%). Why is that so?

[Image: ## Memory|Balloon (%) Chart Description

The chart displays the **Memory Balloon percentage** metric for a CentOS VM over a ~24-hour period (Feb 10 12:00 PM – Feb 11 12:00 PM), showing a **high (H: 63.35%)** and **low (L: 57.61%)** value. The metric remains nearly constant at ~63% throughout the entire period, with a **single sharp dip to ~57.61%** occurring around **9:00–9:30 PM**. This visualization demonstrates the heavy, sustained ballooning caused by the 2 GB memory limit imposed on the 8 GB VM, with the brief dip representing the ~0.46 GB balloon drop referenced in the surrounding text indicating a moment of Guest OS activity.]

The answer for this VM is we set a limit to 2 GB. As a result, Consumed could not exceed 2 GB. Since the VM needed more, it experienced heavy ballooning.

[Image: ## Image Description

The chart displays **Memory Consumed (GB)** for a MySQL VM over approximately 24 hours (Feb 10 12:00 PM to Feb 11 12:00 PM), showing values ranging from a **high of 2.09 GB** to a **low of 1.603 GB**. A sharp spike and immediate drop is visible around **9:00–9:30 PM**, where consumption briefly reached 2.09 GB then fell abruptly to 1.603 GB before gradually climbing back toward ~1.75–2.0 GB. This demonstrates the anomalous memory consumption dip referenced in the surrounding text, where Consumed dropped ~0.46 GB over ~20 minutes despite a constant 2 GB limit, consistent with Guest OS balloon driver activity temporarily releasing memory.]

Did you notice the common deep in Balloon and Consumed?
Can you explain them?
Balloon dropped by 0.46 GB then went back to its limit again. This indicated Guest OS was active.
Consumed went down from 2.09 GB to 1.6 GB, and then slowly going back up. Why did it suddenly consume 0.4 GB less in the span of 20 minutes? Both the configured limit and the runtime limit did not change. They were constant at 2 GB. This makes sense, else the Consumed would not be able to slowly go up again.

[Image: ## Memory | Effective Limit (GB) Chart

The chart displays the **Memory Effective Limit metric remaining completely flat at 2.07 GB** across the entire time range (Wednesday Feb 10, 12:00 PM through Feb 11, 12:00 PM), with both High (H) and Low (L) values identical at **2.07 GB**. The tooltip confirms the value at 09:28:57 PM is exactly 2.07 GB. This constant, unchanging line demonstrates that the runtime effective memory limit remained stable throughout the observation period, which is referenced in the surrounding text to explain why Consumed memory could temporarily dip and then gradually recover — the ceiling never changed, so the VM retained the headroom to reclaim memory back up to the limit.]

There must be activity by the VM and pages were compressed to make room for the newly requested pages. The Non Zero Active counter shows that there are activities.

[Image: The chart displays the **Memory|Non Zero Active (GB)** metric over a ~24-hour period (Feb 10–11), with a high of **2.43 GB** and a low of **0.08 GB**. A sharp spike to **2.43 GB** occurs at **09:23:57 PM on Feb 10**, with values otherwise remaining relatively flat near baseline. This spike in Non Zero Active memory confirms VM page activity during the period when Consumed memory dropped, indicating that the guest OS (Windows/Linux) was actively accessing/modifying memory pages, triggering compression of less-active pages to accommodate new requests.]

The pages that are not used must be compressed or swapped. The Swapped value is negligible, but the Compressed metric shows the matching spike.

[Image: The chart displays **Memory|Compressed (GB)** for a VM over approximately 24 hours (Feb 10–11), with a high of **0.675 GB** and a low of **0.000011 GB**. A sharp spike to 0.675 GB occurs around **09:23 PM on Feb 10**, followed by a sustained plateau near 0.5 GB before dropping to ~0.1 GB around 08:00 AM on Feb 11. This demonstrates the memory compression event referenced in the surrounding text — when the VM's Consumed memory reached capacity, ESXi compressed existing pages (~0.675 GB compressed) to accommodate newly requested pages, confirming that compression (not swapping) was the primary balloon mechanism during that period.]

So far so good. Windows or Linux were active (2.4 GB in 5 minute at the highest point, but some pages were probably part of Consumed). Since Consumed was at 100%, some pages were moved out to accommodate new pages. The compression resulted in 0.6 GB, hence the uncompressed amount was in between 2x and 4x.
Consumed dropped by 0.4 GB as that’s the gap between what was added (new pages) and what was removed (existing pages).

##### Limit

Consumed is affected by Limit. The following is a VM configured with 8 GB RAM but was limited to 2 GB.

[Image: The image shows three time-series charts for a SQL VM over approximately 6 PM–11:30 PM, displaying **Memory Effective Limit (H/L: 2.07 GB)**, **Memory Total Capacity (H/L: 8 GB)**, and **Memory Consumed (H: 2.09 GB, L: 1.603 GB)**. This demonstrates the effect of a **2 GB memory limit applied to a VM configured with 8 GB RAM** — the Effective Limit is capped at ~2.07 GB despite 8 GB total capacity. The Consumed metric shows a notable spike to ~2.09 GB around 9:15 PM followed by a sharp drop to ~1.603 GB, illustrating how the limit constrains and forces memory reclamation when consumption approaches the ceiling.]


##### Total

Consumed may reach but not exceed the configured memory. Both total and consumed do not include the virtualization overhead memory.

[Image: ## Image Description

The image shows three time-series charts for a VM named **LI_3_node_L** over approximately 24 hours (Oct 13 ~6PM to Oct 14 ~8PM), displaying **Memory|Consumed** (ranging from ~31.9726 GB to ~31.996 GB), **Memory|Total Capacity** (flat at **32 GB**), and **Memory|Overhead** (fluctuating narrowly around **0.16 GB**). The Consumed chart shows two step increases — a small rise around 8PM and a larger jump near 12PM Oct 14 — demonstrating that Consumed approaches but does not exceed the 32 GB configured memory. This supports the surrounding text's statement that **Consumed may reach but not exceed configured memory**, and that Total Capacity and Consumed do not include virtualization overhead (shown separately in the third chart).]


#### Active

This is a widely misunderstood counter. ESXi calls this Touch as it better represents the purpose of the metric. Note that vCenter still calls it Active, so I will call it Active.
This counter is often used to determine the VM utilization, which is not what it was designed for. To know why, we need to go back to fundamental. Let’s look at the word active. It is an English word that needs to be quantified before we can use it as metric. There are 2 dimensions to consider before we apply it:
- Definition of active. In RAM context, this means read or write activity. This is similar to disk IOPS. The more read/sec or write/sec to a page, the more active that page is. Note that the same page can be read/written to many times in a second. Because a page may be accessed multiple times, the actual active pages could be lower. Example: a VM do 100 reads and 100 writes on its memory. However, 50 of the writes are on the page that were read. In addition, there are 10 pages that were read multiple times. Because of these 2 factors, the total active pages are far fewer than 300 pages. If the page is average 4 KB, then the total active is way less than 1200 KB.
- Active is time bound. Last week is certainly not active. Is 300 seconds ago active? What exactly, is recent? 1 second can be defended as a good definition of recent. Windows shows memory utilization in 1 second interval. IOPS is always measured per second, hence the name IOPS. So I think 1 second seems like a good definition of recent.
Applying the above understanding, the active counter is actually a rate, not a space. However, the counter reported by vCenter is in KB, not KB/s.
To translate from KB/s to KB, we need to aggregate based on the sampling period. Assuming ESXi samples every 2 seconds, vCenter will have 10 sampling in its 20 second reporting period. The 10 samplings can be sampling the same identical pages, or completely different ones. So in the 20 seconds period, the active memory can be as small as 1 sampling, or as large as 10 samplings.
Examples:
- First 2 seconds: 100 MB Active
- Next 2 seconds: 150 MB Active
In the above 4 seconds, the active page ranges from 150 MB to 250 MB.
Each sampling is done independently, meaning you could be sampling the same block again. But the value is then averaged it with previous samples. Because sampling and averaging takes time, Active won't be exact, but becomes more accurate over time to approximate the amount of active memory for the VM. This is why there is actually a longer version of Active, which you will see in esxtop (it is not available in vSphere Client).
VM Active is typically different from Guest OS working set estimate. Sometimes the difference may be big, because Guest OS and the kernel use different working set estimate algorithm. Also, VM has a different view of active memory, due to ballooning and host swapping. Logically, ballooned memory is considered inactive, so, it is excluded from the sampling. Active is unaware of locked and large pages.
Reference: Active Memory by Mark Achtemichuk.

##### Consumed vs Active

I hope the explanation on Consumed and Active convince you that they serve different purpose. They are not calculated in a similar manner, and are not simply differ based on aggressive vs conservative.
Both Active and Consumed are not suitable for sizing the Guest OS. They are VM level metrics, with little correlation to the Guest OS memory usage.

###### Example 1

The following test shows Active going down while Consumed going up.

[Image: ## Image Description

The image shows a VMware vCenter real-time memory performance chart for a VM named "WindowsTest" over a ~1-hour window (11/06/2018, 10:40–11:39 AM), plotting two metrics: **Active Memory** (blue line) and **Consumed Memory** (black line). The Active memory starts high (~15M KB), drops sharply to near zero around 11:00 AM, then spikes again to ~5M KB around 11:30 AM, while Consumed memory rises steadily from ~9M KB to ~14.4M KB throughout the period. This directly demonstrates the book's claim that **Active and Consumed are inversely correlated** in this scenario — as Active memory drops dramatically (latest: 1,006,632 KB, max: 15,602,808 KB), Consumed continues to climb (latest: 14,462,304 KB, max: 14,464,392 KB), proving they measure fundamentally different things and behave independently.]


###### Example 2

If you plot a VCF Operations VM in vCenter real-time performance chart, you will see 12 peaks in that one-hour line chart. The reason is VCF Operations pulls, process, and writes data every 5-minutes. The chart for CPU, disk and network will sport the same pattern. This is expected.
But if you plot the memory metrics, be it total active, active write or consumed, you will not see the 12 peaks. This is what I got instead.

[Image: ## Image Description

This is a VMware vCenter **Advanced Performance chart** showing memory metrics for a vROps VM over a 1-hour real-time period (03/15/2021, 7:58–8:58 AM). Three metrics are plotted: **Active memory** (blue, ~3–5M KB), **Active Write** (black, ~1–3M KB), and **Consumed** (green, flat at **16,777,216 KB**). 

The chart demonstrates the key anomaly discussed in the text: unlike CPU/disk/network metrics, **no 12 peaks are visible** in any memory metric, and Consumed remains completely flat at its maximum value (~16.7M KB) throughout the entire hour, while Active and Active Write show irregular fluctuations rather than the expected 5-minute collection cycle peaks.]

Consume is completely flat and high. Active (read and write) and Active Write (write only) is much lower but again the 12 peaks are not shown.
Can you figure it out?
My guess is the sampling size. That’s just a guess, so if you have a better answer let me know!
Now let’s go to VCF Operations. In VCF Operations, this metric is called Memory \ Non Zero Active (KB).
vCenter reports in 20 seconds interval. VCF Operations takes 15 of these data and average them into a 300-second average. In the 300 second period, the same page can be read and written multiple times. Hence the active counter over reports the actual count.
Quiz: now that you know Active over reports, why is it lower than Consumed? Why is it lower than Guest OS metrics?
Active is lower than both metrics because these 2 metrics do not actually measure how actively the page is used. They are measuring the disk space used, so it contains a lot of inactive pages. You can see it in the general pattern of Consume and Guest OS used metrics. The following is VCF Operations appliance VM. Notice how stable the metrics are, even over millions of seconds.

[Image: The chart displays four memory metrics for **vrops-prd-1** over approximately 6 weeks (Dec 16 – Jan 25): **Total Capacity** (50,331,648 KB) and **Memory Consumed** (50,327,432 KB) run nearly flat near 50M KB, while **Guest Needed Memory** (50,331,128 KB) shows two brief dips (around Jan 3 and Jan 16). **Non Zero Active** (14,193,523 KB) oscillates cyclically between ~10M–20M KB throughout the period. This demonstrates the core point of the surrounding text: Consumed and Guest OS metrics appear artificially stable and high (near full capacity) because they include inactive pages, while Active memory is significantly lower (~28% of capacity) and reflects actual dynamic usage patterns.]


#### Usage (%)

Usage metric in vCenter differs to Usage metric in VCF Operations.
What you see on the vCenter UI is Active, not Consumed.

[Image: The image shows a **VMware vCenter Server Appliance (VCSA) VM summary page**, displaying a VM running **VMware Photon OS (64-bit)** on ESXi 5.5+ compatibility with 4 CPUs and 16 GB configured memory. Key resource metrics show **CPU Usage: 3.09 GHz**, **Memory Usage: 4.32 GB** (matching the 4.32 GB active memory shown in VM Hardware), and **Storage Usage: 524.76 GB**. This screenshot illustrates the surrounding text's point that vCenter's Memory Usage metric reflects **Active memory** (4.32 GB active out of 16 GB total), not Consumed memory, demonstrating the distinction between these metrics in the context of how vCenter UI reports memory utilization.]

Mapping to Active makes more sense as Consumed contains inactive pages. As covered earlier, neither Active nor Consumed actually measures the Guest OS memory. This is why VCF Operations maps Usage to Guest OS. The formula is:
VM Memory Usage (%) = Guest OS Needed Memory (KB) / VM Memory Total Capacity (KB) * 100
The following shows what Usage (%) = Guest OS Needed Memory over configured memory. The VM has 1 GB of memory, so 757 MB / 1024 = 74%.
Take note that there can be situation where Guest OS metrics do not make it to VCF Operations. In that case, Usage (%) falls back to Active (notice the value dropped to 6.99%) whereas Workload (%) falls back to Consumed (notice the value jump to 98.95%).

[Image: The image shows three time-series charts for **snapshot_01_091220_alik** between ~02:38–02:56 AM, displaying **Memory|Workload (%)** (H: 98.95, L: 73.87), **Memory|Usage (%)** (H: 73.979, L: 6.99), and **Guest|Needed Memory (MB)** (H: 757.55, L: 755.92). Around 02:45–02:46 AM, Workload spikes to ~100% while Usage simultaneously drops to ~6.99%, with the Guest|Needed Memory chart showing **2 missing data points** at the same timestamps. This demonstrates that when VMware Tools guest metrics fail to report (missing data), Usage (%) falls back to Active (~6.99%) and Workload (%) falls back to Consumed (~98.95%), as described in the surrounding text.]


#### Utilization

Utilization (KB) = Guest Needed Memory (KB) + ( Guest Page In Rate per second * Guest Page Size (KB) ) + Memory Total Capacity (KB) – Guest Physically Usable Memory (KB).
Because of the formula, the value can exceed 100%. The following is an example:

[Image: ## Image Description

The chart displays three memory metrics for a VMware "master" VM over approximately 18 hours: **Memory Utilization (KB)**, **Memory Total Capacity (KB)** (8,388,608 KB ≈ 8 GB), and **Guest Needed Memory (KB)** (8,388,088 KB). At **Monday, May 24, 10:05:04 AM**, a sharp spike shows Memory Utilization reaching **8,639,603 KB** — exceeding Total Capacity by ~251 MB, demonstrating how the Utilization metric can **exceed 100%** due to its formula incorporating Guest Page In Rate. The flat teal line representing Total Capacity serves as a visual baseline, confirming the purple Utilization line regularly fluctuates above it.]

It’s possible that VCF Operations shows high value when Windows or Linux does not. Here are some reasons:
- Guest metrics from VMware Tools are not collecting. The value falls back to Consumed (KB). Ensure your collection is reliable, else the values you get over time contains mixed source. If their values aren’t similar, the counter values will be fluctuating wildly.
- Guest Physically Usable Memory (KB) is less than your configured memory. I’ve seen in one case where it’s showing 58 GB whereas the VM is configured with 80 GB. My first guess is the type of OS licensing. However, according to this, it should be 64 GB not 58 GB.
- Low utilization. We add 5% of Total, not Used. A 128 GB VM will show 6.4 GB extra usage.
- Excessive paging. We consider this. The tricky part is excessive is relative.
- We include Available in Linux and cache in Windows, as we want to be conservative.

#### Demand

Can you spot a major counter that exists for CPU, but not for RAM?
That’s right. It’s Demand. There is no memory demand counter in vCenter UI.
To figure out demand, we need to figure out unmet demand, as demand is simply unmet demand + used (which is met demand). Since the context here is VM, and not Guest OS, then unmet demand includes only VM level metrics. The metrics are ballooned + swapped + compressed.
Do you agree with the above?
If we are being strict with the unmet demand definition, then only the memory attributed to contention should be considered unmet demand. That means balloon, swap, or compressed memory can’t be considered unmet demand. Swap in and decompression are the contention portion of memory. The problem then becomes the inability to differentiate contention due to limits using host level metrics, which means we’d need to look at VM level metric to exclude that expected contention.

### Quiz!

Take a look at the following VM. The chart is hard to read, so read the table below it.

[Image: ## Chart Description

This time-series chart displays VMware vSphere memory metrics for a single VM over approximately one hour (09/11/2024, 8:50 PM – 9:45 PM), with **KB on the left Y-axis** and **KBps on the right Y-axis**. The most notable data points are two nearly flat horizontal lines at the top: **Swap Target (~6.8M KB)** and **Actual Swapped (~6.4M KB)**, both remaining constant throughout the monitoring window, indicating no active memory reclamation activity is occurring. Lower in the chart, additional flat lines representing **Granted memory (~1.1M KB)**, and near-zero baseline metrics are visible, collectively demonstrating a VM in a stable but historically memory-constrained state where swap values reflect prior contention rather than active pressure.]


[Image: The table displays VM-level memory metrics including Swap Target (~6.8M KB), Swapped (~6.5M KB), Granted (~1.2M KB), Consumed (~936K KB), Compressed (~644K KB), Shared (~570K KB), and Active (~83K KB), with swap-related rate metrics (Swap in/out, Compression/Decompression rates) all showing zero. The stable maximum/minimum values for most metrics indicate static, non-fluctuating memory states over the observed period. This data illustrates the distinction between historical/passive memory reclamation (high swapped values with zero swap-in rate) versus active contention, supporting the surrounding text's discussion about differentiating true memory contention from limit-induced reclamation using VM-level metrics.]

The 1st line (highest) is Swap Target. It’s hovering around 6.8 million KB. It’s fluctuating every 20 seconds (I did zoom in). ESXi does not have to achieve this if it does not need it.
The 2nd line is actual swapped. It’s also constant in the last 1 hour. You can see the maximum and minimum are the same. The VM does not have limit, and it’s not part of resource pool, so this could be historical.
The 3rd line shows the amount granted. It’s also constant, indicating the VM does not ask for more.
The 4th line shows the amount consumed. It did fluctuate. I zoomed in and confirmed there were minor fluctuations. This is interesting since all other counters are 0.
The patterns of Consumed and Swap Target are mirror image. When Consume goes up, the target swap goes down.

[Image: ## Image Description

The chart displays **host physical memory consumed for backing up guest physical memory pages** (a VMware balloon/swap-related metric) for the VM **CP_for_HubMultiRegionBEValidation** on 09/11/2024 between 9:10 PM and 10:05 PM. Memory consumption rises steadily from ~931,500 KB to a peak of ~939,000 KB around 9:28 PM, then drops sharply and fluctuates between ~934,000–937,000 KB for the remainder of the period. The tooltip highlights a specific data point at **9:41:00 PM showing 936,340 KB**, illustrating the volatile but bounded memory behavior discussed in the surrounding text about consumed memory counter fluctuations.]

Active is a sample. So it could be constant even though it should not be in this case as Consumed was not constant.

## ESXi

Compared with CPU metrics, vCenter provides even more metrics for memory: 38 metrics for RAM plus 11 for the kernel RAM. The kernel has around 50 processes that are tracked. As a result, a cluster of 8 ESXi can have > 800 metrics just for ESXi RAM.
We will cover each metric in-depth, so let’s do an overview first.

### Overview

Just like the case for VM, the primary counter for tracking performance is Page-fault Latency. Take note this is normalized average, so use the Max VM Memory Contention instead.

[Image: ## Image Description

The image shows a **VMware vSphere memory metrics table** displaying counter properties including Rollups, Units, Stat Type, and Description columns. Two visible counters are **Page-fault Latency** (Average rollup, % units, Absolute stat type) and **Reclamation threshold** (Average rollup, KB units, Absolute stat type), with a tooltip visible showing the full description: *"Percentage of time the virtual machine spent waiting to swap in or decompress guest physical memory."*

This image contextually supports the text's identification of **Page-fault Latency as the primary ESXi memory performance counter**, while noting it represents a normalized average — and the tooltip confirms it measures swap/decompress wait time, directly connecting to the subsequent discussion about swap-related contention metrics.]

The contention could be caused by swapping in the past. You’ve got only 5, not 6 metrics for swap. Which counter is missing?

[Image: The image displays a table of **5 ESXi swap memory metrics**: Swap consumed, Swap in, Swap in rate, Swap out, and Swap out rate. Each metric shows its rollup type (Average), unit (KB or KBps), and measurement type (Absolute or Rate). This table contextualizes the surrounding text's point that **Swap target is the missing 6th metric**, as it is notably absent from this list of swap-related counters.]

Swap target is missing. It can be handy to see the total target at ESXi level.
Swap and Compress go hand in hand, so we should check both together. Here are the compressed metrics.

[Image: The image displays a table of **three memory compression metrics** for VMware ESXi: **Compressed** (Average, KB, Absolute) measuring guest physical memory pages that have undergone compression, **Compression rate** (Average, KBps, Rate) measuring the rate of page compression by ESXi, and **Decompression rate** (Average, KBps, Rate) measuring the rate of memory decompression. In the context of the surrounding text, this table follows the swap metrics discussion and presents the available counters for monitoring memory compression activity. Notably, only input/output rate metrics and a size metric are provided, with the author questioning whether "Compressed" measures the pre- or post-compression size.]

I’m unsure if Compressed measures the result of the compression, or the input. My take is the former as that’s more useful from ESXi viewpoint.
Lastly, the performance could be caused by memory being read from the Host Cache. While they are faster than disk, they are still slower than physical memory.

[Image: The image displays a table of **VMware vSphere Host Cache memory metrics**, showing five counters: **Host cache consumed, Host cache swap in, Host cache swap in rate, Host cache swap out, and Host cache swap out rate**. All metrics use **Average** rollup, with absolute metrics measured in **KB** and rate metrics in **KBps**. In context, these metrics are presented to monitor performance degradation caused by guest physical memory being swapped to/from the host cache (SSD-based swap), which is slower than physical RAM but faster than traditional disk.]

Wait! What about Balloon?
As will cover in-depth shortly, that’s more of capacity than performance metrics. One can even say that other than Page-fault Latency, the rest of the metrics are actually for capacity not performance.
The famous balloon is a warning of capacity, assuming you do not play with limit.

[Image: The image shows a table row describing the **Ballooned Memory** metric in VMware vSphere, with attributes: **Average** aggregation, **KB** unit, and **Absolute** rollup type. The description defines it as the "Amount of guest physical memory reclaimed from the virtual machine by t[he balloon driver]" (text truncated). This metric appears in context of distinguishing capacity metrics from performance metrics, illustrating that balloon memory is primarily a **capacity warning indicator** rather than a performance metric.]

When will ballooning kick in? There is a counter for that!

[Image: The image shows a VMware vSphere metric entry for **"Reclamation threshold"**, displaying properties: **Average** rollup, **KB** unit, and **Absolute** stat type, with a description indicating it represents the "Threshold of free host physical memory below which ESXi will begin" (text truncated). This metric defines the memory threshold at which ESXi initiates memory reclamation techniques such as ballooning, directly supporting the surrounding text's discussion of when ballooning will kick in. It is a host-level capacity metric measured in kilobytes.]

The memory state level shows one of the 5 possible states. You want to keep this at Clear state or High state.

[Image: The image shows a metric definition row for the **"Free state"** counter in VMware ESXi, displaying metadata including rollup type (**Latest**), data type (**num**), unit (**Absolute**), and a description stating it represents the "Current memory availability state of ESXi" with possible values of **high, clear, s...** (truncated). This metric corresponds to the memory state level discussed in the surrounding text, which identifies five possible states, with **Clear** and **High** being the desired states. It is the counter referenced for determining when memory ballooning will activate on an ESXi host.]

For environment where performance matters more than cost, you want Balloon to be 0. That means Consume becomes your main counter for capacity. It is related to Granted and Shared.

[Image: The image displays a table of VMware memory metrics including **Host consumed %**, **Consumed**, **Granted**, **Shared**, and **Shared common**, all measured as Average/Absolute values in KB (except Host consumed % which uses %). In the context of the surrounding text, this table illustrates the relationship between Consumed, Granted, and Shared memory counters, which are the primary capacity metrics when Balloon is at 0. The Consumed metric specifically tracks host physical memory backing guest pages, while Shared and Shared common counters quantify memory deduplication savings across VMs.]

Reservation plays a big part in capacity management as it cannot be overcommitted. ESXi, being a provider of resource, has 3 metrics to properly account for reservations.

[Image: The image displays a table of three ESXi memory reservation metrics: **Reservation available** (Average, KB, Absolute), **Reservation consumed** (Average, MB, Absolute), and **Total reservation** (Average, MB, Absolute). Each metric includes a description, with Total reservation representing the sum of available and consumed reservations for powered-on VMs. In the context of the surrounding text, these three counters illustrate how ESXi accounts for memory reservations, which cannot be overcommitted and therefore play a critical role in capacity management.]

There are a few metrics covering 0 pages and overhead. The Heap counter shows the memory used by the kernel heap and other data. This is normally a constant and small value.

[Image: The image displays a table of five ESXi host memory metrics: **Overhead consumed**, **VMkernel consumed**, **Zero pages**, **Heap**, and **Heap free** — all measured in KB as Average/Absolute counters. In the context of the surrounding text, this table documents metrics related to zero pages, memory overhead, and kernel heap usage, with the Heap counter specifically noted as tracking memory used by the kernel heap and other data structures. The descriptions clarify the distinction between ESXi data structure overhead, VMkernel consumption, and heap address space versus free heap space.]


##### Other Metrics

Active is not a counter for capacity or performance. It’s for the kernel memory allocation.

[Image: The image displays a table showing two VMware ESXi memory metrics: **Active** and **Active Write**, both measured as Average values in KB (Absolute). Both metrics relate to guest physical memory activity — "Active" tracks memory being read or written by the guest, while "Active Write" specifically tracks memory being actively written, with activeness estimated by ESXi in both cases. In context, these metrics are categorized as non-capacity/performance counters, described as kernel memory allocation indicators rather than traditional performance measurements.]

Persistent Memory

[Image: The image shows a metrics table with two **Persistent Memory** counters in VMware vSphere: **"Persistent memory available reservation"** and **"Persistent memory reservation managed by DRS"**. Both counters use **Latest** rollup, are measured in **MB**, and use an **Absolute** stat type. These metrics track persistent memory (PMem) reservation availability on a host and DRS-managed PMem reservations respectively, contextually introduced as part of a broader section covering miscellaneous/other memory metrics.]

Lastly, there are a few metrics for VMFS pointer block cache. Read more here. They are internal, only used by the kernel. The only one you might be interested in the cache capacity miss ratio. Let me know if you have a real-world use case them.

[Image: The image displays a table of **VMFS Pointer Block Cache metrics** available in VMware vSphere, listing six counters: Maximum VMFS PB Cache Size (MB), Maximum VMFS Working Set (TB), VMFS PB Cache Capacity Miss Ratio (%), VMFS PB Cache Overhead (KB), VMFS PB Cache Size (MB), and VMFS Working Set (TB). All metrics use **Latest** rollup and **Absolute** stat type. In context, the surrounding text identifies these as internal kernel metrics, with the **VMFS PB Cache Capacity Miss Ratio** being the only one of potential practical interest to administrators.]


### “Contention” Metrics

I put the title in “quote” as none of these counters actually measure contention.
I do not cover the Latency metric as that’s basically a normalized average of all the running VMs on the host.

#### Balloon

Balloon is a leading indicator that an ESXi is under memory pressure, hence it’s one of the primary metrics you should use in capacity. Assuming you’re not using Limit to artificially cap the resource, you should ensure that the balloon amount does not cause VM to experience contention.
We know that contention happens at hypervisor level, not at VM level. The VM is feeling the side effects of the contention, and the degree of contention depends on each VM's shares, reservation and utilization. ESXi begins taking action if it is running low on free memory. This is tracked by a counter called State. The State counter has five states, corresponding to the Free Memory Minimum (%) value

| ESXi State | Threshold | 1 TB ESXi | Example based on ESXi with 1 TB RAM |
| --- | --- | --- | --- |
| High | 300% | 32.4 GB | First, we calculate the Free Memory Minimum value. There is many website to help you with this, such as this.  For 1 TB, the value is 10.8 GB. |
| Clear | 100% | 10.8 GB | First, we calculate the Free Memory Minimum value. There is many website to help you with this, such as this.  For 1 TB, the value is 10.8 GB. |
| Soft | 64% | 6.9 GB. Balloon starts here | First, we calculate the Free Memory Minimum value. There is many website to help you with this, such as this.  For 1 TB, the value is 10.8 GB. |
| Hard | 32% | 3.5 GB. Compress/Swap starts here | First, we calculate the Free Memory Minimum value. There is many website to help you with this, such as this.  For 1 TB, the value is 10.8 GB. |
| Low | 16% | 1.7 GB. Block execution | First, we calculate the Free Memory Minimum value. There is many website to help you with this, such as this.  For 1 TB, the value is 10.8 GB. |

Using the example above, let’s see at which point of utilization does ESXi triggers balloon process.

| ESXi State | 512 GB ESXi | 1 TB ESXi | 1.5 TB ESXi |
| --- | --- | --- | --- |
| Balloon Threshold | 3.7 GB | 6.9 GB | 10.2 GB |
| Threshold | 508.3 GB | 993.1 BB | 1489.8 GB |
| Threshold in % | 99.3% | 99.3% | 99.3% |

As you can see from all the 3 ESXi, balloon only happens after at least 99% of the memory it utilized. It’s a very high threshold. Unless you are deliberately aiming for high utilization, all the ESXi should be in the High state.
In addition, the spare host you add to cater for HA or maintenance mode will help in lowering the overall ESXi utilization. Let’s use example to illustrate
- No of ESXi in a cluster = 12
- Provisioned for HA = 11
- Target ESXi memory utilization = 99% (when HA happens or planned maintenance)
- Target ESXi memory utilization = 99% x 11 / 12 = 90.75% (during normal operations)
Using the above, you will not have any VM memory swapped as you won’t even hit the ballooned stage. If you actually see balloon, that means there is limit imposed.
The Low Free Threshold (KB) counter provides information on the actual level below which ESXi will begin reclaiming memory from VM. This value varies in hosts with different RAM configurations. Check this value only if you suspect ESXi triggers ballooning too early.
ESXi memory region can be divided into three: Used, Cached and Free
- Used is tracked by Active. Active is an estimate of recently touched pages.
- Cached = Consumed - Active. Consumed contains pages that were touched in the past, but no longer active. I'm not sure Ballooned pages are accounted in Consumed, although logically it should not. It should go to Free so it can be reused.
- Free = Total Capacity - Consumed.
The nature of memory as cache means the active part is far lower than the non-active part. It’s also more volatile. The following shows an ESXi with low memory usage, both active and consumed, in the last 3 months.

[Image: ## Image Description

The chart displays three memory metrics for an ESXi host over approximately 4 months (Dec 21 – Mar 15): **Total Capacity (766.62 GB)**, **Memory Consumed (417.36 GB peak)**, and **Guest Active (26.58 GB)** — captured at a tooltip on Wednesday, Feb 3, 06:00–08:59 AM. The flat cyan line represents total capacity (~800 GB), while the pink "Consumed" line remains near zero for most of the period with two notable spikes (peaking ~417 GB around Feb 3 and ~200 GB around Mar 8), and the purple "Guest Active" line stays consistently low (near zero). This demonstrates the book's point that **active memory is far lower than consumed memory**, illustrating low overall ESXi memory utilization with brief intermittent activity spikes.]

Let’s look at an opposite scenario. The following ESXi is running at 100%. It has granted more memory than what it physically has. Initially, since the pages are inactive, there is no ballooning. When the active rise up, the consumed counter goes up and the balloon process kicks in. When the VM is no longer using the pages, the active counter reflects that and ESXi begin deflating the balloon and giving the pages back.

[Image: ## Image Description

The chart displays four ESXi memory metrics over approximately 5 days (Nov 24-29): **Memory Granted (267,539,552 KB)**, **Memory Consumed (264,875,584 KB)**, **Memory Guest Active (13,885,348 KB)**, and **Memory Balloon (5,517,618 KB)** at the tooltip timestamp of **Thursday, Nov 26, 05:59:59 PM**.

The chart demonstrates the described scenario where an ESXi host has granted more memory than physically available (~250M KB threshold visible), with ballooning (~5.5 GB) active while Guest Active memory remains relatively low (~13.8 GB) compared to consumed (~252 GB). This visually confirms the text's explanation that ballooning correlates with rising active memory, then deflates when active memory decreases — the balloon and active lines (teal/cyan) show corresponding spikes around Nov 26 while granted and consumed remain relatively stable.]

I shared in the VM memory counter that just because a VM has balloon, does not mean it experiences contention. You can see the same situation at ESXi level. The following ESXi shows a constant and significant balloon lasting at least 7 days. Yes the worst contention experienced by any VM is not even 1%, and majority of its 19 VMs were not experiencing contention at all.

[Image: The image displays three ESXi-level memory metrics over a 7-day period (Mar 21–28): **Memory Balloon** (ranging 15.2–17.95 GB, showing a consistently elevated and relatively stable baseline), **Worst VM Memory Contention** (peaking at just 1%, with brief spikes that quickly return to ~0%), and **Percentage of VMs Facing Memory Contention** (peaking at 3.85%, indicating only a small fraction of the ~19 VMs experienced contention). This demonstrates the key point from the surrounding text: despite persistent and significant memory ballooning (~16–18 GB sustained over 7 days), actual VM memory contention remains negligible (≤1%), confirming that balloon activity alone does not indicate meaningful VM performance impact.]


#### Swap + Compress

For swap, the metric is the summation of running VMs and the kernel services.
For compress, there are 2 counters at ESXi level. The first is the sum of all amounts that were subjected to compressed. The second is the resultant compressed amount.

| Metrics | Description |
| --- | --- |
| Swap Consumed | Sum of memory swapped of all powered on VMs and vSphere services on the host. This number will reduce if pages are swapped back into the DIMM. I think this is swapped out – swapped in. |
| Swap In | The total amount of memory that have been swapped in or out to date.  Note: These counters are accumulative. |
| Swap Out | The total amount of memory that have been swapped in or out to date.  Note: These counters are accumulative. |
| Swap In Rate | I think this includes compressed, not just swapped, but I’m not 100% sure as I can’t find a proof yet. |
| Swap Out Rate | I think this includes compressed, not just swapped, but I’m not 100% sure as I can’t find a proof yet. |

Pages can and will remain in compressed or swapped stage for a long time. The following screenshot shows compressed remains around 5 GB for around 1 year.

[Image: The chart displays memory metrics for **w1-vrni-tmm-esx012.eng.vmware.com** on April 10, 2022, showing **Swap Out (KB) at 6,803,044**, **Compressed (KB) at 5,018,516**, with **Swap In Rate, Swap Out Rate, and Balloon all at 0**. The trend lines show Compressed memory remaining relatively flat near ~5GB and Swap Out staying elevated over approximately one year (May 2022 – Mar 2023). This demonstrates that compressed/swapped pages persisted long-term without being reclaimed, while the zero Balloon value confirms the ESXi host was not under active memory pressure during this period.]

The above happened because there was no need to bring back those pages. Notice ballooning was flat 0, indicating the ESX host was not under memory pressure.
Swap Out is an accumulative counter.

[Image: ## Image Description

The chart displays **Memory Swap Out (KB)** as a cumulative counter over approximately 12 weeks (October 2 – December 25), showing a **steady, nearly linear increase** from **4,170,432,000 KB to 6,812,044,288 KB** — a growth of ~2.6 TB. The consistently upward slope with no decreases confirms the **accumulative nature of the Swap Out counter**, meaning pages were continuously being swapped/compressed out without being reclaimed. This aligns with the surrounding text's point that pages can remain in compressed or swapped state for extended periods, particularly when the host shows **zero ballooning** (indicating no active memory pressure requiring page retrieval).]

Let’s zoom in, and add the swap in and swap out counters to compare.

[Image: The image displays three charts for **wdc-01-r09esx34.oc.vmware.com** showing: (1) **Memory Swap Used** trending upward from ~6,811,832,832 to 6,812,868,096 bytes over ~6 hours (6:30 AM–12:00 PM), (2) **Memory Swap In Rate** peaking at 352.6 KBps around 8:30 AM with sporadic spikes throughout, and (3) **Memory Swap Out Rate** peaking at 265.47 KBps near 9:00 AM. The key observation supporting the surrounding text is that **Swap Used (accumulative) continues to rise and never decreases** despite active swap-in activity, confirming that the Swap Out counter is cumulative and pages are not being fully reclaimed even as swap-in occurs.]

Notice the value did not go down despite swap in.

#### All “Together”

Balloon operates differently and works at a different layer than Swap and Compress. It takes longer to realize, and is not affected by limit. As a result, you can have 0 balloon while having swapping and zipped.
The following ESXi shows high Consume, and even higher Granted.
- The first line (highest blue line) shows Consume is hovering around 96%.
- The second line (purple line, just below the blue) shows Granted is hovering around 756 million KB.
- The third line shows consumed hovering around 514 million KB. ESXi has 511.46 GB or 536,304,680 KB of memory.

[Image: ## Image Description

This is a VMware vSphere Advanced Performance chart for ESXi host **10.119.161.128**, displaying memory metrics over a ~55-minute window on **09/11/2024 from 8:20 PM to 9:15 PM**. Three relatively flat lines are visible: the highest (cyan/blue) line hovers near **756M+ KB (~96% consumed)**, a purple line just below it representing **Granted memory (~756M KB)**, a mid-range dark blue line at approximately **514M KB (consumed)**, and a dark green line stable around **285M KB**. The chart demonstrates a high memory utilization state on the ESXi host with very stable, consistent consumption — supporting the surrounding text's context that despite high Consume and Granted values, balloon memory remained at 0 while minimal swapping/compression activity occurred.]

Since it’s hard to see, let’s show the table. What do you notice?

[Image: ## Image Description

The table displays ESXi host memory metrics across seven measurements (Granted, Consumed, Shared, Swap Consumed, Compressed, Host Consumed %, and Ballooned Memory), showing Latest, Maximum, Minimum, and Average values. Key data points show **Host Consumed % averaging ~96%**, Granted memory at ~760 GB (760,780,350 KB), Consumed at ~514 GB (514,850,208 KB average), with Swap Consumed at ~1.4 GB and Compressed at ~89 MB — both relatively small. Notably, **Ballooned Memory is consistently 0** across all columns, confirming no balloon driver activity despite the host operating at near-capacity memory utilization with minor swapping and compression occurring.]

Ballooned was 0 constantly.
However, there were swapped and compressed. Let’s see if they are still happening, since these 2 counters are accumulative.
As you can see from the following chart, the amount is negligible. There are 4 instances of swap in, and each time the amount is 1 KB/second or 2 KB/second. Since the number of is the average of 20 seconds, the total amount is 20 KB or 40 KB only.

[Image: ## Image Description

The chart displays **memory swap in rate, swap out rate, compression rate, and decompression rate** for host **10.119.161.128** over a ~1-hour real-time period on 09/11/2024 (8:07–9:07 PM), measured in KBps. The data shows **4 isolated spikes** in swap in rate occurring approximately at 8:25, 8:30, 8:40, and 9:00 PM, with peak values of **1 KBps and 2 KBps** respectively, while swap out, compression, and decompression rates remain at **0 throughout**. This confirms the surrounding text's assertion that memory pressure is negligible — the swap activity is sporadic and minimal (maximum 2 KBps, average 0.028 KBps), totaling only ~20–40 KB per event.]

Does it mean the memory is not active?
Let’s look at the Active metric. It shows there are indeed activities, but they are within the pages already in the DIMM.

[Image: ## Image Description

The chart displays two memory metrics for host **10.119.161.128** over approximately 55 minutes (8:40 PM – 9:35 PM on 09/11/2024): **Active** (blue, averaging ~61.25M KB, max ~73.5M KB) and **Active Write** (purple, averaging ~26.87M KB, max ~37.74M KB), both measured in KB with 20-second average rollups. Both metrics show significant fluctuation with notable drops mid-period before recovering toward the end. This chart demonstrates that while swap activity was negligible, substantial memory pages are actively being accessed within DIMM (Active ~61–68M KB at latest reading), confirming real memory activity without requiring swap involvement.]


### Consumption Metrics

Consumption covers utilization, reservation and allocation.

[Image: ## Image Description

The diagram illustrates the relationship between **Virtual View** (sum of all running VMs) and **Physical View** (Kernel + VM actual pages) for ESXi memory metrics, showing how virtual memory allocations map to physical memory. It displays seven memory categories: **Granted, Before Zip, Swapped, Host Cache, Ballooned, Overhead, and Free**, color-coded (blue=consumed/shared, red=reclamation techniques, yellow=ballooned, green=free/shared savings, black=overhead/kernel). The diagram demonstrates that **Consumed = Physical Memory – Free**, showing how virtual allocations compress into physical pages, with red arrows indicating pages that have been reclaimed via swap, host cache, or compression, while the bottom note clarifies that **Active, Limit, Shared Savings, and Zip Savings are physical-layer metrics**.]


#### Consumed

Consumed is the primary counter for ESXi utilization but it contains a lot of cache and inactive pages. Just like any other modern-day OS, the kernel uses RAM as cache as it's faster than disk. So the Consumed counter will be near 100% in overcommit environment. This is an ideal goal, as opposed to something you need to panic.
The formula is:
Consumed = Physical memory – Free.
What does the above mean since you can overcommit?
Consumed only includes pages mapped in the physical DIMM. That means:
- It does not include ballooned. This metric is at the Guest OS level.
- It does not include swapped. The swapped pages reside on disk or host cache.
- It only includes the resultant zipped, not the amount subjected to compression.
- It only includes the resultant savings from TPS, not the amount subjected to sharing.
- It includes VM overhead
- It includes all the kernel processes, both user space and protected space.
Formula for VCF Operations Metrics:
- Usage (%) = Consumed / Total Capacity.

##### Ballooned

Consumed does not include Ballooned. This makes sense as the pages no longer backed by physical pages. The following screenshot shows consumed drops when balloon went up.

[Image: ## Image Description

The image displays two time-series charts for host **sc2-vsan-stage1-14.infra.vmware.com** covering approximately 08:30 PM to 11:00 PM. The **top chart** shows **Memory|Consumed (KB)** dropping sharply from a high of **278,181,024 KB** to a low of **47,249,968 KB**, then rapidly recovering to ~276,217,312 KB around 09:15 PM before stabilizing near 250M KB. The **bottom chart** shows **Memory|Balloon (KB)** spiking from **0 to a high of 10,680,388 KB** (highlighted in green) beginning around 09:00 PM and persisting until ~09:45 PM, directly correlating with the consumed memory drop — visually demonstrating that **Consumed memory decreases when balloon memory increases**, as ballooned pages are no longer backed by physical RAM.]


##### Swapped

Consumed does not include swapped. This makes sense as the page are no longer in the physical memory. The following screenshot shows consumed drops when swap out went up.

[Image: The image shows two time-series charts from approximately 6:00 PM to 12:30 AM on March 27, tracking **Memory|Swap Out (MB)** (top) and **Memory|Consumed (MB)** (bottom) for a vSphere host. Swap Out increases from a low of **5,875.09 MB** to a high of **5,942 MB**, with a sharp spike around 11:30 PM, while Consumed simultaneously declines from a high of **246,561.77 MB** to a low of **246,445.95 MB**. This demonstrates the inverse relationship described in the surrounding text: as memory pages are swapped out of physical RAM, they are no longer counted in Consumed memory, causing Consumed to drop.]


##### Compressed

Consumed does not include compressed. The following shows that both compressed and swap out went up by almost 200 GB, yet Consumed dropped in the same period. It’s possible pages were removed from Consumed and were swapped and compressed.

[Image: ## Image Description

The chart displays three memory metrics for **wdc-09-r05esx05.oc.vmware.com** over approximately 5 months (July–November): **Memory Consumed** (pink, ~400–700 GB range with high volatility), **Memory Swap Out** (teal, jumping from ~0 to ~175 GB around August 21 and remaining elevated), and **Memory Compressed** (blue, near 0 throughout). At the tooltip timestamp (Nov 23), values show **Consumed: 465.24 GB**, **Swap Out: 176.43 GB**, and **Compressed: 19.06 GB**. The chart demonstrates that **Consumed dropped significantly around August 21** precisely when Swap Out spiked to ~175 GB, visually confirming the preceding text's assertion that swapped and compressed pages are excluded from the Consumed metric.]


##### Kernel

The other part of Consumed is non VM. This means the kernel, vSAN, NSX and whatever else running on the hypervisor. Because ESXi Consumed includes non VM, it can be more than what’s allocated to all running VMs, as shown below.

[Image: The chart displays ESXi host memory **Consumed** (purple, ~525 GB) versus **Allocated** (pink, ~516 GB) from August 13 to September 11, with a tooltip highlighting **Friday, Sep 10, 02:00–03:59 AM** showing Consumed at **525.1323** and Allocated at **516**. This demonstrates the key point that **Consumed exceeds Allocated**, because ESXi Consumed includes non-VM overhead such as the kernel, vSAN, and NSX in addition to VM memory. The y-axis scale shows values between 250 and 500 GB, confirming that kernel/hypervisor components contribute meaningful memory consumption beyond what is allocated to running VMs.]

Take note that Consumed includes the actual consumption, not the reservation. The following ESXi has 0 running VM, so the Consumed is just made of the kernel. You can see the utilization is much lower than the reservation.

[Image: ## Image Description

The chart displays two memory metrics for an ESXi host (`*61-esxi-06.*.com`) over a ~4-day period (Mar 24–28): **ESX System Usage** at **56,860,200 KB (~54 GB)** shown as a flat purple line near the top, and **Memory Consumed** at **17,566,670 KB (~17 GB)** shown as a flat pink line near the 20M mark. Both lines are essentially horizontal with no variance, captured at **Saturday, Mar 26, 11:15–11:29 PM**. This demonstrates the context described in the surrounding text: with **zero running VMs**, Consumed (~17 GB) reflects only kernel/vSAN overhead, while ESX System Usage (~54 GB) represents the total reserved/allocated capacity — illustrating that Consumed is significantly lower than the system reservation.]

If you’re wondering why it’s consuming 17 GB when there is 0 VM, the likely answer is vSAN. Just because there is no VM does not mean vSAN should stop running.

#### Granted

Granted differs to Consumed as it excludes certain part of the kernel. It does not include the kernel space as processes at this privileged level gets what they want. They do not need the granting process, so to speak. Consumed, on the other hand, includes all both user and kernel space as both are indeed consuming pages.
Granted, being a consumer-level counter, can exceed total capacity. The following ESXi has granted 1053 GB of memory to running VMs, way above its total capacity of 755 GB.

[Image: ## Image Description

This time-series chart from vCenter displays memory metrics for **wdc-08-r03esx27.oc.vmware.com** over a ~6-hour window (8:30 AM – 2:30 PM, Tuesday Dec 26). The tooltip at 02:11:42 PM shows **Memory Granted (1,053.715 GB)** in blue exceeding **Total Capacity (766.62 GB)** in pink, while **Memory Consumed (660.75 GB)** in teal remains below capacity, with negligible Swap Used (3.78 GB), Compressed (0.007 GB), and zero Balloon. This directly illustrates the text's assertion that **Granted can exceed total physical capacity** (here by ~287 GB), while Consumed + Swap + Compressed remains safely under the physical limit.]

Notice the sum of consumed + swapped + compressed is always below the total capacity.
I added balloon just in case you’re curious.
The following example shows ESXi hosts with no running VM. I’m surprised to see the granted counter is not 0. My guess the extra memory is for non-VM user world process.

[Image: ## Image Description

This table displays memory metrics for **11 ESXi hosts with no running VMs** (VM column = 0 throughout), showing Total Capacity, Consumed, Granted, VMkernel, and vSAN Host status. Despite having zero running VMs, the **Granted counter ranges from 0.45 GB to 0.56 GB** across all hosts, supporting the author's hypothesis that granted memory is allocated for **non-VM userworld processes**. Six hosts have vSAN enabled (showing higher consumed/VMkernel values of ~35–39 GB) while five show "-", with total capacities ranging from 191.75 GB to 766.62 GB.]

Let’s take one of the ESXi to see the value over time. This time around, let’s use vCenter instead.

[Image: ## Image Description

This is a vCenter real-time memory performance chart for ESXi host **10.155.60.228** over a 1-hour period (10:27–11:27 AM, 3/30/2021), displaying three memory metrics: **Consumed** (~8.33M KB average), **VMkernel Consumed** (~7.69M KB average), and **Granted** (~432K KB average). The chart demonstrates that with **no running VMs**, the ESXi host still shows non-zero Granted memory (averaging ~432,588 KB), supporting the author's hypothesis that this memory is allocated to **non-VM userworld processes**. All three metrics remain remarkably flat/stable throughout the monitoring period, with minimal variance between minimum and maximum values.]

You can verify that ESXi Consumed includes its running VMs Consumes by taking an ESXi with a single running VM. The ESXi below has 255 GB of total capacity but only 229 GB is consumed. The 229 GB is split into 191 GB consumed by VM and 36 GB consumed by the kernel.

[Image: ## Image Description

This is a vCenter time-series chart showing ESXi host memory metrics from March 24–31, displaying four flat/stable trend lines: **Memory|Total Capacity at 255.91 GB** (pink), **Memory|Consumed at 229.8152 GB** (purple), **VM Memory|Consumed at 191.90642 GB** (dark blue), and **Memory|VMkernel Usage at 36.19252 GB** (teal), captured at a Thursday Mar 25, 09:45–09:59 AM tooltip. The chart visually demonstrates that ESXi host Consumed memory (229 GB) is the sum of VM Consumed (191 GB) and VMkernel usage (36 GB), validating the relationship described in the surrounding text. All metrics remain essentially constant over the week, indicating a stable, single-VM workload environment used specifically for metric verification purposes.]

The kernel consumption is the sum of the following three resource pools.

[Image: ## Image Description

This performance chart from vCenter displays **Resource Memory Consumed** (in KB) for three ESXi resource pools — **host/system**, **host/iofilters**, and **host/vim** — over approximately one hour on 3/30/2021 (8:20 PM to 9:15 PM). The dominant metric is **host/system** at ~22M KB (~21.5 GB), remaining nearly flat throughout, while **host/iofilters** (~10,132 KB) and **host/vim** (~623,924 KB) are negligibly small by comparison. This chart demonstrates the **kernel memory consumption breakdown** referenced in the surrounding text, showing that ESXi kernel consumption is composed of these three resource pools, with host/system being the dominant component (~36 GB equivalent in the broader context described).]


#### Shared


| Metrics | Description |
| --- | --- |
| Shared | The sum of all the VM memory pages & the kernel services that are pointing to a shared page. In short, it’s Sum of VM Shared + the kernel Shared. If 3 VMs each have 2 MB of identical memory, the shared memory is 6 MB. |
| Shared Common | The sum of all the shared pages. You can determine the amount of ESXi host memory savings by calculating Shared (KB) - Shared Common (KB) |

Memory shared common is at most half the value of Memory shared, as sharing means at least 2 blocks are pointing to the shared page. If the value is a lot less than half, then you are saving a lot.
The following shows the shared common exceeding half many times in the last 7 days.

[Image: ## Image Description

The chart displays two metrics for **w1-vrni-tmm-esx022.vrni.cmbu.local** over April 23–30: **Memory|Shared (KB)** (dark red, fluctuating between ~4M–5M KB) and **Memory|Shared Common (KB)** (blue/purple, relatively stable ~2.4M–2.5M KB). A tooltip at **Tuesday, Apr 25, 06:30–06:59 PM** shows Shared at **3,837,832 KB** and Shared Common at **2,490,272.75 KB** — where Shared Common (~2.49M) **exceeds 50% of Shared (~3.84M)**, demonstrating the anomalous condition described in the surrounding text where Shared Common unexpectedly surpasses the expected ≤50% threshold multiple times across the 7-day window.]

I’m not sure why. My wild guess is large pages are involved. ESXi hosts sport the hardware-assisted memory virtualization from Intel or AMD. With this technology, the kernel uses large pages to back the VM memory. As a result, the possibility of shared memory is low, unless the host memory is highly utilized. In this high consumed state, the large pages are broken down into small, shareable pages. The smaller pages get reflected in the shared common. Do let me know if my wild guess is correct.
You can also use the Memory shared common counter as leading indicator of host breaking large page into 4K. For that, you need to compare the value over time, as the absolute value may be normal for that host. The following table shows 11 ESXi hosts with various level of shared pages. Notice none of them is under memory pressure as balloon is 0. That’s why you use them as leading indicator.

[Image: ## Image Description

The table displays memory metrics across **11 ESXi hosts**, showing five counters: **Memory Shared (KB)**, **Memory Shared Common (KB)**, **Memory Consumed (KB)**, **Memory Balloon (KB)**, and **Memory Capacity Available to VMs (KB)**. Notably, **Memory Balloon is 0 across all hosts**, confirming no active memory pressure, while Shared values range widely (e.g., ~2.5M to ~78.1M KB) and Shared Common values are consistently lower (e.g., ~766K to ~10.3M KB). This demonstrates that Shared Common (indicating actual deduplicated/large-page-broken memory) can serve as a **leading indicator of TPS activity and large page splitting** even in the absence of memory pressure, as evidenced by the balloon counter remaining at zero throughout.]

With Transparent Page Sharing limited to within a VM, shared pages should become much smaller in value. I’m not sure if salting helps address the issue. From the vSphere manual, “With the new salting settings, virtual machines can share pages only if the salt value and contents of the pages are identical”.
I’m unsure if the above environment has the salting enabled or not. Let me know what level of sharing in your environment, especially after you disable TPS.

#### Utilization

We’ve seen that Consumed is too conservative as mostly cache and Active is too aggressive as it’s not even designed for memory sizing.
This calls for a metric in the middle. This is where Utilization comes in.
It’s the sum of running VM Utilization metrics + the kernel reservation.
Utilization uses the reservation amount for the kernel, instead of the actual utilization. This is technically not accurate but operationally wise as it gives you buffer.
I plotted from 192 ESXi. I averaged the data to remove outlier. Based on 6840 running VMs, the Utilization counter is lower than Consumed by 122 GB. If you include Shared Common, your savings goes up to 152 GB on average.

[Image: ## Image Description

The table displays memory metrics for **6 ESXi hosts** (all named `wdc-01-r0...`), each with identical **Total Capacity of 3,070.46 GB**, showing Consumed, Utilization, Running VMs, and Memory Shared Common columns. Key observations include Consumed consistently exceeding Utilization by approximately **100–850 GB per host**, with Running VMs ranging from 13 to 50. The averages row (Consumed: **522.63 GB**, Utilization: **401.1 GB**, Shared Common: **29.7 GB**) validates the author's claim that Utilization runs ~122 GB lower than Consumed, and including Shared Common increases savings to ~152 GB, demonstrating Utilization's operational efficiency as a memory planning metric.]


#### Validation

The following screenshot shows that ESXi had all its VM evacuated. Not a single VM left, regardless of power on/off status.

[Image: The chart displays **Memory Allocated on All Consumers (GB)** for an ESXi host, showing a dramatic drop from a high of **452 GB to 0 GB** occurring around **6:15–6:20 AM on March 11**, after which the metric remains completely flat at 0. This validates the VM evacuation described in the surrounding text — once all VMs were migrated off the ESXi host, allocated memory fell to zero and stayed there through **8:00 AM**. The sharp cliff-edge pattern (versus a gradual decline) confirms a bulk vMotion/evacuation event rather than organic VM shutdown.]

In the preceding chart, we could see the metric Memory Allocated on All Consumers dropped from 452 GB to 0 GB, and it remained flat after that.
Checking the Reserved Capacity metric, we can see it dropped to 0. This is expected.

[Image: ## Memory | Reserved Capacity (GB) Chart

The chart displays the **Memory Reserved Capacity** metric for an ESXi host over a time range spanning **March 9–12**, with a focused view between **5:00 AM and 8:00 AM**. The metric held steady at a high of **3.272 GB** until approximately **6:15–6:20 AM**, then sharply dropped to **0 GB** by around **6:35 AM**, where it remained flat. This validates the VM evacuation described in the surrounding text — once all VMs were migrated off the host, Reserved Capacity correctly fell to zero, confirming no remaining memory reservations on the ESXi host.]

How about Consumed?

[Image: ## Image Description

The chart displays **Memory|Consumed (GB)** for an ESXi host over a time range spanning March 9–12, with a zoomed view showing approximately 05:00 AM to 08:00 AM. The metric held steady near **400.09 GB (High)** until approximately 06:00–06:15 AM, then sharply dropped to **31.97 GB (Low)** by around 06:40 AM, where it remained flat. This demonstrates that after VM evacuation, Memory Consumed dropped significantly but did not reach 0 GB — stabilizing at ~32 GB — confirming that residual kernel-level processes (primarily vSAN) continue to consume memory even with no VMs present on the host.]

Memory Consumed also dropped. The value was 400 GB, less than 452 GB of allocated to all VM. This indicated some VM had not used the memory, which could happen.
The value dropped to 32 GB, not 0 GB. This is expected as Consumed includes every other process that runs. In this case, it is majority vSAN, which runs in the kernel.
Let’s check the kernel utilization.

[Image: ## Memory | VMkernel Usage (GB) Chart

This chart displays **VMkernel memory usage** on a vSphere host over approximately 4 hours (5:00 AM – 8:15 AM on March 11), showing a **high of 32.95 GB** and a **low of 30.52 GB**. The metric remains relatively flat around ~32 GB before dropping sharply around **6:20–6:40 AM** to ~30.52 GB, then gradually recovering slightly. This demonstrates that VMkernel memory usage remained largely stable even after VMs were powered off, supporting the author's point that kernel memory footprint does **not significantly change** based on the number of running VMs.]

Notice it’s a bit smaller than Consumed, indicating Consumed has other thing. I suspect it’s BIOS and the console in vSphere Client UI.
How come the value didn’t change much? I kind of expect some changes, based on the theory that some kernel modules memory footprint depends on the number of running VM. If you know, let me know!
How about the kernel reservation? What do we expect the value to change?

[Image: ## Image Description

The chart displays **Memory|ESX System Usage (GB)** over a time window spanning approximately **05:00 AM to 08:15 AM on March 11**, with a high of **55.54 GB** and a low of **53.03 GB**. The metric remains relatively flat around ~55.5 GB before experiencing a sharp drop of ~2.5 GB near **06:20 AM**, then stabilizes and gradually trends back upward toward ~54 GB. This supports the surrounding text's observation that ESX kernel memory usage remains largely stable, demonstrating that the kernel's memory footprint does **not change significantly** in correlation with VM workload changes, which the author finds unexpected given theoretical assumptions about kernel module memory scaling with running VM count.]

Well, it won’t since the actual usage does not change.

##### Analysis

I compare 185 production ESXi hosts to understand the behaviour of the metrics. I averaged their results to eliminate outlier.

[Image: ## Image Description

This table displays memory metrics across **11 ESXi hosts** (10 individual hosts plus a bold summary/average row), showing **Total Capacity, Host Usage, Machine Demand, Utilization, and Consumed** memory values in GB, sorted ascending by **Consumed** memory (265.11 GB to 404.42 GB). The summary row highlights the averages: **736.7 GB Total Capacity, 367.07 GB Host Usage, 247.96 GB Machine Demand, 299.56 GB Utilization, and 404.42 GB Consumed**. This data represents the 185 production ESXi host analysis referenced in the surrounding text, demonstrating the relationship between different memory accounting metrics and supporting the stated finding that average total capacity is ~737 GB.]

The average of all the 185 ESXi hosts have total capacity of 737 GB. This is the physical configured memory.
The metric Memory \ Usable Memory is 729 GB (not shown in above table). It’s 1% less or 8 GB than Total Capacity. I suspect this maps to Managed metric in vCenter. It is the total amount of machine memory managed by the kernel. The kernel "managed" memory can be dynamically allocated for VM, the kernel, and User Worlds. I need to check what exactly this is as I don’t see a use case for it.
The metric Memory \ VMkernel Usage is 7.6 GB (not shown in above table). This is much lower than the reservation, which is 51.6 GB.
Consumed is generally higher than the other 3 metrics. The only time it’s lower is when there is a lot of savings from shared pages.
What are these?
- Host Usage. Sum of VM Consumed. ESX System Usage is not included. Use case is only for migration, where we don’t want the ESXi consumption.
- Machine Demand. The sum of VM Utilization
- Utilization. Machine Demand + ESX System Usage. You can see that the value equals ESX System Usage when there is 0 running VM.
- Workload = Utilization against Usable

#### Reservation


| Total reservation (MB) | This is the amount reserved. Note it does not mean it’s actually used by the VM. It only counts reservation by powered on VM. It does not include powered off VM and the kernel reservation. See screenshot below. This metric is also labelled as Reserved Capacity. |
| --- | --- |
| Reservation consumed | The actual consumption. If this number if consistently lower than the reserved capacity, it indicates over reservation. |
| Reservation available | This is the amount that is not even reserved. That means it is available for new reservation. |

The following screenshot shows an ESXi where the CPU reservation was flat 0 MHz. I then set one of its VM reservation to 888 MHz. Notice the immediate yet constant change.

[Image: ## Image Description

The chart displays **CPU Reserved Capacity (MHz)** for ESXi host **10.108.38.3** over a one-hour real-time period on 03/09/2023 (5:05 PM–6:05 PM). The metric shows a flat **0 MHz** from approximately 5:10–5:55 PM, followed by an **immediate, sharp step-change to 888 MHz** that remains constant thereafter. The legend confirms Latest=888, Maximum=888, Minimum=0, and Average=163.71 MHz, demonstrating how setting a single VM's CPU reservation to 888 MHz causes an instantaneous and sustained increase in the host's total reserved capacity counter.]

Chapter 4