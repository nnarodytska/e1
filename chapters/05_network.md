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