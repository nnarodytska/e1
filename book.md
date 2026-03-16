
[Image: This is the **cover page** of a technical book titled *"vSphere Metrics: Deep Dive into VMware vCenter and ESXi Performance and Capacity Counters"* by Iwan "e1" Rahabok of VMware Cloud Foundation at Broadcom (e1@broadcom.com). The cover features a dark space/galaxy background with a circular geometric overlay, styled with cyan/blue typography. No performance data or metrics charts are displayed — this is purely a title/cover image introducing the book's subject matter of VMware vSphere performance monitoring and capacity planning.]

.
Back of cover page.
Delete if you do not plan to print.

[Image: This is not a technical chart or dashboard — it is a **vintage family photograph** (likely from the 1960s–70s, based on the color degradation and styling) showing a couple with a young toddler standing on a table beside a **birthday cake**, posed in a modest home interior.

In the context of the surrounding text, this image serves as a **personal dedication page** from the author of a VMware vSphere Metrics book, honoring his parents ("Mama and Papa") who raised him in **Surabaya, Indonesia** ("Suroboyo" being the local Javanese name for the city).

No technical data, metrics, or chart values are present in this image.]

The book is in your hands because of the couple above. 
It is dedicated to the loving memory of Mama and Papa… 
for your love and sacrifice in raising me in the old town of Suroboyo.
Foreword
Digital transformation is one of the most significant contributors to business transformation. In this digital era, data center modernization, application modernization, and cloud repratiation are the norms. Broadcom VMware Cloud Foundation is at the core of these transformations for many companies globally.
Iwan has spent 3+ decades in the field working with companies of various sizes to make their "IT operaitons transformation" a success. He is the go-to person for our product managers, UX designers & engineering for mapping VMware Cloud Foundation metrics into day-to-day operations. I first met him back in 2015 VMworld and he has since become a trusted technical advisor to our product management team globally.
The book is deeply technical in content. Reading this book feels like having a conversation with Iwan. He has taken time to explain the concept, showing the value of each metric, and mapping them together to answer real-world questions. Many oddities make sense and complexities clear once you understand the underlying architecture.
I am always thankful to have him in my team and proud of his accomplishments. His passion for helping companies run VMware optimally has led him to open-source the book. There is still much to document in the vast body of knowledge that makes up operations management and I hope the VMware community responds to his call for collaboration.
Kameswaran Subramanian
Product Management
VMware Cloud Foundation
Broadcom
Reviewer
John Yani Arrasjid is currently a Field Principal at VMware, Inc. Prior to this he was CTO/CIO at Ottometric, a startup focused on intelligent validation of systems and sensors in the automotive space using AI, Computer Vision, and Deep Learning to increase accuracy, shorten analysis time, and reduce cost. He has spent a lifetime working as an innovation architect and technical evangelist in his roles.
John is co-founder of the IT Architect Series. John is an author with multiple publishing houses on multiple technical topics. He has worked on patents covering workload modelling, blockchain, and accelerator resource management. John was previously the USENIX Association Board of Directors VP. He is currently active in both CERT (Community Emergency Response Team) and VMware ERT (Emergency Response Teams), and is also a Disaster Service Worker.
John continues his interest in IT architecture, autonomous systems, AI, IoT/Edge, Big Data, and Quantum Computing.
Online, John can be reached at LinkedIn.com/in/johnarrasjid/ and Twitter @VCDX001.

| Acknowledgement | A technical book like this took a lot of contribution from many experts. Allow me to highlight one as I use his work the most. Valentin Bondzio thank you for the permission to use your work. Find some of his public talks at his blog.  I’m indebted to the advice and help from folks like Kalin Tsvetkov, Branislav Abadzhimarinov, Prabira Acharya, Stellios Williams, Brandon Gordon, George Stephen Manuel, Sandeep Byreddy, Gayane Ohanyan, Hakob Arakelyan, Ming Hua Zhou, Paul James, Evgeni Kumanov, Asha Kumari and many others. |
| --- | --- |

How To Use This Book
The book is designed to be consumed as offline Microsoft Word document on Windows. It is not designed to be printed. Its table of content is the side menu of Microsoft Word. Follow the steps shown on following screenshot:

[Image: ## Image Description

This is a **Microsoft Word interface screenshot** serving as a how-to guide for navigating the VMware vSphere Metrics book. It demonstrates three key navigation instructions via annotated red dashed arrows: **(1)** enabling the **Navigation Pane** (View menu → Navigation Pane) to use as a dynamic Table of Contents showing hierarchical sections (Metrics Complexity, Architecture, VM CPU, VM Storage, VM Network, Performance, ESXi), **(2)** enabling **Multiple Pages** view, and **(3)** switching to **Print Layout Mode** via the bottom status bar. The document is shown at **Page 13 of 346** with **69,011 words**, displayed in a multi-page layout showing pages 4–11 simultaneously.]

Use the navigation pane as a dynamic table of content, else it’s easy to get lost even when using 43” monitor. If you simply read it top down, without having the navigation on the left, you will feel that the chapters end abruptly. The reason is each chapter does not end with a summary, which is required in printed books but redundant in online books.
Preface
vSphere ships with many metrics and properties. If we take object by object, and document metrics by metrics, it will be both dry and theoretical. You will be disappointed as it does not explain how your real world problems are solved. You’re not in the business of collecting metric.
This document begins with you; experienced VMware professionals tasked with optimizing and troubleshooting production environment. It documents the metric following the Triple See Method, a technique that maps metrics into operations management.
This is advanced-level book. At 400+ pages, it is not a light reading. It is a companion book to Private Cloud Operations book. So grab a cup of coffee or your favourite drink and enjoy a quiet read of both books.
The book is far from completing its mission. The vSphere Cluster chapter and Microsoft Windows chapter are partially finished. I’ve included them as they are still useful to you, and it’s useful for me to get your feedback. Beyond vSphere, vSAN metrics and NSX metrics are not yet added. Beyond metrics, we have events, logs, and properties.
The main reason why I open source the book is it is a call for collaboration to the VCDX, VCIX and all VMware professionals.
By now you get the hint that this book is not a product book. It does not cover how to use vSphere Client performance tab, esxtop, and VCF Operations. There are better manuals on that already😉
This page is intentionally left blank.
Why? I don’t know. Some people do it, so I just follow as IT behaves more like fashion nowadays…
Chapter 1

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

# Storage


## Architecture

To understand storage metrics, be aware that there are 2 dimensions of metrics (speed and space). Both the speed and space dimensions have consumption metrics, but they are completely different.
For speed, the counters are IOPS and throughput, where throughput = IOPS x block size.
For space, the counters are disk space.

| Speed | Performance is measured in 2 ways (contention and utilization).  Contention can happen at all 3 stages of IO processing: pre-processing: each layer has their own queue or outstanding IO.  processing: aborted SCSI commands, dropped frame, etc. post-processing: latency. |
| --- | --- |
| Space | Capacity has no impact of slowness in modern, SSD based storage as access to data is no longer relying on spinning platter. 1% disk space full is not slower/faster than 99% full as defragmentation is no longer causing latency. However, it impacts availability. At 100% full, the storage will stop processing IO and your application will crash as a result. Capacity, as in disk space, is measured in bytes.  Storage differs to compute as reality overwrites projection. In compute, you use a projected capacity remaining number, which takes into account the past. In storage, if you have 0 bytes left, the number overwrites whatever number shown by capacity engine. You should also focus on reclamation as the amount tends to be substantial. |


### Storage Layers

Virtualization increases the complexity in both storage capacity and performance. Just like memory, where we have more than 1 level, we have multiple layers of storage and each layer only has control over its own. In addition, each layer may not use the same terminology. For example, the term disk, LUN and device may mean the same thing. A device is typically physical (something you can hold, like an SSD card). LUN is typically virtual, a striping across physical devices in a volume.
The layers present challenge in management, as they create limitation in end-to-end visibility and raise different questions. You lose VM-level visibility in the physical adapter (for example, you cannot tell how many IOPSs on vmhba2 are coming from a particular VM) and physical paths (for example, how many disk commands travelling on that path are coming from a particular VM).
Storage in VMware IaaS is presented as datastore. In some situation, RDM and network file shares are also used by certain VM.

[Image: ## Image Description

This architectural diagram illustrates the VMware vSphere storage stack, showing how virtual machine disks traverse multiple abstraction layers — from **Guest OS** through the **Virtual Machine (Motherboard)** and **ESXi Virtualization Layer** down to six physical storage types: **PT, Local Datastore, vSAN, vVOL, RDM, and Shared Datastore** (the latter four residing on a Physical Storage Array). The diagram visually demonstrates the key monitoring challenge described in the surrounding text: the virtualization layer abstracts underlying storage protocols (FC, iSCSI, etc.), presenting all storage to the Guest OS as local SCSI disks (e.g., `scsi0:0`), eliminating end-to-end visibility. The many-to-many relationship arrows between VM virtual disk connectors and physical storage targets illustrate why per-VM IOPS attribution at the physical adapter or path level is not directly observable.]

Underlying storage protocol (FC, iSCSI, vSAN, vVOL) is not exposed. Guest OS needs not support the protocol as it’s transparent.

| Layer | Description |
| --- | --- |
| Guest OS | The most upper layer is the Guest OS. It sees virtual disks presented by the VM motherboard. Guest OS typically has multiple partition or drive. Each partition has its own filesystem, serving different purpose such OS drive, paging file drive, and data drive. A large database VM will have even more partitions. Partition may not map 1:1 to the virtual disk. There is no visibility to this mapping. This makes calculating unmapped blocks accurately an impossible task in the case of RDM disk. |
| Guest OS | To make it more complex, there is also networked drive. Windows or Linux mounts them over protocol such as SMB. These filesystems are not visible to the hypervisor; hence they are not virtual disk. The disk IO is not visible to the VM as it goes out via vNIC. |
| VM | See the VM Layer section below |
| ESXi | See the ESXi Layer section below |
| Datastore | See the Datastore Layer section below |
| Storage Subsystem | This can be virtual (e.g. vSAN) or physical (e.g. physical array). If it’s NFS, it can be virtual server or physical. The datastore is normally backed one to one by a LUN, so what we see at the datastore level matches with what we see at the LUN level.  Multiple LUNs reside on a single array. Datastores that share the same underlying physical array can experience problem at the same time. The underlying array can experience a hot spot on its own, as it is made of independent magnetic disks or SSD. |


### VM Layer

The preceding storage layers resulted in 3 different layers of “disks” from the VM downwards. The blue boxes show the 3 layers.

[Image: ## Image Description

This diagram illustrates the **VM storage layer hierarchy** in VMware vSphere, showing two VM configurations with their virtual disk (vDisk) mappings via SCSI controllers (scsi0:0, scsi0:1, scsi0:2) down to underlying storage types. The left VM demonstrates three storage backends — **VMFS Datastore** (backed by a physical Disk), **NFS Datastore**, and **RDM** (Raw Device Mapping, also backed by a physical Disk) — while the right VM shows both disks mapped to **VSAN**. The diagram specifically highlights the **three distinct blue storage layers** (vDisk → Datastore/storage type → physical Disk) referenced in the surrounding text, illustrating how VMs abstract underlying shared storage into simple virtual SCSI disks regardless of the actual storage backend.]

Remember the 3 blue boxes. You will see them, no more no less, in vSphere Client UI. To enable us to focus on the blue boxes, I’ve excluded non virtual disk files such as snapshot and memory swap in the preceding diagram.
The first layer is virtual disk. This exists because the VM does not see the underlying shared storage. It sees as simple local SCSI disks only, as presented by the VM motherboard. This explains why MS-DOS can run on fibre channel, because it’s unaware of the underlying storage architecture.
A virtual disk is identified as scsiM:N, starting with scsi0:0, where M is the adapter bus number.
A virtual disk can sit on top of different underlying storage architecture. I’ve shown 4 in the preceding diagram: NFS, VMFS, vSAN, and RDM. A VM can also be presented with ESXi local physical disk as direct passthrough, although that means the VM cannot run on other ESXi host.
For block datastore (read: VMFS), it can span multiple disks. It is called extend in vSphere. Avoid doing this as it complicates operations. That’s why in the preceding diagram I show a 1:1 relationship.
The discrepancy between VM layer and Guest OS utilization happens because each layer works differently.
If there is RDM or thick VMDK, VM can’t see the actual used inside Guest OS. It simply sees 100% used, regardless of what Windows or Linux uses.
If there is unmapped block, Guest OS can’t see this overhead.
We are interested in data both at the VM aggregate level, and at the individual virtual disk level. If you are running a VM with a large data drive (for example, Oracle database), the performance of the data drive is what the VM owner cares about the most. At the VM level, you get the average of all drives; hence, the performance issue could be obscured.

#### Metric Mapping

While there is a 1:1 mapping between Guest OS and its underlying VM, not all metrics map. The following table explains it:

| Type | Guest OS Metrics | VM Metrics |
| --- | --- | --- |
| Contention | OS Queue | None, as VM is not an OS. Because it is a motherboard, the driver is specific to the Guest OS. |
| Contention | Driver Queue | None, as VM is not an OS. Because it is a motherboard, the driver is specific to the Guest OS. |
| Contention | Latency | Latency. They should be similar, especially when plotted over time. |
| Utilization | IOPS | They should match with the metrics at VM level, especially when plotted over time. If not, there is something wrong. |
| Utilization | Throughput | They should match with the metrics at VM level, especially when plotted over time. If not, there is something wrong. |


#### Performance

Latency can happen when IOPS and throughput are not high, because there are multiple stacks involved and each stack has their own queue. It begins with a process, such as a database, issuing IO request. This gets processed by Windows or Linux storage subsystem, and then send to the VM storage driver.
Ensure that you do not have packet loss for your IP Storage, dropped FC frames for FC protocol, or SCSI commands aborted for your block storage. They are a sign of contention as the datastore (VMFS or NFS) is shared. The metrics Bus Resets and Commands Aborted should be 0 all the time. As a result, it should be fine to track them at higher level objects. Create a super metric that tracks the maximum or summation of both, and you should expect a flat line.
Once you have ensured that you do not have packet loss on IP Storage or aborted commands on block storage, use the latency counter and outstanding IO for monitoring. For troubleshooting, you will need to check both read latency and write latency, as they tend to have different patterns and value. It’s common to only have read or write issue, and not both.
Total Latency is not (Read Latency + Write Latency) / 2. It is not a simple summation. In a given second, a VM issues many IOPS. For example, the VM issues 100 reads and 10 writes in a second. Each of these 110 commands will have their own latency. The “total” latency is the average of these 110 commands. In this example, the total latency will be more influenced by the read latency, as the workload is read dominated.
If you are using IP storage, take note that Read and Write do not map 1:1 to Transmit (Tx) and Receive (Rx) in Networking metrics. Read and Write are both mapped to Transmit counter as the ESXi host is issuing commands, hence transmitting the packets.

#### Capacity


[Image: ## Image Description

The diagram illustrates the **layered abstraction of VM storage capacity** across three perspectives: the Hypervisor layer (VMDKs and RDM), the Guest OS layer (Disks and Partitions), and the VM overhead layer (Config, Log, Swap, Suspend, Snapshot files). The total storage span is shown as **0–1 TB**, with three virtual disks (VMDK 1, VMDK 2, RDM 1) mapping to three Guest OS disks (Disk 1, Disk 2, Disk 3), which further map to two partitions. The blue overhead components (Config, Log, Swap, Suspend, Snapshot) exist **outside the Guest OS visibility**, directly supporting the surrounding text's point that compute virtualization overhead is not visible to the Guest OS.]

A VM can consume storage via:
- Virtual disk. 
Each virtual disk has label, type (RDM or VMDK), provisioning type (thin, lazy zero, eager zero). If it’s RDM, need to know additional properties such as RDM type (physical or virtual).
- Compute virtualization. 
Snapshots, Swapped, Logs. Guest OS can’t see them.This can be overhead and non-overhead. This is not visible to the Guest OS. They are shown in blue in the following diagram.
- Storage virtualization. 
This includes vSAN protection, deduplication and decompression. We need this number to reported separately as it’s not applicable in non vSAN.
There are more file types than shown above. However, from monitoring and troubleshooting viewpoint, the above is sufficient.

### ESXi Layer

Storage at ESXi is more complex than storage at VM level. Reason is ESXi virtualizes the different physical storage subsystem, and VM simply consumes all of them as local SCSI drive. The kernel does the IO on behalf of all the VMs. It also has its own kernel modules, such as vSAN.
Typically, multiple VMs run on the same ESXi, and multiple ESXi hosts mount a shared datastore. This creates what is popularly termed “IO Blender” effect. Sequential operations from each VM and kernel modules become random when combined together. The opposite is when the kernel rearranges these independent IOs and try to sequence them, so on average the latency is lower.

[Image: ## Image Description

The diagram illustrates the **ESXi 6 storage stack architecture**, showing the hierarchical relationship between storage adapters (vmhba3 labeled on adapters 2 and 3), storage paths, and datastores (NFS, VMFS, RDM, and VSAN) terminating at physical media (Disk, SSD, Magnetic). The blue boxes represent **metric collection layers** (vmnic, Storage Adapters, Storage Paths, datastores) that correspond to vCenter performance chart metric groups, while green boxes represent the logical storage constructs visible to administrators. This visualization contextualizes the "IO Blender" effect by showing how multiple storage paths converge through abstraction layers, explaining why per-VM metrics become unavailable at the physical storage layer.]

The green boxes are what you are likely to be familiar with. You have your ESXi host, and it can have NFS Datastore, VMFS Datastore, vSAN Datastore, vVOL datastore or RDM objects. vSAN & vVOL present themselves as a VMFS datastore, but the underlying architecture is different. The blue boxes represent the metric groups you see in vCenter performance charts.
Just like compute virtualization, there is no more association to VM for metrics at physical layers.
In the central storage architecture, NFS and VMFS datastores differ drastically in terms of metrics, as NFS is file-based while VMFS is block-based.
- For NFS, it uses the vmnic, and so the adapter type (FC, FCoE, or iSCSI) is not applicable. Multipathing is handled by the network, so you don't see it in the storage layer.
- For VMFS or RDM, you have more detailed visibility of the storage. To start off, each ESXi adapter is visible and you can check the metrics for each of them. In terms of relationship, one adapter can have many devices (disk or CDROM). One device is typically accessed via two storage adapters (for availability and load balancing), and it is also accessed via two paths per adapter, with the paths diverging at the storage switch. A single path, which will come from a specific adapter, can naturally connect one adapter to one device. The following diagram shows the four paths:

[Image: ## Image Description

The diagram illustrates a **four-path Fibre Channel/iSCSI storage topology** between an ESXi host and a Physical Storage Array, showing two HBA ports (vmhba1, vmhba2) connecting through two fabric switches (Switch A, Switch B) to two storage controllers (Controller A, Controller B) in a cross-connected mesh. The topology demonstrates **multipathing architecture** where each adapter has two paths (diverging at the storage switch level), resulting in four total paths for redundancy and load balancing. This centralized storage model contrasts with vSAN's distributed architecture, explaining why adapter/path metrics are **aggregate only** (no per-VM breakdown) and why vSAN datastores have no equivalent path-level metrics — as vSAN eliminates the discrete HBA→Switch→Controller path construct entirely.]

The counter at ESXi level contains data from all VMs and the kernel overhead. There is no breakdown. For example, the counter at vmnic, storage adapter and storage path are all aggregate metrics. It’s not broken down by VM. The same with vSAN objects (cache tier, capacity disk, disk group). None of them shows details per VM.
Can you figure out why there is no path to the VSAN Datastore?
We’ll do a comparison, and hopefully you will realize how different distributed storage and central storage is from performance monitoring point of view. What look like a simple change has turned the observability upside down.

#### Storage Adapter

The screenshot shows an ESXi host with the list of its adapters. We have selected vmhba2 adapter, which is an FC HBA. Notice that it is connected to 5 devices. Each device has 4 paths, giving 20 paths in total.

[Image: The screenshot shows the **Storage Adapters** view in vSphere for ESXi host `vmsgesxi008.vmsg.lab`, with **vmhba2** (Emulex LPe12000 8Gb PCIe Fibre Channel Adapter) selected, showing **4 targets, 5 devices, and 20 paths** — demonstrating a many-to-many relationship typical of FC SAN connectivity. The adapter details panel confirms its WWNN (`20:00:00:00:c9:c0:4d:83`) and WWPN (`10:00:00:00:c9:c0:4d:83`), which are identifiers specific to Storage Fabric. This serves as the **FC SAN baseline for comparison** against vSAN's simpler 1:1:1 target-device-path mapping described in the surrounding text.]

What do you think it will look like on vSAN? The following screenshot shows the storage adapter vmhba1 being used to connect to two vSAN devices. Both devices have names begin with “Local”. The storage adapter has 2 targets, 2 devices and 2 paths. If you are guessing it is 1:1 mapping among targets, devices and paths, you are right.
We know vSAN is not part of Storage Fabric, so there is no need for Identifier, which is made of WWNN and WWPN.

[Image: The screenshot shows VMware vSphere Storage Adapters configuration with three adapters: **vmhba1** (12G SAS HBA, SAS type, Unknown status, **2 targets/2 devices/2 paths**), **vmhba64** (iSCSI Software Adapter, Online, 0 targets/devices/paths), and **vmhba0** (Lewisburg SATA AHCI, Block SCSI, 1 target/1 device/1 path). The Devices tab at the bottom shows two vSAN disks attached to vmhba1: a **Local ATA Disk (1.75 TB, Flash)** and a **Local TOSHIBA Disk (372.61 GB, Flash)**, both with "Attached" operational status and linked to the same datastore (sc2c...). This demonstrates the 1:1:1 mapping of targets-to-devices-to-paths characteristic of vSAN storage adapters, contrasting with more complex multi-path SAN configurations.]

Let’s expand the Paths tab. We can see the LUN ID here. This is important. The fact that the hypervisor can see the device is important. That means the kernel can report if there is an issue, be it performance or availability. This is different if the disk is directly passed through to the VM. The hypervisor loses visibility.

[Image: ## Image Description

The image shows the **Paths tab** in VMware vSphere for a local storage adapter, displaying two active paths: **vmhba1:C0:T2:L0** (Local ATA Disk, `naa.5002538c407105ed`) and **vmhba1:C0:T0:L0** (Local TOSHIBA Disk, `naa.58ce38ee2001475d`), both with **LUN ID 0** and **Active (I/O)** status. This demonstrates hypervisor-level visibility into local disk paths, contrasting with direct passthrough configurations where the hypervisor loses device visibility. The presence of LUN IDs and Active (I/O) status confirms the kernel can monitor both performance and availability metrics for these devices.]


#### Storage Path

Continuing our comparison, the last one is Storage Path. In a fibre channel device, you will be presented with the information shown in the next screenshot, including whether a path is active or not.

[Image: ## Image Description

The screenshot displays the **VMware vSphere Storage Devices panel** with a selected NETAPP Fibre Channel Disk (1.98 TB, LUN 3) and its associated **Device Details > Paths tab** highlighted by a red arrow. The Paths tab shows **four active paths** (vmhba2:C0:T3:L3, vmhba2:C0:T2:L3, vmhba2:C0:T1:L3, vmhba2:C0:T0:L3), all connected via vmhba2 adapter to the same target (50:0a:09:80:8d:31:4e:46). Two paths show **Active (I/O)** status while two show simply **Active**, demonstrating the multipathing configuration referenced in the surrounding text where not all paths carry I/O simultaneously.]

Note that not all paths carry I/O; it depends on your configuration and multipathing software. Because each LUN typically has four paths, path management can be complicated if you have many LUNs.
What does Path look like in vSAN? As shared earlier, there is only 1 path.

[Image: ## Image Description

The screenshot displays **ESXi storage devices and path information** in vSphere Client, showing 3 storage devices: a 1.75 TB Local ATA Disk and a 372.61 GB Local TOSHIBA Disk (both Flash/SAS, assigned to the **sc2c01vsan01** datastore via vmhba1), plus a 223.57 GB Local ATA Disk (Flash, vmhba0, **Not Consumed**). The **Paths tab** at the bottom confirms the vSAN path behavior described in the surrounding text, showing only **a single active path** (vmhba1:C0:T0:L0) with **Active (I/O)** status and marked as Preferred. This directly illustrates the claim that vSAN storage devices have only one path, contrasting with the multiple paths typical in Fibre Channel configurations.]


#### Storage Devices

The term drive, disk, device, storage can be confusing as they are often used interchangeably in the industry. vSphere Client uses the terms device and disk interchangeably. In vSphere, this means a physical disk or physical LUN partition presented to ESXi host.
The following shows that the ESXi host has 3 storage devices, all are flash drive and the type = disk. The first two are used in vSAN datastore and are accessed via the adapter vmhba1.

[Image: ## Storage Devices Screenshot Description

The image shows the **Storage Devices panel in vSphere Client** for an ESXi host, displaying 3 local flash storage devices: a 1.75 TB ATA disk, a 372.61 GB TOSHIBA disk, and a 223.57 GB Micron disk. The first two devices are consumed by the **sc2c01vsan01** vSAN datastore via adapter **vmhba1** over SAS transport, while the third is "Not Consumed" and uses vmhba0 via Block Adapter. The Properties panel details the selected TOSHIBA disk (naa.58ce38ee2001475d), showing key attributes including **512e sector format, NMP ownership, Fixed (VMware) multipathing policy, and VMW_SATP_LOCAL** storage array type policy.]

A storage path takes data from ESXi to the LUN (the term used by vSphere is Devices), not to the datastore. So if the datastore has multiple extents, there are four paths per extent. This is one reason why you should not use more than one extent, as each extent adds 4 paths. If you are not familiar with VMFS Extent, Cormac Hogan explains it here.
For VMFS (non vSAN), you can see the same metrics at both the Datastore level and the Disk level. Their value will be identical if you follow the recommended configuration to create a 1:1 relationship between a datastore and a LUN. This means you present an entire LUN to a datastore (use all of its capacity). The following shows a VMFS datastore with a NetApp LUN backing it.

[Image: ## Image Description

This screenshot shows the **Device Backing** configuration panel for a VMware VMFS datastore named **SDDC-Datastore-01-FC-NetApp64** in vSphere. It displays a single extent backed by a **NetApp Fibre Channel Disk** (NAA ID: `naa.60a98000375435474 83f3334554e6556`) with **1.00 TB** allocated to the VMFS partition out of a total device capacity of **1.50 TB**, formatted as **GPT**. This illustrates the recommended **1:1 datastore-to-LUN relationship** concept referenced in the surrounding text, though notably this example shows only 1.00 TB of the 1.50 TB LUN is consumed by the VMFS extent, leaving unallocated space.]

In vSAN, there is no connectivity and Multipathing menu. There is also no Capability Sets menu. vSAN datastore is not mapped to a LUN. It is supported by disk groups.

### Datastore Layer

What you can see at this level, and hence how you monitor, depends on the storage architecture.
The underlying storage protocol can be files (NFS) or blocks (VMFS). vSAN uses VMFS as its consumption layer as the underlying layer is unique to vSAN, and hence vSAN requires its own monitoring technique. Because vSAN presents itself as a VMFS datastore you need to know that certain metrics will behave differently when datastore type is vSAN.
For VMFS datastore, the VM IO commands are passed down as is to the Pluggable Storage Architecture (PSA) layer. There is one queue (schedQ) made for each vmdk on each VM. The metrics at this layer is are collected at that layer.
For NFS datastore, as it is network file share (as opposed to block), you have no visibility to the underlying storage. The type of metrics will also be more limited, and network metric becomes more critical.

#### Relationship

A datastore has relationship to 3 other objects:
- VM
- ESXi
- Cluster
A datastore typically has 1:M relationship to VM. It is also typically shared by multiple ESXi. If you design such that a VM spans multiple datastores, and a datastores spans multiple clusters, you create a trade-off in terms of observability.
The value of datastore metric excludes VMDK that is not on the datastore. It includes every files in the datastore, including orphaned files outside the VM folder. Logically, it also excludes RDM.
I created a simple diagram below, with just 4 VMs on 2 ESXi and 2 datastores. What complications do you see?

[Image: The diagram illustrates a many-to-many storage relationship across two ESXi hosts (ESXi 01 and ESXi 02) and two datastores (Datastore AA and Datastore BB), with four VMs (A, B, C, D) each having two VMDKs plus VM A having an RDM connected to a separate LUN. Notably, VM A's VMDKs span **both** datastores (VMDK1 → Datastore AA, VMDK2 → Datastore BB), and similarly VM B and VM C have VMDKs crossing between datastores and ESXi hosts, demonstrating cross-host, cross-datastore VMDK placement. This cross-mapping visually explains the observability complexity described in the text — datastore metrics only capture VMDKs physically residing on that datastore, making it impossible to cleanly aggregate storage capacity or performance metrics at the ESXi cluster level when datastores are shared across clusters.]

Performance and capacity become complex due to many to many relationships. The metrics at ESXi level and cluster will not match the metrics at datastore level. How do you then aggregate the cluster storage capacity when its datastores are shared with other clusters?
You’re right. You can’t.
In summary, while there are use cases where you should separate the VMDK into multiple datastores, take note of the observability compromise.

#### Backing Device

Since datastore is a filesystem, it’s necessary to monitor the backing device. This can be NFS or LUN. For NFS, it looks something like this:

[Image: The image shows the **Device Backing configuration** for an NFS datastore named **SC2-NFS-01** in vSphere, displaying two key properties: **Server: 192.168.107.201** and **Folder: /sc2-hs2-cmbu-4tb**. This screenshot demonstrates how to identify the backing NFS server and export path for a datastore within vSphere's Configure > Device Backing section. In the context of the surrounding text, this illustrates the NFS backing relationship that must be tracked externally (on the storage provider side) to correlate vSphere datastore metrics with underlying storage device metrics.]

For a local disk, it looks something like this:

[Image: ## Device Backing - Local NVMe Disk Details

The image shows the **Device Backing** panel in vSphere for a local NVMe disk (`eui.7170e9078fa5f2c7000c296de3fda11f`), a **32 GB Flash drive** with GPT partition format and 512e sector format. The partition table displays **5 partitions**: four Legacy MBR primary partitions (101 MB, 4 GB, 4 GB, 10 GB) and one **VMFS partition of 13.9 GB** (Primary), which represents the actual datastore-backing extent. This illustrates the surrounding text's point that the backing device exists outside vSphere's direct metrics scope, requiring cross-referencing storage-level metrics (e.g., LUN IOPS) against datastore-level metrics to derive meaningful performance ratios.]

Since the underlying device is outside the realm of vSphere, you need to login to the storage provider and build the relationship. Compare the metrics by deriving a ratio. Investigate if this ratio shows unexpected value.
Take for example, a datastore on a FC LUN. If you divide the IOPS at the LUN level with the IOPS at the datastore, what value do you expect?
Assuming they are mapped 1:1, then the ratio should be 1.
If the value is > 1, that means there are IO operations performed by the array. This could be array level replication or snapshot.
What about NFS datastores? The troubleshooting is different as you now need to at files as opposed to block. In both cases, you need to monitor the filer or array directly.

## VM

We covered earlier that storage differs to compute as it covers both dimensions (speed and space). As a result, we cannot simply use the contention and consumption as grouping. Instead we would group by performance and capacity. This is also good as operationally you manage performance and capacity differently.

### Overview

Recall the 3 layers of storage from VM downward. As stated, the 3 blue boxes appear in the vSphere Client UI as virtual disk, datastore and disk.

[Image: ## Image Description

The screenshot shows the **Chart Options dialog** in VMware vSphere Client for the VM "App-A-AppTier-Node-1," displaying the available **Chart Metrics categories** (CPU, Datastore, Disk, Memory, Network, Power, System, Virtual Disk) with both **Datastore and Virtual Disk highlighted**, and the right panel showing Datastore counters including **Average read/write requests per second, Read/Write latency (ms, Average rollup), and Read/Write rate (KB)**. This directly illustrates the three storage layers referenced in the text — **Datastore, Disk, and Virtual Disk** — as they appear in the vSphere UI, confirming the text's statement about these being the observable storage dimensions. The simultaneous highlighting of Virtual Disk and Datastore visually reinforces the hierarchy described, with Virtual Disk being the closest layer to the VM and offering the most granular observability.]

Among the 3, which one is the most important?
You’re right, virtual disk.
It is the closest to the VM and it is the most detail in terms of observability.

#### Virtual Disk

Use the virtual disk metrics to see VMFS vmdk files, NFS vmdk files, and RDMs.
However, you don’t get data for anything other than virtual disk. For example, if the VM has snapshot, the metric does not include the snapshot data.
A VM typically has multiple virtual disks, typically 1 Guest OS partition maps to 1 virtual disk. The following VM has 3 virtual disks.

[Image: The image shows a vSphere Client UI panel for selecting virtual disk objects to display in a performance chart, listing three SCSI virtual disks: **scsi0:0**, **scsi0:1**, and **scsi0:2**, all with unchecked checkboxes. This screenshot demonstrates the point made in the surrounding text that a VM with 3 virtual disks has no aggregate-level metric — each virtual disk must be selected and monitored individually. The absence of a combined/aggregate option at the VM level illustrates why manual addition in vCenter or use of VCF Operations' "aggregate of all instances" metric is necessary.]

As you can see in the preceding screenshot of vSphere Client UI, there is no aggregate number at VM level. You need to add them manually in vCenter. In VCF Operations, you use the “aggregate of all instances” metric to see the rest.
The following properties is available in VCF Operations for each virtual disk:

| Property Name | Values |
| --- | --- |
| Virtual Device Node | Virtual disks SCSI bus location. Virtual disks are enumerated starting with the first controller and moving along the bus. |
| Compatibility Mode | Physical Virtual Virtual mode specifies full virtualization of the mapped device. Physical mode specifies minimal SCSI virtualization of the mapped device. |
| Disk Mode | Dependent Independent – Persistent Independent – Nonpersistent |
| SCSI Bus Sharing | None Physical Virtual |
| SCSI Controller Type | BusLogic Parallel LSI Logic Parallel LSI Logic SAS VMware Paravirtual |
| Encryption Status |  |
| Is RDM | true false False means the virtual disk is a VDMK not RDM. |
| Virtual Disk Sharing | Unspecified No Sharing Multi-Writer |

The property “Number of VDMK” excludes RDM, as the name implies. The metric “Number of RDMs” only includes RDM attached to the VM.
Pro Tip: sum the property “Number of RDMs” from all the VMs in a single physical storage array. Compare the result with the number of LUNs in the array that are carved out for RDM purpose. If there are more LUNs than this number, you have unused RDM.
You need to do the above per physical array, so you know which array needs attention.

#### Disk

This should be called Physical Disk or Device, as a simple terminology “disk” sounds like a superset of virtual disk.
Disk means device, so we’re measuring at LUN level or RDM level. It’s great to know that we can associate the metrics back to the VM. Notice we can’t associate it to specific virtual disk as they are different layers.

[Image: The image shows a **vRealize Operations Manager object selection dialog** for a chart, displaying a single target object: **vRealize-Operations-Manager-Appliance-8.5.0.18255622_OV...** (truncated). This is a UI element used to select the VM or appliance against which datastore-level metrics will be visualized. In context, this represents the target object at the **datastore metric layer**, illustrating the VM-level aggregated view of storage metrics (combining all virtual disks) as described in the surrounding text about datastore metrics.]

Use the disk metrics to see VMFS and RDM, but not NFS. The data at this level should be the same as at Datastore level because your blocks should be aligned; you should have a 1:1 mapping between Datastore and LUN, without extents. It also has the Highest Latency counter, which is useful in tracking peak latency
The metric is at the disk level. So I’m not 100% sure if the value is per VM or per disk (which typically has many VM).

[Image: ## Image Description

This screenshot shows the **VMware vSphere performance chart configuration** interface for **Disk metrics**, with the counter **"Average commands issued per second"** (internal name: `commandsAverag...`, Rollup: Average, Unit: num, Stat Type: Rate) selected. The object selector (highlighted in green) shows a **Local ATA Disk (naa.55cd2e414f761964)** selected as the target object, with the timespan set to **Real-time (Last 1 Hour)**. This illustrates the disk-level metric configuration referenced in the text, demonstrating how disk counters are scoped to a specific physical LUN/disk rather than per-VM, which supports the author's uncertainty about whether values represent per-VM or per-disk granularity.]


##### Raw Device Mapping

RDM appears clearly as LUN in the VM Edit Settings dialog box:

[Image: ## Image Description

This is a VMware vSphere **Edit Settings dialog** for a VM named "WindowsRDMTest," demonstrating how an **RDM (Raw Device Mapping) disk appears in the VM configuration UI**. Hard disk 3 is configured as a **1024 GB RDM** with **Physical compatibility mode**, mapped to Physical LUN `vml.02000000000600601603640420053958261c290cf1f5652414944 20`, attached via **SCSI(0:2)** on SCSI controller 0. The image contextually illustrates that RDM disks are visible and identifiable as LUNs within the Edit Settings dialog, in contrast to how they appear when browsing the datastore folder.]

But what does it appear when you browse the VM folder in the parent datastore?
RDM appears like a regular VMDK file. There is no way to distinguish it in the folder.

[Image: ## Image Description

This screenshot shows the **vSphere datastore file browser** for "VMFS6 DS," displaying the contents of the "ForInvestigationvROPSCert" VM folder. The file listing reveals 11 items including VMDK files, VMX configuration files, NVRAM, and log files — notably highlighting **ForInvestigationvROPSCert_1.vmdk** (1,073,741,824 KB / ~1TB, outlined in red) as a Virtual Disk type.

This image demonstrates the book's point that **RDM disks appear identical to regular VMDK files** when browsing the VM folder in the datastore — there is no visual distinction in the file browser between an RDM pointer file and a standard virtual disk, as both display with the same "Virtual Disk" type classification.]


#### Datastore

Use the datastore metrics to see VMFS and NFS, but not RDM. Because snapshots happen at Datastore level, the counter will include it. Datastore figures will be higher if your VM has a snapshot. You don’t have to add the data from each virtual disk together as the data presented is already at the VM level. It also has the Highest Latency counter, which is useful in tracking peak latency.
Just like LUN level, we lose the breakdown at virtual disk. The metric is only available at VM level.

[Image: The image shows a **vRealize Operations Manager object selection dialog** for a chart, displaying a single target object: **vRealize-Operations-Manager-Appliance-8.5.0.18255622_OV...** (truncated). This is a UI element used to select the VM or appliance against which datastore-level metrics will be visualized. In context, this represents the target object at the **datastore metric layer**, illustrating the VM-level aggregated view of storage metrics (combining all virtual disks) as described in the surrounding text about datastore metrics.]


#### Mapping

If all the virtual disks of a VM are residing in the same datastore, and that datastore is backed by 1 LUN, then all the 3 layers will have fairly similar metrics. The following VM has 2 virtual disks (not shown). Notice all 3 metrics are identical over time.

[Image: ## Image Description

The chart displays **Total IOPS metrics across three layers** — Physical Disk, Datastore, and Virtual Disk — for a single VM over approximately 20 hours (Thursday Mar 31, ~11AM to Friday Apr 1, ~7AM). At the tooltip timestamp of **4:20:19 PM**, all three metrics show nearly identical values: **Physical Disk: 270.67, Datastore: 270.6, and Virtual Disk: 269.87 IOPS**. This demonstrates the "mapping" concept described in the surrounding text — when a VM's virtual disks reside in a single datastore backed by one LUN, all three storage layers report essentially the same IOPS values over time, with the cyan line representing all three traces nearly perfectly overlapping throughout the entire time series.]

The difference comes from files outside the virtual disks, such as snapshot, log files, and memory swap.

#### Multi-Writer Disk

In application such as database, multiple VMs need to share the same disk.
Shared disk can be either shared RDM or VMDK. The following screenshot shows the option when creating a multi-writer VMDK in vCenter Client.

[Image: The image shows the vCenter Client interface for configuring a new virtual hard disk (40 GB, maximum 755.91 GB), with the **Sharing** dropdown menu expanded, revealing three options: **Unspecified**, **No sharing**, and **Multi-writer**. The Multi-writer option is highlighted, demonstrating how to configure a VMDK for shared access across multiple VMs. This screenshot illustrates the disk sharing configuration step referenced in the text when creating a multi-writer VMDK for use cases such as shared database storage.]

When multiple VMs are sharing the same virtual disk or RDM, it creates additional challenge in capacity, cost and performance management. In the following example, notice the metric become flat 0. See the red arrow.

[Image: ## Image Description

The chart displays **Virtual Disk scsi0:4 Total IOPS** for VM **T00485BRND043**, spanning **September 26 – October 26**, with a recorded high of **745.13 IOPS** and a low of **0**. The metric shows significant IOPS activity (peaking around **October 4-8**), followed by a **sudden drop to flat 0** after approximately **October 9** (indicated by the red arrow). This demonstrates the Active/Passive failover scenario described in the text, where vCenter API returns **0 instead of null/blank** after the VM becomes passive, creating a misleading flat-zero metric rather than showing no data.]

The above is obviously wrong as IOPS are typically not flat 0.
What happens here is typical Active/Passive pair of VM. The application fail over to the second VM, so the first VM becomes passive. vCenter API returns 0 instead of blank, hence you see 0 in VCF Operations.
You can see from the following screenshot that the second VM took over at the time the first VM failover. Notice it started showing IOPS metrics on the same time.

[Image: ## Image Description

The chart displays **Virtual Disk:scsi1:4|Total IOPS** for VM **T00485BRND041**, showing IOPS values ranging from **L:0 to H:1,033.33** over the period **September 26 – October 26**. The metric shows **flat 0 values from approximately September 26 through October 7**, followed by **active IOPS spikes reaching ~1,000 IOPS from October 8 onward**. This demonstrates the Active/Passive failover behavior described in the text — the VM was passive (returning 0 IOPS via vCenter API rather than blank/null) before becoming active, contrasting with the second VM which returned blank data during its passive period.]

Do you notice something inconsistent?
The first VM returns 0 after failover. The second VM returns blank (no data) before taking over.

##### Metrics


| Name | Description |
| --- | --- |
| Disk Space \| Active Not Shared (GB) | The total amount of disk space from all the VMDK and RDM that are exclusively owned by this VM.  Active only cover the virtual disks. Snapshot is considered as non-active files hence it’s not counted. Formula: Disk Space\|Not Shared (GB) - Disk Space\|Snapshot Space (GB) |


### Performance Metrics

Just like CPU and memory, we would cover contention type of metric first, then the consumption type of metrics.

#### Contention Metrics

Contention could happen due to the VM itself (e.g. IOPS Limit has been placed) or the underlying infrastructure.
We will cover them from virtual disk first, then datastore and disk.

##### Virtual Disk

The main metrics for tracking performance is latency. They are provided in both ms and microsecond.

[Image: The table displays four virtual disk latency metrics used in VMware vSphere: **Read latency** and **Write latency** (averaged, measured in milliseconds), and **Read Latency (us)** and **Write Latency (us)** (latest value, measured in microseconds). Each metric includes its aggregation type, unit, and a brief description. This table contextualizes the two granularities of latency measurement available for virtual disks — average ms-level metrics for trend analysis and latest µs-level metrics for more precise, real-time contention detection.]

A related counter to latency is Outstanding IO.
This is the number of I/Os that have been issued, but not yet completed. They are waiting in the queue, indicating a bottleneck

[Image: The image displays a metrics table showing two counters: **"Average number of outstanding read requests"** and **"Average number of outstanding write requests"**, both with aggregation type **"Latest"** and unit **"num"** (numeric). These metrics track the queue depth for virtual disk I/O operations — specifically the count of issued but not yet completed read and write requests. In the context of the surrounding text, this table introduces the Outstanding IO counters that complement latency metrics, where a high queue depth alongside high latency indicates a storage bottleneck.]

The relationship is
Average Latency = Average Outstanding IO / Average IOPS
Outstanding IO should be seen in conjunction with latency. It can be acceptable to have high number of IO in the queue, so long the actual latency is low.
Since your goal is maximum IOPS and minimum latency, the metric is less useful as its value is impacted by IOPS. See this KB article for VSAN specific recommendation on the expected value.
What should be the threshold value?
That depends on your storage, because the range varies widely. Use the profiling technique to establish the threshold that is suitable for your environment.
In the following analysis, we take more than 63 million data points (2400 VM x 3 months worth of data). Using data like this, discuss with the storage vendor if that’s in line with what they sold you.

[Image: ## Image Description

The pie chart displays the distribution of **VM Outstanding I/O (OIOs)** across **2,407 VMs**, using the peak value recorded over a 3-month period. The dominant segment shows **89.32% (2,150 VMs)** have 0–10 OIOs, while the remaining ~10.68% are distributed across higher ranges: 10–20 (3.28%), 20–30 (1.16%), 30–100 (3.12%), and 100–1,000 (3.12%) OIOs. This demonstrates that the vast majority of VMs operate with very low outstanding I/O, supporting the surrounding text's guidance on using empirical profiling data to establish environment-specific OIO thresholds.]


##### Disk

As the physical disk layer, there are 2 error metrics. I always find their values to be 0 all the time, so if you’ve seen a non-zero value let me know.

[Image: The image displays a table showing two SCSI-level error metrics for the **Disk layer**: **Bus resets** and **Commands aborted**, both using a **Summation** rollup type measured in numeric units (num). These metrics track SCSI-bus reset commands and aborted SCSI commands respectively, both collected per interval. This supports the surrounding text's assertion that these error metrics consistently show zero values, serving as fault indicators rather than performance baselines.]

For latency, there is no breakdown. It’s also the highest among all disks. Take note the roll-up is latest, so it’s the single value at the end of the collection period.

[Image: The image shows a single metric row for **"Highest latency"** at the physical disk layer, with a **Latest** roll-up, measured in **milliseconds (ms)**, described as the "Highest latency value across all disks used by the host." This metric represents the peak latency across all disks without any read/write breakdown, and uses a Latest (not average) roll-up, meaning it captures only the single value at the end of the collection period. This is highlighted in the surrounding text to caution that the Latest roll-up may not reflect sustained latency trends.]


##### Datastore

At the datastore layer, the only metric provided for contention is latency. There is no outstanding IO.

[Image: The image shows a table of **datastore latency metrics** in VMware vSphere/VCF Operations, listing three counters: **Highest latency** (Latest rollup), **Read latency** (Average rollup), and **Write latency** (Average rollup), all measured in milliseconds with Absolute stat type. This illustrates the limited contention metrics available at the datastore layer — only latency, with no outstanding I/O metrics. The Highest latency counter maps to the highest value across all datastores used by a host, while Read and Write latency map directly to `datastore.totalReadLatency.average` and `datastore.totalWriteLatency.average` respectively.]

The highest latency is useful for VMs with multiple datastores. But take note the roll-up is Latest, not average.
For the read and write latency, the value in VCF Operations is a raw mapping to these values datastore.totalReadLatency.average and datastore.totalWriteLatency.average

#### Consumption metrics

A typical suspect for high latency is high utilization, so let’s check what IOPS and throughput metrics are available.

##### Virtual Disk

As you can expect, you’re given both IOPS and throughput metrics at virtual disk level.

[Image: The image shows a table of **virtual disk performance counters** in VMware vSphere/VCF Operations, listing four metrics: **Average read/write requests per second** (IOPS, in num units) and **Read/Write rate** (throughput, in KBps), all using **Average rollup**. This table demonstrates the available IOPS and throughput metrics at the virtual disk level, supporting the surrounding text's discussion of consumption metrics used to diagnose high latency through utilization analysis.]

VM Disk IOPS and throughput vary widely among workload. For a single workload or VM, it also depends on whether you measure during its busy time or quiet time.
Take note that vSphere Client does not provide summary at VM level. Notice the target objects are individual scsiM:N, and there is no aggregation at VM level as the option in Target Objects column below.

[Image: The image shows a **vSphere Client object selection interface** for configuring a performance chart, displaying a list of target objects representing individual virtual disk identifiers in **scsiM:N format** (scsi0:0, scsi0:1, scsi0:2). Each object has an individual checkbox with no aggregate/summary option available at the VM level. This screenshot directly illustrates the text's point that vSphere Client only allows selection of **individual virtual disk objects** (scsiM:N), lacking any VM-level aggregation option in the Target Objects column.]

In the following example, I plotted from a 3500 production VMs. They are sorted by the largest IOPS on any given 5 minute. What’s your take?

[Image: ## Image Description

This table displays **storage performance metrics for the top 9 highest-IOPS VMs** (out of 3,500 production VMs), sorted descending by **Bursty IOPS (5-minute peak)**, ranging from **83,252 IOPS (CO...)** down to **41,501 IOPS (cp-...)**. Columns include Sustained IOPS (1-hour), Throughput at both 1-hour and 5-minute intervals, vCPU count, and vDisk count, with color coding indicating severity (red = critical, orange = warning, green = normal). The data demonstrates extreme storage demand at the VM level — for example, **ora...** shows 22.93 Gbps sustained throughput with 26 vDisks, and **cus...** peaks at 32.48 Gbps over 5 minutes — directly supporting the author's point that even a small number of VMs can generate millions of I/O commands and saturate network links.]

I think those numbers are high. At 1000 IOPS averaged over 5 minutes, that means 300,000 total IO commands that need to be processed. So 10K IOPS translates into 3 millions commands, which must be completed within 300 seconds.
A high IOPS can also impact the pipe bandwidth, as it’s shared by many VMs and the kernel. If a single VM chews up 1 Gb/s, you just need a handful of them to saturate 10 Gb ethernet link.
There is another problem, which is sustained load. The longer the time, the higher the chance that other VMs are affected.
In the following example, it’s a burst IOPS. Regardless, discuss with the application team if it is higher than expected. What’s normal from one application may not be for another.

[Image: ## Image Description

The chart displays **VM disk IOPS over a ~36-hour period** (Jul 5–Jul 6), with values ranging from near 0 to approximately **80K IOPS** on the Y-axis, showing two series (purple and pink/rose) that track closely together. Several sharp, narrow **burst spikes** are visible — notably peaks reaching ~70K IOPS around 4:00 PM Jul 5 and ~80K IOPS shortly after midnight Jul 6, with smaller spikes (~55K) around 11:00 PM Jul 5. This demonstrates the **burst IOPS pattern** referenced in the surrounding text, where short-duration, high-magnitude spikes occur rather than sustained elevated load, illustrating the type of activity that warrants discussion with application teams to determine if it exceeds expected thresholds.]

While there is no such thing as normal distribution or range, you can analyse your environment so you get a sense. I plotted all the 3500 VMs and almost 85% did not exceed 1000 IOPS in the last 1 week. The ones hitting >5K IOPS only form around 3%.

[Image: ## Pie Chart: VM IOPS Distribution Across 3,500 VMs

The pie chart shows the distribution of IOPS across ~3,500 VMs, segmented into five ranges: **0–100 (49.45%)**, **100–500 (21.18%)**, **500–1,000 (13.16%)**, **1,000–5,000 (12.89%)**, and **5,000–99,999 (3.33%)**. This confirms the author's statement that **~84% of VMs do not exceed 1,000 IOPS** (49.45% + 21.18% + 13.16%), while only **3.33% exceed 5,000 IOPS**. The chart serves as a baseline reference for understanding typical IOPS distribution in a vSphere environment over a one-week observation period.]

If the IOPS is low, but the throughput is high, then the block size is large. Compare this with your expected block size, as they should not deviate greatly from plan. You do have a plan, don’t you 😉

[Image: The image shows a table listing two storage metrics: **Read request size** and **Write request size**, both using the "Latest" rollup type with a numeric ("num") data type. These metrics measure the **average read and write request sizes in bytes**, effectively representing the I/O block size for VM storage operations. In context, this table supports the surrounding discussion about correlating IOPS with throughput to derive block size, helping administrators validate whether actual I/O patterns align with planned workload specifications.]

You can set the limit for individual virtual disk of VM.

[Image: This screenshot shows the **Virtual Hardware configuration panel** in VMware vSphere for a VM, displaying settings for **CPU (2 vCPUs)**, **Memory (4 GB)**, and **Hard Disk 1 (75 GB)** with a maximum possible size of **2.52 TB**. In context, the image illustrates where an administrator can configure virtual disk size limits for individual VM disks. The "Hard Disk 1" row is expanded/highlighted, showing this is the location where disk I/O limits (referenced in the surrounding text) can be set per virtual disk.]

A few rows below, and you will see the following.

[Image: The image shows a VMware vSphere virtual disk configuration setting for **"Limit - IOPs"**, with the value set to a **custom limit of 1,000 IOPS**. This screenshot demonstrates how an IOPS limit can be applied to an individual virtual disk within a VM's settings. In context, this illustrates the configuration capability mentioned in the surrounding text, where the default (recommended) setting is no limit, but a custom value of 1,000 IOPs can be manually specified.]

The default setting is no limit, which is what I recommend.
Note that the limit on a virtual disk, not the whole VM. That means you cannot set limit on non virtual disk such as snapshot and memory swap. This makes sense as they are part of IaaS.
Take note that since the limit is applied at VM level, the metrics that will show high latency is at Guest OS levels. The VM metric will not show high latency, as the IO that were allowed to pass was not affected by this limit. This is no different to any problem at Guest OS layer. For example, if LSI Logic or PVSCSI driver is causing problem, the VM will not report anything as it’s below the Guest OS driver.
VCF Operations have the following related data at each virtual disk
- IOPS Limit property.
- IOPS per GB metric.

##### Disk

There are 2 sets of metrics for IOPS. Both are basically the same. One if the total number of IO in the collection period, while the other one is average of 1 second.

[Image: ## Image Description

This table displays **VMware vSphere disk/SCSI performance counters** organized into two sets of metrics as described in the surrounding text: **Average-rollup counters** (Average commands issued per second, Average read requests per second, Average write requests per second) and **Summation-rollup counters** (Commands issued, Read requests, Write requests). All metrics use numeric units and cover SCSI commands, disk reads, and disk writes during the collection interval. This directly illustrates the text's point that "there are 2 sets of metrics for IOPS" — one representing total IO count over the collection period (Summation) and the other representing a per-second average (Average).]

There are the usual metrics for throughput.

[Image: The image displays a table of three disk throughput metrics: **Read Rate**, **Usage**, and **Write Rate**, all measured as **Average** values in **KBps**. Read Rate and Write Rate represent the average kilobytes read from or written to disk per second during the collection interval, while Usage represents the aggregated disk I/O rate (including all VMs on a host). In context, this table documents the standard throughput metrics available for virtual disk monitoring in VCF Operations, complementing the previously mentioned IOPS metrics.]

It will be great to have block size, especially the maximum one during the collection period.

##### Datastore

For utilization, both IOPS and throughput are provided.

[Image: The image shows a table of **datastore throughput metrics** in VMware vSphere, listing four counters: **Average read requests per second**, **Average write requests per second** (both in `num` units, Rate/Average rollup), and **Read rate** and **Write rate** (both in `KBps`, Rate/Average rollup). This table demonstrates the available throughput-related metrics for datastores, complementing the IOPS metrics discussed in the preceding text. The metrics measure the rate of read/write commands and data transfer to/from the datastore during collection intervals.]

For the IOPS, the value in VCF Operations is a raw mapping to these values datastore.numberReadAveraged.average and datastore.numberWriteAveraged.average in vCenter.
Review the following screenshot. Notice something strange among the 3 metrics?

[Image: ## Image Description

The chart displays Total IOPS metrics over approximately 7 days (Mar 29–Apr 6) for **ora-prod-ebs-r3** across three layers: **Physical Disk** (purple), **Virtual Disk** (teal/cyan), and **Datastore** (pink). At the highlighted point (Friday, Apr 1, 3:00–3:14 PM), Physical Disk and Virtual Disk IOPS are nearly identical at **~26,311** and **~26,309** respectively, while Datastore IOPS is drastically lower at only **26.53**. The teal Virtual Disk line dominates the chart with sustained activity ranging 5K–25K IOPS, while the pink Datastore line remains near zero with only brief daily spikes to ~5K, visually demonstrating the anomaly explained in the surrounding text — that the majority of the VM's 26 virtual disks are **RDM (Raw Device Mappings)**, which bypass the datastore layer entirely.]

Yes, the total IOPS at datastore level is much lower than the IOPS at physical disk and virtual disk levels. The IOPS at physical disk and virtual disk are identical over the last 7 days. They are quite active.
The IOPS at datastore level is much lower, and only spike once a day. This VM is an Oracle EBS VM with 26 virtual disks. Majority of its disks are RDM, hence the IOPS hitting the datastore is much less.
Snapshot requires additional read operations, as the reads have to be performed on all the snapshots. The impact on write is less. I’m not sure why it goes up so high, but logically it should be because many files are involved. Based on the manual, a snapshot operation creates .vmdk, -delta.vmdk, .vmsd, and .vmsn files. Read more here.
For Write, ESXi just need to write into the newest file.

[Image: This table displays VM-level disk I/O metrics including vDisk Reads/sec, Datastore Reads/sec, vDisk Writes/sec, Datastore Writes/sec, Snapshot Size, and Snapshot Age for 10 VMs. Three VMs (VA...) show significantly elevated Datastore Reads/sec (720.67, 1,064.13, and 472.93 — flagged with red alerts) compared to their vDisk Reads/sec, demonstrating the read amplification effect caused by snapshots. These same VMs have non-zero snapshot sizes (30.45 GB, 58.9 GB, and 53.07 GB) and snapshot ages of 38–47 days, with their Datastore Writes/sec highlighted in green (171.13, 60.33, 39.27), confirming the text's assertion that snapshots disproportionately impact read operations versus writes.]

The pattern is actually identical. I take one of the VM and show it over 7 days. Notice how similar the 2 trend charts in terms of pattern.

[Image: ## Image Description

The image displays two time-series charts spanning **May 11–18**, comparing **Datastore Read IOPS** (top, peak H: 2,947.73, low L: 25.07) versus **Virtual Disk Aggregate Read IOPS** (bottom, peak H: 370.33, low L: 5.27) for the same VM. The key observation is that both charts exhibit **nearly identical patterns** — the spikes, valleys, and periodicity align closely across the 7-day window, with the datastore-level IOPS consistently **~8x higher** than the virtual disk-level IOPS. This demonstrates that VMware snapshot overhead causes artificially inflated Read IOPS at the datastore layer (due to reads spanning multiple snapshot delta files), while the virtual disk metric reflects only the guest-level I/O demand.]

You can validate if snapshot causes the problem by comparing before and after snapshot. That’s exactly what I did below. Notice initially there was no snapshot. There was a snapshot briefly and you could see the effect immediately. When the snapshot was removed, the 2 lines overlaps 100% hence you only see 1 line. When we took the snapshot again, the read IOPS at datastore level is consistently higher.

[Image: ## Image Description

The image displays two overlaid charts: the top chart compares **Datastore Read IOPS** vs. **Virtual Disk Aggregate Read IOPS** for a VM over ~Nov 6 – Jan 3, while the bottom chart shows **Snapshot Space (GB)** over the same period, peaking at **H: 114.23 GB**.

The data demonstrates a clear correlation between snapshot presence and elevated datastore-level Read IOPS: when no snapshot exists (roughly Nov 10 – Dec 12), both IOPS lines are **identical and overlap completely**; when a snapshot is active (Nov 6–10 and Dec 12 onward, ~100 GB), the **Datastore Read IOPS is consistently higher** than the Virtual Disk IOPS, indicating snapshot-induced read overhead.

The red vertical line at ~Dec 12 marks the reintroduction of the snapshot, after which the divergence between the two IOPS metrics becomes persistent and visible, validating that snapshots cause additional read I/O at the datastore layer without returning additional data.]

How I know that’s IOPS effect as the throughput is identical. The additional reads do not bring back any data. Using the same VM but at different time period, notice the throughput at both levels are identical.

[Image: The chart displays **Virtual Disk Read Throughput (KBps)** and **Datastore Read Throughput (KBps)** over a ~12-hour period (May 18 4:45 PM – May 19 4:15 AM), with a notable spike peak of **~18,709 KBps (Datastore) and ~18,600 KBps (Virtual Disk)** at 07:05 PM. The two lines are nearly **identical and overlapping throughout the entire time period**, demonstrating that read throughput at both the VM virtual disk level and datastore level is the same. This supports the surrounding text's argument that any snapshot overhead is **not reflected in throughput** (no additional data is being returned), setting up the contrast with the accompanying IOPS chart where datastore IOPS will be shown to be consistently higher.]

And here is the IOPS on the same time period. Notice the value at datastore layer is consistently higher.

[Image: The chart displays **Datastore Read IOPS** (dark blue) versus **Virtual Disk Aggregate Read IOPS** (cyan/teal) over a ~12-hour period from May 18 ~4:45 PM to May 19 ~4:15 AM. At the highlighted spike (Tuesday, May 18, 07:05:04 PM), Datastore Read IOPS reached **4,777.2** while Virtual Disk Read IOPS was **2,201.67** — roughly 2x higher at the datastore layer. This demonstrates the IOPS overhead introduced by VMware snapshots: the datastore layer consistently reports higher read IOPS than the VM-level virtual disk metrics, while throughput remains identical, confirming the extra IOPS are snapshot-related redirect reads that return no additional data.]

For further reading, Sreekanth Setty has shared best practice here.
In addition of latency and IOPS, snapshot can also consume more than the actual space consumed by the virtual disk, especially if you are using thin and you take snapshot early while the disk is basically empty. The following VM has 3 virtual disks, where the snapshot file _1-00001.vmdk is much larger than the corresponding vmdk.

[Image: The image shows a VMware datastore file listing for a VM named "kmargaryan-dual-stack-D" with three virtual disks and their associated snapshot files. Notably, the snapshot file `kmargaryan-dual-stack-D_1-000001.vmdk` is **77,038,592 KB (~73 GB)**, significantly larger than its base disk `kmargaryan-dual-stack-D_1.vmdk` at **9,224,192 KB (~8.8 GB)**, demonstrating how snapshot files can exceed the size of the original virtual disk. This illustrates the text's point that snapshots on thin-provisioned disks can consume disproportionately more space than the actual virtual disk, particularly when snapshots are taken early in the disk's lifecycle.]


##### Storage DRS

Lastly, there are storage DRS metric and seek size.

[Image: This table displays five Storage DRS virtual disk metrics from VMware vSphere: **Number of large seeks** (>8192 LBNs apart), **Number of medium seeks** (64–8192 LBNs apart), **Number of small seeks** (<64 LBNs apart), **Read workload metric**, and **Write workload metric**. All metrics are categorized as "Latest" rollup type with numeric ("num") units. In the context of the surrounding text, this table documents seek size metrics used by Storage DRS to characterize disk access patterns and workload distribution across virtual disks.]


### Capacity Metrics

Disk space metrics are complex due the different types of consumption in a single Virtual Disk.
- Actual used by Guest OS
- Unmapped block
- vSAN protection (FTT)
- vSAN savings (dedupe and compressed).
Let’s break it down, starting with understanding the files that make up a VM.

#### VM Files

At the end of the day, all those disk space appear as files in the VMFS filesystem, including the RDM pointer files. You can see them when you browse the datastore. The following is a typical example of what vSphere Client will show.

[Image: The image shows a VMware datastore file browser listing the constituent files of a Bitnami Pimcore VM, displaying file names, sizes, and types. The largest file is the **virtual disk** (`bitnami-pimcore-h1.vmdk`) at **13,520,896 KB (~12.9 GB)**, followed by a swap file (`vmx-bitnami-pimcore-h1-...vswp`) at **81,920 KB (80 MB)** and multiple VM log files ranging from **147 KB to 4,505 KB**. This illustrates the context described in the surrounding text — that VM storage consumption manifests as multiple file types on VMFS, with the `.vmdk` (Virtual Disk) dominating storage usage while supporting files like `.vmx`, `.nvram`, `.vmsd`, and log files constitute a small fraction of total consumption.]

Yes, a lot of files 😊
We can categorize them into 4 from operations viewpoint:

| Disk | Virtual disk or RDM. This is typically the largest component. This can be thin provisioned, in which case the provisioned size tends to be larger than the actual consumption as Guest filesystem typically does not fill 100%. All virtual disks are made up of two files, a large data file equal to the size of the virtual disk and a small text disk descriptor file which describes the size and geometry of the virtual disk file. The descriptor file also contains a pointer to the large data file as well as information on the virtual disks drive sectors, heads, cylinders and disk adapter type. In most cases these files will have the same name as the data file that it is associated with (i.e. MyVM1.vmdk and MyVM1-flat.vmdk). A VM can have up to 64 disks from multiple datastores. |
| --- | --- |
| Snapshot | Snapshot protects 3 things:  VMDK Memory Configuration For VMDK, the snapshot filename uses the syntax MyVM-000001.vmdk where MyVM is the name of the VM and the six-digit number 000001 is just a sequential number. There is 1 file for each VMDK. Snapshot does not apply to RDM. You do that at storage subsystem instead, transparent to ESXi. If you take snapshot with memory, it creates a .vmem file to store the actual image. The .vmsn file stores the configuration of the VM. The .vmsd file is a small file, less than 1 KB. It stores metadata about each snapshot that is active on a VM. This text file is initially 0 bytes in size until a snapshot is created and is updated with information every time snapshots are created or deleted. Only 1 file exists regardless of the number of snapshots running as they all update this single file. This is why your IO goes up. |
| Swap | The memory swap file (.vswp). A VM with 64 GB of RAM will generate a 64 GB swap file (minus the size of memory reservation) which will be used when ESXi needs to swap the VM memory into disk. The file gets deleted when the VM is powered off. You can choose to store this locally on the ESXi Host. That would save space on vSAN. The catch is vMotion as the swap file must be transferred too.  There is also a smaller file (in MB) storing the VMX process swap file. But I’m unsure about this and have not seen it yet. |
| Others | All other files. They are mostly small, in KB or MB. So if this counter is large, you’ve got unneeded files inside the VM directory.  Logs files, configuration files, and BIOS/EFI configuration file (.nvram) Note that this includes any other files you put in the VM directory. So if you put a huge ISO image or any file, it gets counted. |


#### Single VMDK

Let’s review with a single virtual VMDK disk. In the following diagram, vDisk 2 is a thin provisioned VMDK file. It still has uncommitted space as it’s not yet fully used up.

[Image: ## Image Description

The diagram illustrates the storage space breakdown for **vDisk 2 (VMDK thin provisioned)**, showing two key metrics: **Disk Space | Virtual Disk Used** (the blue region, covering "Used + Unmapped" space) and **Virtual Disk | Configured Size** (the full width including uncommitted space). The diagram demonstrates that on vSAN, only the committed portion (Used + Unmapped) is physically stored and protected by vSAN's FTT policy (shown in purple), while the **uncommitted space** (green hatched region) has no vSAN footprint. This highlights a critical metric gap: both storage metrics are **vSAN-unaware**, meaning they don't account for vSAN's replication overhead, and unmapped space within the VMDK still consumes protected vSAN capacity unnecessarily.]

Because vSAN is a software-defined storage, the storage-layer gets mixed up. What operational complexity do you spot from the above diagrams?
- Your unmapped file is also protected by vSAN.
- The uncommitted part does not include vSAN, as it’s yet written.
- You can see that the 2 metrics are not aware of vSAN. vSAN protection (Failure To Tolerate) is shown in purple.
There are 2 metric, shown in Times New Roman font:

| Metric | Description |
| --- | --- |
| Disk Space \| Virtual Disk Used (GB) | The actual consumed size of the VMDK files. It excludes other files such as snapshot files. Note: For RDM the used space is the configured size of the RDM, unless the LUN is thin provisioned by the physical storage array. So its disk space consumption at VM level works like a thick provisioned disk.  If this is higher than Guest OS used, and you’re using thin provisioned, then run unmap to trim the unmapped blocks. |
| Virtual Disk \| Configured Size | This metric does not include the vSAN part as it’s taken from consumer layer. |


#### All VM Files

Let’s take an example of a VM with 3 virtual disks, so we can cover all the combinations.
- Thin provisioned
- Thick provisioned
- RDM. Physical or virtual is not relevant.

[Image: ## Image Description

This diagram illustrates how VMware vSphere disk space metrics map to physical storage consumption for a VM with three virtual disk types: **vDisk 1 (RDM)**, **vDisk 2 (VMDK thin)**, and **vDisk 3 (thick provisioned)**. It visually defines the scope of key metrics including **"Disk Space | Provisioned Space for VM"** (total span), **"Disk Space | Virtual Disk Used"** (covering all three vDisks), **"Disk Space | Snapshot | Virtual Machine Used"** (snapshots segment), and **"Disk Space | Virtual Machine Used"** (all files on datastore including swap, logs, config). The diagram also highlights that RDM resides **on LUN** (external storage) while all VMDK and VM files reside **on vSAN**, and specifically calls out the **uncommitted/unmapped space** of the thin VMDK (vDisk 2) as the delta between configured and actually used space.]

The boxes with blue line show the actual consumption at VM layer. Let’s go through each rectangle.

| RDM | It’s not on vSAN as RDM can’t be on a VMFS datastore. It’s mapped to a LUN backed by an external storage. It’s always thick provisioned, regardless of what Windows or Linux uses. The LUN itself could be thin provisioned but that’s another issue and transparent to ESXi (hence VM). |
| --- | --- |
| Thin VMDK | We blended vSAN protection into a single box as you can't see the breakdown. It's inside the same file (so there is only 1 file but inside there is actual data + vSAN protection - vSAN dedupe - vSAN compressed).  Thin Provisioned can accumulate unmapped block over time. You should reclaim them by running a trim operation. Uncommitted space is the remaining amount that the VMDK can grow into. Since it’s not yet written, it does not have vSAN overhead yet. |
| Thick VMDK | The Used size equals the configured size as it’s fully provisioned regardless of usage by Guest OS. I’m not sure the final outcome of dedupe and compression. If the Guest OS has not written to it, then I expect the saving will be near 100% in both lazy zero and eager zero. |

vSAN protection applies to every file in the datastore. Yes, even your snapshot and log files are protected by default.
All the metrics are under Disk Space metric group. The key ones are:

| Metric | Description |
| --- | --- |
| Disk Space \| Provisioned Space for VM | Just like the Disk Space \| Virtual Machine Used (GB), but thin provisioned is based on configured not actual usage. So this metric will have higher value if the thin provisioned is not fully used. This metric is useful at the datastore level. When you overcommit the space and want to know what the total space would be when all the VMs grow to the full size.  This metric is not useful for capacity as it mixes both allocation and utilization. BTW, there can be case where the number here is reported as much higher number. See KB 83990. This is fixed in 7.0.2 P03 or 7.0 U2c, specifically in PR 2725886. |
| Disk Space \| Virtual Machine Used (GB) | Just like above, but includes files other than virtual disks. So this metric is always larger. The actual consumed size of the VM files + the configured size of the RDM files. It includes all files in the VM folder in the datastore(s). Formula: Sum ( [layoutEx.file] uniqueSize != null ? uniqueSize : size) / (1024 * 1024 * 1024) |
| Disk Space \| <Datastore Name> \| Virtual Machine Used (GB) | Just like above, but only includes files in that specific datastore only. For VM that only resides in 1 datastore, the value will be identical to above. |


##### Snapshot


| Disk Space \| Snapshot \| Virtual Machine Used (GB) | Disk Space used by all files created by snapshot (vmdk and non vmdk). This is the total space that can be reclaimed if the snapshot is removed. Use this to quickly determine which VMs have large snapshot. Formula: Sum of all files size / (1024 * 1024 * 1024)  where aggregation is only done for snapshot files. A file is a snapshot file if its layoutEx file type equals to snapshotData, or snapshotList or snapshotMemory |
| --- | --- |
| Disk Space \| Snapshot \| Access Time (ms) | The date and timestamp the snapshot was taken. Note you need to format this. |


##### vSphere Client UI

I’m adding this just in case you got curious 😊
Let’s start with the basic and progress quickly. In the following example, I would create a small VM from scratch, with 2 VMDK disk.

[Image: ## Image Description

This screenshot shows the hardware configuration panel for a VM in vSphere Client, specifically displaying the expanded settings for **Hard disk 2** (20 GB). Key details visible include: VM storage policy set to **Thick Eager Zero**, Maximum Size of **717.61 GB**, Type defined by the VM storage policy, No sharing, and the disk file located on **[vsanDatastore]** with path `1ec8d463-0c1d-b25b-3f4d-246e9662b3c4/vSAN Test_1.vmdk`. This image demonstrates the provisioning configuration of a second VMDK being added to the test VM, contrasting with Hard disk 1 (10 GB) above it, as part of a walkthrough illustrating how disk metrics appear in vSphere for differently provisioned disks.]

Hard disk 1 is 10 GB. Thin Provisioned. On vSAN.
The VM is powered off. All other settings follow default setting.
I created the VM with just the first disk, to validate the metrics value that will be shown upon creation. What do you expect to see on the vCenter UI?
Here is what I got on vSphere 7.

[Image: ## Image Description

The image shows a vSphere 7 vCenter dashboard for a **powered-off VM** with two panels: **Capacity and Usage** (left) and **VM Hardware** (right). The Capacity and Usage panel displays CPU at **0 MHz used / 1 CPU allocated**, Memory at **0 MB used / 512 MB allocated**, and Storage at **1.9 KB used / 12.22 GB allocated**. The VM Hardware panel confirms the configuration: 1 CPU, 1 GB RAM, a **10 GB Thin Provisioned hard disk on vsanDatastore**, and ESXi 7.0 U1 compatibility (VM version 18), with the network adapter disconnected.

This screenshot demonstrates the discrepancy between **"used" (1.9 KB)** and **"allocated" (12.22 GB)** storage metrics for a thin-provisioned, powered-off VM on vSAN — illustrating that allocated storage reflects the configured disk size (10 GB) plus vSAN overhead (~2.22 GB), while actual consumed space is near zero.]

You get 2 numbers, used and allocated, as shown in the Capacity and Usage section.
Used is only 1.9 KB. This is expected as it’s thin provision and the VM is powered off. This is very low, so let’s check the next number….
Allocated is 12.22 GB. This is 10 GB configured + 2.22 GB used. The hard disk 1 size shows 10 GB not 20 GB. This is what is being configured, and what Guest OS see. It is not impacted by vSAN as it’s not utilization.
So you have 2 different numbers for the use portion: 1.9 KB and 2.22 GB.
Why 2 different values?
Let’s see what the files are. We can do this by browsing the datastore and find the VM folder.

[Image: The image shows a VMware vSAN datastore file browser displaying the contents of a VM folder named "vSAN Test," containing five items: a `.sdd.sf` folder, a `.hlog` file (0.29 KB), a `.vmdk` virtual disk (36,864 KB ≈ 36 MB), a `.vmsd` file (0 KB), and a `.vmx` configuration file (2.16 KB), all timestamped 01/28/2023. This supports the surrounding text's explanation that the total file sizes sum to approximately 36 MB, which accounts for neither the 1.9 KB "Used" metric nor the 2.22 GB "Allocated" value shown in vSphere's VM storage metrics. The discrepancy demonstrates that vSphere's storage reporting metrics do not directly correspond to the raw file sizes visible in the datastore browser.]

The total from the files above is 36 MB. This does not explain 1.9 KB nor 2.22 GB.
Let’s continue the validation. This time I added Hard disk 2 and configure it with 20 GB. Unlike the first disk, this is Thick Provisioned so we can see the impact. It is also on vSAN.

[Image: ## Image Description

This VMware vSphere screenshot shows a VM's **Capacity and Usage** panel alongside **VM Hardware** details after adding a second 20 GB thick-provisioned disk on vSAN. Key metrics show **Storage: 760 MB used** (up from 1.9 KB) with **32.93 GB allocated**, while VM Hardware confirms **Hard disk 1 (of 2)** at 10 GB Thin Provision on vsanDatastore, with 1 CPU and 1 GB Memory (512 MB allocated, 0 active). The highlighted values (760 MB used, 0 GB memory active, "1 of 2" disks) demonstrate how thick provisioning on vSAN causes the used storage metric to jump significantly — the 760 MB representing 380 MB vSphere + 380 MB vSAN protection (2x mirror with no dedupe/compression).]

Used has gone up from 1.9 KB to 760 MB. As this is on vSAN, it consists of 380 MB of vSphere + 380 MB of vSAN protection. The vSAN has no dedupe nor compression, so it’s a simple 2x.
Allocated is 32.93 GB as it consists of 30 GB configured and 2.93 GB. This 2.93 is half vSphere overhead + vSAN protection on the overhead.
Looking at the datastore level, the second hard disk is showing 40.86 GB. It maps to hard disk 2.

[Image: The image shows a vSAN datastore file browser displaying the contents of a VM directory named "vSAN Test," listing six objects including a folder (.sdd.sf), an hlog file (0.29 KB), two VMDK virtual disks (36,864 KB and 42,815,488 KB), a vmsd file (0 KB), and a vmx configuration file (2.16 KB), all timestamped 01/28/2023. The notably large **vSAN Test_1.vmdk** at **42,815,488 KB (~40.86 GB)** corresponds to the second hard disk referenced in the surrounding text, confirming the datastore-level allocated size mapping. This screenshot demonstrates how vSAN stores VM files and illustrates the relationship between the configured disk size and the actual datastore footprint discussed in the context of vCenter's Allocated vs. Used metrics.]

From this simple example, you can see that Allocated in vCenter UI actually contains used and allocated. By allocated it means the future potential used, which is up to the hard disk configured size. The used portion contains vSAN consumption if it’s on vSAN, while the unused portion does not (obviously since vSAN has not written any block).

## ESXi

The following screenshot shows the ESXi metric groups for storage in the vCenter performance chart.

[Image: The image shows the **vCenter Performance Chart Options** interface for an ESXi host (`sc2-hs2-b1619.eng.vmware.com`), with the **Datastore** metric group selected from the Chart Metrics panel. The available datastore counters include: **Average read/write requests per second** (Average rollup, num), **Datastore latency observed by VMs** (Latest, µs), **Highest latency** (Latest, ms), **Read latency** (Average, ms), **Read rate** (Average, KBps), and **Storage DRS datastore bytes read** (Latest, num). This screenshot contextually demonstrates the ESXi storage metric groups available in vCenter, specifically illustrating the Datastore counter options referenced in the surrounding text's discussion of the four storage metric groups (Datastore, Disk, Storage adapter, Storage path).]

As expected, there are 4 metrics groups for storage
- Datastore
- Disk
- Storage adapter
- Storage path.
We’ve covered earlier how they work together. We also covered how vSAN impacts them.

### Disk or Device

There are 3 layers from VM to physical LUN
- VM.
- The kernel. This is measured by the KAVG counter and QAVG counter.
- Device.
Compared with Adapter or Path, you get a lot more metrics for disk or device as there is capacity metric.
As expected, there is no breakdown as the kernel cannot actually see anything in between the HBA and the device. So no metrics such as number of hops as it’s not even aware of the fabric topology.

#### Contention Metrics

Frank Denneman, whose blog and book are great references, shows the relationship among the counters using the following diagram:

[Image: ## Image Description

The diagram illustrates the **I/O latency measurement points** in the VMware vSphere storage stack, showing three Average (AVG) latency counters: **Guest AVG (GAVG)**, **Kernel AVG (KAVG)**, and **Device AVG (DAVG)**. The vertical stack displays the I/O path components from Application Guest OS down through VMM, vSCSI, ESX Storage Stack, Driver, HBA, Fabric, Array Storage Processor, to Device, with dashed brackets indicating where each latency counter is measured. This contextualizes the relationship between GAVG, KAVG, and DAVG — specifically that KAVG spans from the Driver layer up through the ESX storage stack (the kernel-controlled portion), while DAVG covers the hardware path from Driver down to the physical Device.]

For further reading, review this explanation by Frank, as that’s where I got the preceding diagram from.

| Guest Average | GAVG | Guest here means VM, not Guest OS as the counter starts from VMM layer not Windows or Linux. |
| --- | --- | --- |
| Kernel Average | KAVG | ESXi is good in optimizing the IO, so in a healthy environment, the value should be within 0.5 ms.  This is computed from Guest AVG and Device AVG, which are raw counters. |
| Kernel Average | QAVG | QAVG, which is queue in the kernel, is part of KAVG. If QAVG is high, check the queue depths at each level of the storage stack. Cody explains why QAVG can be higher than KAVG here. In short, QAVG measures both VM IO and the kernel IO, while KAVG only includes VM IO. |
| Device Average | DAVG | The average time from ESXi physical card to the array and back. Typically, there is a storage fabric in the middle. The array typically starts with its frontend ports, then CPU, then cache, backend ports, and physical spindles. So if DAVG is high, it could be the fabric or the array. If the array is reporting low value, then it’s the fabric of the HBA configuration. I’m unsure what DAVG measures when it’s vSAN and the data happens to be local. |

For each of the above 4 sets, you expect read latency, write latency and the combined latency. That means 12 counters and here are what they are called in vSphere Client UI:

| Device |  |
| --- | --- |
| Kernel |  |
| Queue |  |
| Guest | The counters are not prefixed with Guest, so they are simply called:  Command Latency Write Latency Ready Latency |

With the above understanding, let’s validate with real world values.

[Image: ## Image Description

This table displays **99th and 95th percentile latency metrics** (Device, Kernel, and Queue) for 11 WDC storage devices (`wdc-06-r...`), with color-coded values (green = low/good, yellow/orange = elevated). The **99P Device Latency** ranges from **0.42 ms to 0.81 ms**, with the worst performer showing **0.81 ms device / 0.59 ms kernel latency**. The table validates the surrounding text's discussion of the three latency counter types (Device, Kernel, Queue), demonstrating that device latency dominates (avg 0.06 ms overall but up to 0.81 ms at 99P), kernel latency is secondary, and queue latency is near-zero for most devices (avg 0.0029 ms).]

I chose the last ESXi since that’s the one with worst latency.
I plotted Kernel vs Device.
What do you notice? Can you determine which is which?

[Image: ## Image Description

The chart displays two metrics (Kernel latency in pink and Device latency in purple) plotted over a ~24-hour period from April 27 (~11 AM) to April 28 (~12 PM), with values on the Y-axis ranging from **0 to 0.8 ms**. The pink line (Kernel) shows a prominent spike reaching ~**0.75 ms** around 2:00–3:00 PM, then settles around **0.2–0.4 ms**, while the purple line (Device) shows multiple sharp spikes reaching **0.8+ ms** during the 8:00 PM–3:00 AM window before converging with Kernel latency. The two lines **do not correlate**, validating the text's assertion that Kernel and Device latencies behave independently, with both remaining well below the 5 ms healthy threshold and most values staying under **0.5 ms**.]

They don’t correlate. This is expected since both have reasonably good value (my expectation is below 0.5 ms).
The bulk of the latency should come from the Device. In a healthy environment, it should be well within 5 ms. With SSD, it should be even lower. As you can see below, it’s below 1.75 ms. Notice the kernel latency is 0.2 ms at all times except in 1 spike.

[Image: ## Image Description

The chart displays three disk latency metrics for a VMware ESXi host over a ~14-hour period (approximately 2:30 AM – 4:00 PM on Friday, Sep 24): **Total Latency (1.75 ms)**, **Physical Device Latency (1.06 ms)**, and **Kernel Latency (0.7 ms)** at the highlighted point of 04:46:15 AM. The purple (Total) and cyan (Physical Device) lines track closely together throughout, while the pink (Kernel Latency) line remains consistently near **~0.2 ms or below** with only one notable spike around 4:45 AM reaching ~0.7 ms. This demonstrates that disk latency is dominated by the physical device component, with kernel latency remaining negligible in a healthy storage environment, confirming the author's point that the two components do not correlate and that device latency drives the bulk of total latency.]

What about the Queue latency? It’s part of the kernel latency, so it will be 100% within it. When the kernel latency value is in the healthy range, the 2 values should correlate, as the value is largely dominated by the Queue. Notice the pattern below is basically identical.

[Image: The chart displays **Disk Queue Latency (ms)** aggregated across all instances over approximately 48 hours (Sep 23–24), with a peak high of **0.71 ms** (marked in orange around 09:00 AM on Sep 24) and a low of **0 ms**. The metric shows frequent sharp spikes throughout the period, mostly ranging between 0.1–0.4 ms, with the majority of baseline values near zero. As described in the surrounding text, this pattern closely mirrors the kernel latency chart, confirming that queue latency dominates and correlates with kernel latency when values are in the healthy range (well below 5 ms).]


[Image: This chart displays **Disk Kernel Latency (ms)** aggregated across all instances over approximately 1.5 days (Sep 23–24). The metric remains consistently at or below **0.2 ms** throughout the monitoring period, with one notable spike reaching a **high of 0.76 ms** around 9:00 AM on Sep 24 (marked with an orange dot). This image demonstrates the context claim that kernel latency stays within healthy range at ~0.2 ms except for isolated spikes, serving as the reference chart before the Queue latency comparison in the following image.]


##### Other Metrics

I find the value of Bus Resets and Commands Aborted are always 0

[Image: ## Image Description

The image shows a VMware vSphere metrics table displaying **Bus Resets** and **Commands Aborted** measurements across multiple local disk objects (two ATA disks and one TOSHIBA disk), with Summation rollup in numeric units. All values across **Latest, Maximum, and Minimum columns are consistently 0**, directly supporting the author's claim that these metrics are always zero in practice and have negligible diagnostic value.]

If you’ve seen a non zero let me know.

[Image: The image shows a table listing two VMware vSphere storage metrics: **Highest Latency** (Latest rollup, measured in milliseconds, representing the highest latency value across all disks used by the host) and **Maximum Queue Depth** (Average rollup, measured in num/number, representing the maximum queue depth). These metrics appear in the context of "Other Metrics" for host storage, and the surrounding text notes uncertainty about what latency type "Highest Latency" refers to (Guest, Kernel, or Device) and that **Maximum Queue Depth** is more of a configuration property than a true performance metric.]

I’m not sure what highest latency refers to (Guest, Kernel, or Device).
Maximum Queue Depth is more of a property than a metric, as it’s a setting.

[Image: The image shows a VMware vSphere metrics table displaying **Maximum Queue Depth** measurements for three local storage devices: a TOSHIBA disk with a queue depth of **254**, an ATA disk with **32**, and a Micron 5100 SSD with **31**. All entries use Average rollup with numeric units, and notably each device shows identical Latest, Maximum, and Minimum values, confirming the surrounding text's assertion that this is effectively a **static property rather than a dynamic metric**. The varying queue depths reflect hardware-specific settings (254 for the TOSHIBA, ~32 for the SATA/SSD devices).]


#### Consumption Metrics

You get the standard IOPS and Throughput metrics.

| IOPS |  |
| --- | --- |
| Throughput | The counters names are Read Rate Write Rate Usage All their units are in KB/s |
| Total IO | This is just the number of Read or Write in the time interval. The counters names are Read Requests Write Requests Commands Issued |


### Storage Adapter & Path

They have identical set of counters, hence I’m documenting them together. Ideally, adapter should include metrics such as adapter queue length and commands aborted.
The following screenshot shows the metrics provided:

[Image: The image displays a table of **Storage Adapter & Path performance counters** in VMware vSphere, listing 8 metrics across four columns: Counters, Rollups, Units, and Stat Type. The metrics cover **throughput** (Read Rate, Write Rate in KBps), **I/O requests** (Average commands/read/write requests per second in num), and **latency** (Read latency, Write latency, Highest latency in ms). This table contextualizes the surrounding text by showing that latency metrics use "Average" rollups except Highest latency which uses "Latest," and that throughput metrics are classified as "Rate" type while latency metrics are "Absolute."]

For storage path, the counters may appear that they are measuring the device, as the object name is not based on the friendly name.

[Image: ## Image Description

The chart displays **Read latency metrics (in milliseconds)** for three storage paths over approximately one hour (10:20–11:15 AM), showing periodic sharp spikes reaching **1ms** occurring roughly every 3–5 minutes, while baseline latency remains near **0ms**. The three objects tracked are two **SAS paths** (identified by NAA WWN identifiers) and one **SATA path** (vmhba0-sata.0:0-t10, a Micron 5100 MTFDDAV240TCB SSD), all measuring Read latency. This screenshot demonstrates that storage path object names are based on technical identifiers (adapter/WWN notation) rather than friendly device names, illustrating the point made in the surrounding text that path metrics can appear device-level but are actually per-path measurements.]

The object above is the path, not the device.

#### Contention Metrics

There are 3 metrics provided:
- Read latency
- Write latency
- Highest latency
The highest latency metric takes the worst value among all the adapters or the paths. This can be handy compared to tracking each of them one by one. However, it averages each adapter first, so it’s not the highest read or write. You can see from the following screenshot that its value is lower than the read latency or vmhba0. What you want is the highest read or write among all the adapters or paths.

[Image: ## Image Description

This VMware vSphere performance chart displays **storage adapter read latency** for a single ESXi host over a one-hour window (10:13–11:13 AM on 12/05/2023), showing four metrics in the legend: read latency (Average) for **vmhba64**, **vmhba1**, and **vmhba0**, plus **highest latency** (Latest) for the host. The chart demonstrates that **vmhba0** (green) shows periodic read latency spikes reaching **1 ms** approximately every 5 minutes, while all other adapters and the highest latency metric remain at **0 ms** (Latest=0, Maximum=0). This illustrates the surrounding text's point that the "highest latency" metric reports **0** despite vmhba0 having a maximum of **1 ms**, because it averages adapter values before taking the worst — confirming the author's critique that this metric underrepresents true peak latency.]


##### Analysis

I plotted 192 ESXi host and checked the highest read latency and highest write latency among all their adapters. As the data was returning mostly < 1 ms, I extended to 1 week and took the worst in that entire week. You can see that the absolute worst of write latency was a staggering 250 ms. But plotting the 95th percentile value shows 0.33 ms, indicating it’s a one off occurrence in that week. The 250 ms is also likely an outlier as the rest of the 191 ESXi shows maximum 5 ms, and with much lower value at 95th percentile.

[Image: This table displays disk latency metrics for multiple ESXi hosts (labeled "wd..."), showing **Highest Read Latency, 95th Percentile Read Latency, Highest Write Latency, and 95th Percentile Write Latency**. The data is sorted by Highest Write Latency in descending order, revealing one outlier host with a peak write latency of **250.93 ms** but only **0.33 ms at 95th percentile**, while the remaining hosts cluster around **5.13–5.27 ms** maximum write latency with consistently low 95th percentile values of **0.07–0.21 ms**. This demonstrates the author's point that the 250 ms value is a one-off occurrence, as the 95th percentile effectively filters out the spike and shows normal performance.]

Plotting the value of the first ESXi over 7 days confirmed the theory that it’s a one off, likely an outlier.

[Image: ## Image Description

The image displays four time-series charts for **wdc-08-r04esx07.oc.vmware.com** over a 7-day period (Apr 23–30), showing Storage Adapter metrics: **Highest Read Latency** (H: 3ms, L: 0ms), **Highest Write Latency** (H: 250.93ms, L: 0ms), **Read IOPS** (H: 49,812.07, L: 11,290.67), and **Write IOPS** (H: 23,183.67, L: 12,370.73). All latency metrics show flat near-zero values throughout the week with a **single sharp spike on April 29**, while IOPS remain consistently elevated with regular periodic peaks. This confirms the surrounding text's assertion that the 250ms write latency is an isolated one-off outlier on this specific ESXi host, with otherwise normal latency behavior across the observation period.]

Does it mean there is no issue with the remaining of the 191 ESXi hosts?
Nope. The values at 95th percentile is too high for some of them.
I modified the table by changing Maximum with 99th percentile to eliminate an outlier. I also reduced the threshold so I can see better. The following table shows the values, sorted by the write latency.

[Image: ## Image Description

This table displays **99th and 95th percentile read/write latency metrics** for 192 ESXi hosts (showing items 151-192, page 4), sorted by **99P Write Latency** in ascending order. Write latencies range from **0.73 ms to 1 ms** (highlighted in yellow/orange indicating elevated values), while read latencies vary more widely (0.07 ms to 1.07 ms). The table demonstrates that while a single outlier host was previously identified for read latency, **multiple ESXi hosts exhibit concerning 99P write latencies approaching or reaching the 1 ms threshold**, with an average 99P write latency of 0.26 ms and maximum of 1 ms across all 192 hosts.]

The table revealed that there are indeed latency problem. I plotted one of the ESXi and saw the following.

[Image: ## Image Description

The chart displays **Storage Adapter Highest Read Latency and Highest Write Latency (ms)** for a single ESXi host (`wdc-06-r01esx31....ware.com`) over the period of **April 24–29**, with the pink line representing write latency and the purple line representing read latency. Both metrics show **significant spikes** — write latency peaks appear to reach extremely high values (potentially hundreds of ms) on April 24, 25, and 28 around noon, while sustained elevated latency is visible from April 26 onward for both read and write. This confirms the surrounding text's assertion that drilling into individual ESXi hosts reveals real storage latency problems that aggregate/maximum metrics alone may have obscured.]

From here, you need to drill down to each adapter to find out which one.

#### Consumption Metrics

For each adapter, there are 4 metrics provided:
- Read IOPS, tracking the number of reads per second.
- Write IOPS
- Read throughput
- Write throughput.
The following screenshot is an example of what you get from vSphere Client UI.

[Image: ## Image Description

The chart displays **HBA adapter consumption metrics** for two adapters (vmhba0 and vmhba1), showing average read and write IOPS over approximately one hour (10:48–11:45 AM). A significant spike in **vmhba1 read requests** is visible between ~11:10–11:15 AM, peaking at **7,481 IOPS** (average 422.956, minimum 11), while vmhba1 write requests remain relatively stable at 447–643 IOPS (average 524.844). vmhba0 shows minimal activity (max read: 141, max write: 66), demonstrating how drilling down to individual adapters can isolate which specific HBA is responsible for anomalous I/O behavior contributing to the previously identified latency problems.]

If the block size matters to you, create a super metric in VCF Operations.

### Datastore

For shared datastore, the metrics do not show the same value with the one at datastore object. All these metrics are only reporting from this ESXi viewpoint, not the sum from all ESXi mounting the same datastore. As a result, I’d cover only performance. Capacity will be covered under the datastore chapter.
For each datastore, you get the usual IOPS, throughput and latency. They are split into read and write, so you have 3 x 2 = 6 metrics in total. These are the actual names:

[Image: This table displays **8 datastore performance counters** available per ESXi host in VMware vSphere, organized by counter name, rollup type (Average or Latest), unit (num, µs, ms, KBps), and description. The metrics cover the core I/O performance dimensions: **IOPS** (read/write requests per second in num), **latency** (read latency, write latency, datastore latency observed by VMs, and highest latency in ms/µs), and **throughput** (read rate and write rate in KBps). In context, this table enumerates the 6 primary read/write metrics (3×2) plus the 2 additional latency counters referenced in the surrounding text, establishing the baseline metrics before the author discusses the unexpected gap between "Datastore latency observed by VMs" (µs-granularity, Latest rollup) and the other latency counters.]

There is no block size but you can derive it by dividing Throughput with IOPS.
You also get 2 additional counters:
- Datastore latency observed by VMs
- Highest latency.
I plotted their values and to my surprise the metric Datastore latency observed by VMs is much higher. You can see the blue line below. It makes me wonder what the gap is as there is only the kernel in between.

[Image: The chart displays four metrics for **SC2-NFS-01** datastore over approximately one hour (9:48–10:48 PM): **Datastore latency observed by VMs** (blue, in µs, average 1,639 µs, peaking at **15,330 µs** ~10:08 PM), **Highest latency** (black, in ms, average 0.128 ms, max 3 ms), **Read latency** (green, consistently 0 ms), and **Write latency** (orange, average 1.033 ms, max 4 ms). The chart visually demonstrates the dramatic discrepancy between VM-observed datastore latency (~1,600 µs average) and the storage-side Highest Latency metric (~0.128 ms average), with the blue line running significantly higher than the other metrics throughout the observation period. This supports the author's point that **Highest Latency is a normalized average of read and write** and thus appears lower than the VM-perspective latency metric.]

The metric Highest Latency is a normalized averaged of read and write, hence it can be lower.

#### Outstanding IO

You can derive the outstanding IO metric from latency and IOPS. I think latency counter is more insightful. For example, the following screenshot shows hardly any IO being in the queue:

[Image: The chart displays the **Datastore Outstanding IO Requests (OIOs)** metric over approximately one week (April 23 – May 1), with a peak value of **H: 0.073** (marked in orange around April 26) and a low of **L: 0.00084**. The majority of values remain very close to zero (well below 0.05), indicating minimal IO queue depth throughout the observed period. This supports the surrounding text's assertion that outstanding IO metrics show "hardly any IO being in the queue," while latency charts would reveal more meaningful performance insights.]

However, if you plot latency, you get same pattern of line chart but with higher value.

[Image: ## Image Description

The chart displays **Datastore|Total Latency Max (ms)** over approximately one week (April 23 – May 1), showing a high value (**H: 70ms**) marked in orange around April 23-24, with a low value (**L: 166** — likely 1.66ms or similar near-zero value) marked in yellow. The latency pattern shows elevated spikes in the April 23-25 range that progressively diminish, stabilizing near **0ms** by April 28-30. This chart contextually supports the surrounding text's point that plotting latency reveals meaningful patterns (higher values and variability) compared to Outstanding IO metrics, with the data suggesting write latency as a likely contributor to the early spikes.]

You can check whether it’s read or write by plotting each.
The following screenshot shows it’s caused by write latency. It’s expected if your read is mostly served by cache.

[Image: ## Image Description

The image displays two time-series charts for the ESXi host **wdc-09-r05esx09.oc.vmware.com** covering **April 24–May 1**, showing **Datastore Highest Read Latency** (H: 10.93ms, L: 0ms) and **Datastore Highest Write Latency** (H: 70ms, L: 1.93ms) across all instances. The write latency chart shows significantly higher and more frequent spikes (peaking ~70ms around April 24) compared to the relatively flat read latency (max ~10ms with a notable spike on April 29), demonstrating that the elevated datastore latency identified in the preceding charts is **primarily driven by write operations**, while reads remain low — consistent with a read cache-hit scenario.]


#### Queue Depth

You can also see the queue depth for each datastores (I think this is actually the backing LUN, but unsure if there are extent). Ensure that the settings are matching your expectation and are consistent. You can list them per cluster and see their values.

[Image: The image shows a table displaying **Max Queue Depth** metrics for six ESXi hosts (blr-01-r06esx30/31/32.oc.vmware.com) across two instance names (148341 and 148384). All entries show an identical Max Queue Depth value of **4,294,967,296** (2³², the maximum 32-bit unsigned integer value), with both the Average and Max summary rows confirming the same value. This demonstrates consistent queue depth settings across all hosts in the cluster, illustrating the recommendation in the text to verify that queue depth settings are matching expectations and uniform across the environment.]

Chapter 5

# Network


## Architecture

Network monitoring is complex, especially in large data centers. Adding network virtualization takes the complexity of performance troubleshooting even higher.
Just like CPU, Memory and Disk, there is also a new layer introduced by virtualization. There are virtual network cards on each VM, and software-based switch on each ESXi bridging the VM card to the physical NIC card. The various ESXi kernel modules also do not “talk” directly to the physical card. Basically, what used to be the top of rack switch are now living inside each ESXi as a software switch.

[Image: The diagram illustrates the two-layer virtual network architecture in VMware vSphere, showing **ingress/egress traffic flow** through a software-based virtual switch (vSwitch) connecting VM and VMkernel (VMK) ports to physical NIC cards. Two ESXi hosts are depicted side-by-side, connected at the switch layer (indicated by the dotted red line), with green NIC cards at the physical layer below. This visualization supports the surrounding text's explanation that network virtualization introduces an additional software switching layer between VMs/VMK modules and the physical NIC, which is critical context for understanding why certain VM-to-VM traffic metrics (intra-host) may not register at the physical layer.]

vSphere Client shows the 2 layers side by side (personally I prefer up and down, with the physical layer placed below).

[Image: The image shows the **Virtual Switches configuration panel** in vSphere Client for ESXi host `sc2-hs2-b1614.eng.vmware.com`, displaying a **Distributed Switch (SC2-dSwitch-1)** with three port groups: **NestedESXi-Traffic** (VLAN 1536, 7 VMs), **VM-Traffic** (VLAN 1536, 1 VM), and **vxw-vmknicPg-dvs-81-0-8f710** (VMkernel port, 0 VMs). The uplink section shows **SC2-dSwitch-1-DVUplinks-81** with 4 uplinks, where only **Uplink 1 has 1 physical NIC adapter** connected and Uplinks 2-4 have none. This screenshot illustrates the two-layer virtual networking architecture described in the text — the left side showing software-defined port groups (virtual layer) and the right side showing physical uplink adapters — demonstrating how virtual switches bridge VM virtual NICs to physical NICs.]


| Virtual Network | There are 2 types:  Kernel VM They do not mix, for security reason.  The kernel port group runs specific traffic, such as vMotion and vSAN.  The VM port group runs VM. If the traffic is just a VM-to-VM traffic, within the same ESXi, the packets does not reach the physical network, hence the metrics do not register it. This is why the values in virtual do not always match physical. The virtual network does not have the limit that physical network does, if the traffic remains in the box. This makes it harder to troubleshoot as the total capacity is not statically defined. So instead of just monitoring the throughput metric, you should also check the packet per second metric. |
| --- | --- |
| Physical Network | They are called vmnic instead of pNIC Metrics at this level do not have per-VM breakdown, or per kernel interface breakdown |


### Unique Characteristics

From performance and capacity management point of view, network has different fundamental characteristics to compute or storage. The key differences are summarized below.

|  | Compute or Storage | Network |
| --- | --- | --- |
| Nature | A node | An interconnect |
| Hardware | Single purpose | Multi-purpose |
| Location | Fewer | Many |
| Upper Limit | Yes | No |
| Net available resource to VM | Relatively high | Low |
| Resource allocation at VM level | Granular | Coarse |
| Monitoring | Simpler | Harder |
| Workload Type | 1 | Many |
| Primary Unit | Byte | Bit |


#### Nature of Network

Compute and storage are nodes. They are dots, while network are lines.
When you have a CPU or RAM performance issue on one host, it doesn't typically impact another host on a different cluster. The same thing happens with storage. When a physical array has a performance issue, generally speaking it does not impact other arrays in the data center.
Network is different. A local performance issue can easily be a data center-wide problem. Here is a good read by shared Ivan Pepelnjak. To give a recent example (H2 2021), here is one from a world-class network operator:

[Image: This image shows a **public incident post-mortem statement** from a major platform (consistent with Facebook's October 2021 outage), explaining that a **backbone router configuration change** caused cascading network failures across their data centers, bringing all services to a halt. The statement notes that internal tooling was also impacted, compounding diagnosis and recovery time. In the context of the surrounding text, this serves as a real-world example illustrating how **network failures are uniquely systemic** — unlike CPU, RAM, or storage issues, a single network misconfiguration can cause **data-center-wide or global outages** due to the interconnected nature of routing infrastructure.]

Being an interconnect, it also connects users and servers to the Internet. If you have a global operation, you likely have multiple entry points, provided by different providers. These connectivity needs to be secured and protected with HA, preferably from 2 different ISPs.
There are typically many paths and routes in your network. You need to ensure they are available by testing the connectivity from specific points.

#### Hardware

The networking hardware itself can provide different functionalities.
For compute, you have servers. While they may have different form factors or specifications, they all serve the same purpose—to provide processing power and a set of working memory for hypervisor or VM.
For network, you have a variety of network services (firewall and load balancer) in addition to the basic network functionalities (switch, router, and gateway). You need to monitor all of them to get a complete picture. These functionalities can take the form of software or hardware.
Unlike storage, network has concept of duplex. A full duplex means it has 100% on both directions. For example, an ESXi with a 25 Gb port can theoretically handle 25 Gb TX + 25 Gb RX as its full duplex.
Blade servers and other HCI form factors blur the line between server and network.

#### Location

Server and storage tend to be located fewer places. Even in the ROBO office, they are typically located in a rack, with proper cooling and physical security. Network switch, especially Wireless Access Points, need to be placed in multiple places within the building, if that’s required to provide enough network coverage.
Solution such as SDWAN even requires a network device to be deployed at employee home. I actually have the Dell edge device at my home.

#### Total Capacity

CPU or RAM workload have a per VM physical limit. This makes capacity management possible, and aids in performance troubleshooting.
While network has a physical limit, it can be misleading to assume it is available to all VMs all the time. Because the physical capacity of the network is shared, you have a dynamic upper limit for each workload. The VM Network port group will have more bandwidth when there is no vMotion happening. Furthermore, each VM has a dynamic upper limit as it shares the VM Network port group with other VMs.
The resource available to VM also varies from host to host. Within the same host, the limit changes as time progresses. Unlike Storage I/O Control, Network I/O Control does not provide any metrics that tell you that it has capped the bandwidth.
In many situations, the bandwidth within the ESXi host may not be the smallest pipe between the originating VM and its destination. Within the data center, there could be firewalls, load balancers, routers, and other hops that the packet has to go through. Once it leaves the data center, the WAN and Internet are likely to be a bottleneck. This dynamic nature means every VM has its own practical limit.

#### Net Available Resource

At the end of the day, the net available resources to the VMs are what we care about. What the IaaS platform used is considered an overhead. The more ESXi kernel, NSX, vSAN, vSphere Replication use, the lesser you have left for the business workload.
An ESXi host has a fixed specification (for example, 2 CPUs, 60 cores, 1 TB RAM, 2 x 50 GE NIC). This means we know the upper physical limit. How much of that it available to the VMs? Another word, what is the usable capacity for the business workload?
For compute, the hypervisor consumes a relatively low proportion of resources. Even if you add a software-defined storage such as vSAN, you are looking at around 10% total utilization but depends on many factors.
The same cannot be said about network. Mass vMotion (for example, when the host enters maintenance mode), storage vMotion (in IP storage case), VM provisioning or cloning (for IP storage), and vSAN all take up significant network bandwidth. In fact, the non-VM network takes up the majority of the ESXi resources. If you have 2 x 25 GE NIC, majority of it is not used by VM. The following screenshot shows that VM only gets 100 shares out of 500 shares. So the overhead can be as high as 80%!

[Image: This screenshot shows the **Network I/O Control (NIOC) System Traffic configuration** on a VMware vSphere Distributed Switch (SC2-dSwitch-1), with a total bandwidth capacity of **10.00 Gbit/s** and maximum reservation of **7.50 Gbit/s**. The traffic allocation table reveals that **Virtual Machine Traffic is assigned "High" shares with a value of 100**, while all other traffic types (Management, FT, vMotion, iSCSI, NFS, vSAN, etc.) each receive "Normal" shares of 50, totaling **500 shares across 9 traffic types**. This demonstrates the book's point that VMs receive only 100 out of 500 total shares (~20%), meaning infrastructure/system traffic can consume up to **80% of available network bandwidth**, leaving VMs with a minority of the physical NIC capacity.]


#### Resource Allocation

This means the resource that is given to a single VM itself. For compute, we can configure a granular size of CPU and RAM. For the CPU, we can assign one, two, three, four, etc. vCPUs.
With network, we cannot specify the vNIC speed. It takes the speed of the ESXi vmnic assigned to the VM port group. So each VM will either see 1 GE or 10 GE or 25 GE (you need to have the right vNIC driver, obviously). You cannot allocate another amount, such as 500 Mbps or 250 Mbps in the Guest OS. In the physical world, we tend to assume that each server has 10 GE and the network has sufficient bandwidth. You cannot assume this in a virtual data center as you no longer have 10 GE for every VM at the physical level. It is shared and typically oversubscribed.
A network intensive VM can easily hit 1 Gbps for both egress and ingress traffic. The following chart shows a Hadoop worker node receiving more than 5 Gbps worth traffic multiple times. You need to be careful in sizing the underlying ESXi if you want to run multiple VMs. While you can use Network I/O Control and vSphere Traffic Shaping, they are not configuration property of a VM.

[Image: The chart displays **Network Data Receive Rate (Gbps)** and **Network Data Transmit Rate (Gbps)** for a Hadoop worker node over approximately 24 hours (March 6 2PM – March 7 2PM). The receive rate (purple) consistently ranges between **2–7.5 Gbps** with multiple spikes, peaking dramatically at **11.62 Gbps** at 02:04:37 AM on March 7, while the transmit rate (pink) remains relatively low, hovering near **0–2.5 Gbps** (0.945 Gbps at the highlighted point). This demonstrates the text's assertion that network-intensive VMs can sustain multi-Gbps ingress traffic, illustrating the challenge of sizing ESXi hosts when running multiple such VMs on shared 10 GE infrastructure.]


#### Monitoring and Troubleshooting

A distributed system is harder to monitor than a single node, especially if workload varies among the components that make up the system.
The network resource available to VM also varies from host to host. Within the same host, the limit changes as time progresses. Unlike Storage I/O Control, Network I/O Control (NIOC) does not provide any metrics that tell you that it has capped the bandwidth.
NIOC can help to limit the network throughput for a particular workload or VM. If you are using 10 GE, enable NIOC so that a burst in one network workload does not impact your VM. For example, a mass vMotion operation can saturate the 10 Gb link if you do not implement NIOC. In vCenter 7, there is no counter that tracks when NIOC caps the network throughput. You may need to check the log for that.
The primary contention metrics are
- Latency.
- Dropped Packets
- Retransmit Packets. For TCP, dropped packets will be retransmitted.
- Jitter. This measures the inconsistency of the latency. An application may tolerate poor latency better than variable latency.
Note there is no latency and retransmit metrics in vSphere.
Remember that Storage has 2 metrics (IOPS and Throughput) for consumption? Network also has these 2 types, except the more popular one is the throughput. The PPS (packet per second) is less popular although they are useful in gaining insight into your network. It takes up a significant CPU time to process high number of packets with low latency, as you can see in NSX edge VM.

#### Workload Type

In network, not all packets are of the same type. You can have unicast, multicast and broadcast.
Majority of traffic should be unicast, as ESXi or VM should not be broadcasting to all IP addresses in the network or multicasting to many destinations. The challenge is there are purposes for each type so you need to monitor if the broadcast and multicast happen at the wrong time in the wrong network.
Storage and Server only have 1 type of workload. From operations management viewpoint, for almost all customers, A CPU instruction is a CPU instruction. You do not care what it is. The same goes with memory access and disk IO commands.

#### Conclusion

Because of all these differences, the primary unit is bit, not byte. Storage uses byte as it focuses on the amount of disk space consumed by the data.
The way you approach network monitoring should also be different. If you are not the network expert in your data center, the first step is to partner with experts.
BTW, there are other things which I did not cover. For example, in network there are basic services such as DNS and NTP. All these services need to be monitored, typically for availability and reliability.

### Network Observability

The arrival of software-defined infrastructure services also changes the way you monitor your network. The following diagram shows a simplified setup of an ESXi host.

[Image: ## Image Description

The diagram illustrates a simplified ESXi host network architecture showing **four distinct monitoring areas**: VM network (VM 1, VM 2, VM 3 connected via Port Groups), kernel network (vmk interface), ESXi kernel modules (represented by the sun icon), and Agent VMs (shown with a blue upward arrow indicating separate traffic flow). All components sit atop a **Distributed Switch** layer, which aggregates the Port Groups before connecting to the physical ESXi host. The image contextualizes why network observability requires monitoring at multiple layers — the virtual switching layer (Distributed Switch) handles intra-host VM-to-VM traffic invisibly to physical NICs (vmnics), making traditional physical network metrics insufficient for complete visibility.]

In a single ESXi host, there are 4 areas that need to be monitored for a complete network monitoring:
- VM network
- The kernel network
- ESXi kernel modules
- Agent VMs
There are 2 layers of networking.
- The virtual network consists of VM and the kernel (e.g. vMotion). If the traffic is a VM to VM traffic within the same ESXi, the packets does not reach the physical network, hence the vmnic metrics do not register it. The virtual network does not have the limit that physical network does, if the traffic remains in the box. This makes it harder to use this metric as the 100% is not statically defined. So instead of just monitoring the throughput metric, you should also check the packet per second metric.
- The physical network means traffic going through the physical network card. At this level it’s no longer aware of VM and the kernel.
In the preceding example, we have 3 VMs running in the host. VM 1 and VM 2 are connected to the same VXLAN (or VLAN). VM 3 is on a different VXLAN (or VLAN), hence it is on a different port group. Monitoring at port group level complements monitoring at VM level and ESXi level.
Traffic at Distributed Switch level carries more than VM traffic. It also carries the kernel traffic, such as vMotion and VSAN. Both the kernel network and VM network tend to share the same physical uplinks (ESXi vmnic). As a result, it’s easier to monitor at port group level.
Sounds good so far. What is the limitation of monitoring at distributed port group level?
The hint is at the word distributed.
Yes, the data is the aggregate of all the ESXi hosts using that distributed port group!
By default, VM 1 and VM 2 can talk to each other. The traffic will not leave the ESXi. Network monitoring tools that are not aware of this will miss it. Traffic from VM 3 can also reach VM 1 or VM 2 if NSX Distributed Logical Router is in place. It is a kernel module, just like the NSX Distributed Firewall. As a result, monitoring these kernel modules, and the host overall performance, becomes an integral part of network monitoring.
The 4th area we need to monitor is Agent VM. An Agent VM is mapped to 1 ESXi Host. It does not need HA protection as every ESXi host has one, hence it typically resides on the host local datastore.

[Image: The diagram illustrates an ESXi host running five VMs: three **Agent VMs** (Storage VM, Network VM, Security VM) each consuming **CPU** resources, and two **Business VMs** consuming **Disk** and **Net** resources respectively. This architecture demonstrates how Agent VMs are co-located on the same ESXi host alongside Business VMs, sharing host resources. The image contextualizes the monitoring challenge: Agent VMs (e.g., Nutanix CVM, Trend Micro security appliance) consume CPU overhead that must be accounted for when measuring overall ESXi host performance metrics.]

The above example shows an ESXi host with 3 agent VMs. The first VM provides a storage service (an example is Nutanix CVM), the second VM provides Network service, and the 3rd VM provides a Security VM.
Let’s use the Security service as an example. A popular example here is Trend Micro Deep Security virtual appliance. It is in the data path. If the Business VMs are accessing files on a fileserver on another network, the files have to be checked by the security virtual appliance first. If the agent VM is slow (and it could be due to factor that is not network related), it will look like a network or storage issue as far as the business VMs are concerned. The Business VMs do not know that their files have been intercepted for security clearance, as it is not done at the network level. It is done at the hypervisor level.

#### Source of Data

A complete network monitoring requires you to get the data from 5 different sources, not just from vSphere. In SDDC, you should also get data from the application, Guest OS, NSX and NetFlow/sFlow/IPFIX from VDS and physical network devices. For VDI, you need to get data at application level. We have seen packet loss at application-layer (Horizon Blast protocol) when Windows sees no dropped packet. The reason was the packet arrives out of order and hence unusable from protocol viewpoint.
The following shows a simplified stack. It shows the five sources of data and the 4 tools to get the data. It includes a physical switch as we can no longer ignore physical network once you move from just vSphere to complete SDDC.

[Image: ## Image Description

This architectural diagram illustrates the **five sources of network metrics** in a VMware vSphere/SDDC environment and the **four collection tools** used to aggregate them. The five metric sources are: Application level counters, Guest OS level counters, NSX counters, vSphere counters, and Physical network counters — collected from a stack comprising VMs, Port Groups, Distributed Switch, ESXi hosts, and Physical Switches. These metrics flow into four collection mechanisms (**Network Flow, vCenter, Syslog, SNMP**), which ultimately feed into **vRealize Operations Insight** for unified monitoring and analysis.]

The network packet analysis comes in 2 main approaches: Header analysis and full packet analysis. The header analysis is certainly much lighter but lack the depth of full analysis. You use this to provide overall visibility as it does not impose heavy load on your environment.
The impact of virtualization on network monitoring goes beyond what we have covered. Let’s add NSX Edge into the above, so you can see the traffic flow when the edge services are also virtualized. You will see that a network problem experienced by a VM on one ESXi could be caused by another VM running on another ESXi. The following diagram is a simplified setup, showing a single NSX Edge residing on another cluster.

[Image: ## Image Description

The diagram illustrates a **virtualized network topology** showing traffic flow (indicated by red and blue arrows) between VM 1 and an NSX Edge VM across two separate clusters. The left cluster contains a Distributed Switch with ESXi A/B hosts, while the right cluster hosts the NSX Edge VM on ESXi C/D, both clusters connecting through redundant Physical Switches and Routers. The colored arrows demonstrate that VM 1's traffic must traverse **multiple physical hops** (ESXi C → Physical Switch → Router path shown in red, return path in blue), illustrating how network performance issues for VM 1 can originate from resource contention (CPU/RAM) on a completely different ESXi host running the NSX Edge VM.]

In the above example, let’s say VM 1 needs to talk to outside world. An NSX Edge VM provides that connectivity, so every TCP/IP packet has to go through it. The Edge VM has 2 virtual NICs, one for each network. If the NSX Edge VM has CPU issue, or the underlying ESXi has RAM issue, it can impact the network performance of VM 1.

| Type | Guest OS Metric | VM Equivalent |
| --- | --- | --- |
| Contention | Dropped Packet | None, as the dropped packet at VM is a different level. |
| Contention | Latency | None, no such metric available in vSphere |
| Utilization | Throughput | They should match with the metrics at VM level. If not, there is dropped packets.  They should be reported based on traffic type: unicast, multicast, broadcast. |
| Utilization | Packet/second | They should match with the metrics at VM level. If not, there is dropped packets.  They should be reported based on traffic type: unicast, multicast, broadcast. |


#### Traffic Flow

The terminology Egress and Ingress are used in context of an environment. For example, the flow from a VM to the Internet, where it will hop through different types of network devices. Typically, going further “inside” is considered ingress. That’s why a VM does not have ingress traffic.
The terminology receive/RX and transmit/TX/send are used in context of a single port. A port has both incoming and outgoing traffic.
The following shows a simple example:

[Image: The diagram illustrates the relationship between **Egress/Ingress** directional terminology and **Transmit/Receive** port-level terminology in a network traffic flow context. It shows traffic flowing from an external source through an **NSX Edge Appliance** to a **Web Server**, with the left interface of the Edge labeled as Egress (Receive/Transmit) and the right interface labeled as Ingress (Transmit/Receive), while the Web Server's interface is labeled Egress (Receive/Transmit). This clarifies that Egress/Ingress describe traffic direction relative to the environment, while Transmit/Receive describe traffic direction relative to an individual port.]

The following applies that to vSphere distributed vSwitch. Notice the ESXi host is not shown as it’s not part of the hop. The ESXi host physical NIC card is the distributed vSwitch uplink.

[Image: The diagram illustrates network traffic flow directionality across three hops: a **Physical Switch (top of rack)**, a **Distributed vSwitch** (with an ESXi NIC uplink), and a **VM** (connected via a vPort). It maps the relationship between **Ingress/Egress** perspectives and **Transmit/Receive** directions at each port boundary — for example, traffic transmitted by the physical switch is received at the ESXi NIC's ingress side. The VM has **no ingress designation** because it represents the end of a flow, which contextually explains why vSphere metrics lack ingress metrics at the VM level.]


#### Traffic Type

VCF Operations provides these metrics at VM, ESXi, Distributed Port Group and Distributed Switch level. As vSphere Tanzu Pod is basically a VM, it also has the metric.
BTW, one way to check what objects in what adapter have the specific metric is in the VCF Operations policy. Open any policy, and search the metric using its name. The list of matching metrics will be shown, grouped by the objects.

[Image: ## Image Description

This screenshot from VMware VCF Operations (vROps) shows the **Metrics and Properties policy editor**, filtered by "Name: multicast" to display multicast-related network metrics for the **Virtual Machine** object type. Four multicast metrics are visible under the Network category: **Multicast Packets Received** and **Total Multicast Packets Received** are both **Disabled (Inherited)**, while **Multicast Packets Transmitted** and **Total Multicast Packets Transmitted** are **Enabled (Inherited)** but show **Disabled** in the Instanced State column. This demonstrates how to locate which object types (VM, Host System, vSphere Distributed Port Group/Switch) carry specific metrics across adapters, as referenced in the surrounding text about traffic type metrics.]

As you can see from above, there is no aggregation at higher level, so create super metric for the time being. I have not created those metric out of the box as I’m yet to use them in dashboard or alert.

#### Packet Size

It’s typically 1600 byte with NSX, or 9000 bytes if you enable jumbo frames).
Special purpose packet such as ping test is smaller. But they should be a small percentage of your network.
Track the packet sizes and compare them with your expectation.

## VM

VM is not an Operating System, so it has far less networking metric than Windows or Linux.

### Overview

We will cover each metric in-depth, so let’s do an overview first.
As usual, we start with contention. All we have is the dropped packet metrics.

[Image: The image displays a metrics table showing two **contention-related counters** for VM networking: **"Receive packets dropped"** and **"Transmit packets dropped"**, both using **Summation** rollup and **num** (number) units. These metrics represent dropped inbound and outbound packets respectively, and serve as the primary (and only) contention indicators available at the VM level for network performance monitoring in vSphere.]

Next, you check if there are unusual traffic. Your network should be mostly unicast, so it’s good to track the broadcast and multicast packets. They might explain why you have many dropped packets. If packets are broadcast packets, it might be dropped by the network.

[Image: The image displays a metrics reference table with four network packet counters: **Broadcast receives**, **Broadcast transmits**, **Multicast receives**, and **Multicast transmits**. All four metrics share the same properties: **Summation** rollup type, **num** (numeric) unit, and measure packets received/transmitted during the sampling interval. In the context of the surrounding text, these metrics are used to identify unusual non-unicast traffic patterns that could explain dropped packets, since broadcast and multicast packets may be dropped at the network level.]

Next you check utilization. There are 6 metrics, but I think they are triplicate.

[Image: The image shows a table of **VM network utilization metrics** available in vSphere, listing 6 entries that appear to be **triplicate pairs**: "Data receive rate" and "Data transmit rate" (each appearing twice with slightly different descriptions), plus their underlying counter equivalents **`counter.net.pnicBytesRx`** and **`counter.net.pnicBytesTx`**. All metrics use **Average** aggregation and are measured in **KBps**. This confirms the author's assertion that the 6 utilization metrics are effectively duplicates, measuring the same Rx/Tx throughput through different naming conventions.]

Each packet takes up CPU for processing, so it’s good to check if the packet per second becomes too high

[Image: The image shows a table defining two network metrics: **Packets Received** and **Packets Transmitted**, both using a **Summation** aggregation method with a numeric (`num`) data type. These metrics measure the count of packets received and transmitted during a monitoring interval, respectively. In context, this table supports the discussion about tracking packets-per-second rates, as high packet counts can increase CPU overhead on vNICs.]

The metrics are available at each individual vNIC level and at the VM level. Most VMs should only have 1 vNIC, so the data at VM level and vNIC level will be identical.
The vNICs are named using the convention "400x". That means the first vNIC is 4000, the second vNIC is 4001, and so on. The following is a vCenter VM. Notice it receives a few broadcast packets, but it’s not broadcasting (which is what you expect). It also does not participate in multicast, which is again expected.

[Image: ## Image Description

This real-time performance chart from vCenter displays network broadcast and multicast packet metrics for a VM's vNIC (object "4000") over a one-hour window on 09/27/2021. The chart shows **Broadcast receives** (blue line) with a notable spike reaching a maximum of **45 packets** around 1:00 PM, an average of **2.333**, and a latest value of **7**, while **Broadcast transmits**, **Multicast receives**, and **Multicast transmits** all remain at **0** throughout the monitoring period. This demonstrates the expected behavior described in the surrounding text — the VM receives occasional broadcast packets but does not transmit broadcasts or participate in multicast traffic.]

The metrics are grouped into 2:
- Transmit for outgoing
- Receive for incoming.
For each group, the following metrics are provided:

| Broadcast packets | Count of packets.  It is the sum during the sampling window, not the rate (which is packet/second). Multicast packet and broadcast packet are listed separately. This is handy as they are supposed to low for most VM. Understand the nature of the applications so you can check if the behaviour is normal or not. |
| --- | --- |
| Multicast packets | Count of packets.  It is the sum during the sampling window, not the rate (which is packet/second). Multicast packet and broadcast packet are listed separately. This is handy as they are supposed to low for most VM. Understand the nature of the applications so you can check if the behaviour is normal or not. |
| Packet dropped | Count of packets.  It is the sum during the sampling window, not the rate (which is packet/second). Multicast packet and broadcast packet are listed separately. This is handy as they are supposed to low for most VM. Understand the nature of the applications so you can check if the behaviour is normal or not. |
| Total packets | The total includes the broadcast and multicast, but not the dropped ones. |
| Throughput per second | This is measured in kilobyte, as packet length is typically measured in bytes. While there are other packet sizes, the standard packet is 1500 bytes.  BTW, esxtop measures in megabit. I assume this includes broadcast and multicast, but not the dropped packet. |

Guess what metrics are missing?
- Retransmit. This can be useful in troubleshooting TCP packet. It naturally does not apply to UDP traffic.
- Latency. 
A normalized latency would help, especially if it’s broken into internal network and external network. Network latency could be impacted by CPU. CPU might not fast enough to process the packet. In VM, this could also be due to the VM having CPU contention. 
If the latency is caused by too many hops and firewall, optimize the traffic using tools such as vRealize Network Insight.
- Packets per second. This can be derived by packet count / sampling window. If you have 200 packets in 20 seconds, that means 10 packets per second.
- Packet size. This can be computed by throughput / packet count. Expect this to be around 1500 byte.
BTW, if you see a pair of metrics with identical name, but one of them is prefixed with “Total”, avoid the one without “Total.” They are averaged over 15 data points, so their value is 15x lower.

[Image: The image shows a legend comparison between two metrics: **"Broadcast Packets Received"** and **"Total Broadcast Packets Received"**, visually highlighting the word "Total" in green on the second entry. This illustrates the warning described in the surrounding text — that metrics prefixed with "Total" should be preferred over their non-prefixed counterparts, as the latter are averaged over 15 data points, making their values artificially **15x lower** than actual figures.]


### Contention Metrics

As usual, let’s approach the metrics starting with Contention. We covered earlier that the only contention metric is packet loss.
For TCP connection, dropped packet needs to be retransmitted and therefore increases network latency from application point of view. The counter will not match the values from Guest OS level. RX packets are dropped before it’s handed into Guest OS, and TX packets are dropped after it left the Guest OS. ESXi dropped the packet because it’s not for the Guest OS or it violates the security setting you set.
The following summary proves that receive packet gets dropped many more times than transmit packet. This is based on 3938 VMs. Each shows the last 1 month, so approximately 35 million data points in total. The average of 35 million data points show that dropped RX is significantly higher than dropped TX. This is why it’s not in the SLA.

[Image: The table displays network packet drop metrics across 3,938 VMs, showing **Average Drop (%), RX Drop, TX Drop, RX, and TX** values for four named VMs plus a summary row. The top entries show Average Drop percentages ranging from **1.56% to 1.71%**, with RX Drop values (~1,863–1,969) dramatically exceeding TX Drop values (~0.07–0.67), and the Summary row confirms this disparity with **RX Drop of 6,095.61 versus TX Drop of only 941.5**. This data directly supports the surrounding text's assertion that received packets are dropped significantly more frequently than transmitted packets, justifying why dropped RX is excluded from SLA calculations.]

The following table shows that the drop is short and spiky, which is a good thing. The value at 99th percentile is 35x smaller than the value at 100th percentile.

[Image: ## Image Description

This is a VMware vRealize Operations **List View** showing network packet drop metrics across **4,060 items** (VMs) in the vSphere World environment. The table displays columns for **All Drop at 99th Percentile**, **Max All Drop**, **Average RX**, and **Average TX**, with the Summary row showing a 99th percentile drop of **0.22%** versus a Max All Drop of **7.61%** — approximately a **35x difference** — confirming the spiky, short-duration nature of packet drops. The **Average RX of 14.91** (underlined in red) is significantly higher than **Average TX of 1.25**, visually reinforcing the preceding text's point that receive-side drops dominate over transmit-side drops.]

The high value in receive can impact the overall packet dropped (%) counter, as it’s based on the following formula
dropped = Network|Received Packets Dropped + Network|Transmitted Packets Dropped
delivered = Network|Packets Received + Network|Packets Transmitted
Network|Packets Dropped (%) = dropped / (dropped + delivered) * 100
I’ve seen multiple occurrences where the packet dropped (%) jumps to well over 95%. That’s naturally worrying. They typically do not last beyond 15 minutes.

[Image: ## Chart Description

This line chart displays **Network Packets Dropped (%)** as an aggregate across all instances, spanning approximately **04:15 AM to 06:45 AM**. The metric shows two sharp spikes reaching nearly **100%** (High: 98.4%) — one around **05:15–05:30 AM** and another at approximately **06:30 AM** — with baseline values otherwise near **0%** (Low: 0.091%). This chart illustrates the text's claim that packet dropped percentage can spike well above 95% but typically resolves within ~15 minutes, visually confirming the formula-driven relationship where dropped packets dominate the delivered+dropped denominator during low-throughput periods.]

In this, plot the following 4 metrics. You will likely notice that the high spike is driven by low network throughput and high received packet dropped.

[Image: ## Image Description

The image displays four time-series charts spanning approximately **04:15 AM to 06:45 AM**, showing network metrics for a VM: **Total Packets Received** (H: 74,362 / L: 9,825), **Total Packets Transmitted** (H: 44,963 / L: 652), **Total Received Packets Dropped** (H: 968,475 / L: 30), and **Total Transmitted Packets Dropped** (H: 7 / L: 0). The data demonstrates the text's assertion that high packet drop percentages are driven by **disproportionately high received packet drops** (peaking near 1,000K at ~06:30 AM) relative to actual throughput, while transmitted drops remain negligible (max: 7). Two correlated spikes are visible around **05:00 AM and 06:00–06:30 AM** across all metrics, confirming the pattern of low throughput coinciding with massive received packet drops.]

Because of the above problem, profile your VM dropped packets, focusing on the transmit packets. The following is one way to do it, giving surprising results like this:

[Image: ## Image Description

This table displays **VM network transmit packet drop metrics** across 12 VMs, sorted by **Count of TX drop at 99th Percentile** (descending). The three columns show: percentage of all dropped packets at 99th percentile (ranging from **0.01% to 13.13%**, color-coded green/yellow/red), sum of total TX dropped packets (ranging from **687,848 to 12,406,013**), and the 99th percentile count of TX drops within any 300-second window (ranging from **604.77 to 4,050**).

The table reveals that **wv...** has the highest raw drop count (4,050) with a moderate 2.26% drop rate, while **SC...** shows the highest drop percentage (13.13%) but lower count (1,344), demonstrating that high absolute packet drops don't necessarily correlate with high drop percentages across different VMs.]

The design of the preceding table is:
- First column calculates the percentage packets dropped. I took 99th percentile else many of the results will be 100%.
- Second column sums all the transmitted dropped packets (actual packet counts).
- Third column takes the 99th percentile maximum of dropped packet within any 300 seconds. Each network packet is typically 1500 bytes. Using 1.5 KB packet size, 1 thousand packets dropped = 1500 MB worth of packets within 300 seconds.
I don’t expect dropped packets in data center network, so to see millions of dropped packets over a month needs further investigation with network team. Moreover, those metrics are Transmit, not Received. So the VM sent them but they got dropped. No one seem to complain, because packets are automatically retransmitted.
What I typically notice is the spike rarely happens. They look like an outlier, especially when the number is very high. The following is an example. I only showed in the last 1 month as the rest of the 6 months had similar pattern. The jump is well cover 100 million packets, and they were all dropped. Assuming each packet is 1 KB, since VCF Operations reports every 5 minutes, that’s 333 MB per second sustained for 300 seconds.

[Image: ## Image Description

The chart displays **Network|Total Transmitted Packets Dropped** and **Network|Total Packets Transmitted** metrics over a ~30-day period (Jan 22 – Feb 21). Two sharp, isolated spikes are visible — the highlighted spike on **Sunday, Jan 30 at 07:00 AM** shows **155,488,240 dropped packets** against only **21,274 total transmitted packets**, with a second similar spike around **Feb 14**. This demonstrates the "outlier" pattern described in the surrounding text — extremely rare but massive packet drop events (exceeding 150M packets) that stand out sharply against an otherwise near-zero baseline, consistent with the author's example of a potential false positive from NSX firewall rejections.]

I also notice regular, predictable pattern like this. This is worth discussing with network team. It’s around 3800 packets each 5-minute, so it’s worth finding out.

[Image: ## Image Description

The chart displays **Network Total Transmitted Packets Dropped** over a ~5.5-hour window (12:00 PM – 5:30 PM, Sunday Sep 12), showing a highly **regular, periodic spike pattern** occurring approximately every 30 minutes. A tooltip highlights a specific data point at **04:32:59 PM showing 3,813 dropped packets**, consistent with the surrounding text's observation of ~3,800 packets per 5-minute interval. The predictable, cyclical nature of the spikes (roughly uniform height and spacing) suggests a scheduled or recurring process is systematically generating packet drops rather than random network congestion.]

False positive on TX dropped packet because NSX firewall reject the outgoing packet. See this KB article.
Packet loss in Guest OS using VMXNET3: When using the VMXNET3 driver, you may see significant packet loss during periods of very high traffic bursts. The VM may even freeze entirely. This issue occurs when packets are dropped during high traffic bursts. This can occur due to a lack of receive and transmit buffer space or when receive traffic which is speed constrained.

### Consumption Metrics

There are 2 main metrics to measure utilization: throughput and packets.
Both metrics matter as you may still have bandwidth but unable to process that many packets per second. This outage shows 700K packets per second that only consumes 800 Mbps as the packet is small. The broadcast packet is only 60 bytes long, instead of the usual 1500 bytes.

[Image: The image shows a **forum/support post** describing a network outage caused by a VM misconfiguration in vSphere, where two vNICs were added to the same portgroup running Suricata IPS in AF_PACKETS mode. The misconfiguration resulted in **700K ARP broadcast packets per second** at approximately **100 Mbps bandwidth**, which propagated to a secondary site and overwhelmed network switches. This real-world incident illustrates the surrounding text's point that **packet rate (pps) can be a critical bottleneck independent of bandwidth consumption**, since small 60-byte broadcast packets can cause network failures even at relatively low throughput.]

The packets transmitted does not include those dropped packets. Another word, it only counts packets that were successfully transmitted.
The following diagram proves the above relationship.

[Image: ## Image Description

The chart displays two metrics for **esxmgmt-02a-vjvs** over a ~4-hour window (10:00 AM – 2:00 PM): **Total Packets Transmitted** (blue, ~1,409 at cursor) and **Total Transmitted Packets Dropped** (pink, ~1,350 at cursor), both measured in packets. The key observation is that the two lines **converge toward the end of the timeframe**, with dropped packets (~1,350) nearly equaling transmitted packets (~1,409), demonstrating that the "transmitted" counter only reflects **successfully sent packets** and excludes drops. This visually proves the book's stated relationship: total packets transmitted does **not** include dropped packets, as the two metrics track independently rather than one being a subset of the other.]

As a consequence, the packets transmitted per second = Total Packets Transmitted / 300 seconds.

[Image: ## Image Description

The chart displays **Network: Aggregate of all Instances | Packets Transmitted per second** over a time range from 8:00 AM to 12:00 PM on Monday, January 22. The metric starts at **7.62 packets/second** at 8:00 AM, drops significantly to a low of approximately **4.66** around 9:45–10:30 AM, then stabilizes at roughly **5.26 packets/second** by 10:35:47 AM (highlighted tooltip). This graph demonstrates the relationship between successfully transmitted packets (excluding dropped packets), visually correlating with the preceding explanation that packets transmitted per second equals total packets transmitted divided by the 300-second collection interval.]


## ESXi

In vSphere Client, you can’t see the virtual network traffic. The following shows that you can only see the physical network card.

[Image: This screenshot shows the **vSphere Client object selection interface** for a network chart, displaying available Target Objects for an ESXi host: one physical IP address (**10.217.66.45**) and four physical NIC adapters (**vmnic0, vmnic1, vmnic2, vmnic3**). The image demonstrates the surrounding text's point that vSphere Client only exposes **physical network cards (vmnics)** as selectable objects, with no virtual switch or port group objects available. This confirms that virtual network traffic metrics are not accessible through this interface.]

The metrics are provided at both physical NIC card and ESXi level. The counter at host level is basically the sum of all the vmnic instances. There could be small variance, which should be negligible.

[Image: ## Image Description

The image shows a vSphere Client metrics table displaying **network Usage (in KBps) for three objects**: two physical NICs (`vmnic0` and `vmnic1`) and one IP address (`10.217.66.45`), all using Average rollup. The data confirms the text's claim that vSphere Client only exposes **physical NIC-level metrics**, with `vmnic0` showing the lowest average (3.067 KBps, max 25) and `10.217.66.45` showing the highest average (16.556 KBps, max 164). This demonstrates that virtual network traffic is not visible at the Standard Switch or port group level, only at the physical vmnic layer.]

Just like vCenter, VCF Operations also does not provide the metrics at the Standard Switch and its port groups. This means you cannot aggregate or analyze the data from these network objects point of view. You need to look at the parent ESXi one by one. Create a dashboard with interaction to cycle through the ESXi hosts.

### Contention Metrics

In addition to the dropped packet, there are 2 other metrics tracking contention. They are error packets and unknown protocol frames.

#### Error Metrics


[Image: The image shows a table defining three network contention metrics in VCF Operations: **Packet receive errors**, **Packet transmit errors**, and **Unknown protocol frames**. All three use **Summation** aggregation with numeric (**num**) units, measuring error/unknown packets during the sampling interval. This table supports the surrounding text's discussion of contention metrics beyond dropped packets, establishing the definitions for the error and unknown protocol frame metrics that are expected to remain at **0** at all times.]

A packet is considered unknown if ESXi is unable to decode it and hence does not know what type of packet it is. You need to enable this metric in VCF Operations as it’s disabled by default.
Expect these error packets, unknown packets and dropped packets to be 0 at all times. The following shows from a single ESX:

[Image: The image shows a metrics table for the host **evn1-hs1-0804.eng.vmware.com** displaying five network error measurements: Packet receive errors, Packet transmit errors, Receive packets dropped, Transmit packets dropped, and Unknown protocol frames. All metrics use a Summation rollup in numeric units, with Latest, Maximum, Minimum, and Average values all showing **0** across the board. This demonstrates the ideal/expected healthy state referenced in the surrounding text, where all error, dropped, and unknown protocol frame counters should remain at zero at all times.]

To see from all your ESXi, use the view “vSphere \ ESXi Bad Network Packets”.

[Image: ## Image Description

This table displays network error metrics across multiple ESXi hosts, showing **Error Packets Received, Error Packets Transmitted, Received Packets Dropped, and Transmitted Packets Dropped** columns, with a summary row totaling **34,503 error packets received**. The data reveals that the top 12 hosts (mix of `10.144.117.*` and `w2-haas.*` entries, all **Dell Inc. PowerEdge R630**) show consistently high error RX values of **2,834–2,841**, while all other metrics across all hosts remain at **0** — except the summary row showing **1 received packet dropped** (highlighted in green). The red arrow annotation highlights the cluster of R630 hosts with elevated error packet counts, illustrating the point in the surrounding text that error packets are concentrated across specific hosts sharing the same hardware model.]

The hosts with error RX spans across different clusters, different hardware models and different ESXi build number. I can’t check if they belong to the same network.
If you see a value, drill down to see if there is any correlation with other types of packets. In the following example, I do not see any correlation.

[Image: The image shows four network metric charts for ESXi host **10.144.117.28** over a ~2-day period (Jun 25–27): **Total Error Packets Received** (H:156, L:0), **Total Broadcast Packets Received** (H:148,547, L:17,293), **Total Packets Received** (H:247,541, L:110,148), and **Total Multicast Packets Received** (H:9,950, L:7,517). Two vertical green markers highlight specific timestamps (~12:00 PM and ~6:00 PM on Jul 4) where error packet spikes occurred. The charts demonstrate that the error packet spikes show **no visible correlation** with corresponding anomalies in broadcast, total, or multicast packet counters, supporting the author's conclusion that error RX packets cannot be explained by other packet type behavior.]

What I see though, is a lot of irregular collection. I marked with red dots some of the data collection.

[Image: ## Image Description

The chart displays **Network | Total Error Packets Received** for host **10.144.117.28**, showing values over a ~19-hour period (4:00 AM to 11:00 PM), with a high of **156** and low of **0**. The metric shows two significant spikes around **1:00 PM (~120)** and **2:00 PM (~156, the peak)**, followed by a smaller rise around **5:00 PM (~85)**, with near-zero values for most of the monitored period. **Red dots** are marked at various irregular intervals across the timeline, visually demonstrating the **inconsistent/irregular data collection intervals** referenced in the surrounding text, contrasting with the regular collection behavior seen in the Error Packet Transmit counter.]

You can see they are irregular. Compare it with the Error Packet Transmit counter, which shows a regular collection.

[Image: ## Image Description

The image shows a time-series chart for device **10.144.117.28** displaying the metric **"Network|Total Error Packets Transmitted"** over a period from **4:00 AM to 11:00 PM**. The data line remains completely **flat at 0** throughout the entire timeframe, with High (H) and Low (L) values both recorded as **0**. In the context of the surrounding text, this chart serves as the **reference example of regular data collection** — contrasting with the irregular collection pattern shown in the previous chart (image409), demonstrating that the Error Packet Transmit counter collects data at consistent, evenly-spaced intervals across the full observation window.]


##### esxcli

The metrics at vCenter UI only shows the total. If you want to see the details, go to ESXi host console and issue an esxcli command.
The syntax is:
$ watch esxcli network nic stats get -n vmnic#
Take note:
- The counter is accumulative. That means the issue could have happened in the past.
See this KB for details. I’d copy the summary for convenience.
The error counters are:

| Total receive errors Total transmit errors | I think these 2 are what you see in the vCenter UI. It’s the summation of all the error below, including checksum error (which is not reported separately). |
| --- | --- |
| Total receive errors Total transmit errors | Based on this KB article, the csumerr counter, available inside the driver’s private statistics, cover the following: Layer 3, which is introduced by hardware issue (typically cabling), Layer 4, which cover Ingress packet has Layer4 checksum (packet is encapsulated, e.g. in vxlan or overlay), Receive packet rate on the vmnic is too high and the hardware is unable to perform the checksum calculations in timely manner. This traffic will be passed on to the ESXi for delivery to the VM/vmknic (which is expected to do it's own checksum validations), but this traffic will be declared as error. |
| Receive length errors | The actual size of the packet does not match with the size of the packet being reported via the packet header |
| Receive over errors | Count the packets that are discarded by the hardware buffer of the card. This includes CRC error. |
| Receive CRC errors | The CRC value calculated by receiving ESXi does not match the value in the FCS field.  If you’re unfamiliar with CRC, see this. |
| Receive frame errors |  |
| Receive FIFO errors Transmit FIFO errors | The physical network card unable to process due to RX ring buffe size is full |
| Receive missed errors | The physical network card unable to store or process packets due to hardware limitations |
| Transmit aborted errors |  |
| Transmit carrier errors |  |
| Transmit heartbeat errors |  |
| Transmit window errors |  |


#### Dropped Packet


[Image: The image shows a two-row metrics table defining **dropped packet counters** at the ESXi physical layer, listing **"Receive packets dropped"** and **"Transmit packets dropped"**, both using **Summation** aggregation with a **num** (numeric) unit type. These metrics track the number of inbound and outbound packets dropped before reaching the ESXi kernel. In context, this table contrasts with VM-level dropped packets, representing physical NIC-layer drops that may aggregate values from multiple underlying hardware counters per VMware KB guidance.]

You’ve seen the dropped packet situation at VM. That’s a virtual layer, above the ESXi. What do you expect to see at ESXi layer, as it’s physically cabled to the physical top of rack switches? The counter tracks packets that are dropped prior to the packet reaching the ESXi kernel. According to this KB, “quite often this counter is a combination of the values from other counters that can be found in the Private Statistics section of the nicinfo.sh.txt file that is contained in the commands directory of ESXi host log bundles.”
I plotted 319 production ESXi hosts, and here is what I got for Transmit. What do you think?

[Image: ## Image Description

This is a tabular dashboard showing **transmit (TX) packet drop metrics** for 319 production ESXi hosts, displaying Max TX Dropped, 99th Percentile TX Dropped, Average TX throughput, and Peak TX throughput for the top 10 entries. The Max TX Dropped values range from **12 to 362 packets** (highlighted in orange/red), while the **99th percentile column shows 0 across all rows**, confirming drops are statistically negligible. The summary row shows an aggregate average of **0.29 Gbps** with a peak of **6.67 Gbps**, demonstrating that while occasional TX drops occur, they are extremely rare outliers in normal ESXi NIC operation.]

There are packet drops, although they are very minimal. Among 319 hosts, one has 362 dropped transmit packet in the last 3 months. That host was doing 0.6 Gbps on average and peaked at 8.38 Gbps.
As expected, the dropped packet rarely happened. At 99th percentile, the value is perfectly 0.
I tested with another set of ESXi hosts. Out of 123 servers, none of them has any dropped TX packet in the last 6 months. That’s in line with my expectation. However, a few of them experienced rather high dropped RX packets.

[Image: ## Image Description

This table displays **network packet drop metrics** for multiple ESXi hosts (truncated names beginning with "wdc-0..." and "wdc-it..."), showing **Received Packets Dropped** (sorted descending) and **Transmitted Packets Dropped** columns. The top three hosts show significantly high RX drop counts of **2,574,166**, **1,945,080**, and **935,837**, while the remaining hosts show dramatically lower values (50,356 down to 550). Notably, **Transmitted Packets Dropped is 0 across all hosts**, confirming the surrounding text's assertion that TX drops are rare/nonexistent while RX drops are the primary concern requiring investigation.]


[Image: ## Image Description

The chart displays **Network | Total Received Packets Dropped** for a single ESXi host over approximately two months (June 24 – August 21). The metric shows **sporadic spikes** with a peak high (H) of **1,030 dropped packets**, while the low (L) remains at **0**, indicating the drops are intermittent rather than continuous. The pattern aligns with the surrounding text's observation that dropped RX packets began occurring only after the ESXi host experienced increased load, with notable spikes visible around **July 26** and **August 3-4**.]

The dropped only happened since the ESXi had an increased load

[Image: ## Image Description

This chart displays **Network Data Receive Rate (Gbps)** over approximately two months (late June through August 21). The metric shows a **dramatic and sustained increase around July 25-26**, where the baseline jumps from near **0 Gbps to consistently 5-10 Gbps**, with a highlighted peak of **H: 13.99 Gbps** marked around August 7. This visual directly supports the surrounding text's claim that "dropped [packets] only happened since the ESXi had an increased load," as the sharp inflection point clearly correlates increased network receive throughput with the onset of the problematic behavior.]

If you see something like this, you should investigate which physical NIC card is dropping packet, and which VMK interface is experiencing it.
While the number is very low, many hosts have packet drops, so my take is I should discuss with network team as I expect data center network should be free of dropped packets.

##### Received

What do you think you will see for Received?
Remember how VM RX is much worse than VM TX? Here is what I got:

[Image: ## Image Description

This is a network metrics dashboard table showing **ESXi host RX (receive) packet drop statistics** across 319 hosts, displaying the top 10 worst performers. The data reveals severe packet drop issues, with the top host showing **7,415,656 Max RX Dropped** packets, and several hosts showing high 99th percentile values (e.g., 2,121,175.76 and 1,424,756.4), indicating **sustained/recurring drops** rather than isolated spikes. Critically, **Max TX Dropped is 0 for all individual hosts** (summary shows only 2.24), confirming the packet loss problem is exclusively on the **receive path**, mirroring the VM-level RX degradation described in the surrounding text.]

Surprisingly, the situation is the same for ESXi.
Some of them have >1 million packet dropped in 5 minute. Within these set of ESXi, some have regular packet dropped, as the value at 99th percentile is still very high. Notice none of the ESXi is dropping any TX packet.
I plotted the 2nd ESXi from the table, as it has high value at 99th percentile. As expected, it has sustained packet dropped lasting 24 hours. I marked the highest packet drop time, as it mapped to the lowest packets received.

[Image: ## Image Description

The image displays two time-series charts spanning **Sep 23–25** for an ESXi host: **Network|Total Received Packets Dropped** (top, peaking at **H: 5,633,351** with a sustained elevated baseline of ~5M for approximately 24 hours starting Sep 24) and **Network|Data Receive Rate (KBps)** (bottom, ranging **L: 16,945.2 to H: 104,531.87**). Red and orange annotation markers highlight the peak packet drop event (~06:00 AM Sep 24), which correlates with the **lowest point in the data receive rate**, visually confirming the inverse relationship between dropped packets and received throughput. This demonstrates the sustained RX packet dropping behavior described in the text, where the 99th percentile remains critically high and the drop period aligns precisely with reduced incoming network data.]


##### vsish

vsish provides more information that is not available in vSphere Client UI and VCF Operations.
vsish -e get /net/portsets/DvsPortset-0/ports/67109026/clientStats
port client stats {
pktsTxOK:154121
bytesTxOK:63326625
droppedTx:0
pktsTsoTxOK:0
bytesTsoTxOK:0
droppedTsoTx:0
pktsSwTsoTx:0
droppedSwTsoTx:0
pktsZerocopyTxOK:45817
droppedTxExceedMTU:0
pktsRxOK:339700
bytesRxOK:257901191
droppedRx:2620  the reason will appear on the next output below
pktsSwTsoRx:0
droppedSwTsoRx:0
actions:0
uplinkRxPkts:0
clonedRxPkts:0
pksBilled:0
droppedRxDueToPageAbsent:0
droppedTxDueToPageAbsent:0
}
We saw dropped packets, so we probe deeper for the reason
vsish -e get /net/portsets/DvsPortset-0/ports/67109026/vmxnet3/rxSummary
stats of a vmxnet3 vNIC rx queue {
LRO pkts rx ok:0
LRO bytes rx ok:0
pkts rx ok:340093
bytes rx ok:257984247
unicast pkts rx ok:253678
unicast bytes rx ok:245663220
multicast pkts rx ok:42220
multicast bytes rx ok:7497292
broadcast pkts rx ok:44195
broadcast bytes rx ok:4823735
running out of buffers:2620    the reason for 2620 packets dropped
pkts receive error:0
1st ring size:512
2nd ring size:512   the ring size is on the small side. I’d say set to 2K.
# of times the 1st ring is full:354    this line shows the first ring is full 354x
# of times the 2nd ring is full:0
fail to map a rx buffer:0        other reasons look good
request to page in a buffer:0
# of times rx queue is stopped:0      other reasons look good
failed when copying into the guest buffer:0     other reasons look good
# of pkts dropped due to large hdrs:0
# of pkts dropped due to max number of SG limits:0
pkts rx via data ring ok:0
bytes rx via data ring ok:0
Whether rx burst queuing is enabled:0
current backend burst queue length:0
maximum backend burst queue length so far:0
aggregate number of times packets are requeued:0
aggregate number of times packets are dropped by PktAgingList:0
# of pkts dropped due to large inner (encap) hdrs:0
number of times packets are dropped by burst queue:0
number of times packets are dropped by rx try lock queueing:0
number of packets delivered by burst queue:0
number of packets dropped by packet steering:0
number of memory region lookup pass in Rx.:0
number of packets dropped due to pkt length exceeds vNic mtu:0
number of packets dropped due to pkt truncation:0
}
Networking VMs, such as firewall and routers, or any high VMs expecting high packet rates, check if the VM is requesting NetQ RSS.

### Consumption Metrics

As expected, you get the 2 types of throughput:
- bits/second
- packets/second.
For bits/second, the metrics are:

[Image: The table displays five VMware vSphere network consumption metrics, all using **Average rollup** and **KBps units**. It shows duplicate entries for both **Data receive rate** and **Data transmit rate** (with slightly different descriptions), plus a **Usage** metric defined as combined transmit and receive rates (full duplex aggregation). This table contextualizes the author's noted confusion about duplicate metrics, illustrating that vSphere exposes redundant counters for the same network throughput measurements.]

I’m unsure why there are duplicates metrics.
We covered earlier that full duplex means the aggregated metric can exceed the physical speed. Notice the Usage Rate is the sum of Receive and Transmit on the following screenshot.

[Image: ## Image Description

The screenshot displays three network metrics for IP **10.119.161.127** over a ~12-hour period (11:00 PM Nov 15 – 12:00 PM Nov 16): **Data Receive Rate** (peak 0.99 Gbps, baseline ~0.0397 Gbps), **Data Transmit Rate** (peak 0.53 Gbps, baseline ~0.0513 Gbps), and **Network Usage Rate** (peak 1.25 Gbps, baseline ~0.092 Gbps). The charts demonstrate the author's point that **Usage Rate equals the sum of Receive + Transmit** (0.99 + 0.53 ≈ 1.25 Gbps at peak), confirming full-duplex aggregation behavior. All three metrics share identical spike patterns, with major bursts around 1:00 AM and a secondary spike near 10:30 AM.]

You can also plot each vmnic one by one. Since you may not know which one to plot for a given ESXi, you can show them all in table first.

[Image: This table displays **TX (Transmit) and RX (Receive) rates in Gbps for six vmnics (vmnic0–vmnic5)** on ESXi host **10.119.161.131**. Most vmnics show 0 Gbps activity, with **vmnic2 showing minimal traffic (TX: 0.03 Gbps, RX: 0.01 Gbps)** and **vmnic3 carrying the bulk of traffic (TX: 0.67 Gbps, RX: 0.48 Gbps)**. This screenshot demonstrates the recommended approach of displaying all vmnics in a table view to quickly identify which physical NICs are actively carrying traffic before drilling down into individual vmnic metrics.]

For packets/second, the metrics are:

[Image: The image shows a metrics table defining two network packet counters: **Packets received** and **Packets transmitted**, both using **Summation** aggregation and **num** (numeric) units. These metrics track the number of packets received and transmitted during a given interval. In context, this table introduces the packet-per-second metrics for ESXi network interfaces, which the surrounding text notes can be divided by bits/second to calculate average packet size.]

It’s interesting to divide the packet/second with the bits/second, as you get the packet size. If this number change drastically in large environment, it’s something worth investigating.

#### Unusual Packets


[Image: The image displays a table of **four network metrics** related to unusual/non-unicast packet traffic, all using **Summation** aggregation and **num** (numeric) units. The metrics cover **Broadcast Receives, Broadcast Transmits, Multicast Receives, and Multicast Transmits**, each measuring the count of their respective packet types during a sampling interval. In context, these metrics are used to monitor and verify that broadcast and multicast traffic remains within expected thresholds on both VMs and ESXi hosts.]

Your VM network should be mostly unicast traffic. So check that broadcast and multicast are within your expectation. Your ESXi Hosts should also have minimal broadcast and multicast packets.

[Image: ## Network Unusual Packets Chart

This VMware vSphere performance chart displays **broadcast and multicast packet metrics** for a VM over a 1-hour real-time window (09/27/2021, 1:58–2:58 PM), showing four summation metrics in num units. **Broadcast receives** (blue) dominates with an average of **1,197.928** and peaks reaching **2,310**, while **Multicast receives** (green) averages **228.933** with a max of **839**; both **Broadcast transmits** (black, avg 35.15) and **Multicast transmits** (orange, avg 7.033) remain near-zero by comparison. This illustrates the book's guidance that VM network traffic should be predominantly unicast — the relatively elevated broadcast/multicast receive counts shown here represent the type of anomalous non-unicast traffic administrators should investigate.]

Chapter 6

# Consumer


## Performance: VM

This section covers metrics that cut across the 4 elements of infrastructure, or metrics that are outside these 4 elements.

### VM Performance (%)

With so many metrics, how do you monitor at scale? Say you have 5000 VMs, and you want to monitor every 5 minutes and see the performance trend in the last 24 hours. That would be far too many trend charts.
Enter Performance (%) metric.
Now that we’ve mastered the raw metrics, we’re in the position to combine them to answer complex question. When we combine, we need to be mindful of which persona needs this summary metric. The answer is VM Owner. The metric is not designed for infrastructure team.
The following diagram put together all the metrics from Guest OS and VM. VM KPI includes Guest OS metrics as operationally we troubleshoot them as one, due to their 1:1 relationship.
For completeness, I added the utilization metrics to act as leading indicators.

[Image: ## Image Description

This table categorizes VMware vSphere performance metrics across four resource domains (**CPU, RAM, Network, Disk**) split into two monitoring perspectives: **Inside Guest OS** (requiring VMware Tools, applicable to Linux/Windows) and **Outside Guest OS** (hypervisor-level, invisible to the guest). Key metrics highlighted in **red** indicate critical KPIs — notably **CPU Utilization**, **OS Output Queue Length**, **Driver Queue**, **Throughput (Mbps)**, **Latency** (Network), and **Latency** (Disk). 

In context, this diagram supports the surrounding text's explanation of constructing **VM KPI metrics** by combining Guest OS and hypervisor-layer metrics, with red highlighting identifying the leading indicator/utilization metrics referenced in the preceding paragraph. The Outside Guest OS row captures contention metrics (e.g., **Ready + Co-Stop + Overlap, IO Wait + Swap Wait**) that the guest OS cannot observe or control, explaining why multiple metrics per resource are required rather than a single combined value.]


#### Metric Used

Here is what I recommend, including their threshold.

[Image: ## Image Description

This table presents **VM and Guest OS performance metric thresholds** organized across four severity tiers (Green/Yellow/Orange/Red) for 13 distinct metrics spanning five layers: **Guest OS Contention, Guest OS Utilization, VM Contention, VM Utilization, and IaaS High Utilization**. Key metrics include CPU Queue Length (Green: 0–4, Red: 16–32), Peak CPU Ready (Green: 0–2%, Red: 8–16%), Peak Read/Write Latency (Green: 0–10ms, Red: 40–80ms), and Free Memory (Green: 512–1024MB, Red: 0–128MB). The table serves as the recommended **KPI threshold reference** referenced in the surrounding text, consolidating Guest OS and VM metrics into a unified scoring framework for VM Owner persona consumption.]

Q: Why do we use 4 metrics for CPU instead of 1? Wouldn’t that quadruple their share?
A: Yes, it will. This is a known limitation. We cannot combine them into a single metric as they don’t peak at the same time within the 20-sec period.
Q: Why do the 4 components of CPU contention have different threshold since their impact is the same?
A: They have different level of sensitivity. The gap is sizable. To standardize will result in compromise. For example, Ready tends to have 2x the value of Co-Stop.
We can only add a metric in the table if it can be quantified into the 4 brackets. If a metric cannot be bucketized, it could do a disservice to the KPI. Hence majority of utilization metrics (e.g. disk IOPS, network throughput) are not here. I do not recommend you add them as they can mask out the real problem.

| Guest OS | Guest OS metrics are included as they do not have VM equivalent, and they change the course of troubleshooting. |
| --- | --- |
| Guest OS | CPU run queue is set to higher than normal to reduce false positive. |
| VM CPU | The complete set of CPU contention is provided. There are 4 metrics tracking the different type of contention or wait that CPU experiences. |
| VM CPU | Do you know why we use CPU Net Run as opposed to CPU Usage? Read the VM CPU Metrics section. Theoretically, we should have chosen a higher threshold for CPU utilization. Practically, it’s rare the CPU Run goes to 95% as CPU Used would have reached the VM CPU capacity. I set 60% as the starting line so there is no penalty for utilization below 60%. |
| VM Memory | Memory Contention is the only counter tracking if the VM has memory problem. VM and Guest OS can have memory problem independently.  In future, we should add Guest OS memory performance metrics, if we find a good one. Linux and Windows do not track memory latency, only track memory disk space consumption, throughput and IOPS. These 2 OSes do not track latency, which unfortunately is the main counter for performance. |
| VM Memory | Memory Ballooned, Swapped, Compressed are added even though their presence does not indicate real performance as they are leading indicators. That’s why their threshold is higher than memory contention. |
| VM Memory | Swapped and Compressed are combined as they are the result of the same action. Together they tell the complete picture. As they may not indicate actual problem, their threshold is 2x of memory contention |
| Network | vCenter does not have latency and re-transmit. So we have to resort to dropped packet metric. |
| Network | The threshold is not low as dropped packets are automatically restranmitted. Practically, this means the application team may not notice it. |
| Network | Take note of known limitation. While the packet dropped is based on the peak 20-second, the packet transmitted is based on the average of the collection period. The reason is we don’t know which data points to take among the 15 data points in the default collection period. |

With so many metrics, it can get difficult to debug. Also, the number will tend to be high as a single number will not have enough weightage to bring down. These are 2 things you can do:
- Combine the 4 VM CPU contention into a single metric. The drawback is there is possibility that the 4 peak values happened at different time within the 5 minute window.
- Split the table into 2 and take the lowest. There are 2 ways, both have their pro’s and con’s.
- Approach 1 is by layer. Table 1 is for Guest OS (4 metrics), while Table 2 is for the rest (7 metrics).
- Approach 2 is by importance. Move less important metrics to Table 2.

#### Metrics Not Used

What metrics are missing from the tables?
Most utilization, such as disk IOPS, are excluded as we can map their values to the 4 brackets. There is no univeral mapping that works for all VMs.
The following metrics are not included, along with the reason why:

| Guest OS : VM Ratio | Guest OS IOPS : VM IOPS Ratio. They should be near 1 or a stable number, as the block size should be identical. The actual numbers may not match, as Guest OS tends to report the last value, while VM tends to report average value. If they fluctuate greatly, something amiss. I do not include as I do not have the data yet. |
| --- | --- |
| Guest OS | CPU Context Switch is not included as the profiling shows this metrics has a very wide band, making it impractical. |
| Guest OS | Memory page-in could contain Windows or Linux application binary, so its value could be over reported. Based on our profiling of 3300 production VM, the page-in is more volatile so I’m less confident of applying a threshold |
| Guest OS | Guest OS swap file remaining free capacity is not included as I’m not sure if low value impacts performance |
| Guest OS | Number of dead processes is not included as I’m not sure what value to set for each bracket. We need to profile Windows and Linux separately |
| Memory | Popular VM metrics such as Consumed, Active, Granted, etc are not shown as they do not indicate performance problem |
| Memory | RAM Page Fault is not included as we do not have the metric. |
| Memory | Swapped File Remaining is not included as it may corelate with available memory? |
| Memory | Memory page-in is not included as it contains proactive fetch |
| Storage | Adding Disk Outstanding IO will be duplicating as it’s a function of IOPS x latency |
| Storage | Snapshot latency is excluded as the metric VM Other Wait already covers it, so no need to double count |
| Network | Network packets, such as broadcast and multicast, are not desirable. However, they do not actually cause performance. |
| Network | Error packets are excluded as Tools do not have it. |
| Network | Network queue is excluded as no such metric. |
| Network | RX Dropped Packets is excluded as too many false positive. |
| Network | Packets per second is excluded as we can’t quantify the 100%. |
| VM DRS Score | Niels Hagoort states here that “a VM running a lower score is not necessarily not running properly. It is about the execution efficiency, taking all the metrics/costs into consideration.” Reading the blog and other material, this metric is more about the cluster performance than the individual VM performance. Plus, it’s using metrics that are already included in the KPI, so it’s double counting |
| vMotion | I do not have enough data to decide the value to put for each range of either downtime or stun time. It should be within 0.2 second for green, but what about yellow?  Typically, I used 2K – 4K VMs over 3 months to convince myself that the thresholds are representing real world. Use Log Insight to profile this. |
| CPU Other Wait | Too many counters for CPU, which incorrectly inflates the importance of CPU factor. Plus, there is a rare bug which results in false positive. |

Notice all of them are VM or Guest OS metrics. No ESXi, Resource Pool, Datastore, Cluster, etc metrics. Why?
The reason is the metrics at these “higher-level” objects are mathematically an average of the VMs in the object. A datastore with 10 ms disk latency represents a normalized/weighted average of all the VMs in the datastore. Another word, these metrics give less visibility than the 12 above, and they can be calculated from the 12.
And 1 more reason: You troubleshoot VM, not infrastructure. If there is no VM, there is no problem 😊

#### 20-second Peak Metrics

VCF Operations collects and stores data every 5 minutes. This is good enough for monitoring use case, but not for troubleshooting. 300-second average is not granular enough, as performance problem may not be sustained that long. Even a performance issue that last days may consist of repeated microbursts. I check if repeated bursts exist by profiling a few thousand VMs. Here are some of the results. I compare 3 metrics (disk latency, network throughput and CPU context switch).

[Image: The image displays a three-panel table comparing **300-second average metrics vs. 20-second peak metrics** across three dimensions: Disk Latency (ranging from 0–35.74 ms average vs. 102–272 ms peak), Network Usage (7.84–9,192.6 Mbps average vs. 50.59–18,636.24 Mbps peak), and CPU Context Switch (5,632–35,597 average vs. 20,752–38,560 peak). The data is sorted descending by peak latency, with disk latency showing the most dramatic disparity — averages as low as 0 ms while peaks reach 272 ms. This demonstrates the core argument that 300-second averages significantly **underrepresent microburst severity**, with peak values consistently and substantially worse than the averages across all three metrics.]

The peak column is based on 20-second average. So it’s 15x sharper than the 300-second average. It gives better visibility into the microbursts. If the burst exists, you will see something like this, where the 20-second shows much worse value consistently.

[Image: ## Image Description

The chart displays two Virtual Disk latency metrics over a ~24-hour period (May 9–10): **Peak Latency within collection cycle (20-second, purple)** reaching **10,370 ms** at 2:47 PM, and **Aggregate Total Latency (300-second average, pink)** showing only **257.53 ms** at the same timestamp. The purple peak metric shows repeated sharp spikes throughout the day (many exceeding 2,500–7,500 ms), while the pink average line remains nearly flat near zero. This dramatic disparity (~40x difference rather than the expected 15x) visually demonstrates how short-duration microbursts are masked by longer collection intervals, with the 20-second granularity exposing extreme latency events that the 5-minute average effectively hides.]

Are you surprised to see that the 20-second peak is a lot worse than 15x worse? The preceding chart shows 10370 ms latency at 20-second vs 257 ms at 300 second.
The huge gap is due to 2 things
- There is only 1 or 2 microbursts, and it’s much higher than the average. This can happen on counter such as disk latency and CPU context switch, where the value can be astronomically high.
- There are many sets. A VM can have many disks. For example, a database VM with 20 virtual disks will have 40 sets of metrics. Each set has 15 datapoints, giving a total of 600 metrics. The peak is reporting the highest of 600 metrics. If the remaining is much lower, then the gap will naturally be high.

##### How are they chosen?

Take a look at the table below. It shows a VM with 2 virtual disks. Each disk has its own read latency and write latency, giving us a total of 4 metrics.

[Image: ## Image Description

The table displays disk latency metrics for a single VM with two virtual disks (Disk 1 and Disk 2), each tracked for both read and write latency across 15 datapoints collected over 5 minutes (20-second intervals). Notable values include a **100 ms peak read latency spike on Disk 1** at the 40-60 second interval, while other measurements range from 1-51 ms, with the VM-level summary showing an **average of 25 ms** and a **peak of 100 ms**. The table demonstrates how peak values can be significantly misleading compared to averages — the 100 ms peak is 4× the 25 ms average — illustrating the core problem the surrounding text describes about peak metrics being skewed by isolated spikes across multiple disks and datapoints.]

What VCF Operations 8.3 does is to add a new metric. It does not change the existing metric, because both have their own purpose. The 5-minute average is better for your SLA and performance guarantee claim. If you guarantee 10 ms disk latency for every single IOPS, you’d be hard pressed to deliver that service. These new metrics act as early warning. It’s an internal threshold that you use to monitor if your 5-minute SLA is on the way to be breached.
VCF Operations 8.3 takes the peak of these 15 data points, and stores them every 5 minutes. It does not store all 15 data points, because that will create a lot more IOPS and consume more storage. It answers the question “Does the VM or Guest OS experience any performance problem in any 20-second period?”
Having all 20-second data points are more natural to us, as we’re used to 1 second in Windows and 20 second in vCenter performance charts. But how does that additional 14 data points change the end remediation action? If the action you take to troubleshoot is the same (e.g. adjust the VM size), why pay the price of storing 15x more data points?
In the case of virtual disk (as opposed to say memory), a VM can have many of them. A database VM with 20 virtual disks will have 40 peak metrics. That also means you need to check each one by one. So VCF Operations 8.3 takes the peak among all virtual disks read and write. It does the same thing with vCPU. A monster VM with 64 vCPU will only have 1 metric, but this metric is the highest among 64 virtual CPU. There is no need to have visibility into each vCPU as the remediation action is the same. Whether it’s vCPU 7 or vCPU 63 that has the problem, it does not change the conclusion of troubleshooting in most cases.

|  | 5-minute Average | 20-second Average |
| --- | --- | --- |
| Guest OS | CPU Run Queue | Peak CPU Queue within collection cycle |
| Guest OS | CPU Context Switch | Peak CPU Context Switch within collection cycle |
| Guest OS | Memory Page-out Rate | Peak Guest OS Page-out Rate within collection cycle |
| Guest OS | Disk Queue Length | Peak Disk Queue within collection cycle |
| VM CPU | Ready (%) | Peak vCPU Ready within collection cycle |
| VM CPU | Co-Stop (%) | Peak vCPU Co-Stop within collection cycle |
| VM CPU | Other Wait (%) | Peak Other Wait within collection cycle |
| VM CPU | Overlap (second) | Peak vCPU Overlap within collection cycle |
| VM Memory | Contention (%) | Peak Memory Contention within collection cycle |
| VM Disk | Read Latency (ms) | Peak Latency within collection cycle |
| VM Disk | Write Latency (ms) | Peak Latency within collection cycle |
| VM Network | Usage Rate (KB/s) | Peak Usage Rate within collection cycle |
| VM Network | Packet/sec | Peak Network Packets/sec within collection cycle |
| VM Network | Transmitted Packet Dropped | Peak Transmitted Packet Dropped within collection cycle |

What’s the limitation?
- You can’t see a pattern within the 300 seconds window as you only have 1 data point. This is largely mitigated by having the average counter also. If the delta between the maximum and average is high that means the maximum is likely a one-off occurrence. The pattern can also be seen over longer period of time.
- The peak can be from a different 20-second block. That means you can’t associate that the contention is caused by high utilization as the 2 metrics can come from different 20-second block within that 5-minute time period.

#### Implementation

The following shows the part of the formula where we label the metrics used. Label is handy to shorten the overall length while improving readability.
It shows the 12 metrics used.

[Image: ## Image Description

This image shows a **vRealize Operations (vROps) formula snippet** using the `sum()` function that assigns alias labels to **14 VM performance metrics** spanning CPU, memory, disk, and network categories. The metrics include 20-second peak values (e.g., `cpu|20_sec_peak_readyPct` as `Ready`, `mem|20_sec_peak_host_contentionPct` as `mLatc`) alongside latest-value metrics (e.g., `guest|mem.free_latest` as `mFree / 1024`). The image demonstrates the labeling/aliasing technique used to shorten metric references in a composite formula, with the notable observation that `mFree` requires a `/1024` conversion (KB→MB) applied **outside** the label assignment.]

I copied into an external editor to show each metric as 1 line so you can see them more easily.
Free memory measures the disk space. It’s more important to see the latest value. Average of last 5 minutes is better than lowest 20-second period within that 5 minute period.
I’ve rearranged the metrics so you can see the 20 second peak metrics first.
Guest OS Free Memory is in KB, so we need to divide by 1024. Note the division can’t be part of the label.
There is no metric that sums the VM zipped page and swapped page, so I created a super metric for it.

##### The Green Range

See the concept of the 4 ranges in the Performance Modelling section of Chapter 1.
To see the threshold more easily, I rearranged the metrics from the smallest threshold, and have skipped the metrics with special logic. They will be covered later.

[Image: ## Image Description

The image displays a **scoring formula table** for 12 VM performance metrics, each following the pattern: `metric < threshold ? (100 - (metric / threshold * 25))`. Metrics include network/storage indicators (**netTXd, Overlap, mLatc, ZipSwap, cpuQ, coStop, oWait, Ready, Balloon, dLatc, DiskQ, PageO**) with thresholds ranging from **0.25 to 1000**, ordered by ascending threshold value. The formulas implement a **green range prorating logic** that converts raw metric values into scores between **75–100 points** when the metric falls below its defined threshold, as explained in the surrounding text.]

Let’s go through the first line. It checks if network TX dropped is below 0.25%, it will prorate the value to a number between 75% and 100%. To prorate, we do this logic:
- Divide the value with the green range size to get the fraction.
- Multiply the result by 25 to adjust the scale to 25 points.
- Subtract the result from 100 (perfect score), the starting line for green.
BTW, I didn’t add the * 1 weightage multiplier for green at the end to keep the formula simpler. Mathematically it’s not required.
Now let’s look at CPU Run, as it’s a special case.

[Image: ## Image Description

The image displays a **conditional scoring formula** for the **CPU Run metric**: `Run < 80 ? (100 - (max([Run - 60, 0]) / 20 * 25))`. This formula demonstrates the special-case handling where the green range is **60%–80%** (not 0–80%), using a `max()` function to prevent negative values when Run is below 60%, which returns a perfect score of **100**. The formula prorates scores between **75–100** for values within the 60–80% green band by dividing by the range size (20) and scaling to 25 points.]

The range of green is 60% – 80%, not 0 – 80. This means utilization below 60% is given a perfect score of 100%.
Why do we take the maximum of Run – 60 and 0? To ensure we don’t have negative value when the CPU Net Run metric is below 60%. This max() function will return 0, hence giving us 100 – 0 = 100%.
Now let’s look Guest OS Free Memory.

[Image: ## Image Description

This image shows a **conditional formula for calculating a green-range score for Guest OS Free Memory**, written in a ternary/inline conditional syntax. The formula evaluates whether `mFree/1024 > 512` (i.e., free memory exceeds 512 MB), and if true, calculates `min([mFree/1024 - 512, 512]) / 512 * 25 + 75`, which maps excess free memory above 512 MB to a **score range of 75–100%**. The `min()` function caps the value at 512 MB of headroom, while the `+75` offset anchors the minimum score at 75% when the condition is met.]

This one is special as the threshold is going descending. We also need to convert the unit from KB to MB.
We want the value of free memory > 512 MB of RAM to translate into 100%. Since the formula returns 0% - 25%, I had to add 75.

##### The Yellow Range

When the metric value does not within green threshold, it gets evaluated for yellow.
The outcome is 50% - 75%, hence the formula deducts from 75.
Just like the green range, let’s start with the easy ones. You notice the following looks similar to the green range.

[Image: The image displays a series of conditional (ternary-style) scoring formulas for **12 VMware vSphere performance metrics**: `netTXd`, `Overlap`, `mLatc`, `ZipSwap`, `cpuQ`, `coStop`, `oWait`, `Ready`, `Balloon`, `dLatc`, `DiskQ`, and `PageO`. Each formula evaluates whether a metric falls within the **yellow threshold range** (returning a score between 50–75%), using the pattern: `metric < [upper_threshold] ? (75 - ((metric - [lower_threshold]) / [range_size] * 25)) * 2`. The thresholds vary by metric (e.g., `netTXd < 0.5`, `DiskQ < 40`, `PageO < 2000`), with a **2x weightage multiplier** applied to all yellow-range calculations, distinguishing them from the green range formulas.]

Let’s go through the first line. It checks if network TX dropped is below 0.5%, as it’s definitely above 0.25%.
It then prorates the value to a number between 50% and 75%. To prorate, it applies a logic similar to the green range.
- Divide the value with the yellow range size to get the fraction.
- Multiply the result by 25 to adjust the scale to 25 points.
- Subtract the result from 75, the starting line for yellow.
The * 2 at the end is the weightage multiplier. Green is given a 1x weightage, while yellow is 2x, orange is 4x and red is 8x. The value is amplified, and then normalized again at a later portion (not shown in the screenshot).
As we’re not dealing with the edge of the range, the next 2 metrics have simpler logic.
For CPU Run, the logic becomes consistent with the simpler metrics. Just need to map 80% - 90% Run value to 75% - 50% range.

[Image: ## Image Description

The image shows a **conditional formula for CPU Run metric in the yellow range (80%–90%)**, expressed as:

`Run < 90 ? ( 75 - ((Run - 80)/10 * 25) ) * 2`

This maps CPU Run values between **80%–90% to a score range of 75%–50%**, where `(Run - 80)/10` normalizes the position within the range, multiplied by 25 to span the 25-point interval, subtracted from 75 (the yellow range starting point). The `* 2` applies the **2x weightage multiplier** for the yellow band, which will later be normalized alongside other weighted scores.]

For Memory Free, we have to keep on dividing by 1024.

[Image: ## Image Description

This image shows a **conditional formula for calculating a Memory Free metric score** in the yellow range. The formula maps memory free values between **256 MB and 512 MB** (i.e., `mFree/1024 > 256`) to a normalized score using the expression `((mFree/1024 - 256)/256 * 25 + 50) * 2`, which scales the metric into a specific percentage range. The `* 2` multiplier at the end reflects the **2x yellow range weightage** mentioned in the preceding text.]


##### The Orange Range and Red Range

I’m showing them together as it’s an IF THEN ELSE. Whatever not caught by the orange is handled by red.

[Image: ## Image Description

The image displays a table of **conditional scoring formulas** for 12 VMware vSphere performance metrics (netTXd, Overlap, mLatc, ZipSwap, cpuQ, coStop, oWait, Ready, Balloon, dLatc, DiskQ, PageO), each using an **IF-THEN-ELSE structure** to map raw metric values into health scores across orange and red ranges. Each formula follows the pattern: `metric < threshold ? (50 - ((metric - offset) / offset*25))*4 : (25 - (min([metric - threshold, threshold]) / threshold*25))*8`, with thresholds scaling from **1 (netTXd) to 4000 (PageO)**. This demonstrates the dual-range scoring logic where the orange range maps to **50–25%** scores (multiplier ×4) and the red range maps to **25–0%** scores (multiplier ×8), with `min()` clamping extreme values to prevent negative scores.]

What do you notice in the red range?
It has a min() function. This is to guard against a very large value. For example, in CPU Ready, any value above 8% will be given a score of 0%, not negative.
The formula for CPU Run becomes simpler as it cannot go above 100. We do not need to do the min() function for the red range.

[Image: ## Image Description

This image displays a **conditional formula (ternary expression)** for calculating a performance score based on a metric called **"Run"**, split into two ranges:

- **Orange range** (Run < 95): `(50 - ((Run - 90) / 5 * 25)) * 4`
- **Red range** (Run ≥ 95): `(25 - ((Run - 95) / 5 * 25)) * 8`

The formula demonstrates the IF-THEN-ELSE scoring logic where the orange range is capped at **50%** with a **4x multiplier**, and the red range is capped at **25%** with an **8x multiplier**, with baseline thresholds of **90** and **95** respectively for the CPU Run metric.]

The expression 50 – caps the value of orange at 50%, while the red is capped at 25.
The * 4 at the end is the weightage multiplier for orange. The * 8 at the end is the weightage multiplier for red.
Now let’s look at the remaining metrics.
For Guest OS Memory Free, since the threshold is descending, the logic is simpler as the value cannot be less than 0.

[Image: ## Image Description

This image shows a **conditional scoring formula** for the **Guest OS Memory Free** metric, expressed as a ternary operation. The formula evaluates whether free memory (in MB converted to GB via `/1024`) exceeds **128 GB**: if true, it calculates a weighted orange score using `((mFree/1024 - 128) / 128 * 25 + 25) * 4`; if false, it calculates a weighted red score using `mFree/1024/128 * 25 * 8`. The multipliers `* 4` (orange) and `* 8` (red) represent severity weightage, with the descending threshold logic simplified since the value cannot drop below zero.]


### vMotion

There are 3 metrics to watch. In order of importance, they are:
- Downtime
- Stun time
- Copy Bandwidth
The first 2 are contention metrics. You should set alarm for high values.
The last one is a consumption metric.
Since the values for each vMotion migration can vary, monitor both the outlier and the average, and match them to your expectation.

#### Downtime

Log Insight explains it well, so I will use it with some modification:
During the final phase of a vMotion operation, the VM is momentarily quiesced on the source ESXi host. This enables the last set of memory changes to be copied to the target ESXi host. After that, the VM is resumed on the target host. The guest briefly pauses processing during this step. Although the duration of this phase is generally less than  200 milliseconds, it is where the largest impact on guest performance (an abrupt, temporary increase of latency) is observed. The impact depends on a variety of factors such as network infrastructure, shared storage configuration, host hardware, vSphere version, and dynamic guest workload.
The following screenshot shows trend towards unhealthy range.

[Image: ## Image Description

This bar chart displays **VM downtime (vmw_esxi_vmdowntime)** in microseconds over approximately 5 minutes (19:36:30–19:41:00), showing the duration of guest pauses during vMotion migrations. Most values fluctuate between **~100k–600k microseconds**, remaining within acceptable range, but a significant spike occurs around **19:40:30 reaching ~1,250,000 microseconds (1.25 seconds)** — exceeding the 1,000,000 microsecond (1 second) concern threshold. This demonstrates an example of VM downtime trending into the **unhealthy range**, where the migration stun time surpassed the acceptable 200ms target by more than 6x.]

The time unit is in microseconds. The expected time is 200 milliseconds. Anything over one million microseconds (one second) is a cause for concern.
Log Insight has a metric called vmw_esxi_vmdowntime. Plot the worst value as it’s a leading indicator.

[Image: ## Image Description

The screenshot shows a **Kibana/Log Insight visualization configuration** for the metric **`vmw_esxi_vmdowntime`**, plotting the **Max (worst-case) value over time** using a Column chart type with 5-second bar intervals. The query filter shows `vmw_esxi_vmdowntime` **exists**, applied over a custom time range of **Nov 1, 2023, 19:36:08 to 19:41:08** (a 5-minute window). The red arrow highlights the **"Max of vmw_esxi_vmdowntime"** aggregation selector, emphasizing the book's guidance to plot the worst value as a leading indicator for vMotion-related VM downtime concerns.]


#### Stun Time

Stun Time is the period the VM gets a checkpoint stun, where no guest instruction is executed on the same vmx file. Operations that incur checkpoint are device reset, disk branching, disk promotion, snapshot take, and snapshot consolidate. A long stun time will impact Guest OS performance.
During the first phase of a vMotion operation, a snapshot is created for the VM. Snapshot means a delta VMDK is being created, which requires a stun operation. The VM then switches its write operations to the delta disk.
The time unit is in microseconds. 200 millisecond is a good threshold, and anything above 1 second should be investigated.

[Image: ## Image Description

This is a time-series bar chart displaying **VMware vMotion stun time metrics** (in microseconds) over approximately a 5-minute window from **20:24:00 to 20:28:30**. The chart shows sporadic spikes with the highest peak reaching approximately **14M microseconds (~14 seconds)** at 20:24:00, with additional notable spikes of ~8M at 20:24:45 and ~6M at 20:26:30. 

In the context of the surrounding text, this chart illustrates VM stun time events — likely corresponding to snapshot creation during vMotion operations — where several spikes **far exceed the recommended 1-second (1M microsecond) investigation threshold**, indicating potentially problematic stun durations impacting Guest OS performance.]

Log Insight has a metric called vmw_esxi_vmprecopystuntime. Plot the highest value as it’s a leading indicator.

[Image: This screenshot shows a **VMware Log Insight query** configured to plot the **maximum value of `vmw_esxi_vmprecopystuntime`** over time, with a 1-second bar resolution. The query filters for records where the `vmw_esxi_vmprecopystuntime` metric **exists**, applied against the **latest 5 minutes of data** (Nov 1, 2023, 20:23:57.874 to 20:28:57.873). This visualization demonstrates how to track the peak pre-copy stun time during vMotion operations, which is the leading indicator for VM stun duration thresholds (200ms warning, >1 second critical).]

Complement the above trend chart with a table that shows the ESXi host. Note the table does not show the VM name.

[Image: ## Image Description

This **Field Table** from VMware Log Insight displays the **vmw_esxi_vmprecopystuntime** metric across multiple ESXi hosts, showing pre-copy stun times in microseconds captured on **November 1, 2023** around **8:35–8:36 PM**. The values range significantly, with the highest value being **1,180,548 microseconds (~1.18 seconds)** on host `wdc-12-r05esx09.h2o-77-16685.h2o.vmware.com`, which exceeds the recommended 1-second investigation threshold, while other hosts show values between **~20,000–157,983 microseconds**. This table complements the trend chart by identifying the specific ESXi hosts contributing to elevated pre-copy stun times during vMotion operations, though notably it does not display individual VM names.]


#### Copy Bandwidth

Since this is a consumption metric, ensure the values are not too low, as that will slow down vMotion progress.
The bandwidth (Gb/s) should be relatively stable and matches the assigned capacity for vMotion traffic.

[Image: ## Image Description

This bar chart displays **vMotion Copy Bandwidth** measured in **megabytes per second (MB/s)** over approximately a 24-hour period spanning from **21:00 (Oct 31) through ~20:00 (Nov 1)**. Values consistently range between **~1,000M and ~1,300M MB/s**, with one notable spike reaching approximately **1,300M** around the 11:00–12:00 hour. The chart demonstrates stable, relatively uniform copy bandwidth throughout the period, confirming that vMotion traffic is utilizing its allocated network capacity consistently without significant drops or interruptions.]


### Latency Sensitivity

You can reduce the latency and jitter caused by virtualization by essentially “reserving” the physical resource to a VM. In the vSphere Client UI, edit VM settings, and go to VM Options tab.

[Image: This screenshot shows the **VM Options tab** within the **Edit Settings** dialog for a virtual machine named "WindowsVMvsan020202" in the vSphere Client UI. The view displays the **General Options** section, which confirms the VM Name as "WindowsVMvsan020202." This image serves as a navigation reference, illustrating where to access VM-level configuration options (specifically the VM Options tab) as a precursor to locating the **Latency Sensitivity** setting described in the surrounding text.]

Scroll down until you see this option.

[Image: The image shows a VMware vSphere VM settings dialog with a **Latency Sensitivity** dropdown menu currently set to **"High"**, with the dropdown expanded to reveal two available options: **"Normal"** and **"High"**. This screenshot demonstrates the configuration step for enabling high latency sensitivity on a virtual machine, which as described in the surrounding text, reserves physical CPU resources exclusively for the VM to minimize virtualization-induced latency and jitter. The **Fibre Channel NPIV** section is also partially visible below, along with standard **Cancel/OK** dialog buttons.]

What happens to the metrics when you set Latency Sensitivity = High?

#### CPU Impact

The CPU “pipeline” has to be made available. In a sense, the CPU is scheduled 100% of the time. This prevents any wakeup or scheduling latencies that result of having to schedule a vCPU when it wakes up in the first place. Yes, the exclusive bit of exclusive affinity is literal.
Let’s see what it looks like in esxtop. I’ve removed unnecessary information so it’s easier to see. What do you notice?
GID NAME                             %USED    %RUN    %SYS   %WAIT  %IDLE
153670 vmx                               0.03    0.03    0.00  100.00   0.00
153670 NetWorld-VM-2127520               0.00    0.00    0.00  100.00   0.00
153670 NUMASchedRemapEpochInitialize     0.00    0.00    0.00  100.00   0.00
153670 vmast.2127520                     0.00    0.00    0.00  100.00   0.00
153670 vmx-vthread-212                   0.00    0.00    0.00  100.00   0.00
153670 vmx-filtPoll:WindowsTest          0.00    0.00    0.00  100.00   0.00
153670 vmx-mks:WindowsTest               0.00    0.00    0.00  100.00   0.00
153670 vmx-svga:WindowsTest              0.00    0.00    0.00  100.00   0.00
153670 vmx-vcpu-0:WindowsTest            0.31  100.21    0.00    0.00   0.00
153670 vmx-vcpu-1:WindowsTest            0.16  100.21    0.00    0.00   0.00
153670 vmx-vcpu-2:WindowsTest            0.15  100.21    0.00    0.00   0.00
153670 vmx-vcpu-3:WindowsTest            0.15  100.21    0.00    0.00   0.00
153670 LSI-2127520:0                     0.00    0.00    0.00  100.00   0.00
153670 vmx-vthread-212:WindowsTest       0.00    0.00    0.00  100.00   0.00
We can see Run shot up to 100%. This means Wait has to go down to 0%.
Strangely, Used remains low, so we can expect that Usage remains low too. This means the formula that connect Run and Used do not apply in this extreme scenario. You’re basically cutting a physical core to the VM.
But what about Demand?
Demand shot up to 100% flat out.

[Image: ## Image Description

The chart displays **CPU Demand (MHz) for WindowsVMvsan020202** on 02/23/2022, showing a dramatic spike from near-zero (~15 MHz minimum) to **4,391 MHz maximum** at approximately 6:08:40 PM, where it plateaus and remains elevated. The legend confirms two metrics: **Demand** (latest: 4,390 MHz, average: 2,441.911 MHz) and **Usage in MHz** (latest: 12 MHz, maximum: 184 MHz, average: 18.256 MHz). This visually demonstrates the key anomaly described in the surrounding text — **Demand shot to ~4,391 MHz (effectively 100%) while Usage in MHz remained essentially flat near zero**, illustrating the disconnect between Demand and Usage under extreme CPU contention/limiting conditions.]

So you have an interesting situation here. Demand is 100%, Usage is 0%, yet Contention is 0%.
Now let’s plot what happened to Wait and Idle. Notice both went from 100% to 0%.

[Image: ## Image Description

The chart displays **CPU Idle and Wait time (in milliseconds, Summation rollup)** for VM `WindowsVMvsan020202` over approximately 35 minutes on 2/23/2022. Both metrics hover near **~39,685–39,781 ms** (near maximum/100%) from 5:40 PM until approximately **6:05 PM**, at which point they **sharply drop to 0 ms** and remain there. The legend confirms: Idle has a maximum of **39,774 ms** and average of **18,993 ms**; Wait has a maximum of **39,781 ms** and average of **19,001 ms**, both with a latest value of **0**.

This demonstrates the scenario described in the surrounding text — when a physical CPU core is effectively removed from the VM, both Wait and Idle metrics collapse from 100% to 0%, confirming the VM has no idle or wait time because it is being severely CPU-constrained.]

So if you combine Run, Demand, Wait and Usage metrics, you can see basically Run and Demand shot up to 100% as Wait drops to 0%, while Usage is oblivious to the change.

[Image: ## Image Description

This performance chart displays four CPU metrics for a WindowsVMvsan020 VM over approximately 40 minutes on 2/23/2022: **Demand** (blue, peaks at 4,391 MHz), **Usage in MHz** (black, max 184 MHz), **Wait** (green, max 39,781 ms), and **Run** (orange, max 40,005 ms). Around 6:05 PM, a dramatic transition occurs where **Wait drops to near zero** while **Run and Demand spike sharply to ~4,390 MHz and ~3,900 MHz** respectively, remaining elevated. This illustrates the book's point that when a physical core is dedicated to the VM, Run and Demand shoot to 100% as Wait collapses to 0%, while Usage remains oblivious (staying near 0/flat) to the underlying scheduling change.]

Just for documentation purpose, System and Ready are obviously not affected.

[Image: ## Image Description

This table displays CPU performance metrics for a Windows VM, showing six measurements (Run, Used, System, Ready, Wait, Idle) all using Summation rollup in milliseconds. The **Latest** column shows Run at 40,005ms and Used at 75ms, while System, Ready, Wait, and Idle are all **0**. The **Maximum** column reveals historical peaks of Wait (39,781ms) and Idle (39,774ms), confirming the text's assertion that Wait and Idle dropped to 0% as Run shot up to ~100% (40,005ms), while Ready and System remained unaffected.]


#### Memory Impact

Memory is fundamentally storage. So I do not expect any of the counters to go up. They will go up when the VM actually needs them.

[Image: ## Image Description

The chart displays the **"Amount of host physical memory the virtual machine deserves, as determined by ESXi"** (entitlement metric) for **WindowsVMvsan020202** over approximately one hour on 02/23/2022 (5:20 PM – 6:20 PM). The metric holds a **flat, constant value of ~1,436,448 KB (~1.4 GB)** throughout the entire observation period with no variation whatsoever. This demonstrates the author's point that memory counters do not fluctuate in response to CPU activity changes, as the VM remains essentially idle despite its 4 GB RAM allocation being fully reserved.]

The above VM has 4 GB of RAM, fully reserved. But since it’s basically idle, there is no change on the counter.

## Capacity: VM

VM right-sizing is a commonly misunderstood term because there are actually 2 distinct formulas: 1 internal and 1 external.
- Internal means sizing the Guest OS, which lives inside a VM. Let’s call this Guest OS Sizing.
- External means sizing the footprint of the VM to the underlying ESXi and infrastructure. Let’s call this VM Footprint.

### VM Footprint | Guest OS Sizing

To see the difference between internal and external sizing, let’s examine a few popular use cases:
- Your application team asks for extra vCPU. In this case, the hypervisor overhead is irrelevant. When you size NSX edge vCPU, you do not need to add extra vCPU for the overhead to do the packet processing. This means you’re sizing Guest OS.
- Infrastructure team is migrating a VM to a new ESXi with CPUs that are 2x the speed. For example, from a 2 GHz ESXi to 4 GHz. All else being equal, you can cut down the VM size by 2. A 16 vCPU becomes 8. In this case, the hypervisor counter is more accurate. 
However, you are worried about causing queue inside the Guest OS as the application may expect 16 slow threads vs 8 fast ones. In this case, you need to look inside Guest OS but do that after rightsizing.
- You’re migrating a VM from classic VMFS to vSAN. In this case, use the hypervisor metric as it will be adjusted according to vSAN FTT policy.
- You’re converting VM virtual disks from thin to thick. In this case, the consumption at Guest OS level is irrelevant as you’re inflating the virtual disk into its configured size.
From the above use cases, we need two different formulas:

| Purpose | Method |
| --- | --- |
| Guest OS Sizing | Using Windows/Linux counters. Excludes VM overhead, includes Guest OS Queue. Used to size the “VM”, meaning the CPU and RAM requirements of Windows or Linux. For disk, that means the size of the Guest partitions, but expressed in terms of virtual disks. |
| VM Footprint | Using vSphere counters. Includes VM overhead, excludes Guest OS Queue. Used to size the “infrastructure footprint” of the VM |

Once we know what the VM needs, we need to project based on past data and recommend the new size. The new size is then adjusted to comply with NUMA.
You’ll see below that CPU, RAM and storage all require different approach.

### Benefits

Rightsizing is important for a VM, more so than for a physical server. Here are some benefits:

[Image: ## Image Description

The image displays **seven hexagonal tiles** listing the negative consequences of **oversized VMs** in a vSphere environment, serving as justification for rightsizing. The metrics/issues shown are: **Longer boot time**, **Longer vMotion time**, **Risk of NUMA effect**, **Higher co-stop and ready time** (highlighted in dark blue, indicating higher severity), **Longer time taken to snapshot**, **Process ping-pong**, and **Lack of performance visibility**. In context, this diagram supports the argument that oversizing VMs degrades performance — particularly CPU scheduling metrics like **co-stop and ready time** — making rightsizing a performance improvement rather than merely a cost-saving measure.]

I’ve seen large enterprise customers try to do a mass adjustment, downsizing many VMs, only to have the effort backfire when a tiny percentage of VM performance suffers. Take time and effort to educate the VM Owner that right sizing actually improves performance, despite the seemingly odd logic. A carrot is a lot more effective than a stick, especially for those with money. Saving money is a weak argument in most cases, as VM Owners have paid for the VMs.
Here is an example where accuracy in right-sizing matters:
- The ESXi CPU has 2 socket, 16 cores each.
- The VM has 16 vCPU. It runs at 90%, so it fits into a single socket.
- The queue inside Linux is below 2 per vCPU for 95% of the time. This means the 16 vCPU is working hard, but able to serve all processes well.
- However, you decide to use the CPU Usage counter, which runs 25% higher due to Turbo.
- 16 vCPU x 90% x 125% = 18 vCPU
- Based on the above, you incorrectly increase the size to 18 vCPU
- The VM now spread into 2 NUMA nodes. You can have either 9 per side, or 10 vs 6. You do not like the idea of running odd numbers, plus you think it’s safer to give buffer, so you bump the number to 20 vCPU.
- The VM vCPU will now be spread into 2 CPU. This means the memory will be spread too. The result is NUMA effect.
With CPU having CCD complex within a single socket, the NUMA effect does happen within a socket albeit with less penalty.
Another benefit of rightsizing is potentially faster speed from higher CPU frequency. Less vCPU means less physical threads to run. This means ESXi is able to boost the active threads by keeping unused cores. To see this, choose the CPU Usage (MHz) counter and show all the vCPU.

[Image: ## Image Description

The chart displays **CPU Usage in MHz** for 4 vCPUs (Objects 0-3) on a VM between **9:40–10:05 PM on 01/19/2024**, with values typically ranging **30–100 MHz** but showing a dramatic spike to approximately **~315–360 MHz** around **9:52 PM**. 

The four vCPUs (represented by purple, gray, dark navy, and teal lines) show relatively similar usage patterns with average rollup metrics, demonstrating that individual vCPUs can achieve **higher burst frequencies** during periods of demand. 

In context, this illustrates the book's point that **rightsizing VMs with fewer vCPUs allows ESXi to boost clock frequency** on active threads by keeping unused cores idle, resulting in higher MHz availability per vCPU during peak workloads.]

Lower co-stop and ready time. Even if not all vCPU is used by the application, the Guest OS will still demand all the vCPU be provided by the hypervisor.
Faster snapshot time, especially if memory snapshot is included.
Faster vMotion. Windows and Linux use memory as cache. The more it has, the more it uses, all else being equal.
Faster boot time. If a VM does not have a reservation, vSphere will create a swap file the size of the configured RAM. This can impact the boot time if the storage subsystem is slow.

### Guest OS Sizing

What rules to follow then sizing the Guest OS?

#### CPU Sizing

What metrics should be excluded when sizing Guest OS? What metrics should be included?
Having the correct inputs increase the accuracy of the prediction.

##### Exclusion


| Hyper-Threading | The Guest OS is unaware of HT. Windows/Linux is still running, regardless of speed and throughput.  When Windows/Linux vCPU happens to run on a thread that is sharing a core with another thread, the OS will simply run with lower efficiency. It experiences 37.5% drops in computing power. For example, instead of running on a 3 GHz, it feels like it’s running on 1.875 GHz chip. The VM CPU Demand and VM CPU Usage metrics are not suitable as their values are affected by CPU Frequency and HT. |
| --- | --- |
| CPU Frequency | Same reason as above.  The only exception here is the initial sizing, when the VM is not yet created. The application team may request 32 vCPU at 3 GHz. If what you have is 2 GHz, you need to provide more vCPU. |
| CPU idle time | Guest OS CPU will be idle for a while when waiting for ESXi to execute IO. However, while making the IO subsystem faster will result in higher CPU utilization, that’s a separate scope. |
| CPU Context Switch | 3 reasons: There is no translation into CPU size.  It is not something you can control.  A high context switch could be caused by too many vCPU or IO. Guest OS is simply balancing among its vCPUs. |
| Hypervisor overhead | Reason is they are not used by the Guest OS. MKS, VMX, System. While it’s part of Demand, it’s not a demand coming from within the Guest. The VM CPU Used, Demand, Usage counter include system time at VM level, hence they are not appropriate. |


##### Inclusion


| Co-stop & Ready | The Guest OS actually wants to run. Had there been no blockage, the CPU would have been utilized. Adding/reducing CPU does not change the value of these waits, as this represents a bottleneck somewhere else. However, it does say that this is what the CPU needs, and we need to reflect that. We need not consider CPU Limit as it’s already accounted for. Guest OS number will be inaccurate because there is “no data”, due to its time being frozen. |
| --- | --- |
| Other Wait | Guest OS becomes idle as CPU is waiting for RAM or IO (disk or network). So this is the same case with Ready and Co-stop. |
| Swap Wait | Guest OS becomes idle as CPU is waiting for RAM or IO (disk or network). So this is the same case with Ready and Co-stop. |
| Overlap | The Guest OS actually wants to run, but it’s interrupted by the kernel. Note that this is already a part of CPU Run, so mathematically is not required if we use CPU Run counter. |
| Guest OS CPU Run Queue | This is the primary counter tracking if Windows or Linux is unable to cope with the demand. |


##### Formula

Based on all the above, the formula to size the Guest OS is:
Guest OS CPU Needed = Configured vCPU – Idle + CPU Run Queue factor
The result is in the number of vCPU. It is not in % or GHz. We are sizing the Guest OS, not the VM.
We’re including all the time the vCPU cannot run (Ready, Costop, Swap Wait, Other Wait) as the Guest OS would have wanted to run.
Guest OS CPU Run Queue metric needs some conversion before it can be used. Let’s take an example:
VM has 8 vCPU.
CPU Run Queue = 28 for the entire VM.
VM can handle 8 x 3 = 24 queues.
There is a shortage of 28 – 24 = 4 queues.
Each additional vCPU can handle 1 process + 3 queues.
Conclusion: we add 1 vCPU.
Compared with CPU Usage, Guest OS Needed without the CPU run queue factor tends to be within 10% difference. Usage is higher as it includes system time, and turbo boost. Usage would be lower in HT and CPU frequency clocked down case.
Here is an example where Usage is higher.

[Image: ## Image Description

The chart displays two metrics for **hdp-sse-wrk12** over a ~24-hour period: **CPU|Usage (%)** (pink) and **Super Metric|Ops. Guest OS CPU Needed (%)** (purple), both ranging from ~0–60%. The CPU Usage (pink) consistently runs **higher** than Guest OS CPU Needed (purple), with the most pronounced divergence visible at the **Nov 16 ~11 PM spike** where Usage reaches ~58% versus Needed at ~48%, and earlier peaks around **6 AM (~45%)** and **5 PM (~50%)** show similar separation. This demonstrates the specific case mentioned in the surrounding text where **CPU Usage exceeds Guest OS CPU Needed**, attributed to system time and turbo boost factors inflating the Usage metric beyond what the Guest OS actually required.]

Here is an example where Usage is lower.

[Image: The chart displays two metrics for **sc2-corp-esrs-gw1** over approximately 24 hours (Nov 12–13): **CPU Usage (%)** (dark purple) and **Super Metric|Ops. Guest OS CPU Needed (%)** (pink), both fluctuating generally between 0–20% with periodic spikes. A significant anomaly occurs around **4:00–4:30 PM**, where the Guest OS CPU Needed metric spikes to approximately **60–65%** while CPU Usage remains comparatively lower (~20–25%). This example demonstrates the scenario where **CPU Usage is higher than Guest OS Needed** for most of the timeframe, consistent with the surrounding text's explanation that Usage includes system time and turbo boost effects, though the 4 PM spike shows a divergence where demand briefly far exceeded reported usage.]

Once we know what the Guest OS needs, we can then calculate the recommended size. This is a projection, taking lots of value. Ideally, the recommendation is NUMA aware. It is applied after the sizing is determined. You size, then adjust to account for NUMA. This adjustment depends on the ESXi Host. So it can vary from cluster to cluster, if your vSphere clusters are not identical.
Guest OS Recommended Size (vCPU) = round up NUMA (projection (Guest OS Needed (vCPU))
For basic NUMA compliant, use 1 socket many cores until you exceed the socket boundary. That means you use 2 vCore 1 vSocket instead of 2 vSockets with 1 vCore each.
With the release of Windows 2008, switching the Hardware Abstraction Layer (HAL) was handled automatically by the OS, and with the release of 64-bit Windows, there is no concept of a separate HAL for uniprocessor and multi-processor machines. That means one vCPU is a valid configuration and you shouldn’t be making two vCPU as the minimum.
You should use the smallest NUMA node size across the entire cluster, if you have mixed ESXi with different NUMA node sizes in the cluster. For example, a 12-vCPU VM should be 2 socket x 6 cores and not 1 socket x 12 core as that fits better on both the dual socket 10 core and dual socket 12 core hosts. Take note that the amount of memory on the host and VM could change that recommendation, so this recommendation assumes memory is not a limiting factor in your scenario.
Notice the number is in vCPU, not GHz, not %. Reason is the adjustment is done at a whole vCPU. In fact in most case, it should be an even number, as odd numbers don’t work in NUMA when you cross the size of a CPU socket.
Note that when you change the VM configuration, application setting may need to change. This is especially on applications that manage its own memory (e.g. database and JVM), and schedule fixed number of threads.
You can enable Hot Add on VM, but take note of impact on NUMA.
Reference: rightsizing by Brandon Gordon.

#### Memory Sizing

Accuracy of Guest OS memory has been a debate for a long time in virtualization world. Take a look at the following utilization diagram. It has two bars, showing memory utilization of Windows/Linux. They use different set of thresholds.
Which one should you use for memory?

[Image: ## Image Description

The image shows two horizontal bar charts (VM 1 and VM 2) displaying memory utilization thresholds from 0% to 100%, using a color-coded scale: **gray** (waste/idle), **green** (optimal), **yellow** (warning), **orange** (high), and **red** (critical).

**VM 1** applies aggressive thresholds, with green starting around **35%** and red beginning near **85%**, representing a Windows/Linux-style utilization model with a wide actionable range. **VM 2** applies more conservative thresholds, with green not starting until approximately **75%** and a much narrower warning/critical band near **90-100%**, reflecting a higher tolerance for utilization before alerting.

This illustrates the contrast between two different memory sizing threshold philosophies, supporting the author's recommendation to use VM 2's thresholds — treating memory as cache and accepting high utilization as normal rather than wasteful.]

My recommendation is no 2.
The reason is memory is a form of cache. It stays even though it’s not actively used.
When you spend your money on infrastructure, you want to maximize its use, ideally at 100%. After all, you pay for the whole box. In the case of memory, it even makes sense to use the whole hardware as the very purpose of memory is just a cache for disk.
The green range is where you want the utilization to fall. Below the green threshold lies a grey zone, symbolizing wastage. The company is wasting money if the utilization falls below 50%. So what lies beneath the green zone is not an even greener zone; it is a wastage zone. On the other hand, higher than 75% opens the risk that performance may be impacted. Hence I put a yellow, orange and red threshold. The green zone is actually a relatively narrow band.
In general, applications tend to work on a portion of its Working Set at any given time. The process is not touching all its memory all the time. As a result, the rest becomes cache. This is why it’s fine to have active + cache beyond 95%. If your ESXi is showing 99%, do not panic. In fact, ESXi will wait until it touches 99.1% before it triggers ballooning process. Windows and Linux are doing this too. The modern-day OS is doing its job caching all those pages for you. So you want to keep the Free pages low.

| Include cache | Guest OS uses RAM as cache. If you size the OS based on what it actually uses, it will have neither cache nor free memory. It will start paging out to make room for Cache and Free, which can cause performance problems. As a result, the name of this proposed counter should not be called Demand as it contains more than unmet demand. It is what the OS needs to operate without heavy paging. Hence the counter name to use is Needed Memory, not Memory Demand. The challenge here is how much cache do you want to include? |
| --- | --- |
| Exclude page file | Including the pagefile will result in sizing that is too conservative as Windows and Linux already has cache even in their In Use counter. Guest OS uses virtual RAM and physical RAM together. They page-in proactively, prefetching pages when there is no real demand due to memory mapped files. This makes determining unmet demand impossible. A page vault does not distinguish between real need versus proactive need. |
| Exclude balloon | It results in more usage inside the Guest OS, if it comes from the free page. |
| Don’t fallback to VM metric | Since we are sizing the Guest OS, we use Guest OS only. No falling back to VM as it’s inaccurate. |
| Exclude latency | RAM contention measures latency, hence not applicable. We’re measuring the disk space, not latency. Space, not Speed. Utilization, not Performance. |

Unlike CPU, there are more difference between Windows and Linux when it comes to memory.
For VCF Operations specific implementation, review this post by Brandon Gordon.

### VM Footprint

What rules to follow then sizing the footprint of the VM to the underlying SDDC?

#### CPU Sizing


| Include Hyper-Threading | When a VM runs on a thread that has a peer thread running, it’s getting less CPU cycle. |
| --- | --- |
| Include CPU Frequency | It impacts the footprint.  For example, moving a VM to cluster with lower frequency may require more vCPU |
| Include contention | The VM actually wants to run, but blocked by hypervisor. This means Overlap needs to be added as Used does not include it. |
| Include VM overhead | They are not insignificant in cases such as Fault Tolerant. |
| Exclude Guest OS queue | It’s transparent to the VM |

Based on all the above, the formula to size the VM is:
VM CPU Needed = (Used + Overlap + Co-stop + Ready + Other Wait + Swap Wait) + System / 20000
You express in GHz (utilization model) and vCPU (allocation model).
The GHz is especially important when you need to migrate into another ESXi with different clock speed. To convert into GHz, we multiply the number by the nominal, static clock speed.
Enhance the sizing by considering CPU generation and speed. Take note this can introduce a new problem if not done properly. An application may perform poorly after the reduction in vCPU if it works better with many slow threads vs a few fast threads.

#### Memory Sizing

Since the goal is to calculate the total footprint, you need to include all the pages associated to the VM.
VM Memory Needed = Consumed + Overhead + Swapped + Compressed + Ballooned
The effect of Transparent Page Sharing should be included as that likely persist when you vMotion the VM. The challenge is it’s not possible to separate intra-VM sharing and inter-VM sharing.
Memory contention is not included as that measures speed, not space.
Chapter 7

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


# Epilogue

Thank you for reading the book. I hope it’s been valuable.
The book has taken me a long time. The following timeline summarizes its journey.

[Image: ## Image Description

The timeline graphic illustrates the **publishing journey of a series of VMware technical books from approximately 2008 to 2026**, showing the evolution and growth of content across multiple publications. Key milestones include: a **250-page** vRealize Operations Performance Management book (~2012), expanding to a **500-page** VMware Performance and Capacity Management book (~2014), a **750-page** VMware Operations Transformation (~2019), and most recently three concurrent works still in progress — a **25-page Executive Summary**, **450-page vSphere Metrics**, and **500-page Private Cloud Operations** (all extending to 2026). The timeline also tracks the author's professional milestones including VCAP DCD certification (~2011), blogging activity (~2012–2020), and vCommunity involvement (VMUG, vExpert, VCP) from ~2021 onward.]

The book is a companion book to the main book (Private Cloud Operations). Part of its content dated back to 2012, when I first started blogging and sharing my learning. For the first 10 years, the book was part of the main book. As the main book exceeded 1000 pages, I had to trim down content. One outcome was the birth of vSphere Metrics as a separate book.
I shared details about how the 2 books evolved over the years in the main book.
Thank you
E1@broadcom.com