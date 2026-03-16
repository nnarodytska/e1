# MS Windows


## Introduction

There are 3 tools in Windows:
- Performance Monitor. This is the oldest one, and is superceded by the next two.
- Task Manager
- Resource Monitor
They use different names. It is also possible that they use different formula.
One major difference between Guest OS and VM is that Windows/Linux runs a lot of processes. The problem is there is minimal observability on these processes. For example, there is no CPU queue metric, memory page fault, network dropped packet, and disk latency at process level.
The following shows Windows Sysinternal, a great tool for Windows troubleshooting. As you can see, they are just utilization metrics. There is no contention metric.

[Image: ## Image Description

The screenshot shows **Process Monitor (Sysinternals)** with two overlaid dialogs: a **Column Selection** dialog and a **Process Timeline for firefox.exe (PID 15280)**, displaying utilization metrics including CPU Utilization (100%), File I/O Bytes (479 KB/sec), File I/O Operations (432), Registry Operations (1007), Network Bytes (100 MB/sec), Network Operations (100 ops/sec), Private Memory Bytes (367 MB), and Memory Working Set (440 MB). The main capture shows 393,284 of 1,139,942 events (34%), with TCP and Registry operations visible for firefox.exe and svchost.exe. This directly supports the surrounding text's argument that Windows process-level tooling provides **only utilization metrics** (throughput, byte counts, operation rates) with **no contention metrics** such as CPU queue length, memory page faults, network dropped packets, or disk latency at the per-process level.]


## CPU

Performance Monitor is still the main tool for Windows, despite the fact it has not been enhanced for decades. Go to docs.microsoft.com and browse for Windows Server. It took me to this article, which cover PerfMon. Many explanations on metrics at https://learn.microsoft.com/ are still based on end of life Windows.
PerfMon groups the counters under Processor group. However, it places the Processor Queue Length and Context Switches metrics under the System group. The System group covers system wide metrics, not just CPU.
The following screenshot show the counters under Processor group.

[Image: ## Image Description

The screenshot displays the **Windows Performance Monitor (PerfMon) counter selection interface**, showing the **Processor performance object group** with its available counters (% C1/C2/C3 Time, % DPC Time, % Idle Time, % Interrupt Time, % Privileged Time, % Processor Time, % User Time, C1/C2/C3 Transitions/sec, DPC Rate, DPCs Queued/sec, Interrupts/sec) in the "Added counters" panel. All counters are configured for **\<All Instances\>** (wildcard `*`), monitoring the local computer with no Parent hierarchy. This illustrates the full set of CPU-level metrics available under PerfMon's Processor group, contextualizing the subsequent table explaining each counter's meaning, while noting that **Processor Queue Length and Context Switches are absent** here because they reside under the System group instead.]

PerfMon UI provides a description, which I use as a reference below:

| % C1 Time % C2 Time % C3 Time | Based on this April 2004 article, Windows can operate in 4 different power level. The C0 is the highest, while C3 consumes the least amount of power.  If you set dynamic power management, expect the lower power to be registering higher value during idle period. Reference: here. |
| --- | --- |
| C1 Transitions/sec C2 Transitions/sec C3 Transitions/sec | The amount of time on each power level does not tell the full picture. You also need to know how frequent you enter and exit that level. These 3 metrics track the number of transitions into the respective level. For example, a high number on all 3 counters mean Windows is fluctuating greatly, resulting in inconsistent speed. |
| % DPC Time | Deferred Procedure Calls (DPC). According to this, this counter is a part of the Privileged Time (%) because DPCs are executed in privileged mode. They are counted separately and are not a component of the interrupt counters. |
| % Interrupt Time | Interrupt means the processor was interrupted from executing normal thread. This can happen for a variety of reasons, such as system clock, incoming network packets, mouse and keyboard activity. Interrupt can happen on regular basis, not just ad hoc. For example, the system clock does it every 10 milliseconds in the background.  A high interrupt value can impact performance. |
| % Processor Time % Idle Time | These 2 metrics add up to 100% |
| % User Time % Privileged Time | These 2 metrics add up to 100%.  A program’s process can switch between user mode and kernel mode (when executing system service call). This does not incur CPU context switch as it’s the same thread. As a result, I’m not seeing the use case of knowing the split between kernel mode and user mode. Reference: Windows |
| DPCs Queued/sec | Unlike the CPU Run Queue, this metric captures per processor. It can be handy to compare across processors as there can be imbalance.  Note this is a rate counter, not a count of the present queue. It tracks the speed per second. |
| DPC Rate | This is an input to the above, as the above is calculated as the delta of 2 rates, divided over sampling period. |
| Interrupts/sec | As above, but for interrupts. |


### Run Queue

Number of threads in the processor queue. Unlike Linux, Windows excludes the threads that are running (being executed).
Let’s take a VM configured with 8 vCPUs. The Guest OS sees 8 threads so it will schedule up to 8 parallel processes. If there is more demand, it will have to queue them. This means the queue needs to be accounted for in Guest OS sizing.
Because it reports the queue, this is the primary counter to measure Guest OS performance. It tells you if the CPU is struggling to serve the demand or not.
What is a healthy value?
Windows Performance Monitor UI description is not consistent with MSDN documentation (based on Windows Server 2016 documentation). The description shown in Windows UI is “Processor Queue Length is the number of threads in the processor queue. Unlike the disk counters, this counter shows ready threads only, not threads that are running. There is a single queue for processor time even on computers with multiple processors. Therefore, if a computer has multiple processors, you need to divide this value by the number of processors servicing the workload. A sustained processor queue of less than 10 threads per processor is normally acceptable, dependent of the workload.”
MSDN document states that a sustained processor queue of greater than 2 threads generally indicates processor congestion. SQL Server document states 3 as the threshold. Let me know if you have seen other recommendations from Microsoft or Linux.
Windows or Linux utilization may be 100%, but as long as the queue is low, the workload is running as fast as it can. Adding more vCPU will in fact slow down the performance as you have higher chance of context switching.
You should profile your environment, because the number can be high for some VMs. Just look at the numbers I got below. I profiled 800 VM in the last 1 month. I plotted the highest value, and these VMs have well over 3 queues per vCPU.

[Image: ## Image Description

This table displays CPU queue metrics for **16 VMs** (out of 800 profiled over 1 month), showing four columns: **Highest CPU Queue**, **Queue at 99th Percentile**, and **CPU Run at that time**. The top entries show extreme peak CPU queue values (78.75, 58.7, 46, 45.5), with color-coded indicators (red/orange/yellow/green) reflecting severity. The data demonstrates that **high peak CPU queues do not necessarily indicate CPU contention** — for example, the top VM has a peak queue of 78.75 but only 13.48% CPU utilization, while notably `pgsql...`, `xd-vd...`, and `oc-db...` show both elevated 99th percentile queues **and** high CPU run percentages (97.1%, 98.28%, 99.84%), making them the true candidates for investigation.]


| First VM | Peak queue is very high at 79 but the CPU Run was low at 13%. The queue also dropped to 14 at the 99th percentile.  Conclusion: ignore it. |
| --- | --- |
| Second VM | Peak queue is very high at 59 but the CPU Run was low at 8%. The queue also dropped to a healthy range of 2 at the 99th percentile.  Conclusion: ignore it. |
| Third VM | Peak queue is very high at 46 and the CPU Run was moderate at 56%. The queue remained elevated at 26 at the 99th percentile.  Conclusion: check the details, and then proactively share the trend charts with VM Owner |
| Forth VM | Peak queue is very high at 46 but the CPU Run was very high at 97%. The queue remained elevated at 26 at the 99th percentile.  Conclusion: check the details, and then proactively share the trend charts with VM Owner. |

Let’s drill down on the 4th VM.
The following shows the utilization is flat near 100% and the queue varied between 9 to 45.

[Image: ## Image Description

The chart displays two metrics for **pgsql-1312.tvs.vmware.com** over a ~5-hour window (4:30 PM – 9:30 PM on Friday, Sep 20): **CPU|Net Run (%)** (pink line, hovering near **97.17%** consistently) and **Guest|Peak vCPU Queue within collection cycle** (blue line, ranging from ~10 to a peak of **46 at 05:30 PM** and another spike of ~46 near 8:00 PM). The tooltip highlights the 05:30:11 PM data point where CPU Run = **97.1658%** and vCPU Queue = **44**. This demonstrates a VM under sustained near-100% CPU saturation with persistently elevated and volatile vCPU queuing, confirming the conclusion that the VM owner should be engaged to investigate application-level CPU demand behavior.]

Because of the high queue, I recommend discussing with the application team on why their application behave this way.

#### Queue and Idle

It is possible that Guest OS shows high CPU queue when it was idling. This is abnormal, indicating the application created a lot of threads. The following shows the application was idling while having high queue.

[Image: ## Image Description

The chart displays two metrics over a full day (September 5): **Guest OS CPU Queue** (blue) and **CPU|Net Run %** (pink/purple), with the CPU Queue peaking at **13.5** at 08:28:33 AM while CPU Net Run sits at only **0.9535%**. The blue CPU Queue spikes appear multiple times throughout the day (notably at ~02:00 AM, ~07:00 AM, ~08:28 AM, and ~12:00 PM) reaching values up to ~10, while the pink CPU usage line remains consistently near zero. This demonstrates the **"Queue and Idle" anomaly** described in the surrounding text — the Guest OS reports high CPU run queue spikes despite near-zero actual CPU utilization, indicating abnormal thread behavior by the application rather than genuine CPU contention.]

The CPU Run Queue spikes multiple times. It does not match the CPU Usage. It also did not match CPU Context Switch Rate pattern. The spike only last 20 seconds, as the 5-minute average shows identical pattern but much smaller number.

[Image: The image displays two vSphere metrics charts for **MA-TMM-AUTO-WIN2K22-Cloudbase-init-Template** over a ~24-hour period (Sep 5–6): **Guest|CPU Queue** (peaking at ~0.9) and **Guest|Peak vCPU Queue within collection cycle** (peaking at ~13.5). Both charts show sharp, intermittent spikes — most notably around **08:00–09:00 AM** — against an otherwise near-zero baseline. This illustrates the described anomaly where the VM exhibits high CPU queue spikes that are transient (~20 seconds, evidenced by the 5-minute average showing much smaller values) and do not correlate with sustained CPU usage, indicating thread contention rather than underlying host-level resource pressure.]

The following is a 2 vCPU VM running Photon OS. CPU Queue is high, even though Photon is only running at 50%. Could it be that the application is configured with too many threads that the CPU is busy doing context switching? Notice the CPU Queue maps the CPU Context Switch Rate and CPU Run. In this situation, you should bring it up to the application team attention, as it may cause performance problem and the solution is to look inside. As a proof that it’s not because of underlying contention, I added CPU Ready.

[Image: ## Image Description

The image displays a **VMware vSphere performance dashboard** for a 2-vCPU VM showing four metrics over approximately 24 hours (Feb 23–25): **Guest|CPU Queue** (peak H: 54.07, low ~0), **CPU|Run in ms** (H: 20,685.73ms, L: 5,369.73ms), **Guest|CPU Context Switch Rate** (H: 2,847.93, L: 2,057.27), and **CPU|Ready in ms** (H: 176.47ms, L: 7.27ms).

The first three metrics show **strong visual correlation** — the periodic spike patterns of CPU Queue, CPU Run, and Context Switch Rate are nearly identical, demonstrating that high CPU queuing is driven by excessive thread context switching rather than CPU saturation.

Critically, **CPU Ready remains near zero** until approximately 4:00–8:00 PM on Feb 24 (peaking at 176.47ms), confirming there is **no underlying host-level contention** — the CPU Queue issue is application-internal, supporting the recommendation to engage the application team.]

What is the behaviour of CPU Queue? I profiled 800 VM in the last 1 month. For each VM, I extracted the peak value and the 99th percentile value. From the following scatter chart, you can see that the value at 99th percentile is less than half. Using a spreadsheet, the average value of the 99th percentile is 34% for peak that is ≥ 3.

[Image: ## Scatter Plot: CPU Queue Peak vs. 99th Percentile Analysis

This scatter chart plots **peak CPU queue values (x-axis) against 99th percentile values (y-axis)** across ~800 VMs sampled over one month. The data shows a clear pattern where **99th percentile values are consistently less than half of peak values** — for example, peaks reaching 40-50 have 99th percentile values below 10, and the dense cluster of VMs (x: 0-15, y: 0-8) confirms most VMs maintain low queue depths. The chart visually validates the stated finding that **the average 99th percentile is ~34% of the peak** for peaks ≥ 3, demonstrating that CPU queue spikes are transient outliers rather than sustained contention events.]

BTW, the value from Guest OS displays the last observed value only; it is not an average. Windows & Linux do not provide the highest and lowest variants either.
The counter name in Tools is guest.processor.queue. For Windows, it is based on Win32_PerfFormattedData_PerfOS_System = @#ProcessorQueueLength from WMI
Reference: Windows
I can’t find documentation that states if CPU Hyper Threading (HT) technology provides 2x the number of queue length. Logically it should as the threads are at the start of the CPU pipelines, and both threads are interspersed in the core pipeline.

#### CPU Priority

If a process is often in queue, one possility is it has lower relative priority. Priority is a concept of Windows that ESXi does not have. ESXi uses a fair-share scheduler instead, as it does not have foreground processes.
Windows or Linux provides priority for foreground activities, as that’s what the user experience. For Windows, there are 6 levels as shown below. Ensure all your agents are given lower priority and limited CPU resource.

[Image: The image shows a **Windows Task Manager context menu** demonstrating the six CPU priority levels available in Windows: Realtime, High, Above Normal, **Normal** (currently selected, indicated by the bullet point), Below Normal, and **Low** (highlighted). The screenshot illustrates the "Set priority" submenu accessed by right-clicking on processes (Acrobat.exe and AcroCEF.exe instances visible), with "Low" priority highlighted as the recommended setting. This supports the surrounding text's guidance that background agents/processes should be assigned **lower priority levels** to minimize their CPU resource consumption relative to foreground workloads.]


### Context Switch

CPU Context Switch costs performance “due to running the task scheduler, TLB flushes, and indirectly due to sharing the CPU cache between multiple tasks”. It’s important to track this counter and at least know what’s an acceptable behaviour for that specific application.
Context switches are considered “expensive” operations, as the CPU can complete many instructions within the time taken to switch context from one process to another. If you are interested, I recommend reading this paper.
Based on Windows 10 Performance Monitor documentation, context switches/sec is the combined rate at which all processors on the computer are switched from one thread to another. All else being equal, the more the processors, the higher the context switch. Note that thread switches can occur either inside of a single multi-thread process or across processes. A thread switch can be caused either by one thread asking another for information, or by a thread being pre-empted by another, higher priority thread becoming ready to run.
There are context switch metrics on the System and Thread objects. VCF Operations only report the total.
The rate of Windows or Linux switching CPU context per second ranges widely. The following is taken from a Windows 10 desktop with 8 physical threads, which runs around 10% CPU. I observe the value hovers from 10K to 50K.

[Image: ## Image Description

This is a **Windows Performance Monitor chart** displaying **CPU Context Switches/sec** over a ~1:40 duration window around **2:06-2:07 PM**, showing values that fluctuate between a **minimum of 9,235 and a maximum of 53,586 switches/sec**, with an average of **16,509** and last value of **12,164**. The metric exhibits a largely stable baseline of ~10,000-15,000 switches/sec with periodic spikes, the most prominent reaching ~53,586 (marked by a vertical red cursor line). This chart serves as the real-world baseline reference for a Windows 10 desktop at ~10% CPU utilization, establishing the expected context switch range (10K–50K/sec) before the author discusses its variable correlation with CPU utilization across 3,328 VMs.]


#### Correlation

The value does not always correlate with CPU “utilization”, because not all CPU instructions require context switching. Overall, the higher the utilization the higher the chance of CPU context switch. I plotted 3328 VM on a scatter chart.

[Image: ## Image Description

This scatter plot charts **CPU Usage (GHz) on the Y-axis (0–90)** against **CPU Context Switch count on the X-axis (0–600,000)** across **3,328 VMs**. The data shows a heavy concentration of points clustered at low context switch values (0–100,000) with CPU usage mostly below 30 GHz, with sparse outliers extending to ~600,000 context switches maintaining relatively low CPU usage (~20 GHz). This demonstrates the **weak/non-linear correlation** between CPU utilization and context switch rate referenced in the surrounding text — high context switches can occur without proportionally high CPU usage, and vice versa.]

The above does not mean there is no correlation. The following chart shows a near perfect corelation. Every time CPU Usage went up, CPU Context Switch also. I should have plotted the disk IO or network IO as IO operations tend to require context switch.

[Image: ## Image Description

The image displays two time-series charts for a VM ("prod-app-a1") spanning **February 18–25**: **CPU Usage (%)** with a high of **100%** and low of **49.82%**, and **Guest CPU Context Switch Rate** with a high of **3,022.33** and low of **599.6**. Both charts exhibit **near-identical spike patterns** at the same timestamps throughout the week, demonstrating the strong correlation referenced in the surrounding text — every time CPU usage spiked toward 100%, the context switch rate correspondingly spiked toward or above **2K switches**, visually confirming that elevated CPU utilization drives increased CPU context switching activity.]

CPU context switch can happen even in a single thread application. The following shows a VDI VM with 4 vCPU. I plotted the CPU Usage Disparity vs CPU Context Switch. You can see the usage disparity went up to 78%, meaning the gap between the busiest vCPU and the idlest vCPU is 78%. This was running a security agent, which is unlikely to be designed to occupy multiple vCPU.

[Image: ## Image Description

The chart displays **CPU|vCPU Usage Disparity (%)** for a VM over approximately 6 days (May 13–19), showing the percentage gap between the busiest and idlest vCPU. The metric reaches a **high of 78.46%** with a prominent spike visible around May 15 (evening), while the **low is 0.036%**, with the baseline remaining near zero for most of the period. This demonstrates the context referenced in the surrounding text — a security agent causing uneven vCPU load distribution, with the 78% disparity indicating the workload was largely single-threaded rather than utilizing all 4 vCPUs efficiently.]

Let’s plot the context switch at the same period. There is a spike at the same time, indicating that the agent was busy context switching. Note that it does not always have to be this way. The red dot shows there is no spike in context switch even though the vCPU Usage Disparity went up.

[Image: ## Guest|CPU Context Switch Rate Chart

The chart displays the **CPU Context Switch Rate** for a Guest VM from May 13-19, showing a dramatic spike reaching **H: 14,254.8** (highlighted in orange) around May 15-16, against an otherwise low baseline with a minimum of **L: 513.8**. The spike correlates with the vCPU Usage Disparity event discussed in the preceding text, while the **red dot** (positioned slightly before the spike) illustrates a counterexample where vCPU Usage Disparity increased *without* a corresponding context switch spike. The chart demonstrates that high context switching and vCPU disparity can be correlated but are not always causally linked.]


#### Range Analysis


[Image: ## Image Description

The chart displays **CPU Context Switch** metrics for a VM over the period of **May 4–11**, with values ranging between a minimum of **9,792,877** and a maximum of **12,199,200** context switches. The time series shows relatively sustained high values (oscillating around **11,500K–12,000K**) with periodic sharp downward spikes dropping as low as ~**9,800K**, and two orange dots highlighting notable anomalies — a **minimum point (~9,800K) around May 8** and a **maximum point (~12,200K) around May 10–11**. This chart demonstrates that the VM sustains extremely high context switch rates (well above 10 million) without necessarily correlating to high CPU usage or heavy IOPS, supporting the text's argument that application-specific baseline profiling is critical for interpreting this metric.]

The values of CPU Context Switch vary widely. For many VM, the values will be in low hundreds. In extreme situation, it can sustain well beyond 10 millions, as shown in the preceding chart. The above VM was not doing heavy IOPS nor high CPU usage. There was no correlation with these 2 metrics either.
Because of above, it’s important to profile and establish a normal base line for that specific application. What is healthy for 1 VM may not be healthy for another.

[Image: This table displays CPU Context Switch metrics for multiple VMs, showing **Worst Value, Value at 95th Percentile, Average Value, Average CPU Queue, and Configured CPU**. The data highlights significant variance across VMs: two "_old" VMs (4 vCPU each) show dangerously high 95th percentile values of **873,558 and 820,889** (underlined in red), while one VM labeled "1_old" shows a notably low 95th percentile of **3,796** (highlighted in green), indicating only a momentary burst rather than sustained high context switching. This contrast illustrates the text's point that sustained vs. transient context switch spikes must be distinguished, and that 95th-99th percentile values are more meaningful than worst-case peaks for identifying genuine performance problems.]

You can see from the table that some VM experience prolonged CPU context switch, while others do not. The VM #4 only has a short burst as the value at worst 5th percentile dropped to 3796. Momentary peak of context switch may not cause performance problem so in general it’s wiser to take the value somewhere between 95th and 99th percentile.
Let’s drill down to see the first VM. This CentOS VM sporting only 4 vCPU constantly hit almost 1 million context switches. The pattern match CPU Usage.

[Image: The image displays three performance metrics for a CentOS VM (4 vCPU) from March 7–8: **Guest CPU Context Switch Rate** (peaking at ~982,603/sec), **CPU Usage %** (peaking at ~98.19%), and **Guest CPU Queue** (peaking at ~2.55). All three metrics show a sharp, sustained spike beginning around **12:00–1:00 PM on March 7**, jumping from near-baseline values (lows of ~192, 0.2%, and 0.033 respectively) to near-maximum levels that persist continuously through March 8. The image demonstrates the correlation between near-100% CPU saturation and extremely high context switch rates, while the CPU queue remaining below 3 supports the surrounding text's argument that adding vCPUs is unnecessary despite the high context switch rate.]

Do you add more CPU?
You should not, as the queue remain manageable. Check what the queue like on a more granular reading.
The following distribution chart shows the values from 11372 VMs. I had to use log-10 scale as the values vary wildly.

[Image: ## CPU Context Switch: Values Distribution Chart

This log-scale chart displays the distribution of CPU context switch values across **11,372 VMs**, with the Y-axis ranging from 10 to 1,000,000 (log-10 scale) and the X-axis representing ranked VMs (1 to ~11,400). The curve shows a steep power-law decline, starting near **~700,000** context switches for the highest VM and dropping to approximately **~30** at the tail end. The chart demonstrates the extremely wide variance in CPU context switch rates across the VM population, justifying the log scale, and contextually supports the observation that roughly **80% of VMs fall below 10,000** context switches.]

Majority of Guest OS spends well below 10K. You can see that the values between 0 – 10000 accounts for 80%.
Now that you know the wide distribution, you can use buckets. Adjust the bucket size by grouping all the values above 10K as one bucket, and splitting 0 – 10K bucket into multiple buckets. You can see more than half has < 1000 CPU Context Switch Rate.

[Image: ## Pie Chart: CPU Context Switch Rate Distribution

This pie chart displays the distribution of CPU Context Switch Rate across **2,197 VMs** (a subset), broken into 6 buckets ranging from 0 to 200,000. The largest segments are **500–1,000 (25.94%)** and **100–500 (25.85%, = 568 VMs)**, followed by **1,000–5,000 (21.76%)**, confirming that the majority of VMs have context switch rates below 1,000. The chart visually supports the surrounding text's claim that **over 50% of VMs have fewer than 1,000 CPU Context Switches**, with the 10,000–200,000 range (10.79%) and 5,000–10,000 (9.42%) representing a smaller tail of higher-activity VMs.]


#### Thread Ping Pong

The following is a Windows Server 2019 DC edition VM with 10 vCPU. It’s basically idle, as you can see below.

[Image: ## Image Description

This chart displays **CPU utilization (or a similar performance metric) for a Windows Server 2019 VM with 10 vCPUs** over a roughly 24-hour period (Nov 2 ~3:30 PM to Nov 3 ~4:00 PM), showing an overall **high value near 75.39 (H)** and a **low of 37.76 (L)**. The metric appears relatively flat and near-idle at the aggregate level, with periodic sharp downward spikes throughout the timeframe. This demonstrates the concept described in the surrounding text — that while the **overall VM-level metric appears essentially idle/stable**, the underlying per-vCPU behavior is masked at this aggregated view, setting up the subsequent discussion of individual vCPU "ping pong" behavior.]

But if we zoom into each vCPU, they are taking turn to be busy.
In the span of just 1 hour, the 10 vCPU inside Windows take turn.

[Image: ## Image Description

This line chart displays **individual vCPU utilization metrics for 10 vCPUs** on a Windows Server 2019 VM over approximately one hour (1:30 PM – 2:25 PM). Each colored line represents a separate vCPU, showing highly volatile, alternating utilization patterns where different vCPUs spike at different times. This demonstrates the **thread ping-pong behavior** described in the surrounding text — the vCPUs are taking turns becoming active rather than distributing load evenly, indicating a process/thread scheduling anomaly on the Horizon Connection Server workload.]

This is a bit illogical. Is this a process ping pong?
It is hard to tell
We can see them clearer if we stack them up. Notice they take turn, except the 3rd one from the top (I drew a green line on it). That one is actually fairly stable.

[Image: ## Image Description

This stacked area chart displays **10 individual vCPU utilization metrics** for a Windows VM (running Horizon Connection Server) from approximately **1:30 PM to 2:22 PM**, with each vCPU represented by a different colored band. The **red dots mark peak utilization points** for individual vCPUs, demonstrating a clear **round-robin/ping-pong pattern** where vCPUs take turns spiking in activity rather than loading simultaneously. The **green line highlights the 3rd vCPU from the top**, which remains notably stable compared to the others, visually confirming the "process ping pong" behavior described in the surrounding text while one vCPU maintains consistent utilization.]

It is running Horizon Connection Server. It has around 118 – 125 processes, but much higher threads counts.

[Image: The image displays two monitoring charts for **Windows OS on Connection-server-01-81**: the top chart shows **System|Processes** ranging between a low of **118** and high of **125**, while the bottom chart shows **System|Threads** ranging between a low of **2,194** and high of **2,299**. Both metrics are tracked over approximately a 24-hour period (Nov 2 ~3:00 PM to Nov 3 ~3:00 PM). This illustrates the point in the surrounding text that the Horizon Connection Server maintains a relatively stable but disproportionate ratio — roughly **120 processes** supporting over **2,200+ threads** — running on just 10 vCPUs, which directly sets up the subsequent discussion of context switching behavior (~3.5K switches/CPU/second).]

CPU Run Queue is very low, which is expected as the system is basically idle.
Context switches is fairly steady. The following screenshot shows it hovers between 34K and 37K switches per second. This is expected as it consistently run >2K threads on >100 processes on just 10 CPU. Each CPU does ~3.5K switches per second.

[Image: The image displays two time-series charts for **Windows OS on Connection-server-01-81** covering approximately 01:45 PM to 02:55 PM. The top chart shows **System|Context Switches per second** fluctuating between a low of **34,107.99** and a high of **37,150.49**, demonstrating relatively steady switching activity consistent with the server running 2K+ threads across 100+ processes on 10 CPUs (~3.5K switches/CPU/sec). The bottom chart shows **System|Processor Queue Length** remaining at **0** (low of 0, high of 2) for nearly the entire period with only a brief spike to 2 near 02:40 PM, confirming the system is effectively idle from a CPU scheduling perspective.]


### DPC Time

According to System Center wiki, the system calls are deferred as they are lower priority than standard interrupts. A high percentage of deferral means Windows was busy doing higher priority requests.
They can happen even during low CPU utilization if there is issue with driver or application. The following screenshot is taken on Performance Monitor in Windows 11 laptop which was not running high. Notice the DPC time for CPU 0 is consistently higher than CPU 15, indicating imbalance. It did exceed >5% briefly. My Dell laptop has 8 cores 16 threads.

[Image: ## Performance Monitor Screenshot Analysis

The image shows a **Windows Performance Monitor** graph tracking **% DPC Time** across three instances on **\\DELL-5560**: the `_Total` processor (red), CPU core `0` (green), and CPU core `15` (blue), all at scale 1.0 over a **1:40 duration**. The statistics show a **Last: 0.000%, Average: 0.573%, Minimum: 0.000%, Maximum: 6.174%**, with the green line (CPU 0) showing consistently higher and more frequent DPC spikes compared to the nearly flat blue line (CPU 15). This demonstrates **CPU-level DPC imbalance** — CPU 0 repeatedly handles more deferred procedure calls than CPU 15, briefly exceeding the 5% threshold (~6.174% peak), indicating a potential driver or interrupt affinity issue on an 8-core/16-thread Dell system.]

Set the graph scale to 1 for ease of reading, and change the axis scale accordingly.

### Runaway Process

What do you see from the CPU charts below?

|  | There are 8 CPU as seen by Windows 10. Hint: look at the total picture, no need to see each in detail. That’s why I made the screenshot tiny.  Yes, you’re right. CPU0 is running flat. The reason was one of Windows common service went into infinite loop. Ironically, this is the troubleshooting service (Diagnostic Policy Service) itself. So it’s chewing up CPU flat out non-stop. But since there are 7 other CPU, Windows overall is responsive. I could still do my work.   A counter that tracks at entire Guest OS level will not capture it. You need to complement it with a counter that tracks the highest among its CPU. If this is flat out all the time, you likely have a runaway process. |
| --- | --- |


### Usage | Utilization | Time

The 3 tools in Windows use different names to measure CPU consumption:
- Performance Monitor uses the name Processor Time.
- Task Manager uses the name CPU Utilization.
- Resource Monitor uses the name CPU Usage.
Looking at the values, they are not measuring the same thing. The following screenshot is a side-by-side comparison between Task Manager and Resource Monitor.

[Image: ## Image Description

The image shows a **side-by-side comparison** of **Windows Task Manager** (left) and **Resource Monitor** (right), both displaying CPU metrics for the same **Intel Core i7-12800H** system at the same moment. Task Manager reports **9% CPU Utilization** at **2.84 GHz**, while Resource Monitor displays **CPU - Total** and **Service CPU Usage** graphs separately. The comparison demonstrates that despite measuring the same physical CPU activity, the two tools use **different nomenclature** (Utilization vs. Usage) and display **different granularity** — Resource Monitor separates service CPU consumption from total CPU consumption, illustrating that these Windows tools do not measure identical metrics despite appearing functionally similar.]

Let’s compare Performance Monitor and Task Manager:

[Image: The image shows a side-by-side comparison of **Resource Monitor** (left, red graph) and **Task Manager** (right, blue graph) measuring CPU activity over approximately 1 minute 40 seconds. Resource Monitor displays CPU Usage with a last value of **17.510%**, average of **16.778%**, minimum of **3.838%**, and maximum of **36.461%**, while Task Manager shows **18% utilization** at **2.10 GHz** on a 2.40 GHz base speed socket. Despite measuring the same CPU activity simultaneously, the two tools display slightly different values, demonstrating that **Windows CPU measurement tools use different methodologies** and do not report identical metrics even when monitoring the same workload.]

CPU Usage in Windows is not aware of the underlying hypervisor hyper-threading. When Windows run a CPU at 100% flat, that CPU could be competing with another physical thread at ESXi level. In that case, what do you expect the value of VM CPU Usage will be, all else being equal?
62.5%.
Because that’s the hyper-threading effect.
What about VM CPU Demand? It will show 100% .
However, CPU Usage is affected by power management. Windows 8 and later will report CPU usage >100% in Task Manager and Performance Monitor when the CPU Frequency is higher than nominal speed. The reason for the change is the same with what we have covered so far, which is the need to distinguish amount of work being done. More here.

[Image: The Windows Resource Monitor screenshot displays **105% CPU Usage** and **134% Maximum Frequency**, with CamtasiaStudio.exe consuming 38 CPU units as the top process. This demonstrates how Windows reports CPU usage exceeding 100% when the processor runs above its nominal clock speed due to CPU frequency scaling (Turbo Boost). The discrepancy between 105% usage and 134% maximum frequency indicates the CPU was not running at boosted speed continuously — if it had run at 134% the entire time, CPU Usage would have reported 134% rather than 105%.]

BTW, what does the Maximum Frequency mean?
Let’s show an opposite scenario, where CPU Usage (%) is low.

[Image: The image shows **Windows Resource Monitor's CPU tab** displaying **8% CPU Usage** and **69% Maximum Frequency**, with two processes visible: Secure System (PID 280) and SystemSettings.exe (PID 69464), both in a **Suspended** state with 0 CPU utilization. This screenshot demonstrates the **low utilization/power conservation scenario** described in the surrounding text, where Windows reduces CPU frequency below nominal speed (69% of rated clock speed) to conserve power during idle periods. The 69% Maximum Frequency illustrates how power management downclocks the CPU, meaning the actual productive work completed is proportionally less than even the reported 8% usage figure would suggest.]

The number means the speed it’s running relative to the nominal frequency. During low utilization, Windows will conserve power by lowering the speed.
In the first screenshot, since it’s running at 134% of the clock speed, the total time exceeded 105%, meaning there were time it did not run. Had it run all the time, it would report 134% instead.
In the first screenshot, it could be running more than 8% of the time. But since it’s only running at 69% of the speed, the CPU productive cycle completed is only 8%. The througput was degraded.
What happens to CPU Usage when VM is experiencing contention? VM Contention = Ready, Co-Stop, Overlap, Other Wait.
Time basically stops. So there is a gap in the system time of Windows. How does it deal with the gap? Does it ignore the gap, or artificially fills it with best guess values? I’m not sure. If you do let me know.
The above nature of CPU Usage brings an interesting question. Which VM counters can be used when you have no visibility into the Guest? Let’s do a comparison:

| Metric | Frequency Scaling | Hyperthreading | VM Contention |
| --- | --- | --- | --- |
| Guest CPU Usage | Yes | No | No |
| VM CPU Run | No | Yes | No |
| VM CPU Usage | Yes | Yes | No |
| VM CPU Demand | Yes | No | Yes |

If there is slowness but utilization is low, it’s worth checking if the utilization is coming from lower power state. This is important for application that requires high frequency (as opposed to just lots of light threads).
Windows provides the time the CPU spent on C1, C2 and C3 state. The following is taken from my laptop. Notice a dip when the total of C1 + C2 + C3 < 100%. That’s basically the time on C0.

[Image: ## Image Description

The Windows Performance Monitor screenshot displays three CPU C-state metrics (% C1 Time in red, % C2 Time in green, % C3 Time in blue) for a Dell-5560 system over a ~1:40 duration. The **% C3 Time (blue) dominates at 85-94%** (Average: 86.963, Min: 44.466, Max: 94.446), while C1 and C2 remain near 0%, with occasional green spikes reaching ~11%. The chart demonstrates that **dips in C3 time (notably dropping to ~44% at one point) represent CPU transitioning to C0 (active execution state)**, illustrating how low CPU utilization metrics can mask performance issues when processors are spending time in low-power states rather than actively processing workloads.]

The Idle loop is typically executed on C3. Try plotting the Idle Time (%) and C3 Time (%), and they will be similar.

#### OS vs Process

CPU imbalance can happen in large VM.
Review the following chart carefully. It’s my physical desktop running Windows 10. The CPU has 1 socket 4 cores 8 threads, so Windows see 8 logical processors. You can see that Microsoft Word is not responding as its window is greyed out. The Task Manager confirms that by showing that none of the 3 documents are responding. Word is also consuming a very high power, as shown in the power usage column.
It became unresponsive because I turned on change tracking on a 500 page document and deleted hundreds of pages. It had to do a lot of processing and it did not like that. Unfortunately I wasn’t able to reproduce the issue after that.
At the operating system, Windows is responding well. I was able to close all other applications, and launched Task Manager and Snip programs. I suspect because Word does not consume all CPUs. So if we track at Windows level, we would not be aware that there is a problem. This is why process-level monitoring is important if you want to monitor the application. Specific to hang state, we should monitor the state and not simply the CPU consumption.
From the Windows task bar, other than Microsoft Word and Task Manager, there is no other applications running. Can you guess why the CPU utilization at Windows level is higher than the sum of its processes? Why Windows show 57% while Word shows 18.9%?

[Image: ## Image Description

The screenshot shows **Windows Task Manager** with Microsoft Word (3 instances) in a **"Not Responding"** state, consuming **18.9% CPU and 413.1 MB memory**, while the overall Windows CPU utilization displays **57%** — a significant discrepancy. The Power Usage column shows **"Very high"** (highlighted in red/orange) for the Word process group, despite only 3% disk and 0% GPU utilization. This illustrates the book's core point: process-level CPU metrics (18.9%) dramatically underreport actual CPU consumption (57%) when **CPU Turbo Boost** or a **CPU lock condition** is involved, making OS-level and per-vCPU peak monitoring essential for accurate performance diagnosis.]

My guess is Turbo Boost. The CPU counter at individual process level does not account for it, while the counter at OS level does.
I left it for 15 minutes and nothing change. So it wasn’t that it needed more time to process the changes. I suspect it encountered a CPU lock, so the CPU where Word is running is running at 100%. Since Windows overall only reports 57%, it’s important to track the peak among Windows CPU. This is why VCF Operations provides the peak value among the VM vCPU.

## Memory

Windows memory management is not something that is well documented. Ed Bott sums it this article by saying “Windows memory management is rocket science”. Like what Ed has experienced, there is conflicting information, including the ones from Microsoft. Mark Russinovich, cofounder of Winternals software, explains the situation in this TechNet post.
Windows Performance Monitor provides many metrics, some are shown below.

[Image: ## Image Description

This screenshot shows the **Windows Performance Monitor (PerfMon) counter selection interface**, displaying the **Memory performance object** and its available counters. The left panel shows Memory counters including **Available Bytes, Available KBytes, Available MBytes, Cache Bytes, Cache Faults/sec, and Commit Limit**, while the right panel shows the full list of Memory counters with their Parent relationships (all showing "---"), including metrics like **% Committed Bytes In Use, Page Faults/sec, Page Reads/sec, Page Writes/sec, Pages Input/sec, and Pages Output/sec**. This image contextualizes the surrounding text's discussion of Windows memory metrics by illustrating the breadth of available memory counters that can be monitored, several of which (Available Bytes/KBytes/MBytes, Cache Bytes) are directly referenced in the subsequent definitions of **Cached** and **Available** memory formulas.]

In formula, here is their definition:
- Cached = Standby + Modified
- Available = Standby + Free
Available means exactly what the word means. It is the amount of physical memory immediately available for use. Immediately means Windows does not need to copy the existing page before it can be reused.
It is easier to visualize it, so here it is:

[Image: ## Image Description

The image shows a **Windows Resource Monitor Physical Memory breakdown** with 8192 MB installed (8017 MB total usable), displaying memory segments: Hardware Reserved (175 MB), In Use (3451 MB), Modified (194 MB), Standby (1159 MB), and Free (3213 MB), with Available = 4372 MB and Cached = 1353 MB.

Two annotated arrows visually demonstrate the relationships defined in the surrounding text: the **"Cached" arrow** spans the Modified + Standby segments, and the **"Available" arrow** spans the Standby + Free segments — directly illustrating the formulas **Cached = Standby + Modified** and **Available = Standby + Free**.]

Microsoft SysInternal provides more detail breakdown. In addition to the above, it shows Transition and Zeroed.

[Image: ## RamMap Screenshot Description

This RamMap (Sysinternals) screenshot displays a detailed **physical memory breakdown** of a Windows system with **16,620,388 K (~16 GB) total RAM**, showing usage categories including Process Private (6,073,792 K), Mapped File (2,302,968 K), and Unused (5,409,416 K). Key memory state columns show **Active: 7,344,668 K**, **Standby: 2,465,152 K**, **Modified: 1,401,000 K**, **Zeroed: 1,533,088 K**, and **Free: 3,876,328 K**, which directly illustrates the formulas defined in the surrounding text (Available = Standby + Free ≈ **6,341,480 K**; Cached = Standby + Modified ≈ **3,866,152 K**). The image demonstrates the more granular memory categorization that RamMap provides compared to standard Windows Task Manager, including the additional **Transition** and **Zeroed** states referenced in the surrounding text.]


### In Use

This is the main counter used by Windows, as it’s featured prominently in Task Manager.

[Image: ## Image Description

This is a **Windows Task Manager Memory performance panel** showing a system with **32.0 GB total RAM**, currently using **20.5 GB (with 3.2 GB compressed)** and **10.9 GB available**, running at **4800 MHz across 2 SODIMM slots**. The memory usage graph shows a **nearly flat line near the bottom** over 60 seconds, indicating stable, low utilization relative to total capacity, with only **417 MB free** (highlighted in the memory composition bar). In the context of the surrounding text, this screenshot illustrates the **"In Use"** metric in Task Manager — the primary Windows memory counter — demonstrating that Windows is compressing active pages (3.2 GB compressed) even while substantial available memory exists, contrasting with ESXi's compression behavior.]

This is often thought as the minimum that Windows needs to operate. This is not true. If you notice on the preceding screenshot, it has compressed 457 MB of the 6.8 GB In Use pages, indicating they are not actively used. Windows compresses its in-use RAM, even though it has plenty of Free RAM available (8.9 GB available). This is a different behaviour to ESXi, which do not compress unless it’s running low on Free.
Look at the chart of Memory Usage above. It’s sustaining for the entire 60 seconds. We know this as the amount is too high to sustain for 60 seconds if they are truly active, let alone for hours.
Formula:
In use = Total – (Modified + Standby + Free)
A problem related to the In Use counter is memory leak. Essentially, the application or process does not release pages that it no longer needs, so over time it accumulates. This is hard to detect as the amount varies by application. The process will continue growing until the OS runs out of memory.
Take note this is a new metric in VCF Operations 8.6. We call it Used Memory. You’re welcome.

### Modified

Page that was modified but no longer used, hence it’s available for other usage but requires to be saved to disk first. It’s not counted as part of Available, but counted as part of Cache.
OS does not immediately write all inactive pages to disk, especially if the disk is on power saving mode. It will consolidate these pages and write them in one shot, minimizing IO to the disk. In the case, of SSD disk, it can shorten the life span as SSD has physical limits on the number of writes.

### Standby

Windows has 3 levels of standby. As reported by VMware Tools, their names are:
- Standby Core
- Standby Normal
- Standby Reserve
Different applications use the memory differently, resulting in different behaviour of the metrics. As a result, determining what Windows actually uses is difficult.
The Standby Normal counter can be fluctuating wildly, resulting in a wide difference if it’s included in rightsizing. The following VM is a Microsoft Exchange 2013 server mailbox utility.

[Image: ## Image Description

The chart displays VMware guest memory metrics for a **Microsoft Exchange 2013 mailbox server** over approximately **3 months (April 8 – July 5)**, showing five metrics: Guest Physically Usable Memory (pink, flat ~30M KB), Guest Needed Memory (gray, near zero), and three Standby memory counters. **Standby Normal (purple)** dominates and fluctuates dramatically — dropping from ~25M KB to as low as ~5-8M KB during several sharp dips (around May 2, May 18, May 30, June 7, and late June) before recovering, while **Standby Reserve and Standby Core (teal/blue)** remain consistently negligible near zero throughout. This demonstrates the key point from the surrounding text: Standby Normal can fluctuate wildly (spanning nearly the full usable memory range), making it unreliable as a sole metric for VM rightsizing calculations.]

Notice the Standby Normal fluctuates wildly, reaching as high at 90%. The other 2 cache remains constantly negligible. The chart above is based on >26000 samples, so there is plenty of chance for each 3 metrics to fluctuate.
Now let’s look at another example. This is a Windows Server 2016. I think it was running Business Intelligence software Tableau.

[Image: ## Image Description

The chart displays four memory metrics for a Windows Server 2016 VM over approximately 3 months (April 8 – July 5): **Guest Physically Usable Memory (KB)** (purple), and three standby memory metrics — **core**, **normal**, and **reserve** (various blues/cyan). Around **May 22**, the purple line doubles abruptly (approximately **2x increase** in usable memory), while **Standby Reserve** (dark blue) correspondingly jumps and exhibits high-amplitude fluctuations reaching ~**4GM**, whereas **Standby Normal** remains relatively flat near the baseline. This demonstrates that when VM memory was expanded, the Reserve cache absorbed the additional memory rather than Normal cache, with the reserve metric fluctuating wildly in sawtooth patterns throughout the observation period.]

Notice the VM usable memory was increased 2x in the last 3 months. Standby Normal hardly move, but Standby Reserve took advantage of the increments. It simply went up accordingly, although again it’s fluctuating wildly.

### Cache

Cache is an integral part of memory management, as the more you cache, the lower your chance of hitting a cache miss. This makes sense. RAM is much faster than Disk, so if you have it, why not use it? Remember when Windows XP introduced pre-fetch, and subsequently Windows SuperFetch? It’s a clue that memory management is a complex topic. There are many techniques involved. Unfortunately, this is simplified in the UI. All you see is something like this:

[Image: ## Windows Resource Monitor – Memory Tab

The screenshot displays the **Windows Resource Monitor Memory tab**, showing process-level memory metrics (Hard Faults/sec, Commit, Working Set, Shareable, and Private KB) alongside a **Physical Memory summary** indicating **42% utilization** (6,992 MB In Use out of 16,384 MB installed). The Physical Memory breakdown shows **Hardware Reserved: 113 MB, Modified: 176 MB, Standby: 5,922 MB, and Free: 3,181 MB**, with 9,103 MB available (including cached memory of 6,098 MB). In context, this image illustrates the **simplified cache representation** in the Windows UI, where "Cached" (6,098 MB) combines Standby memory — demonstrating that a relatively low "Free" value (3,181 MB) is not concerning given the large Standby/cache pool available.]


### Free

As the name implies, this is a block of pages that is immediately available for usage. This excludes the cached memory. A low free memory does not mean a problem if the Standby value is high. This number can reach below 100 MB, and even touch 0 MB momentarily. It’s fine so long there is plenty of cache. I’d generally keep this number > 500 MB for server VM and >100 MB for VDI VM. I set a lower number for VDI because they add up. If you have 10K users, that’s 1 TB of RAM.
When Windows or Linux frees up a memory page, it normally just updates its list of free memory; it does not release it. This list is not exposed to the hypervisor, and so the physical page remains claimed by the VM. This is why the Consumed counter in vCenter remains high when the Active counter has long dropped. Because the hypervisor has no visibility into the Guest OS, you may need to deploy an agent to get visibility into your application. You should monitor both at the Guest OS level (for example, Windows and Red Hat) and at the application level (for example, MS SQL Server and Oracle). Check whether there is excessive paging or the Guest OS experiences a hard page fault. For Windows, you can use tools such as pfmon, a page fault monitor.
This is one the 3 major metrics for capacity monitoring. The other 2 metrics are Page-in Rate and Commit Ratio. These 3 are not contention metrics, they are utilization metrics. Bad values can contribute to bad performance, but they can’t measure the severity of the performance. Windows and Linux do not have a counter that measures how long or how often a CPU waits for memory.
In Windows, this is the Free Memory counter. This excludes the cached memory. If this number drops to a low number, Windows is running out of Free RAM. While that number varies per application and use case, generally keep this number > 500 MB for server VM and >100 MB for VDI VM. The reason you should set a lower number for VDI because they add up quickly. If you have 10K users, that’s 1 TB of RAM.
It’s okay for this counter to be low, so long other memory metrics are fine. The following table shows VMs with near 0 free memory. Notice none of them are needing more memory. This is the perfect situation as there is no wastage.

[Image: ## Image Description

This table displays VM memory metrics for 11 virtual machines, showing **Free Memory** (all critically low, ranging from 0.0003 GB to 0.05 GB, highlighted in red), **Capacity** (8–24 GB), **Needed Memory** (3.4–13.01 GB), **Page In**, **Page Out**, and **Guest|Active** memory. Despite near-zero free memory across all VMs, **Page Out values are universally 0** and Page In values are mostly minimal (with one outlier "e..." at 23,790.2), demonstrating that low free memory alone is not indicative of a memory problem. This supports the surrounding text's assertion that near-zero free RAM is acceptable when other memory pressure indicators (particularly Page Out) remain at zero, indicating no actual memory contention or wastage.]


### Page File

Memory paging is an integral part of Guest OS Memory Management. OS begins using it even though it still has plenty of physical memory. It uses both physical memory and virtual memory at the same time. Microsoft recommends that you do not delete or disable the page file. See this for reference.

[Image: ## Image Description

The diagram illustrates the **Windows Guest OS memory architecture**, showing how multiple processes interact with memory through two layers: **Working Sets** (the portion of virtual memory actively used by each process) and the OS memory hierarchy.

The OS memory stack shows **Virtual Memory** backed by two components: **Page File** (disk-based) and **Physical Memory** (backed by **Memory DIMM**), demonstrating that processes only see virtual memory addresses, never physical memory directly.

This diagram contextualizes the surrounding text's explanation that paging operations occur **between the page file and physical memory** — not between physical disk and page file — and illustrates why Windows maintains both simultaneously even when physical memory is abundant.]

As shown on the diagram, processes see virtual memory, not physical memory. Guest OS presents this as system API to processes. The virtual memory is backed by the page file and physical memory. Guest OS shields the physical memory and hardware. Paging is an operation of reading/writing from the page file into the physical memory, not from physical disk into the page file.
Let Windows manages the pagefile size. This is the default setting, so you likely have it already. By default, windows sets the pagefile size to the same size with the physical memory. So if the VM has 8 GB of RAM, the pagefile is an 8 GB file. Anything above 8 GB indicates that Windows is under memory pressure.
The VM metric Guest \ Swap Space Remaining tracks the amount of swap space that's free.
The size of Page File is not a perfect indicator of the RAM usage, because they contain pages that are never demanded by the application. Windows does SuperFetch, where it predicts what pages will be used and prefetch them in advance. Some of these pages are never demanded by the application. Couple with the nature that Guest OS treats RAM as cache, including the page file will result in oversized recommendation. Paging rate is more realistic as it only considers the recent time period (300 seconds in VCF Operations case)
A page would be used as cache if it was paged out at some point due to memory pressure and it hasn’t been needed since. The OS will reuse that page as cache. That means that at some point the OS was constrained on memory enough to force the page out to happen.
A page that was paged out earlier, has to be brought back first before it can be used. This creates performance issue as the application is waiting longer, as disk is much slower than RAM.
There are 2 types of page operations:
- Page In. This is a potential indicator for performance.
- Page-out. This is a potential indicator for capacity.
While Paging impacts performance, the correlation between the paging metrics and performance varies per application. You can’t set a threshold and use it to monitor different applications or VM. The reason is paging is not always used when Guest OS runs out of memory. There are a few reasons why paging may not correlate to memory performance:
- Application binary. The initial loading causes a page-in. Nobody will feel the performance impact as it’s not even serving anyone.
- Memory mapped files. This is essentially a file that has a mapping to memory. Processes use this to exchange data. It also allows the process to access a very large file (think of database) without having to load the entire database into memory.
- Proactive pre-fetch. It predicts the usage of memory and pre-emptively reads the page and bring it in. This is no different to disk where the storage array will read subsequent blocks even though it’s not being asked. This especially happens when a large application starts. Page-in will go up even though there is no memory pressure (page out is low or 0).
- Windows performs memory capacity optimization in the background. It will move idle processes out into the page file.
If you see both Page-in and Page-out having high value, and the disk queue is also high, there is a good chance it’s memory performance issue.
The rate pages that are being brought in and out can reveal memory performance abnormalities. A sudden change, or one that has sustained over time, can indicate page faults. Page faults indicate pages aren’t readily available and must be brought in. If a page fault occurs too frequently it can impact application performance. While there is no concrete guidance, as it varies by application, you can judge by comparing to its past behaviour and its absolute amount.
Operating Systems typically use 4KB or 2MB page sizes. Larger page size will result in more cache, which translates into more memory required.
The counter %pagefile tracks how much of the pagefile is used, meaning the value 100% indicate the pagefile is fully utilized. While the lower the number the better, there is no universal guidance. If you know, let me know!
Reference: this is an old article as it covers 32 bit Windows. If you find a newer one, kindly let me know.

#### Guest OS Paging metrics

There are 2 metrics. Page-in and Page-out.
The unit is in number of pages, not MB. It's not possible to convert due to mix use of Large Page (2 MB) and Page (4 KB). A process can have concurrent mixed usage of large and non-large page in Windows. The page size isn’t a system-wide setting that all processes use. The same is likely true for Linux Huge Pages.
The page-in rate metric tracks the rate OS brings memory back from disk to DIMM per second. Another word, the rate of reads going through paging/cache system. It includes not just swap file I/O, but cacheable reads as well (so it’s double pages/s).
Page Out is the opposite of the above process. It is not as important as Page In. Just because a block of memory is moved to disk that does not mean the application experiences memory problem. In many cases, the page that was moved out is the idle page. Windows does not page out any Large Pages.
The following shows the page out value at 99th percentile in the last 4 months. What do you observe?

[Image: ## Image Description

This donut/pie chart displays the **distribution of VM page-out rates** (at the 99th percentile over 4 months) across 3,325 VMs, segmented into six ranges. The dominant segment shows **79.67% of VMs (2,649/3,325) have page-out rates of 0–2,000 pages/sec**, with progressively smaller segments for higher ranges: 3.49% (2K–4K), 6.71% (4K–8K), 4.06% (8K–16K), 3.13% (16K–32K), and 2.95% (32K–99,999,999). This demonstrates that the vast majority of VMs experience minimal paging activity, while approximately 3% exhibit extremely high page-out rates, illustrating a heavily skewed distribution consistent with the surrounding text's observation about excessive paging in a small subset of VMs.]

There are 3325 VM in the above chart. In the last 4 months, 97% of them have page-out rate of less than 32000 pages, on a 5-minute average basis.
How about the remaining 3%?
Surprisingly, a few of them can be well 500000, indicating there is a wide range. So majority of VMs do not page out, but those that do, they do it excessively.
The block size is likely 4 KB. Some applications like Java and databases use 2 MB pages. Using 8 KB as the average, 10000 pages per second sustained over 5 minutes means 80000 KB x 300 = 24 GB worth of data.
You can profile your environment to see which VMs are experiencing high paging. Create a view with the following 6 columns
- Highest Page-In. Color code it with 1000, 10000, and 100000 as the thresholds. That means red is 10x orange, which in turn is 10x yellow.
- Page-In value at 99th percentile. Same threshold as above.
- Highest Page-Out. Same threshold as above.
- Page-Out value at 99th percentile. Same threshold as above.
- Sum of Page-In
- Sum of Page-Out
Set the dates to the period you are interested, but make it at least 1 week, preferably 3 months. There 2016 data points in a week, so the 99th percentile ignores the highest 20 datapoints.
In the following example, I used 4 months. I listed the top VMs in terms, sorted by the highest page-in. What observation do you see?

[Image: ## Image Description

The table displays **memory paging metrics** for the top 9 VMs (sorted by highest Max Page-In), showing six columns: Max Page-In, Max Page-Out, 99th Percentile Page-In, 99th Percentile Page-Out, Total Page-In, and Total Page-Out. Values highlighted in **red** indicate high/critical thresholds, while **orange/yellow** values indicate moderate thresholds. The data demonstrates a clear pattern where **Page-In consistently dominates Page-Out** across all rows — for example, the top VM shows Max Page-In of **5,069,497** versus Max Page-Out of only **485,203.81**, and Total Page-In of **134,816,679.69** versus Total Page-Out of **16,388,061.44** — visually supporting the surrounding text's assertion that Page-In is approximately **4-9x higher** than Page-Out across the VM fleet.]

For a start, some of those numbers are really high!
They are above 1 millions. Assuming 8K block size, that’s 8 GB per second, sustained for 300 seconds.
What else do you notice?
Page-In is higher than Page-Out. I average all the 3K VMs and I got the following result:

[Image: The image displays **six numerical values** representing VMware vSphere memory paging metrics (likely Page-In and Page-Out statistics) across different percentile or aggregation levels: **102,768.57 | 24,285.03 | 36,470.28 | 4,063.16 | 48,519,306.68 | 24,862,411.77**.

The data supports the surrounding text's observation that **Page-In values significantly exceed Page-Out values**, with the larger numbers (48.5M and 24.8M) likely representing maximum or high-percentile Page-In counts, while the smaller values represent averages or lower percentiles across the ~3,000 VM dataset.

These figures contextualize the **4x higher Page-In max value** and **9x higher 99th percentile** disparity discussed in the surrounding text.]

Page-In is 4x higher in the max value. Page-In also sustains longer, while Page-Out drops significantly. At the 99th percentile mark, Page-In is 9x higher. I suspect it is the non-modifiable page, like binary. Since it cannot be modified, it does not need to be paged out. It can simply be discarded and retrieved again from disk if required.
The good news is both do not sustain, so the paging is momentary. The following shows that the value at 99th percentile can drop well below 5x.

[Image: The image displays a two-column table showing **Max Page Out** (sorted descending) and **99th Percentile Page Out** values for multiple VMs/samples. Max Page Out values range from ~99,579 to ~132,995, while the corresponding 99P values vary dramatically — some drop to as low as **435.82** and **1,010.02** (highlighted in yellow with green indicators), while others remain relatively high (e.g., **44,771.87**). This demonstrates the author's point that the 99th percentile Page Out value frequently drops well below the maximum — in several cases by **100x or more** — confirming that paging events are largely momentary rather than sustained.]


[Image: The image shows a two-column table displaying **Max Page In** and **99th Percentile (99P) Page In** values across 9 data points, with Max values ranging from ~1.69M to ~5.07M and corresponding 99P values that are significantly lower. Green indicator bars appear next to several 99P values where the drop is most dramatic (e.g., Max of 5,069,497 vs. 99P of 29,154.43, a ~174x reduction). This data demonstrates the author's point that the **ratio between max and 99th percentile can drop well below 5x** — and in several cases far more drastically — confirming that peak paging events are momentary rather than sustained.]

To confirm the above, I downloaded the data so I can determine if the paging is indeed momentarily. Using a spreadsheet, I build a ratio between the 99th percentile value and the maximum value, where 10% means there is a drop of 10x. I plotted around 1000 value and got the following.

[Image: ## Image Description

This bar chart displays a frequency distribution of approximately 1,000 ratio values between the 99th percentile and maximum paging values, binned into 10% intervals from [0%, 10%] to (90%, 100%]. The distribution is heavily right-skewed, with the **[0%, 10%] bucket containing ~635 occurrences** (the dominant bar), followed by (10%, 20%] at ~90, and all remaining buckets progressively decreasing to near zero. This demonstrates that in the vast majority of cases (~63%), the 99th percentile paging value drops to less than 10% of the maximum value, confirming that high paging events are momentary spikes rather than sustained conditions.]

As you can see, majority of the paging drops drastically at 99th percentile.
Let’s dive into a single VM, so we can see pattern over time. I pick a database, as it does heavy paging. The following is a large Oracle RAC VM. Notice this has a closer ratio between page in and page out, and there is correlation between the two.

[Image: ## Image Description

The image displays two time-series charts from VMware VCF Operations showing **Guest|Page In Rate per second** (High: 1,173,266.63, Low: 591.47) and **Guest|Page Out Rate per second** (High: 831,899.88, Low: 184.13) for a large Oracle RAC VM over approximately 24 hours (Oct 10 ~7PM to Oct 11 ~6PM). Both charts exhibit **correlated spike patterns** — particularly prominent peaks around 10-11 PM and 7-9 AM — demonstrating that this database VM experiences heavy, bursty memory paging activity with a relatively close ratio between page-in and page-out rates, contrasting with typical workloads where these values diverge significantly.]

Assuming the page size is 4 KB, that means 100,000 pages = 400 MB/sec. Since VCF Operations averages the value over 300 seconds, that means 400 MB x 300 = 120 GB worth of paging in 5 minutes!

### Active File Cache Memory

This is the actively in-use subset of the file cache. Unused file cache and non-file backed anonymous buffers (mallocs etc) are not included.
This is the size of the portion of the system file cache which is currently resident and active in physical memory. The System Cache Resident Bytes and Memory \ Cache Bytes metrics are equivalent. Note that this counter displays the last observed value only; it is not an average during the collection period.
For further reading, refer to Windows

### Committed

Commit sounds like a guaranteed reservation, which means it’s the minimum the process can get.
This tracks the currently committed virtual memory, although not all of them are written to the pagefile yet. It measures the demand, so commit can go up without In Use going up, as Brandon Paddock shares here. If Committed exceeds the available memory, paging activity will increase. This can impact performance.
Commit Limit: Commit Limit is physical RAM + size of the page file. Since the pagefile is normally configured to map the physical RAM, the Commit Limit tends to be 2x. Commit Limit is important as a growing value is an early warning sign. The reason is Windows proactively increases its pagefile.sys if it’s under memory pressure.
The pagefile is an integral part of Windows total memory, as explained by Mark Russinovich explains here. There is Reserved Memory, and then there is Committed Memory. Some applications like to have its committed memory in 1 long contiguous block, so it reserves a large chunk up front. Databases and JVM belong in this category. This reserved memory does not actually store meaningful application data or executable. Only when the application commits the page that it becomes used. Mark explains that “when a process commits a region of virtual memory, the OS guarantees that it can maintain all the data the process stores in the memory either in physical memory or on disk”.
Notice the word on disk. Yes, that’s where the pagefile.sys comes in. Windows will use either the physical memory or the pagefile.sys.
So how do we track this committed memory?
The metric you need to track is the Committed Byte. The % Committed metric should not hit 80%. Performance drops when it hits 90%, as if this is a hard threshold used by Windows. We disabled the pagefile to verify the impact on Windows. We noticed a visibly slower performance even though Windows 7 showing >1 GB of Free memory. In fact, Windows gave error message, and some applications crashed. If you use a pagefile, you will not hit this limit.
We have covered Free Memory and Committed Memory. Do they always move in tandem? If a memory is committed by Windows, does it mean it’s no longer free and available?
The answer is no. Brandon Paddock demonstrated here that you can increase the committed page without increasing the memory usage. He wrote a small program and explained how it’s done. The result is Windows committed page is double that of memory usage. The Free Memory & Cached Memory did not change.

### Needed Memory

This is not a raw counter from Windows or Linux. This is a derived counter provided by VMware Tools to estimate the memory needed to run with minimum swapping. It’s a more conservative estimate as it includes some of the cache. It has 5% buffer for spike, based on the general guidance from Microsoft. Below this amount, the Guest OS may swap.
= physical memory - Maximum of (0, ( Unneeded  - 5 % of physical ))
where Unneeded = Free + Reserve Cache + Normal Priority Cache
Example: the VM has 10 GB of RAM. So the Physical RAM = 10 GB
So 5% of physical = 0.5 GB
Situation 1: max memory utilization.
Memory Available = 0 GB. 
Tools will calculate Needed memory as
= 10 GB - Maximum (0, 0 – 0.5)
= 10 - Maximum (0, -0.5)
= 10 - 0 GB
= 10 GB
Needed memory is the same as it’s already maxed.
Situation 2: high memory utilization.
Memory Available = 2 GB. 
Tools will calculate Needed memory as
= 10 GB - Maximum (0, 2 – 0.5)
= 10 - Maximum (0, 1.5 GB)
= 10 - 1.5 GB
= 8.5 GB
You actually still have 2 GB here. But Tools adds around 5%
Situation 3: low memory utilization.
Memory Available = 8 GB. 
Tools will calculate Needed memory as
= 10 GB - Maximum (0, 8 – 0.5)
= 10 - Maximum (0, 7.5 GB)
= 10 - 7.5 GB
= 2.5 GB
Again, Tools adds around 5%.
We’ve covered that you need to look at more than 1 metric before you decide to add more memory. I’m afraid it is case by case, as shown in the following table. All these VMs are low on free memory, but other than VM on row no 3, the rest has sufficient memory.

[Image: ## Image Description

This table displays VM memory metrics across 13 virtual machines, showing **Free memory, Capacity, Needed Memory, Page In, Page Out, and Guest|Active** values. All VMs show critically low free memory (0.1–0.13 GB, highlighted in red), but the third VM (**ap...**) is flagged as the most critical — its Needed Memory equals its full 12 GB capacity (indicated by a red dot), and it has an extremely high Page In rate of **306,841.47**, indicating severe memory pressure and active swapping. The table demonstrates that while all VMs appear memory-constrained based on free memory alone, only the third VM shows definitive signs of memory insufficiency through the combination of maxed-out Needed Memory and extreme paging activity.]


## Storage

This is the layer that application team care as it is what is presented to them.

| Questions | Description |
| --- | --- |
| Configuration | For each partition, need to know name, filesystem type (e.g. NTFS, ext4), network or local, block size.  Ideally, we get the mapping between partition and virtual disk. |
| Capacity | For each partition, need to know the configured space and used space. For free space, we need to know both in absolute (GB) and relative (%).  Need to alert before running out of disk space, else the OS crashes. We should not include the networked drive in Guest OS capacity, because the networked drive is typically shared by many. An exception is in VDI use case, where the user personal files is stored on the network. |
| Reclamation | This can be determined from the free space. Reclamation is tricky as it needs to shrink partition. |
| Performance | Queue, Latency (read and write), IOPS, Throughput |


### Disk Queue

With VMware Tools, you get Guest OS visibility into the partitions and disk queue. The first one is critical for capacity, while the second is critical for performance.
This counter tracks the queue inside Linux or Windows storage subsystem. It’s not the queue at SCSI driver level, such as LSI Logic or PVSCSI. If this is high then the IO from applications did not reach the underlying OS SCSI driver, let alone the VM. If you are running VMware storage driver, such as PVSCSI, then discuss with VMware Support.

[Image: This Windows Performance Monitor screenshot displays **Avg. Disk Queue Length** (red line, scale 1.0) for a PhysicalDisk on \\DELL-5560, showing values that are generally near zero (Average: 0.161, Minimum: 0.002, Maximum: 1.582) with one dramatic spike reaching **10.0** at approximately 1:17:05 PM. The chart also includes Avg. Disk Read Queue Length (green, scale 100.0) and Avg. Disk Write Queue Length (blue, scale 1000.0), though neither is currently enabled for display. In context, this demonstrates the Guest OS-level disk queue metric being monitored via VMware Tools, where the isolated spike illustrates the type of transient queue buildup that can indicate storage performance pressure within the Windows storage subsystem before requests reach the SCSI driver layer.]

There are actually 2 metrics: One is a point in time and the other is average across the entire collection cycle. Point in time means the snapshot at the collection period. For example, if the collection is every 5 minute, then it’s number on the 300th second, not the average of 300 numbers.
Windows documentation said that “Multi-spindle disk devices can have multiple requests active at one time, but other concurrent requests await service. Requests experience delays proportional to the length of the queue minus the number of spindles on the disks. This difference should average < 2 for good performance.”

| guest.disk.queue | Win32_PerfFormattedData_PerfDisk_PhysicalDisk.Name = \"_Total\"#CurrentDiskQueueLength" from WMI |
| --- | --- |
| guest.disk.queueAvg | Win32_PerfFormattedData_PerfDisk_PhysicalDisk.Name = \"_Total\"#AvgDiskQueueLength" from WMI |

High disk queue in the guest OS, accompanied by low IOPS at the VM, can indicate that the IO commands are stuck waiting on processing by the OS. There is no concrete guidance regarding these IO commands threshold as it varies for different applications. You should view this in relation to the Outstanding Disk IO at the VM layer.
Based on 3000 production VMs in the last 3 months, the value turn out to be sizeable. Almost 70% of the value is below 10. Around 10% is more than 100 though, which I thought it’s rather high.

[Image: This pie chart displays the distribution of **Outstanding Disk IO commands** across 3,000 production VMs, segmented into 7 ranges. The dominant segment is **0–2.5 at 42.19%**, with cumulative values below 10 (covering ranges 0–2.5, 2.5–5, and 5–10) totaling approximately **68.78%**, confirming the author's ~70% claim. Notably, the **100–9,999,999 range accounts for 9.15%**, supporting the author's observation that ~10% of VMs show unusually high outstanding IO values that may indicate either a counter bug or severe performance issues.]

Strangely, there are values that seem to off the chart. I notice this in a few metrics already, including this. Look at the values below. Do they look like a bug in the counter, or severe performance problem?

[Image: The image shows a table displaying **Guest|Disk Queue** metric values for several VMs, sorted in ascending order. The values range from approximately **214,653 to 214,750**, which are extraordinarily high disk queue depths. In context, these values appear to represent anomalous outliers that the author is questioning as potential **counter bugs** rather than genuine severe performance problems, given that disk queue values in the hundreds of thousands would be implausibly extreme in a real-world scenario.]

Unfortunately, we can’t confirm as we do not have latency counter at Guest OS level, or even better, as application level. I am unsure if the queue is above the latency, meaning the latency counter does not start counting until the IO command is executed.
I plot the values at VM level, which unsurprisingly does not correlate. The VM is tracking IO that has been sent, while Guest OS Disk Queue tracks the one that has not been sent.

[Image: The image displays three time-series line charts spanning **Sep 23–29**, showing: **Guest|Disk Queue** (peak H: 42,949.94, with a dramatic spike near Sep 23 noon), **Virtual Disk: Outstanding IO Requests/OIOs** (H: 2.64), and **Virtual Disk: Peak Read Latency in ms** (H: 4.11). The charts demonstrate that the Guest OS Disk Queue spike (~43K) does **not correlate** with VM-level IO metrics (OIOs max 2.64, latency max 4.11ms), which remain relatively flat and low throughout the period. This supports the author's argument that Guest OS Disk Queue tracks unsubmitted IOs while VM-level counters track executed IOs, making direct correlation between the two metrics unreliable for diagnosing performance issues.]

The preceding line chart also reveals an interesting pattern, which is disk queue only happens rarely. It’s far less frequent than latency.
Let’s find out more. From the following heat map, you can see there are occurrences where the value is >100.

[Image: ## Image Description

This is a **vSphere heat map** displaying **Guest|Disk Queue** metrics across virtual machines in a vSphere World, with the tooltip highlighting VM **ora-dev12-ebs-r1** showing a value of **63.7**. The color scale ranges from green (0) through yellow/orange to red (>100), with the vast majority of VMs showing green (near-zero queue depth), while a small cluster of VMs along the left edge display yellow, orange, and red colors indicating elevated disk queue values. This heat map demonstrates that while most VMs have negligible disk queue lengths, a few VMs exhibit significantly high Guest OS disk queue values (some exceeding 100), confirming the text's assertion that disk queue occurrences are rare but can reach extreme values when they do occur.]

However, when we compare between current value and maximum value, the value can be drastically different.

[Image: ## Image Description

This table displays VM-level disk performance metrics including **Current Queue**, **Current Outstanding IO**, **Max Disk Queue**, **Max Outstanding IO**, and **vDisk count** for 9 VMs, sorted by Max Disk Queue in descending order. The data illustrates a stark contrast between current and maximum values — for example, "AT..." shows a current queue of only **196.82** but a Max Disk Queue of **5,036.62**, while its Current Outstanding IO is just **0.8 OIOs** versus a Max of **4.24 OIOs**. This comparison directly supports the surrounding text's point that current and maximum values can be **drastically different**, indicating disk queue spikes are intermittent rather than sustained.]

Let’s take one of the VMs and drill down. This VM has regular spikes, with the last one exceeding 1000.

[Image: ## Guest|Disk Queue Chart Analysis

The chart displays the **Guest OS Disk Queue metric** for a single VM over approximately 24 hours (May 27–28), with a recorded **high of 1,089.02** and a **low of 0**. The data shows mostly near-zero baseline activity punctuated by **irregular sharp spikes**, with a notable spike of ~600 around 11:00 AM and the peak spike exceeding **1,000 at approximately 8:00–8:30 PM**.

In context, this chart illustrates the drill-down referenced in the surrounding text — demonstrating that disk queue pressure is occurring **inside the Guest OS** rather than at the VM/hypervisor layer, as the spikes represent IO requests queuing within the guest before being sent down to the underlying storage stack.]

Their values should correlate with disk outstanding IO. However, the values are all low. That means the queue happens inside the Guest OS. The IO is not sent down to the VM.

[Image: ## Image Description

The chart displays **Virtual Disk: Aggregate of all Instances | Outstanding IO requests (OIOs)** over a ~24-hour period (May 26 ~9PM to May 28). Values remain consistently near **0** throughout most of the timeframe, with minor periodic spikes reaching approximately **0.1–0.2**, and a single prominent spike near **8:00 PM** reaching the high value of **H: 0.8**.

In the context of the surrounding text, this chart demonstrates that **VM-level disk outstanding IOs are essentially negligible** (low: 0, high: 0.8), confirming that the IO queue is **not** accumulating at the hypervisor/VM layer — the bottleneck exists **inside the Guest OS** and the IO is never being passed down to the virtual disk layer.]

Which in turn should have some correlation with IOPS, especially if the underlying storage in the Guest OS (not VM) is unable to cope. The queue is caused by high IOPS which cannot be processed.

[Image: ## Image Description

The chart displays **Virtual Disk | Peak Virtual Disk IOPS** over approximately 24 hours (May 27–28), with a high value of **554.8** and a low of **0**. The metric shows mostly near-zero baseline activity with **sporadic sharp spikes**, the most notable occurring around **8:00–8:30 PM on May 28**, reaching approximately **500 IOPS**.

In context, this chart correlates with the disk queue discussion — the relatively low and intermittent IOPS values help explain why latency metrics appear deceptively normal, as the IO bottleneck is occurring **within the Guest OS** before reaching the hypervisor layer, meaning only a fraction of actual IO demand is reflected in these VM-level metrics.]

Finally, it would manifest in latency. Can you explain why the latency is actually still good?

[Image: ## Image Description

The chart displays **Virtual Disk | Peak Virtual Disk Write Latency (ms)** over approximately 24 hours (May 27–28), with a **high of 3.8 ms** and a **low of 0 ms**. The metric remains consistently low (near 0–1 ms) throughout most of the period, with occasional spikes reaching ~2.5 ms, and one notable peak highlighted in orange around 3:00–4:00 PM. This demonstrates the surrounding text's explanation that **write latency at the hypervisor level appears deceptively low/acceptable** because IO queued inside the Guest OS (Windows) never reaches the hypervisor, so the VM-level latency metric does not capture the true latency experienced by the application.]

It’s because that’s from the IO that reaches the hypervisor. The IO that was stuck inside Windows is not included here.
The application feels latency is high, but the VM does not show it as the IO is stuck in between.
Can the disk queue be constantly above 100?
The following VM shows 2 counters. The 20-second Peak metric is showing ~200 – 250 queue, while the 5-minute average shows above 125 constantly. The first counter is much more volatile, indicating the queue did not sustain.

[Image: ## Image Description

The chart displays two disk queue metrics for **vrops-saas-06-ysot** over approximately 24 hours (Sunday 6PM to Monday ~9PM): the **Guest|Peak Disk Queue within collection cycle** (pink, ~200–250 range with spikes up to ~325) and **Guest|Disk Queue** (purple, consistently above 125 with a tooltip showing **152.38** and **128.42** respectively at Monday 07:37:13 AM). The Peak metric is significantly more volatile with sharp spikes, while the 5-minute average (purple) remains persistently elevated above 125–150 throughout the entire period. This demonstrates the concept described in the text — that disk queue can be **constantly above 100**, with the peak counter revealing momentary bursts that the averaged counter smooths out, both indicating sustained storage contention within the Windows guest.]