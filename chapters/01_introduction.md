# Introduction


## The World of Metrics


[Image: ## Image Description

This image presents a **side-by-side parallel text comparison** using the *Star Trek* opening monologue as a creative framing device. The left panel ("Our Inspiration") shows the original Star Trek quote, while the right panel ("Our Endeavour") maps each line to IT/VMware concepts: "Space" → "Metrics," "Starship Enterprise" → "The Book," "five-year mission" → "10-year mission," "new worlds" → "new systems," "new life" → "new observability," and "new civilizations" → "proactive operations."

In the context of Chapter 1's introduction, this serves as a **thematic mission statement**, positioning the book's goal of deep VMware vSphere metrics understanding as an ambitious, exploratory endeavour — emphasizing that the work goes beyond surface-level product documentation to boldly explore territory "no IT Architect has gone before."]

Metric is essentially an accounting of system in operations. To understand the counter properly hence requires a knowledge of how the entire system works. Without internalizing the mechanics, you will have to rely on memorizing. In my case, memorizing is only good for getting a certificate.
Take time to truly understand the reasons behind the metrics. You will appreciate the threshold better when you know how it is calculated.

### Nuances in Metrics

It is useful to know the subtle differences in the behaviour of metrics. By knowing their differences, we can pick the correct metrics for the tasks at hand.

#### Naming Complexity


| Same name, same object, different formula | The metrics have the same name, belong to the same object, yet they have a different formula depending on where in the object you measure it.  Example: VM CPU Used in vCPU level does not include System time but at the VM level it does. The reason is that System time does not exist at vCPU level since the accounting is charged at the VM level. |
| --- | --- |
| Same name, same purpose, different formula | Metrics with the same name do not always have the same formula in different vSphere objects. |
| Same name, same purpose, different formula | Memory Usage: in VM this is mapped to Active, while in ESXi Host this is mapped to Consumed. In Cluster, this is Consumed + Overhead.  Technically speaking, mapping usage to active for VM and consumed for ESXi makes sense, due to the 2-level memory hierarchy in virtualization. At the VM level, we use active as it shows what the VM is physically consuming (related to performance). At the host and cluster levels, we use consumed because it is related to what the VM claimed (related to capacity management). This confusion has resulted in customers buying more RAM than what they need. VCF Operations uses Guest OS data for Usage, and falls back to Active if it’s not available. |
| Same name, same purpose, different formula | Memory Consumed: in ESXi this includes memory consumed by ESXi, while in Cluster it only includes memory consumed by VM. In VM this does not include overhead, while in Cluster it does. |
| Same name, same purpose, different formula | VM Used includes Hyper Threading but penalty is 37.5%. ESXi Used is also aware of HT but the penalty is 50%. |
| Same name, same purpose, different formula | Virtual Disk: in VM includes RDM, but in Datastore it does not. Technically, this makes sense as they have different vantage points. |
| Same name, same purpose, different formula | Steal Time in Linux only includes CPU Ready, while stolen time in VM (CPU Latency) include many other factors including CPU frequency. |
| Same name, different meaning | Metrics with identical name, yet different meaning. Be careful of misinterpretation. |
| Same name, different meaning | VM CPU Usage (%) shows 62.5% when ESXi CPU Usage (%) shows 100%. This happens due to different perspectives. When both threads are running, ESXi CPU Usage does not. |
| Same name, different meaning | Disk Latency and Memory Latency indicate a performance problem. They are in fact the primary counter for how well the VM is being served by the underlying IaaS. But CPU Latency does not always indicate a performance problem. Its value is affected by CPU Frequency, which can go up or down. Sure, the VM is running at a higher or lower CPU speed, but it is not waiting to be served. It’s the equivalent on running on older CPU. |
| Same name, different behaviour | VM CPU Usage (MHz) is not capped at 100%, while ESXi CPU Usage (MHz) is. The later won’t exceed the total capacity. |
| Same name, different behaviour | Memory Reservation and CPU Reservation have different behaviors from monitoring viewpoint. |
| Same name, different behaviour | In Microsoft Windows, the CPU queue includes only counts the queue size, while the disk queue excludes the IO commands being processed. |
| Same purpose, different name | You would expect if the purposes are identical then the labels or names will be identical.  Swapped Memory in VM is called Swapped, while in ESXi is called Swap Used. Static frequency CPU utilization in VM is called Run, while ESXi calls it Utilization. Different names make sense as they reflect different vantage points. |
| Same purpose, different name | What vCenter calls Logical Processor (in the client UI) is what ESXi calls Physical CPU (in esxtop panel). I think the word logical is confusing. Easier to use virtual vs physical. |
| Same purpose, different name | vCenter uses Consumed (%) and Usage (%) for the same ESXi CPU utilization. |
| Confusing name | The name of the counter may not be clear. |
| Confusing name | VM CPU Wait counter includes idle time. Since many VMs do not run at 100%, you will see CPU Wait counter to be high. You may think it’s waiting for something (e.g. Disk or Memory) but it’s just idle. If we see from the viewpoint of kernel schedule, that vCPU is waiting to be used. So the name is technically correct |
| Confusing name | The term virtual disk includes RDM. It’s not just VMDK. The reason is RDM appears as virtual disk when you browse the directory in the datastore, even though the RDM file is just a pointer to an external LUN. |
| Incorrect name | Task Manager in Windows is not correct as the kernel does not have such concept. The terminology that Windows has is called Job. A job is a group of processes that can be managed as one. Do you want it to be called Job Manager? 😊  I think Process Manager is better as that’s what running on top of the kernel. |
| Mixing terminology | Allocation and reservation are 2 different concepts. When you allocate something to someone, it does not mean it’s guaranteed. If you want a guarantee, then do reservation. Allocation is a maximum (you can’t go beyond it), while Reservation is a minimum. The actual utilization can be below reservation but can’t exceed allocation. You cannot overcommit reservation as it’s a guarantee. You can overcommit allocation as it is not a guarantee. Avoid using metric names like these: Allocation Reservation. This makes no sense. Maximum Reservation. Simply use Allocation instead. Minimum Allocation. Simply use Reservation instead. |
| Mixing terminology | The word device, disk and LUN are used interchangebly. They are actually not identical.  Device is actually generic. It does not have to be storage device. It can be network device or security device.  Disk tends to be phsyical, something you can hold in your hands. It is typically part of a disk group called RAID. Advanced storage array takes the concept further. It can create a logical volume spanning multiple RAID groups. The lazy name LUN was chosen. I prefer to call it Logical Volume, but will stick to LUN in this book. LUN is what ESXi host mounts and then format it with VMFS filesystem. |


#### Architecture Complexity

The 4 basic elements of infrastructure have been around since Adam built the first data center for Eve. Humankind has not invented the 5th Element yet. However, each of these 4 has their own unique nature. They have “speed vs space” dimensions. This in turn creates complexity in observability.
The following table shows how the 4 elements of infrastructure relate to these 2 dimensions.

|  | Speed | Space | Analysis |
| --- | --- | --- | --- |
| CPU | Yes | N/A | Space is not applicable as CPU is a form of instruction. |
| Memory | Limited | Yes | Speed is practically not applicable as the latency is in nanoseconds. Memory read/write is speed, but since the latency negligible, it is generally not used in performance management. |
| Storage | Yes | Yes | The speed and space have different consumption metrics. |
| Network | Depends on the nature | Depends on the nature | Unlike server and storage, network takes >1 shape. It’s both a line and a dot. The cables are the lines, the switch is the dot. |

Let’s elaborate.

| CPU | The primary speed metric (GHz) is not comparable across different hardware generation or architecture. 1 GHz in today’s CPU is more efficient than 1 GHz in older CPU. |
| --- | --- |
| CPU | Different variants of CPU models in the same generation from the same vendor. |
| Memory | Its function is caching, so its counters tend to be near 100%, and that is what you expect as cache is typically much smaller than the actual source. Anything less than 100% is not maximizing your money. CPU and memory metrics have different nature. 95% utilization for memory could be low, while 85% for CPU could be high already. |
| Memory | It’s a form storage, so its metrics are mostly about space and not speed. There is VM CPU Demand, but not VM Memory Demand. Demand does not apply to memory as it’s a form of storage, just as there is no such thing as a Demand metric for your laptop disk space. |
| Storage | It has 2 sides (speed and space), but both have consumption metrics. The speed has 2 components for consumption: IOPS and Throughput. The throughput depends on the block size. It is also measured in bytes/second, not bit/second. The reason is you’re measurign the amount of disk space being read or written from the storage. Unlike network throughput, which focuses on the cable or wire, the disk throughput focuses on the node. |
| Storage | There is limit for disk IOPS, but not for disk throughput. The latter is not practical to implement due to varying block size. |
| Network | While server and storage are nodes, network is interconnect. This makes it more challenging. We will cover this in-depth in the System Architecture section |

Their complexity results in difference in type of metrics applicable:

|  | Utilization | Reservation | Allocation |
| --- | --- | --- | --- |
| CPU | Yes | Yes | Yes |
| Memory | Yes | Yes | Yes |
| Disk | Yes | Not Applicable | Yes |
| Network | Yes | Yes | Yes |

And lastly, beyond metrics there are also further complications such as:

| VM vs ESXi | The CPU metrics from a VM viewpoint differs to the CPU metrics from ESXi viewpoint. A VM is a consumer. Multiple VMs can share the same physical core, albeit at the price of performance. So metrics such as Ready does not apply to ESXi. The core and the thread are always ready. |
| --- | --- |
| ESXi vs vCenter | While ESXi is the source of metrics, vCenter may add its own metrics and the formula don’t always match 100% in all scenarios, such as Used vs Usage. |
| ESXi vs vCenter | ESXi provides Run (ms), Used (ms), Demand (MHz) for VM CPU. vCenter adds Usage (MHz) and Usage (%). |
| ESXi vs vCenter | ESXi shows Used (%), while vCenter shows Used (ms). The first one affected by CPU frequency and can go beyond 100%. |
| ESXi ≠ VMs + Kernel | The metrics at ESXi is more complex than the sum of its VM + the kernel. |
| M:N relationship | A VM with multiple virtual disks can span across multiple datastores, and even RDMs. On the other hand, a datastore typically hosts many VMs. An ESXi may mount multiple LUNs and a LUN is typically presented into multiple ESXi or even multiple clusters. These many to many relationships make the metrics across VM, datastore, ESXi, Cluster, Data Center inconsistent when viewed overall. Each of them is correct as each has to look from their own vantage point. |


#### Other Nuances


| Time | Some metrics reflect what happened in the past. That’s why the name is in past tense. |
| --- | --- |
| Time | Memory ballooned does not mean there is an active ballooning happening. The process could have happened days ago, and the page was simply idling, never been asked by Guest OS. |
| Roll up | vCenter measures every 20000 ms, but the maximum value for a completely idle thread is 10000. The reason is 20000 is the value set at the core level. Since a core has 2 threads when HT enabled, each was allocated 10000. |
| Unit | VM CPU Ready can be above 100%. If you look at esxtop, many VM level metrics are >100%. |
| Unit | Why are CPU metrics expressed in milliseconds instead of percentage or GHz? How can a time counter (milliseconds in this case) account for CPU Frequency? |
| Unit | For CPU, 1 GHz = 1000 MHz. For memory and disk space, 1 GiB = 1024 KiB and 1 GB = 1000 KB. |
| Unit | Esxtop and vSphere Client use different units for the same metric. For example, esxtop use megabit while vCenter UI use kilobyte for networking counter. |
| Formula | ESXi CPU Core Utilization reports 100% when 1 thread is running. But it also reports 100% when both threads are running, making it impossible to guess which scenarios. |
| Formula | ESXi CPU Idle (ms) includes low activities. It also considers CPU frequency, and not simply whether CPU is running or now. |

In addition to all the above nuances, there are complexity created by choices and scale.

| Choices | When you have 2 watches showing different times, you become unsure which watch is the correct one. |
| --- | --- |
| Choices | There are 5 metrics for VM CPU “consumption”: Run, Used, Usage, Usage in MHz, and Demand. |
| Choices | There are 7 metrics for ESXi CPU “consumption”: Core Utilization, Utilization, Used, Usage, Usage in MHz, Consumed, and Demand. |
| Volumes of Metric | The sheer number of metrics make analysis difficult. |
| Volumes of Metric | Take for example, vCenter has 17 CPU metrics available at the VM level, and 12 of them are available at a vCPU level too. In addition, each VM comes with 28 memory metrics. That means a VM with 4 vCPUs will have 93 metrics (17 + 4 x 12 + 28). A vSphere environment with 1,000 VMs with 4 vCPUs as the average VM size will have process 93K metrics each time it collects. If you do that every minute, you will collect almost 134 million metrics per day. Since many customers like to keep for at least 6 months, that’s 24+ billion metrics. |
| Volumes of Metric | With so many metrics, the amount of business value received becomes a valid concern. At the end of the day, you are not in the business of collecting metrics. |


#### Interpretation Challenge

At the end of the day, you care about the interpretation of the value. What is considered good? As you can guess, the answer is “it depends”. Different applications have different tolerances. Even the same software has variable tolerance, depending on the use case. Even on identical user case, the end users have different tolerances.
The above makes it challenging to set up out of the box thresholds, which are universal for all cases. Set too low, and you see red too often when there is no actual complaint, and set too high, and you miss the actual problem.
As an example, let’s take disk latency. I take Microsoft SQL Server as that’s a popular application and it’s used in many production environments. The following is a guidance from Microsoft:

[Image: This image shows a **Microsoft documentation note** explaining the 10-15 milliseconds I/O latency threshold used as a bottleneck indicator for SQL Server. It provides context that Microsoft CSS has observed I/O request times ranging from sub-millisecond (modern SSD/NVMe) up to 15 seconds per transfer in extreme cases. In the context of the surrounding text, it supports the author's argument that threshold-setting is complex — the 10-15ms figure applies at the **SQL Server/Windows layer**, meaning thresholds at the **vSphere VM layer** must be set even lower to account for additional stack latency.]

It says 10 – 15 milliseconds. But that’s at MS SQL layer. That means at MS Windows layer it needs to be lower, to account for processing latency and queue in the stack. This also means at vSphere VM layer, it needs to be even lower. So what should we set the value at VM level? How about read versus write? It is indeed a challenge to set.
It says “consistently”. Since IO measure per second, does it mean 300 seconds is far too long? That means 300x, which is definitely consistent. From what I’ve seen, if you set at 5 minutes, you are likely to get a lot of alerts but little complaint.
You can read more at Troubleshoot slow SQL Server performance caused by I/O issues.

#### Documentation Challenge

To master metrics, you need to be able to see them from 3 different perspectives:

| Technology | Computer architecture has not fundamentally changed since the first day of the mainframe. You have CPU, memory, disk and network. Documenting via this route is useful for infrastructure. |
| --- | --- |
| Technology | There are variants such as GPU and APU, and components become distributed and virtual. You need to be able to see how the metrics behaviour change. |
| Pillars of Operations | Each pillar brings their own set of metrics.  For examples:  Capacity creates new metrics such as Time Remaining and Recommended Size Cost creates new metrics such as Month-to-Date Cost Performance creates new metric such as KPI (%) Compliance creates new metric such as PCI-DSS Compliance Score (%) |
| Product | Product such as vSphere, NSX, and Kubernetes bring their own set of objects.  Each type of object (e.g. VM, K8 Pod, AWS S3, Oracle DB) has their own set of metrics. Since objects typically have relationship with other objects and are grouped under a parent (e.g. a K8 Cluster has multiple nodes, which in turn can have multiple pods), you end up with multiple parallel hierarchies or overlapping hierarchies. |

As a book has a simple and fixed structure, it’s impossible to document in 3 different ways. That’s why this book blends the approach.
- It starts with the raw metrics, followed by derived metrics. Raw metrics tend to be simple and narrow in scope. Derived metrics combine multiple raw metrics. It tends to cover multiple areas.
- For raw metrics, it follows the technology route. For each of the 4 infrastructure elements, it covers contention first, then consumption.
- For derived metrics, it follows the product or object approach. Within each object, it follows the pillar of operations.
Ideally, we use an interactive website where you can browse from different perspectives. Or maybe we simply use Generative AI, assuming we can augment it with logic instead of 100% relying on English and Maths.

### Virtualization Impact

vSphere counters are more complex than physical machine counters because there are many components as well as inconsistencies that are caused by virtualization. When virtualized, the 4 elements of infrastructure (CPU, RAM, Disk, Network) behave differently.
Virtualization splits the IT stack into Provider and Consumer. The providers have 2 types of counters:
- Provider metric. This metric does not exist at consumer. For example, the physical network in ESXi.
- Sum of Consumer metric. This metric aggregates the metric of consumers. For example, the sum of VM network in the ESXi.
The confusion comes because the metric name does not tell what type of metric it is. For example, is ESXi CPU Demand a consumer or provider metric?
Not all VMware-specific characteristics are well understood by management tools that are not purpose-built for it. Partial understanding can lead to misunderstanding as wrong interpretation of metrics can result in wrong action taken.
The complexity is created by a new layer because it impacts the adjacent layers below and above it. So the net effect is you need to learn all 3 layers (Guest OS layer, virtualization layer and physical layer). That’s why from a monitoring and troubleshooting viewpoint, Kubernetes and container technology require an even deeper knowledge as the boundary is even less strict. Think of all the problems you have with vSphere Resource Pool performance troubleshooting, and now make it granular at process level. You’re having a good time mastering K8 right? 😉
Since VMkernel is technically an operating system, it has kernel space and user space. Some counters include both, while others don’t.

#### What, exactly, is a VM?

From observability viewpoint, a VM is not what most of us think it is. It changes the fundamental of operations management. It introduces a whole set of metrics and properties, and relegates many known concepts as irrelevant.
For example, you generally talk about these types of system-level metrics in Windows or Linux
- Processes
- Threads
- System Calls/sec
But when it comes to VM, you don’t. The reason these OS-level metrics are not relevant is because a VM is not an OS.
To master vSphere metrics, you need to know ESXi kernel. The kernel is a different type of OS as its purpose is to run multiple virtualized motherboard (I personally prefer to call VM as virtual motherboard). As a result, its metrics are different to typical OS such as Windows and Linux.
From the kernel’s vantage point, a VM is just a collection of process that needs to be run together. Each process is called World. So there is a world for each vCPU of a VM, as each can be scheduled independently. The following screenshot shows both VM and non VM worlds running side by side. I’ve marked the kernel modules with red dot. You can spot familiar process like vpxa and hostd running alongside VM (marked with the yellow line).

[Image: This is an **esxtop screenshot** showing ESXi kernel worlds (processes) with CPU scheduling metrics including %USED, %RUN, %SYS, %WAIT, %VMWAIT, and %RDY columns. The data shows both VM worlds (e.g., VMware vCenter at 12.46% used, blr01m01win01 at 0.48%) and kernel module worlds marked with red dots (vpxa, hostd, vsanmgmtd), alongside the **system world (ID=1) showing an extreme %WAIT of 54,256.64** and %RDY of 109.13. This illustrates the surrounding text's point that ESXi treats VMs as collections of schedulable "World" processes — with each vCPU as an independent world — visible at the hypervisor layer in ways the Guest OS metrics cannot expose.]


#### Visibility

Guest OS and VM are 2 closely related due to their 1:1 relationship. They are adjacent layers in SDDC stacks. However, the two layers are distinct, each provide unique visibility that the other layer may not be able to give. Resource consumed by Guest OS is not the same as resource consumed by the underlying VM. Other factors such as power management and CPU SMT also contribute to the differences.
The different vantage points result in different metrics. This creates complexity as you size based on what happens inside the VM, but reclaim based on what happens outside the VM (specifically, the footprint on the ESXi). In other words, you size the Guest OS and you reclaim the VM.
The following diagram uses the English words demand and usage to explain the concept, where demand consists of usage and unmet demand. It does not mean the demand and usage metrics in vSphere and VCF Operations, meaning don’t assume these metrics actually mean this. They were created for a different purpose.

[Image: ## Image Description

The diagram illustrates the **memory/CPU resource visibility gap** between the Guest OS view and the VM/Hypervisor (ESXi) view, showing four labeled regions: **A** (demand visible only to Guest OS, not to the hypervisor — e.g., CPU run queue, page file), **B** (usage visible to both Guest OS and VM/hypervisor), **C** (ESXi overhead not visible to Guest OS, such as virtualization tax), and **D** (additional ESXi-layer consumption not visible to Guest OS). The diagram demonstrates that **Guest OS "Usage" ≠ VM "Usage"** and **Guest OS "Demand" ≠ VM "Demand"** — the VM view's demand and usage spans B+C+D, while the Guest OS view only sees A+B. This directly supports the surrounding text's point that **sizing decisions should be based on Guest OS internals (A+B), while reclamation decisions must be based on the VM's actual ESXi footprint (B+C+D)**.]

I tried adding application into the above diagram, but that complicated the whole picture that I removed it. So just take note that some applications such as Java VM and database manage their own resources. Another virtualization layer such as Container certainly takes the complexity to another level.
We can see from the above that area A is not visible to the hypervisor.

| Layer A | Queue inside the Guest OS (CPU Run Queue, RAM Page File, Disk Queue Length, Driver Queue, network card ring buffer). These queues are not visible to the underlying hypervisor as they have not been sent down to the kernel. For example, if Oracle sends IO requests to Windows, and Windows storage subsystem is full, it won’t send this IO to the hypervisor. As a result, the disk IOPS counter at VM level will under report as it has not received this IO request yet. |
| --- | --- |
| Layer B | What the Guest uses. This is visible to the hypervisor as a VM is basically a multi-process application. The Guest OS CPU utilization somehow translates into VM CPU Run. I added the word “somehow” as the two metrics are calculated independently of each other, and likely taken at different sampling time and use different roll up technique. |
| Layer C | Hypervisor overhead (CPU System, CPU MKS, CPU VMX, RAM Overhead, Disk Snapshot). This overhead is obviously not visible to the Guest OS. You can get some visibility by installing Tools, as it will add new metrics into Windows/Linux. Tools do not modify existing Windows/Linux metrics, meaning they are still unaware of virtualization. From the kernel viewpoint, a VM is group of processes or user worlds that run in the kernel. There are 3 main types of groups: VM Executable (VMX) process is responsible for handling I/O to devices that are not critical to performance. The VMX is also responsible for communicating with user interfaces, snapshot managers, and remote console. VM Monitor (VMM) process is responsible for virtualizing the guest OS instructions, and managing memory mapping. The VMM passes storage and network I/O requests to the kernel, and passes all other requests to the VMX process. There is a VMM for each virtual CPU assigned to a VM. Mouse Keyboard Screen (MKS) and SVGA processes are responsible for rendering the guest video and handling guest OS user input. When you console into the VM via vCenter client, the work done is charged to this process. This in turn is charged to the VM, and not specific vCPU. If you want to see example of errors in the above process, review this KB article. |
| Layer D | Unmet Demand (CPU Ready, CPU Co-Stop, CPU Overlap, CPU VM Wait, RAM Contention, VM Outstanding IO).  The Guest OS experiences a frozen time or slowness. It’s unaware what it is, meaning it can’t account for it. |

I’ve covered the difference in simple terms, and do not do justice to the full difference. If you want to read a scientific paper, I recommend this paper by Benjamin Serebrin and Daniel Hecht.

#### Resource Management

vSphere uses the following to manage the shared resources:
- Reservation
- Limit
- Share
- Entitlement
Reservation and Limit are absolute. Share is relative to the value of other VMs on the same cluster.
Unlike a physical server, you can configure a Limit and a Reservation on a VM. This is done outside the Guest OS, so Windows or Linux does not know. You should minimize the use of Limit and Reservation as it makes SDDC operations more complex.

[Image: ## Image Description

This is a VMware vSphere **VM Edit Settings screenshot** for a virtual machine named "ARC," showing the **Virtual Hardware tab** with CPU configuration details. The VM is configured with **4 vCPUs** (1 core per socket, 4 sockets), **CPU Reservation set to 0 MHz**, **Limit set to Unlimited**, and **Shares set to Normal (4000)**. 

In the context of the surrounding text, this screenshot visually illustrates the resource management controls discussed — specifically Reservation, Limit, and Shares — demonstrating where these settings are configured at the hypervisor level, outside the Guest OS awareness.]

Reservation represents a guarantee. It impacts the Provider (e.g. ESXi) as that’s where the reservation takes place. However, it works differently on CPU vs RAM.

| CPU | CPU Reservation is on demand. If the VM does not use the resource, then it does not come into play as far as the VM is concerned. The reservation is basically not applied. Accounting wise, it does not impact CPU utilization metrics. Run, Used, Demand, Usage do not include it. Their value will be 0 or near 0 if the Guest OS is not running. |
| --- | --- |
| RAM | Memory Reservation is permanent, hence impacts memory utilization metric. The Memory Consumed counter includes it even though the page is not actually consumed yet. If you power on a 16 GB RAM VM into a BIOS state, and it has 10 GB Memory Reservation, the VM Consumed memory counter will jump to 10 GB. It has not actually consumed the 10 GB, but since ESXi has reserved the space, it is not available to other VMs. If it’s not yet used, then it does not take effect. Meaning ESXi Host does not allocate any physical RAM to the VM. However, once a VM asks for memory and it is served, the physical RAM is reserved. From then on, ESXi continues reserving the physical RAM even though the VM is no longer using it. In a sense, the page is locked despite the VM become idle for days. |

Limit should not be used as it’s not visible to the Guest OS. The result is unpredictable and could create a worse performance problem than reducing the VM configuration. For CPU, it impacts the CPU Ready counter. For RAM, in the VMX file, this is sched.mem.max.

##### Entitlement

Entitlement means what the VM is entitled to. It's a dynamic value determined by the hypervisor. It varies every second, determined by Limit, Shares and Reservation of the VM itself and any shared allocation with other VMs running on the same host. For Shares, it certainly must consider shares of other VMs running on the same host. A VM can’t use more than what ESXi entitles it.
Obviously, a VM can only use what it is entitled to at any given point of time, so the Usage counter cannot go higher than the Entitlement counter.
In a healthy environment, the ESXi host has enough resources to meet the demands of all the VMs on it with sufficient overhead. In this case, you will see that the Entitlement and Usage metrics will be similar to one another when the VM is highly utilized.
The numerical value may not be identical because of reporting technique. vCenter reports Usage in percentage, and it is an average value of the sample period. vCenter reports Entitlement in MHz and it takes the latest value in the sample period. This also explains why you may see Usage a bit higher than Entitlement in highly-utilized vCPU. If the VM has low utilization, you will see the Entitlement counter is much higher than Usage.

#### Overhead vs Not Overhead

Be careful not to lump every additional load as overhead.
- Overhead means it’s mandatory (cannot be avoided) and has negative impact (such as slower performance or more resource required).
- Not Overhead means it’s optional. You do not have to use the feature. Typically, it brings new capabilities that is often not possible to achieve without virtualization.
Let’s list some examples:

| Overhead | ESXi kernel. While it delivers value, it’s not optional and it’s not negligible. It impacts your usable capacity too. |
| --- | --- |
| Overhead | IO processing by hypervisor. There is an additional processing done by the kernel, which could result in IO blender effect. However, this does not reduce the resource allocated to Guest OS. |
| Overhead | VM CPU and Memory overhead for the VM Monitor layer. This is a small amount and operationally negligible. |
| Overhead | ESXi memory consumed and CPU used by vSAN processes. |
| Overhead | VM log files. VM is a layer on its own and the log provides necessary observability. |
| Not Overhead | VM snapshot. Snapshot is optional and it delivers new functionalities not available in Guest OS. |
| Not Overhead | VM memory snapshot. This does not have the same purpose with hibernation file inside Windows or Linux. This feature enables memory overcommit at ESXi level. |
| Not Overhead | vSphere HA. The extra ESXi hosts provides availability protection. |
| Not Overhead | vSAN Failures-to-Tolerate policy. They provide availability protection since vSAN does not use hardware-level redundancy. For workloads where the VM is transient and you have the master template, you can set this to 0 (no protection). |

In addition, there is buffer. There are at least 3 types of buffers:
- Capacity buffer. This reduces the Usable Capacity.
- Cost buffer. This reduces the Sellable Capacity. This is typically on top of the Usable Capacity.
- Disaster Recovery buffer
- Security Attack buffer. This is sometimes call the clean room

## Metric Mastery

There are thousands of metrics across a diverse architecture. How do you master them?
One way is to see the commonality. I studied The USE Method by Brendan Gregg, The RED Method by Weave Works, and the Golden Signal by Google. Based on their strengths and weaknesses, I came up with The Triple See Method, which is designed specifically for Broadcom VCF.

### Triple See Method

There are 3 types of metrics you need to see and verify as 1 integrated set, before you make your final conclusion. These Triple See metric-type are peers, and they have their own purpose:

| Type of Metrics | Primary Application |
| --- | --- |
| Contention | Performance Management |
| Consumption | Capacity Management Cost Management Sustainability |
| Context | Configuration Management Compliance Management Inventory Management |

Let’s explain further:

| Contention | They measure something bad. They can be further divided by their impact Performance. Metrics such as contention, latency, and queue, impact the performance of the system. The system is not down, meaning nothing is dropped, but the overall throughput is reduced. Availability. Metrics such as errors and dropped impact the availability. Most system can recover from soft errors by re-attempting the operations (e.g. retransmit the dropped packet, recalculate the cache, resend the SCSI command). There is lack of observability for such automatic-recovery, and the even the logs may not reveal. |
| --- | --- |
| Consumption | They measure something good. A high number is good for the business, if the load is useful (e.g. not a DDOS attack). Hence, make sure both the patterns and values match your expectation. There are 3 types of consumption. Deploy all 3 techniques above accordingly. |
| Context | They provide answer to the “it depends” type of answer, by accounting for something (e.g. inventory, configuration) and provide context.  The context is obviously only useful to someone who can derive insight from that context, else there is no meaning to it. For example, a high number of vMotion depends on your expectation. If you’re doing cluster live migration after office hours, you expect the number to match the theoretical limit. |

While contention is what you care, consumption gets the limelight as it’s easier to monitor and simpler to explain. Also, many systems do not scale well. Their “performance” drops when reaching certain level of utilization. Take a parallel database. As you add more nodes, the overall throughput drops as the nodes spend more time maintaining overall integrity among them. The CPU utilization of each node gets higher, only to be spent on overhead activities. In this case, what you should do is measures the overhead and the metric you refer to as “performance”. Do not use the CPU utilization to represent all these metrics.
There is a tendency to monitor utilization as if it is a pillar of operations. Just like contention, utilization is not something you manage. Yes, you monitor utilization, but you monitor it for a reason. By itself, utilization has no meaning. The meaning depends on the purpose.

#### Primary | Secondary Metrics

Metrics can be grouped into 2.

| Primary | Secondary |
| --- | --- |
| The “What” It defines the situation. | The “Why” It explains. It covers the possible causes behind the value of the primary metric. |
| Typically only 1 metric per use-case | Typically many metrics to explain that single primary metric. |
| Typically can be color coded | Some can be color coded, some cannot as it’s contextual |
| The unit is normally percentage, where 0% is bad and 100% is good | Unit varies. Examples are GB, MHz, packets/seconds, and milliseconds. |
| Used in Monitoring | Used in Troubleshooting |
| Example: Capacity Remaining (%) | Supporting secondary metrics: CPU Utilisation Memory Usable Capacity CPU Allocation |
| Example: VM Performance (%) | Supporting secondary metrics: VM peak vCPU Ready among all the VM vCPU VM peak Read/Write latency among all the VM virtual disks VM CPU Context Switch |


### Collection

Before we cover the metrics, you need to know how they get collected within a collection period (e.g. 20 second), and what units are used.

#### Interval

When you collect a metric, you have a choice on what to collect:
- Collect the data at that point in time. 
Example: collect the value at 00:00:00.
- Collect the average of all the data within the collection cycle.
Example: collect the average of all values from 00:00:00 to 00:05:00.
- Collect the maximum (or minimum) of all the data within the collection cycle.
The 1st choice is the least ideal, as you will miss majority of the metric. For example, if you collect every 5 minutes, that means you collect the data of the 300th second, and miss 299 seconds worth of data points. On the other hand, it’s good when the latest data is more valuable, such as disk space and free memory.
The 2nd choice gives you the complete picture, as no data is missing. The limitation is your collection interval can’t be too long for the use case you’re interested in.
Comparing the 2 choices, the 1st choice will result in wider fluctuations. You will have a higher maximum and lower minimum over time. Telegraf chooses the 2nd choice, while Tools choose the 1st choice. You can see below the result. Overall, their pattern will be similar, especially for something relatively stable such as memory consumption and disk space consumption.

[Image: ## Image Description

The image shows two time-series charts for the host **wdc-spp-web-1-FNdj** over a ~12-hour period (10 PM Aug 2 – 10 AM Aug 3), comparing **Linux OS Memory|Free (MB)** (top, via Telegraf) and **Guest|Free Memory (MB)** (bottom, via VMware Tools). The top chart shows a higher range (L: 65.73, H: 152.75 MB) while the bottom chart shows a narrower range (L: 74.98, H: 124.1 MB), with both charts exhibiting similar overall patterns including spikes around 3 AM, 6 AM, and 9 AM, and a dip near 4:30 AM. This directly illustrates the surrounding text's claim that **VMware Tools (1st choice) produces wider fluctuations** with higher maximums and lower minimums compared to **Telegraf (2nd choice)**, while both capture the same general memory consumption trend.]

The 3rd choice complements the 2nd choice by picking the worst. That means you need 2 number per metrics for certain use case.
As you collect regularly, you also need to decide if you reset to 0, or you continue from previous cycle. Most metrics reset to 0 as accumulation is less useful in operations.
Let’s take a look at what you see at vCenter UI, when you open the performance dialog box. What do the columns Rollups and Stat Type mean?

[Image: This screenshot shows the **vCenter Performance Chart configuration UI**, displaying CPU metric counters available for charting. Four counters are visible: **Co-stop** (Summation, ms, Delta), **Core Utilization** (Average, %, Rate), **Demand** (Average, MHz, Absolute), and **Idle** (Summation, ms, Delta). The image illustrates the **Rollups** and **Stat Type** columns referenced in the surrounding text, demonstrating how metrics are classified — for example, millisecond-unit metrics (Co-stop, Idle) are Delta type, while Core Utilization is Rate type with percentage units.]

Stat Type explains the nature of the metrics. There are 3 types:

| Delta | The value is derived from a running counter that perpetually accumulates over time. What you see is difference between 2 points in time. As a result, all the units in milliseconds are of delta type. |
| --- | --- |
| Rate | The value measures the rate of change, such as throughput per second. Rate is always the average across the 20 second period. Note: there are metrics with percentage as unit and rate as stat type. I’m puzzled why. |
| Absolute | The value is a standalone number, not relative to other numbers.  Absolute can be latest value at 20th second or the average value across the 20 second period. |

Some common units are milliseconds, MHz, percent, KBps, and KB.
Metrics in MHz is more complex as you need to compare with the ESXi physical CPU static frequency. In large environments, this can be operationally difficult as you have different ESXi hosts from different generations or sport a different GHz. This is one of the reasons why I see vSphere cluster as the smallest logical building block. If your cluster has ESXi hosts with different frequencies, these MHz-based metrics can be difficult to use, as the VMs get vMotion-ed by DRS.

##### Why Milliseconds as Unit?

vSphere uses 3 types of units for CPU: millisecond, MHz and %.
Of the 3, the millisecond is the source. Time is the raw unit, meaning both the percentage unit and the MHz unit are derived from it, because they are expressed as the average/minimum/maximum over time. When we see the CPU demand is 2 GHz at 9:00:00 am what vSphere likely means is it the average from previous collection. It is not a point in time.
Time as a unit to measure CPU utilization does not seem logical. Where does it come from and why?
Hint: the stat type is Delta.
To answer that, we need to see from the ESXi kernel scheduler point of view. Think in terms of the passage of time and the amount of CPU cycles that get completed during that time. A CPU core running at 2 GHz will get 2x CPU cycles completed compared with a core running at 1 GHz. The same goes with Hyper Threading. You get less cycles completed when there is a peer thread competing at the same time.
What you think as utilization or usage or demand or used, it will be easier if you see them as cycles, once you make that small paradigm shift.
Let’s take VM CPU Ready. The following is taken from ESXi vsish command. It shows that the original, raw counter is actually a running number. To calculate the CPU ready of a given time period, we need to subtract the last number from the first number. To convert to percentage, we divide over the collection, which is 20000 ms in the screenshot.

[Image: ## Image Description

The image demonstrates how **VM CPU Ready percentage (%RDY)** is calculated from raw ESXi vsish counter data for vCPU ID **1977647**. Two sequential `vsish` readings (separated by a 20-second sleep) show `ready-time` values of **137,388,718 µsec** and **139,168,396 µsec**, with the delta of **1,779,678 µsec (~1780 ms)** divided by the 20,000 ms collection interval yielding **~8.9% CPU Ready**. The bottom table confirms this vCPU shows **%RDY = 8.02%** in the scheduler statistics, validating that the raw counter is a monotonically increasing cumulative value requiring subtraction between samples to derive the per-interval metric.]

In the above, the slightly different values are due to different time in sample interval start and end.
I’ll take another example, to show that the original unit is time (microsecond, not millisecond).
/sched/groups/169890525/stats/cpuStatsDir/> cat /sched/groups/169890525/stats/cpuStatsDir/cpuStats
group CpuStats {
   number of vsmps:7
   size:19
   used-time:905379300543 usec
   latency-stats:latency-stats {
      cpu-latency:798578245914 usec 
      memory-latency:memory-latency {
         swap-fault-time:0 usec
         swap-fault-count:0
         compress-fault-time:0 usec
         compress-fault-count:0
         mem-fault-time:17939139 usec
         mem-fault-count:3834600
      }
      network-latency:0 usec
      storage-latency:0 usec
In vSphere UI and API, the counter for CPU Latency is percentage. But in the above, you can see that it’s true unit is microseconds.
Because of the above, when collection is running late or the source is busy, the sum may exceed 20000 ms by a bit. In that case, you may see something like this.

[Image: ## Image Description

This VMware vSphere Advanced Performance chart displays **CPU metrics over ~1 hour on 29/11/2025 (11:44–12:43)**, showing two counters: **CPU Idle** (purple, Summation, average ~18,920,989 ms) and **CPU Used** (gray, Summation, average ~1,080,267 ms). The tooltip highlights a data point at **12:28:20 where CPU Idle = 20,211 ms**, which exceeds the theoretical 20,000 ms maximum (20 seconds × 1000 ms per physical second per CPU). This directly illustrates the preceding text's point that **the sum of CPU time components can occasionally exceed 20,000 ms** when collection is running late or the source is busy, validating why values slightly above the expected ceiling can appear in real-world monitoring data.]


##### Rollup Type

The Rollups column tells you how the data is rolled up to longer time period. The types of roll up are:

| Average | This means taking the average of the collected values. vCenter may average 20 values and report it every 20 seconds as a single value. |
| --- | --- |
| Maximum | This means taking the highest value. Useful when you want to catch the outlier. |
| Minimum | The opposite of above. Useful in situations such as free memory. |
| Summation | It is actually average for those metrics where accumulation makes more sense. For example, CPU Ready Time gets accumulated over the sampling period. vCenter reports metrics every 20 seconds, which is 20000 milliseconds. This is why the number keeps going up as you roll up to bigger object. |
| Latest | This is the most recent value. This is useful in cases such as disk space, where you care more about the present value. |

VCF Operations adds percentile, which is useful when you want to ignore outlier.
The following table shows a VM has different CPU Ready Time on each second. It has 900 ms CPU Ready on the 5th and 6th second, but has lower number on the remaining 18 seconds.

[Image: The bar chart displays CPU Ready Time (in milliseconds) for a VM across 20 consecutive seconds (x-axis: 1–20, y-axis: 0–1000 ms). The dominant spikes occur at seconds 5 and 6, both reaching **900 ms**, while the remaining 18 seconds show values between **100–300 ms**. This illustrates why the **average/summation rollup method** obscures peak performance issues — the two 900 ms outliers are diluted when summed across all 20 seconds and divided by 20,000, producing a misleadingly low aggregate value.]

Over a period of 20 seconds, a VM may accumulate different CPU Ready Time for each second. vCenter sums all these numbers, then divides it by 20,000. This is actually an average, as you lose the peak within the period.
Latest, on the other hand, is different. It takes the last value of the sampling period. For example, in the 20-second sampling, it takes the value between 19th and 20th seconds. This value can be lower or higher than the average of the entire 20 seconds period. Latest is less popular compared with average as you miss 95% of the data.
Rolling up from 20 seconds to 5 minutes or higher results in further averaging, regardless of the rollup techniques (summation or average). This is the reason why it is better to use VCF Operations than vCenter for data older than 1 day, as vCenter averages the data further, into a 0.5 hour average.
Because the source data is based on 20-second, and VCF Operations by default averages these data, the “100%” of any millisecond data is 20,000 ms, not 300,000 ms. When you see CPU Ready of 3000 ms, that’s actually 15% and not 1%.
By default, VCF Operations takes data every 5 minutes. This means it is not suitable to troubleshoot performance that does not last for 5 minutes. In fact, if the performance issue only lasts for 5 minutes, you may not get any alert, because the collection could happen exactly in the middle of those 5 minutes. For example, let's assume the CPU is idle from 08:00:00 to 08:02:30, spikes from 08:02:30 to 08:07:30, and then again is idle from 08:07:30 to 08:10:00. If VCF Operations is collecting at exactly 08:00, 08:05, and 08:10, you will not see the spike as it is spread over two data points. This means, for VCF Operations to pick up the spike in its entirety without any idle data, the spike may have to last for 10 minutes.
VCF Operations is capable of storing the individual 20-seconds data. But that would result in 15x more data. In most cases, what you want is the peak among the 15 data points.
The Collection Level in vCenter, shown in the following table, does not apply to VCF Operations. Changing the collection level does not impact what metrics get collected by VCF Operations. It collects majority of metrics from vCenter using its own filter, which you can customize via policy.

| Statistics Levels | Metrics |
| --- | --- |
| Level 1 | Cluster Services (VMware Distributed Resource Scheduler) – all metrics  CPU –entitlement, total MHz, usage (average), usage MHz  Disk – capacity, max Total Latency, provisioned, unshared, usage (average), used  Memory – consumed, mem entitlement, overhead, swap in Rate, swap out Rate, swap used, total MB, usage (average), balloon, total bandwidth (DRAM or PMem) Network – usage (average), IPv6  System – heartbeat, uptime  VM Operations – num Change datastore, num Change Host, num Change Host datastore |
| Level 2 | Level 1 metrics, plus the following: CPU – idle, reserved Capacity  Disk – All metrics, excluding number Read and number Write.  Memory – All metrics, excluding Used, maximum and minimum rollup values, read or write latency (DRAM or PMem).  VM Operations – All metrics |
| Level 3 | Level 2 metrics, plus the following: Metrics for all metrics, excluding minimum and maximum rollup values.  Device metrics |
| Level 4 | All metrics, including minimum and maximum rollup values. |

Take note: vSAN API gives you the last data, not the average or peak of the entire period. Since VCF Operations collect every 5 minutes, you get the data for the 300th second.

##### Real Time Collection

Do we really need real-time collection and analysis for every single metrics, on every single objects, 24 x 7?
We collect the metrics for a reason, such as performance and capacity. The reasons dictate the frequency for each type of metrics.
Take note that how frequent you collect is not the same with how granular the data points. For example, VCF Operations collect every 5 minutes by default from vCenter, but it grabs 15 data points in 1 collection cycle. For majority of the data, it averages these 15 data points and store as 1 number.

| Use Case | Collection Point | Collection Frequency |
| --- | --- | --- |
| Performance: Profiling | 1 – 20 seconds for all counters | 1 – 20 seconds |
| Performance: Troubleshooting | 1 - 20 seconds for raw contention, 5 minutes for everything else. More explanation after this table. | 5 minutes for both |
| Performance: SLA | 5 minutes.  Why SLA differs to troubleshooting and why 5-minute is the sweet spot is covered in the book VMware Operations Transformation, 4th edition. | 5 minutes |
| Capacity | 15 minutes for all. Value is the average over 15 minutes, not the peak. Functionally, you do not need 15-minute granularity. Operationally, it’s safer to do 15 minutes. If there is collection failure, either due to collector or target system, you only lose 15 minutes’ worth of data. | 15 minutes for all. Value is the average over 15 minutes, not the peak. Functionally, you do not need 15-minute granularity. Operationally, it’s safer to do 15 minutes. If there is collection failure, either due to collector or target system, you only lose 15 minutes’ worth of data. |
| Cost | 15 minutes for all. Value is the average over 15 minutes, not the peak. Functionally, you do not need 15-minute granularity. Operationally, it’s safer to do 15 minutes. If there is collection failure, either due to collector or target system, you only lose 15 minutes’ worth of data. | 15 minutes for all. Value is the average over 15 minutes, not the peak. Functionally, you do not need 15-minute granularity. Operationally, it’s safer to do 15 minutes. If there is collection failure, either due to collector or target system, you only lose 15 minutes’ worth of data. |
| Compliance | 15 minutes for all. Value is the average over 15 minutes, not the peak. Functionally, you do not need 15-minute granularity. Operationally, it’s safer to do 15 minutes. If there is collection failure, either due to collector or target system, you only lose 15 minutes’ worth of data. | 15 minutes for all. Value is the average over 15 minutes, not the peak. Functionally, you do not need 15-minute granularity. Operationally, it’s safer to do 15 minutes. If there is collection failure, either due to collector or target system, you only lose 15 minutes’ worth of data. |
| Sustainability | 15 minutes for all. Value is the average over 15 minutes, not the peak. Functionally, you do not need 15-minute granularity. Operationally, it’s safer to do 15 minutes. If there is collection failure, either due to collector or target system, you only lose 15 minutes’ worth of data. | 15 minutes for all. Value is the average over 15 minutes, not the peak. Functionally, you do not need 15-minute granularity. Operationally, it’s safer to do 15 minutes. If there is collection failure, either due to collector or target system, you only lose 15 minutes’ worth of data. |
| Inventory | 15 minutes for all. Value is the average over 15 minutes, not the peak. Functionally, you do not need 15-minute granularity. Operationally, it’s safer to do 15 minutes. If there is collection failure, either due to collector or target system, you only lose 15 minutes’ worth of data. | 15 minutes for all. Value is the average over 15 minutes, not the peak. Functionally, you do not need 15-minute granularity. Operationally, it’s safer to do 15 minutes. If there is collection failure, either due to collector or target system, you only lose 15 minutes’ worth of data. |


##### Performance Troubleshooting

For troubleshooting, you want per-second data. Who does not want sharper visibility? However, there are potential problems:
It may not be possible. The system you’re monitoring may not be able to produce the data, or it comes with capacity or performance penalty.
It’s expensive. Your monitoring system might grow to be as large as the systems being monitored. You could be better off spending the money on buying more hardware, preventing the problem to begin with.
You get diminishing return. The first data point is the most valuable. Subsequent data points are less valuable if they are not providing new information.
The remediation action is likely the same as there are only a handful of things you can do to fix the problem. The number of problems outweigh the actual solution.
So what can you do instead?
Begin with the end in mind. Look at the solution (e.g. add hardware, change some settings) and ask what metrics are required. For each required metrics, ask what granularity is required.
I find that 1 – 20 second is only required for the contention-type of metrics. For utilization-type and contextual-type, I think 5 minute is enough. You need higher resolution when the contention-type metrics do not exist. For example, there is no metric for network latency and packet retransmit at VM level. All you have is packet dropped. To address the missing metrics, use utilization metric such as packet per second and network throughput.

#### Units

No thanks to lack of consistent implementation among vendors, there is a common confusion on units.

##### 1000 vs 1024

There is confusion between 1024 and 1000.
- Is 1 gigabyte = 1024 megabyte or 1000 megabyte?
- Is 1 Gigabit = 1000 Mb or 1024 Mbit?
The answer from Google is 1000 for both.
Google does not distinguish network throughput and storage throughput

[Image: The image shows a Google unit conversion result demonstrating that **1 Gigabyte = 1000 Megabytes**, using the decimal (base-10) conversion formula of multiplying by 1000. This supports the surrounding text's point that Google uses the **1000-based (SI/decimal) standard** rather than the binary 1024-based standard. The example illustrates the vendor inconsistency discussed in the text, where Google and theoretical standards use 1 GB = 1000 MB, while many storage and network vendors use the binary convention (1 GB = 1024 MB) in practice.]

As expected, Google uses 1 byte = 8 bits

[Image: The image shows a **unit conversion calculator** demonstrating that **1 Gigabyte per second (GB/s) = 8,000 Megabits per second (Mbps)**, using the formula of multiplying by 8,000. In the context of the surrounding text, this illustrates that Google's conversion tool uses the **decimal (base-10) standard** (1 GB = 1,000 MB) combined with the **1 byte = 8 bits** relationship, yielding 8,000 rather than 8,192 (which would result from binary/base-2 conversion). This serves as a reference point before the author discusses how many vendors deviate from this standard by using binary conversions instead.]

However, many products from many vendors use the binary conversion instead of decimal. This is one of those issues, where what’s popular in practice is different to what it should be in theory.
To add further confusion, there is consistency among storage and network vendors. For example, you get shortchanged when you buy storage hardware.
Guess how many GB do you actually get from this 128 GB? This screenshot is from the vendor official website. I think many hardware vendors do the same.

[Image: ## Image Description

This is a screenshot from the **Western Digital official product page** for the **SanDisk Ultra Fit USB 3.2 Flash Drive** (Part# SDCZ430-128G-G46), showing the **128GB capacity option selected** (highlighted in black and circled in green). The page displays available capacity variants: 16GB, 32GB, 64GB, 128GB, 256GB, and 512GB, with a 5-Year Limited Warranty noted.

In the context of the surrounding text, this image serves as evidence that the **vendor advertises 128GB using decimal (base-10) measurement**, while Windows and VMware VCF Operations report only **116GB** (using binary/base-1024 conversion) — representing a **~9% capacity loss** from the consumer's perspective.]

The answer is 116 GB.
The following is the above actual disk in Windows 11.

[Image: ## Image Description

This is a **Windows 11 Properties dialog** for a SanDisk USB drive (Drive D:), showing storage capacity metrics. The drive reports **125,077,028,864 bytes total capacity**, displayed as **116 GB** by Windows, with **2.50 MB used** and **116 GB free**, using the **exFAT** file system.

This screenshot demonstrates that Windows uses **1024-based (binary) calculations** (GiB), confirming the "9% loss" discussed in the surrounding text — a marketed **128 GB** drive only shows **116 GB** in Windows because 125,077,028,864 ÷ 1024³ ≈ 116.44 GiB, illustrating the discrepancy between vendor decimal (1000-based) and OS binary (1024-based) storage reporting.]

You lost 9%!
Microsoft Windows use 1024 for storage.
VCF Operations use 1024 for storage, 1024 for network, 1024 for memory, but 1000 for CPU.
Here is the proof for storage. Yes, I validated network and memory too.

[Image: ## Image Description

The image displays a **VMware vCenter/VCF Operations metric chart** titled "Virtual Disk:scsi0:0|Configured Size (KB)" showing two data points both at **52,428,800 KB**. This value (52,428,800 KB ÷ 1,024³) equals exactly **50 GB in binary (GiB)**, confirming the surrounding text's assertion that **VCF Operations uses 1024-based calculations for storage metrics** — a 50 GB configured virtual disk is represented in kibibytes rather than kilobytes.]


[Image: ## Image Description

The chart displays **Virtual Disk:scsi0:0 | Configured Size (GB)** for what appears to be two VMs (or data points), showing values of **50 GB** (orange, top), an unlabeled smaller value ~**16 GB** (blue, middle), and **50 GB** (orange, bottom).

In context, this chart demonstrates that VCF Operations reports virtual disk sizes using **1024-based calculations**, which explains why three disks totaling a nominal 116 GB appear as shown — consistent with the binary (GiB) storage measurement methodology being discussed.

The data supports the author's proof that VCF Operations uses **1024 for storage** conversions, contrasting with the 1000-based convention used for CPU metrics.]

VCF Operations use 1000 for CPU

|  |  |
| --- | --- |


##### Kilo vs Kibi

To address the confusion, the committee at International System of Quantities came up with a new set of name for the binary units. Instead of kilo, mega, giga, they use kibi, mebi and gibi.
It is confusing to drop familiar terms like kilo, mega and giga. I prefer kilobi instead of kibi as it shows the relationship to the commonly known units. Or if you want to emphasize the binary nature, perhaps kilo2byte, mega2byte, giga2byte as the name.
Let’s take an example
- 1 Kibibyte = 1024 bytes. That means 1 Kibibyte = 1.024 KB.
- 1 Gibibyte = 1024 Mebibytes = 1,073,741,824 bytes
The abbreviation is also changed from K, M, G to Ki, Mi, Gi, where the letter i is small case. This confuses the population further as Ki can mean Kilo or Kibi. I’d have chosen another letter instead of i.
Note the conversion from byte to bit remains. 1 byte = 8 bit.

##### Bit vs Byte

Do you use Byte/second or bit/second?
To me, it depends on the context. If you talk about disk space, you should use byte. You measure the amount of disk space read or written per second. If you talk about network line, you should use bit. You measure the amount of SCSI blocks travelling inside ethernet or FC cable. Pearson uses 1024 for disk space, and 1000 for transmission speed, in their certification. There are other references, such as gbmb.org, NIST, and Lyberty. In short, there is really no standard.
The following is network transmit. It’s showing 30.81 MBps. So this is a rate, showing bandwidth consumption or network speed.

[Image: The chart displays **Network Data Transmit Rate in MBps** over a time period from approximately 5:00 AM to 6:00 PM, with a **high (H) of 30.81 MBps** and a **low (L) of 4.21 MBps**. The metric remains relatively flat (~4 MBps) throughout most of the day, with a significant spike of activity occurring between approximately **11:00 AM and 12:30 PM**, peaking at 30.81 MBps (marked with an orange dot near 12:00 PM). This chart serves as the baseline example in the surrounding text for unit conversion demonstrations, showing the raw MBps value that is subsequently converted to KBps and Mbps (bits).]

What would it show if you convert into KBps?
30810, if it uses 1000.

[Image: ## Image Description

The chart displays **Network Data Transmit Rate in KBps** over a single day (approximately 6:00 AM to 6:00 PM), with a **high (H) of 31,553.13 KBps** and a **low (L) of 4,314.87 KBps**. The metric is largely stable near baseline (~4-5K KBps) throughout the day, with a significant **spike cluster around 11:30 AM–12:00 PM** reaching the peak value of ~31,553 KBps (marked with an orange dot). This chart demonstrates vRealize's use of **1 Mega = 1024 Kilo** conversion, explaining why the ~30.81 MBps value from the previous chart translates to **31,553.13 KBps** rather than 30,810 KBps (which would result from a 1000-based conversion).]

Since vRealize treats 1 Mega = 1024 Kilo, the above is what you get.
Since it’s network, let’s convert into bit.
What do you expect you get in Mbps?

[Image: ## Image Description

This is a time-series line chart displaying a network metric (likely **Mbps**) over a single day from approximately 5:00 AM to 6:00 PM, with a **High (H) of 246.51** and a **Low (L) of 33.71**. The chart shows a dramatic spike between approximately **11:00 AM and 12:30 PM**, peaking at **246.51** (marked with an orange dot), while the baseline remains relatively flat near 33.71 throughout the rest of the day. This chart demonstrates the conversion result referenced in the surrounding text — converting 30.81 MBps network transmit rate into **Mbps (megabits per second)**, yielding the peak value of ~246.51 Mbps (consistent with the formula: `30.81 × 1024 × 8 / 1024 ≈ 246.51`).]

You get 31 x 553.13 x 8 bits / 1024 = 246 / 51.

### Aggregation

We discussed in earlier part of the book about data collection. After collecting lots of data across objects and across time, how do you summarize so you get meaningful insight?
Aggregating to a higher-level object is complex as there is no lossless solution. You are representing a wide range of values by picking up 1 value among them, so you lose some details. The choices of techniques are mean, median, maximum, minimum, percentile, sum and count of.

#### The Problem with Average

The default technique used by many observability tools is the average() function as that represents every value to be aggregated. Average is great across time, but not across members of a group.
The problem is it will mask out the outlier unless they are widespread. By the time the average performance of 1000 VMs is bad, you likely have a hundred VMs in bad shape.
Let’s take an example. The following table shows ESXi hosts. The first host has CPU Ready of 149,116.33 ms. Is that a bad number?

[Image: ## Image Description

The image shows a **VMware vSphere ESXi host performance table** with four hosts displaying **CPU Co-stop, CPU Ready, and VM count metrics**. The first host (36 cores, 67 VMs) is highlighted in green with critically high values: **Co-stop of 7,627.33 ms** and **CPU Ready of 149,116.33 ms**, while the second similar host (36 cores, 45 VMs) shows elevated but lower values (4,832.73 ms / 128,698.73 ms), and the remaining two hosts show near-normal metrics. This demonstrates the outlier masking problem described in the text — the first host is severely CPU-contended, and averaging these values across all hosts would obscure the severity of the performance issue on that specific host.]

It is hard to conclude. It depends on the number of running vCPU, not the number of physical cores.
That host has 67 running VMs, and each of those VMs can have multiple vCPU. In total there are 195 vCPU. Each vCPU could potentially experience CPU Ready of 20,000 ms (which is the worst possible scenario).
If you sum the CPU Ready of the 67 VM, what number would you get?

[Image: ## Image Description

The image shows a **VMware vSphere performance table** listing running VMs on an ESXi host, displaying three metrics: **CPU Ready (ms)**, **Co-Stop (ms)**, and **vCPU count** per VM. The 8 visible VMs show CPU Ready values ranging from **1,556.07 ms to 2,108.6 ms**, with vCPU counts of 2–8 per VM, and the table displays aggregate **Sum values of 149,116.33 ms (CPU Ready)**, **7,627.33 ms (Co-Stop)**, and **195 vCPUs** across 50 total VMs (shown across 3 pages). This illustrates the concept that ESXi-level CPU Ready is the **summation of all VM CPU Ready values**, which is why converting to a percentage requires dividing by the total running vCPU count (195) rather than physical core count.]

You’re right, you get the same number reported by the ESXi host.
This means the ESXi CPU Ready = Sum (VM CPU Ready), and the VM CPU Ready = Sum (VM vCPU Ready).
Because it’s a summation of the VMs, to convert into % requires you to divide with the number of running VM vCPU.
ESXi CPU Ready (%) = ESXi CPU Ready (ms) / Sum (vCPU of running VMs)
Are the CPU Ready values equally distributed among the VMs? What do you think?
It depends on many settings, so there is a good chance you get something like the following. This heat map shows the 67 VMs on the above host, colored by CPU Ready and sized by VM CPU configuration. You can see that the larger VMs tend to have higher CPU ready, as they have more vCPU.

[Image: ## Heat Map Description

This treemap/heat map displays **CPU Ready distribution across 67 VMs** on a single ESXi host, where **cell size represents vCPU count** and **color represents CPU Ready severity** (red = high CPU Ready, green = low/acceptable, brown/olive = intermediate values). The visualization clearly demonstrates the correlation described in the surrounding text: **larger cells (VMs with more vCPUs) trend toward red (higher CPU Ready)**, while smaller VMs are predominantly green. This illustrates that CPU Ready is not equally distributed — VMs with higher vCPU counts experience disproportionately greater CPU Ready contention, supporting the formula `ESXi CPU Ready (%) = ESXi CPU Ready (ms) / Sum(vCPU of running VMs)`.]


#### Lagging vs Leading Indicators

When it comes to performance management, you need to see the problem while it’s still early, when only a small percentage of users or applications are affected. For that, you need a leading indicator, not a lagging indicator (after the fact). Leading indicators complement the lagging indicator by giving the early warning, so you have more time to react.
Performance use the contention metric as its primary input. The problem with contention metrics is it drops (or spike, depending on how you see it) suddenly, typically at the point of overcommit. It differs to consumption metrics which goes up towards 100%.

[Image: The chart illustrates a **contention metric** (y-axis: 0–100%) plotted over time, showing a flat line at 100% that drops sharply near the **95th percentile** marker (indicated by a green dotted vertical line). This demonstrates the characteristic behavior of contention metrics described in the text — remaining stable until an overcommit threshold is reached, then dropping suddenly rather than gradually declining like consumption metrics. The 95th percentile reference point highlights why average is insufficient as a rollup metric, as the steep drop only affects a small percentage of users but would be obscured by averaging across the full dataset.]

As a result, average is not suitable for rolling up performance metrics to higher level parents. For example, a VDI system that was designed for 1000 users should serve the first 1000 well, and it should struggle after the capacity is exceeded.
Average is a lagging indicator. The average of a large group tends to be low, so you need to complement it with the peak. On the other hand, the absolute peak can be too extreme, containing outliers.
The following chart shows where Maximum() picks up the extreme (outlier) while average fails to detect the problem. This is where the worst 5th percentile or the worst 1st percentile makes more sense.

[Image: The image shows a 2D heatmap grid (0-100 on both axes) with a green-to-red color gradient illustrating how different aggregation methods position data points differently in terms of severity detection. Three data points are plotted: **Max()** sits in the top-right red zone (highest severity, ~90-95 on both axes), the **95th percentile** sits in the orange zone (~75-80), and **Average** sits in the green zone (~40-45), appearing benign. This visually demonstrates that Average() masks performance problems while Max() may be overly sensitive to outliers, making the 95th percentile the recommended balance for groups with >20 members.]

These are the techniques to complement average(). Depending on the situation, you apply the appropriate technique.

| Worst() | This returns the worst value of a group.  It’s suitable when the number of members is low, such as ESXi hosts in a cluster or containers in a Kubernetes pod. It’s also suitable for hourly value, as there are only 12 data points. If you want to ignore outlier, then use Percentile function. |
| --- | --- |
| Percentile() | It is similar to the Worst() function, but it returns the number after eliminating a percentage of the worst. See this handy calculator to learn the percentile function. I’ve summarized the most common scenarios, showing the worst 5th percentile works well the number of members is less than 100. If the number of members is >250, I’d take 97th percentile (3 standard deviations). The problem with percentile is it picks a single member. It cannot tell if there is a population problem. |
| Average of Worsts | This solves the percentile by averaging all the numbers above the percentile. If you take the average from 95th percentile to 100th percentile, you represent all these numbers. This results in a number that is more conservative than 95th percentile.  This is superior to percentile as the band between 95 – 100 may vary. By not hardcoding at a single point, you pick a better representation. |
| Average of Worsts | The limitation of this technique is when you have outlier. It can skew the number. If you suspect that, choose a lower percentile, such as 90th or 92.5th percentile. |
| Count() | This is different to the Worst() or Percentile(), as you need to define the threshold first. For example, if you do Count of VM that suffers from bad performance, you need to define what bad is. That’s why Count() requires you to define the band for red, orange, yellow and green. You can then track the number of objects in the red band, as you expect this number to be 0 at all times. Waiting until an object reaches the red band can be too late in some cases, so consider complimenting it with a count of the members in orange band. |
| Count() | Count() works better than average() when the number of members is very large. For example, in a VDI environment with 100K users, 5 users affected is 0.005%. It’s easier to monitor using count as you can see how it translates into real life. |
| Sum() | Sum works well when the threshold for green is 0. Even better, the threshold for yellow is 0. With this, you just need to watch when the total is above 0. The main limitation of Sum() is setting the threshold. You need to adjust the threshold based on the number of members. If there are many members, it’s possible that they are all in the green, but the parent is in the red. |
| Disparity() | When members are uniformed and meant to share the load equally, you can also track the disparity among them. This reveals when part of the group is suffering when the average is still good. |

In some situations, you may need multiple metrics for more complete visibility. For example, you may need Worst for the depth and Percentile for the breadth. In this case, pick one of them as the primary and the rest as secondary metrics. You can also use worst and worst 5th percentile numbers together for better insight. If the numbers are far apart, that indicates the Worst number is likely an outlier. If the numbers are similar, you have a problem

#### “Peak” Utilization

One common requirement is the need to monitor for peak. Be careful in defining peak, as by default, averages get in the way.
How do you define peak utilization or contention without being overly conservative or aggressive?
There are two dimensions of peaks.
- Peak across time of the same metric.
- Peak among members of the group at the same time
Let's take a cluster with 8 ESXi hosts as an example. The following chart shows the 8 ESXi utilizations.
What’s the cluster peak utilization on that day?
The problem with this question is there are 1440 minutes in a day, so each ESXi Host has at least 288 metrics (based on the 5-minute reporting period). So this cluster has 288 x 8 = 2304 metrics on that day. A true peak has to be the highest metric among these 2304 metrics.

[Image: The image shows two bar charts of **ESXi Host Utilization** across 8 hosts, captured at two different time points: **9:05 AM** and **11:05 PM**, each representing a **5-minute average**. The bar heights vary across hosts at both timestamps, with different hosts showing peak utilization at each time period (e.g., host 1 appears tallest at 9:05 AM, while a different host peaks at 11:05 PM). This illustrates the core challenge described in the text: identifying the true cluster peak requires evaluating **2,304 individual data points** (288 samples × 8 hosts) across time, as the highest-utilized host changes between sample periods.]

To get this true peak, you need to measure across members of the group. For each sample data, take the utilization from the host with the highest utilization. In our cluster example, at 9:05 am, host number 1 has the highest utilization among all hosts. Let’s say it hit 99%. We then take it that the cluster peak utilization at 9:05 am is also 99%.
You repeat this process for each sample period (e.g. 9:10 am, 9:15 am). You may get different hosts at different times. You will not know which host provides the peak value as that varies from time to time.
What’s the problem of this true peak?
Yup, it might be too sensitive. All it takes is 1 number out of 2304 metrics. If you want to ignore the outlier, you need to use percentile. For example, if you do 99th percentile, it will remove the highest ~23 datapoints.
Take note that the most common approach is to take the average utilization among all the 8 ESXi hosts in the cluster. So you lose the true peak, as each data point becomes an average. For the cluster to hit 80% average utilization, at least 1 ESXi host must have hit over 80%. That means you can't rule out the possibility that one host might hit near 100%.
The same logic applies to a VM. If a VM with 64 vCPUs hits 90% utilization, some cores probably hit 100%. This method results in under-reporting as it takes an average of the “members” at any given moment, then take the peak across time (e.g. last 24 hours).
This “averaging issue” exists basically everywhere in monitoring, as it’s the default technique when rolling up. For a more in-depth reading, look at this analysis by Tyler Treat.
There is another nuance of peak.

#### Depth vs Breadth

There are 2 dimensions of problem:
- How deep or acute is the problem?
- How widespread is the problem?
Both measure the severity of the problem.
A deep problem is suitable for a single entity. For example, if a VM has a very high CPU ready, it’s worth looking into.
A broad problem is suitable for the population. For example, if many VMs experience a moderate CPU ready, it’s worth looking into. You do not want to wait until the CPU ready becomes higher. As a result, use a lower threshold.
What do you notice from the following screenshot? There are 2 metrics, the maroon line shows the worst among all the VMs in the cluster, the pale blue shows the cluster wise average.

[Image: ## Chart Description

The chart displays two CPU contention metrics for **east-mgmt** cluster from January 16-23: the cluster-average CPU contention (pale blue line, ~0.55%) and the maximum VM CPU contention super metric (maroon line, peaking at **8.83%** on Jan 20 at 2:00-2:29 PM). The maximum metric shows a step-change increase around January 19, rising from ~2.5% to a sustained **7.5-10%** range, while the cluster average remains nearly flat near **0%** throughout. This demonstrates the critical difference between average and maximum aggregation — the average completely masks a severe per-VM contention problem, illustrating why maximum-based super metrics are essential for detecting localized resource starvation in a cluster.]

Notice the Maximum is >10x higher than the average. The average is also very stable relative to the maximum. It did not move even though the maximum became worse. Once the Cluster is unable to cope, you’d see a pattern like this. Almost all VMs can be served, but 1-2 were not served well. The maximum is high because there is always one VM that wasn’t served.
Be careful when you look at metrics at parent object such as cluster and datastore, as average is the default counter used in aggregation. Here is another example. This shows a cluster wise average. What do you think of the value?

[Image: ## Image Description

The chart displays **CPU Contention (%)** for a VMware ESXi cluster over a **7-day period (March 9–16)**, showing an average aggregated metric. The values remain extremely low, ranging from a **high of 0.49%** to a **low of 0.0161%**, with most readings hovering near **0.25% or below**. This demonstrates the book's point that **cluster-level averages mask individual VM performance issues** — the near-zero average appears healthy, but could obscure a small number of VMs experiencing significant contention while the majority perform well.]

That’s right. No performance issue at all in the last 7 days. The cluster is doing well. This cluster run hundreds of VMs. What you see above is the average experience of all these VMs, aggregated at cluster level. If there is only a few VMs having a problem, but the majority are not, the above fails to show it.
Now look at the pattern. You can see there are changes in that 1 week period.
What do you expect when you take the worst of any VM? Would you get the same pattern?

[Image: ## Image Description

The chart displays **CPU | Worst VM CPU Contention (%)** over a 7-day period (March 9–16), showing the **maximum CPU contention experienced by any single VM** in the cluster. The metric peaks at **H: 32.109%** and drops as low as **L: 0.0693%**, with values frequently hovering near **20%** — roughly **60x worse** than the cluster average shown previously. The chart demonstrates a cyclical pattern of high contention punctuated by sharp drops to near-zero, illustrating that while the cluster-level average appeared healthy, individual VMs are experiencing significant CPU contention on a rotating basis — supporting the concept that "worst VM" metrics expose hidden performance problems invisible in averaged data.]

Answer is possible (not always!), if every VM is given the same treatment. They will take turn to be hit.
Notice the scale. It’s 60x worse.
The following diagram explains how such thing can happen.

[Image: The chart displays disk latency (ms) for 6 disk groups over a 35-minute window (9:00–9:35), with individual group latencies oscillating between ~0–21ms in alternating peaks and valleys. The thick red line tracks the **maximum latency among all 6 groups**, remaining consistently elevated at **~18–22ms** even as individual groups cycle through low values. This demonstrates the "round-robin" effect described in the surrounding text: individual objects take turns experiencing high latency, so while any single disk group's average appears moderate, the worst-case (maximum) metric remains persistently high — approximately **60x worse** than the average would suggest.]

The above charts show 6 objects that have varying disk latency. The thick red line shows that the worst latency among the 6 objects varies over time.
Plotting the maximum among all the 6 objects, and taking the average, give us two different results as shown below:

[Image: The chart displays two metrics over a 35-minute window (9:00–9:35): **Max latency among all VMs** (blue line, oscillating between ~18–21 ms) and **Average latency among all VMs** (pink line, steady at ~5 ms). Two SLA threshold lines are marked — 23 ms (green, "good") and 14 ms (red, "bad") — illustrating that the same underlying data can appear compliant or non-compliant depending on which SLA threshold is applied. This demonstrates that using **average latency masks the true worst-case experience**, as the max is consistently 3–4x higher than the average, and would breach a 15 ms SLA while the average remains well below it.]

If you don’t have the SLA Line, how do you know how much buffer you have?
Proactive monitoring requires insights from more than one angle. When you hear that a VM is hit by a performance problem, your next questions are naturally:
- How bad is it? You want to gauge the depth of the problem. The severity also may provide a clue to the root cause.
- How long did the problem last? Is there any pattern?
- How many VMs are affected? Who else are affected? You want to gauge the breadth of the problem.
Notice you did not ask “What’s the average performance?”. Obviously, average is too late in this case.
The answer to the 3rd question impacts the course of troubleshooting. Is the incident isolated or widespread? If it’s isolated, then you will look at the affected object more closely. If it’s a widespread problem then you’ll look at common areas (e.g. cluster, datastore, resource pool, host) that are shared among the affected VMs.
How do you calculate the breadth of a problem?
There are 2 methods:
- Threshold based. You determine the percentage of the population above a certain threshold. The limitation is defining the threshold is hard as it depend on the metric.
- Percentile based. You determine the number at certain percentile. I recommend 90th percentile as average is too late and you want a leading indicator. The limitation is you don’t know the percentage of the population.
I recommend the percentile-based as it can be consistently applied to any metric.
The following table uses the threshold-based.

[Image: ## Image Description

This table defines a **color-coded severity framework** for VMware vSphere performance metrics, organized across two dimensions: **"How Broad?"** (percentage of VMs affected) and **"How Deep?"** (maximum severity on individual VMs). The breadth metrics (% VMs with CPU Ready >1%, RAM Contention >1%, Disk Latency >10ms) use thresholds of **0–2.5% (Green)**, **2.5–5% (Yellow)**, **5–10% (Orange)**, and **10–15% (Red)**, while depth metrics (Max VM CPU Ready, RAM Contention, Disk Latency) have independent thresholds — for example, Disk Latency ranges from **0–10ms (Green)** to **40–80ms (Red)**. In context, this threshold-based table provides the classification boundaries referenced in the surrounding text, enabling operators to assess both the **scope** and **severity** of infrastructure performance problems simultaneously.]

The following shows an example where both breadth and dept confirm you have a CPU Ready problem.

[Image: The image shows two VMware vSphere charts side by side: **"% VMs with CPU Ready"** (breadth) and **"Worst VM CPU Ready %"** (depth), both spanning May 12–16. The right chart displays key percentile markers: a minimum of **1.54%**, a maximum of **50.7%**, and a current value of **2.81%**, with recurring spikes visible across both charts. Together, these charts demonstrate the concept described in the surrounding text — that **both breadth (percentage of affected VMs) and depth (worst-case CPU Ready value) confirm a CPU Ready performance problem** when spikes appear consistently across both metrics.]


#### Usage Disparity

Imbalance among utilization can reveal a problem, as there are many examples where you expect balance utilization:
- Usage among VM vCPU. If a VM has 32 vCPU, you don’t want the first 8 are heavily used while the last 16 are not used.
- Usage among ESXi in a cluster
- Usage among RDS Hosts in a farm
- Usage among Horizon Connection Server in a pod
- Usage among disk in a vSAN disk group
- Usage among web server in a farm
We define imbalance as highest – lowest.
It is expressed in percentage, meaning we need to divide over something. There are 2 options:
- Divide over total. This is a fixed number, as the total is a constant number.
- Divide over max (highest). This is a dynamic number, as the max is fluctuating. The imbalance is relative, as it depends on the value of the Max metric.
Both use cases have their purpose. We are taking the first use for these reasons:
- That’s the most common one. The second use case is used in low level application profiling or tuning, not general IaaS operations.
- It’s also easier to understand.
- It does not result in high number when imbalance is low in absolute terms. See the charts below

[Image: ## Image Description

The image shows two bar charts comparing CPU utilization across 4 CPUs (CPU 0–3) under two scenarios. **Scenario 1 (High imbalance)** displays dramatically varied utilization: ~25%, ~65%, ~100%, and ~85% respectively. **Scenario 2 (Low imbalance)** shows uniformly low utilization: ~10%, ~15%, ~25%, and ~25% respectively.

The charts demonstrate why **absolute imbalance** (max minus min) is preferred over **relative imbalance** (divide by max) for IaaS monitoring — Scenario 2 would produce a misleadingly high relative imbalance ratio (~150% spread relative to max) despite all CPUs being lightly loaded with only ~10–15% absolute difference between them.]

The following calculation shows that using the relatively imbalance results in a high number, which can be misleading as the actual imbalance is only 10%

[Image: The image shows a VM vCPU utilization table with 10 CPUs, where CPU 1 has 10% utilization and CPUs 2-10 each have 1%, yielding a 2% VM average. The accompanying metrics box calculates an imbalance of 9% (highest 10% minus lowest 1%), with **Imbalance over Highest** at **90%** (highlighted in red) versus **Imbalance over Total** at **9%** (highlighted in green). This demonstrates the misleading nature of relative imbalance calculation — where dividing by the highest value (10%) produces an inflated 90% imbalance figure, while the total-based method yields a more representative 9%, supporting the author's argument for using the latter approach.]


## Performance Modelling

There are 3 main reasons why we need to model performance of a system or object into a simple, higher-level set of metrics.

| Persona | Monitoring is first performed by Level 1 operators. As first line of defence, they need to cover wide not deep. It’s not practical to track many metrics for thousands of objects. In addition, some of the raw metrics require specialist knowledge. |
| --- | --- |
| Scale | A single metric enables monitoring at scale. For example, if you have a single metric representing a VM, you can do aggregation on these VMs. |
| Reporting | Senior IT management prefer to see a higher-level metric as it’s easier to relate to the business. They understand VM Performance (%) but may not appreciate CPU CoStop (ms). |

Quantifying something complex with many components is difficult. It’s like trying to figure out the inflation rate of a country. It’s impossible to have the Consumer Price Index that properly represents the economy as different individuals have different baskets of goods. Even if we could develop the basket for each individual, that basket changes each year, rendering comparison with previous year invalid.
On the other hand, a country needs the number in order to manage its economy. The approximation is certainly much better than nothing.
Let’s take another example. This time, we go down to a much smaller scope. A person, you or me. We take annual health check, performing all sort of tests, and the results will be a series of metrics (e.g. your bad cholesterol level). Are they 100% accurate for you from young until you are old? Are the guidelines 100% accurate for everyone in your country?
Beside the absolute value, the relative movement of the value over time also provides insight. The patterns and trends over time are useful for management.
Now that we’ve seen real life examples, can we apply them to IT systems? For example, how do we define the performance of a large system such as vSphere, NSX, Horizon or Kubernetes?
The challenge is there are many components that makes up this metric. There is a need to consolidate all the performance metrics into a single KPI so you can manage at scale.
Say you have 1000 AWS EC2 instances to be monitored. You have a bunch of metrics, and you then consolidate them into 2 KPIs instead of 1. How would you know which EC2 has issues? You need to show 2 sets of heat map or table. That means you need to manually corelate the first table with the second. It’s not scalable operationally.
Having >1 metric also presents challenge as you roll up to higher level object. How do you show a trend chart of performance over time at vSphere data center levels when you have >1 metric?
After years of trials and improvements on the model, I’m happy to share that we can define system performance as a metric. This means you can have the performance metric for any object, such as vSphere Cluster Performance (%) and Kubernetes Node Performance (%).

### Calculation

Performance is defined as 0 – 100%. 100% means best possible performance. This means a perfect score of 100.00% is not possible as certain contention such as disk latency cannot be 0.
0% means it’s at your worst expectation, not the absolute slowest possible. For example, if you expect 40 ms as the least you can tolerate, then the value will turn to 0% when disk latency hits 40 ms.
We use 4 colors, so we can divide 100% into 4 equal parts. So Green is simply 75% - 100% and Red is simply 0% - 25%. This is more natural than dividing into 3, where you end up with odd numbers such as 33.33% and 66.67%.
The other advantage is it gives you leading indicator (shown as yellow).

[Image: The image displays a **4-band color scale** ranging from 0% to 100%, divided into equal 25-point intervals: **Red (0–25%), Orange (25–50%), Yellow (50–75%), and Green (75–100%)**. A bidirectional arrow beneath the scale indicates the spectrum from worst (right, 0%) to best (left, 100%) performance. This visualization illustrates the KPI scoring framework described in the surrounding text, demonstrating how equal-width bands simplify threshold definition for vSphere performance metrics.]

Why don’t we make green 95% - 100%? 75% for green sounds rather bad or low.
My answer is if you create an unequal distribution, some bands will have to be narrower than others. With uneven bands, you also need to be extra careful when defining the threshold for each metric that make up the KPI. I made the 4 bands equal, so the thresholds are easier to set.
Making the threshold easy to set is critical. As you design your KPI, you will vrealize that the threshold is the hardest part. In fact, I exclude metric when I do not feel comfortable with its threshold.
The following KPI uses 4 metrics as its input. Each metric has a set of thresholds for green, yellow, orange and red.

[Image: ## Image Description

This table defines **color-coded thresholds for four vSphere performance metrics**: Consumed RAM (%), Active RAM (%), Dropped Packet (%), and Disk Latency (ms), across four severity bands (Green, Yellow, Orange, Red). The thresholds progress linearly — for example, Consumed RAM escalates from 80% (Green) → 85% → 90% → 95% → 100% (Red), while Disk Latency ranges from 0ms to 40ms in equal 10ms increments. Greyed-out cells (Consumed RAM at 80%, Active RAM at 30%, and Dropped Packet's Green threshold) represent **special baseline values** that are neither 0, 100%, nor infinity, illustrating the challenge of defining KPI thresholds where the "healthy" starting point is a non-trivial number.]

Now that we have the threshold for each metric, we can convert each metric into green – red. The model is also able to handle when the entire range is defined by a single number. This is useful when you want to define green = 0. That means a single packet loss will put the metric into the yellow range already.
What if anything above 0 is red?
You simply set 0 for green, yellow and orange. Within the red zone, you can set 0 – 1, or 0 to something.

#### Translation

Since the metrics have different units, we need translate to a common unit so we can aggregate.
How do we translate a row?
Let’s use an example. Take the Disk Latency (%) metric. It has range from 0 to 40 ms, which maps into the 0 – 100% using the following mapping table.

[Image: ## Image Description

The image displays a **VM Disk Latency translation table** showing how raw millisecond values (0–40 ms) map to a 0–100% KPI scale across four color-coded severity zones: Green (0–10 ms → 75–100%), Yellow (10–20 ms → 50–75%), Orange (20–30 ms → 25–50%), and Red (30–40 ms → 0–25%). Below the mapping table, four concrete examples demonstrate the translation: **9 ms → 77.5% (Green)**, **11 ms → 72.5% (Yellow)**, **21 ms → 47.5% (Orange)**, and **42 ms → 0% (Red)**. This illustrates the normalization mechanism that converts heterogeneous metrics with different units into a common percentage-based scale for aggregation purposes.]

With the above mapping, we can be precise in assigning the value. For examples:
- 9 millisecond disk latency translates into KPI value of 77.5%, which is green. The reason is green ranges from 75% to 100%, where 0 ms equals to 100% and 10 ms equals to 75%. So each millisecond is around 2.5%.
- 42 millisecond disk latency translates into 0%. It is above the upper threshold of 40 millisecond. Since we do not show negatives, anything above the limit is shown as 0%

#### Threshold

The threshold is designed to support proactive, not alert-based operations. Hence, the red range does not mean emergency and you must drop everything. It means you need to take a look within the next 24 hours. This also gives you time to evaluate how many times it falls into the red zone and the overall trend.
The threshold could be argued from 2 ways:
- Scientifically
- “Practically”
Scientifically, a VM does not care what’s stopping it. Whether it’s Ready or Co-Stop or Overlap, the Guest OS does not know. Using this logic, you should set all the threshold the same way. On the other hand, you can follow what happens in production, in healthy environment. These metrics do not follow the same scale.
I take the lowest of the two, as the requirement is proactive monitoring.
If you have many metrics that make up the KPI, and one of them is red but the remaining is all green, the overall KPI value may not reveal that there is problem. That single red does not have enough weight to bring down the rest.
So how do we solve it?
Enter progressive weightage.
We assign weightage so that yellow is 2x green, orange is 2x yellow and red is 2x orange. Mathematically, a single red has equal weightage with 8 green. The following table shows that 1 perfect red and 8 perfect green will result in the score of 50.

[Image: ## Image Description

The table demonstrates **progressive weightage scoring** with 9 metrics: rows 1–8 each have a Score of 100 and Weightage of 1 (Adjusted Score = 100), while row 9 has a Score of 0 (red/critical) with Weightage of **8**, resulting in an Adjusted Score of 0. The total weightage sums to **16**, producing a final **Total Adjusted Score of 50.00**, illustrating that a single "perfect red" metric (weighted 8x) mathematically cancels out 8 perfect green metrics (each weighted 1x). This demonstrates the core principle that in progressive weightage, one red indicator carries equal weight to eight green indicators combined.]

That also means that if you have 1 perfect red, and your green are not perfect, you can expect your value to be in the orange category.
This relative weightage plays a key role in determining the threshold. Try to match the actual value so they also correspond to 1x 2x 4x 8x. For example, set the VM disk latency so it goes up from 20 ms  40 ms  80 ms  160 ms. Notice they always double.

[Image: ## Image Description

This table defines a **KPI scoring framework** for six VMware vSphere performance metrics (Peak CPU Queue Length per vCPU, Peak Disk Queue Length, Peak Network TX Dropped Packets, CPU Run-CPU Overlap, VM Memory Ballooned, and VM Memory Compressed+Swapped), organized into four color-coded performance bands (Green, Yellow, Orange, Red) corresponding to KPI percentage ranges (75-100%, 50-75%, 25-50%, 0-25%). Each band carries an exponentially increasing **weightage multiplier of 1X, 2X, 4X, and 8X** respectively, with thresholds that consistently double across bands (e.g., CPU Queue Length: 0-1, 1-2, 2-4, 4-8). The image demonstrates how degrading performance exponentially penalizes the composite KPI score, supporting the surrounding text's explanation that a single "perfect red" metric (8X weight) can offset eight "perfect green" metrics (1X each), yielding a 50% KPI score.]

Note that this method does not replace assigning different weightage to each metric. You can still do that.

### Optional Features

The above model is capable of handling many cases. To handle more complex requirements, apply any of these optional techniques. They can also be used together or individually.

#### Important Metrics

What if some metrics are relatively more important than others?
Give it a higher weightage. If metric A is 2x more important than metric B, then ensure metric A weightage is 2x of metric B.
If both are equally important, but the chance of metric B hitting bad is 2x higher, then give it 2x the weightage if you want an earlier warning.
The sum of all weightages is 100%. In the following example, the CPU is given highest weightage. Notice they sum to exactly 100%

| Metric | Weightage |
| --- | --- |
| CPU Usage | 40% |
| Memory Usage | 20% |
| Disk Usage | 20% |
| Network Usage | 20% |


#### Multi-table KPI

What if you have a long list of metrics and they are equally important? For example, if you have 21 metrics, and one of them is red while others are green, that single red will not be able to pull the overall KPI down low. If you want the KPI to be low because the issue is severe, you need to split the large table into smaller table. Ensure the grouping is logical.
For example, a Kubernetes cluster can be affected by either infrastructure problem or application (workload) problem. If we combine all the metrics, each metric has a relatively low weightage, as their sum is 100%. We solve this by combining them into 2. We then take the lowest of the 2 sub-KPI metrics.
Creating a 2nd table is also useful for override.
How do you deal with a serious problem that rarely happens? What weightage do you give it? Take for example, error packet in Kubernetes. Say you give it 40%, because it is a serious hit on performance. But since it rarely happens, then this 40% is basically a given. If you want to avoid taking 40% from the total weightage, you take this metric from the row, and place it on a separate table. This 2nd table overrides the first table with its value if it produces a lower value.
For example, if there is any error packet, you want to set the KPI value to red to reflect that there is a severe problem happening.

### Validation

Once you design the KPI for a specific object, always do a validation. This helps you validates if the thresholds, weightage, metrics actually deliver the score that matches your expectation. Write down the common scenarios along with the expected value.
I got a surprise on the result, that I thought there was a bug in the formula. Remember that 1 red has the weight of 8 green? So when I see 3 reds and 9 greens, I expect the value to be in the red, which is below 25. But I got a low orange.
So let’s do some validation. I find testing the corner case useful. So let’s see what value we get when we have 9 perfect green and 3 worst red. What value do you expect?
A simple, non-weighted average will give a value of 75. This is right in the border of green or yellow.
What color does the weightage score give us?

[Image: ## Image Description

The table displays a weighted scoring calculation with 12 metrics: rows 1–9 each have a **Score of 100** with a **Weightage of 1** (Adjusted Score: 100 each), while rows 10–12 have a **Score of 0** with a **Weightage of 8** (Adjusted Score: 0 each). The summary row shows a total weightage of **33** and a total adjusted score of **900**, yielding a final weighted average of **27.27**. This demonstrates that even with 9 perfect green scores (100) and 3 worst-case red scores (0 with 8x weight), the weighted formula produces **27.27**—a low orange rather than red—validating that the 8:1 red-to-green weighting heavily penalizes red metrics but still doesn't push the result into the red zone.]

It gives us a low orange. It is not red, but close enough to be red. This is why the score is important too, not just the color.
What if your red is not the worst, but barely red? How many borderline red (near 25%) required before a perfect green (100%) is showing red?
The following table shows 1 perfect green score and 11 barely-red scores. What color do you get at the end?

[Image: ## Image Description

The table displays a scoring scenario with **12 items**: item 1 has a perfect score of **100** with weightage **1** (Adjusted Score: 100), while items 2–12 each have a borderline-red score of **24.9** with weightage **8** (Adjusted Score: 199.2 each). The **Summary row** shows a total weightage of **89**, combined Adjusted Score of **2291.2**, and a final weighted score of **25.74**.

This demonstrates that **11 barely-red scores (24.9%) combined with 1 perfect green (100%)** still produce an orange result (~25.74) rather than red, illustrating how the weightage system prevents individual borderline-red metrics from dragging the overall score into red territory.]

Yup, you get orange, not red. It takes many red scores, which makes it practically impossible to get a red if each red is barely there. That’s why your red threshold needs to be 2x your orange threshold. If you make it too big, you will get barely-red in most cases.
In actual environment, you certainly do not want to see red, even in development environment. Each VM will have their own score, but overall you want to see majority green. Use heatmap to show, as it will automatically order them by the value.

[Image: ## Image Description

This is a **live heatmap** displaying VM performance scores across three vCenter/VMC environments: **EVN-HS1-VC2**, **VMC_CMBU-PRD-VMCOrg-M15GA-06-10-21**, and **VMC_CMBU-PRD-VMCOrg-M16GA-10-06-21**, with a color scale ranging from **0 (red) to 100 (green)**. The majority of VMs show **green to yellow scores**, indicating healthy performance, but several VMs in the M15GA cluster display **orange cells** (scores roughly 25-40), with a couple approaching red. This demonstrates the text's point about using heatmaps to visualize VM scores ordered by value, where the goal is predominantly green with minimal orange/red indicators.]

Chapter 2