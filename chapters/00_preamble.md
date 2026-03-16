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