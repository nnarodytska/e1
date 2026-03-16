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