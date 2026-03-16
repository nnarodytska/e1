
![image1.png](images/image1.png)

.
Back of cover page.
Delete if you do not plan to print.

![image2.jpg](images/image2.jpg)

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

![image3.png](images/image3.png)

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


![image4.png](images/image4.png)

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

![image5.png](images/image5.png)

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

![image6.png](images/image6.png)


#### Visibility

Guest OS and VM are 2 closely related due to their 1:1 relationship. They are adjacent layers in SDDC stacks. However, the two layers are distinct, each provide unique visibility that the other layer may not be able to give. Resource consumed by Guest OS is not the same as resource consumed by the underlying VM. Other factors such as power management and CPU SMT also contribute to the differences.
The different vantage points result in different metrics. This creates complexity as you size based on what happens inside the VM, but reclaim based on what happens outside the VM (specifically, the footprint on the ESXi). In other words, you size the Guest OS and you reclaim the VM.
The following diagram uses the English words demand and usage to explain the concept, where demand consists of usage and unmet demand. It does not mean the demand and usage metrics in vSphere and VCF Operations, meaning don’t assume these metrics actually mean this. They were created for a different purpose.

![image7.png](images/image7.png)

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

![image8.png](images/image8.png)

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

![image9.png](images/image9.png)

The 3rd choice complements the 2nd choice by picking the worst. That means you need 2 number per metrics for certain use case.
As you collect regularly, you also need to decide if you reset to 0, or you continue from previous cycle. Most metrics reset to 0 as accumulation is less useful in operations.
Let’s take a look at what you see at vCenter UI, when you open the performance dialog box. What do the columns Rollups and Stat Type mean?

![image10.png](images/image10.png)

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

![image11.png](images/image11.png)

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

![image12.png](images/image12.png)


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

![image13.png](images/image13.png)

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

![image14.png](images/image14.png)

As expected, Google uses 1 byte = 8 bits

![image15.png](images/image15.png)

However, many products from many vendors use the binary conversion instead of decimal. This is one of those issues, where what’s popular in practice is different to what it should be in theory.
To add further confusion, there is consistency among storage and network vendors. For example, you get shortchanged when you buy storage hardware.
Guess how many GB do you actually get from this 128 GB? This screenshot is from the vendor official website. I think many hardware vendors do the same.

![image16.png](images/image16.png)

The answer is 116 GB.
The following is the above actual disk in Windows 11.

![image17.png](images/image17.png)

You lost 9%!
Microsoft Windows use 1024 for storage.
VCF Operations use 1024 for storage, 1024 for network, 1024 for memory, but 1000 for CPU.
Here is the proof for storage. Yes, I validated network and memory too.

![image18.png](images/image18.png)


![image19.png](images/image19.png)

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

![image22.png](images/image22.png)

What would it show if you convert into KBps?
30810, if it uses 1000.

![image23.png](images/image23.png)

Since vRealize treats 1 Mega = 1024 Kilo, the above is what you get.
Since it’s network, let’s convert into bit.
What do you expect you get in Mbps?

![image24.png](images/image24.png)

You get 31 x 553.13 x 8 bits / 1024 = 246 / 51.

### Aggregation

We discussed in earlier part of the book about data collection. After collecting lots of data across objects and across time, how do you summarize so you get meaningful insight?
Aggregating to a higher-level object is complex as there is no lossless solution. You are representing a wide range of values by picking up 1 value among them, so you lose some details. The choices of techniques are mean, median, maximum, minimum, percentile, sum and count of.

#### The Problem with Average

The default technique used by many observability tools is the average() function as that represents every value to be aggregated. Average is great across time, but not across members of a group.
The problem is it will mask out the outlier unless they are widespread. By the time the average performance of 1000 VMs is bad, you likely have a hundred VMs in bad shape.
Let’s take an example. The following table shows ESXi hosts. The first host has CPU Ready of 149,116.33 ms. Is that a bad number?

![image25.png](images/image25.png)

It is hard to conclude. It depends on the number of running vCPU, not the number of physical cores.
That host has 67 running VMs, and each of those VMs can have multiple vCPU. In total there are 195 vCPU. Each vCPU could potentially experience CPU Ready of 20,000 ms (which is the worst possible scenario).
If you sum the CPU Ready of the 67 VM, what number would you get?

![image26.png](images/image26.png)

You’re right, you get the same number reported by the ESXi host.
This means the ESXi CPU Ready = Sum (VM CPU Ready), and the VM CPU Ready = Sum (VM vCPU Ready).
Because it’s a summation of the VMs, to convert into % requires you to divide with the number of running VM vCPU.
ESXi CPU Ready (%) = ESXi CPU Ready (ms) / Sum (vCPU of running VMs)
Are the CPU Ready values equally distributed among the VMs? What do you think?
It depends on many settings, so there is a good chance you get something like the following. This heat map shows the 67 VMs on the above host, colored by CPU Ready and sized by VM CPU configuration. You can see that the larger VMs tend to have higher CPU ready, as they have more vCPU.

![image27.png](images/image27.png)


#### Lagging vs Leading Indicators

When it comes to performance management, you need to see the problem while it’s still early, when only a small percentage of users or applications are affected. For that, you need a leading indicator, not a lagging indicator (after the fact). Leading indicators complement the lagging indicator by giving the early warning, so you have more time to react.
Performance use the contention metric as its primary input. The problem with contention metrics is it drops (or spike, depending on how you see it) suddenly, typically at the point of overcommit. It differs to consumption metrics which goes up towards 100%.

![image28.png](images/image28.png)

As a result, average is not suitable for rolling up performance metrics to higher level parents. For example, a VDI system that was designed for 1000 users should serve the first 1000 well, and it should struggle after the capacity is exceeded.
Average is a lagging indicator. The average of a large group tends to be low, so you need to complement it with the peak. On the other hand, the absolute peak can be too extreme, containing outliers.
The following chart shows where Maximum() picks up the extreme (outlier) while average fails to detect the problem. This is where the worst 5th percentile or the worst 1st percentile makes more sense.

![image29.png](images/image29.png)

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

![image30.png](images/image30.png)

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

![image31.png](images/image31.png)

Notice the Maximum is >10x higher than the average. The average is also very stable relative to the maximum. It did not move even though the maximum became worse. Once the Cluster is unable to cope, you’d see a pattern like this. Almost all VMs can be served, but 1-2 were not served well. The maximum is high because there is always one VM that wasn’t served.
Be careful when you look at metrics at parent object such as cluster and datastore, as average is the default counter used in aggregation. Here is another example. This shows a cluster wise average. What do you think of the value?

![image32.png](images/image32.png)

That’s right. No performance issue at all in the last 7 days. The cluster is doing well. This cluster run hundreds of VMs. What you see above is the average experience of all these VMs, aggregated at cluster level. If there is only a few VMs having a problem, but the majority are not, the above fails to show it.
Now look at the pattern. You can see there are changes in that 1 week period.
What do you expect when you take the worst of any VM? Would you get the same pattern?

![image33.png](images/image33.png)

Answer is possible (not always!), if every VM is given the same treatment. They will take turn to be hit.
Notice the scale. It’s 60x worse.
The following diagram explains how such thing can happen.

![image34.png](images/image34.png)

The above charts show 6 objects that have varying disk latency. The thick red line shows that the worst latency among the 6 objects varies over time.
Plotting the maximum among all the 6 objects, and taking the average, give us two different results as shown below:

![image35.png](images/image35.png)

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

![image36.png](images/image36.png)

The following shows an example where both breadth and dept confirm you have a CPU Ready problem.

![image37.png](images/image37.png)


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

![image38.png](images/image38.png)

The following calculation shows that using the relatively imbalance results in a high number, which can be misleading as the actual imbalance is only 10%

![image39.png](images/image39.png)


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

![image40.png](images/image40.png)

Why don’t we make green 95% - 100%? 75% for green sounds rather bad or low.
My answer is if you create an unequal distribution, some bands will have to be narrower than others. With uneven bands, you also need to be extra careful when defining the threshold for each metric that make up the KPI. I made the 4 bands equal, so the thresholds are easier to set.
Making the threshold easy to set is critical. As you design your KPI, you will vrealize that the threshold is the hardest part. In fact, I exclude metric when I do not feel comfortable with its threshold.
The following KPI uses 4 metrics as its input. Each metric has a set of thresholds for green, yellow, orange and red.

![image41.png](images/image41.png)

Now that we have the threshold for each metric, we can convert each metric into green – red. The model is also able to handle when the entire range is defined by a single number. This is useful when you want to define green = 0. That means a single packet loss will put the metric into the yellow range already.
What if anything above 0 is red?
You simply set 0 for green, yellow and orange. Within the red zone, you can set 0 – 1, or 0 to something.

#### Translation

Since the metrics have different units, we need translate to a common unit so we can aggregate.
How do we translate a row?
Let’s use an example. Take the Disk Latency (%) metric. It has range from 0 to 40 ms, which maps into the 0 – 100% using the following mapping table.

![image42.png](images/image42.png)

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

![image43.png](images/image43.png)

That also means that if you have 1 perfect red, and your green are not perfect, you can expect your value to be in the orange category.
This relative weightage plays a key role in determining the threshold. Try to match the actual value so they also correspond to 1x 2x 4x 8x. For example, set the VM disk latency so it goes up from 20 ms  40 ms  80 ms  160 ms. Notice they always double.

![image44.png](images/image44.png)

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

![image45.png](images/image45.png)

It gives us a low orange. It is not red, but close enough to be red. This is why the score is important too, not just the color.
What if your red is not the worst, but barely red? How many borderline red (near 25%) required before a perfect green (100%) is showing red?
The following table shows 1 perfect green score and 11 barely-red scores. What color do you get at the end?

![image46.png](images/image46.png)

Yup, you get orange, not red. It takes many red scores, which makes it practically impossible to get a red if each red is barely there. That’s why your red threshold needs to be 2x your orange threshold. If you make it too big, you will get barely-red in most cases.
In actual environment, you certainly do not want to see red, even in development environment. Each VM will have their own score, but overall you want to see majority green. Use heatmap to show, as it will automatically order them by the value.

![image47.png](images/image47.png)

Chapter 2

# CPU


## Architecture

What used to be Windows or Linux running on a server has transformed into Guest OS  VM  ESXi. There 3 distinct layers resulted in complexity documented in Part 2 Chapter 1. This is not as complex as memory, where you have 4 layers as process running inside a Guest OS represents another layer.
The following infographic shows how the nature of CPU metrics changes as a result of virtualization.

![image48.png](images/image48.png)

Specifically for CPU, we need to be aware of dynamic metric. This means their values fluctuates depending on CPU clock speed and HT effect. As a result, the values are harder to figure out due to lack of observability on the fluctuation. This is not an issue if the range is negligible. It is not. For example, HT can increase the value of CPU Latency anywhere from 0% to 37.5%.

### Guest OS vs VM

CPU metrics for a VM differ greatly from those in the Guest OS. For example, vCenter provides 5 metrics to account for the utilization of VM CPU, yet none directly maps to Windows/Linux CPU utilization.
The following diagram shows some of the differences.

![image49.png](images/image49.png)

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

![image50.png](images/image50.png)

We will explain the above diagram after we cover the counters.

### ESXi ≠ VM + Kernel

Let’s use an example to drive the point. Can you explain the following?

![image51.png](images/image51.png)

Yes, the sum of VM CPU Usage is greater than the ESXi total capacity! How could it be?
The answer is different perspective.
Just like Guest OS and VM have different vantage points, the same complexity happens between VM and ESXi.
The complexity comes from the different vantage points. The metrics at ESXi and VM level measure different things. As a result, the counter at ESXi level cannot be the sum of its VMs + kernel.

![image52.png](images/image52.png)

VM takes the consumer view, meaning it sees the virtual layer. It sees 2 virtual CPUs, unaware of HT. A VM may compete with other VMs, but they are always unaware of one another.
ESXi takes the provider view, meaning it sees the physical layer. It sees 1 core with 2 threads, fully aware of HT. Concept such as Ready and Wait are not applicable as a core is either runs or idle. The kernel practically does not experience contention as it has the highest priority.

![image53.png](images/image53.png)

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

![image54.png](images/image54.png)

Let’s apply the above into the 2 pillars of operations management:
- performance
- capacity
Review the following infographic. Go through it vertically, then horizontally.
What’s your take on the metrics?

![image55.png](images/image55.png)

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

![image56.png](images/image56.png)


#### System on a Chip

As CPU architecture moves towards System on a Chip design, it’s important not to assume that a CPU socket is a simple and linear collection of cores. Take a 64-core AMD EPYC for example. It’s actually made of 8 Core Complex Dies. Each CCD has their own L3 cache. Within a CCD, there are 8 Zen 3 cores, each having their own L2 cache.
The following diagram (taken from page 5 on the AMD link above) shows there its locality effect within a single socket. A thread is closer to another thread on the same CCD. You can see an example of the performance impact on this blog here by Todd Muirhead.

![image57.png](images/image57.png)

Another consideration is NUMA. NUMA Node = Socket / Package, as 1 socket can have >1 package (if you enable Cluster-on-Die feature of Intel Xeon).
The whitepaper from AMD on EPYC 9005 Series processors shows that you can divide the socket into 4 NUMA domain. It shows the following diagram, where each domain has 6 memory DIMMS and 3 memory controllers.

![image58.png](images/image58.png)

Review the NUMA effect in this KB.
From workload perspective, the situation is similar in Intel CPU. The paper from SAP below shows that SAP recommends Intel Sub-NUMA Cluster (SNC) to be enabled:

![image59.png](images/image59.png)

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

![image60.png](images/image60.png)

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

![image61.png](images/image61.png)


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

![image62.png](images/image62.png)

vCenter happens to use 20000 milliseconds as the reporting cycle, hence 20000 milliseconds = 100%.
The above visually shows why Ready (%) + Co-stop (%) needs to be seen in context of Run. Ready at 5% is low when Run is at 95%. Ready at 2% is very high when Run is only 10%, because 20% of the time when the VM wanted to run it couldn’t.
The above is per vCPU. A VM with 24 vCPU will have 480,000 as the total. It matters not if the VM is configured with 1 vCPU 24 vCores or 24 vCPU with 1 vCore each.
You can prove the above by stacking up the 4 metrics over time. In this VM, the total is exactly 80000 ms as it has 4 vCPU. If you wonder why CPU Ready is so high, it’s a test VM where we artificially placed a limit.

![image63.png](images/image63.png)

The formula for the millisecond metrics in VCF Operations are also not normalized by the number of vCPU. The following shows the total adds up to 80000 as the VM has 4 vCPU.

![image64.png](images/image64.png)

This is why you should avoid using the millisecond counter. Use the % version instead. They have been normalized.

#### State Across Multiple vCPU


![image65.png](images/image65.png)


![image66.png](images/image66.png)


### 2 Metrics Not 1

When you order a taxi, you expect 2 numbers on your mobile phone.
- The first number shows time. It tells you how long you have to wait.
- The second number show distance. It tells you how far the car is.
For example, the application tells you the car will reach in 3:50 minutes and it’s 2.8 kilometres away.
What metric you don’t need, hence it’s not provided?
The progress is 78%. A relative metric like this has no purpose as the 100% is undeterministic. The car may experience traffic jam, diversion, or simply makes a wrong turn.
The same thing in CPU, although it’s not obvious to us.
Review the following diagram. What do you observe?

![image67.png](images/image67.png)

Yes, the amount of CPU cycles completed varies. This is the equivalent of distance travelled.
The following table provides the comparison.

![image68.png](images/image68.png)


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

![image69.png](images/image69.png)


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

![image70.png](images/image70.png)

Let’s take a more recent example. The following is Intel Xeon 6520P. It can run at 3.4 GHz, which is 42% higher than the base speed.

![image71.png](images/image71.png)

BTW, there is no setting in ESXi to disable or enable Turbo Boost directly. Yes, I’m aware Windows has it. In the case of ESXi, it’s enabled by default and all you have to do is set the power management.
Thanks to Sushil Kavi, I learned Turbo can still kick in despite the BIOS setting to static high power management. We verified that the value of %A/MPERF in esxtop showing all cores running at 129%.

##### Impacts on ESXi

The following table shows the difference in value if All Core Turbo is 20%.

![image72.png](images/image72.png)

Usage (%) is what vSphere Client UI shows.

##### High Performance vs Balance

Should you always set power management to maximum?
No. ESXi uses power management to save power without impacting performance. A VM running on lower clock speed does not mean it gets less done. You only set it to high performance on latency sensitive applications, where sub-seconds performance matters. VDI, VoIP, video calling, Telco NFV are some examples that are best experienced with low latency.
Review the vSphere 9 performance best practices paper. I’ve copied the part you need to focus below:

![image73.png](images/image73.png)

In mission critical cluster, the overcommit ratio is lower and the VMs tend to be over-provisioned. Or you have 2 hosts for HA as you worry about availability. The end result is your ESXi actual core utilization is not high.

###### Impact on Oversized VM

One downside of an oversized VM is higher risk of some vCPU becoming idle. When the VM becomes idle, the power enters C1 State, but does not go deeper to C2. This enables the VM to quickly spike, which is evident on the spikes at the end.
The following diagram is taken from page 24 of “Host Power Management in VMware vSphere 7.0” whitepaper by Ranjan Hebbar and Praveen Yedlapalli.

![image74.png](images/image74.png)

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

![image75.png](images/image75.png)

Each VM runs for half the time. The CPU Run counter = 50%, because it’s not aware of HT. But is that really what each VM gets, since they have to fight for the same core?
The answer is obviously no. Hence the need for another counter that accounts for this. The diagram below shows what VM A actually gets. The allocation is fixed.

![image76.png](images/image76.png)

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

![image78.png](images/image78.png)

One 1 extreme, the entire CPU only runs 1 core out of 20 cores. If a vCPU runs at 100% and has 0% contention, it will get 1.7 GHz cycles. This is 70% higher than the nominal speed. VM CPU counter such as Demand will report 170%. If you’re not careful, you will think you need more vCPU. In this case, adding more vCPU will make the situation worse.
Let’s say you add a second vCPU. For simplicity, let’s assume they run on the same core. What happens is hyperthreading penalty kicks in. Each only gets 62.5%. So now both vCPU gets 1.06 GHz. So instead of getting 3.4 GHz total, you get 2.12 GHz.
Now let’s look at the other extreme. All the cores are running at the same time. A VM with 1 vCPU will run at 1.3 GHz. Again, since VM CPU Demand is based on 1 GHz, it will report 130%. You then add another vCPU. Now, since all the cores are busy, there is a real chance that the VM 2 vCPU will end up on the same core. In this case, each will run at 812 GHz. You will now be confused, as both runs at 81% yet it seems to have maxed out.
The flow over time in the preceding example is 1.7 GHz  1.3 GHz  1.06 GHz  0.81 GHz, as ESXi CPU scheduler will maximize throughput. The problem is CPU Usage (%) metric mask out this degradation. Couple with the fact that it happens over time as VMs get added into the clusters, it becomes complex to figure out.

![image79.png](images/image79.png)


## VM

Take note that some metrics are for the kernel internal consumption, and not for vSphere administrators. Just because they are available in the UI and have names that sound useful do not mean it’s for your operations. Their name is written from CPU scheduler viewpoint.
I will use the vSphere Client as the source of metrics in the following screenshots.
vSphere provides 6 metrics to track contention.

![image80.png](images/image80.png)

You get 9 metrics for consumption.

![image81.png](images/image81.png)

I group Wait metrics separately as it mixes both contention and consumption.

![image82.png](images/image82.png)


### Contention Metrics

Let’s dive into each counter. As usual, we start with contention type of metrics, then utilization.
Contention has to be judged within the context of consumption. A 2% CPU Ready relative to a 10% CPU Run is “not good”, while 2% Ready on 98% Run is “good”. What I meant is the application may not feel the later, as 98% Run means the application gets a lot of work done. On the other hand, if you have an oversized VM, and it only needs 10% CPU power because business is bad, a 2% CPU Ready means 20% of that business transactions were delayed.
The main 2 counters are Ready and Co-stop. The other 2 counters (Overlap and Other Wait) tend to show much lower value, hence less important operationally. The following shows a typical observation, where both are very high, yet CPU Overlap is near 0.

![image83.png](images/image83.png)

The preceding showed the 20-second peak metric, taken at vCPU level. Taking at the VM level (it has 8 vCPU) shows a similar pattern.
Guest OS is not aware of both Co-stop and Ready. The vCPU freezes. “What happens to you when time is frozen?” is a great way to put it. As far as the Guest OS is concerned, time is frozen when it is not scheduled. Time jumps when it’s scheduled again.
The time it spends under Co-stop or Ready should be included in the Guest OS CPU sizing formula as the vCPU wants to run actually.
If VM utilization is not high, reduce its vCPU while following NUMA best practice.
High CPU Ready can happen at low CPU Co-stop. This means everytime the VM vCPU wants to run, there is enough physical CPU threads to run all the vCPU at the same time. So it’s an all or nothing situation.
The following shows an 8 vCPU VM with ready hit 7.5% multiple times, while Co-stop remains near 0% for days.

![image84.png](images/image84.png)


#### Ready

Ready tracks the time when a VM vCPU wants to run, but ESXi does not have a physical thread (not core) to run it. This could be due to the VM itself (e.g. it has insufficient shares relative to other VMs, it was vMotion) or the ESXi (e.g. it is highly utilized. A sign of ESXi struggling is other VMs are affected too).
When the above happens, ESXi CPU Scheduler places the VM vCPU into Ready state.
Ready also accounts when Limit is applied, as the impact to the vCPU is the same (albeit for a different reason altogether). When a VM is unable to run due to Limit, it accumulates limbo time when sitting in the limbo queue. Be careful when using a Resource Pool, as it can unintentionally cause limits.
Take a look at the high spikes on CPU Ready value. It hits 40%!

![image85.png](images/image85.png)

Notice the overall pattern of the line chart correlates very well with CPU Usage and CPU Demand. The CPU Usage hit 3.95 GHz but the Demand shot to 6.6 GHz. This is a 4 vCPU VM running on a 2.7 GHz CPU, so its total capacity is 10.77 GHz. Why did Usage stop at 3.95 GHz?
What’s causing it?
If your guess is Limit you are right. This VM had a limit set at 4 GHz.
Ready also includes the CPU scheduling cost (normally completed in microseconds), hence the value is not a flat 0 on idle VM. You will notice a very small number. Ready goes down when Guest OS is continually busy, versus when a process keeps waking up and going to sleep, causing the total scheduling overhead to be higher. The following shows Ready is below 0.2% on an idle VM (running at only 0.8%). Notice Co-stop is basically flat 0.

![image86.png](images/image86.png)

CPU Ready tends to be higher, ceteris paribus, in larger VMs. The reason is the chance of running more vCPU at the same time is lower in a busy ESXi host.
Instead of thinking of CPU ready in 2D (as shown in the first chart below), think in 3D where each vCPU moves across time. Each needs to be scheduled, and ideally they run together. The 2nd chart below shows how the 8 vCPUs move across time better.

![image87.png](images/image87.png)


##### Best Practice

I sample 3937 VMs from production environment. For each of them, I took the 20-second peak and not the 5-minute peak.
Why do I take the 20-second?
Unless the performance issue is chronic, CPU Ready tends to last in seconds instead of minutes. The following is one such example.

![image88.png](images/image88.png)

The following shows a different behaviour. Notice initially both metrics are bad, indicating severe CPU ready. However, the gap is not even 2x. I think partly because the value is already very high. Going beyond 50% CPU Ready when CPU Usage is high will result in poor performance. This VM has 16 vCPU.

![image89.png](images/image89.png)

Subsequently, the performance improved, and both values became very similar and remained in a healthy range.
I collected 4 months’ worth of data, so it’s around 35K metrics per VM.
The following screenshot was my result. What do you expect to get in your environment?

![image90.png](images/image90.png)

The first column takes the highest value from ~35K data points. The table is sorted by this column, so you can see the absolute worst from 35040 x 3937 = 137 million data points. Unsurprisingly, the number is bad. Going down the table, it’s also not surprising as the worst 10 are bad.
But notice the average of these “worst metrics”. It’s just 0.97%, which is a great number.
The 2nd column complements the first one. I eliminate the worst 1% of the data, then took the highest. So I took out 350 datapoints. Since VCF Operations collects every 5 minutes, that eliminates the worst 29 hours in 4 months. As you can expect, for most VMs the values improve dramatically. The 2nd column is mostly green.

##### Ready | Readiness

There are 2 metrics provided: Ready (ms) and Readiness (%).
I plotted both of them. They show identical pattern. This is a 4 vCPU VM, hence the total is 80000 ms.

![image91.png](images/image91.png)

The Readiness (%) has been normalized, taking into account the number of vCPU. Notice 80000 ms matches with 100%. If it is not normalized, you will see 80000 as 400%.

#### Co-stop

Co-stop is a different state than Ready because the cause is different. The effect to the VM is the same. A pause is a pause. The Guest OS is unaware of the cause and experience the same contention.
Co-stop only happens on Simultaneous Multi Processor (SMP) VMs. SMP means that the OS kernel executes parallel threads. This means Co-stop does not apply to 1 vCPU VMs, as there is only 1 active process at any given time. It is always 0 on single vCPU VM.
In a VM with multiple vCPUs, ESXi kernel is intelligent enough to run some of the VM vCPUs when it does not have all physical threads to satisfy all the vCPU. At some point, it needs to stop the running vCPU, as it’s too far ahead of its sibling vCPU (which it cannot serve, meaning they were in ready state). This prevents the Guest OS from crashing. The Co-stop metrics track the time when the vCPU is paused due to this reason. This explains why Co-stop tends to be higher on a VM with more vCPUs.
Say one vCPU is in ready state. The remaining vCPU will eventually be co-stopped, until all the vCPUs are co-started. The following diagram show vCPU 0 hit a ready state first. Subsequently, the remaining 7 vCPU hit a co-stop, even though there were actually physical thread to run them.

![image92.png](images/image92.png)

One reason for Co-stop is snapshot. Refer to this KB article for details.

##### Best Practice

The value of Co-stop should be <1% in high performing environment. This is based on 64 million datapoints, as shown on the following pie chart.

![image93.png](images/image93.png)

The value of Co-stop tends to be smaller than Ready, as shown below. Ready and Co-stop may or may not corelate with Usage. In the following chart you can see both the correlation and lack of correlation.

![image94.png](images/image94.png)


#### Overlap

When ESXi is running a VM, this activity might get interrupted with IO processing (e.g. incoming network packets). If there is no other available cores in ESXi, the kernel has to schedule the work on a busy core. If that core happens to be running VM, the work on that VM is interrupted. The counter Overlap accounts for this, hence it’s useful metric just like Ready and Co-stop counter.
The interrupt is to run a system service, and it could be on behalf of the interrupted VM itself or other VM.
Notice the word system services, a process that is part of the kernel. This means it is not for non-system services, such as vCPU world. That’s why the value in general is lower than CPU Ready or even Co-Stop. The value is generally affected by disk or network IO.
Some documentation in VMware may refer to Overlap as Stolen. Linux Guest OS tracks this as Stolen time.
When a vCPU in a VM was interrupted, the vCPU Run counter is unaware of this and continues tracking. To the Guest OS, it experiences freeze. Time stops for this vCPU, as everything is paused. The clock on motherboard does not tick for this vCPU. Used and Demand do account for this interruption, making them useful in accounting the actual demand on the hypervisor. When the VM runs again, the Guest OS experiences a time jump.
Review the following charts. It shows CPU Usage, CPU Overlap and CPU Run. See the green highlights and yellow highlights. What do you notice?

![image95.png](images/image95.png)

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

![image96.png](images/image96.png)

Overlap should be included in Guest OS sizing as the Guest OS wants to run actually. The effect is the same with an unmet Demand.
A high overlap indicates the ESXi host is doing heavy IO (Storage or Network). Look at your NSX Edge clusters, and you will see the host has relatively higher Overlap value versus non IO-intensive VM.

#### Contention

This is a value add by Aria Operations in July 2024. Before that, it’s mapped to the CPU Latency metric.
The formula is.
Contention (%) = Overlap + CoStop + Ready + Other Wait (if less than 1%)
Contention means the vCPU is not getting the CPU time. Using this logic, the CPU frequency is not even applicable as the vCPU is not even running.

![image97.png](images/image97.png)

In most situations, the value will be mostly coming from CPU Ready. The following screenshot shows the CPU Contention is basically identical to CPU Ready

![image98.png](images/image98.png)

Why does the counter include Ready by Limit?
Because we need to separate the what and the why. The fact is the VM faces contention. Whether that is because of VM Limit, insufficient VM Shares, or high ESXi utilization is a different issue.
What is the limitation for including Ready by Limit?
You cannot use the counter to define ESXi or cluster performance. The limit has nothing to do with the cluster.

#### Latency

CPU Latency tracks the “stolen time”, which measures the CPU cycle that could have been given to the VM in ideal scenario. It maps to %LAT_C counter in esxtop.
The diagram shows what it includes. Latency excludes Max Limited in Ready, but it includes Co-stop even if the Co-stop was the result of Limit. It also excludes Other Wait.
Notice that HT and CPU Frequency are effect and not metrics. You can see the impact of CPU Frequency in esxtop %A/MPERF counter.

![image99.png](images/image99.png)

Latency also includes 37.5% impact from Hyper Threading. In ESXi CPU accounting, Hyper Threading is recorded as giving 1.25x throughput, regardless of actual outcome. That means when both threads are running, each thread is recorded as only getting 62.5%. This will increase the CPU Latency value to 37.5%. All else being equal, VM CPU Contention will be 37.5% when the other HT is running. This is done so Used + Latency = 100%, as Used will report 62.5% when the vCPU has a competing thread running.
In the above scenario, what’s the value of CPU Ready?
Yup, it’s 0%.
CPU Latency also accounts for power management. When the clock speed falls below nominal frequency, CPU Latency goes up accordingly.
Because of these 2 factors, its value is more volatile, making it less suitable as a formal Performance SLA. Use CPU Ready for Performance SLA, and CPU Contention for performance troubleshooting.
The following table only shows 5 VM out of 2500 that I analyzed. These 2 metrics do not have good correlation, as they are created for different purpose.

![image100.png](images/image100.png)

In many cases, the impact of both threads running is not felt by the application running on each thread. If you use CPU Latency as formal SLA, you may be spending time troubleshooting when the business does not even notice the performance degradation.
The following screenshot shows CPU Latency went down when both Ready and Co-stop went up.

![image101.png](images/image101.png)

How about another scenario, where Latency is near 0% but Ready is very high? Take a look at this web server. Both CPU Demand and CPU Usage are similar identical. At around 1:40 am mark, both Demand and Usage showed 72.55%, Contention at 0.29%, but Ready at above 15%. What’s causing it?

![image102.png](images/image102.png)

The answer is Limit. Unlike CPU Ready, it does not account for Limit (Max Limited) because that’s an intentional constraint placed upon the VM. The VM is not contending with other VMs. VMware Cloud Director sets limit on VM so this counter will not be appropriate if you aim to track VM performance using Contention (%) metric.
Here is a clearer example showing latency consistently lower than Ready due to limit.

![image103.png](images/image103.png)

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

![image104.png](images/image104.png)

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

![image105.png](images/image105.png)

I was curious if the value corelates with CPU Ready or Co-stop. From around 4000 production VM in the last 1 month, the answer is a no.

![image106.png](images/image106.png)

Since snapshot is another potential culprit, let’s compare with disk latency and outstanding IO.
What do you expect?

![image107.png](images/image107.png)

Again, negative corelation. None of the VMs with high VM Wait is experiencing latency. Notice I put a 99th percentile, as I wanted to rule out a one-time outlier. I’m plotting the first VM as the value at 99th is very near to the max, indicating sustained problem.

![image108.png](images/image108.png)

It turned out to be true. It has sustained VM Wait value around 15% (above is zoomed into 1 week so you can see the pattern).
I’m curious why it’s so high. First thing is to plot utilization. I checked Run, Usage and Demand. They are all low.

![image109.png](images/image109.png)

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

![image110.png](images/image110.png)


#### Run | Net Run

Run is when the Guest OS gets to run and process instruction. It is the most basic counter among the CPU consumption metrics. It’s the only counter not affected by CPU frequency scaling and hyper threading. It does not check how fast it runs (frequency) or how efficient it runs (SMT).
Run at VM level = Sum of Run at vCPU levels
Since the unit is millisecond, this means the value of CPU Run at VM level can exceed 20000 ms in vCenter.
The following screenshot shows CPU Run higher than CPU Used. We can’t tell if the difference is caused by power management or hyperthreading, or mix of both.

![image111.png](images/image111.png)

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

![image112.png](images/image112.png)

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

![image113.png](images/image113.png)

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

![image114.png](images/image114.png)


###### Usage (MHz)

Turbo Boost’s impact on Usage is real. In the following, you can see the value exceeds the total capacity by a sizable amount.

![image115.png](images/image115.png)

Let’s do a calculation so you can quantify the impact of power management.
Review the following example. This is a single VM occupying an entire ESXi.
The ESXi has 12 cores with nominal frequency of 2.4 GHz. The number of sockets does not matter in this case.
Since HT is enabled, the biggest VM you can run is a 24 vCPU. The 24 vCPU will certainly have to share 12 cores, but that’s not what we’re interested here.
What do you expect the VM CPU Usage (GHz) when you run the VM at basically 100%?

![image116.png](images/image116.png)

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

![image117.png](images/image117.png)

Around 12 May, the VM experienced some contention. That’s why Demand was higher than Usage.

###### Usage vs Net Run

Usage is greatly affected by CPU speed and power management.
As a result, it’s more volatile than CPU Run. What do you notice on the following chart?

![image118.png](images/image118.png)

CPU Usage is both higher and lower than CPU Net Run. CPU Net Run is CPU Run minus CPU Overlap, so it’s closer to Usage. I hide CPU Ready as the value was basically 0%.
Generally speaking, during high utilization, Usage (%) will over-report due to CPU turbo boost.

![image119.png](images/image119.png)

During low utilization, Usage (%) will under report due to power savings

![image120.png](images/image120.png)


#### CPU Usage Disparity

This metric is required to convince the owners of the VM to downsize their large VMs. It’s very common for owners to refuse sizing it down even though utilization is low, because they have already paid for it or cost is not an issue.
Let’s an example. This VM has 104 vCPU. In the last 90 days, it’s utilization is consistently low. The Usage (%) counter never touch 40%. Demand is only marginally higher. Idle (%) is consistently ~20%.

![image121.png](images/image121.png)

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

![image122.png](images/image122.png)

To answer, we need to plot each vCPU one by one.
Below is what we get.

![image123.png](images/image123.png)

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

![image124.png](images/image124.png)

Demand is identical to Usage, despite Contention (%) being near 0%.
The reason is Demand is a kernel internal metric. From the kernel perspective, the VM did not demand as limit is intentionally set.
In the event the VM vCPU is running on a core where both threads are busy, the value of Usage will be 37.5% lower, reflecting the fact that the VM only gets 62.5% of the core. This makes sense as the HT throughput benefit is fixed at 1.25x.
If there is no competition for resource, Demand and Usage will be similar.
Take a look at the following screenshot from vCenter. It’s comparing Demand (thick line) and Usage (grey line)
What do you notice?

![image125.png](images/image125.png)

How can Usage be higher than Demand at some of the point?
The reason is Demand is averaged over a longer time, giving it a steadier value. That’s why the peak is shorter but wider. Notice the average over 1 hour is higher for Demand.
Due to Turbo Boost, Demand (MHz) and Usage (MHz) can exceed 100%. The following is a 32-vCPU Hadoop worker node. Notice it exceeds the total capacity multiple times, as total capacity is based on base clock speed. Demand and Usage are identical as it’s the only VM running and the host has more than 32 cores, hence there is 0 issue.

![image126.png](images/image126.png)

Okay, now that you have some knowledge, let’s test it 😊
Quiz Time! Looking at the chart below, what could be causing it?

![image127.png](images/image127.png)

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

![image128.png](images/image128.png)

ESXi typically uses another core for this work instead of the VM vCPU, and put that that VM vCPU in wait state. This work has to be accounted for and then charged back to the associated VM. The System counter tracks this. System counter is part of VMX world of the VM.
Guest OS isn’t aware of the 2nd processing. It thinks the disk is slower as it has to wait longer.
If there is snapshot, then the kernel has to do even more work as it has to traverse the snapshot.
The work has to be charged back to the VM since CPU Run does not account for it. Since this work is not performed by any of the VM CPU, this is charged to the VM CPU 0. The system services are accounted to CPU 0. You may see higher Used on CPU 0 than others, although the CPU Run are balanced for all the VCPUs. So this is not a problem for CPU scheduling. It’s just the way the kernel does the CPU accounting.
The System counter is not available per vCPU. Reason is the underlying physical core that does the IO work on behalf of the VM may be doing it for more than 1 vCPU. There is no way to break it down for each vCPU. The following vCenter screenshot shows the individual vCPU is not shown when System metric is selected.

![image129.png](images/image129.png)

ESXi is also performing IOs on behalf of all VMs that are issuing IOs on that same time, not just VM 1. The kernel may serialize multiple random IO into sequential for higher efficiency.
Note that I wrote to CPU accounting, not Storage accounting. For example, vSphere 6.5 no longer charges the Storage vMotion effort to the VM being vMotion-ed.
Majority of VMs will have System value less than 0.5 vCPU most of the time. The following is the result from 2431 VMs.

![image130.png](images/image130.png)

On IO intensive VM like NSX Edge, the System time will be noticeable, as reported by this KB article. In this case, adding more vCPU will make performance worse. The counter inside Linux will differ to the counter in vSphere. The following table shows high system time.

![image131.png](images/image131.png)


#### Reservation


![image132.png](images/image132.png)

The number is only available in MHz or GHz, not in vCPU. That means when you move the VM to an ESXi of different frequency, you need to adjust the number manually.

### Quiz!

By now I hope you vrealize that the various “utilization” metrics in the 4 key objects (Guest OS, VM, ESXi and Cluster) varies. Each has their own unique behaviour. Because of this, you are right to assume that they do not map nicely across the stack. Let’s test your knowledge 😊

#### VM vs ESXi

Review the following chart carefully. Zoom in if necessary.

![image133.png](images/image133.png)

The vCenter chart above shows a VM utilization metrics from a single VM. The VM is a large VM with 24 vCPUs running controlled CPU test. The power management is fixed so it runs at nominal clock speed. This eliminates CPU frequency scaling factor.
The ESXi only has 12 cores. Hyper threading is enabled, so it has 24 threads.
The VM starts at 50% “utilization”, with each vCPU pinned to a different physical core. It then slowly ramps up over time until it reaches 100%.
Can you figure out why the three metrics moved up differently? What do they measure?
Now let’s look at the impact on the parent ESXi. It only has a single VM, but the VM vCPU matches the ESXi physical cores. The ESXi starts at 50% “consumption”, then slowly ramp up over time until it reached 100%.

![image134.png](images/image134.png)

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

![image135.png](images/image135.png)

Now let’s see the Used (ms) metric.
It’s also flat, around 18600 ms. Using the 20000 as the 100%, it’s around 93%. This is fairly expected, as I think Usage (MHz) contains non vCPU worlds (e.g. MKS)
Now let’s plot Run (ms) alongside. Why is it much lower?

![image136.png](images/image136.png)

Why is Used consistently 41% higher than Run?
Answer is CPU Ready.
If you sum up Run + Ready  + Overlap + Idle, it will be 20000.

![image137.png](images/image137.png)


#### When Run is higher than Used

Now let’s look at the opposite scenario.
This VM is a 64-bit Ubuntu running 4 vCPU. Used (ms) is around 44% of Run (ms). The VM had minimal System Time (ms) and Overlap (ms), so Used is basically lowered by both power savings and CPU SMT.

![image138.png](images/image138.png)

In this example, if Run is far from 100% and the application team want faster performance, your answer is not to add vCPU. You should check the power management and CPU SMT, assuming the contention metrics are low.

## ESXi

Throughout this book, I always cover the contention metrics first, then consumption. Why is it that I swap the order for ESXi Host?
Because in the provider layer there is no contention. The one that faces contention is the consumer (VM).

### Consumption Metrics

vSphere Client UI provides 6 counters to track ESXi CPU “consumption” and 1 to track reservation.

![image139.png](images/image139.png)

Why 6?
Let’s dive into the utilization metrics with a quiz.

#### Quiz: 50% or 75% or 100%?!

Hope you like the tour of VM CPU accounting. Can you apply that knowledge into ESXi and explain the following?

![image140.png](images/image140.png)

The above is an ESXi host, showing 3 types of utilization metrics.
- One shows ~50%, indicating you have capacity.
- The second one shows 100%, indicating you do not have capacity. BTW, this was the old version, where the metric was capped at 100%.
- The 3rd shows ~70%.
Which metrics do you take for the ESXi CPU “consumption” then?
They also do not move in tandem. Towards the end, both the black line and green line fluctuate, but the blue one was flat at 100%. Why?
Since the graph is a bit small, let’s zoom in:

![image141.png](images/image141.png)

Notice they have similar pattern, but their sensitivity differs.
- Why is Usage (%) = 100% when Utilization (%) is around 47%? The gap is more than double. What could be causing it?
- Why is Utilization (%) fluctuating yet Usage (%) remains constant? Notice both Utilization varies between 45% and 55% while Usage remains flat at 100%
- Why is Core Utilization (%) in the “middle”? What does it actually measure then?

##### High Load Example

The preceding example shows Utilization (%) mostly below 50%. Let’s pick the opposite example, where at least half the threads are utilized. What do you expect the value of Usage (%) and Core Utilization (%)?

![image142.png](images/image142.png)

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

![image143.png](images/image143.png)

Going back to our example, here are metrics reported:
- Thread Utilization (%) for HT 0 = 10 seconds / 20 seconds = 50%
- Thread Utilization (%) for HT 1 = 10 seconds / 20 seconds = 50%
- Core Utilization (%) for entire core = 15 seconds / 20 seconds = 75%
BTW, in vSphere Client performance tab, you can’t select a core if you enable HT. You can only choose PCPU, which is a thread. So what happens on the Core Utilization counter at thread level?
Does it get split into half?
As you can see below, no. The value is duplicated.

![image144.png](images/image144.png)

Notice in the above chart, the 2 have identical value.
Thread Utilization (%), on the other hand, will be different. Each thread has different value.

![image145.png](images/image145.png)

If you simply sum them up, you get more than 100%, so don’t! Their context is a single thread.

![image146.png](images/image146.png)

Now let’s roll this up to the ESXi level. The following shows a tiny ESXi with 2 cores, where each core has 2 threads.

![image147.png](images/image147.png)

The metrics at ESXi level is
- CPU Thread Utilization (%) = (50% + 50% + 100% + 0% ) / 4 = 50%.
- CPU Core Utilization (%) = (75% + 100% ) / 2 = 87.5%
Thread Utilization = 50% because each thread is counted independently. There are 4 threads in the preceding ESXi, each runs 50%, so the average at ESXi level is 50%. This counter basically disregards that HT does not deliver 2x the throughput.
This is why the Core Utilization (%) will tend to be consistently higher than Thread Utilization (%). The following chart demonstrate that.

![image148.png](images/image148.png)

Now let’s go back to the chart shown earlier. Can you now explain Thread Utilization (%) and Core Utilization (%)?
Great! Let’s move to the next one.
In the following example, this ESXi has no hyper-threading. What do you notice?

![image149.png](images/image149.png)

Yup, the Core Utilization is identical with Thread Utilization.

#### Core vs Thread


![image150.png](images/image150.png)


![image151.png](images/image151.png)

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

![image152.png](images/image152.png)

The above translates that the total per core should be 20000, since there are 2 threads per core.
You can confirm the above ESXi is idle by plotting idle at the host level. The sum is near 640000 ms.

![image153.png](images/image153.png)

If HT is not available, then there is no counter at thread level. The counter at the core level adds up to 20000 ms.

![image154.png](images/image154.png)


#### Used | Usage

You are now ready to tackle the next metrics, which are Used (ms), Used (%), Usage (%) and Usage (MHz). Used (%) is used in esxtop, while vSphere Client UI uses the other 3 metrics.
vSphere Client uses the name Used instead of Usage. But in the metrics chart page, it uses Usage. As a result, I’m going to assume that Used (MHz) = Usage (MHz) as vSphere Client UI uses them interchangeably. While I’ve found differences in rare cases, it is safe to take as Usage = Used.
I only see the use case for Usage (MHz). The other 2 units (second and percentage) are not needed. Using millisecond is hard to account for “how fast you run” and “how efficient you run”. With MHz, we gain an additional dimension, which is speed. We can plot the speed across time.
If you have a specific need on Used (ms), Used (%) and Usage (%), reach out to me with the reason and happy to provide the documentation on these 3 metrics.
Usage (MHz) relates to Utilization in a similar way that VM Usage metric relates to VM Run metric. The difference is a physical thread does not experience overlap, and system is not applicable as it’s run in the kernel.
Here is how Utilization and Usage are related at PCPU level:

![image155.png](images/image155.png)

Used is calculated based on a hardware counter called Non-Halted Core Cycle (NHCC). Logically, the higher the CPU clock speed, the more cycles you complete. That’s why the value gets higher in turbo boost.
From the diagram above, you can see that Usage accounts for 2 factors that Utilization does not:
- A physical thread is either executing (running) or halted (idle). Its execution will be less efficient if its paired thread is also running at the same time.
- While it’s running, it can run at lower/higher CPU clock speed due to power management.

##### Usage

vCenter adds this counter, meaning it does not exist at ESXi level.
You see both the Capacity of 35.18 GHz and Used of 11.3 GHz. There is no concept of Usable Capacity in vSphere, so the Free amount is basically Capacity – Used.

![image156.png](images/image156.png)

The Used CPU is summary.quickStats.overallCpuUsage.
The value above is likely some average of say 5 minutes as it remains static for a while, and it does not exactly match the number below as the roll up period is not the same.

##### Usage and 100%

Usage no longer capped at 100% of total capacity at the nominal frequency. This was fixed in Aria Operations 8.18. In a highly utilized host, you will see Usage exceed it. This is indeed a desirable situation as you bought the host to be used as much as possible.

![image157.png](images/image157.png)


#### Consumed

When vSphere UI lists ESXi Hosts, it typically includes the present utilization. It lists the metrics as Consumed CPU (%) and Consumed Memory (%).

![image158.png](images/image158.png)

Consumed CPU maps to CPU Usage (%). Consumed Memory (%) maps to Memory Consumed (KB).
To confirm it, simply plot CPU Usage value. The last value is what you see at the table.

![image159.png](images/image159.png)

You also see them in vSphere Host Client.

![image160.png](images/image160.png)

As a bonus, you get the breakdown by CPU package.

#### Demand


![image161.png](images/image161.png)

This is an internal counter. It’s for the kernel CPU scheduler to optimize the running of VM as the kernel is aware that hyper-threading has performance impact. As a result, demand looks at different context than Utilization/Used. The value you see at ESXi is the summation of all the VMs, not physical threads.
Demand is consumer-view, while Usage is provider view. Now you know why Demand is not available on a per-core or thread basis. If a host has no VM, Demand will show flat 0. Usage will not show 0 as it includes the kernel.

![image162.png](images/image162.png)

Demand includes the reservation by VM.
Usage includes kernel actual utilization. The following shows Demand remains perfectly flat at 10.21% for weeks. The ESXi has 0 running VM. The only explanation is the kernel reservation.

![image163.png](images/image163.png)

The following chart shows the same ESXi, where the Demand (MHz) = Overhead (MHz). Overhead tracks the kernel reservation.

![image164.png](images/image164.png)

If the kernel reservation is lower than the kernel utilization, then Demand could be lower than Usage. The following example shows that.

![image165.png](images/image165.png)

Once there is enough utilization, defined as some VMs are sharing the same cores, Demand will be higher than Usage. The following screenshot shows Demand being consistently higher

![image166.png](images/image166.png)


#### Summary


![image167.png](images/image167.png)


##### Comparison

Let’s evaluate all the possible scenarios so you can compare the values returned by the metrics. We will use a simple ESXi with 2 cores. Each core has 2 threads. In each of the scenario, a thread is either running or not running. There is no partial run within a thread as that’s mathematically covered in our scenarios.
I will also use 20000 ms as that’s more familiar. The following table shows an ESXi with 2 cores. There are 6 possible permutations in their utilization.

![image168.png](images/image168.png)

The table shows clearly that Used splits the Utilization into 2 when both threads are running.
Look at scenario 1. While Utilization charges 20000 ms to each thread, Used charges 10000. This is not intuitive as ESXi considers HT to deliver 1.25x. Personally I find 12500 easier to understand. The good news is this number is normalized back when it is rolled up to the ESXi host level.
How will those scenarios roll up at the ESXi level?
The following table shows the 4 metrics (Utilization, Used, Core Utilization, Usage). I have expressed each in % so it’s easier to compare.
There are 6 different scenarios, so logically there should be 6 different values. But they are not, so I added my personal take on what I like them to show. I’m keen to hear your thought.

![image169.png](images/image169.png)

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

![image170.png](images/image170.png)

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

![image171.png](images/image171.png)

Let’s zoom on an ESXi with a very high utilization.
Take a look at the 4 numbers below. Demand is consistently around 130%.
With such a high demand value, it’s no surprise that Usage is 100% flat out.
Do we have a performance problem? What can you deduce from the other 3 numbers?

![image172.png](images/image172.png)

Core Utilization at 85% is not very high. The box still has 15% of the cores not running. The box has 40 cores 80 threads. Unless there is limit, there are still 6 cores available.
Utilization at 62% is moderate. This means ~38% x 80 threads, or 30 threads are available.
Based on the raw utilization above, I expect the CPU ready to be low.
Let’s check. What’s your conclusion from below?

![image173.png](images/image173.png)

The value peaks at 128 seconds.
But that’s for the entire box. There are 250 vCPU at that time.
Dividing the value, it’s only 514 ms per vCPU. This translates into 2.5%, a relatively low number.
Let’s validate this further by going into each VM.
I took the average of the entire 7 hour period, and got around 2% for Ready and less than 0.1% for Co-Stop. This is pretty good considering these VMs are large. They are 15.29 vCPU on average. Some of them also have limit, which could contribute to the CPU read.

![image174.png](images/image174.png)

Now let’s pick the opposite example.
The following chart shows an ESXi with low utilization. What do you notice?

![image175.png](images/image175.png)

This time around, Usage is lower than Core Utilization.
This ESXi is not even 50% utilized, as the core utilization shows 48%. The kernel decides that it could complete the job with less power, and clocks down the core.

#### Reservation

There is only 1 metric provided, which is Reserved Capacity (MHz). Compare this with memory, which provides 3 counters. Why is that so?
Review the System Architecture section. In short, it is not applicable to CPU as due to its highly transient nature. When the VM is not running, the reserved capacity can be used by other VM. This differs to memory, which is “sticky” as it’s a form of storage.
The metric does not include hypervisor reservation.

![image176.png](images/image176.png)


#### Peak Core CPU Usage

An ESXi with 72 CPU cores will have 144 threads. You will not be able to see when a single core peak at ESXi Host level as it’s the average of 144 metrics. If you are concerned that any of them is running hot, you need to track the peak among them.
Imbalance among the cores happen because when a VM runs, it runs on as few core as possible, not spread out to all ESXi cores. It’s more efficient to schedule that way, as will requires less context switches.
The following shows an ESXi where 3 of the threads hit >90%

![image177.png](images/image177.png)

The average, however, is low. The total usage can hit 5600% as there are 56 threads, hence the total is only hovering 1100%, which translates into 20%.

![image178.png](images/image178.png)

Peak CPU Core Usage (%) tracks the highest CPU Usage among the CPU cores. A constantly high number indicates that one or more of the physical cores has high utilization. So long the highest among any cores at any given time is low, it does not matter which one at a specific point in time. They can take turn to be hot, it does not change the conclusion of troubleshooting. Max() is used instead of 95thpercentile as both result in the same remediation action, and Max() can give better early warning.
The imbalance value among the cores is not needed because it is expected when utilization is not high.

#### Metrics to Avoid

Do not use the following metrics. Use the recommended metric instead.

##### CPU Utilization for Resources

Under the System metric group, you will see 17 metrics with names starting with “CPU Utilization for Resources”.

![image179.png](images/image179.png)

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

![image180.png](images/image180.png)


### Contention Metrics

The nature of average is also one reason why ESXi “consumption” does not correlate to ESXi “contention”. The 4 highlighted area are examples where the metrics don’t correlate, even go the opposite way in some of them. Can you guess why?

![image181.png](images/image181.png)

The above picture is a little too small. The following ESXi has total capacity of 111 GHz. So Demand hit 315%! Sum of VM CPU Usage also unbelievably high at 143%. Sure, Ready + CoStop were high at that moment, but how do you explain these 2 exceed Total Capacity?

![image182.png](images/image182.png)

These are the reasons why they don’t match:
- One looks at physical CPU, the other the virtual CPU. One looks at ESXi, while the other looks at VM.
- Hyperthreading and Power Management.
- Imbalance utilization. There are many VMs in this host. Their experience will not be identical.
- Limit may impact the VM, either directly or via resource pool.
- CPU pinning, although this rarely happens.
So what metrics should you use?
Here are the latency metrics provided by vSphere Client.

![image183.png](images/image183.png)

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

![image184.png](images/image184.png)

From the process’ point of view, this technique provides a contiguous address space, which makes memory management easier. It also provides isolation, meaning process A can’t see the memory of process B. This isolation provides some level of security. The isolation is not as good as isolation by container, which in turn is inferior to isolation by VM.
Virtual memory abstraction provides the possibility to overcommit. Microsoft Windows may only have 16 GB of physical RAM, but by using pagefile the total memory available to its processes can exceed 16 GB. The process is unaware what is backing its virtual address. It does not know whether a page is backed by Physical Memory or Swap File. All it experiences is slowness, but it won’t know why as there is no counter at process level that can differentiate the memory source.
On the other hand, some applications manage its own memory and do not expose to the operating system. Example of such applications as are database and Java VM. Oleg Ulyanov shared in this blog SQL Server has its own operating system called SQLOS. It handles memory and buffer management without communicating back to underlying operating system.

![image185.png](images/image185.png)

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

![image186.png](images/image186.png)

Read further and you will see that the kernel large page setting contributes more to ESXi capacity and the VM performance.

#### Relationship

Let’s put the 4 layers in a diagram, showing how a page maps across the 4 layers.
What can we notice from the diagram?

![image187.png](images/image187.png)

Yup, a few things:
- Balloon did not map to physical layer. Notice there is no arrow on the yellow blocks
- The physical memory is “shared” between VM and hypervisor own processes, meaning you need to manage them as one. Sum their utilization to form the total consumption.
- At the physical layer, there can be host cache and tiered memory, and not just DIMM.
- Just to be complete, the mapping may not be to the closest DIMM. You can have NUMA effect.
The VM Monitor for each VM maps the VM pages to the ESXi pages. This page mapping is not always 1:1. Multiple VM pages may point to the same ESXi pages due to transparent page sharing. On the other hand, VM page may not map to ESXi page due to balloon and swapped. The net effect is the VM pages and ESXi pages (for that VM) will not be the same, hence we need two sets of metrics.
Let’s zoom into the key metrics that form a single VM.

![image188.png](images/image188.png)

Take note the difference between the VM perspective and the ESXi perspective.
- The VM looks at the “input”, while ESXi looks at the “output”. For example, VM metrics will report 3 pages being shared, while ESXi will report 1 page of the result shared page.
- Balloon does not exist at physical view as the page has been removed. It’s not pointing to any block in the ESXi memory address space.
Further reading: vSphere Resource Management technical paper.

### Guest OS vs VM

Both come with dozens of metrics. Compared with Guest OS such as Windows, can you notice what’s missing and what’s added?
The following diagram compares the memory metrics between VM and Guest OS,

![image189.png](images/image189.png)

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

![image190.png](images/image190.png)

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

![image191.png](images/image191.png)

What do you think you will see inside Windows?
Will the Windows In Use counter show that it’s using 0 GB or somewhere near there? You know that it won’t show 0 GB as it’s impossible that any OS does not use any memory while it’s running. So what number will the In Use counter show?

![image192.png](images/image192.png)

It’s showing 7.2 GB! That’s nowhere near 0%.
Look at the chart. What do you notice?
It portrays that it has been constantly or actively using that much of memory. In reality, we know it’s idle because ESXi is the one doing the actual reading and writing. The other proof that it is idle is Windows actually compressed 1.5 GB of this 7.2 GB.
One possible reason why Windows is showing high usage when there is none is applications that manage their own memory. These applications will ask for the memory upfront in 1 contiguous block. You can see in the example below:

|  | You can see that java.exe takes up 26 GB. JVM (Java Virtual Machine) manages that memory and Windows can’t see inside this block. Windows sees the entire block as used and committed, regardless of the application actually uses it or not. BTW, the above is taken from old blog article of Manny Sidhu. The blog no longer available, hence I could not provide the link. |
| --- | --- |


![image194.png](images/image194.png)

I hope the above simple experiments shows that you should use the right counter for the right purpose.

## VM

Just like the case for CPU, some metrics are for the kernel consumption, not your operations.

### Overview

For performance use case, the only counter tracking actual performance is Page-fault Latency.

![image195.png](images/image195.png)

Next, check for swapping as it’s slower than compressed. You get 6 metrics for it

![image196.png](images/image196.png)

Next is compressed

![image197.png](images/image197.png)

Host Cache should be faster than disk (at least I assume you designed it with faster SSD), so you check it last.

![image198.png](images/image198.png)

Lastly, there is the balloon.

![image199.png](images/image199.png)

Wait! Where is the Intel Optane memory metrics?
It does not exist yet, as that’s supposed to be transparent to ESXi.
Performance is essentially the only use case you have at VM level. For Capacity, you should look at Guest OS. The VM capacity metrics serve as input to the host capacity and are used in determining the VM memory footprint (e.g. when migrating to another ESXi).
You’ve got 5 metrics, with consume being the main one.

![image200.png](images/image200.png)

I’m going to add Active next, although I don’t see any use case for it. It’s an internal counter used by the kernel memory management.

![image201.png](images/image201.png)

Lastly, you get the shared pages and 0 pages.

![image202.png](images/image202.png)

Now that we’ve got the overview, let’s dive into the first counter!

### “Contention” Metrics

I use quote because the only true contention counter is latency. The second reason is VCF Operations has a metric called Contention, which is actually vCenter counter called latency.

#### Latency

Memory Latency, aka "Page-fault latency" is tracking the amount of time a vCPU spends waiting on the completion of a page fault. Its value is mostly swap wait, with a bit of page decompression / copy-on-write-break. The counter is called %LAT_M in esxtop.
The latency metric is highly corelated with the swap-in rate.

![image203.png](images/image203.png)

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

![image204.png](images/image204.png)


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

![image205.png](images/image205.png)

The higher the value is for balloon, swapped, and compressed, the higher the chance of a performance hit happening in the future if the data is requested. The severity of the impact depends on the VM memory shares, reservation, and limit. It also depends upon the size of the VM's configured RAM. A 10-MB ballooning will likely have more impact on a VM with 4 GB of RAM than on one with 512 GB.
How high?
Let’s take a VM and plot its value over time. The VM is configured with 16 GB memory. As you can see, the value in the last 4 weeks is a constant 16 GB.

![image206.png](images/image206.png)

The line is a perfect flat. Both the Highest value and Lowest value show 16,384 MB.
The VM was heavily ballooned. 63.66% of its memory was reclaimed. That’s a whopping 10,430 MB!

![image207.png](images/image207.png)

Notice something strange.
The Ballooned did not change at all for 4 weeks.
That likely means the Guest OS is not active. It never needs any of those 10+ GB that was ballooned out.
So Guest was playing with the remaining 6 GB. It never page in those pages.
So what do you expect if we plot Granted + Swapped + Compressed?
You got it. A flat line.

![image208.png](images/image208.png)


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

![image209.png](images/image209.png)

The above are the main metrics that you should track. vSphere provides additional visibility as swap and compress are complex process.

##### Transition

Read the following carefully, as there will be a quiz after this.

| Input | This is the number of pages that will be subjected to compression and swapping.  It’s not the number of pages that was processed already.  The metric is called Swap Target. Think of it as Compress-Swap Target as the page that cannot be compressed is swapped. |
| --- | --- |
| Process | You need metrics to track the progress as it’s happening. This complements the result as it covers how much memory is compressed or swapped at any given period.  A 10 MB compressed in 1 second is different to 10 KB compressed over 1000 seconds. Both results in the same amount, but the problem is different. One is an acute but short fever; the other is low grade but persistent fever. You don’t want neither, but good to know what exactly you’re dealing with. This is the rate of  compression decompression swapping from DIMM into the swap file. swapping from the swap file into the DIMM The In and Out can happen at the same, as they typically involve different pages. You can have 10 MB being decompressed and another 10 MB being compressed. Your swap file size is unchanged but the content has changed. This is why Swapped is not Swapped In – Swapped Out.  Swap-out does not mean there is contention. If you are lucky, the page being swapped is not required. However, swap out means the ESXi was under memory pressure or the VM hit a limit. Swap-in means there is contention. The page was called for, hence it was brought in. Plot them together and you will see a high correlation. Swap-in doesn't happen because there's memory pressure on the host. Swap-in just means there was memory pressure in the past and now the guest OS wants some of that data. |
| Output | You need a metric to track the result and the savings.  For swap, 3 counters are provided Swapped  Swapped Out Swapped In For compress, the compressed-in and compressed-out are not provided. You do get the savings from compression. |


###### Example


![image210.png](images/image210.png)

Swapped Out Rate was 6331.93	+ 5026.4 + 1882.13 + 615.86. This gives a total of 13856. Since it’s sustained for 300 seconds, we multiply by 300 and then divide by 1024 to get the total of 4059 MB being swapped out. This is pretty close to the 4157 MB of Swapped.
There is no Swap In. The rate metric was showing 0 during the entire period.
Consumed drops by 4868 MB (7719 – 2851). There were other factors impacting it.

##### Quiz

Explain why swap and compress move in opposite direction in the following chart.
This VM is configured with 64 GB of memory. So it experienced high amount of swapping and compressed in the last 7 days. It peaked at 20 GB, which is really bad.

![image211.png](images/image211.png)

Let’s plot consumed and granted. What’s your conclusion?

![image212.png](images/image212.png)

Why is consumed basically flat for 7 days?
Granted looks rather normal as it hovers above consumed, with some movement.
If you guess Limit, you’re right! Let’s plot all the counters together now.

![image213.png](images/image213.png)

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

![image214.png](images/image214.png)

It’s given a bad limit of 2 GB.
In the last 7 days, we can see the limit is a perfectly flat line. It’s 2.12 GB as it includes the overhead value.

![image215.png](images/image215.png)

The VM, or rather the Guest OS, did ask for more. You can see the demand by looking at the Granted or Compressed or Swapped metrics. I’m only showing Granted here:

![image216.png](images/image216.png)

Because of the limit, the Consumed counter did not past the 2 GB. It’s constantly hovering near it as the VM is asking more than that.

![image217.png](images/image217.png)

What do you expect to see the Balloon value?
If Balloon has something to do with it, it would not stay a perfectly flat line.
But this is what you got. A perfectly flat line, proving Limit had nothing to do with Balloon.

![image218.png](images/image218.png)


### Consumption Metrics


![image219.png](images/image219.png)


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

![image220.png](images/image220.png)

The same vantage point reason is why Limit impacts Consumed, but not Granted. The following is VM is a Windows 2016 server, configured with 12 GB of RAM, but was limited to 8 GB. Limit is shown as the flat line in cyan near the bottom, hovering just above the pink line).

![image221.png](images/image221.png)

The purple line jumping up and down is Granted. Granted ignores the limit completely and runs way above it.
Notice Consumed (KB) is consistently below Limit. Granted does not exceed 12 GB as it does not exceed configured.

##### Compressed + Swapped

Granted does not include Compressed + Swapped because the page is no longer directly accessible without some extra processing.
The following shows Granted move up while the other 2 metrics went down.

![image222.png](images/image222.png)

Summing up the above resulted in a delta of 0.7 MB.

##### Ballooned

Balloon driver removes page from the granted list. Granted does not include ballooned as the page is not functionally used. Technically, Guest OS memory counters include it so don’t forget to exclude it when working out the Guest OS utilization.

![image223.png](images/image223.png)


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

![image224.png](images/image224.png)

Review the last row. What are the total savings?
Granted – Consumed = (103.26 – 79.56) = 23.7 TB
Savings = 29.83 TB – 23.7 TB = 6.13 TB.
That’s around 6% saving.
Profile your own environment. What savings do you get?
Savings does not include compressed as that is not true saving. Zipped results in performance impact, while saving should not.

##### Zero

A commonly shared page is certainly the zero page. A common technique to initialize space is to simply write 0.
The following screenshot shows the 2 moved in tandem over several days.

![image225.png](images/image225.png)


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

![image226.png](images/image226.png)

When you see Consumed is lower than Guest OS Used, check if there are plenty of shared pages. Consumed does not include shared page.
The following screenshot shows Guest OS Used consistently higher. It’s also constant, around 156 GB throughout. Consumed was relatively more volatile, but never exceed 131 GB. The reason for it is Shared. Notice the value of page with all 0 is high, around 61 – 63 GB.

![image227.png](images/image227.png)


##### Ballooned

This 64-bit CentOS VM runs My SQL and is configured with 8 GB of RAM.
Linux was heavily ballooned out (default limit is around 63%). Why is that so?

![image228.png](images/image228.png)

The answer for this VM is we set a limit to 2 GB. As a result, Consumed could not exceed 2 GB. Since the VM needed more, it experienced heavy ballooning.

![image229.png](images/image229.png)

Did you notice the common deep in Balloon and Consumed?
Can you explain them?
Balloon dropped by 0.46 GB then went back to its limit again. This indicated Guest OS was active.
Consumed went down from 2.09 GB to 1.6 GB, and then slowly going back up. Why did it suddenly consume 0.4 GB less in the span of 20 minutes? Both the configured limit and the runtime limit did not change. They were constant at 2 GB. This makes sense, else the Consumed would not be able to slowly go up again.

![image230.png](images/image230.png)

There must be activity by the VM and pages were compressed to make room for the newly requested pages. The Non Zero Active counter shows that there are activities.

![image231.png](images/image231.png)

The pages that are not used must be compressed or swapped. The Swapped value is negligible, but the Compressed metric shows the matching spike.

![image232.png](images/image232.png)

So far so good. Windows or Linux were active (2.4 GB in 5 minute at the highest point, but some pages were probably part of Consumed). Since Consumed was at 100%, some pages were moved out to accommodate new pages. The compression resulted in 0.6 GB, hence the uncompressed amount was in between 2x and 4x.
Consumed dropped by 0.4 GB as that’s the gap between what was added (new pages) and what was removed (existing pages).

##### Limit

Consumed is affected by Limit. The following is a VM configured with 8 GB RAM but was limited to 2 GB.

![image233.png](images/image233.png)


##### Total

Consumed may reach but not exceed the configured memory. Both total and consumed do not include the virtualization overhead memory.

![image234.png](images/image234.png)


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

![image235.png](images/image235.png)


###### Example 2

If you plot a VCF Operations VM in vCenter real-time performance chart, you will see 12 peaks in that one-hour line chart. The reason is VCF Operations pulls, process, and writes data every 5-minutes. The chart for CPU, disk and network will sport the same pattern. This is expected.
But if you plot the memory metrics, be it total active, active write or consumed, you will not see the 12 peaks. This is what I got instead.

![image236.png](images/image236.png)

Consume is completely flat and high. Active (read and write) and Active Write (write only) is much lower but again the 12 peaks are not shown.
Can you figure it out?
My guess is the sampling size. That’s just a guess, so if you have a better answer let me know!
Now let’s go to VCF Operations. In VCF Operations, this metric is called Memory \ Non Zero Active (KB).
vCenter reports in 20 seconds interval. VCF Operations takes 15 of these data and average them into a 300-second average. In the 300 second period, the same page can be read and written multiple times. Hence the active counter over reports the actual count.
Quiz: now that you know Active over reports, why is it lower than Consumed? Why is it lower than Guest OS metrics?
Active is lower than both metrics because these 2 metrics do not actually measure how actively the page is used. They are measuring the disk space used, so it contains a lot of inactive pages. You can see it in the general pattern of Consume and Guest OS used metrics. The following is VCF Operations appliance VM. Notice how stable the metrics are, even over millions of seconds.

![image237.png](images/image237.png)


#### Usage (%)

Usage metric in vCenter differs to Usage metric in VCF Operations.
What you see on the vCenter UI is Active, not Consumed.

![image238.png](images/image238.png)

Mapping to Active makes more sense as Consumed contains inactive pages. As covered earlier, neither Active nor Consumed actually measures the Guest OS memory. This is why VCF Operations maps Usage to Guest OS. The formula is:
VM Memory Usage (%) = Guest OS Needed Memory (KB) / VM Memory Total Capacity (KB) * 100
The following shows what Usage (%) = Guest OS Needed Memory over configured memory. The VM has 1 GB of memory, so 757 MB / 1024 = 74%.
Take note that there can be situation where Guest OS metrics do not make it to VCF Operations. In that case, Usage (%) falls back to Active (notice the value dropped to 6.99%) whereas Workload (%) falls back to Consumed (notice the value jump to 98.95%).

![image239.png](images/image239.png)


#### Utilization

Utilization (KB) = Guest Needed Memory (KB) + ( Guest Page In Rate per second * Guest Page Size (KB) ) + Memory Total Capacity (KB) – Guest Physically Usable Memory (KB).
Because of the formula, the value can exceed 100%. The following is an example:

![image240.png](images/image240.png)

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

![image241.png](images/image241.png)


![image242.png](images/image242.png)

The 1st line (highest) is Swap Target. It’s hovering around 6.8 million KB. It’s fluctuating every 20 seconds (I did zoom in). ESXi does not have to achieve this if it does not need it.
The 2nd line is actual swapped. It’s also constant in the last 1 hour. You can see the maximum and minimum are the same. The VM does not have limit, and it’s not part of resource pool, so this could be historical.
The 3rd line shows the amount granted. It’s also constant, indicating the VM does not ask for more.
The 4th line shows the amount consumed. It did fluctuate. I zoomed in and confirmed there were minor fluctuations. This is interesting since all other counters are 0.
The patterns of Consumed and Swap Target are mirror image. When Consume goes up, the target swap goes down.

![image243.png](images/image243.png)

Active is a sample. So it could be constant even though it should not be in this case as Consumed was not constant.

## ESXi

Compared with CPU metrics, vCenter provides even more metrics for memory: 38 metrics for RAM plus 11 for the kernel RAM. The kernel has around 50 processes that are tracked. As a result, a cluster of 8 ESXi can have > 800 metrics just for ESXi RAM.
We will cover each metric in-depth, so let’s do an overview first.

### Overview

Just like the case for VM, the primary counter for tracking performance is Page-fault Latency. Take note this is normalized average, so use the Max VM Memory Contention instead.

![image244.png](images/image244.png)

The contention could be caused by swapping in the past. You’ve got only 5, not 6 metrics for swap. Which counter is missing?

![image245.png](images/image245.png)

Swap target is missing. It can be handy to see the total target at ESXi level.
Swap and Compress go hand in hand, so we should check both together. Here are the compressed metrics.

![image246.png](images/image246.png)

I’m unsure if Compressed measures the result of the compression, or the input. My take is the former as that’s more useful from ESXi viewpoint.
Lastly, the performance could be caused by memory being read from the Host Cache. While they are faster than disk, they are still slower than physical memory.

![image247.png](images/image247.png)

Wait! What about Balloon?
As will cover in-depth shortly, that’s more of capacity than performance metrics. One can even say that other than Page-fault Latency, the rest of the metrics are actually for capacity not performance.
The famous balloon is a warning of capacity, assuming you do not play with limit.

![image248.png](images/image248.png)

When will ballooning kick in? There is a counter for that!

![image249.png](images/image249.png)

The memory state level shows one of the 5 possible states. You want to keep this at Clear state or High state.

![image250.png](images/image250.png)

For environment where performance matters more than cost, you want Balloon to be 0. That means Consume becomes your main counter for capacity. It is related to Granted and Shared.

![image251.png](images/image251.png)

Reservation plays a big part in capacity management as it cannot be overcommitted. ESXi, being a provider of resource, has 3 metrics to properly account for reservations.

![image252.png](images/image252.png)

There are a few metrics covering 0 pages and overhead. The Heap counter shows the memory used by the kernel heap and other data. This is normally a constant and small value.

![image253.png](images/image253.png)


##### Other Metrics

Active is not a counter for capacity or performance. It’s for the kernel memory allocation.

![image254.png](images/image254.png)

Persistent Memory

![image255.png](images/image255.png)

Lastly, there are a few metrics for VMFS pointer block cache. Read more here. They are internal, only used by the kernel. The only one you might be interested in the cache capacity miss ratio. Let me know if you have a real-world use case them.

![image256.png](images/image256.png)


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

![image257.png](images/image257.png)

Let’s look at an opposite scenario. The following ESXi is running at 100%. It has granted more memory than what it physically has. Initially, since the pages are inactive, there is no ballooning. When the active rise up, the consumed counter goes up and the balloon process kicks in. When the VM is no longer using the pages, the active counter reflects that and ESXi begin deflating the balloon and giving the pages back.

![image258.png](images/image258.png)

I shared in the VM memory counter that just because a VM has balloon, does not mean it experiences contention. You can see the same situation at ESXi level. The following ESXi shows a constant and significant balloon lasting at least 7 days. Yes the worst contention experienced by any VM is not even 1%, and majority of its 19 VMs were not experiencing contention at all.

![image259.png](images/image259.png)


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

![image260.png](images/image260.png)

The above happened because there was no need to bring back those pages. Notice ballooning was flat 0, indicating the ESX host was not under memory pressure.
Swap Out is an accumulative counter.

![image261.png](images/image261.png)

Let’s zoom in, and add the swap in and swap out counters to compare.

![image262.png](images/image262.png)

Notice the value did not go down despite swap in.

#### All “Together”

Balloon operates differently and works at a different layer than Swap and Compress. It takes longer to realize, and is not affected by limit. As a result, you can have 0 balloon while having swapping and zipped.
The following ESXi shows high Consume, and even higher Granted.
- The first line (highest blue line) shows Consume is hovering around 96%.
- The second line (purple line, just below the blue) shows Granted is hovering around 756 million KB.
- The third line shows consumed hovering around 514 million KB. ESXi has 511.46 GB or 536,304,680 KB of memory.

![image263.png](images/image263.png)

Since it’s hard to see, let’s show the table. What do you notice?

![image264.png](images/image264.png)

Ballooned was 0 constantly.
However, there were swapped and compressed. Let’s see if they are still happening, since these 2 counters are accumulative.
As you can see from the following chart, the amount is negligible. There are 4 instances of swap in, and each time the amount is 1 KB/second or 2 KB/second. Since the number of is the average of 20 seconds, the total amount is 20 KB or 40 KB only.

![image265.png](images/image265.png)

Does it mean the memory is not active?
Let’s look at the Active metric. It shows there are indeed activities, but they are within the pages already in the DIMM.

![image266.png](images/image266.png)


### Consumption Metrics

Consumption covers utilization, reservation and allocation.

![image267.png](images/image267.png)


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

![image268.png](images/image268.png)


##### Swapped

Consumed does not include swapped. This makes sense as the page are no longer in the physical memory. The following screenshot shows consumed drops when swap out went up.

![image269.png](images/image269.png)


##### Compressed

Consumed does not include compressed. The following shows that both compressed and swap out went up by almost 200 GB, yet Consumed dropped in the same period. It’s possible pages were removed from Consumed and were swapped and compressed.

![image270.png](images/image270.png)


##### Kernel

The other part of Consumed is non VM. This means the kernel, vSAN, NSX and whatever else running on the hypervisor. Because ESXi Consumed includes non VM, it can be more than what’s allocated to all running VMs, as shown below.

![image271.png](images/image271.png)

Take note that Consumed includes the actual consumption, not the reservation. The following ESXi has 0 running VM, so the Consumed is just made of the kernel. You can see the utilization is much lower than the reservation.

![image272.png](images/image272.png)

If you’re wondering why it’s consuming 17 GB when there is 0 VM, the likely answer is vSAN. Just because there is no VM does not mean vSAN should stop running.

#### Granted

Granted differs to Consumed as it excludes certain part of the kernel. It does not include the kernel space as processes at this privileged level gets what they want. They do not need the granting process, so to speak. Consumed, on the other hand, includes all both user and kernel space as both are indeed consuming pages.
Granted, being a consumer-level counter, can exceed total capacity. The following ESXi has granted 1053 GB of memory to running VMs, way above its total capacity of 755 GB.

![image273.png](images/image273.png)

Notice the sum of consumed + swapped + compressed is always below the total capacity.
I added balloon just in case you’re curious.
The following example shows ESXi hosts with no running VM. I’m surprised to see the granted counter is not 0. My guess the extra memory is for non-VM user world process.

![image274.png](images/image274.png)

Let’s take one of the ESXi to see the value over time. This time around, let’s use vCenter instead.

![image275.png](images/image275.png)

You can verify that ESXi Consumed includes its running VMs Consumes by taking an ESXi with a single running VM. The ESXi below has 255 GB of total capacity but only 229 GB is consumed. The 229 GB is split into 191 GB consumed by VM and 36 GB consumed by the kernel.

![image276.png](images/image276.png)

The kernel consumption is the sum of the following three resource pools.

![image277.png](images/image277.png)


#### Shared


| Metrics | Description |
| --- | --- |
| Shared | The sum of all the VM memory pages & the kernel services that are pointing to a shared page. In short, it’s Sum of VM Shared + the kernel Shared. If 3 VMs each have 2 MB of identical memory, the shared memory is 6 MB. |
| Shared Common | The sum of all the shared pages. You can determine the amount of ESXi host memory savings by calculating Shared (KB) - Shared Common (KB) |

Memory shared common is at most half the value of Memory shared, as sharing means at least 2 blocks are pointing to the shared page. If the value is a lot less than half, then you are saving a lot.
The following shows the shared common exceeding half many times in the last 7 days.

![image278.png](images/image278.png)

I’m not sure why. My wild guess is large pages are involved. ESXi hosts sport the hardware-assisted memory virtualization from Intel or AMD. With this technology, the kernel uses large pages to back the VM memory. As a result, the possibility of shared memory is low, unless the host memory is highly utilized. In this high consumed state, the large pages are broken down into small, shareable pages. The smaller pages get reflected in the shared common. Do let me know if my wild guess is correct.
You can also use the Memory shared common counter as leading indicator of host breaking large page into 4K. For that, you need to compare the value over time, as the absolute value may be normal for that host. The following table shows 11 ESXi hosts with various level of shared pages. Notice none of them is under memory pressure as balloon is 0. That’s why you use them as leading indicator.

![image279.png](images/image279.png)

With Transparent Page Sharing limited to within a VM, shared pages should become much smaller in value. I’m not sure if salting helps address the issue. From the vSphere manual, “With the new salting settings, virtual machines can share pages only if the salt value and contents of the pages are identical”.
I’m unsure if the above environment has the salting enabled or not. Let me know what level of sharing in your environment, especially after you disable TPS.

#### Utilization

We’ve seen that Consumed is too conservative as mostly cache and Active is too aggressive as it’s not even designed for memory sizing.
This calls for a metric in the middle. This is where Utilization comes in.
It’s the sum of running VM Utilization metrics + the kernel reservation.
Utilization uses the reservation amount for the kernel, instead of the actual utilization. This is technically not accurate but operationally wise as it gives you buffer.
I plotted from 192 ESXi. I averaged the data to remove outlier. Based on 6840 running VMs, the Utilization counter is lower than Consumed by 122 GB. If you include Shared Common, your savings goes up to 152 GB on average.

![image280.png](images/image280.png)


#### Validation

The following screenshot shows that ESXi had all its VM evacuated. Not a single VM left, regardless of power on/off status.

![image281.png](images/image281.png)

In the preceding chart, we could see the metric Memory Allocated on All Consumers dropped from 452 GB to 0 GB, and it remained flat after that.
Checking the Reserved Capacity metric, we can see it dropped to 0. This is expected.

![image282.png](images/image282.png)

How about Consumed?

![image283.png](images/image283.png)

Memory Consumed also dropped. The value was 400 GB, less than 452 GB of allocated to all VM. This indicated some VM had not used the memory, which could happen.
The value dropped to 32 GB, not 0 GB. This is expected as Consumed includes every other process that runs. In this case, it is majority vSAN, which runs in the kernel.
Let’s check the kernel utilization.

![image284.png](images/image284.png)

Notice it’s a bit smaller than Consumed, indicating Consumed has other thing. I suspect it’s BIOS and the console in vSphere Client UI.
How come the value didn’t change much? I kind of expect some changes, based on the theory that some kernel modules memory footprint depends on the number of running VM. If you know, let me know!
How about the kernel reservation? What do we expect the value to change?

![image285.png](images/image285.png)

Well, it won’t since the actual usage does not change.

##### Analysis

I compare 185 production ESXi hosts to understand the behaviour of the metrics. I averaged their results to eliminate outlier.

![image286.png](images/image286.png)

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

![image287.png](images/image287.png)

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

![image288.png](images/image288.png)

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

![image289.png](images/image289.png)

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


![image290.png](images/image290.png)

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

![image291.png](images/image291.png)

The green boxes are what you are likely to be familiar with. You have your ESXi host, and it can have NFS Datastore, VMFS Datastore, vSAN Datastore, vVOL datastore or RDM objects. vSAN & vVOL present themselves as a VMFS datastore, but the underlying architecture is different. The blue boxes represent the metric groups you see in vCenter performance charts.
Just like compute virtualization, there is no more association to VM for metrics at physical layers.
In the central storage architecture, NFS and VMFS datastores differ drastically in terms of metrics, as NFS is file-based while VMFS is block-based.
- For NFS, it uses the vmnic, and so the adapter type (FC, FCoE, or iSCSI) is not applicable. Multipathing is handled by the network, so you don't see it in the storage layer.
- For VMFS or RDM, you have more detailed visibility of the storage. To start off, each ESXi adapter is visible and you can check the metrics for each of them. In terms of relationship, one adapter can have many devices (disk or CDROM). One device is typically accessed via two storage adapters (for availability and load balancing), and it is also accessed via two paths per adapter, with the paths diverging at the storage switch. A single path, which will come from a specific adapter, can naturally connect one adapter to one device. The following diagram shows the four paths:

![image292.png](images/image292.png)

The counter at ESXi level contains data from all VMs and the kernel overhead. There is no breakdown. For example, the counter at vmnic, storage adapter and storage path are all aggregate metrics. It’s not broken down by VM. The same with vSAN objects (cache tier, capacity disk, disk group). None of them shows details per VM.
Can you figure out why there is no path to the VSAN Datastore?
We’ll do a comparison, and hopefully you will realize how different distributed storage and central storage is from performance monitoring point of view. What look like a simple change has turned the observability upside down.

#### Storage Adapter

The screenshot shows an ESXi host with the list of its adapters. We have selected vmhba2 adapter, which is an FC HBA. Notice that it is connected to 5 devices. Each device has 4 paths, giving 20 paths in total.

![image293.png](images/image293.png)

What do you think it will look like on vSAN? The following screenshot shows the storage adapter vmhba1 being used to connect to two vSAN devices. Both devices have names begin with “Local”. The storage adapter has 2 targets, 2 devices and 2 paths. If you are guessing it is 1:1 mapping among targets, devices and paths, you are right.
We know vSAN is not part of Storage Fabric, so there is no need for Identifier, which is made of WWNN and WWPN.

![image294.png](images/image294.png)

Let’s expand the Paths tab. We can see the LUN ID here. This is important. The fact that the hypervisor can see the device is important. That means the kernel can report if there is an issue, be it performance or availability. This is different if the disk is directly passed through to the VM. The hypervisor loses visibility.

![image295.png](images/image295.png)


#### Storage Path

Continuing our comparison, the last one is Storage Path. In a fibre channel device, you will be presented with the information shown in the next screenshot, including whether a path is active or not.

![image296.png](images/image296.png)

Note that not all paths carry I/O; it depends on your configuration and multipathing software. Because each LUN typically has four paths, path management can be complicated if you have many LUNs.
What does Path look like in vSAN? As shared earlier, there is only 1 path.

![image297.png](images/image297.png)


#### Storage Devices

The term drive, disk, device, storage can be confusing as they are often used interchangeably in the industry. vSphere Client uses the terms device and disk interchangeably. In vSphere, this means a physical disk or physical LUN partition presented to ESXi host.
The following shows that the ESXi host has 3 storage devices, all are flash drive and the type = disk. The first two are used in vSAN datastore and are accessed via the adapter vmhba1.

![image298.png](images/image298.png)

A storage path takes data from ESXi to the LUN (the term used by vSphere is Devices), not to the datastore. So if the datastore has multiple extents, there are four paths per extent. This is one reason why you should not use more than one extent, as each extent adds 4 paths. If you are not familiar with VMFS Extent, Cormac Hogan explains it here.
For VMFS (non vSAN), you can see the same metrics at both the Datastore level and the Disk level. Their value will be identical if you follow the recommended configuration to create a 1:1 relationship between a datastore and a LUN. This means you present an entire LUN to a datastore (use all of its capacity). The following shows a VMFS datastore with a NetApp LUN backing it.

![image299.png](images/image299.png)

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

![image300.png](images/image300.png)

Performance and capacity become complex due to many to many relationships. The metrics at ESXi level and cluster will not match the metrics at datastore level. How do you then aggregate the cluster storage capacity when its datastores are shared with other clusters?
You’re right. You can’t.
In summary, while there are use cases where you should separate the VMDK into multiple datastores, take note of the observability compromise.

#### Backing Device

Since datastore is a filesystem, it’s necessary to monitor the backing device. This can be NFS or LUN. For NFS, it looks something like this:

![image301.png](images/image301.png)

For a local disk, it looks something like this:

![image302.png](images/image302.png)

Since the underlying device is outside the realm of vSphere, you need to login to the storage provider and build the relationship. Compare the metrics by deriving a ratio. Investigate if this ratio shows unexpected value.
Take for example, a datastore on a FC LUN. If you divide the IOPS at the LUN level with the IOPS at the datastore, what value do you expect?
Assuming they are mapped 1:1, then the ratio should be 1.
If the value is > 1, that means there are IO operations performed by the array. This could be array level replication or snapshot.
What about NFS datastores? The troubleshooting is different as you now need to at files as opposed to block. In both cases, you need to monitor the filer or array directly.

## VM

We covered earlier that storage differs to compute as it covers both dimensions (speed and space). As a result, we cannot simply use the contention and consumption as grouping. Instead we would group by performance and capacity. This is also good as operationally you manage performance and capacity differently.

### Overview

Recall the 3 layers of storage from VM downward. As stated, the 3 blue boxes appear in the vSphere Client UI as virtual disk, datastore and disk.

![image303.png](images/image303.png)

Among the 3, which one is the most important?
You’re right, virtual disk.
It is the closest to the VM and it is the most detail in terms of observability.

#### Virtual Disk

Use the virtual disk metrics to see VMFS vmdk files, NFS vmdk files, and RDMs.
However, you don’t get data for anything other than virtual disk. For example, if the VM has snapshot, the metric does not include the snapshot data.
A VM typically has multiple virtual disks, typically 1 Guest OS partition maps to 1 virtual disk. The following VM has 3 virtual disks.

![image304.png](images/image304.png)

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

![image305.png](images/image305.png)

Use the disk metrics to see VMFS and RDM, but not NFS. The data at this level should be the same as at Datastore level because your blocks should be aligned; you should have a 1:1 mapping between Datastore and LUN, without extents. It also has the Highest Latency counter, which is useful in tracking peak latency
The metric is at the disk level. So I’m not 100% sure if the value is per VM or per disk (which typically has many VM).

![image306.png](images/image306.png)


##### Raw Device Mapping

RDM appears clearly as LUN in the VM Edit Settings dialog box:

![image307.png](images/image307.png)

But what does it appear when you browse the VM folder in the parent datastore?
RDM appears like a regular VMDK file. There is no way to distinguish it in the folder.

![image308.jpeg](images/image308.jpeg)


#### Datastore

Use the datastore metrics to see VMFS and NFS, but not RDM. Because snapshots happen at Datastore level, the counter will include it. Datastore figures will be higher if your VM has a snapshot. You don’t have to add the data from each virtual disk together as the data presented is already at the VM level. It also has the Highest Latency counter, which is useful in tracking peak latency.
Just like LUN level, we lose the breakdown at virtual disk. The metric is only available at VM level.

![image305.png](images/image305.png)


#### Mapping

If all the virtual disks of a VM are residing in the same datastore, and that datastore is backed by 1 LUN, then all the 3 layers will have fairly similar metrics. The following VM has 2 virtual disks (not shown). Notice all 3 metrics are identical over time.

![image309.png](images/image309.png)

The difference comes from files outside the virtual disks, such as snapshot, log files, and memory swap.

#### Multi-Writer Disk

In application such as database, multiple VMs need to share the same disk.
Shared disk can be either shared RDM or VMDK. The following screenshot shows the option when creating a multi-writer VMDK in vCenter Client.

![image310.png](images/image310.png)

When multiple VMs are sharing the same virtual disk or RDM, it creates additional challenge in capacity, cost and performance management. In the following example, notice the metric become flat 0. See the red arrow.

![image311.png](images/image311.png)

The above is obviously wrong as IOPS are typically not flat 0.
What happens here is typical Active/Passive pair of VM. The application fail over to the second VM, so the first VM becomes passive. vCenter API returns 0 instead of blank, hence you see 0 in VCF Operations.
You can see from the following screenshot that the second VM took over at the time the first VM failover. Notice it started showing IOPS metrics on the same time.

![image312.png](images/image312.png)

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

![image313.png](images/image313.png)

A related counter to latency is Outstanding IO.
This is the number of I/Os that have been issued, but not yet completed. They are waiting in the queue, indicating a bottleneck

![image314.png](images/image314.png)

The relationship is
Average Latency = Average Outstanding IO / Average IOPS
Outstanding IO should be seen in conjunction with latency. It can be acceptable to have high number of IO in the queue, so long the actual latency is low.
Since your goal is maximum IOPS and minimum latency, the metric is less useful as its value is impacted by IOPS. See this KB article for VSAN specific recommendation on the expected value.
What should be the threshold value?
That depends on your storage, because the range varies widely. Use the profiling technique to establish the threshold that is suitable for your environment.
In the following analysis, we take more than 63 million data points (2400 VM x 3 months worth of data). Using data like this, discuss with the storage vendor if that’s in line with what they sold you.

![image315.png](images/image315.png)


##### Disk

As the physical disk layer, there are 2 error metrics. I always find their values to be 0 all the time, so if you’ve seen a non-zero value let me know.

![image316.png](images/image316.png)

For latency, there is no breakdown. It’s also the highest among all disks. Take note the roll-up is latest, so it’s the single value at the end of the collection period.

![image317.png](images/image317.png)


##### Datastore

At the datastore layer, the only metric provided for contention is latency. There is no outstanding IO.

![image318.png](images/image318.png)

The highest latency is useful for VMs with multiple datastores. But take note the roll-up is Latest, not average.
For the read and write latency, the value in VCF Operations is a raw mapping to these values datastore.totalReadLatency.average and datastore.totalWriteLatency.average

#### Consumption metrics

A typical suspect for high latency is high utilization, so let’s check what IOPS and throughput metrics are available.

##### Virtual Disk

As you can expect, you’re given both IOPS and throughput metrics at virtual disk level.

![image319.png](images/image319.png)

VM Disk IOPS and throughput vary widely among workload. For a single workload or VM, it also depends on whether you measure during its busy time or quiet time.
Take note that vSphere Client does not provide summary at VM level. Notice the target objects are individual scsiM:N, and there is no aggregation at VM level as the option in Target Objects column below.

![image320.png](images/image320.png)

In the following example, I plotted from a 3500 production VMs. They are sorted by the largest IOPS on any given 5 minute. What’s your take?

![image321.png](images/image321.png)

I think those numbers are high. At 1000 IOPS averaged over 5 minutes, that means 300,000 total IO commands that need to be processed. So 10K IOPS translates into 3 millions commands, which must be completed within 300 seconds.
A high IOPS can also impact the pipe bandwidth, as it’s shared by many VMs and the kernel. If a single VM chews up 1 Gb/s, you just need a handful of them to saturate 10 Gb ethernet link.
There is another problem, which is sustained load. The longer the time, the higher the chance that other VMs are affected.
In the following example, it’s a burst IOPS. Regardless, discuss with the application team if it is higher than expected. What’s normal from one application may not be for another.

![image322.png](images/image322.png)

While there is no such thing as normal distribution or range, you can analyse your environment so you get a sense. I plotted all the 3500 VMs and almost 85% did not exceed 1000 IOPS in the last 1 week. The ones hitting >5K IOPS only form around 3%.

![image323.png](images/image323.png)

If the IOPS is low, but the throughput is high, then the block size is large. Compare this with your expected block size, as they should not deviate greatly from plan. You do have a plan, don’t you 😉

![image324.png](images/image324.png)

You can set the limit for individual virtual disk of VM.

![image325.png](images/image325.png)

A few rows below, and you will see the following.

![image326.png](images/image326.png)

The default setting is no limit, which is what I recommend.
Note that the limit on a virtual disk, not the whole VM. That means you cannot set limit on non virtual disk such as snapshot and memory swap. This makes sense as they are part of IaaS.
Take note that since the limit is applied at VM level, the metrics that will show high latency is at Guest OS levels. The VM metric will not show high latency, as the IO that were allowed to pass was not affected by this limit. This is no different to any problem at Guest OS layer. For example, if LSI Logic or PVSCSI driver is causing problem, the VM will not report anything as it’s below the Guest OS driver.
VCF Operations have the following related data at each virtual disk
- IOPS Limit property.
- IOPS per GB metric.

##### Disk

There are 2 sets of metrics for IOPS. Both are basically the same. One if the total number of IO in the collection period, while the other one is average of 1 second.

![image327.png](images/image327.png)

There are the usual metrics for throughput.

![image328.png](images/image328.png)

It will be great to have block size, especially the maximum one during the collection period.

##### Datastore

For utilization, both IOPS and throughput are provided.

![image329.png](images/image329.png)

For the IOPS, the value in VCF Operations is a raw mapping to these values datastore.numberReadAveraged.average and datastore.numberWriteAveraged.average in vCenter.
Review the following screenshot. Notice something strange among the 3 metrics?

![image330.png](images/image330.png)

Yes, the total IOPS at datastore level is much lower than the IOPS at physical disk and virtual disk levels. The IOPS at physical disk and virtual disk are identical over the last 7 days. They are quite active.
The IOPS at datastore level is much lower, and only spike once a day. This VM is an Oracle EBS VM with 26 virtual disks. Majority of its disks are RDM, hence the IOPS hitting the datastore is much less.
Snapshot requires additional read operations, as the reads have to be performed on all the snapshots. The impact on write is less. I’m not sure why it goes up so high, but logically it should be because many files are involved. Based on the manual, a snapshot operation creates .vmdk, -delta.vmdk, .vmsd, and .vmsn files. Read more here.
For Write, ESXi just need to write into the newest file.

![image331.png](images/image331.png)

The pattern is actually identical. I take one of the VM and show it over 7 days. Notice how similar the 2 trend charts in terms of pattern.

![image332.png](images/image332.png)

You can validate if snapshot causes the problem by comparing before and after snapshot. That’s exactly what I did below. Notice initially there was no snapshot. There was a snapshot briefly and you could see the effect immediately. When the snapshot was removed, the 2 lines overlaps 100% hence you only see 1 line. When we took the snapshot again, the read IOPS at datastore level is consistently higher.

![image333.png](images/image333.png)

How I know that’s IOPS effect as the throughput is identical. The additional reads do not bring back any data. Using the same VM but at different time period, notice the throughput at both levels are identical.

![image334.png](images/image334.png)

And here is the IOPS on the same time period. Notice the value at datastore layer is consistently higher.

![image335.png](images/image335.png)

For further reading, Sreekanth Setty has shared best practice here.
In addition of latency and IOPS, snapshot can also consume more than the actual space consumed by the virtual disk, especially if you are using thin and you take snapshot early while the disk is basically empty. The following VM has 3 virtual disks, where the snapshot file _1-00001.vmdk is much larger than the corresponding vmdk.

![image336.png](images/image336.png)


##### Storage DRS

Lastly, there are storage DRS metric and seek size.

![image337.png](images/image337.png)


### Capacity Metrics

Disk space metrics are complex due the different types of consumption in a single Virtual Disk.
- Actual used by Guest OS
- Unmapped block
- vSAN protection (FTT)
- vSAN savings (dedupe and compressed).
Let’s break it down, starting with understanding the files that make up a VM.

#### VM Files

At the end of the day, all those disk space appear as files in the VMFS filesystem, including the RDM pointer files. You can see them when you browse the datastore. The following is a typical example of what vSphere Client will show.

![image338.png](images/image338.png)

Yes, a lot of files 😊
We can categorize them into 4 from operations viewpoint:

| Disk | Virtual disk or RDM. This is typically the largest component. This can be thin provisioned, in which case the provisioned size tends to be larger than the actual consumption as Guest filesystem typically does not fill 100%. All virtual disks are made up of two files, a large data file equal to the size of the virtual disk and a small text disk descriptor file which describes the size and geometry of the virtual disk file. The descriptor file also contains a pointer to the large data file as well as information on the virtual disks drive sectors, heads, cylinders and disk adapter type. In most cases these files will have the same name as the data file that it is associated with (i.e. MyVM1.vmdk and MyVM1-flat.vmdk). A VM can have up to 64 disks from multiple datastores. |
| --- | --- |
| Snapshot | Snapshot protects 3 things:  VMDK Memory Configuration For VMDK, the snapshot filename uses the syntax MyVM-000001.vmdk where MyVM is the name of the VM and the six-digit number 000001 is just a sequential number. There is 1 file for each VMDK. Snapshot does not apply to RDM. You do that at storage subsystem instead, transparent to ESXi. If you take snapshot with memory, it creates a .vmem file to store the actual image. The .vmsn file stores the configuration of the VM. The .vmsd file is a small file, less than 1 KB. It stores metadata about each snapshot that is active on a VM. This text file is initially 0 bytes in size until a snapshot is created and is updated with information every time snapshots are created or deleted. Only 1 file exists regardless of the number of snapshots running as they all update this single file. This is why your IO goes up. |
| Swap | The memory swap file (.vswp). A VM with 64 GB of RAM will generate a 64 GB swap file (minus the size of memory reservation) which will be used when ESXi needs to swap the VM memory into disk. The file gets deleted when the VM is powered off. You can choose to store this locally on the ESXi Host. That would save space on vSAN. The catch is vMotion as the swap file must be transferred too.  There is also a smaller file (in MB) storing the VMX process swap file. But I’m unsure about this and have not seen it yet. |
| Others | All other files. They are mostly small, in KB or MB. So if this counter is large, you’ve got unneeded files inside the VM directory.  Logs files, configuration files, and BIOS/EFI configuration file (.nvram) Note that this includes any other files you put in the VM directory. So if you put a huge ISO image or any file, it gets counted. |


#### Single VMDK

Let’s review with a single virtual VMDK disk. In the following diagram, vDisk 2 is a thin provisioned VMDK file. It still has uncommitted space as it’s not yet fully used up.

![image340.png](images/image340.png)

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

![image341.png](images/image341.png)

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

![image342.png](images/image342.png)

Hard disk 1 is 10 GB. Thin Provisioned. On vSAN.
The VM is powered off. All other settings follow default setting.
I created the VM with just the first disk, to validate the metrics value that will be shown upon creation. What do you expect to see on the vCenter UI?
Here is what I got on vSphere 7.

![image343.png](images/image343.png)

You get 2 numbers, used and allocated, as shown in the Capacity and Usage section.
Used is only 1.9 KB. This is expected as it’s thin provision and the VM is powered off. This is very low, so let’s check the next number….
Allocated is 12.22 GB. This is 10 GB configured + 2.22 GB used. The hard disk 1 size shows 10 GB not 20 GB. This is what is being configured, and what Guest OS see. It is not impacted by vSAN as it’s not utilization.
So you have 2 different numbers for the use portion: 1.9 KB and 2.22 GB.
Why 2 different values?
Let’s see what the files are. We can do this by browsing the datastore and find the VM folder.

![image344.png](images/image344.png)

The total from the files above is 36 MB. This does not explain 1.9 KB nor 2.22 GB.
Let’s continue the validation. This time I added Hard disk 2 and configure it with 20 GB. Unlike the first disk, this is Thick Provisioned so we can see the impact. It is also on vSAN.

![image345.png](images/image345.png)

Used has gone up from 1.9 KB to 760 MB. As this is on vSAN, it consists of 380 MB of vSphere + 380 MB of vSAN protection. The vSAN has no dedupe nor compression, so it’s a simple 2x.
Allocated is 32.93 GB as it consists of 30 GB configured and 2.93 GB. This 2.93 is half vSphere overhead + vSAN protection on the overhead.
Looking at the datastore level, the second hard disk is showing 40.86 GB. It maps to hard disk 2.

![image346.png](images/image346.png)

From this simple example, you can see that Allocated in vCenter UI actually contains used and allocated. By allocated it means the future potential used, which is up to the hard disk configured size. The used portion contains vSAN consumption if it’s on vSAN, while the unused portion does not (obviously since vSAN has not written any block).

## ESXi

The following screenshot shows the ESXi metric groups for storage in the vCenter performance chart.

![image347.png](images/image347.png)

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

![image348.png](images/image348.png)

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

![image352.png](images/image352.png)

I chose the last ESXi since that’s the one with worst latency.
I plotted Kernel vs Device.
What do you notice? Can you determine which is which?

![image353.png](images/image353.png)

They don’t correlate. This is expected since both have reasonably good value (my expectation is below 0.5 ms).
The bulk of the latency should come from the Device. In a healthy environment, it should be well within 5 ms. With SSD, it should be even lower. As you can see below, it’s below 1.75 ms. Notice the kernel latency is 0.2 ms at all times except in 1 spike.

![image354.png](images/image354.png)

What about the Queue latency? It’s part of the kernel latency, so it will be 100% within it. When the kernel latency value is in the healthy range, the 2 values should correlate, as the value is largely dominated by the Queue. Notice the pattern below is basically identical.

![image355.png](images/image355.png)


![image356.png](images/image356.png)


##### Other Metrics

I find the value of Bus Resets and Commands Aborted are always 0

![image357.png](images/image357.png)

If you’ve seen a non zero let me know.

![image358.png](images/image358.png)

I’m not sure what highest latency refers to (Guest, Kernel, or Device).
Maximum Queue Depth is more of a property than a metric, as it’s a setting.

![image359.png](images/image359.png)


#### Consumption Metrics

You get the standard IOPS and Throughput metrics.

| IOPS |  |
| --- | --- |
| Throughput | The counters names are Read Rate Write Rate Usage All their units are in KB/s |
| Total IO | This is just the number of Read or Write in the time interval. The counters names are Read Requests Write Requests Commands Issued |


### Storage Adapter & Path

They have identical set of counters, hence I’m documenting them together. Ideally, adapter should include metrics such as adapter queue length and commands aborted.
The following screenshot shows the metrics provided:

![image361.png](images/image361.png)

For storage path, the counters may appear that they are measuring the device, as the object name is not based on the friendly name.

![image362.png](images/image362.png)

The object above is the path, not the device.

#### Contention Metrics

There are 3 metrics provided:
- Read latency
- Write latency
- Highest latency
The highest latency metric takes the worst value among all the adapters or the paths. This can be handy compared to tracking each of them one by one. However, it averages each adapter first, so it’s not the highest read or write. You can see from the following screenshot that its value is lower than the read latency or vmhba0. What you want is the highest read or write among all the adapters or paths.

![image363.png](images/image363.png)


##### Analysis

I plotted 192 ESXi host and checked the highest read latency and highest write latency among all their adapters. As the data was returning mostly < 1 ms, I extended to 1 week and took the worst in that entire week. You can see that the absolute worst of write latency was a staggering 250 ms. But plotting the 95th percentile value shows 0.33 ms, indicating it’s a one off occurrence in that week. The 250 ms is also likely an outlier as the rest of the 191 ESXi shows maximum 5 ms, and with much lower value at 95th percentile.

![image364.png](images/image364.png)

Plotting the value of the first ESXi over 7 days confirmed the theory that it’s a one off, likely an outlier.

![image365.png](images/image365.png)

Does it mean there is no issue with the remaining of the 191 ESXi hosts?
Nope. The values at 95th percentile is too high for some of them.
I modified the table by changing Maximum with 99th percentile to eliminate an outlier. I also reduced the threshold so I can see better. The following table shows the values, sorted by the write latency.

![image366.png](images/image366.png)

The table revealed that there are indeed latency problem. I plotted one of the ESXi and saw the following.

![image367.png](images/image367.png)

From here, you need to drill down to each adapter to find out which one.

#### Consumption Metrics

For each adapter, there are 4 metrics provided:
- Read IOPS, tracking the number of reads per second.
- Write IOPS
- Read throughput
- Write throughput.
The following screenshot is an example of what you get from vSphere Client UI.

![image368.png](images/image368.png)

If the block size matters to you, create a super metric in VCF Operations.

### Datastore

For shared datastore, the metrics do not show the same value with the one at datastore object. All these metrics are only reporting from this ESXi viewpoint, not the sum from all ESXi mounting the same datastore. As a result, I’d cover only performance. Capacity will be covered under the datastore chapter.
For each datastore, you get the usual IOPS, throughput and latency. They are split into read and write, so you have 3 x 2 = 6 metrics in total. These are the actual names:

![image369.png](images/image369.png)

There is no block size but you can derive it by dividing Throughput with IOPS.
You also get 2 additional counters:
- Datastore latency observed by VMs
- Highest latency.
I plotted their values and to my surprise the metric Datastore latency observed by VMs is much higher. You can see the blue line below. It makes me wonder what the gap is as there is only the kernel in between.

![image370.png](images/image370.png)

The metric Highest Latency is a normalized averaged of read and write, hence it can be lower.

#### Outstanding IO

You can derive the outstanding IO metric from latency and IOPS. I think latency counter is more insightful. For example, the following screenshot shows hardly any IO being in the queue:

![image371.png](images/image371.png)

However, if you plot latency, you get same pattern of line chart but with higher value.

![image372.png](images/image372.png)

You can check whether it’s read or write by plotting each.
The following screenshot shows it’s caused by write latency. It’s expected if your read is mostly served by cache.

![image373.png](images/image373.png)


#### Queue Depth

You can also see the queue depth for each datastores (I think this is actually the backing LUN, but unsure if there are extent). Ensure that the settings are matching your expectation and are consistent. You can list them per cluster and see their values.

![image374.png](images/image374.png)

Chapter 5

# Network


## Architecture

Network monitoring is complex, especially in large data centers. Adding network virtualization takes the complexity of performance troubleshooting even higher.
Just like CPU, Memory and Disk, there is also a new layer introduced by virtualization. There are virtual network cards on each VM, and software-based switch on each ESXi bridging the VM card to the physical NIC card. The various ESXi kernel modules also do not “talk” directly to the physical card. Basically, what used to be the top of rack switch are now living inside each ESXi as a software switch.

![image375.png](images/image375.png)

vSphere Client shows the 2 layers side by side (personally I prefer up and down, with the physical layer placed below).

![image376.png](images/image376.png)


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

![image377.png](images/image377.png)

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

![image378.png](images/image378.png)


#### Resource Allocation

This means the resource that is given to a single VM itself. For compute, we can configure a granular size of CPU and RAM. For the CPU, we can assign one, two, three, four, etc. vCPUs.
With network, we cannot specify the vNIC speed. It takes the speed of the ESXi vmnic assigned to the VM port group. So each VM will either see 1 GE or 10 GE or 25 GE (you need to have the right vNIC driver, obviously). You cannot allocate another amount, such as 500 Mbps or 250 Mbps in the Guest OS. In the physical world, we tend to assume that each server has 10 GE and the network has sufficient bandwidth. You cannot assume this in a virtual data center as you no longer have 10 GE for every VM at the physical level. It is shared and typically oversubscribed.
A network intensive VM can easily hit 1 Gbps for both egress and ingress traffic. The following chart shows a Hadoop worker node receiving more than 5 Gbps worth traffic multiple times. You need to be careful in sizing the underlying ESXi if you want to run multiple VMs. While you can use Network I/O Control and vSphere Traffic Shaping, they are not configuration property of a VM.

![image379.png](images/image379.png)


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

![image380.png](images/image380.png)

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

![image381.png](images/image381.png)

The above example shows an ESXi host with 3 agent VMs. The first VM provides a storage service (an example is Nutanix CVM), the second VM provides Network service, and the 3rd VM provides a Security VM.
Let’s use the Security service as an example. A popular example here is Trend Micro Deep Security virtual appliance. It is in the data path. If the Business VMs are accessing files on a fileserver on another network, the files have to be checked by the security virtual appliance first. If the agent VM is slow (and it could be due to factor that is not network related), it will look like a network or storage issue as far as the business VMs are concerned. The Business VMs do not know that their files have been intercepted for security clearance, as it is not done at the network level. It is done at the hypervisor level.

#### Source of Data

A complete network monitoring requires you to get the data from 5 different sources, not just from vSphere. In SDDC, you should also get data from the application, Guest OS, NSX and NetFlow/sFlow/IPFIX from VDS and physical network devices. For VDI, you need to get data at application level. We have seen packet loss at application-layer (Horizon Blast protocol) when Windows sees no dropped packet. The reason was the packet arrives out of order and hence unusable from protocol viewpoint.
The following shows a simplified stack. It shows the five sources of data and the 4 tools to get the data. It includes a physical switch as we can no longer ignore physical network once you move from just vSphere to complete SDDC.

![image382.png](images/image382.png)

The network packet analysis comes in 2 main approaches: Header analysis and full packet analysis. The header analysis is certainly much lighter but lack the depth of full analysis. You use this to provide overall visibility as it does not impose heavy load on your environment.
The impact of virtualization on network monitoring goes beyond what we have covered. Let’s add NSX Edge into the above, so you can see the traffic flow when the edge services are also virtualized. You will see that a network problem experienced by a VM on one ESXi could be caused by another VM running on another ESXi. The following diagram is a simplified setup, showing a single NSX Edge residing on another cluster.

![image383.png](images/image383.png)

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

![image384.png](images/image384.png)

The following applies that to vSphere distributed vSwitch. Notice the ESXi host is not shown as it’s not part of the hop. The ESXi host physical NIC card is the distributed vSwitch uplink.

![image385.png](images/image385.png)


#### Traffic Type

VCF Operations provides these metrics at VM, ESXi, Distributed Port Group and Distributed Switch level. As vSphere Tanzu Pod is basically a VM, it also has the metric.
BTW, one way to check what objects in what adapter have the specific metric is in the VCF Operations policy. Open any policy, and search the metric using its name. The list of matching metrics will be shown, grouped by the objects.

![image386.png](images/image386.png)

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

![image387.png](images/image387.png)

Next, you check if there are unusual traffic. Your network should be mostly unicast, so it’s good to track the broadcast and multicast packets. They might explain why you have many dropped packets. If packets are broadcast packets, it might be dropped by the network.

![image388.png](images/image388.png)

Next you check utilization. There are 6 metrics, but I think they are triplicate.

![image389.png](images/image389.png)

Each packet takes up CPU for processing, so it’s good to check if the packet per second becomes too high

![image390.png](images/image390.png)

The metrics are available at each individual vNIC level and at the VM level. Most VMs should only have 1 vNIC, so the data at VM level and vNIC level will be identical.
The vNICs are named using the convention "400x". That means the first vNIC is 4000, the second vNIC is 4001, and so on. The following is a vCenter VM. Notice it receives a few broadcast packets, but it’s not broadcasting (which is what you expect). It also does not participate in multicast, which is again expected.

![image391.png](images/image391.png)

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

![image392.png](images/image392.png)


### Contention Metrics

As usual, let’s approach the metrics starting with Contention. We covered earlier that the only contention metric is packet loss.
For TCP connection, dropped packet needs to be retransmitted and therefore increases network latency from application point of view. The counter will not match the values from Guest OS level. RX packets are dropped before it’s handed into Guest OS, and TX packets are dropped after it left the Guest OS. ESXi dropped the packet because it’s not for the Guest OS or it violates the security setting you set.
The following summary proves that receive packet gets dropped many more times than transmit packet. This is based on 3938 VMs. Each shows the last 1 month, so approximately 35 million data points in total. The average of 35 million data points show that dropped RX is significantly higher than dropped TX. This is why it’s not in the SLA.

![image393.png](images/image393.png)

The following table shows that the drop is short and spiky, which is a good thing. The value at 99th percentile is 35x smaller than the value at 100th percentile.

![image394.png](images/image394.png)

The high value in receive can impact the overall packet dropped (%) counter, as it’s based on the following formula
dropped = Network|Received Packets Dropped + Network|Transmitted Packets Dropped
delivered = Network|Packets Received + Network|Packets Transmitted
Network|Packets Dropped (%) = dropped / (dropped + delivered) * 100
I’ve seen multiple occurrences where the packet dropped (%) jumps to well over 95%. That’s naturally worrying. They typically do not last beyond 15 minutes.

![image395.png](images/image395.png)

In this, plot the following 4 metrics. You will likely notice that the high spike is driven by low network throughput and high received packet dropped.

![image396.png](images/image396.png)

Because of the above problem, profile your VM dropped packets, focusing on the transmit packets. The following is one way to do it, giving surprising results like this:

![image397.png](images/image397.png)

The design of the preceding table is:
- First column calculates the percentage packets dropped. I took 99th percentile else many of the results will be 100%.
- Second column sums all the transmitted dropped packets (actual packet counts).
- Third column takes the 99th percentile maximum of dropped packet within any 300 seconds. Each network packet is typically 1500 bytes. Using 1.5 KB packet size, 1 thousand packets dropped = 1500 MB worth of packets within 300 seconds.
I don’t expect dropped packets in data center network, so to see millions of dropped packets over a month needs further investigation with network team. Moreover, those metrics are Transmit, not Received. So the VM sent them but they got dropped. No one seem to complain, because packets are automatically retransmitted.
What I typically notice is the spike rarely happens. They look like an outlier, especially when the number is very high. The following is an example. I only showed in the last 1 month as the rest of the 6 months had similar pattern. The jump is well cover 100 million packets, and they were all dropped. Assuming each packet is 1 KB, since VCF Operations reports every 5 minutes, that’s 333 MB per second sustained for 300 seconds.

![image398.png](images/image398.png)

I also notice regular, predictable pattern like this. This is worth discussing with network team. It’s around 3800 packets each 5-minute, so it’s worth finding out.

![image399.png](images/image399.png)

False positive on TX dropped packet because NSX firewall reject the outgoing packet. See this KB article.
Packet loss in Guest OS using VMXNET3: When using the VMXNET3 driver, you may see significant packet loss during periods of very high traffic bursts. The VM may even freeze entirely. This issue occurs when packets are dropped during high traffic bursts. This can occur due to a lack of receive and transmit buffer space or when receive traffic which is speed constrained.

### Consumption Metrics

There are 2 main metrics to measure utilization: throughput and packets.
Both metrics matter as you may still have bandwidth but unable to process that many packets per second. This outage shows 700K packets per second that only consumes 800 Mbps as the packet is small. The broadcast packet is only 60 bytes long, instead of the usual 1500 bytes.

![image400.png](images/image400.png)

The packets transmitted does not include those dropped packets. Another word, it only counts packets that were successfully transmitted.
The following diagram proves the above relationship.

![image401.png](images/image401.png)

As a consequence, the packets transmitted per second = Total Packets Transmitted / 300 seconds.

![image402.png](images/image402.png)


## ESXi

In vSphere Client, you can’t see the virtual network traffic. The following shows that you can only see the physical network card.

![image403.png](images/image403.png)

The metrics are provided at both physical NIC card and ESXi level. The counter at host level is basically the sum of all the vmnic instances. There could be small variance, which should be negligible.

![image404.png](images/image404.png)

Just like vCenter, VCF Operations also does not provide the metrics at the Standard Switch and its port groups. This means you cannot aggregate or analyze the data from these network objects point of view. You need to look at the parent ESXi one by one. Create a dashboard with interaction to cycle through the ESXi hosts.

### Contention Metrics

In addition to the dropped packet, there are 2 other metrics tracking contention. They are error packets and unknown protocol frames.

#### Error Metrics


![image405.png](images/image405.png)

A packet is considered unknown if ESXi is unable to decode it and hence does not know what type of packet it is. You need to enable this metric in VCF Operations as it’s disabled by default.
Expect these error packets, unknown packets and dropped packets to be 0 at all times. The following shows from a single ESX:

![image406.png](images/image406.png)

To see from all your ESXi, use the view “vSphere \ ESXi Bad Network Packets”.

![image407.png](images/image407.png)

The hosts with error RX spans across different clusters, different hardware models and different ESXi build number. I can’t check if they belong to the same network.
If you see a value, drill down to see if there is any correlation with other types of packets. In the following example, I do not see any correlation.

![image408.png](images/image408.png)

What I see though, is a lot of irregular collection. I marked with red dots some of the data collection.

![image409.png](images/image409.png)

You can see they are irregular. Compare it with the Error Packet Transmit counter, which shows a regular collection.

![image410.png](images/image410.png)


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


![image411.png](images/image411.png)

You’ve seen the dropped packet situation at VM. That’s a virtual layer, above the ESXi. What do you expect to see at ESXi layer, as it’s physically cabled to the physical top of rack switches? The counter tracks packets that are dropped prior to the packet reaching the ESXi kernel. According to this KB, “quite often this counter is a combination of the values from other counters that can be found in the Private Statistics section of the nicinfo.sh.txt file that is contained in the commands directory of ESXi host log bundles.”
I plotted 319 production ESXi hosts, and here is what I got for Transmit. What do you think?

![image412.png](images/image412.png)

There are packet drops, although they are very minimal. Among 319 hosts, one has 362 dropped transmit packet in the last 3 months. That host was doing 0.6 Gbps on average and peaked at 8.38 Gbps.
As expected, the dropped packet rarely happened. At 99th percentile, the value is perfectly 0.
I tested with another set of ESXi hosts. Out of 123 servers, none of them has any dropped TX packet in the last 6 months. That’s in line with my expectation. However, a few of them experienced rather high dropped RX packets.

![image413.png](images/image413.png)


![image414.png](images/image414.png)

The dropped only happened since the ESXi had an increased load

![image415.png](images/image415.png)

If you see something like this, you should investigate which physical NIC card is dropping packet, and which VMK interface is experiencing it.
While the number is very low, many hosts have packet drops, so my take is I should discuss with network team as I expect data center network should be free of dropped packets.

##### Received

What do you think you will see for Received?
Remember how VM RX is much worse than VM TX? Here is what I got:

![image416.png](images/image416.png)

Surprisingly, the situation is the same for ESXi.
Some of them have >1 million packet dropped in 5 minute. Within these set of ESXi, some have regular packet dropped, as the value at 99th percentile is still very high. Notice none of the ESXi is dropping any TX packet.
I plotted the 2nd ESXi from the table, as it has high value at 99th percentile. As expected, it has sustained packet dropped lasting 24 hours. I marked the highest packet drop time, as it mapped to the lowest packets received.

![image417.png](images/image417.png)


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

![image418.png](images/image418.png)

I’m unsure why there are duplicates metrics.
We covered earlier that full duplex means the aggregated metric can exceed the physical speed. Notice the Usage Rate is the sum of Receive and Transmit on the following screenshot.

![image419.png](images/image419.png)

You can also plot each vmnic one by one. Since you may not know which one to plot for a given ESXi, you can show them all in table first.

![image420.png](images/image420.png)

For packets/second, the metrics are:

![image421.png](images/image421.png)

It’s interesting to divide the packet/second with the bits/second, as you get the packet size. If this number change drastically in large environment, it’s something worth investigating.

#### Unusual Packets


![image422.png](images/image422.png)

Your VM network should be mostly unicast traffic. So check that broadcast and multicast are within your expectation. Your ESXi Hosts should also have minimal broadcast and multicast packets.

![image423.png](images/image423.png)

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

![image424.png](images/image424.png)


#### Metric Used

Here is what I recommend, including their threshold.

![image425.png](images/image425.png)

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

![image426.png](images/image426.png)

The peak column is based on 20-second average. So it’s 15x sharper than the 300-second average. It gives better visibility into the microbursts. If the burst exists, you will see something like this, where the 20-second shows much worse value consistently.

![image427.png](images/image427.png)

Are you surprised to see that the 20-second peak is a lot worse than 15x worse? The preceding chart shows 10370 ms latency at 20-second vs 257 ms at 300 second.
The huge gap is due to 2 things
- There is only 1 or 2 microbursts, and it’s much higher than the average. This can happen on counter such as disk latency and CPU context switch, where the value can be astronomically high.
- There are many sets. A VM can have many disks. For example, a database VM with 20 virtual disks will have 40 sets of metrics. Each set has 15 datapoints, giving a total of 600 metrics. The peak is reporting the highest of 600 metrics. If the remaining is much lower, then the gap will naturally be high.

##### How are they chosen?

Take a look at the table below. It shows a VM with 2 virtual disks. Each disk has its own read latency and write latency, giving us a total of 4 metrics.

![image428.png](images/image428.png)

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

![image429.png](images/image429.png)

I copied into an external editor to show each metric as 1 line so you can see them more easily.
Free memory measures the disk space. It’s more important to see the latest value. Average of last 5 minutes is better than lowest 20-second period within that 5 minute period.
I’ve rearranged the metrics so you can see the 20 second peak metrics first.
Guest OS Free Memory is in KB, so we need to divide by 1024. Note the division can’t be part of the label.
There is no metric that sums the VM zipped page and swapped page, so I created a super metric for it.

##### The Green Range

See the concept of the 4 ranges in the Performance Modelling section of Chapter 1.
To see the threshold more easily, I rearranged the metrics from the smallest threshold, and have skipped the metrics with special logic. They will be covered later.

![image430.png](images/image430.png)

Let’s go through the first line. It checks if network TX dropped is below 0.25%, it will prorate the value to a number between 75% and 100%. To prorate, we do this logic:
- Divide the value with the green range size to get the fraction.
- Multiply the result by 25 to adjust the scale to 25 points.
- Subtract the result from 100 (perfect score), the starting line for green.
BTW, I didn’t add the * 1 weightage multiplier for green at the end to keep the formula simpler. Mathematically it’s not required.
Now let’s look at CPU Run, as it’s a special case.

![image431.png](images/image431.png)

The range of green is 60% – 80%, not 0 – 80. This means utilization below 60% is given a perfect score of 100%.
Why do we take the maximum of Run – 60 and 0? To ensure we don’t have negative value when the CPU Net Run metric is below 60%. This max() function will return 0, hence giving us 100 – 0 = 100%.
Now let’s look Guest OS Free Memory.

![image432.png](images/image432.png)

This one is special as the threshold is going descending. We also need to convert the unit from KB to MB.
We want the value of free memory > 512 MB of RAM to translate into 100%. Since the formula returns 0% - 25%, I had to add 75.

##### The Yellow Range

When the metric value does not within green threshold, it gets evaluated for yellow.
The outcome is 50% - 75%, hence the formula deducts from 75.
Just like the green range, let’s start with the easy ones. You notice the following looks similar to the green range.

![image433.png](images/image433.png)

Let’s go through the first line. It checks if network TX dropped is below 0.5%, as it’s definitely above 0.25%.
It then prorates the value to a number between 50% and 75%. To prorate, it applies a logic similar to the green range.
- Divide the value with the yellow range size to get the fraction.
- Multiply the result by 25 to adjust the scale to 25 points.
- Subtract the result from 75, the starting line for yellow.
The * 2 at the end is the weightage multiplier. Green is given a 1x weightage, while yellow is 2x, orange is 4x and red is 8x. The value is amplified, and then normalized again at a later portion (not shown in the screenshot).
As we’re not dealing with the edge of the range, the next 2 metrics have simpler logic.
For CPU Run, the logic becomes consistent with the simpler metrics. Just need to map 80% - 90% Run value to 75% - 50% range.

![image434.png](images/image434.png)

For Memory Free, we have to keep on dividing by 1024.

![image435.png](images/image435.png)


##### The Orange Range and Red Range

I’m showing them together as it’s an IF THEN ELSE. Whatever not caught by the orange is handled by red.

![image436.png](images/image436.png)

What do you notice in the red range?
It has a min() function. This is to guard against a very large value. For example, in CPU Ready, any value above 8% will be given a score of 0%, not negative.
The formula for CPU Run becomes simpler as it cannot go above 100. We do not need to do the min() function for the red range.

![image437.png](images/image437.png)

The expression 50 – caps the value of orange at 50%, while the red is capped at 25.
The * 4 at the end is the weightage multiplier for orange. The * 8 at the end is the weightage multiplier for red.
Now let’s look at the remaining metrics.
For Guest OS Memory Free, since the threshold is descending, the logic is simpler as the value cannot be less than 0.

![image438.png](images/image438.png)


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

![image439.png](images/image439.png)

The time unit is in microseconds. The expected time is 200 milliseconds. Anything over one million microseconds (one second) is a cause for concern.
Log Insight has a metric called vmw_esxi_vmdowntime. Plot the worst value as it’s a leading indicator.

![image440.png](images/image440.png)


#### Stun Time

Stun Time is the period the VM gets a checkpoint stun, where no guest instruction is executed on the same vmx file. Operations that incur checkpoint are device reset, disk branching, disk promotion, snapshot take, and snapshot consolidate. A long stun time will impact Guest OS performance.
During the first phase of a vMotion operation, a snapshot is created for the VM. Snapshot means a delta VMDK is being created, which requires a stun operation. The VM then switches its write operations to the delta disk.
The time unit is in microseconds. 200 millisecond is a good threshold, and anything above 1 second should be investigated.

![image441.png](images/image441.png)

Log Insight has a metric called vmw_esxi_vmprecopystuntime. Plot the highest value as it’s a leading indicator.

![image442.png](images/image442.png)

Complement the above trend chart with a table that shows the ESXi host. Note the table does not show the VM name.

![image443.png](images/image443.png)


#### Copy Bandwidth

Since this is a consumption metric, ensure the values are not too low, as that will slow down vMotion progress.
The bandwidth (Gb/s) should be relatively stable and matches the assigned capacity for vMotion traffic.

![image444.png](images/image444.png)


### Latency Sensitivity

You can reduce the latency and jitter caused by virtualization by essentially “reserving” the physical resource to a VM. In the vSphere Client UI, edit VM settings, and go to VM Options tab.

![image445.png](images/image445.png)

Scroll down until you see this option.

![image446.png](images/image446.png)

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

![image447.png](images/image447.png)

So you have an interesting situation here. Demand is 100%, Usage is 0%, yet Contention is 0%.
Now let’s plot what happened to Wait and Idle. Notice both went from 100% to 0%.

![image448.png](images/image448.png)

So if you combine Run, Demand, Wait and Usage metrics, you can see basically Run and Demand shot up to 100% as Wait drops to 0%, while Usage is oblivious to the change.

![image449.png](images/image449.png)

Just for documentation purpose, System and Ready are obviously not affected.

![image450.png](images/image450.png)


#### Memory Impact

Memory is fundamentally storage. So I do not expect any of the counters to go up. They will go up when the VM actually needs them.

![image451.png](images/image451.png)

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

![image452.png](images/image452.png)

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

![image453.png](images/image453.png)

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

![image454.png](images/image454.png)

Here is an example where Usage is lower.

![image455.png](images/image455.png)

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

![image456.png](images/image456.png)

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

![image457.png](images/image457.png)

For each of the group, there is basic set of metrics. Here it is for memory:

![image458.png](images/image458.png)

The group Cluster Services only provides 3 metrics:

![image459.png](images/image459.png)


#### VM Operations

vSphere Cluster, being the main object where VM runs, has a set of event metrics. They count the number of times an event, such as a VM gets deleted, happens. This provides insight into the dynamics of the environment.

![image460.png](images/image460.png)

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

![image461.png](images/image461.png)

A logical question here would be what’s the impact on VM performance? Are they getting the CPU they asked? The cluster has 550 running VM.
This is where the contention metrics come in. One tracks the depth of the problem, the other the breadth of the problem.
The counter Percentage of VMs facing CPU Ready > 1% shows a nearly identical pattern. We can see that a big percentage of the VM population is affected.

![image462.png](images/image462.png)

The second counter tracks the depth, giving the absolute worst CPU Ready value experienced by any VM in the cluster.

![image463.png](images/image463.png)


#### Example showing no Correlation

Performance is unmet demand. VM 007 can face very high contention when all other VMs on the same cluster face no contention.
It is possible for VMs in the cluster to suffer from poor performance, while the cluster utilization is low. One main reason is cluster utilization looks at the provider layer (ESXi), while performance looks at individual consumer (VM).
The following cluster has 32 ESXi supporting 2357 VM. The average demand across the cluster is <40%. Since it has 32 ESXi and 2357 VM, we can retire 8 ESXi or add 1K VM.

![image464.png](images/image464.png)

And yet the VMs in the clusters are facing contention. Both VM CPU Ready and CPU Co-stop are high.

![image465.png](images/image465.png)

Let me take another example, where you can see the corelation between cluster utilization and VM contention in the cluster. My apology that the picture is not sharp. You can see the cluster has 774 running VM at the start. One month later it has dropped to 629, a drop of 145 VM or 19%. The second line chart reveals the number of running vCPU dropped from 3019 to 1980, a whopping 1039 vCPU or 34%. That indicates the big VMs were moved out.
This cluster was running mission critical VMs. What’s going on?! What caused the mass evacuation.
Notice the mass evacuation happened multiple times, so it’s not accidental.
Looking at the last chart. It has 2 line. Maroon showing utilization, blue showing contention. Can you figure out what happened?

![image466.png](images/image466.png)

The cluster utilization was hovering around 50%. In that entire month, it barely moved. This cluster was probably 16 nodes, so 50% utilization means you can easily take out a few ESXi hosts actually.
The Max VM CPU Contention told a different story. Notice it spiked well above 75%. That impacted at least 1 VM. There were multiple spikes, leading to multiple complaints, and eventually infrastructure was forced to evacuate the cluster to fix the performance problem. Notice the counter dropped gradually in November, despite utilization remains fairly stable.

#### Example for Memory

We covered 2 examples for CPU. What about memory, since it’s a form storage. It’s just a disk space basically, so can VM experience contention when Cluster consume metric is not high?
I’d zoom into ESXi, so it’s easier to see. What do you deduce from this ESXi? This chart shows 1 month worth of data.

![image467.png](images/image467.png)

It has 759 GB of usable memory. All the powered on VM has 444 GB configured, out of which only 413 GB is mapped to physical DIMM. So there is plenty of memory left.
To confirm that it has plenty of memory, let’s plot Balloon. What do you expect?

![image468.png](images/image468.png)

There is no ballooning. ESXi was under no memory pressure whatsoever.
So that’s the situation at provider level. How about consumer level?
VCF Operations has a metric that tracks the highest memory contention experienced by any VM in the host. This is a good leading indicator as all it takes is 1 VM, it matters not which VM.
As we can see here, there is a problem.

![image469.png](images/image469.png)

Can you explain why?
A VM experiences contention when the page is not in the DIMM. It was compressed or swapped out. Checking the compressed metric, it reveals that pages had to be brought it. Notice the swap metric lagged a bit, which makes sense.

![image470.png](images/image470.png)

I am not able to explain the earlier dropped, the one in red circle. If you can drop me a note.
Let’s complete by plotting Swapped. I’m plotting all the way to the beginning of tracking.
It’s all 0. What happened?
That means all the pages could be compressed, so ESXi decided to compress instead of putting them into swapped file.
Now that we know it’s due to compression, we know the contention on 5 September was caused by compression. When was that page compressed, no one knows. Plotting back, the compression started around 2 August.

![image471.png](images/image471.png)

The compression was only 342 MB. Not even 0.1% of consumed memory. But if you are unlucky, it was the active VM that got hit, as in the case here.
The past is harder to debug, as we lack the ability to travel back in time and see the environment as it was. My guess here is the VM had limit, be it indirectly via resource pool or directly.

### Cluster Performance (%)

We’ve covered in the VM chapter how we quantify the KPI of a single VM. How would you represent all the VMs in the cluster? Do you simply average the VM KPI (%)?
The answer is no. A cluster has a different purpose to a VM, so we need to see it from cluster point of view. For examples:
- Contention inside a VM (this means Windows or Linux) is not that relevant to the cluster performance.
- ESXi physical network is relevant to the cluster performance, but not to the VM performance.
A cluster is more of a group of ESXi hosts serving a VM.

![image472.png](images/image472.png)

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

![image473.png](images/image473.png)

What do you think will happen to the VM CPU Ready and CPU Co-stop?

![image474.png](images/image474.png)

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

![image475.png](images/image475.png)

All the super metrics are fairly simple. They are simply taking the average or the maximum of either ESXi or VM in the cluster.
Something a little trickier is Ballooned (%). The formula is below.

![image476.png](images/image476.png)

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

![image477.png](images/image477.png)

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

![image478.png](images/image478.png)

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

![image479.png](images/image479.png)


##### Relative Comparison

You will notice major differences in the way the resource groups consume resources.

|  | CPU | Memory |
| --- | --- | --- |
| System | Surprisingly low. It can be well below 1 GHz. | Relatively high. It’s ~20 – 30 GB depending on the ESXi |
| VIM | Relatively high. It’s around 4 – 12 GHz depending on the ESXi. | Surprisingly low. It could be even 0 GB. |


![image480.png](images/image480.png)


##### Metrics

In the vSphere Client UI, you will see the list of resource grouping in the Target Objects section in the performance chart.
I’ve highlighted them in the following screenshot:

![image481.png](images/image481.png)

To see the kernel consumption, select only these 3 from the list above:
- host/iofilters
- host/system
- host/vim.
The rest of the items are part of them, so no need to plot them. More importantly, they are fairly small, well below 0.5 GHz. The following screenshot shows their highest 20-second average in the last 1 hour.

![image482.png](images/image482.png)

To see their total, plot their values in vCenter by stacking up their values, as shown below.

![image483.png](images/image483.png)


### CPU

When you buy a CPU, what exactly is the capacity that you actually get?
To recap, this is what vSphere uses for ESXi.

![image156.png](images/image156.png)

vSphere simply takes the base frequency x number of cores.
- It does not include turbo boost
- It does not include hyper threading.
The above is great for mission critical, where you need to be conservative and performance takes priority. For the rest of the workload, you can actually squeeze more. However, you need to set expectation as as the CPU speed depends on the model you buy.
I recommend you optimize the above answer. You can get more while keeping the trade off low. How?
Let’s answer with a simple example. You have 2 ESXi servers:

![image484.png](images/image484.png)

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

![image485.png](images/image485.png)

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

![image486.png](images/image486.png)

Yes, the roll up of the counter.
In general, when you take the latest value of something, you tend to get a much higher value than averaging the entire period.

##### Utilization

There are 3 counters provided to track the actual utilization.
- Usage
- Running
- Active
Usage is what you should use as it has the 4 resource groups and their sub pools.
Running and Active counters only has these 3 objects, hence they are less useful. You lose host/user, host/opt so you won’t get complete picture.

![image487.png](images/image487.png)

Plus, Active uses “latest” as its rollup.
If you still need to know about Active and Running, reach out to me and happy to share more details.

###### Usage

Now that we know which counters to use, what do you expect the values of the 4 groups?
Here is a sample from ~400 ESXi hosts, where I sort the top 7 from highest System usage.

![image488.png](images/image488.png)

The bottom two rows show the summary. The first summary is the average among all the hosts, while the last row is the highest value.
Usage maps to the ESXi CPU Usage metrics under CPU group.

![image489.png](images/image489.png)

The value at host matches the value of CPU Usage. This means the metric CPU \ Usage (MHz) is the same with System \ Resource CPU Usage (Average) (MHz).
As the value contains VM metrics, the value is much higher than the kernel. You can see the host/system is far lower.

![image490.png](images/image490.png)


###### Real World Samples

I plotted 364 ESXi hosts running production workload. All of them are doing at least 100 GHz and are running vSAN and NSX. For vSAN, they are a mixed of OSA and ESA architecture.
The line below shows the kernel relative to the total CPU Usage.

![image491.png](images/image491.png)

In terms of absolute utilization, the actual utilization has a wide range. This is despite all these ESXi were running at least 100 GHz.

![image492.png](images/image492.png)

Take note there is no perfect correlation between kernel utilization and VM utilization. This is especially true when the kernel has NSX and vSAN. All these 364 ESXi were running vSAN (mixed of OSA and ESA) and NSX.
The following chart shows that a great majority were below 10%. There is no strong correlation between the relative overhead and the absolute overhead.

![image493.png](images/image493.png)

Another measurement, taken at a different time. This time there were 557 ESXi with CPU Usage > 100 GHz, with 2 of them clocking > 170 GHz.

![image494.png](images/image494.png)

There were 2 outliers at > 40 GHz, highlighted in orange. The hypervisor overhead remains steady at 100 GHz vs > 150 GHz. I drew a red line at 25 GHz to show that majority of the numbers are below this.
Plot the values across all your ESXi hosts. If you take enough hosts, you will notice the values vary. The following chart shows 558 ESXi hosts. Almost all are running both vSAN and NSX. They are all running at least 100 GHz. What do you notice?
Yes, there is hardly any correlation between total CPU Usage and hypervisor CPU Usage.
I drew the following illustration to show the lack of predictable relationship between hypervisor CPU reservation, hypervisor CPU usage and total CPU usage.

![image495.png](images/image495.png)


###### Network Impact

What’s the kernel overhead to do network packet processing?
The following ESXi was doing > 40 Gigabit per second multiple times. It was processing > 3 million packets.

![image496.png](images/image496.png)

Hardly any impact on the kernel. The kernel was less than 8 GHz.

![image497.png](images/image497.png)


###### Storage Impact

Storage IO processing can require more kernel if the IOPS and throughput are high. The following ESXi hit > 200K IOPS two times.

![image498.png](images/image498.png)

You can see a corresponding spike in the kernel. It went above 10 GHz.
The red dot is because of network.

![image499.png](images/image499.png)


##### Reservation

Utilization is relatively more volatile or dynamic, while reservation is logically more stable. The following screenshot shows CPU Usage fluctuates every 20 seconds, while reservation remains perfectly constant. Expect Usage to be higher reservation at high utilization.

![image500.png](images/image500.png)

Notice the maximum limited value is perfectly flat. That’s what you want as kernel processes should not have a limit.
The above is for host/system. The reservation is surprisingly low.
Now let’s look at host/vim. What do you notice from the following screenshot?

![image501.png](images/image501.png)

Surprisingly the reservation is not low. It’s around 6.6 GHz.

###### Real World Samples

The above is from 1 ESXi. We need to plot for many to get a better understanding. The following diagram shows the distribution of the kernel overhead based on a sample of almost 400 ESXi in production environment.

![image502.png](images/image502.png)

By far the majority of the values lie in 6 – 10 GHz.
Their values tend to be stable over days, although from time to time I see fluctuating metrics, which is reasonable as there are multiple factors impacting the reservation.
The following chart shows both the fluctuating pattern and steady pattern (most common). They are from 2 ESXi hosts.

![image503.png](images/image503.png)


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

![image504.png](images/image504.png)

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

![image505.png](images/image505.png)

The number dropped to well below 10% once Consumed passed 800 GB. This means that the absolute amount plateau at a certain level. We can validate that by plotting the absolute utilization.

![image506.png](images/image506.png)

Interestingly, there are levels. From the preceding chart, you can see there are 5 groups of similar number range. I think it’s because of vSAN configuration.

##### Reservation

The metric name is Memory \ ESX System Usage (KB).
It is a raw counter from vCenter. Just in case you’re wondering, the name ESX System Usage is a legacy name.

![image507.png](images/image507.png)

The following is an ESXi 6.7 U3 host with 1.5 TB of memory. Notice the kernel values remains constant over a long period. The number of running VM eventually dropped to 0. While the Granted counter drops to 1.5 GB (not sure what it is since there is no running VM), the kernel did not drop. This makes sense as they are reservation and not the actual usage.

![image508.png](images/image508.png)

Based on a sample of 500+ ESXi hosts, the range varies from 6 GB to 88 GB. In an ultra large ESXi with 12 TB RAM running vSAN and NSX, the reservation went up to 300 GB.

##### Utilization vs Reservation

Logically, utilization does not always correspond to the reserved amount. The following chart shows the reservation remains steady when the utilization drops by 90%, from 40 GB to single digit.

![image509.png](images/image509.png)

To see the actual usage, choose the metric Resource Memory Consumed metric from vSphere Client. Stack them, and you see something like this. The system part typically dwarfs the other 2 resources.

![image510.png](images/image510.png)

Do not take the value from Memory \ VMkernel consumed counter. That’s only the system resource. You can verify by plotting this and compare against host/system resource. You will get identical charts.

![image511.png](images/image511.png)

This value is for vSphere kernel modules. It does not include vSAN.

### Implementation

Download the Capacity Planning spreadsheet from here. It combines both models, and apply 3 class of services.

![image512.png](images/image512.png)


##### Total Capacity

The first thing you need to confirm is the size of the host. The spreadsheet comes with default values that I think provides a good balance between cost and size.

![image513.png](images/image513.png)


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


![image514.png](images/image514.png)

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

![image515.png](images/image515.png)


## Other Metrics


### Availability

The availability of a complex system such as an ESXi host is not a simple binary. There is degradation, which is important to distinguish to help manage in large farm.

![image516.png](images/image516.png)

Implementation using VCF Operations super metric:

![image517.png](images/image517.png)

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

![image518.png](images/image518.png)

There are relationships among some of the 10 panels, but they are not obvious as the UI simply presents them as a list. To facilitate understanding of the metrics, we need to group them differently.
So instead of documenting the 10 panels, I’d group the panels into 4.

| Group | Consumer | Provider | Remarks |
| --- | --- | --- | --- |
| CPU | Yes | Sort of | The CPU panel has a 4 line summary that provides the provider’s viewpoint.  I moved Power Management panel here as it only covers CPU. It does not cover memory, disk, network and other parts of the box (e.g. fan, motherboard). It complements the CPU panel as it covers the provider’s viewpoint. Take note that it does not show at socket level. And if you enable HT, it does not show at core level. I moved interrupt panel here as it’s about CPU. |
| Memory | 1 shared panel for both | 1 shared panel for both | Provider and Consumer are shown in 1 panel. The panel has a summary at the top, which cover the provider’s viewpoint |
| Storage | Yes | Almost | The Disk VM panel covers from consumer’s viewpoint. The Disk Adapter panel and Disk Device panel cover from provider’s viewpoint, and are best to be analyzed together.  BTW, notice the Path panel is missing. I moved vSAN panel here as all the metrics are disk metrics. There is no vSAN network and CPU counter, but you can see them in the respective network and CPU panel. |
| Network | 1 shared panel for both | 1 shared panel for both | Provider and Consumer are shown in 1 panel I moved RDMA device here as it’s about network card |


#### Export


![image519.png](images/image519.png)

Avoid exporting to CSV file. If you need to do it, limit to specific metrics and keep the time short. If you collect everything, you end up with a large file (easily > 100 MB) with >10K metrics. The following shows 16384 metrics being collected.

### CPU

The CPU panel consists of 2 parts:
- Summary
- Detail. It shows a table.
Here is the summary section. It has 4 lines.

![image520.png](images/image520.png)

The first line shows the summary of the physical load average in the last 1 minute, 5 minute and 15 minutes, respectively.
The next 3 lines covers Used (%), Utilization (%) and Core Utilization (%). The reason why I swapped the order in the book is Used (%) is built upon Utilization, and it’s a more complex counter. You can see in the following screenshot that Used (%) hit 131% while Util (%) maxed at 100%.
Note that their values are in percentage, meaning you need to know what they use for 100%.

![image521.png](images/image521.png)

If you guess that Used (%) and Utilization (%) eventually map into vSphere Client metrics Usage (%) and Utilization (%), respectively, you are right. However, you need to know how they map.
PCPU means a physical, hardware execution context. That means it is a physical core if CPU SMT is disabled, or a physical thread inside a core if SMT is enabled. It does not mean CPU socket. A single socket with 10 cores and 20 threads will have 20 PCPU metrics.
The white vertical line shows where I cut the screenshot, as the text became too small and unreadable if I were to include all of them. Anyway, it’s just repeating for each CPU physical thread.
At the end of each 3 lines (after the white line in preceding screenshot), there are NUMA information. It shows the average value across each NUMA node (hence there are 2 numbers as my ESXi has 2 NUMA nodes). The number after AVG is the whole box, system wide average. The per NUMA node metric values are useful to easily identify if a particular NUMA node is overloaded.
The detail section takes a consumer view. It is different to the physical view above.
Take a look at the panel below. Notice something interesting?

![image522.png](images/image522.png)

It mixes VM and non VM processes in a single table. The non-VM also has Ready time. What it does not have is VM Wait, which is expected.
If you want to only show VMs, just type the capital letter V.
- Name based filtering allows regular expression based filtering for groups and worlds.
- Type the capital letter G to only show groups that match given string. This is useful when a host has large number of VMs and you want to focus on a single or set of interesting VMs.
- Once a group is expanded you can type the small letter g to show only the worlds that match the given string. This is useful when running a VM with many vCPUs and you want to focus on specific worlds like storage worlds or network worlds.
If you want to see all, how to tell which ones are VM? I use %VMWAIT column. This tracks the various waits that VM world gets, so it does not apply to non VM.
Notice the red dot in the picture. Why the Ready time is so high for system process?
Because this group includes the idle thread. Expand the GID and you will see Idle listed.
There are many columns, as shown below. The most useful one is the %State Times, which you get by pressing F.

![image523.png](images/image523.png)

The rest of the information are relatively static or do not require sub-20 second granularity.
You know that only Utilization (%) and Used (%) exist at the thread level because they are the only one you see at, as shown below.

#### CPU State

We covered earlier in the CPU Metric that there are only 4 states. But esxtop shows a lot more metrics.

![image524.png](images/image524.png)

So what does it mean? How come there are more than 4 states?
The answer is below. Some of these metrics are included in the other metrics.

![image525.png](images/image525.png)

Review the metrics below, starting with %USED.
Which one does not actually belong to a CPU state, meaning it’s not something you mix with the rest?

![image526.png](images/image526.png)

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


![image527.png](images/image527.png)


| SWTCH/s | Number of world switches per second, the lower the better. I guess this number correlates with the overcommit ratio, the number of VM and how busy they are.  What number will be a good threshold and why? |
| --- | --- |
| MIG/s | Number of NUMA and core migrations per second.  It will be interesting to compare 2 VM, where 1 is the size of a single socket, and the other is just a bit larger. Would the larger one experience a lot more switches? |
| WAKE/s | Number of time the world wakeups per second. A world wakes up when its state is changes from WAIT to READY. A high number can impact performance. |

The metric QEXP/s (Quantum Expirations per second) has been deprecated from ESXi 6.5 in an effort to improve vCPU switch time.
In rare case where the application has a lot of micro bursts, CPU Ready can be relatively higher to its CPU Run. This is due to the CPU scheduling cost. While each scheduling is negligible, having too many of them may register on the counter. If you suspect that, check esxtop, as shown below:

![image528.png](images/image528.png)


#### Summary Stats


![image529.png](images/image529.png)

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


![image530.png](images/image530.png)


| AMIN | Allocation Minimum. Basically, the reservation |
| --- | --- |
| AMAX | Allocation Maximum. Basically, the limit. |
| ASHRS | Allocation shares |
| AMLMT | Max Limited. I’m unsure if this is when it’s applied or not. |
| AUNITS | Units. For VM, this is in MHz. For the kernel module, this is in percentage. |


#### Power Stats

This complements the power management panel as it lists per VM and kernel module, while the power panel lists per ESXi physical treads (logical CPU).

![image531.png](images/image531.png)


| POWER | Current CPU Power consumption in Watts. So it does not include memory, disk, etc. |
| --- | --- |


#### Power Consumption

Power management is given its own panel. This measures the power consumption of each physical thread. If you disable hyper-threading, then it measures at physical core

![image532.png](images/image532.png)

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

![image533.png](images/image533.png)

Utilization (%) shows 100% for both. This means both threads run, hence competing.
The core is in Turbo Boost. The %A/MPERF shows frequency increase of 30% above nominal. The core is in C0 state and P0 state. This counter was introduced in ESXi 6.5. It is not available via vSphere Client UI.
Why is Used (%) for PCPU 10 and 11 are showing 63.0% and 62.9%?
Unlike Utilization (%) which adds up to 200%, Used (%) adds up to 100%. So each thread maxes out at 50%. But Used (%) considers frequency scaling. Since there is a turbo boost at 130%, you get 50% x 130% = 65%. Pretty close to the numbers shown there.

#### Interrupt

This panel captures the interrupt vectors. In the following screenshot, I’ve added 2 vertical white lines to show where I cropped the screenshot. It’s showing the value of each CPU thread, so the column became too wide.

![image534.png](images/image534.png)


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

![image535.png](images/image535.png)


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

![image536.png](images/image536.png)


| MCTL? | ‘Y’ means the line is a VM, as the kernel processes is not subjected to ballooning. |
| --- | --- |
| MCTLSZ (MB) | Memory Control Size is the present size of memory control (balloon driver). If larger than 0 hosts is forcing VMs to inflate balloon driver to reclaim memory as host is overcommitted |
| MCTLTGT (MB) | Amount of physical memory the ESXi system attempts to reclaim from the resource pool or VM by way of ballooning. If this is not 0 that means the VM can experience ballooning. |
| MCTLMAX (MB) | Maximum amount of physical memory the ESXi system can reclaim from the resource pool or VM by way of ballooning. This maximum depends on the type of Guest OS. |


##### Compressed & Swapped

I think that Swap and Compressed should be shown together as what can’t be compressed is swapped.
Why am I showing Compressed first?
Because it’s faster than swapped.

![image537.png](images/image537.png)


| CACHESZ (MB) | Compression memory cache size. |
| --- | --- |
| CACHEUSD (MB) | Used compression memory cache |
| ZIP/s (MB/s) | The rate at which memory pages are being zipped. Once zipped, it’s not immediately available for the VM. This is a capacity problem. Your ESXi needs more RAM. If the pages being zipped is unused, the VMs will not experience memory contention. Keep this number 0. See Capacity chapter for details. |
| UNZIP/s (MB/s) | The rate at which memory pages are being unzipped so it can be used by VM. This is a performance problem. The pages are being asked. The VM CPU is waiting for the data. If you check the VM memory contention counter, it will not be 0%. Make sure that number is within your SLA or KPI. |


##### Swapped


![image538.png](images/image538.png)


| SWCUR (MB) | Swapped Current is the present size of memory on swapped. It typically contains inactive pages. |
| --- | --- |
| SWTGT (MB) | The target size the ESXi host expects the swap usage by the resource pool or VM to be. This is an estimate. |
| SWR/s (MB) | Swapped Read per second and Swapped Write per second. The amount of memory in megabyte that is being brought back to memory or being moved to disk |
| SWW/s (MB) | Swapped Read per second and Swapped Write per second. The amount of memory in megabyte that is being brought back to memory or being moved to disk |
| LLSWR/s (MB) | These are similar to SWR/s but is about host cache instead of disk. It is the rate at which memory is read from the host cache. The reads and writes are attributed to the VMM group only, so they are not displayed for VM.  LL stands for Low Latency as host cache is meant to be faster (lower latency) than physical disk.  Memory to host cache can be written from both the physical DIMM and disk. So the counter LLSWW/s covers all these sources, and not just from physical DIMM. |
| LLSWW/s (MB) | These are similar to SWR/s but is about host cache instead of disk. It is the rate at which memory is read from the host cache. The reads and writes are attributed to the VMM group only, so they are not displayed for VM.  LL stands for Low Latency as host cache is meant to be faster (lower latency) than physical disk.  Memory to host cache can be written from both the physical DIMM and disk. So the counter LLSWW/s covers all these sources, and not just from physical DIMM. |


##### NUMA

Logically, this statistic is applicable only on NUMA systems.

![image539.png](images/image539.png)


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


![image541.png](images/image541.png)


| MEMSZ (MB) | Amount of physical memory allocated to a resource pool or VM. The values are the same for the VMM and VMX groups.  MEMSZ = GRANT + MCTLSZ + SWCUR + "never touched"  I’m unsure where the compressed page goes. It’s still occupying space but 50% or 25%. |
| --- | --- |
| GRANT (MB) | Do not confuse it with Consumed 😊 |
| CNSM | Yup, this is that legendary Consumed metric. |
| SZTGT (MB) | Size Target in MB. Amount of machine memory the ESXi kernel wants to allocate to a resource pool or VM. The values are the same for the VMM and VMX groups. |
| TCHD (MB) | The size of touched pages in MB Working set estimate for the resource pool or VM. The values are the same for the VMM and VMX groups. |
| TCHD_W | As per above, but only for the write operations. A relatively much lower value compared to TCHD means the activities are mostly read. |


##### Overhead

I find overhead is a small amount that is practically negligible, considering ESXi nowadays sports a large amount of RAM. Let me know the use case where you find otherwise.

![image542.png](images/image542.png)


| OVHD (MB) | Current space overhead for resource pool. |
| --- | --- |
| OVHDMAX (MB) | Maximum space overhead that might be incurred by resource pool or VM. |
| OVHDUW (MB) | Current space overhead for a user world. It is intended for VMware use only. |


##### Shared


![image543.png](images/image543.png)


| ZERO (MB) | Resource pool or VM physical pages that are zeroed. |
| --- | --- |
| SHRD (MB) | Total amount that is shared. |
| SHRDSVD (MB) | Machine pages that are saved because of sharing.  Notice this counter does not exist in vSphere Client UI. |
| COWH (MB) | Copy on Write Hint. An estimate of the amount of Guest OS pages for TPS purpose. |


##### Active

The manual uses the word Guest to refer to VM. I distinguish between VM and Guest. Guest is an OS, while a VM is just a collection of processes. Guest has its own memory management that is completely invisible to the hypervisor.

![image544.png](images/image544.png)


| %ACTV | Active is covered in-depth in Active metric |
| --- | --- |
| %ACTVS | Percentage Active Slow and Percentage Active Fast. Slow is the slow moving average, taking longer period. Longer is more accurate. I don’t have a use case for the fast moving average. |
| %ACTVF | Percentage Active Slow and Percentage Active Fast. Slow is the slow moving average, taking longer period. Longer is more accurate. I don’t have a use case for the fast moving average. |
| %ACTVN | Percentage Active Next. It predicts of what %ACTVF will be at next sample estimation. It is intended for VMware use only. |


##### Committed

Committed page means the page has been reserved for that process. Commit is a counter for utilization but it’s not really used, especially for VM.
Note: none of these metrics exist in vSphere Client and VCF Operations, as they are meant for internal use.

![image545.png](images/image545.png)


| MCMTTGT | Minimum Commit Target in MB. I think this value is not 0 when there is reservation, but I’m not sure. |
| --- | --- |
| CMTTGT | Commit Target in MB. |
| CMTCHRG | Commit Charged in MB. I think this is the actual committed page. |
| CMTPPS | Commit Pages Per Share in MB |


##### Allocation & Reservation


![image546.png](images/image546.png)


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

![image547.png](images/image547.png)


#### VM

We begin with VM as that’s the most important one. It complements vSphere Client by providing unmap and IO Filter metrics.
You can see at VM level, or virtual disk level. In the following screenshot, I’ve expanded one of the VM. The VM shown as vRealize-Operat has 3 virtual devices.

![image548.png](images/image548.png)


##### Contention


| LAT/rd | Average latency (in milliseconds) per read. |
| --- | --- |
| LAT/wr | Average latency (in milliseconds) per write. |


##### Consumption


![image549.png](images/image549.png)


| CMDS/s | Count of disk IO commands issued per second. This is basically IOPS. Both the Read IOPS and Write IOPS are provided. |
| --- | --- |
| READS/s | Count of disk IO commands issued per second. This is basically IOPS. Both the Read IOPS and Write IOPS are provided. |
| WRITES/s | Count of disk IO commands issued per second. This is basically IOPS. Both the Read IOPS and Write IOPS are provided. |
| MBREAD/s | Total disk amount transferred per second in MB. This is basically throughput. Both the read throughput and write throughput are provided. |
| MBWRTN/s | Total disk amount transferred per second in MB. This is basically throughput. Both the read throughput and write throughput are provided. |


##### Unmap

It has unmap statistics. This can be useful that there is no such information at vSphere Client. In the UI, you can only see at ESXi level.

![image550.png](images/image550.png)


| SC_UMP/s | Successful, Failed and Total Unmaps per second.  Unmap can fail for a variety of reason. One example that was addressed in vSphere 6.7 Patch ESXi670-202008001 and documented in in KB is Guest OS does not refresh unmap granularities and keep sending unmap based on older value. Eventually limit is reached and the operation fail. |
| --- | --- |
| FL_UMP/s | Successful, Failed and Total Unmaps per second.  Unmap can fail for a variety of reason. One example that was addressed in vSphere 6.7 Patch ESXi670-202008001 and documented in in KB is Guest OS does not refresh unmap granularities and keep sending unmap based on older value. Eventually limit is reached and the operation fail. |
| UMP/s | Successful, Failed and Total Unmaps per second.  Unmap can fail for a variety of reason. One example that was addressed in vSphere 6.7 Patch ESXi670-202008001 and documented in in KB is Guest OS does not refresh unmap granularities and keep sending unmap based on older value. Eventually limit is reached and the operation fail. |
| SC_UMP_MBS/s | As above, but in MB/second. |
| FL_UMP_MBS/s | As above, but in MB/second. |


##### IO Filter

I/O Filter in ESXi enable the kernel to manipulate the IO sent by Guest OS before processing it. This obviously opens up many use cases, such as replication, caching, Quality of Service, encryption.
There is no such metric at vSphere Client. You will not find IO Filter metrics at both VM object and ESXi object.

![image551.png](images/image551.png)


| NUMIOFILTERS | Number of IO Filters |
| --- | --- |
| IOFILTERCLASS | Type of IO Filter Class |
| FAILEDIO | I think Failed IO should be 0 at all times. |
| TOTALIO | I think Failed IO should be 0 at all times. |
| LATENCY | I’m unsure if this latency measures the additional overhead introduced by IO Filter, or the total latency as seen by the VM. |


##### Configuration


![image552.png](images/image552.png)


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

![image553.png](images/image553.png)

Compare the above with what esxtop provides, which is the following:

![image554.png](images/image554.png)


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

![image555.png](images/image555.png)


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

![image556.png](images/image556.png)


###### Path/World/Partition

They are grouped as 1 column, and you can only see one at a time.
By default, none of them is shown. To bring up one of them, type the corresponding code. In the following screenshot, I’ve type the letter e, which them prompted me to enter one of the device.

![image557.png](images/image557.png)

Path is obviously the path name, such as vmhba0:C0:T0:L0.
A disk device can have >1 world, which I’m unsure why. You can see each world ID, and you get the statistics per world.

![image558.png](images/image558.png)

Partition shows the partition ID. Typically this is a simple number, such as 1 for the first partition. vSphere Client provides the following, which is more details yet easier.

![image559.png](images/image559.png)


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

![image560.png](images/image560.png)


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

![image561.png](images/image561.png)

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

![image562.png](images/image562.png)


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


![image563.png](images/image563.png)


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

![image564.png](images/image564.png)


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

![image565.png](images/image565.png)


#### RDMA Device

Remote Direct Memory Access (RDMA) enable direct access to the physical network card, bypassing the OS overhead. The following screenshot, taken from here, shows 2 types of access from application (that lives inside a VM. The VMs are not shown).

![image566.png](images/image566.png)


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

![image567.png](images/image567.png)

You also get the queue usage information.

| QP | Number of Queue Pairs Allocated and Completion Queue Pairs Allocated. RDMA uses these queues for communication. |
| --- | --- |
| CQ | Number of Queue Pairs Allocated and Completion Queue Pairs Allocated. RDMA uses these queues for communication. |
| SRQ | Number of Shared Receive Queues Allocated I think this is required in virtualization as the physical NIC card can be shared. |
| MR | Memory Regions Allocated. Check that this is inline with your expectation. |

For more reading on RDMA, I found this academic paper, title “Understanding the concepts and mechanisms of RDMA” useful.

##### Configuration

vSphere Client provides the following information. You get the first 4 columns in esxtop.

![image568.png](images/image568.png)

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

![image569.png](images/image569.png)


## CPU

Performance Monitor is still the main tool for Windows, despite the fact it has not been enhanced for decades. Go to docs.microsoft.com and browse for Windows Server. It took me to this article, which cover PerfMon. Many explanations on metrics at https://learn.microsoft.com/ are still based on end of life Windows.
PerfMon groups the counters under Processor group. However, it places the Processor Queue Length and Context Switches metrics under the System group. The System group covers system wide metrics, not just CPU.
The following screenshot show the counters under Processor group.

![image570.png](images/image570.png)

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

![image571.png](images/image571.png)


| First VM | Peak queue is very high at 79 but the CPU Run was low at 13%. The queue also dropped to 14 at the 99th percentile.  Conclusion: ignore it. |
| --- | --- |
| Second VM | Peak queue is very high at 59 but the CPU Run was low at 8%. The queue also dropped to a healthy range of 2 at the 99th percentile.  Conclusion: ignore it. |
| Third VM | Peak queue is very high at 46 and the CPU Run was moderate at 56%. The queue remained elevated at 26 at the 99th percentile.  Conclusion: check the details, and then proactively share the trend charts with VM Owner |
| Forth VM | Peak queue is very high at 46 but the CPU Run was very high at 97%. The queue remained elevated at 26 at the 99th percentile.  Conclusion: check the details, and then proactively share the trend charts with VM Owner. |

Let’s drill down on the 4th VM.
The following shows the utilization is flat near 100% and the queue varied between 9 to 45.

![image572.png](images/image572.png)

Because of the high queue, I recommend discussing with the application team on why their application behave this way.

#### Queue and Idle

It is possible that Guest OS shows high CPU queue when it was idling. This is abnormal, indicating the application created a lot of threads. The following shows the application was idling while having high queue.

![image573.png](images/image573.png)

The CPU Run Queue spikes multiple times. It does not match the CPU Usage. It also did not match CPU Context Switch Rate pattern. The spike only last 20 seconds, as the 5-minute average shows identical pattern but much smaller number.

![image574.png](images/image574.png)

The following is a 2 vCPU VM running Photon OS. CPU Queue is high, even though Photon is only running at 50%. Could it be that the application is configured with too many threads that the CPU is busy doing context switching? Notice the CPU Queue maps the CPU Context Switch Rate and CPU Run. In this situation, you should bring it up to the application team attention, as it may cause performance problem and the solution is to look inside. As a proof that it’s not because of underlying contention, I added CPU Ready.

![image575.png](images/image575.png)

What is the behaviour of CPU Queue? I profiled 800 VM in the last 1 month. For each VM, I extracted the peak value and the 99th percentile value. From the following scatter chart, you can see that the value at 99th percentile is less than half. Using a spreadsheet, the average value of the 99th percentile is 34% for peak that is ≥ 3.

![image576.png](images/image576.png)

BTW, the value from Guest OS displays the last observed value only; it is not an average. Windows & Linux do not provide the highest and lowest variants either.
The counter name in Tools is guest.processor.queue. For Windows, it is based on Win32_PerfFormattedData_PerfOS_System = @#ProcessorQueueLength from WMI
Reference: Windows
I can’t find documentation that states if CPU Hyper Threading (HT) technology provides 2x the number of queue length. Logically it should as the threads are at the start of the CPU pipelines, and both threads are interspersed in the core pipeline.

#### CPU Priority

If a process is often in queue, one possility is it has lower relative priority. Priority is a concept of Windows that ESXi does not have. ESXi uses a fair-share scheduler instead, as it does not have foreground processes.
Windows or Linux provides priority for foreground activities, as that’s what the user experience. For Windows, there are 6 levels as shown below. Ensure all your agents are given lower priority and limited CPU resource.

![image577.png](images/image577.png)


### Context Switch

CPU Context Switch costs performance “due to running the task scheduler, TLB flushes, and indirectly due to sharing the CPU cache between multiple tasks”. It’s important to track this counter and at least know what’s an acceptable behaviour for that specific application.
Context switches are considered “expensive” operations, as the CPU can complete many instructions within the time taken to switch context from one process to another. If you are interested, I recommend reading this paper.
Based on Windows 10 Performance Monitor documentation, context switches/sec is the combined rate at which all processors on the computer are switched from one thread to another. All else being equal, the more the processors, the higher the context switch. Note that thread switches can occur either inside of a single multi-thread process or across processes. A thread switch can be caused either by one thread asking another for information, or by a thread being pre-empted by another, higher priority thread becoming ready to run.
There are context switch metrics on the System and Thread objects. VCF Operations only report the total.
The rate of Windows or Linux switching CPU context per second ranges widely. The following is taken from a Windows 10 desktop with 8 physical threads, which runs around 10% CPU. I observe the value hovers from 10K to 50K.

![image578.png](images/image578.png)


#### Correlation

The value does not always correlate with CPU “utilization”, because not all CPU instructions require context switching. Overall, the higher the utilization the higher the chance of CPU context switch. I plotted 3328 VM on a scatter chart.

![image579.png](images/image579.png)

The above does not mean there is no correlation. The following chart shows a near perfect corelation. Every time CPU Usage went up, CPU Context Switch also. I should have plotted the disk IO or network IO as IO operations tend to require context switch.

![image580.png](images/image580.png)

CPU context switch can happen even in a single thread application. The following shows a VDI VM with 4 vCPU. I plotted the CPU Usage Disparity vs CPU Context Switch. You can see the usage disparity went up to 78%, meaning the gap between the busiest vCPU and the idlest vCPU is 78%. This was running a security agent, which is unlikely to be designed to occupy multiple vCPU.

![image581.png](images/image581.png)

Let’s plot the context switch at the same period. There is a spike at the same time, indicating that the agent was busy context switching. Note that it does not always have to be this way. The red dot shows there is no spike in context switch even though the vCPU Usage Disparity went up.

![image582.png](images/image582.png)


#### Range Analysis


![image583.png](images/image583.png)

The values of CPU Context Switch vary widely. For many VM, the values will be in low hundreds. In extreme situation, it can sustain well beyond 10 millions, as shown in the preceding chart. The above VM was not doing heavy IOPS nor high CPU usage. There was no correlation with these 2 metrics either.
Because of above, it’s important to profile and establish a normal base line for that specific application. What is healthy for 1 VM may not be healthy for another.

![image584.png](images/image584.png)

You can see from the table that some VM experience prolonged CPU context switch, while others do not. The VM #4 only has a short burst as the value at worst 5th percentile dropped to 3796. Momentary peak of context switch may not cause performance problem so in general it’s wiser to take the value somewhere between 95th and 99th percentile.
Let’s drill down to see the first VM. This CentOS VM sporting only 4 vCPU constantly hit almost 1 million context switches. The pattern match CPU Usage.

![image585.png](images/image585.png)

Do you add more CPU?
You should not, as the queue remain manageable. Check what the queue like on a more granular reading.
The following distribution chart shows the values from 11372 VMs. I had to use log-10 scale as the values vary wildly.

![image586.png](images/image586.png)

Majority of Guest OS spends well below 10K. You can see that the values between 0 – 10000 accounts for 80%.
Now that you know the wide distribution, you can use buckets. Adjust the bucket size by grouping all the values above 10K as one bucket, and splitting 0 – 10K bucket into multiple buckets. You can see more than half has < 1000 CPU Context Switch Rate.

![image587.png](images/image587.png)


#### Thread Ping Pong

The following is a Windows Server 2019 DC edition VM with 10 vCPU. It’s basically idle, as you can see below.

![image588.png](images/image588.png)

But if we zoom into each vCPU, they are taking turn to be busy.
In the span of just 1 hour, the 10 vCPU inside Windows take turn.

![image589.png](images/image589.png)

This is a bit illogical. Is this a process ping pong?
It is hard to tell
We can see them clearer if we stack them up. Notice they take turn, except the 3rd one from the top (I drew a green line on it). That one is actually fairly stable.

![image590.png](images/image590.png)

It is running Horizon Connection Server. It has around 118 – 125 processes, but much higher threads counts.

![image591.png](images/image591.png)

CPU Run Queue is very low, which is expected as the system is basically idle.
Context switches is fairly steady. The following screenshot shows it hovers between 34K and 37K switches per second. This is expected as it consistently run >2K threads on >100 processes on just 10 CPU. Each CPU does ~3.5K switches per second.

![image592.png](images/image592.png)


### DPC Time

According to System Center wiki, the system calls are deferred as they are lower priority than standard interrupts. A high percentage of deferral means Windows was busy doing higher priority requests.
They can happen even during low CPU utilization if there is issue with driver or application. The following screenshot is taken on Performance Monitor in Windows 11 laptop which was not running high. Notice the DPC time for CPU 0 is consistently higher than CPU 15, indicating imbalance. It did exceed >5% briefly. My Dell laptop has 8 cores 16 threads.

![image593.png](images/image593.png)

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

![image595.png](images/image595.png)

Let’s compare Performance Monitor and Task Manager:

![image596.png](images/image596.png)

CPU Usage in Windows is not aware of the underlying hypervisor hyper-threading. When Windows run a CPU at 100% flat, that CPU could be competing with another physical thread at ESXi level. In that case, what do you expect the value of VM CPU Usage will be, all else being equal?
62.5%.
Because that’s the hyper-threading effect.
What about VM CPU Demand? It will show 100% .
However, CPU Usage is affected by power management. Windows 8 and later will report CPU usage >100% in Task Manager and Performance Monitor when the CPU Frequency is higher than nominal speed. The reason for the change is the same with what we have covered so far, which is the need to distinguish amount of work being done. More here.

![image597.png](images/image597.png)

BTW, what does the Maximum Frequency mean?
Let’s show an opposite scenario, where CPU Usage (%) is low.

![image598.png](images/image598.png)

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

![image599.png](images/image599.png)

The Idle loop is typically executed on C3. Try plotting the Idle Time (%) and C3 Time (%), and they will be similar.

#### OS vs Process

CPU imbalance can happen in large VM.
Review the following chart carefully. It’s my physical desktop running Windows 10. The CPU has 1 socket 4 cores 8 threads, so Windows see 8 logical processors. You can see that Microsoft Word is not responding as its window is greyed out. The Task Manager confirms that by showing that none of the 3 documents are responding. Word is also consuming a very high power, as shown in the power usage column.
It became unresponsive because I turned on change tracking on a 500 page document and deleted hundreds of pages. It had to do a lot of processing and it did not like that. Unfortunately I wasn’t able to reproduce the issue after that.
At the operating system, Windows is responding well. I was able to close all other applications, and launched Task Manager and Snip programs. I suspect because Word does not consume all CPUs. So if we track at Windows level, we would not be aware that there is a problem. This is why process-level monitoring is important if you want to monitor the application. Specific to hang state, we should monitor the state and not simply the CPU consumption.
From the Windows task bar, other than Microsoft Word and Task Manager, there is no other applications running. Can you guess why the CPU utilization at Windows level is higher than the sum of its processes? Why Windows show 57% while Word shows 18.9%?

![image600.png](images/image600.png)

My guess is Turbo Boost. The CPU counter at individual process level does not account for it, while the counter at OS level does.
I left it for 15 minutes and nothing change. So it wasn’t that it needed more time to process the changes. I suspect it encountered a CPU lock, so the CPU where Word is running is running at 100%. Since Windows overall only reports 57%, it’s important to track the peak among Windows CPU. This is why VCF Operations provides the peak value among the VM vCPU.

## Memory

Windows memory management is not something that is well documented. Ed Bott sums it this article by saying “Windows memory management is rocket science”. Like what Ed has experienced, there is conflicting information, including the ones from Microsoft. Mark Russinovich, cofounder of Winternals software, explains the situation in this TechNet post.
Windows Performance Monitor provides many metrics, some are shown below.

![image601.png](images/image601.png)

In formula, here is their definition:
- Cached = Standby + Modified
- Available = Standby + Free
Available means exactly what the word means. It is the amount of physical memory immediately available for use. Immediately means Windows does not need to copy the existing page before it can be reused.
It is easier to visualize it, so here it is:

![image602.png](images/image602.png)

Microsoft SysInternal provides more detail breakdown. In addition to the above, it shows Transition and Zeroed.

![image603.png](images/image603.png)


### In Use

This is the main counter used by Windows, as it’s featured prominently in Task Manager.

![image604.png](images/image604.png)

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

![image605.png](images/image605.png)

Notice the Standby Normal fluctuates wildly, reaching as high at 90%. The other 2 cache remains constantly negligible. The chart above is based on >26000 samples, so there is plenty of chance for each 3 metrics to fluctuate.
Now let’s look at another example. This is a Windows Server 2016. I think it was running Business Intelligence software Tableau.

![image606.png](images/image606.png)

Notice the VM usable memory was increased 2x in the last 3 months. Standby Normal hardly move, but Standby Reserve took advantage of the increments. It simply went up accordingly, although again it’s fluctuating wildly.

### Cache

Cache is an integral part of memory management, as the more you cache, the lower your chance of hitting a cache miss. This makes sense. RAM is much faster than Disk, so if you have it, why not use it? Remember when Windows XP introduced pre-fetch, and subsequently Windows SuperFetch? It’s a clue that memory management is a complex topic. There are many techniques involved. Unfortunately, this is simplified in the UI. All you see is something like this:

![image607.png](images/image607.png)


### Free

As the name implies, this is a block of pages that is immediately available for usage. This excludes the cached memory. A low free memory does not mean a problem if the Standby value is high. This number can reach below 100 MB, and even touch 0 MB momentarily. It’s fine so long there is plenty of cache. I’d generally keep this number > 500 MB for server VM and >100 MB for VDI VM. I set a lower number for VDI because they add up. If you have 10K users, that’s 1 TB of RAM.
When Windows or Linux frees up a memory page, it normally just updates its list of free memory; it does not release it. This list is not exposed to the hypervisor, and so the physical page remains claimed by the VM. This is why the Consumed counter in vCenter remains high when the Active counter has long dropped. Because the hypervisor has no visibility into the Guest OS, you may need to deploy an agent to get visibility into your application. You should monitor both at the Guest OS level (for example, Windows and Red Hat) and at the application level (for example, MS SQL Server and Oracle). Check whether there is excessive paging or the Guest OS experiences a hard page fault. For Windows, you can use tools such as pfmon, a page fault monitor.
This is one the 3 major metrics for capacity monitoring. The other 2 metrics are Page-in Rate and Commit Ratio. These 3 are not contention metrics, they are utilization metrics. Bad values can contribute to bad performance, but they can’t measure the severity of the performance. Windows and Linux do not have a counter that measures how long or how often a CPU waits for memory.
In Windows, this is the Free Memory counter. This excludes the cached memory. If this number drops to a low number, Windows is running out of Free RAM. While that number varies per application and use case, generally keep this number > 500 MB for server VM and >100 MB for VDI VM. The reason you should set a lower number for VDI because they add up quickly. If you have 10K users, that’s 1 TB of RAM.
It’s okay for this counter to be low, so long other memory metrics are fine. The following table shows VMs with near 0 free memory. Notice none of them are needing more memory. This is the perfect situation as there is no wastage.

![image608.png](images/image608.png)


### Page File

Memory paging is an integral part of Guest OS Memory Management. OS begins using it even though it still has plenty of physical memory. It uses both physical memory and virtual memory at the same time. Microsoft recommends that you do not delete or disable the page file. See this for reference.

![image609.png](images/image609.png)

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

![image610.png](images/image610.png)

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

![image611.png](images/image611.png)

For a start, some of those numbers are really high!
They are above 1 millions. Assuming 8K block size, that’s 8 GB per second, sustained for 300 seconds.
What else do you notice?
Page-In is higher than Page-Out. I average all the 3K VMs and I got the following result:

![image612.png](images/image612.png)

Page-In is 4x higher in the max value. Page-In also sustains longer, while Page-Out drops significantly. At the 99th percentile mark, Page-In is 9x higher. I suspect it is the non-modifiable page, like binary. Since it cannot be modified, it does not need to be paged out. It can simply be discarded and retrieved again from disk if required.
The good news is both do not sustain, so the paging is momentary. The following shows that the value at 99th percentile can drop well below 5x.

![image613.png](images/image613.png)


![image614.png](images/image614.png)

To confirm the above, I downloaded the data so I can determine if the paging is indeed momentarily. Using a spreadsheet, I build a ratio between the 99th percentile value and the maximum value, where 10% means there is a drop of 10x. I plotted around 1000 value and got the following.

![image615.png](images/image615.png)

As you can see, majority of the paging drops drastically at 99th percentile.
Let’s dive into a single VM, so we can see pattern over time. I pick a database, as it does heavy paging. The following is a large Oracle RAC VM. Notice this has a closer ratio between page in and page out, and there is correlation between the two.

![image616.png](images/image616.png)

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

![image617.png](images/image617.png)


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

![image618.png](images/image618.png)

There are actually 2 metrics: One is a point in time and the other is average across the entire collection cycle. Point in time means the snapshot at the collection period. For example, if the collection is every 5 minute, then it’s number on the 300th second, not the average of 300 numbers.
Windows documentation said that “Multi-spindle disk devices can have multiple requests active at one time, but other concurrent requests await service. Requests experience delays proportional to the length of the queue minus the number of spindles on the disks. This difference should average < 2 for good performance.”

| guest.disk.queue | Win32_PerfFormattedData_PerfDisk_PhysicalDisk.Name = \"_Total\"#CurrentDiskQueueLength" from WMI |
| --- | --- |
| guest.disk.queueAvg | Win32_PerfFormattedData_PerfDisk_PhysicalDisk.Name = \"_Total\"#AvgDiskQueueLength" from WMI |

High disk queue in the guest OS, accompanied by low IOPS at the VM, can indicate that the IO commands are stuck waiting on processing by the OS. There is no concrete guidance regarding these IO commands threshold as it varies for different applications. You should view this in relation to the Outstanding Disk IO at the VM layer.
Based on 3000 production VMs in the last 3 months, the value turn out to be sizeable. Almost 70% of the value is below 10. Around 10% is more than 100 though, which I thought it’s rather high.

![image619.png](images/image619.png)

Strangely, there are values that seem to off the chart. I notice this in a few metrics already, including this. Look at the values below. Do they look like a bug in the counter, or severe performance problem?

![image620.png](images/image620.png)

Unfortunately, we can’t confirm as we do not have latency counter at Guest OS level, or even better, as application level. I am unsure if the queue is above the latency, meaning the latency counter does not start counting until the IO command is executed.
I plot the values at VM level, which unsurprisingly does not correlate. The VM is tracking IO that has been sent, while Guest OS Disk Queue tracks the one that has not been sent.

![image621.png](images/image621.png)

The preceding line chart also reveals an interesting pattern, which is disk queue only happens rarely. It’s far less frequent than latency.
Let’s find out more. From the following heat map, you can see there are occurrences where the value is >100.

![image622.png](images/image622.png)

However, when we compare between current value and maximum value, the value can be drastically different.

![image623.png](images/image623.png)

Let’s take one of the VMs and drill down. This VM has regular spikes, with the last one exceeding 1000.

![image624.png](images/image624.png)

Their values should correlate with disk outstanding IO. However, the values are all low. That means the queue happens inside the Guest OS. The IO is not sent down to the VM.

![image625.png](images/image625.png)

Which in turn should have some correlation with IOPS, especially if the underlying storage in the Guest OS (not VM) is unable to cope. The queue is caused by high IOPS which cannot be processed.

![image626.png](images/image626.png)

Finally, it would manifest in latency. Can you explain why the latency is actually still good?

![image627.png](images/image627.png)

It’s because that’s from the IO that reaches the hypervisor. The IO that was stuck inside Windows is not included here.
The application feels latency is high, but the VM does not show it as the IO is stuck in between.
Can the disk queue be constantly above 100?
The following VM shows 2 counters. The 20-second Peak metric is showing ~200 – 250 queue, while the 5-minute average shows above 125 constantly. The first counter is much more volatile, indicating the queue did not sustain.

![image628.png](images/image628.png)


# Epilogue

Thank you for reading the book. I hope it’s been valuable.
The book has taken me a long time. The following timeline summarizes its journey.

![image629.png](images/image629.png)

The book is a companion book to the main book (Private Cloud Operations). Part of its content dated back to 2012, when I first started blogging and sharing my learning. For the first 10 years, the book was part of the main book. As the main book exceeded 1000 pages, I had to trim down content. One outcome was the birth of vSphere Metrics as a separate book.
I shared details about how the 2 books evolved over the years in the main book.
Thank you
E1@broadcom.com