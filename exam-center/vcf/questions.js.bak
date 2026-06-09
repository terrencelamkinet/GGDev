// VMware 2V0-13.25 Exam - All 89 Questions
// Complete Question Bank with Support for Single/Multiple Select

const questionBank = [
  // Question 1
  {
    text: "An architect has made an assumption that existing support staff are adequately skilled to operate the proposed infrastructure design.<br>The risk associated with this assumption would be that existing support staff are inadequately skilled to operate the proposed infrastructure design.<br>How would the architect mitigate the risk?",
    options: [
      { text: "Complete a skills assessment of the existing support staff to identity the skill gap.", value: "A" },
      { text: "Allocate the necessary time and budget to train existing support staff on the necessary skills required to operate.", value: "B" },
      { text: "Engage a third-party company to deploy and configure the proposed solution.", value: "C" },
      { text: "Hire additional support staff with the same skillsets to add more support capacity.", value: "D" }
    ],
    correct: "B",
    type: "radio",
    multi: false
  },
  // Question 2
  {
    text: "An architect is designing a VMware Cloud Foundation (VCF)-based solution.<br>The company policy mandates that all VCF patches and upgrades must be tested in a development environment before applying to production.<br>Which VCF construct design decision would comply with this mandate?",
    options: [
      { text: "Deploy two VCF vSphere Clusters within a VCF Domain.", value: "A" },
      { text: "Deploy two VCF Domains within a VCF Instance.", value: "B" },
      { text: "Deploy two VCF Instances within a VCF Fleet.", value: "C" },
      { text: "Deploy two VCF Fleets within a VCF Private Cloud.", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
    text: "An architect is responsible for designing a VMware Cloud Foundation (VCF)-based solution for a customer.<br>The customer has the following requirement:<br>There should be no single points of failure within the solution.<br>To comply with the customer requirement, the architect has decided to include physical NIC teaming for all ESX servers in the design.<br>When documenting this design decision, which consideration should the architect make?",
    options: [
      { text: "Only 10GbE NICs should be used for NIC teaming.", value: "A" },
      { text: "Embedded NICs should not be used for NIC teaming.", value: "B" },
      { text: "Each NIC team must include NICs from the same physical NIC Card.", value: "C" },
      { text: "Each NIC team must include NICs from different physical NIC Cards.", value: "D" }
    ],
    correct: "D",
    type: "radio",
    multi: false
  },
  {
    text: "An architect is designing a Business Continuity Disaster Recovery (BCDR) strategy for a Virtual Cloud Foundation (VCF) environment with a management domain and multiple workload domains deployed in two datacenters located in the same city.<br>During one of the initial workshops with stakeholders, the following information was identified:<br>• The Recovery Time Objective (RTO) for workloads is 24 hours.<br>• The management domain must remain continuously available with Recovery Point Objective (RPO) of 0.<br>• Hardware overhead should be minimized by utilizing standby resources that hosts test workloads during normal operation.<br>• Operational overhead should be minimized.<br>• Latency between both datacenters is 2 ms.<br>Which design decision should the architect document to satisfy provided requirements?",
    options: [
      { text: "Use VCF Automation to redeploy the entire environment in case of a failure.", value: "A" },
      { text: "Use asynchronous replication for both management and workload domains.", value: "B" },
      { text: "Back up all workloads daily and store them in a central repository to meet RTO expectations.", value: "C" },
      { text: "Implement vSAN stretched cluster for the management domain and Live Recovery for the workload domains.", value: "D" }
    ],
    correct: "D",
    type: "radio",
    multi: false
  },
  {
    text: "An architect is responsible for the design of a VMware Cloud Foundation (VCF) Fleet and the following risk has been identified:<br>RISK001: There is a risk that frequent infrastructure design changes may break Disaster Recovery (DR) plans and Service Level Objectives.<br>What should the architect suggest to mitigate this risk?",
    options: [
      { text: "Configure VM replication with recovery point object of 5 minutes or less for all workloads from the primary to DR site.", value: "A" },
      { text: "Setup monitoring & alerting against defined infrastructure service level objectives.", value: "B" },
      { text: "Develop a process to review and update DR plans between changes and schedule monthly end to end DR tests.", value: "C" },
      { text: "Limit infrastructure design change frequency to a maximum of once a month.", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },

  // --- Imported Questions 6-89 ---
  {
    text: "As part of the VMware Cloud Foundation (VCF) logical design, the architect documented the following requirement:<br>The solution must include high security hardening levels to meet military compliance standards.<br>Which two physical design decisions will meet this security requirement in the workload domain? (Choose two.)",
    options: [
      { text: "VCF Operations will be configured to renew the SSL certificate for vCenter Server per security policies.", value: "A" },
      { text: "The vSAN storage policy will be configured as Secondary Failures to Tolerate = 1.", value: "B" },
      { text: "The certificate of the VI workload domain vCenter Server will be issued by RootCA.Military.Domain.com.", value: "C" },
      { text: "The advanced setting UserVars.SuppressShellWarning will be configured to 0 across all ESXi hosts in a VI workload domain cluster.", value: "D" },
      { text: "NTP will be configured to the internal NTP servers of 192.168.12.1 and 192.168.24.1.", value: "E" }
    ],
    correct: ["C", "E"],
    type: "checkbox",
    multi: true
  },
  {
    text: "An architect is designing a new VMware Cloud Foundation (VCF) solution.<br>During the discovery workshops with the customer, the following information was shared:<br>• The company is structured into multiple business units.<br>• Some business units were formed through the acquisition of other companies.<br>• As the acquisitions were completed recently, these business units use their own Active Directory (AD) instances for authentication.<br>• All business units operate independently of each other, and need their own dedicated development environments.<br>The customer wants to use VCF Automation to provide its employees with the ability to self-service the provisioning and ongoing management of their resources within defined boundaries.<br>Which two design decisions should the architect include in the design when documenting the configuration of VCF Automation? (Choose two.)",
    options: [
      { text: "A VCF Automation tenant will be created for each business unit.", value: "A" },
      { text: "A VCF Automation project will be created for each business unit.", value: "B" },
      { text: "All tenants will be configured to use their dedicated AD instance for authentication.", value: "C" },
      { text: "All projects will be configured to use their dedicated AD instance for authentication.", value: "D" },
      { text: "All tenants will be configured to use the corporate AD instance for authentication.", value: "E" }
    ],
    correct: ["A", "C"],
    type: "checkbox",
    multi: true
  },
  {
    text: "An architect is responsible for designing a VMware Cloud Foundation (VCF)-based private cloud for a customer.<br>The architect noted the following requirements during a design workshop:<br>• Co-locate application workloads with VCF management component workloads within the same vSphere cluster.<br>• Shared storage data is always available and 100% current in the event of a single site outage.<br>• Have two sites available no more than 10 miles apart (10ms latency) connected with high speed network technology to host their virtual infrastructure.<br>• Protect against outages of a single site designated as an availability zone.<br>Which two storage technologies could meet the stated requirements? (Choose two.)[cite: 328-333]",
    options: [
      { text: "NVME over Fibre Channel (FC)", value: "A" },
      { text: "VMFS on Fibre Channel (FC)", value: "B" },
      { text: "vSphere Virtual Volumes (vVols)", value: "C" },
      { text: "NVME over TCP", value: "D" },
      { text: "vSAN", value: "E" }
    ],
    correct: ["B", "E"],
    type: "checkbox",
    multi: true
  },
  {
    text: "As part of the VMware Cloud Foundation (VCF) logical design, the architect has determined that the VCF Private Cloud will encompass multiple VCF instances contained within a single VCF Fleet.<br>The architect documented the following requirements when using VCF Operations:<br>• Monitoring downtime must be minimized.<br>• Alerting downtime must be minimized.<br>Which design decision supports these requirements? [cite: 385-387]",
    options: [
      { text: "Deploy two VCF Operations instances and configure the Aggregator Management Pack.", value: "A" },
      { text: "Deploy a single VCF Operations instance across a multi-VCF instance fleet.", value: "B" },
      { text: "Deploy VCF Operations using the High Availability model with Collector nodes at remote sites.", value: "C" },
      { text: "Deploy VCF Operations using the Simple model with Collector nodes at remote sites.", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
   text: "As part of the initial design workshop, one of the customer stakeholders has stated the following:<br>\"All Virtual Machines must be encrypted.\"<br>How would the architect classify this statement? [cite: 413-414]",
    options: [
      { text: "An Assumption", value: "A" },
      { text: "A Requirement", value: "B" },
      { text: "A risk", value: "C" },
      { text: "A Constraint", value: "D" }
    ],
    correct: "B",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is designing a VMware Cloud Foundation (VCF) solution for a customer.<br>During the discovery phase, the customer outlined the following availability requirements:<br>• All business-critical applications and workloads must adhere to a Recovery Point Objective (RPO) of 2 business hours.<br>• The infrastructure components supporting the VCF solution must comply with a Recovery Time Objective (RTO) of 8 business hours.<br>Based on this context, what does the RTO metric represent? [cite: 432-435]",
    options: [
      { text: "The minimum acceptable duration required to recover a service to an operational state", value: "A" },
      { text: "The maximum allowable time within which a system or service must be restored to a usable state", value: "B" },
      { text: "The maximum amount of data loss that is considered acceptable during a failure", value: "C" },
      { text: "The minimum volume of data loss tolerated in the event of a disruption", value: "D" }
    ],
    correct: "B",
    type: "radio",
    multi: false
  },
  {
   text: "An architect has compiled a list of statements following a workshop with the business stakeholders.<br>Which statement would be included in a conceptual model? [cite: 450-451]",
    options: [
      { text: "The solution must meet a Mean Time To Recovery (MTTR) of 6 hours.", value: "A" },
      { text: "Sites A and B will each have a stretched layer-2 for their management network.", value: "B" },
      { text: "The das.isolationshutdowntimeout setting will be configured to 120 seconds.", value: "C" },
      { text: "Users will connect to the application servers via the NSX Advanced Load Balancer.", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
    text: "The following requirements were gathered during the customer workshops:<br>• For critical transactional database workloads, the solution must provide low-latency and high performance storage to support processing of real-time financial transactions.<br>• For all non-critical workloads, the solution must provide the most efficient capacity utilization.<br>Which three design decisions would the architect make to meet the requirements for the workload domain cluster? (Choose three.)[cite: 472-474]",
    options: [
      { text: "Configure vSAN Policies (RAID-1) for all workloads.", value: "A" },
      { text: "Deploy a vSAN ESA cluster with a minimum of 6 nodes.", value: "B" },
      { text: "Configure vSAN Policies (RAID-5) for all critical transactional database workloads.", value: "C" },
      { text: "Configure vSAN Policies (RAID-5/6) for all non-critical workloads.", value: "D" },
      { text: "Deploy a vSAN OSA (All-NVMe) cluster with a minimum of 4 nodes.", value: "E" },
      { text: "Configure vSAN Policies (RAID-1) for all critical transactional database workloads.", value: "F" }
    ],
    correct: ["B", "D", "F"],
    type: "checkbox",
    multi: true
  },
  {
    text: "The architect documented a requirement for 99.95% high availability to meet the customer's resiliency needs.<br>Which two physical design decisions will help meet this requirement in the management domain? (Choose two.)[cite: 497-498]",
    options: [
      { text: "Host Overlay DHCP Scope Lease: 14 Days", value: "A" },
      { text: "vSAN Cache Tier Sizing: 800GB", value: "B" },
      { text: "Host isolation response: Power Off and restart VM", value: "C" },
      { text: "Physical Switch MTU: 9000", value: "D" },
      { text: "Management Port Group: Route based on physical NIC load", value: "E" }
    ],
    correct: ["C", "E"],
    type: "checkbox",
    multi: true
  },
  {
   text: "Which type of design would include specific details about server hardware, port connections, or Fibre Channel zones? [cite: 527]",
    options: [
      { text: "Logical", value: "A" },
      { text: "Service", value: "B" },
      { text: "Conceptual", value: "C" },
      { text: "Physical", value: "D" }
    ],
    correct: "D",
    type: "radio",
    multi: false
  },
  {
    text: "An architect is tasked to plan for an upgrade of an existing vSphere only deployment utilizing vSAN to VMware Cloud Foundation (VCF).<br>Which three new infrastructure components are required for the upgrade? (Choose three.)[cite: 539-540]",
    options: [
      { text: "SDDC Manager", value: "A" },
      { text: "VCF Operations", value: "B" },
      { text: "vSphere Supervisor", value: "C" },
      { text: "NSX", value: "D" },
      { text: "VCF Identity Broker", value: "E" }
    ],
    correct: ["A", "B", "D"],
    type: "checkbox",
    multi: true
  },
  {
    text: "An architect is responsible for designing a VMware Cloud Foundation (VCF)-based private cloud.<br>During the design requirements gathering workshop, the following information was captured:<br>• The solution must capture events from all infrastructure components of the VCF fleet.<br>• The solution must provide a single pane of glass management interface for troubleshooting, alerting, and monitoring using metrics, events, and flows.<br>• The solution must meet a 99.9% Service Level Agreement for Availability.<br>Which three design decisions should the architect make to meet the stated requirements? (Choose three.)[cite: 561-565]",
    options: [
      { text: "The solution will configure VCF Operations for logs to capture events from only VCF Management components.", value: "A" },
      { text: "The solution will configure the integration for VCF Operations and VCF Operations for logs.", value: "B" },
      { text: "The solution will configure the integration for VCF Operations and VCF Automation.", value: "C" },
      { text: "The solution will deploy VCF Operations for logs in a Simple model.", value: "D" },
      { text: "The solution will deploy VCF Operations for logs in a High Availability model.", value: "E" },
      { text: "The solution will configure VCF Operations for logs to capture events from all VCF infrastructure components.", value: "F" }
    ],
    correct: ["B", "E", "F"],
    type: "checkbox",
    multi: true
  },
  {
   text: "An architect is responsible for designing a new VMware Cloud Foundation (VCF)-based Private Cloud solution.<br>During the requirements gathering workshop with key customer stakeholders, the following information was captured:<br>• The solution must ensure all components are configured with SSL certificates that have been signed by the corporate Certificate Authority.<br>• The solution must ensure that users with administrative access are authenticated through an approved Identity Provider.<br>When creating the design document, which design quality should be used to classify the stated requirements? [cite: 588-591]",
    options: [
      { text: "Security", value: "A" },
      { text: "Recoverability", value: "B" },
      { text: "Manageability", value: "C" },
      { text: "Availability", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is responsible for designing a new VMware Cloud Foundation (VCF)-based Private Cloud solution.<br>During the requirements gathering workshop with key customer stakeholders, the following information was captured:<br>• The solution must support the monitoring of up to 10,000 objects.<br>• The solution must support 24 months retention for all monitoring data.<br>When creating the design document, which design quality should be used to classify the stated requirements? [cite: 601-604]",
    options: [
      { text: "Manageability", value: "A" },
      { text: "Availability", value: "B" },
      { text: "Performance", value: "C" },
      { text: "Recoverability", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
   text: "During a discovery workshop for a VMware Cloud Foundation (VCF) design, the customer provided the following information:<br>• Business Units pay for their own compute hardware.<br>• Business Units expect exclusive access to their compute hardware.<br>• IT Services is expected to maintain and manage all compute infrastructure within a single workload domain.<br>• IT Services are expected to design and offer standardized catalog items.<br>Which VCF Automation feature achieves this requirement? [cite: 622-624]",
    options: [
      { text: "Project Constraints", value: "A" },
      { text: "Cloud Account", value: "B" },
      { text: "Cloud Zones", value: "C" },
      { text: "Project-Level Placement Policy", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is responsible for designing a new VMware Cloud Foundation (VCF)-based Private Cloud solution.<br>During the requirements gathering workshop with key customer stakeholders, the following information was captured:<br>The solution must ensure that all workloads running on the platform comply with the Payment Card Industry Data Security Standard (PCI-DSS).<br>When creating the design document, which design quality should be used to classify the stated requirements? [cite: 648-650]",
    options: [
      { text: "Recoverability", value: "A" },
      { text: "Performance", value: "B" },
      { text: "Security", value: "C" },
      { text: "Manageability", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
   text: "Which statement would be classified as a functional (business) requirement? [cite: 661]",
    options: [
      { text: "The solution must provide the ability for users to view and track the progress of their requests.", value: "A" },
      { text: "Applications must be designed to tolerate the failure of a single datacenter.", value: "B" },
      { text: "Third-party pen testing must be executed against the solution yearly with a pass rate of 80 percent or higher.", value: "C" },
      { text: "The self service catalog must meet the Service Level Objective (SLO) of 75% successful requests measured over a 12 month period.", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
   text: "An organization is evacuating their current datacenter and moving all workloads to a new datacenter.<br>The organization has a total of 800 workloads to move, and the migration must be completed with no downtime within a planned change window that is scheduled to occur in four weeks.<br>What migration method will meet the requirements? [cite: 678-680]",
    options: [
      { text: "HCX Replication Assisted vMotion", value: "A" },
      { text: "Cross vCenter vMotion", value: "B" },
      { text: "HCX OS Assisted Migration", value: "C" },
      { text: "HCX Bulk Migration", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
    text: "An architect is responsible for designing a new VMware Cloud Foundation (VCF)-based private cloud.<br>During the discovery workshops, the following information was captured from key customer stakeholders:<br>• The private cloud will operate with three different monitoring levels:<br>• For the Self-Managed Service, the solution will be responsible for monitoring the virtual machine construct only.<br>• For the OS Managed Service, the solution will be responsible for monitoring operating system level metrics and virtual machine constructs.<br>• For the Fully Managed Service, the solution will be responsible for monitoring approved infrastructure applications, operating system level metrics, and virtual machine constructs.<br>The approved infrastructure applications are: Microsoft IIS, Microsoft SQL Server, MySQL, PostgresSQL, Tomcat Server, and Apache HTTPD.<br>For an application team to be able to deploy workloads into the private cloud, each workload must subscribe to a monitoring level at request time or when the service is onboarded.<br>The solution must ensure minimal management overhead for the ongoing management monitoring agents.<br>Which two design decision should the architect make to meet the stated monitoring requirements? (Choose two.)[cite: 695-702]",
    options: [
      { text: "Deploy the Open Source Telegraf Agent for all workloads that subscribe to the Fully Managed service.", value: "A" },
      { text: "Configure the Service Discovery for all workloads that subscribe to the Self-Managed service.", value: "B" },
      { text: "Deploy the Managed Telegraf Agent for all workloads that subscribe to the Fully Managed service.", value: "C" },
      { text: "Deploy the Managed Telegraf Agent for all workloads that subscribe Self-Managed service.", value: "D" },
      { text: "Deploy the Managed Telegraf Agent for all workloads that subscribe to the OS Managed service.", value: "E" }
    ],
    correct: ["C", "E"],
    type: "checkbox",
    multi: true
  },
  {
   text: "During a VMware Cloud Foundation (VCF) architectural design workshop, one of the stakeholders made the following comment:<br>\"The company has just used the remaining budget to purchase eight vSAN Ready Nodes for this project.\"<br>How would the architect classify this statement within the conceptual model document? [cite: 722-723]",
    options: [
      { text: "Constraint", value: "A" },
      { text: "Assumption", value: "B" },
      { text: "Requirement", value: "C" },
      { text: "Risk", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
   text: "A company is deploying a new VMware Cloud Foundation (VCF) environment to support their growing infrastructure requirements.<br>The company is planning to scale their environment over time by adding more workload domains as new applications and departments are onboarded.<br>The company requires that the architecture must be highly scalable and flexible, able to accommodate both current and future demands.<br>They also require a seamless transition when adding new workload domains.<br>Which design decisions should the architect make to meet the stated scalability requirements and facilitate the future growth? [cite: 739-743]",
    options: [
      { text: "Use a single workload domain for all departments and increase the size of the vSphere clusters as the demand grows.", value: "A" },
      { text: "Use multiple workload domains for each department and ensure that each workload domain is independently scaled.", value: "B" },
      { text: "Use multiple workload domains for each department but combine them into a single vSphere cluster to reduce complexity.", value: "C" },
      { text: "Use a single workload domain and rely on storage and network scaling to accommodate future growth.", value: "D" }
    ],
    correct: "B",
    type: "radio",
    multi: false
  },
  {
    text: "An architect is planning resources for a new cluster that will be part of an existing workload domain.<br>The new cluster will provide resources for a number of new workloads, including a mission-critical application consisting of five resource-intensive virtual machines.<br>The following requirements were provided for the new cluster:<br>• The solution must ensure that the new workload cluster meets the company's availability standard of N+1.<br>• The solution must minimize the overall investment in hardware.<br>Which two design recommendations should the architect make to meet the stated requirements? (Choose two.)[cite: 765-768]",
    options: [
      { text: "Use automated placement rules to keep the mission-critical application virtual machines apart.", value: "A" },
      { text: "Create a cluster with five hosts.", value: "B" },
      { text: "Use automated placement rules to keep the mission-critical application virtual machines together.", value: "C" },
      { text: "Use resource pools to prioritise resource for the mission-critical application virtual machines.", value: "D" },
      { text: "Create a cluster with six hosts.", value: "E" }
    ],
    correct: ["A", "E"],
    type: "checkbox",
    multi: true
  },
  {
   text: "An architect is designing a private cloud infrastructure based on VMware Cloud Foundation (VCF) for a client.<br>The architect documented the following requirements and constraints from the client.<br>• The client has three datacenters, all located within a 1 mile radius of the headquarter campus with high speed LAN connectivity between them.<br>• The private cloud must be hosted within the client's on-premise datacenter at their headquarters.<br>• The client would like to protect against outages with no data loss in the event of losing a single datacenter.<br>Which design model would meet these requirements and constraints? [cite: 819-824]",
    options: [
      { text: "VCF fleet with fault domains on a stretched cluster model", value: "A" },
      { text: "VCF fleet with disaster recovery on a single-rack cluster model", value: "B" },
      { text: "VCF fleet with disaster recovery on a multi-rack cluster model", value: "C" },
      { text: "VCF fleet with fault domains on a multi-rack cluster model", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is expanding an existing private cloud infrastructure based on VMware Cloud Foundation (VCF).<br>the requirement is to deploy two additional instances of VCF at two separate datacenters within the existing private cloud with minimal additional footprint.<br>• Datacenter A is 90 miles from the existing VCF fleet instance with a network round trip time of 90ms.<br>• Datacenter B is 120 miles from the existing VCF fleet instance with a network round trip time of 120ms.<br>Which design decision would meet the requirement for this expansion? [cite: 844-848]",
    options: [
      { text: "Deploy two additional VCF instances within the existing VCF fleet, one each in datacenters A and B.", value: "A" },
      { text: "Deploy an additional VCF fleet in datacenter B and an additional VCF instance within the existing VCF fleet in datacenter A.", value: "B" },
      { text: "Deploy two additional VCF fleets, one for each VCF instance in datacenters A and B.", value: "C" },
      { text: "Deploy an additional VCF fleet in datacenter A and an additional VCF instance within the existing VCF fleet in datacenter B.", value: "D" }
    ],
    correct: "B",
    type: "radio",
    multi: false
  },
  {
   text: "Which VMware Cloud Foundation (VCF) Storage Model can be deployed to scale storage capacity independent of compute and network? [cite: 886]",
    options: [
      { text: "vSAN Capacity Cluster Model", value: "A" },
      { text: "vSAN ESA Storage Cluster Model", value: "B" },
      { text: "vSAN Compute Cluster Storage Model", value: "C" },
      { text: "vSAN ESA Storage Model", value: "D" }
    ],
    correct: "B",
    type: "radio",
    multi: false
  },
  {
    text: "An architect is gathering business requirements for a new VMware Cloud Foundation (VCF) solution from the customer stakeholders and subject matter experts.<br>Which two factors should the architect discuss with the customer to determine any potential impact on the business requirements? (Choose two.)[cite: 915-916]",
    options: [
      { text: "Service-level agreements (SLAs)", value: "A" },
      { text: "Product versions", value: "B" },
      { text: "Storage capacity", value: "C" },
      { text: "Organizational structure", value: "D" },
      { text: "Average virtual machine size", value: "E" }
    ],
    correct: ["A", "D"],
    type: "checkbox",
    multi: true
  },
  {
   text: "An architect is working with an organization on the creation of a new VMware Cloud Foundation (VCF) Private Cloud.<br>The organization has provided the following business objectives they wish to achieve with the new platform:<br>• Reduce the operating costs associated with running separate areas of hosting capacity and separate/duplicate systems.<br>• Reduce the risks, time and effort associated with managing platforms that are out of vendor support.<br>• Reduce the operating costs associated with native public cloud usage.<br>• Reduce the risks associated with having incomplete documentation for application inventory and dependency mappings.<br>They have grouped these business objectives into a set of use cases:<br>• Migration - Provide a platform that supports the migration of virtualized workloads from existing platforms.<br>• Containerization - Provide a platform that supports the deployment of containerized workloads.<br>• Centralization and Consolidation - Provide a central private cloud platform accessible to all relevant areas of the business.<br>When considering these objectives and use cases, what should the architect include in the design documentation as a part of the Conceptual Model? [cite: 934-943]",
    options: [
      { text: "A requirement that the solution will provide support for provisioning and managing workloads based on virtualization and containerization technologies.", value: "A" },
      { text: "A constraint that the solution must be accessible via a HTTPS GUI to all relevant areas of the business.", value: "B" },
      { text: "A risk that the solution may not support the migration of containerized workloads.", value: "C" },
      { text: "An assumption that a complete mapping of application dependencies is not available.", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
   text: "An organization is designing a VMware Cloud Foundation (VCF) solution hosting a business-critical database.<br>The application owners specified the following requirements:<br>• All workload domains will use vSAN for storage.<br>• A maximum acceptable data loss of 5 minutes (Recovery Point Objective (RPO) = 5 minutes)<br>• An automated failover in case of a site outage where Recovery Time Objective should not exceed 30 minutes.<br>• The performance impact should be minimized.<br>Which design approach aligns with the application's requirement? [cite: 971-974]",
    options: [
      { text: "Use vSAN stretched cluster.", value: "A" },
      { text: "Use synchronous replication on the storage array level.", value: "B" },
      { text: "Use asynchronous replication with snapshots taken every 30 minutes to reduce storage impact.", value: "C" },
      { text: "Configure backup-based recovery with backup jobs scheduler set to every 30 minutes.", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is developing a VMware Cloud Foundation (VCF) solution with NSX VPC Full Services Model for single tenant with the following requirement:<br>The configuration must prevent advertisements from being dropped by the BGP loop detection check.<br>When designing the network architecture to support this solution, what element should be considered as part of the physical network design? [cite: 1005-1006]",
    options: [
      { text: "Use a unique, private BGP AS number for each Tier-0 gateway.", value: "A" },
      { text: "Configure edge datapath interface to transports only TEP traffic.", value: "B" },
      { text: "Use iBGP as the routing protocol between the Tier-0 gateway and the physical network.", value: "C" },
      { text: "Adjust the default BGP timers.", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is responsible for designing a new VMware Cloud Foundation (VCF)-based Private Cloud solution.<br>During the requirements gathering workshop with key customer stakeholders, the following information was captured:<br>• In the event of a disaster affecting the primary site, all tier 1 production services must be restored to the secondary site within 1 hour.<br>• In the event of a disaster affecting the primary site, all tier 3 production services must be restored to the secondary site within 8 hours.<br>When creating the design document, which design quality should be used to classify the stated requirements? [cite: 1029-1032]",
    options: [
      { text: "Manageability", value: "A" },
      { text: "Recoverability", value: "B" },
      { text: "Availability", value: "C" },
      { text: "Performance", value: "D" }
    ],
    correct: "B",
    type: "radio",
    multi: false
  },
  {
   text: "Which configuration should the architect recommend as part of the design of a VMware Cloud Foundation (VCF) solution to ensure optimal performance in a multi-tenant environment? [cite: 1037]",
    options: [
      { text: "Configure all workloads to operate on a single ESXi host to minimize network latency.", value: "A" },
      { text: "Allow an unlimited number of virtual machines per host to consume all available resources.", value: "B" },
      { text: "Implement vSAN with tiered storage policies to ensure high I/O performance and low latency for tenant workloads.", value: "C" },
      { text: "Use a single large datastore for all tenants to simplify management.", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
    text: "A financial services company is deploying a VMware Cloud Foundation (VCF)-based solution for its core banking applications.<br>The architect needs to ensure that the design can handle peak transaction loads while maintaining the performance SLA.<br>Which two approaches should be included in the design validation strategy? (Choose two.)[cite: 1055-1057]",
    options: [
      { text: "Conduct stress testing using representative workloads to evaluate system behavior under extreme load conditions.", value: "A" },
      { text: "Simulate peak transaction loads in a staging environment to validate resource scalability and vSAN performance.", value: "B" },
      { text: "Rely on vendor-supplied performance benchmarks that were provided for the selected hardware and validate manually the Live Recovery configuration.", value: "C" },
      { text: "Perform the live recovery test for the master recovery plan to ensure the Recovery Time Objective (RTO) is within the defined SLA.", value: "D" },
      { text: "Deploy the solution to production first and optimize based on live performance feedback from end users.", value: "E" }
    ],
    correct: ["A", "B"],
    type: "checkbox",
    multi: true
  },
  {
   text: "An architect is tasked with designing a new VMware Cloud Foundation (VCF) solution.<br>During workshops with the customer, the following requirements were captured:<br>• REQ01: The solution must provide a self service catalog.<br>• REQ02: The solution must support the segregation of the Development and Production resources (networks, virtual machines, users).<br>When documenting the design decisions, which statement should the architect include in order to help meet these requirements? [cite: 1080-1083]",
    options: [
      { text: "VCF Automation will be configured with separate service catalog instances for Development and Production.", value: "A" },
      { text: "VCF Automation will be configured with separate organizations for Development and Production.", value: "B" },
      { text: "Separate workload domains must be configured to provide segregation between the Development and Production environments.", value: "C" },
      { text: "VCF Automation does not support the use of multiple Active Directory domains.", value: "D" }
    ],
    correct: "B",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is designing a private cloud infrastructure for two departments (HR and Finance) based on VMware Cloud Foundation (VCF) and has been given the following requirements:<br>• HR and Finance superusers require access to VCF Operations.<br>• VCF Operations access, monitoring, and logging information must not be shared across departments.<br>Which design decision would meet the requirement? [cite: 1109-1110]",
    options: [
      { text: "Deploy two VCF Fleet instances within the private cloud, one for HR and one for Finance.", value: "A" },
      { text: "Configure two tenant instance within VCF Operations, one for HR and one for Finance.", value: "B" },
      { text: "Deploy two VCF Operations instances within a VCF Fleet, one for HR and one for Finance.", value: "C" },
      { text: "Configure two sets of scopes and index partitions within VCF Operations, one for HR and one for Finance.", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
   text: "Which statement defines the purpose of Technical Requirements? [cite: 1143]",
    options: [
      { text: "They define which goals and objectives can be achieved.", value: "A" },
      { text: "They define how the goals and objectives can be achieved.", value: "B" },
      { text: "They define what goals and objectives need to be achieved.", value: "C" },
      { text: "They define which audience need to be involved.", value: "D" }
    ],
    correct: "B",
    type: "radio",
    multi: false
  },
  {
    text: "An architect is designing the network model for a new VMware Cloud Foundation (VCF) solution.<br>During the requirements gathering phase, the customer stated that the VCF solution must comply with the organization's security policy for traffic separation.<br>The customer provided the architect with the following information from the policy:<br>• The physical network architecture is divided into multiple security zones.<br>• Traffic is not permitted to traverse between the zones with the exception of pre-approved monitoring tools.<br>• Physical servers may not may connected to multiple zones via a single network interface.<br>• Management and Storage traffic must be kept within network zone 1.<br>• Workload traffic must be kept within network zone 2.<br>The architect makes a design decision to use two vSphere Distributed Switches per cluster for both the Management and VI Workload domains.<br>Which two additional design decisions should the architect include in the virtual networking design for the separation of traffic between the vSphere Distributed Switches? (Choose two.)[cite: 1174-1180]",
    options: [
      { text: "Configure one vSphere Distributed Switch for ESX Management, Storage and vMotion traffic.", value: "A" },
      { text: "Configure one vSphere Distributed Switch for all workload traffic and all NSX - Host and Edge TEP/Edge Uplinks.", value: "B" },
      { text: "Configure one vSphere Distributed Switch for ESX Management, Storage, vMotion traffic and NSX - Host and Edge TEP/Edge Uplinks.", value: "C" },
      { text: "Configure one vSphere Distributed Switch for all NSX - Host and Edge TEP/Edge Uplinks.", value: "D" },
      { text: "Configure one vSphere Distributed Switch for all storage traffic.", value: "E" }
    ],
    correct: ["A", "B"],
    type: "checkbox",
    multi: true
  },
  {
    text: "The architect documented a requirement for 99.95% high availability to meet the customer's resiliency needs.<br>Which two physical design decisions will help meet this requirement in the management domain? (Choose two.)[cite: 1205-1206]",
    options: [
      { text: "Configure vCenter HA for the management domain vCenter server.", value: "A" },
      { text: "Advanced Cluster Setting: das.iostatsinterval = 0", value: "B" },
      { text: "Set the restart priority policy for the vCenter Server appliance to high.", value: "C" },
      { text: "ESX Host Uplink Setting: EtherChannel = Enable", value: "D" },
      { text: "ESX Host Uplink Setting: EtherChannel = Disable", value: "E" }
    ],
    correct: ["A", "C"],
    type: "checkbox",
    multi: true
  },
  {
    text: "An architect is designing for a VMware Cloud Foundation (VCF) Instance. The following requirements and constraints were documented.<br>• The management domain cluster utilizes vSAN stretched as the principal storage.<br>• Company policy states that compute and storage capacity utilization must not exceed 90% at all times.<br>Which three statements should the architect consider when designing the solution to satisfy the requirements? (Choose three.)[cite: 1240-1243]",
    options: [
      { text: "Use a heterogenous cluster configuration.", value: "A" },
      { text: "Size and monitor the cluster for a maximum compute peak utilization of < 45%.", value: "B" },
      { text: "Size and monitor the cluster for a maximum storage utilization of 90%.", value: "C" },
      { text: "Size and monitor the cluster for a maximum compute peak utilization of < 90%.", value: "D" },
      { text: "Size and monitor the cluster for a maximum storage utilization of 40%.", value: "E" },
      { text: "Use a homogenous cluster configuration.", value: "F" }
    ],
    correct: ["B", "E", "F"],
    type: "checkbox",
    multi: true
  },
  {
   text: "A cloud architect is designing a VMware Cloud Foundation (VCF) Automation solution for an organization.<br>The design must fulfill the following requirements:<br>• The design must minimize provider infrastructure lifecycle tasks.<br>• The design must minimize infrastructure management overhead.<br>• Each tenant must have isolated compute infrastructure.<br>Which of the following deployment models best meets these requirements? [cite: 1281-1284]",
    options: [
      { text: "Dedicated VCF instances per tenant in a Standard Architecture", value: "A" },
      { text: "Single VCF instance with dedicated Workload Domains per tenant", value: "B" },
      { text: "Consolidated VCF deployment per tenant", value: "C" },
      { text: "Shared Workload Domain for tenants", value: "D" }
    ],
    correct: "B",
    type: "radio",
    multi: false
  },
  {
    text: "During an initial design workshop with stakeholders, an Architect was provided with an overview of the current state and other information required to proceed to the design phase:<br>• Business requirements indicated support for operations of a different business unit.<br>• A multi-tenancy statement should be documented.<br>As a result, the Architect makes the decision to enable multi-tenancy within VCF Automation.<br>A combination of which two design implications would also need to be documented? (Choose two.)[cite: 1298-1300]",
    options: [
      { text: "All Tenants must use a single VCF Automation Orchestrator instance.", value: "A" },
      { text: "The Provider Tenant must use the embedded VCF Orchestrator instance.", value: "B" },
      { text: "The Provider Tenant must use an external VCF Orchestrator instance.", value: "C" },
      { text: "Each Tenant must use an Embedded VCF Automation Orchestrator instance.", value: "D" },
      { text: "Each Tenant must use an External VCF Automation Orchestrator instance.", value: "E" }
    ],
    correct: ["C", "E"],
    type: "checkbox",
    multi: true
  },
  {
   text: "During an initial design workshop with stakeholders, an Architect was provided with an overview of the current state and other information required to proceed to the design phase.<br>Which statement should be documented as a requirement? [cite: 1352-1353]",
    options: [
      { text: "Existing storage arrays provide sufficient capacity for building the environment.", value: "A" },
      { text: "The customer network team is not trained to support NSX VPC.", value: "B" },
      { text: "Existing shared storage array must be used.", value: "C" },
      { text: "Block-based storage must be used within a workload domain.", value: "D" }
    ],
    correct: "D",
    type: "radio",
    multi: false
  },
  {
   text: "During an initial design workshop with stakeholders, the architect was provided with an overview of the current state and other information required to proceed to the design phase.<br>The architect has assumed that the solution will need to support high availability for workloads.<br>Given the assumption, which statement should the architect document as a risk? [cite: 1424-1426]",
    options: [
      { text: "The entire infrastructure is hosted on a single physical site.", value: "A" },
      { text: "The solution supports the separation of management components from production workloads.", value: "B" },
      { text: "The solution supports a recovery point objective (RPO) of 24 hours for infrastructure components.", value: "C" },
      { text: "BGP is the dynamic routing protocol on the physical fabric and cannot be changed.", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
   text: "During a design workshop, the cloud architect captured the following constraint and requirement:<br>• CON-00l: The customer's existing stretched cluster model will be used.<br>• REQ-001: The design must minimize management infrastructure downtime.<br>Which Supervisor deployment model supports the design constraint and requirement? [cite: 1453-1454]",
    options: [
      { text: "Three Management Zone Supervisor deployment with High Availability control plane", value: "A" },
      { text: "Single Management Zone Supervisor deployment with High Availability control plane", value: "B" },
      { text: "Single Management Zone Supervisor deployment with Simple Availability control plane", value: "C" },
      { text: "Three Management Zone deployment with Simple Availability control plane", value: "D" }
    ],
    correct: "B",
    type: "radio",
    multi: false
  },
  {
   text: "As part of an initial stakeholder meeting, one of the stakeholders has stated the following:<br>\"According to the hardware standards, all new host server hardware must be deployed using our selected hardware vendor and server model.\"<br>How would the architect classify this statement? [cite: 1477-1478]",
    options: [
      { text: "A risk", value: "A" },
      { text: "A requirement", value: "B" },
      { text: "A constraint", value: "C" },
      { text: "An assumption", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
   text: "A large financial institution is designing a VMware Cloud Foundation (VCF) solution.<br>During the initial discovery meetings, the customer detailed the following requirements:<br>• Management of the physical network environment is handled by an outsourced team.<br>• The VMware Administration team cannot re-configure the physical network.<br>• All hosts must use Link Aggregation.<br>• The storage environment is disaggregated.<br>• NFS will be used as principal storage.<br>The customer provided the bill-of-materials for the physical servers that are being purchased.<br>Each server will have four 25 GbE physical NICs, with two connected to the network fabric for Management, vMotion, and virtual machine traffic.<br>The other two NICs will be connected to the storage fabric hosting the NFS server.<br>How does the information provided impact the overall design? [cite: 1495-1500]",
    options: [
      { text: "Link Aggregation cannot be used in the Workload Domain.", value: "A" },
      { text: "NIC teaming for Virtual Standard Switch (vSS) must be configured.", value: "B" },
      { text: "Multiple Link Aggregation Groups are not supported.", value: "C" },
      { text: "Link Aggregation cannot be used in the Management Domain.", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is responsible for designing a new VMware Cloud Foundation (VCF)-based Private Cloud solution.<br>During the requirements gathering workshop with key customer stakeholders, the following information was captured:<br>• The solution must support running 50,000 workloads concurrently across all sites.<br>• The solution must support the concurrent deployment of up to 10 workloads.<br>When creating the design document, which design quality should be used to classify the stated requirements? [cite: 1523-1526]",
    options: [
      { text: "Performance", value: "A" },
      { text: "Availability", value: "B" },
      { text: "Recoverability", value: "C" },
      { text: "Manageability", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
   text: "During the design workshop, the customer stated the following requirement:<br>\"The solution will support secure communication.\"<br>Which design decision should be included in the logical design for the workload domain? [cite: 1572-1573]",
    options: [
      { text: "Set promiscuous mode port group security policy to reject.", value: "A" },
      { text: "Ensure the host servers have TPM 2.0 hardware.", value: "B" },
      { text: "Verify all physical components used for the deployments are on the hardware compatibility list.", value: "C" },
      { text: "Use a SHA-2 algorithm or higher for signed certificates.", value: "D" }
    ],
    correct: "D",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is designing a VMware Cloud Foundation (VCF) solution.<br>The following information has been provided by the customer:<br>• Due to budget constraints, the solution must utilize the existing server hardware.<br>• The existing server hardware consists of server models from the same vendor but different generations.<br>• There are four servers available for use in this solution.<br>What design decision should the architect make for the lifecycle management of the solution based on this information? [cite: 1597-1601]",
    options: [
      { text: "Use vSphere Lifecycle Manager baselines for the management domain cluster.", value: "A" },
      { text: "Use a single vSphere Lifecycle Manager composite image for the management and workload domain clusters.", value: "B" },
      { text: "Use separate vSphere Lifecycle Manager images for the management and workload domain clusters.", value: "C" },
      { text: "Use a single vSphere Lifecycle Manager composite image for the management domain cluster.", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
   text: "As a part of designing the VMware Cloud Foundation (VCF) Operations deployment, the architect must ensure that VCF Operations is capable of monitoring the customer's infrastructure made up of a central datacenter and multiple remote sites in different countries.<br>During a design workshop, the following requirements were identified:<br>REQ-001: Corporate IT users must be able to review performance, alerts, and capacity details from a single management point.<br>REQ-002: The monitoring solution must support local data collection at remote sites to prevent data loss from unstable WAN connections.<br>REQ-003: The monitoring solution must comply with local data sovereignty regulations.<br>Which deployment model fulfills all design requirements? [cite: 1700-1703]",
    options: [
      { text: "A single fleet with multiple VCF instances.", value: "A" },
      { text: "All remote sites will be a single VCF fleet.", value: "B" },
      { text: "Single VCF fleet with Cloud Proxies in each remote site.", value: "C" },
      { text: "Each remote site will be it's own VCF fleet.", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is documenting the design for a new VMware Cloud Foundation (VCF) solution and makes the following design decision:<br>Two vSphere clusters will be deployed within the single VI workload domain.<br>What statement should the architect include as an implication of this design decision? [cite: 1732-1733]",
    options: [
      { text: "Deploying multiple clusters within the single VI workload domain meets the requirement to segregate Production and Development workloads.", value: "A" },
      { text: "All clusters within the single VI workload domain must use vSAN as their principal storage type.", value: "B" },
      { text: "If the solution needs to be scaled at a future date, additional VI workload domains can be deployed.", value: "C" },
      { text: "Deploying multiple clusters in the single VI workload domain reduces the number of vCenter Server instances that must be managed.", value: "D" }
    ],
    correct: "D",
    type: "radio",
    multi: false
  },
  {
   text: "An architect has compiled a list of design choices following a design workshop with the business stakeholders.<br>Which statement represents a logical design decision? [cite: 1773-1774]",
    options: [
      { text: "Synchronous data replication will be used to meet the stated Recovery Point Objective (RPO) between site A and B.", value: "A" },
      { text: "Users must connect to the application servers via a shared Global Load Balancer.", value: "B" },
      { text: "Sites A and B will each have a /16 subnet for their networks.", value: "C" },
      { text: "Users must experience application availability in under 2 seconds.", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is working on a VMware Cloud Foundation (VCF) architecture design and identified the following requirements:<br>• The organization is using a third-party virtual appliance that does not support overlay networks.<br>• The virtual appliance must reside on the same L2 domain as an external physical firewall.<br>• The virtual appliance also needs access to workloads that are currently hosted on overlay segments provided by NSX.<br>Which design decision should the architect make to meet these requirements? [cite: 1802-1805]",
    options: [
      { text: "Place the virtual appliance and all workloads on VLAN-backed segments.", value: "A" },
      { text: "Connect the virtual appliance to a VLAN-backed segment and configure NSX bridging to allow access to overlay segments.", value: "B" },
      { text: "Request the third-party vendor to certify the virtual appliance for NSX Overlay segments.", value: "C" },
      { text: "Connect the virtual appliance to an overlay-backed segment and use static routes to the firewall.", value: "D" }
    ],
    correct: "B",
    type: "radio",
    multi: false
  },
  {
   text: "Why would an architect specify the default NSX segment profiles in a VMware Cloud Foundation (VCF) design? [cite: 1837]",
    options: [
      { text: "Default segment profiles provide sufficient security and operational baseline settings for most common workloads and simplify lifecycle management.", value: "A" },
      { text: "Default segment profiles offer enhanced performance and are automatically optimized for overlay traffic.", value: "B" },
      { text: "Default segment profiles enable distributed firewall policy enforcement and avoid the need for overlay segments.", value: "C" },
      { text: "Default segment profiles are required for VLAN-backed segments and cannot be overridden.", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
   text: "During a requirements gathering workshop, several business and technical requirements were captured from the customer.<br>Which requirement will be classified as a Business Requirement? [cite: 1857-1858]",
    options: [
      { text: "The solution must provide a component-level SLA of 99.9% or higher.", value: "A" },
      { text: "The solution must provide the best end-user experience.", value: "B" },
      { text: "The solution must allow the migration of legacy server infrastructure.", value: "C" },
      { text: "The solution must consider security and resiliency to ensure business continuity.", value: "D" }
    ],
    correct: "B",
    type: "radio",
    multi: false
  },
  {
    text: "An architect is responsible for designing a VMware Cloud Foundation (VCF) Private Cloud.<br>During a requirements gathering workshop with key customer stakeholders, the following information was captured:<br>• The service catalog solution must meet a minimum availability SLA of 99.9%.<br>• The performance of the service catalog solution must not be impacted by maintenance activities or a single physical ESX host failure.<br>During the logical design phase of the project, the following design decisions were made:<br>• The solution will deploy VCF Automation using the highly available deployment model.<br>Which two corresponding physical design decisions should the architect make to meet the stated requirements? (Choose two.)[cite: 1897-1901]",
    options: [
      { text: "The solution will deploy three VCF Automation appliances using the small size.", value: "A" },
      { text: "The solution will configure the external load balancer to send all traffic to the native Kubernetes load balancer.", value: "B" },
      { text: "The solution will create a VM-host affinity rule to ensure all nodes of the VCF Automation cluster are located on the same ESX host.", value: "C" },
      { text: "The solution will deploy an external load balancer to replace the native load balancer.", value: "D" },
      { text: "The solution will create a VM-host anti-affinity rule to ensure all nodes of the VCF Automation cluster are located on different ESX hosts.", value: "E" }
    ],
    correct: ["B", "E"],
    type: "checkbox",
    multi: true
  },
  {
   text: "A customer has a new initiative to build a private cloud based on VMware Cloud Foundation (VCF).<br>The customer technical team is presenting an overview of the current state of the infrastructure as well as describing what the expectations are for the private cloud.<br>Based on the notes captured by the architect, which statement should be documented as a constraint? [cite: 1946-1948]",
    options: [
      { text: "The design must address security zone requirements for management, production, dev/test, and QA workloads.", value: "A" },
      { text: "The existing storage is out of hardware vendor maintenance.", value: "B" },
      { text: "No funding exists for a new storage array. Therefore, existing storage hardware must be used.", value: "C" },
      { text: "The design must provide a centralized management console to manage both data centers.", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is drafting a design document in preparation for the deployment of a new VMware Cloud Foundation (VCF) solution.<br>To minimize costs, the customer has asked that the VCF solution utilize existing the vSphere infrastructure.<br>The customer has migrated all virtual machines off this infrastructure in preparation for the deployment of VCF.<br>The following information has been provided about the existing vSphere infrastructure:<br>• There are three separate vSphere clusters, each consisting of five hosts.<br>• All networking is vSphere based, with a vSphere Distributed Switch (vDS) configured per vSphere cluster.<br>• All clusters use NFSv3 for shared storage.<br>• A single vCenter manages the three vSphere clusters.<br>Based on this information, the architect makes a decision to create a new VCF fleet with a single VCF instance.<br>What design implication should the architect document for this decision? [cite: 1970-1977]",
    options: [
      { text: "NSX will be automatically deployed during the creation of the VCF fleet.", value: "A" },
      { text: "The ESX hosts will be converted to use vSphere Lifecycle Manager baselines during the creation of the VCF fleet.", value: "B" },
      { text: "The vCenter VM must be migrated to a standalone host before the creation of the VCF fleet.", value: "C" },
      { text: "The clusters will be automatically configured to use vSAN storage before the creation of the VCF fleet.", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is designing a VMware Cloud Foundation (VCF) deployment to meet the following design requirements:<br>• Tenants need dedicated external network access.<br>• The number of NSX Edge clusters should be minimized.<br>To fulfill these requirements, the architect made a design decision to use a Workload Networking VPC with Full Services Model.<br>Which additional design decision should be considered by the architect as part of the logical network design to fulfill these requirements? [cite: 2010-2013]",
    options: [
      { text: "Use NSX Federation providing a dedicated NSX instance for each tenant.", value: "A" },
      { text: "Deploy the maximum number of 10 NSX Edges into a single Edge cluster.", value: "B" },
      { text: "Use Virtual Routing and Forwarding (VRF) lite to create a separate VRF T0 Gateway for each tenant.", value: "C" },
      { text: "Install two NSX bare metal Edges with multiple physical interfaces to separate tenants.", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is responsible for designing a new VMware Cloud Foundation (VCF)-based Private Cloud solution.<br>During the requirements gathering workshop with key customer stakeholders, the following information was captured:<br>• The solution must support a yearly workload growth of up to 10%.<br>When creating the design document, which design quality should be used to classify the stated requirements? [cite: 2032-2034]",
    options: [
      { text: "Performance", value: "A" },
      { text: "Manageability", value: "B" },
      { text: "Security", value: "C" },
      { text: "Availability", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
   text: "A customer is deploying VMware Cloud Foundation (VCF) in an enterprise environment.<br>During a series of workshops with stakeholders, the following requirements were identified:<br>• The network solution must be capable of complete logical isolation.<br>• The network solution must be capable of supporting independent upgrade cycles for network stacks.<br>• The network solution must be capable of tenant-specific customization of NSX configurations.<br>The architect has made the following design decisions:<br>• The solution will consist of a single VCF instance.<br>• The solution will include a management domain and two workload domains.<br>Based on the scenario, which additional design decision meets all of the stated requirements? [cite: 2049-2055]",
    options: [
      { text: "Deploy NSX only in the management domain and use VLAN-backed segments in the workload domains.", value: "A" },
      { text: "Deploy a dedicated NSX instance per workload domain.", value: "B" },
      { text: "Use a shared NSX instance across both workload domains.", value: "C" },
      { text: "Use a global NSX Federation configuration across workload domains.", value: "D" }
    ],
    correct: "B",
    type: "radio",
    multi: false
  },
  {
    text: "An architect is responsible for the design of a new VMware Cloud Foundation (VCF)-based private cloud solution.<br>During a requirements gathering workshop, key stakeholders provided the following requirement:<br>• The solution must identify any configuration changes made to the Management Infrastructure every 30 days.<br>Which three design decisions should the architect make to meet the stated requirements? (Choose three.)[cite: 2079-2081]",
    options: [
      { text: "Schedule Configuration Drift to Check the configuration every 30 days.", value: "A" },
      { text: "Configure a Configuration Template for the Management Cluster.", value: "B" },
      { text: "Schedule Configuration Drift to Remediate the configuration every 30 days.", value: "C" },
      { text: "Create a Configuration Template for the Management NSX Manager.", value: "D" },
      { text: "Configure a Configuration Template for the Management vCenter.", value: "E" },
      { text: "Configure Host Profiles for the Workload Domain.", value: "F" }
    ],
    correct: ["A", "B", "E"],
    type: "checkbox",
    multi: true
  },
  {
    text: "During the design workshop, the customer stated the following requirement:<br>• The solution must comply with the organization’s security standards.<br>Which two design decisions should be included in the logical design for the workload domain? (Choose two.)[cite: 2101-2102]",
    options: [
      { text: "Use an SHA-2 algorithm or higher when signing certificates.", value: "A" },
      { text: "Enable Inter-SR iBGP routing.", value: "B" },
      { text: "Use large-size NSX Edge virtual appliances to account for the additional firewall rules.", value: "C" },
      { text: "Enable VM Monitoring for each workload within the cluster.", value: "D" },
      { text: "Establish an operations practice to capture and update the thumbprint of the NSX Local Manager certificate on the NSX Global Manager every time the certificate is updated.", value: "E" }
    ],
    correct: ["A", "E"],
    type: "checkbox",
    multi: true
  },
  {
   text: "During a design workshop, the security team provides the following requirement for the VMware Cloud Foundation (VCF) Automation deployment:<br>• All Virtual Machine images must be reviewed and vetted by the security team prior to consumption.<br>Which Content Library type supports the requirement? [cite: 2119-2120]",
    options: [
      { text: "Local Content Library", value: "A" },
      { text: "Tenant-managed Content Library", value: "B" },
      { text: "Subscribed Content Library", value: "C" },
      { text: "Provider-managed Content Library", value: "D" }
    ],
    correct: "D",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is designing for a greenfield VMware Cloud Foundation (VCF) solution.<br>This would be the first VCF Fleet in the VCF solution, and the customer would like to start with a minimal footprint with the option to scale up and out later.<br>Which VCF Operations deployment model should the architect choose? [cite: 2134-2136]",
    options: [
      { text: "Simple", value: "A" },
      { text: "High Availability", value: "B" },
      { text: "Standard", value: "C" },
      { text: "Advanced", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
   text: "As part of an initial stakeholder meeting, one of the stakeholders has stated the following:<br>• The initial design must be completed within the next 3 months so that hardware can be ordered within the current budget cycle.<br>How would the architect classify and record this statement? [cite: 2150-2151]",
    options: [
      { text: "An assumption", value: "A" },
      { text: "A risk", value: "B" },
      { text: "A requirement", value: "C" },
      { text: "A constraint", value: "D" }
    ],
    correct: "D",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is responsible for designing a new VMware Cloud Foundation (VCF)-based Private Cloud solution.<br>During the requirements gathering workshop with key customer stakeholders, the following information was captured:<br>• The solution must ensure all components meet a software version of N-1.<br>When creating the design document, which design quality should be used to classify the stated requirements? [cite: 2168-2171]",
    options: [
      { text: "Security", value: "A" },
      { text: "Availability", value: "B" },
      { text: "Manageability", value: "C" },
      { text: "Recoverability", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
    text: "Which two VCF components are replicated across availability zones in a VMware Cloud Foundation (VCF) Fleet with Disaster Recovery model design with two availability zones? (Choose two.)[cite: 2181-2182]",
    options: [
      { text: "SDDC Manager", value: "A" },
      { text: "VCF Operations", value: "B" },
      { text: "VCF Automation", value: "C" },
      { text: "vCenter", value: "D" },
      { text: "NSX", value: "E" }
    ],
    correct: ["D", "E"],
    type: "checkbox",
    multi: true
  },
  {
    text: "An architect has been tasked with designing a new VMware Cloud Foundation (VCF) solution.<br>During the requirements gathering workshops with the customer, the following requirements were captured:<br>• REQ01: The solution must support workloads being deployed to multiple physical datacenter locations (DC01, DC02).<br>• REQ02: The solution must support the use of the two factor authentication for authenticating user access to the administrative tools.<br>• REQ03: The solution must prioritize reducing the operational overhead associated with managing the deployed infrastructure platform.<br>A combination of which two design decisions should the architect document for the VCF Single Sign-On architecture in order to meet these requirements? (Choose two.)[cite: 2200-2204]",
    options: [
      { text: "Deploy VCF Identity Broker (VIDB) in the management domain of every VCF instance in all sites.", value: "A" },
      { text: "Configure all additional VCF instances in the same region to point to the VIDB in the first VCF instance at DC02.", value: "B" },
      { text: "Configure all additional VCF instances in the same private cloud to point to the VIDB in the first VCF instance at DC01.", value: "C" },
      { text: "Deploy VCF Identity Broker (VIDB) in the management domain of each VCF instance at DC02.", value: "D" },
      { text: "Deploy VCF Identity Broker (VIDB) in the first VCF instance management domain at DC01.", value: "E" }
    ],
    correct: ["C", "E"],
    type: "checkbox",
    multi: true
  },
  {
   text: "A VMware Cloud Foundation (VCF) architect is planning for the expansion of an existing VCF instance.<br>The existing VCF instance is deployed with a single workload domain.<br>The number of ESX hosts has grown to the maximum number the existing vCenter can support.<br>Which design decision would the architect need to make to allow the existing VCF Instance to add more ESX hosts? [cite: 2220-2223]",
    options: [
      { text: "Deploy a second VCF Instance within the existing VCF Fleet.", value: "A" },
      { text: "Deploy a second vCenter server appliance within the existing workload domain.", value: "B" },
      { text: "Deploy a second cluster within the existing vCenter.", value: "C" },
      { text: "Deploy a second workload domain within the existing VCF Instance.", value: "D" }
    ],
    correct: "D",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is responsible for designing a VMware Cloud Foundation (VCF)-based solution for a customer.<br>During a discovery workshop, the following requirements were stated by the customer:<br>• All applications/workloads designated as business critical have a Recovery Point Objective (RPO) of 1 business hour.<br>• The infrastructure components of the VCF solution must have a Recovery Time Objective (RTO) of 4 business hours.<br>In the context provided, what does the RTO determine? [cite: 2239-2242]",
    options: [
      { text: "The maximum tolerable amount of time allowed before an application/service should be recovered to a useable state", value: "A" },
      { text: "The minimum tolerable amount of time allowed before an application/service should be recovered to a useable state", value: "B" },
      { text: "The maximum amount of data loss that can be tolerated", value: "C" },
      { text: "The minimum amount of data loss that can be tolerated", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is designing a VMware Cloud Foundation (VCF) fleet.<br>The following information has been provided by the customer:<br>• Due to budget constraints, the solution must utilize the existing server hardware.<br>• The existing server hardware consists of server models from the same vendor but different generations.<br>• There are ten servers available for use in this solution.<br>• Management and Business workloads should be hosted in different clusters.<br>What design decision should the architect make for the lifecycle management of the solution based on this information? [cite: 2250-2255]",
    options: [
      { text: "Use a single vSphere Lifecycle Manager composite image for the management and workload domain clusters.", value: "A" },
      { text: "Use vSphere Lifecycle Manager baselines for the management domain cluster.", value: "B" },
      { text: "Use separate vSphere Lifecycle Manager composite images for the management and workload domain clusters.", value: "C" },
      { text: "Use a single vSphere Lifecycle Manager composite image for the management domain cluster.", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
    text: "An architect has been tasked with designing a new VMware Cloud Foundation (VCF) solution.<br>The following design decisions were documented after requirements gathering workshops with the customer:<br>• Deploy a VCF Fleet into each of the DC1 and DC2 datacenters.<br>• Deploy two VCF instances (VCF1 and VCF2) into each VCF Fleet.<br>• Use the existing, supported third-party solution to provide Multifactor Authentication (MFA) for users accessing the VCF components.<br>The architect also documented the following information from the workshops:<br>• The customer wants to minimize the risk of a single operational task performed by an administrator impacting multiple components.<br>• The customer wants to avoid single points of failure by using high availability architectures.<br>Which two design decisions should the architect include for the authentication approach based on the information provided? (Choose two.)[cite: 2271-2277]",
    options: [
      { text: "Deploy a shared VCF Identity Broker for all VCF instances within a VCF Fleet.", value: "A" },
      { text: "Deploy a shared VCF Identity Broker for all VCF instances across all VCF Fleets.", value: "B" },
      { text: "Use the external VCF Identity Broker model.", value: "C" },
      { text: "Use the embedded VCF Identity Broker model.", value: "D" },
      { text: "Deploy a dedicated VCF Identity Broker for each VCF instance within a VCF Fleet.", value: "E" }
    ],
    correct: ["C", "E"],
    type: "checkbox",
    multi: true
  },
  {
   text: "A large financial institution is designing a VMware Cloud Foundation (VCF) solution.<br>During the initial discovery meetings, the customer detailed the following requirements:<br>• Management of the physical network environment is handled by an outsourced team.<br>• The VMware Administration team cannot re-configure the physical network.<br>• The environment is configured to use Link Aggregation.<br>How does the information provided impact the overall design? [cite: 2306-2309]",
    options: [
      { text: "NIC teaming for Virtual Standard Switch (vSS) must be configured.", value: "A" },
      { text: "LACP failback must be configured.", value: "B" },
      { text: "Link Aggregation cannot be used in the Management Domain.", value: "C" },
      { text: "Link Aggregation cannot be used for Workload Domains.", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
   text: "Which statement would the architect document as a design decision within the logical design? [cite: 2339]",
    options: [
      { text: "vSphere High Availability (HA) will be enabled.", value: "A" },
      { text: "The VMware Distributed Resource Scheduler (DRS) latency sensitivity value will be set to high for the workload cluster.", value: "B" },
      { text: "Service Levels will align with the defined Business Impact Analysis findings.", value: "C" },
      { text: "The solution must provide the ability to patch an existing template.", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
    text: "An architect was in an architectural workshop and noted the following business objectives:<br>• The solution must prioritize optimal end-to-end user shopping experience for customers accessing the web site.<br>• The web site must be available 24 x 7 x 365.<br>Which three conceptual model items relate to these business objectives? (Choose three.)[cite: 2376-2377]",
    options: [
      { text: "A constraint of any planned changes limited to outside of business hours only", value: "A" },
      { text: "A risk that the external internet network provider does not meet the service level agreement (SLA) requirements", value: "B" },
      { text: "An assumption that there is sufficient budget for the design to meet the performance requirements", value: "C" },
      { text: "A requirement to have 99.99% availability uptime measured at the front-end application layer", value: "D" },
      { text: "An assumption that site performance is not a key performance indicator (KPI) for the customer", value: "E" },
      { text: "A requirement to have 99.99% availability uptime measured at the network infrastructure layer", value: "F" }
    ],
    correct: ["B", "C", "D"],
    type: "checkbox",
    multi: true
  },
  {
   text: "Which design defines how to arrange and use components and features of the infrastructure to satisfy service dependencies and other relationships specified in the Conceptual Model? [cite: 2401]",
    options: [
      { text: "Physical Design", value: "A" },
      { text: "Configuration Guide", value: "B" },
      { text: "High Availability Design", value: "C" },
      { text: "Logical Design", value: "D" }
    ],
    correct: "D",
    type: "radio",
    multi: false
  },
  {
   text: "An architect had been given a constraint to use an existing storage array to support the virtual infrastructure design project.<br>The architect documents the following:<br>• Assumption01: The existing storage array has sufficient capacity and performance to support the intended virtual infrastructure workloads.<br>• Risk01: There is a risk that the performance and capacity of the existing storage array may not be sufficient for the solution.<br>How would the architect mitigate the risk? [cite: 2410-2412]",
    options: [
      { text: "Ensure that the customer allocates budget for new hardware in case the risk is realized.", value: "A" },
      { text: "Setup a RAID mirror configuration on the existing storage array for redundancy.", value: "B" },
      { text: "Request for additional budget to purchase more fibre channel switches.", value: "C" },
      { text: "Ignore the constraint and design the solution using VMware VSAN Express Storage Architecture (ESA).", value: "D" }
    ],
    correct: "A",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is designing a new VMware Cloud Foundation (VCF) solution.<br>They are meeting with the key stakeholders and subject matter experts (SMEs) for the first time as part of the requirements gathering process.<br>The following information has been shared with the architect prior to the meeting:<br>• Names and job titles of the attendees<br>• Project timelines and budget<br>What step should the architect perform as part of this initial requirements gathering workshop? [cite: 2428-2430]",
    options: [
      { text: "Ask questions to agree on the key product features the SMEs want from the design.", value: "A" },
      { text: "Ask questions to start a discussion on the business objectives and desired outcomes.", value: "B" },
      { text: "Open the meeting with a list of the VCF design decisions from the public documentation to agree on any required changes.", value: "C" },
      { text: "Open the meeting with a diagram of the VCF topology that must meet the customer requirements in order to start a discussion.", value: "D" }
    ],
    correct: "B",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is responsible for designing a new VMware Cloud Foundation (VCF)-based Private Cloud solution.<br>During the requirements gathering workshop with key customer stakeholders, the following information was captured:<br>• The solution must ensure all management components are redundant at the component level.<br>When creating the design document, which design quality should be used to classify the stated requirements? [cite: 2446-2448]",
    options: [
      { text: "Recoverability", value: "A" },
      { text: "Performance", value: "B" },
      { text: "Availability", value: "C" },
      { text: "Manageability", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
    text: "As part of the VMware Cloud Foundation (VCF) logical design, the architect documented the following requirement:<br>• The solution must be able to support latency-sensitive workloads.<br>Which two physical design decisions will meet this performance requirement in the workload domain? (Choose two.)[cite: 2456-2457]",
    options: [
      { text: "vSAN Deep Snapshots: Enabled", value: "A" },
      { text: "vSAN Global Deduplication: Enabled", value: "B" },
      { text: "Advanced Memory Tiering with NVMe: Enabled", value: "C" },
      { text: "NSX Enhanced Data Path: Enabled", value: "D" },
      { text: "Intel TDX and AMD’s SEV-SNP integration", value: "E" }
    ],
    correct: ["C", "D"],
    type: "checkbox",
    multi: true
  },
  {
   text: "As part of a design for a VMware Cloud Foundation (VCF) solution, an architect has documented the following dependencies and constraints:<br>• CONS001 - Internet access will not be permitted from anywhere within the VCF solution.<br>• CONS002 - The password must not be stored in plain text anywhere within the VCF solution.<br>• DEP001 - The customer must make the required VCF binaries accessible to the VCF Installer appliance during the deployment phase.<br>Which design decision should the architect include in the design for the download of the VCF binaries? [cite: 2481-2484]",
    options: [
      { text: "The Bundle Transfer Utility will be used on the VCF Installer appliance.", value: "A" },
      { text: "The VCF Installer appliance will be configured to connect to an online depot.", value: "B" },
      { text: "The VCF Installer appliance will be configured to connect to an offline depot.", value: "C" },
      { text: "The VCF Download Tool will be used on the VCF Installer appliance.", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
   text: "During a requirements gathering workshop, the customer has provided a list of business and technical requirements.<br>Which requirement should be classified as a business requirement? [cite: 2502]",
    options: [
      { text: "The solution needs to grow by 30% over the next three years.", value: "A" },
      { text: "The solution must consider security and resiliency to ensure continuity.", value: "B" },
      { text: "The solution should reduce operational costs.", value: "C" },
      { text: "The solution must provide no Single Point of Failure (SPOF).", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
   text: "An architect is responsible for designing a VMware Cloud Foundation (VCF)-based private cloud for a customer.<br>During the customer requirements gathering workshop, the customer has stated the following:<br>• All Platinum application/services must have an availability SLA of 99.99%.<br>• All Gold application/services must have an availability SLA of 99.9%.<br>• All Silver application/services must have an availability SLA of 99%.<br>• The private cloud must have an availability SLA of 99.9%.<br>What should the architect recommend to meet the stated requirements? [cite: 2516-2521]",
    options: [
      { text: "The private cloud SLA can only be met using multiple VMware Cloud Foundation instances configured as a single VCF Fleet.", value: "A" },
      { text: "The platinum service availability requirements must be met by configuring Proactive High Availability (HA) on the workload domain.", value: "B" },
      { text: "The platinum service availability requirements must be met by the application.", value: "C" },
      { text: "The private cloud must only be used to host Silver and Gold services.", value: "D" }
    ],
    correct: "C",
    type: "radio",
    multi: false
  },
  {
    text: "A customer is designing a multi-site VMware Cloud Foundation (VCF) and vSAN Data Protection (DP) architecture to ensure business continuity.<br>The customer’s support team must validate the failover and recovery processes before being allowed to deploy into production.<br>Which two validation activities should be included in the strategy to meet the objective? (Choose two.)[cite: 2539-2541]",
    options: [
      { text: "Conduct recovery plan testing annually, as frequent testing may introduce instability in DR environments.", value: "A" },
      { text: "Perform planned and unplanned failover tests in a controlled environment to validate recovery time objectives.", value: "B" },
      { text: "Configure recovery plans based on generic VMware best practices rather than workload-specific requirements to decrease the architecture complexity.", value: "C" },
      { text: "Configure vSphere HA and DRS features to manage disaster recovery automatically, eliminating the need for additional validation.", value: "D" },
      { text: "Assess the impact of failover scenarios on application dependencies and inter-site connectivity.", value: "E" }
    ],
    correct: ["B", "E"],
    type: "checkbox",
    multi: true
  }
];

// Export for use in quiz
// If using in Node.js: module.exports = { questionBank };