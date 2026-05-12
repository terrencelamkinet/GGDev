const ngfwQuestions = [
  {
    "num": 1,
    "text": "To maintain security efficacy of its public cloud resources by using native tools, a company purchases Cloud NGFW credits to replicate the\nPanorama, PA-Series, and VM-Series devices used in physical data centers. Resources exist on AWS and Azure:\nThe AWS deployment is architected with AWS Transit Gateway, to which all resources connect\nThe Azure deployment is architected with each application independently routing traffic\nThe engineer deploying Cloud NGFW in these two cloud environments must account for the following:\nMinimize changes to the two cloud environments\nScale to the demands of the applications while using the least amount of compute resources\nAllow the company to unify the Security policies across all protected areas\nWhich two implementations will meet these requirements? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "Deploy a VM-Series firewall in AWS in each VPC, create an IPSec tunnel between AWS and Azure, and manage the policy with Panorama."
      },
      {
        "letter": "B",
        "text": "Deploy Cloud NGFW for Azure in vNET/s, update the vNET/s routing to path traffic through the deployed NGFWs, and manage the policy with Panorama."
      },
      {
        "letter": "C",
        "text": "Deploy Cloud NGFW for Azure in vWAN, create a vWAN to route all appropriate traffic to the Cloud NGFW attached to the vWAN, and manage the policy with local rules."
      },
      {
        "letter": "D",
        "text": "Deploy Cloud NGFW for AWS in a centralized Security VPC, update the Transit Gateway to route all appropriate traffic through the Security VPC, and manage the policy with Panorama."
      }
    ],
    "answer": "BD",
    "type": "multi"
  },
  {
    "num": 2,
    "text": "During an upgrade to the routing infrastructure in a customer environment, the network administrator wants to implement Advanced Routing\nEngine (ARE) on a Palo Alto Networks firewall.\nWhich firewall models support this configuration?",
    "choices": [
      {
        "letter": "A",
        "text": "PA-5280, PA-7080, PA-3250, VM-Series"
      },
      {
        "letter": "B",
        "text": "PA-455, VM-Series, PA-1410, PA-5450"
      },
      {
        "letter": "C",
        "text": "PA-3260, PA-5410, PA-850, PA-460"
      },
      {
        "letter": "D",
        "text": "PA-7050, PA-1420, VM-Series, CN-Series"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 3,
    "text": "Which two statements apply to configuring required security rules when setting up an IPSec tunnel between a Palo Alto Networks firewall and a\nthird- party gateway? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "For incoming and outgoing traffic through the tunnel, creating separate rules for each direction is optional."
      },
      {
        "letter": "B",
        "text": "The IKE negotiation and IPSec/ESP packets are allowed by default via the intrazone default allow policy."
      },
      {
        "letter": "C",
        "text": "For incoming and outgoing traffic through the tunnel, separate rules must be created for each direction."
      },
      {
        "letter": "D",
        "text": "The IKE negotiation and IPSec/ESP packets are denied by default via the interzone default deny policy."
      }
    ],
    "answer": "AB",
    "type": "multi"
  },
  {
    "num": 4,
    "text": "Which statement describes the role of Terraform in deploying Palo Alto Networks NGFWs?",
    "choices": [
      {
        "letter": "A",
        "text": "It acts as a logging service for NGFW performance metrics."
      },
      {
        "letter": "B",
        "text": "It orchestrates real-time traffic inspection for network segments."
      },
      {
        "letter": "C",
        "text": "It provides Infrastructure-as-Code (IaC) to automate NGFW deployment."
      },
      {
        "letter": "D",
        "text": "It manages threat intelligence data synchronization with NGFWs."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 5,
    "text": "By default, which type of traffic is configured by service route configuration to use the management interface?",
    "choices": [
      {
        "letter": "A",
        "text": "Security zone"
      },
      {
        "letter": "B",
        "text": "IPSec tunnel"
      },
      {
        "letter": "C",
        "text": "Virtual system (VSYS)"
      },
      {
        "letter": "D",
        "text": "Autonomous Digital Experience Manager (ADEM)"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 6,
    "text": "In regard to the Advanced Routing Engine (ARE), what must be enabled first when configuring a logical router on a PAN-OS firewall?",
    "choices": [
      {
        "letter": "A",
        "text": "License"
      },
      {
        "letter": "B",
        "text": "Plugin"
      },
      {
        "letter": "C",
        "text": "Content update"
      },
      {
        "letter": "D",
        "text": "General setting"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 7,
    "text": "Which two zone types are valid when configuring a new security zone? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "Tunnel"
      },
      {
        "letter": "B",
        "text": "Intrazone"
      },
      {
        "letter": "C",
        "text": "Internal"
      },
      {
        "letter": "D",
        "text": "Virtual Wire"
      }
    ],
    "answer": "AD",
    "type": "multi"
  },
  {
    "num": 8,
    "text": "An organization has configured GlobalProtect in a hybrid authentication model using both certificate-based authentication for the pre-logon stage\nand SAML-based multi-factor authentication (MFA) for user logon.\nHow does the GlobalProtect agent process the authentication flow on Windows endpoints?",
    "choices": [
      {
        "letter": "A",
        "text": "The GlobalProtect agent uses the machine certificate to establish a pre-logon tunnel; upon user sign-in, it prompts for SAML-based MFA credentials, ensuring both device and user identities are validated before granting full access."
      },
      {
        "letter": "B",
        "text": "The GlobalProtect agent uses the machine certificate during pre-logon for initial tunnel establishment, and then seamlessly reuses the same machine certificate for user-based authentication without requiring MFA."
      },
      {
        "letter": "C",
        "text": "Once the machine certificate is validated at pre-logon, the Windows endpoint completes MFA on behalf of the user by passing existing Windows Credential Provider details to the GlobalProtect gateway without prompting the user."
      },
      {
        "letter": "D",
        "text": "GlobalProtect requires the user to log in first for SAML-based MFA before establishing the pre-logon tunnel, rendering the pre-logon certificate authentication (CA) flow redundant."
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 9,
    "text": "An NGFW engineer is configuring multiple Panorama-managed firewalls to start sending all logs to Strata Logging Service. The Strata Logging\nService instance has been provisioned, the required device certificates have been installed, and Panorama and the firewalls have been\nsuccessfully onboarded to Strata Logging Service.\nWhich configuration task must be performed to start sending the logs to Strata Logging Service and continue forwarding them to the Panorama\nlog collectors as well?",
    "choices": [
      {
        "letter": "A",
        "text": "Modify all active Log Forwarding profiles to select the “Cloud Logging” option in each profile match list in the appropriate device groups."
      },
      {
        "letter": "B",
        "text": "Enable the “Panorama/Cloud Logging” option in the Logging and Reporting Settings section under Device --> Setup --> Management in the appropriate templates."
      },
      {
        "letter": "C",
        "text": "Select the “Enable Duplicate Logging” option in the Cloud Logging section under Device --> Setup --> Management in the appropriate templates."
      },
      {
        "letter": "D",
        "text": "Select the “Enable Cloud Logging” option in the Cloud Logging section under Device --> Setup --> Management in the appropriate templates."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 10,
    "text": "An NGFW engineer is configuring multiple Layer 2 interfaces on a Palo Alto Networks firewall, and all interfaces must be assigned to the same\nVLAN. During initial testing, it is reported that clients located behind the various interfaces cannot communicate with each other.\nWhich action taken by the engineer will resolve this issue?",
    "choices": [
      {
        "letter": "A",
        "text": "Configure each interface to belong to the same Layer 2 zone and enable IP routing between them."
      },
      {
        "letter": "B",
        "text": "Assign each interface to the appropriate Layer 2 zone and configure a policy that allows traffic within the VLAN."
      },
      {
        "letter": "C",
        "text": "Assign each interface to the appropriate Layer 2 zone and configure Security policies for interfaces not assigned to the same zone."
      },
      {
        "letter": "D",
        "text": "Enable IP routing between the interfaces and configure a Security policy to allow traffic between interfaces within the VLAN."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 11,
    "text": "In a Palo Alto Networks environment, GlobalProtect has been enabled using certificate-based authentication for both users and devices. To ensure proper validation of certificates, one or more certificate profiles are configured. What function do certificate profiles serve in this context?",
    "choices": [
      {
        "letter": "A",
        "text": "They store private keys for users and devices, effectively allowing the firewall to issue or reissue certificates if the primary Certificate Authority (CA) becomes unavailable, providing a built-in fallback CA to maintain continuous certificate issuance and authentication."
      },
      {
        "letter": "B",
        "text": "They define trust anchors (root / intermediate Certificate Authorities (CAs)), specify revocation checks (CRL/OCSP), and map certificate attributes (e.g., CN) for user or device authentication."
      },
      {
        "letter": "C",
        "text": "They allow the firewall to bypass certificate validation entirely, focusing only on username / password-based authentication."
      },
      {
        "letter": "D",
        "text": "They provide a one-click mechanism to distribute certificates to all endpoints without relying on external enrollment methods."
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 12,
    "text": "How does a Palo Alto Networks NGFW respond when the preemptive hold time is set to 0 minutes during configuration of route monitoring?",
    "choices": [
      {
        "letter": "A",
        "text": "It does not accept the configuration."
      },
      {
        "letter": "B",
        "text": "It accepts the configuration but throws a warning message."
      },
      {
        "letter": "C",
        "text": "It removes the static route because 0 is a NULL value."
      },
      {
        "letter": "D",
        "text": "It reinstalls the route into the routing information base (RIB) as soon as the path comes up."
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 13,
    "text": "After an engineer configures an IPSec tunnel with a Cisco ASA, the Palo Alto Networks firewall generates system messages reporting the tunnel is failing to establish. Which of the following actions will resolve this issue?",
    "choices": [
      {
        "letter": "A",
        "text": "Ensure that an active static or dynamic route exists for the VPN peer with next hop as the tunnel interface."
      },
      {
        "letter": "B",
        "text": "Configure the Proxy IDs to match the Cisco ASA configuration."
      },
      {
        "letter": "C",
        "text": "Check that IPSec is enabled in the management profile on the external interface."
      },
      {
        "letter": "D",
        "text": "Validate the tunnel interface VLAN against the peer’s configuration."
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 14,
    "text": "Which configuration in the LACP tab will enable pre-negotiation for an Aggregate Ethernet (AE) interface on a Palo Alto Networks high availability (HA) active/passive pair?",
    "choices": [
      {
        "letter": "A",
        "text": "Set Transmission Rate to “fast.”"
      },
      {
        "letter": "B",
        "text": "Set passive link state to “Auto.”"
      },
      {
        "letter": "C",
        "text": "Set “Enable in HA Passive State.”"
      },
      {
        "letter": "D",
        "text": "Set LACP mode to “Active.”"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 15,
    "text": "When integrating Kubernetes with Palo Alto Networks NGFWs, what is used to secure traffic between microservices?",
    "choices": [
      {
        "letter": "A",
        "text": "Service graph"
      },
      {
        "letter": "B",
        "text": "Ansible automation modules"
      },
      {
        "letter": "C",
        "text": "Panorama role-based access control (RBAC)"
      },
      {
        "letter": "D",
        "text": "CN-Series firewalls"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 16,
    "text": "When configuring a Zone Protection profile, in which section (protection type) would an NGFW engineer configure options to protect against activities such as spoofed IP addresses and split handshake session establishment attempts?",
    "choices": [
      {
        "letter": "A",
        "text": "Flood Protection"
      },
      {
        "letter": "B",
        "text": "Protocol Protection"
      },
      {
        "letter": "C",
        "text": "Packet-Based Attack Protection"
      },
      {
        "letter": "D",
        "text": "Reconnaissance Protection"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 17,
    "text": "For which two purposes is an IP address configured on a tunnel interface? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "Use of dynamic routing protocols"
      },
      {
        "letter": "B",
        "text": "Tunnel monitoring"
      },
      {
        "letter": "C",
        "text": "Use of peer IP"
      },
      {
        "letter": "D",
        "text": "Redistribution of User-ID"
      }
    ],
    "answer": "AB",
    "type": "multi"
  },
  {
    "num": 18,
    "text": "Which PAN-OS method of mapping users to IP addresses is the most reliable?",
    "choices": [
      {
        "letter": "A",
        "text": "Port mapping"
      },
      {
        "letter": "B",
        "text": "GlobalProtect"
      },
      {
        "letter": "C",
        "text": "Syslog"
      },
      {
        "letter": "D",
        "text": "Server monitoring"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 19,
    "text": "In an active/active high availability (HA) configuration with two PA-Series firewalls, how do the firewalls use the HA3 interface?",
    "choices": [
      {
        "letter": "A",
        "text": "To forward packets to the HA peer during session setup and asymmetric traffic flow"
      },
      {
        "letter": "B",
        "text": "To exchange hellos, heartbeats, HA state information, and management plane synchronization for routing and User-ID information"
      },
      {
        "letter": "C",
        "text": "To synchronize sessions, forwarding tables, IPSec security associations, and ARP tables between firewalls in an HA pair"
      },
      {
        "letter": "D",
        "text": "To perform session cache synchronization among all HA peers having the same cluster ID"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 20,
    "text": "A PA-Series firewall with all licensable features is being installed. The customer’s Security policy requires that users do not directly access websites. Instead, a security device must create the connection, and there must be authentication back to the Active Directory servers for all sessions. Which action meets the requirements in this scenario?",
    "choices": [
      {
        "letter": "A",
        "text": "Deploy the transparent proxy with Web Cache Communications Protocol (WCCP)."
      },
      {
        "letter": "B",
        "text": "Deploy the Next-Generation Firewalls as normal and install the User-ID agent."
      },
      {
        "letter": "C",
        "text": "Deploy the Advanced URL Filtering license and captive portal."
      },
      {
        "letter": "D",
        "text": "Deploy the explicit proxy with Kerberos authentication scheme."
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 21,
    "text": "What must be configured before a firewall administrator can define policy rules based on users and groups?",
    "choices": [
      {
        "letter": "A",
        "text": "User Mapping profile"
      },
      {
        "letter": "B",
        "text": "Authentication profile"
      },
      {
        "letter": "C",
        "text": "Group mapping settings"
      },
      {
        "letter": "D",
        "text": "LDAP Server profile"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 22,
    "text": "Which statement applies to the relationship between Panorama-pushed Security policy and local firewall Security policy?",
    "choices": [
      {
        "letter": "A",
        "text": "When a policy match is found in a local firewall policy, if any Panorama shared post-rule is configured, it will still be evaluated."
      },
      {
        "letter": "B",
        "text": "Local firewall rules are evaluated after Panorama pre-rules and before Panorama post-rules."
      },
      {
        "letter": "C",
        "text": "Panorama post-rules can be configured to be evaluated before local firewall policy for the purpose of troubleshooting."
      },
      {
        "letter": "D",
        "text": "The order of policy evaluation can be configured differently in different device groups."
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 23,
    "text": "Which networking technology can be configured on Layer 3 interfaces but not on Layer 2 interfaces?",
    "choices": [
      {
        "letter": "A",
        "text": "DDNS"
      },
      {
        "letter": "B",
        "text": "Link Duplex"
      },
      {
        "letter": "C",
        "text": "NetFlow"
      },
      {
        "letter": "D",
        "text": "LLDP"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 24,
    "text": "What is a result of enabling split tunneling in the GlobalProtect portal configuration with the “Both Network Traffic and DNS” option?",
    "choices": [
      {
        "letter": "A",
        "text": "It specifies when the secondary DNS server is used for resolution to allow access to specific domains that are not managed by the VPN."
      },
      {
        "letter": "B",
        "text": "It allows users to access internal resources when connected locally and external resources when connected remotely using the same FQDN."
      },
      {
        "letter": "C",
        "text": "It allows devices on a local network to access blocked websites by changing which DNS server resolves certain domain names."
      },
      {
        "letter": "D",
        "text": "It specifies which domains are resolved by the VPN-assigned DNS servers and which domains are resolved by the local DNS servers."
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 25,
    "text": "According to dynamic updates best practices, what is the recommended threshold value for content updates in a mission- critical network?",
    "choices": [
      {
        "letter": "A",
        "text": "8 hours"
      },
      {
        "letter": "B",
        "text": "16 hours"
      },
      {
        "letter": "C",
        "text": "32 hours"
      },
      {
        "letter": "D",
        "text": "48 hours"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 26,
    "text": "Which type of firewall resource can be assigned when configuring a new firewall virtual system (VSYS)?",
    "choices": [
      {
        "letter": "A",
        "text": "CPU"
      },
      {
        "letter": "B",
        "text": "Sessions limit"
      },
      {
        "letter": "C",
        "text": "Memory"
      },
      {
        "letter": "D",
        "text": "Security profile limit"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 27,
    "text": "Which forwarding methods can be used on the Objects tab when configuring the Log Forwarding profile?",
    "choices": [
      {
        "letter": "A",
        "text": "Panorama, syslog, email"
      },
      {
        "letter": "B",
        "text": "Syslog, HTTP, NetFlow"
      },
      {
        "letter": "C",
        "text": "Panorama, ADEM, syslog"
      },
      {
        "letter": "D",
        "text": "SNMP, HTTP, RADIUS"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 28,
    "text": "In a hybrid cloud deployment, what is the primary function of Ansible in managing Palo Alto Networks NGFWs?",
    "choices": [
      {
        "letter": "A",
        "text": "It provides a web interface for managing NGFW hardware clusters."
      },
      {
        "letter": "B",
        "text": "It enables centralized log collection and correlation for NGFWs."
      },
      {
        "letter": "C",
        "text": "It facilitates dynamic updates to NGFW threat databases."
      },
      {
        "letter": "D",
        "text": "It automates NGFW policy updates and configurations through playbooks."
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 29,
    "text": "Palo Alto Networks NGFWs use SSL/TLS profiles to secure which two types of connections? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "NAT tables"
      },
      {
        "letter": "B",
        "text": "User Authentication"
      },
      {
        "letter": "C",
        "text": "GlobalProtect Gateways"
      },
      {
        "letter": "D",
        "text": "GlobalProtect Portal"
      }
    ],
    "answer": "CD",
    "type": "multi"
  },
  {
    "num": 30,
    "text": "How does a Palo Alto Networks firewall choose the best route when it receives routes for the same destination from different routing protocols?",
    "choices": [
      {
        "letter": "A",
        "text": "The route that was received first will be entered into the forwarding table, and all subsequent routes will be rejected."
      },
      {
        "letter": "B",
        "text": "It will attempt to load balance the traffic across all routes."
      },
      {
        "letter": "C",
        "text": "It compares the administrative distance and chooses the one with the highest value."
      },
      {
        "letter": "D",
        "text": "It compares the administrative distance and chooses the one with the lowest value."
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 31,
    "text": "A large enterprise wants to implement certificate-based authentication for both users and devices, using an on-premises Microsoft Active Directory Certificate Services (AD CS) hierarchy as the primary certificate authority (CA). The enterprise also requires Online Certificate Status Protocol (OCSP) checks to ensure efficient revocation status updates and reduce the overhead on its NGFWs. The environment includes multiple Active Directory forests, Panorama management for several geographically dispersed firewalls, GlobalProtect portals and gateways needing distinct certificate profiles for users and devices, and strict Security policies demanding frequent revocation checks with minimal latency. Which approach best addresses these requirements while maintaining consistent policy enforcement?",
    "choices": [
      {
        "letter": "A",
        "text": "Deploy self-signed certificates at each site to simplify local certificate validation and reduce dependencies on a centralized CTurn off certificate revocation checks for lower overhead, rely on IP-based rules for GlobalProtect authentication, and use a single certificate profile for both users and devices."
      },
      {
        "letter": "B",
        "text": "Distribute the root and intermediate CA certificates via Panorama as shared objects to ensure all firewalls have a consistent trust chain. Configure OCSP responder profiles on each firewall to offload revocation checks to an internal OCSP server while keeping CRL checks as a fallback. Maintain separate certificate profiles for user and device authentication and use an automated enrollment method – such as Group Policy or SCEP – to deploy certificates to endpoints."
      },
      {
        "letter": "C",
        "text": "Configure each firewall independently to trust the root and intermediate CA certificates. Rely only on manual CRL checks for certificate revocation, and import both user and device certificates directly into each firewall’s local certificate store for authentication."
      },
      {
        "letter": "D",
        "text": "Obtain wildcard certificates from a public CA for both user and device authentication, and configure firewalls to perform CRL polling at the default update interval. Manually install user certificates on endpoints and synchronize firewall certificate stores through frequent manual SSH updates to maintain consistency."
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 32,
    "text": "An organization runs multiple Kubernetes clusters both on-premises and in public clouds (AWS, Azure, GCP). They want to deploy the Palo Alto Networks CN-Series NGFW to secure east-west traffic within each cluster, maintain consistent Security policies across all environments, and dynamically scale as containerized workloads spin up or down. They also plan to use a centralized Panorama instance for policy management and visibility. Which approach meets these requirements?",
    "choices": [
      {
        "letter": "A",
        "text": "Install standalone CN-Series instances in each cluster with local configuration only. Export daily policy configuration snapshots to Panorama for recordkeeping, but do not unify policy enforcement."
      },
      {
        "letter": "B",
        "text": "Configure the CN-Series only in public cloud clusters, and rely on Kubernetes Network Policies for on-premises cluster security. Synchronize partial policy information into Panorama manually as needed."
      },
      {
        "letter": "C",
        "text": "Use Kubernetes-native deployment tools (e.g., Helm) to deploy CN-Series in each cluster, ensuring local insertion into the service mesh or CNI. Manage all CN-Series firewalls centrally from Panorama, applying uniform Security policies across on-premises and cloud clusters."
      },
      {
        "letter": "D",
        "text": "Deploy a single CN-Series firewall in the on-premises data center to process traffic for all clusters, connecting remote clusters via VPN or peering. Manage this single instance through Panorama."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 33,
    "text": "When deploying Palo Alto Networks NGFWs in a cloud service provider (CSP) environment, which method ensures high availability (HA) across multiple availability zones?",
    "choices": [
      {
        "letter": "A",
        "text": "Deploying Ansible scripts for zone-specific scaling"
      },
      {
        "letter": "B",
        "text": "Implementing Terraform templates for redundancy within one availability zone"
      },
      {
        "letter": "C",
        "text": "Using load balancer and health probes"
      },
      {
        "letter": "D",
        "text": "Configuring active/active HA"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 34,
    "text": "An engineer at a managed services provider is updating an application that allows its customers to request firewall changes to also manage SDWAN. The application will be able to make any approved changes directly to devices via API. What is a requirement for the application to create SD-WAN interfaces?",
    "choices": [
      {
        "letter": "A",
        "text": "REST API’s “sdwanInterfaceprofiles” parameter on a Panorama device"
      },
      {
        "letter": "B",
        "text": "REST API’s “sdwanInterfaces” parameter on a firewall device"
      },
      {
        "letter": "C",
        "text": "XML API’s “sdwanprofiles/interfaces” parameter on a Panorama device"
      },
      {
        "letter": "D",
        "text": "XML API’s “InterfaceProfiles/sdwan” parameter on a firewall device"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 35,
    "text": "Which two actions in the IKE Gateways will allow implementation of post-quantum cryptography when building VPNs between multiple Palo Alto Networks NGFWs? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "Select IKE v2, enable the Advanced Options (cid:0) PQ PPK, then set a 64+ character string for the post-quantum pre shared key."
      },
      {
        "letter": "B",
        "text": "Ensure Authentication is set to “certificate,” then import a post-quantum derived certificate."
      },
      {
        "letter": "C",
        "text": "Select IKE v2 Preferred, enable the Advanced Options (cid:0) PQ KEM, then add one or more “Rounds.”"
      },
      {
        "letter": "D",
        "text": "Select IKE v2, enable the Advanced Options (cid:0) PQ KEM, then create an IKE Crypto Profile with Advanced Options adding one or more “Rounds.”"
      }
    ],
    "answer": "AD",
    "type": "multi"
  },
  {
    "num": 36,
    "text": "An NGFW engineer is establishing bidirectional connectivity between the accounting virtual system (VSYS) and the marketing VSYS. The traffic needs to transition between zones without leaving the firewall (no external physical connections). The interfaces for each VSYS are assigned to separate virtual routers (VRs), and inter-VR static routes have been configured. An external zone has been created correctly for each VSYS. Security policies have been added to permit the desired traffic between each zone and its respective external zone. However, the desired traffic is still unable to successfully pass from one VSYS to the other in either direction. Which additional configuration task is required to resolve this issue?",
    "choices": [
      {
        "letter": "A",
        "text": "Create a transit VSYS and route all inter-VSYS traffic through it."
      },
      {
        "letter": "B",
        "text": "Add each VSYS to the list of visible virtual systems of the other VSYS."
      },
      {
        "letter": "C",
        "text": "Enable the “allow inter-VSYS traffic” option in both external zone configurations."
      },
      {
        "letter": "D",
        "text": "Create Security policies to allow the traffic between the two external zones."
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 37,
    "text": "Without performing a context switch, which set of operations can be performed that will affect the operation of a connected firewall on the Panorama GUI?",
    "choices": [
      {
        "letter": "A",
        "text": "Restarting the local firewall, running a packet capture, accessing the firewall CLI"
      },
      {
        "letter": "B",
        "text": "Modification of local security rules, modification of a Layer 3 interface, modification of the firewall device hostname"
      },
      {
        "letter": "C",
        "text": "Modification of pre-security rules, modification of a virtual router, modification of an IKE Gateway Network Profile"
      },
      {
        "letter": "D",
        "text": "Modification of post NAT rules, creation of new views on the local firewall ACC tab, creation of local custom reports"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 38,
    "text": "Which set of options is available for detailed logs when building a custom report on a Palo Alto Networks NGFW?",
    "choices": [
      {
        "letter": "A",
        "text": "Traffic, User-ID, URL"
      },
      {
        "letter": "B",
        "text": "Traffic, threat, data filtering, User-ID"
      },
      {
        "letter": "C",
        "text": "GlobalProtect, traffic, application statistics"
      },
      {
        "letter": "D",
        "text": "Threat, GlobalProtect, application statistics, WildFire submissions"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 39,
    "text": "An administrator plans to upgrade a pair of active/passive firewalls to a new PAN-OS release. The environment is highly sensitive, and downtime must be minimized. What is the recommended upgrade process for minimal disruption in this high availability (HA) scenario?",
    "choices": [
      {
        "letter": "A",
        "text": "Suspend the active firewall to trigger a failover to the passive firewall. With traffic now running on the former passive unit, upgrade the suspended (now passive) firewall and confirm proper operation. Then fail traffic back and upgrade the remaining firewall."
      },
      {
        "letter": "B",
        "text": "Shut down the currently active firewall and upgrade it offline, allowing the passive firewall to handle all traffic. Once the active firewall finishes upgrading, bring it back online and rejoin the HA cluster. Finally, upgrade the passive firewall while the newly upgraded unit remains active."
      },
      {
        "letter": "C",
        "text": "Isolate both firewalls from the production environment and upgrade them in a separate, offline setup. Reconnect them only after validating the new software version, resuming HA functionality once both units are fully upgraded and tested."
      },
      {
        "letter": "D",
        "text": "Push the new PAN-OS version simultaneously to both firewalls, having them upgrade and reboot in parallel. Rely on automated HA reconvergence to restore normal operations without manually failing over traffic."
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 40,
    "text": "Which two statements describe an external zone in the context of virtual systems (VSYS) on a Palo Alto Networks firewall? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "It is associated with an interface within a VSYS of a firewall."
      },
      {
        "letter": "B",
        "text": "It is a security object associated with a specific virtual router of a VSYS."
      },
      {
        "letter": "C",
        "text": "It is not associated with an interface; it is associated with a VSYS itself."
      },
      {
        "letter": "D",
        "text": "It is a security object associated with a specific VSYS."
      }
    ],
    "answer": "CD",
    "type": "multi"
  },
  {
    "num": 41,
    "text": "Which zone type allows traffic between zones in different virtual systems (VSYS), without the traffic leaving the firewall?",
    "choices": [
      {
        "letter": "A",
        "text": "Isolated"
      },
      {
        "letter": "B",
        "text": "Transient"
      },
      {
        "letter": "C",
        "text": "External"
      },
      {
        "letter": "D",
        "text": "Internal"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 42,
    "text": "A multinational organization wants to use the Cloud Identity Engine (CIE) to aggregate identity data from multiple sources (on premises AD, Azure AD, Okta) while enforcing strict data isolation for different regional business units. Each region’s firewalls, managed via Panorama, must only receive the user and group information relevant to that region. The organization aims to minimize administrative overhead while meeting data sovereignty requirements. Which approach achieves this segmentation of identity data?",
    "choices": [
      {
        "letter": "A",
        "text": "Create one CIE tenant, aggregate all identity data into a single view, and redistribute the full dataset to all firewalls. Rely on per-firewall Security policies to restrict access to out-of-scope user and group information."
      },
      {
        "letter": "B",
        "text": "Establish separate CIE tenants for each business unit, integrating each tenant with the relevant identity sources. Redistribute user and group data from each tenant only to the region’s firewalls, maintaining a strict one-to-one mapping of tenant to business unit."
      },
      {
        "letter": "C",
        "text": "Disable redistribution of identity data entirely. Instead, configure each regional firewall to pull user and group details directly from its local identity providers (IdPs)."
      },
      {
        "letter": "D",
        "text": "Deploy a single CIE tenant that collects all identity data, then configure segments within the tenant to filter and redistribute only the relevant user/group sets to each regional firewall group."
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 43,
    "text": "An engineer is implementing a new rollout of SAML for administrator authentication across a company’s Palo Alto Networks NGFWs. User authentication on company firewalls is currently performed with RADIUS, which will remain available for six months, until it is decommissioned. The company wants both authentication types to be running in parallel during the transition to SAML. Which two actions meet the criteria? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "Create a testing and rollback plan for the transition from Radius to SAML, as the two authentication profiles cannot be run in tandem."
      },
      {
        "letter": "B",
        "text": "Create an authentication sequence that includes both the “RADIUS” Server Profile and “SAML Identity Provider” Server Profile to run the two services in tandem."
      },
      {
        "letter": "C",
        "text": "Create and apply an authentication profile with the “SAML Identity Provider” Server Profile."
      },
      {
        "letter": "D",
        "text": "Create and add the “SAML Identity Provider” Server Profile to the authentication profile for the “RADIUS” Server Profile."
      }
    ],
    "answer": "AC",
    "type": "multi"
  },
  {
    "num": 44,
    "text": "An enterprise uses GlobalProtect with both user- and machine-based certificate authentication and requires pre-logon, OCSP checks, and minimal user disruption. They manage multiple firewalls via Panorama and deploy domain-issued machine certificates via Group Policy. Which approach ensures continuous, secure connectivity and consistent policy enforcement?",
    "choices": [
      {
        "letter": "A",
        "text": "Use a wildcard certificate from a public CA, disable all revocation checks to reduce latency, and manage certificate renewals manually on each firewall."
      },
      {
        "letter": "B",
        "text": "Distribute root and intermediate CAs via Panorama template, use distinct certificate profiles for user versus machine certs, reference an internal OCSP responder, and automate certificate deployment with Group Policy."
      },
      {
        "letter": "C",
        "text": "Configure a single certificate profile for both user and machine certificates. Rely solely on CRLs for revocation to minimize complexity."
      },
      {
        "letter": "D",
        "text": "Deploy self-signed certificates on each firewall, allow IP-based authentication to override certificate checks, and use default GlobalProtect settings for user / machine identification."
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 45,
    "text": "Which statement applies to Log Collector Groups?",
    "choices": [
      {
        "letter": "A",
        "text": "Log redundancy is available only if each Log Collector has the same amount of total disk storage."
      },
      {
        "letter": "B",
        "text": "Enabling redundancy increases the log processing traffic in a Collector Group by 50%."
      },
      {
        "letter": "C",
        "text": "In any single Collector Group, all the Log Collectors must run on the same Panorama model. D. The maximum number of Log Collectors in a Log Collector Group is 18 plus two hot spares."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 46,
    "text": "Which interface types should be used to configure link monitoring for a high availability (HA) deployment on a Palo Alto Networks NGFW?",
    "choices": [
      {
        "letter": "A",
        "text": "HA, Virtual Wire, and Layer 2"
      },
      {
        "letter": "B",
        "text": "Tap, Virtual Wire, and Layer 3"
      },
      {
        "letter": "C",
        "text": "Virtual Wire, Layer 2, and Layer 3"
      },
      {
        "letter": "D",
        "text": "HA, Layer 2, and Layer 3"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 47,
    "text": "Which CLI command is used to configure the management interface as a DHCP client?",
    "choices": [
      {
        "letter": "A",
        "text": "set network dhcp interface management"
      },
      {
        "letter": "B",
        "text": "set network dhcp type management-interface"
      },
      {
        "letter": "C",
        "text": "set deviceconfig system type dhcp-client"
      },
      {
        "letter": "D",
        "text": "set deviceconfig management type dhcp-client"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 48,
    "text": "Which configuration step is required when implementing a new self-signed root certificate authority (CA) certificate for SSL decryption on a Palo Alto Networks firewall?",
    "choices": [
      {
        "letter": "A",
        "text": "Import the new subordinate CA certificate into the trust stores of all client devices."
      },
      {
        "letter": "B",
        "text": "Set the subordinate CA certificate as the default routing certificate for all network traffic."
      },
      {
        "letter": "C",
        "text": "Configure the subordinate CA to issue certificates with indefinite validity periods."
      },
      {
        "letter": "D",
        "text": "Disable all existing SSL decryption rules until the new certificate is fully propagated."
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 49,
    "text": "What are the phases of the Palo Alto Networks AI Runtime Security: Network Intercept solution?",
    "choices": [
      {
        "letter": "A",
        "text": "Scanning, Isolation, Whitelisting, Logging"
      },
      {
        "letter": "B",
        "text": "Discovery, Deployment, Detection, Prevention"
      },
      {
        "letter": "C",
        "text": "Policy Generation, Discovery, Enforcement, Logging"
      },
      {
        "letter": "D",
        "text": "Profiling, Policy Generation, Enforcement, Reporting"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 50,
    "text": "What is the purpose of assigning an Admin Role Profile to a user in a Palo Alto Networks NGFW?",
    "choices": [
      {
        "letter": "A",
        "text": "Allow access to all resources without restrictions."
      },
      {
        "letter": "B",
        "text": "Enable multi-factor authentication (MFA) for administrator access."
      },
      {
        "letter": "C",
        "text": "Define granular permissions for management tasks."
      },
      {
        "letter": "D",
        "text": "Restrict access to sensitive report data."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 51,
    "text": "An organization is deploying VM-Series firewalls in Microsoft Azure to secure its VNets. A key requirement is that the security infrastructure must be resilient to the failure of an entire Azure Availability Zone. What is the recommended method to achieve this goal?",
    "choices": [
      {
        "letter": "A",
        "text": "Deploy multiple, independent VM-Series firewalls in different Availability Zones and use an Azure Load Balancer to distribute traffic to them."
      },
      {
        "letter": "B",
        "text": "Implement a Terraform configuration that automatically redeploys the firewall in a new zone if the original one fails."
      },
      {
        "letter": "C",
        "text": "Use Azure Traffic Manager to direct traffic to a primary VM-Series firewall, with a second firewall in another zone as a failover target."
      },
      {
        "letter": "D",
        "text": "Configure PAN-OS active/passive high availability (HA) between two VM-Series instances in separate Availability Zones using HA links over a VNet peering connection."
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 52,
    "text": "When creating a Log Forwarding profile on a PAN-OS firewall to direct logs to various external and internal systems, which set of methods is available?",
    "choices": [
      {
        "letter": "A",
        "text": "Syslog, Panorama, SD-WAN"
      },
      {
        "letter": "B",
        "text": "Panorama/Cloud logging, email, Syslog"
      },
      {
        "letter": "C",
        "text": "Email, Syslog, NetFlow"
      },
      {
        "letter": "D",
        "text": "HTTP, RADIUS, SNMP"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 53,
    "text": "A company is enabling SSL Forward Proxy to inspect encrypted traffic. A security engineer generates a new certificate on the firewall and flags it with the \"Forward Trust\" certificate property. What is the critical next step that must be performed for decryption to function correctly without causing security warnings for end users?",
    "choices": [
      {
        "letter": "A",
        "text": "Set the forward trust certificate as the SSL/TLS Service profile for the management interface."
      },
      {
        "letter": "B",
        "text": "Create a Security policy rule that allows traffic from the certificate of the firewall to all the zones."
      },
      {
        "letter": "C",
        "text": "Import the private key of the forward trust certificate onto the domain controller."
      },
      {
        "letter": "D",
        "text": "Install the public portion of the forward trust certificate into the trust store of all client machines."
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 54,
    "text": "An administrator is configuring a site-to-site IPSec VPN and assigns an IP address to the tunnel interface. Which two abilities are enabled by this specific configuration step? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "Configuring tunnel monitoring to verify the liveliness of the connection."
      },
      {
        "letter": "B",
        "text": "Firewall performing NAT traversal."
      },
      {
        "letter": "C",
        "text": "Running a dynamic routing protocol like OSPF over the tunnel."
      },
      {
        "letter": "D",
        "text": "Firewall encrypting and decrypting packet payloads."
      }
    ],
    "answer": "AC",
    "type": "multi"
  },
  {
    "num": 55,
    "text": "A DevOps team is building a repeatable process for deploying new Palo Alto Networks VM-Series firewalls. The entire infrastructure, including virtual networks, subnets, and the firewalls themselves, must be defined in code to ensure consistency and enable version control. Which tool is primarily used for this type of declarative Infrastructure as Code (IaC) provisioning?",
    "choices": [
      {
        "letter": "A",
        "text": "Terraform"
      },
      {
        "letter": "B",
        "text": "Azure DevOps"
      },
      {
        "letter": "C",
        "text": "Ansible"
      },
      {
        "letter": "D",
        "text": "Panorama"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 56,
    "text": "A network security engineer is segmenting a single firewall into VSYS-A and VSYS-B. For traffic to flow from VSYS-A to VSYS-B, external zones are required. What are two fundamental properties of the external zones needed for this configuration? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "They must be linked to the same virtual router as the ingress interface."
      },
      {
        "letter": "B",
        "text": "They represent their parent VSYS without being tied to a physical or logical interface."
      },
      {
        "letter": "C",
        "text": "They are a security construct belonging to a single VSYS."
      },
      {
        "letter": "D",
        "text": "They are automatically created when inter-VSYS routing is enabled."
      }
    ],
    "answer": "BC",
    "type": "multi"
  },
  {
    "num": 57,
    "text": "A network engineer observes a pattern of anomalous traffic hitting an external-facing zone, including a high volume of TCP packets that are not part of a new session handshake (non-SYN), and a large number of ICMP fragments. The engineer decides to apply a Zone Protection profile to mitigate these potential threats. Which protection type within the profile must be configured?",
    "choices": [
      {
        "letter": "A",
        "text": "Protocol Protection"
      },
      {
        "letter": "B",
        "text": "Flood Protection"
      },
      {
        "letter": "C",
        "text": "Reconnaissance Protection"
      },
      {
        "letter": "D",
        "text": "Packet-Based Attack Protection"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 58,
    "text": "An administrator is configuring a GlobalProtect pre-logon VPN. The administrator has already imported the necessary internal certificate authority (CA) certificates for issuing machine certificates onto the firewall. Which configuration is required on the GlobalProtect Gateway to enable pre-logon using these machine certificates?",
    "choices": [
      {
        "letter": "A",
        "text": "Create a device-based Security policy that allows traffic from the pre-logon user to an internal management zone."
      },
      {
        "letter": "B",
        "text": "Create an authentication profile that points to the machine certificate's CA and assign it by using the client authentication settings of the GlobalProtect Portal."
      },
      {
        "letter": "C",
        "text": "Create a certificate profile that trusts the machine certificate's CA and assign it within the Gateway Agent --> Client Authentication settings."
      },
      {
        "letter": "D",
        "text": "Configure the Gateway Agent --> Tunnel Settings to use IPSec with machine certificate authentication for the pre- logon tunnel."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 59,
    "text": "A network administrator needs to replace the default self-signed certificate on a firewall with one signed by the company's internal certificate authority (CA). Which two firewall features would require this new certificate to be assigned via an SSL/TLS service profile? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "User-ID agent redistribution"
      },
      {
        "letter": "B",
        "text": "RADIUS server authentication"
      },
      {
        "letter": "C",
        "text": "Authentication portal"
      },
      {
        "letter": "D",
        "text": "GlobalProtect gateway"
      }
    ],
    "answer": "CD",
    "type": "multi"
  },
  {
    "num": 60,
    "text": "A network administrator is establishing a site-to-site VPN between a Palo Alto Networks firewall and a partner's Check Point Security Gateway. The partner has provided a specific list of local and remote IP address subnets that are permitted through the tunnel. The initial tunnel configuration on the PAN-OS firewall fails during the IKE Phase 2 exchange. Which configuration step is essential to ensure compatibility with the policy-based Check Point gateway?",
    "choices": [
      {
        "letter": "A",
        "text": "Define the local and remote subnets provided by the partner in the Proxy ID settings."
      },
      {
        "letter": "B",
        "text": "Create individual Security policies for each pair of local and remote subnets."
      },
      {
        "letter": "C",
        "text": "Assign a specific IP address to the tunnel interface to match the Check Point gateway."
      },
      {
        "letter": "D",
        "text": "Enable Dead Peer Detection (DPD) in the IKE Gateway configuration."
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 61,
    "text": "Which method creates the most reliable user-to-IP mapping due to being based on a direct authentication from the user's device to the firewall?",
    "choices": [
      {
        "letter": "A",
        "text": "Portal authentication"
      },
      {
        "letter": "B",
        "text": "PAN-OS XML API to push mappings"
      },
      {
        "letter": "C",
        "text": "Polling security event logs with a User-ID agent"
      },
      {
        "letter": "D",
        "text": "Authentication logs from Syslog receiver"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 62,
    "text": "An administrator configures a GlobalProtect gateway with split tunneling for network traffic based on an access route. Users report that public web browsing works, but they cannot resolve the names of internal servers. The administrator determines that all DNS queries are being sent to the public DNS servers configured on the users' endpoints. Which GlobalProtect portal setting should be configured to resolve this issue?",
    "choices": [
      {
        "letter": "A",
        "text": "Split tunneling for DNS and specify the internal corporate domains in the \"Domain\" list"
      },
      {
        "letter": "B",
        "text": "DNS Proxy feature on the firewall to point clients to the gateway IP for DNS"
      },
      {
        "letter": "C",
        "text": "\"DNS Forwarding\" option on the gateway's tunnel interface"
      },
      {
        "letter": "D",
        "text": "NAT rule to allow DNS traffic from the GlobalProtect clients to the internal DNS servers"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 63,
    "text": "Which initial action is required to configure logical routers?",
    "choices": [
      {
        "letter": "A",
        "text": "Changing the virtual router type from \"default\" to \"advanced\""
      },
      {
        "letter": "B",
        "text": "Activating an advanced routing subscription"
      },
      {
        "letter": "C",
        "text": "Committing a new advanced routing software module"
      },
      {
        "letter": "D",
        "text": "Checking \"advanced routing\" in general settings"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 64,
    "text": "A network security engineer at a 24/7 online retailer is upgrading an active/passive high availability (HA) cluster of PAN-OS firewalls. The primary goal is to perform the upgrade with no service interruption to online transactions. The engineer has already downloaded the new software to both devices. Which sequence of actions will meet this requirement?",
    "choices": [
      {
        "letter": "A",
        "text": "From Panorama, create a scheduled software update job targeting both firewalls in the HA pair to run at the same time, then rely on the HA election process to manage the failover automatically."
      },
      {
        "letter": "B",
        "text": "Upgrade the passive firewall first while it is still in the passive state. Once it reboots and is operational, suspend the active firewall to fail over to the newly upgraded device. Then, upgrade the remaining firewall."
      },
      {
        "letter": "C",
        "text": "Force the active firewall into a suspended state to trigger a failover, then upgrade and reboot it. Suspend the currently active firewall to fail traffic back to the upgraded unit. Upgrade the remaining firewall."
      },
      {
        "letter": "D",
        "text": "Disable HA synchronization on the active firewall, upgrade the passive firewall, and then re-enable synchronization. Once synchronized, repeat the process on the other firewall."
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 65,
    "text": "A government agency needs to ensure that all user web access is explicitly mediated and authenticated. The agency has the following requirements: • Client browsers must be manually configured to send traffic to the firewall's IP address and a specific port. • The firewall must support seamless single sign-on (SSO) with the users' existing Active Directory credentials. Which feature set should the engineer configure to meet the agency's requirements?",
    "choices": [
      {
        "letter": "A",
        "text": "Web proxy in explicit mode with an Authentication policy by using Kerberos"
      },
      {
        "letter": "B",
        "text": "Decryption policy that redirects users to a SAML identity provider for authentication"
      },
      {
        "letter": "C",
        "text": "Web proxy in transparent mode with an Authentication policy by using multi-factor authentication (MFA)"
      },
      {
        "letter": "D",
        "text": "User-ID agent integration with Authentication Portal for authentication"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 66,
    "text": "A network security engineer is reviewing the dynamic update settings for a fleet of firewalls in a financial institution that has a policy prioritizing operational stability above all else. The engineer notes that the current content update threshold is set to 24 hours. Following the Palo Alto Networks recommended best practices for mission-critical deployments, which adjustment should be made to the threshold?",
    "choices": [
      {
        "letter": "A",
        "text": "Change to \"download only\" and schedule manual installation."
      },
      {
        "letter": "B",
        "text": "Increase to 48 hours."
      },
      {
        "letter": "C",
        "text": "Decrease to 12 hours."
      },
      {
        "letter": "D",
        "text": "Reset to reconfirm 24 hours."
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 67,
    "text": "What is the correct sequence of evaluation for Security policy rulebases?",
    "choices": [
      {
        "letter": "A",
        "text": "Panorama Pre-Rules --> Local Firewall Rules --> Panorama Post-Rules"
      },
      {
        "letter": "B",
        "text": "Panorama Post-Rules --> Panorama Pre-Rules --> Local Firewall Rules"
      },
      {
        "letter": "C",
        "text": "Panorama Shared Rules --> Local Firewall Rules --> Device Group Rules"
      },
      {
        "letter": "D",
        "text": "Local Firewall Rules --> Panorama Pre-Rules --> Panorama Post-Rules"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 68,
    "text": "An administrator needs to ensure that a firewall can download threat prevention and software updates, but the management port is on an isolated network without internet access. Which service must be rerouted through a data plane interface using a service route to allow the firewall to download these updates?",
    "choices": [
      {
        "letter": "A",
        "text": "External dynamic lists"
      },
      {
        "letter": "B",
        "text": "GlobalProtect Clientless VPN"
      },
      {
        "letter": "C",
        "text": "Palo Alto Networks Services"
      },
      {
        "letter": "D",
        "text": "Syslog"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 69,
    "text": "An organization is adopting an Infrastructure as Code (IaC) approach to manage its entire network environment, including its Palo Alto Networks firewalls. The organization has chosen Ansible as its primary tool for this initiative. How does Ansible enable an IaC model for managing this organization's firewalls?",
    "choices": [
      {
        "letter": "A",
        "text": "By providing real-time threat intelligence feeds directly to the firewalls' data plane"
      },
      {
        "letter": "B",
        "text": "By providing a graphical user interface that simplifies the creation of security policies through a drag-and-drop interface"
      },
      {
        "letter": "C",
        "text": "By automatically discovering and mapping all network devices to generate a baseline configuration"
      },
      {
        "letter": "D",
        "text": "By defining firewall configurations in playbooks that can be version-controlled and executed repeatedly"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 70,
    "text": "A network security engineer wants to create Security policy rules that allow or deny traffic based on a user's department, which corresponds to groups in the company's Active Directory. To achieve this, the firewall needs to retrieve group information from the directory server. Which configuration object must be created first to establish the connection with the Active Directory server?",
    "choices": [
      {
        "letter": "A",
        "text": "LDAP server profile"
      },
      {
        "letter": "B",
        "text": "User-ID agent service account"
      },
      {
        "letter": "C",
        "text": "Authentication sequence"
      },
      {
        "letter": "D",
        "text": "Kerberos server profile"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 71,
    "text": "When an engineer creates a new VSYS on a supported firewall platform, which resource can be explicitly limited in the VSYS configuration to control its capacity?",
    "choices": [
      {
        "letter": "A",
        "text": "Dedicated dataplane memory"
      },
      {
        "letter": "B",
        "text": "Maximum number of admin accounts"
      },
      {
        "letter": "C",
        "text": "Maximum number of log entries"
      },
      {
        "letter": "D",
        "text": "Maximum number of NAT rules"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 72,
    "text": "A large organization has separate production and development environments, each with its own set of firewalls managed by Panorama. The organization uses Cloud Identity Engine (CIE) to consolidate user identities from Active Directory (AD) and Okta. A security mandate requires that development firewalls must only learn about \"DEV\" and \"QA\" user groups, while production firewalls should only see \"Prod\" user groups. How can an administrator enforce this separation using CIE with minimal complexity?",
    "choices": [
      {
        "letter": "A",
        "text": "Create two segments, one with only \"DEV\" and \"QA\" groups, and one with \"Prod\" groups Redistribute each segment to the corresponding group of firewalls."
      },
      {
        "letter": "B",
        "text": "Redistribute all user and group information to all firewalls and use Panorama Device Group hierarchy to apply different Group Mapping profiles."
      },
      {
        "letter": "C",
        "text": "Create filters using CLI commands to filter \"Prod,\" \"DEV,\" and \"QA\" groups."
      },
      {
        "letter": "D",
        "text": "Configure two separate CIE instances, one for production and the other for development. Sync each instance to both AD and Okta."
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 73,
    "text": "An administrator must perform several actions on a fleet of firewalls from a central Panorama instance. To maintain efficiency, the administrator wants to only perform actions that do not require switching context into each firewall's individual web interface. Which set of actions is available to the administrator directly from the Panorama UI?",
    "choices": [
      {
        "letter": "A",
        "text": "Creating a new VLAN - Assigning an interface to the new VLAN Configuring a new DHCP server on the firewall"
      },
      {
        "letter": "B",
        "text": "Modifying a pre-rule - Editing a shared service object - Creating a new certificate profile"
      },
      {
        "letter": "C",
        "text": "Accessing the CLI - Restarting the device - Installing the latest content and software versions"
      },
      {
        "letter": "D",
        "text": "Configuring a new IPSec tunnel - Modifying the IKE gateway - Changing the DNS server settings of the firewall"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 74,
    "text": "A network administrator is configuring an Aggregate Ethernet (AE) interface on an active/passive high availability (HA) pair. To reduce network downtime during a failover, the administrator wants the passive firewall's AE interface to be fully negotiated with the switch before it becomes active. Which Link Aggregation Control Protocol (LACP) setting achieves this administrator's goal?",
    "choices": [
      {
        "letter": "A",
        "text": "LACP Mode active"
      },
      {
        "letter": "B",
        "text": "Enable in HA passive state"
      },
      {
        "letter": "C",
        "text": "System Priority: 1"
      },
      {
        "letter": "D",
        "text": "Transmission Rate: fast"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 75,
    "text": "A firewall administrator needs to configure a new Palo Alto Networks firewall so that its management interface automatically obtains an IP address, netmask, and default gateway from the network. Which command should be executed in the CLI to accomplish this goal?",
    "choices": [
      {
        "letter": "A",
        "text": "set deviceconfig system interface mgt mode dhcp"
      },
      {
        "letter": "B",
        "text": "set network interface management dhcp enable"
      },
      {
        "letter": "C",
        "text": "set deviceconfig system type dhcp-client"
      },
      {
        "letter": "D",
        "text": "configure system management-interface ip dynamic"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 76,
    "text": "When multiple routes have the same destination prefix, which attribute does the firewall use first to determine route preference?",
    "choices": [
      {
        "letter": "A",
        "text": "Administrative distance"
      },
      {
        "letter": "B",
        "text": "Route metric"
      },
      {
        "letter": "C",
        "text": "Next-hop availability"
      },
      {
        "letter": "D",
        "text": "Longest prefix match"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 77,
    "text": "An organization must secure its AWS and Azure environments using a managed Palo Alto Networks solution, and all policies must be synchronized from an existing Panorama deployment. The organization wants to insert security with the least possible impact on its application teams and use existing hub-and-spoke network designs. • The AWS environment uses a centralized AWS Transit Gateway (TGW) architecture. • The Azure environment uses a Virtual WAN (vWAN) hub. Which two actions are the most appropriate in this use case? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "Deploy Cloud NGFW endpoints in every application virtual private cloud (VPC), ignoring the TGW."
      },
      {
        "letter": "B",
        "text": "Deploy Cloud NGFW into the vWAN hub as a trusted security partner, and update routing policies to secure traffic."
      },
      {
        "letter": "C",
        "text": "Deploy individual VM-Series firewalls in each spoke virtual network (VNet) and manage them as a device group in Panorama."
      },
      {
        "letter": "D",
        "text": "Deploy Cloud NGFW endpoints into a security virtual private cloud (VPC), and adjust the TGW route tables to inspect traffic flowing though the hub."
      }
    ],
    "answer": "BD",
    "type": "multi"
  },
  {
    "num": 78,
    "text": "A cloud security team wants to extend its existing Palo Alto Networks Security policies into the organization's Kubernetes environments. The team requires an NGFW solution that can be deployed natively as a container and managed by Panorama. Which firewall form factor meets these requirements?",
    "choices": [
      {
        "letter": "A",
        "text": "Cloud NGFW"
      },
      {
        "letter": "B",
        "text": "PA-5400 Series"
      },
      {
        "letter": "C",
        "text": "VM-Series"
      },
      {
        "letter": "D",
        "text": "CN-Series"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 79,
    "text": "A network architect is planning the deployment of a new IPSec VPN tunnel to connect a local data center to a cloud environment. The plan must include all necessary Security policy configurations for both tunnel negotiation and data transit. Which two Security policy requirements must be included in the implementation plan? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "A policy must explicitly permit the IPSec container application between the external-facing zone and local zone."
      },
      {
        "letter": "B",
        "text": "A policy must explicitly permit only the IKE application between the external-facing zone and local zone."
      },
      {
        "letter": "C",
        "text": "A pair of policies is required to control the flow of data traffic into and out of the security zone assigned to the tunnel interface."
      },
      {
        "letter": "D",
        "text": "The default interzone-default security policy is sufficient to allow the tunnel negotiation traffic between the firewall and the remote peer."
      }
    ],
    "answer": "BC",
    "type": "multi"
  },
  {
    "num": 80,
    "text": "A network security engineer needs to permit traffic between two distinct VSYS that reside on one Palo Alto Networks firewall. This traffic will not egress the firewall to an external device. Which zone type must be configured to act as the logical source and destination for this traffic flow?",
    "choices": [
      {
        "letter": "A",
        "text": "External"
      },
      {
        "letter": "B",
        "text": "TAP"
      },
      {
        "letter": "C",
        "text": "Layer 3"
      },
      {
        "letter": "D",
        "text": "Layer 2"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 81,
    "text": "What is the requirement for interface link speeds when configuring a virtual wire on a Palo Alto Networks firewall?",
    "choices": [
      {
        "letter": "A",
        "text": "They must be configured with auto-negotiate settings regardless of the port type."
      },
      {
        "letter": "B",
        "text": "They must all be either copper or fiber optic, however they can be different."
      },
      {
        "letter": "C",
        "text": "They must have the same link speed and transmission mode."
      },
      {
        "letter": "D",
        "text": "They must be the same media type."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 82,
    "text": "When configuring a physical interface on a Palo Alto Networks firewall, which IP-based service is only available if the interface is set to Layer 3 mode?",
    "choices": [
      {
        "letter": "A",
        "text": "DDNS client"
      },
      {
        "letter": "B",
        "text": "NetFlow export"
      },
      {
        "letter": "C",
        "text": "QoS"
      },
      {
        "letter": "D",
        "text": "Link monitoring"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 83,
    "text": "A network engineer observes that after a primary link recovers, the firewall immediately switches traffic back from the backup static route to the primary static route. The engineer checks the path monitoring configuration for the primary route. Which value is configured for the preemptive hold time to cause this behavior?",
    "choices": [
      {
        "letter": "A",
        "text": "Lowest possible value greater than 0"
      },
      {
        "letter": "B",
        "text": "0"
      },
      {
        "letter": "C",
        "text": "Default value"
      },
      {
        "letter": "D",
        "text": "Feature disabled"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 84,
    "text": "A Palo Alto Networks firewall has the following interfaces configured: • ethernet1/1 (Layer 3) • ethernet1/2 (TAP) • ethernet1/3 (Layer 2) • ethernet1/4 (virtual wire) An administrator needs to create a link group to monitor upstream connectivity for high availability (HA) failover. Which set of interfaces can be added to the link group?",
    "choices": [
      {
        "letter": "A",
        "text": "ethernet1/1, ethernet1/2, ethernet1/4"
      },
      {
        "letter": "B",
        "text": "ethernet1/1, ethernet1/2, ethernet1/3"
      },
      {
        "letter": "C",
        "text": "ethernet1/2, ethernet1/3, ethernet1/4"
      },
      {
        "letter": "D",
        "text": "ethernet1/1, ethernet1/3, ethernet1/4"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 85,
    "text": "An administrator is designing a public key infrastructure (PKI) integration for a large-scale deployment with thousands of users authenticating via client certificates. A key design goal is to ensure that certificate revocation status is checked efficiently with minimal impact on firewall performance and minimal delay for the connecting user. What is the primary advantage of using the Online Certificate Status Protocol (OCSP) instead of certificate revocation lists (CRLs) in this scenario?",
    "choices": [
      {
        "letter": "A",
        "text": "OCSP allows the firewall to act as its own certificate authority (CA), and it simplifies certificate management."
      },
      {
        "letter": "B",
        "text": "OCSP provides real-time status for a certificate on demand, is more scalable, and uses less firewall memory."
      },
      {
        "letter": "C",
        "text": "OCSP is an older, more widely supported protocol than CRLs. ensuring compatibility with all client devices."
      },
      {
        "letter": "D",
        "text": "OCSP bundles all certificate statuses into a single, digitally signed file for faster downloads by the firewall."
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 86,
    "text": "An organization is migrating its data center to Amazon Web Services (AWS) and needs to deploy VM-Series firewalls to inspect all ingress and egress traffic. The solution must provide both resilience across multiple Availability Zones and the ability to scale horizontally. Which combination of AWS services and Palo Alto Networks components is required for this use case?",
    "choices": [
      {
        "letter": "A",
        "text": "AWS Lambda function that monitors the firewall's health and re-routes traffic using the AWS API"
      },
      {
        "letter": "B",
        "text": "PAN-OS active/active high availability (HA) pair with an AWS Transit Gateway"
      },
      {
        "letter": "C",
        "text": "Amazon EC2 Auto Scaling group with VM-Series firewalls and an Amazon Gateway Load Balancer"
      },
      {
        "letter": "D",
        "text": "Single VM-Series firewall with an Elastic IP address that can be re-associated upon failure"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 87,
    "text": "Which two services are configured by applying an SSL/TLS service profile? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "Global Protect portal"
      },
      {
        "letter": "B",
        "text": "Log forwarding to Strata Logging Service"
      },
      {
        "letter": "C",
        "text": "Forward-Trust certificate"
      },
      {
        "letter": "D",
        "text": "Syslog server monitoring"
      }
    ],
    "answer": "AD",
    "type": "multi"
  },
  {
    "num": 88,
    "text": "A firewall administrator uses Panorama to manage a fleet of firewalls. After successfully onboarding the firewalls to Strata Logging Service and enabling cloud logging via a template, the security operations team reports that they can no longer see new logs on the on-premises Panorama log collectors. Logs are appearing correctly in Strata Logging Service. Which setting was likely missed in the Panorama template configuration?",
    "choices": [
      {
        "letter": "A",
        "text": "The device certificates for the Panorama log collectors were not renewed after enabling the cloud logging connection."
      },
      {
        "letter": "B",
        "text": "Duplicate logging (cloud and on-premises) is disabled under Device --> Setup --> Management."
      },
      {
        "letter": "C",
        "text": "The Log Forwarding profile was modified to send logs only to the Strata Logging Service and no longer includes the on-premises Panorama log collectors."
      },
      {
        "letter": "D",
        "text": "The Panorama log collectors were not defined as primary destinations within the collector group configuration for the managed firewalls."
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 89,
    "text": "What is a valid configurable limit for setting resource quotas when defining a new VSYS on a Palo Alto Networks firewall?",
    "choices": [
      {
        "letter": "A",
        "text": "Percentage of total CPU utilization"
      },
      {
        "letter": "B",
        "text": "Maximum number of SSL decryption rules"
      },
      {
        "letter": "C",
        "text": "Maximum number of virtual routers"
      },
      {
        "letter": "D",
        "text": "Disk space allocation for logs"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 90,
    "text": "When considering the various methods for User-ID to learn user-to-IP address mappings, which source is considered the most accurate due to the mapping being explicitly created through an authentication event directly with the firewall?",
    "choices": [
      {
        "letter": "A",
        "text": "X-Forwarded-For (XFF) headers"
      },
      {
        "letter": "B",
        "text": "Server monitoring"
      },
      {
        "letter": "C",
        "text": "GlobalProtect"
      },
      {
        "letter": "D",
        "text": "Authentication Portal"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 91,
    "text": "After a recent high availability (HA) failover test on an active/passive cluster, an engineer noted a 30-45 second delay before traffic started flowing through a Link Aggregation Control Protocol (LACP) aggregate interface on the newly active firewall. What should have been configured to support LACP pre-negotiation to minimize LACP convergence delay?",
    "choices": [
      {
        "letter": "A",
        "text": "Enable LACP fast failover."
      },
      {
        "letter": "B",
        "text": "Set LACP mode to passive."
      },
      {
        "letter": "C",
        "text": "Enable in HA passive state."
      },
      {
        "letter": "D",
        "text": "Set HA link monitoring to aggressive."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 92,
    "text": "An engineer is creating an automation workflow. The first step is to deploy a new VM-Series firewall into a VMware vSphere environment, including its virtual machine (VM) configuration and network interfaces. The second step is to connect to the firewall and configure a complex set of Security policies and objects. The team uses both Terraform and Ansible. For which part of this workflow would Terraform typically be used?",
    "choices": [
      {
        "letter": "A",
        "text": "Pushing threat intelligence updates to the new firewall"
      },
      {
        "letter": "B",
        "text": "Deploying the VM and associated network interfaces"
      },
      {
        "letter": "C",
        "text": "Storing the credentials needed to access the vSphere environment"
      },
      {
        "letter": "D",
        "text": "Applying the detailed Security policies and objects"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 93,
    "text": "An organization uses Cloud Identity Engine (CIE) to gather user information from its on-premises Active Directory (AD) for employees and a separate Azure AD for external partners. Due to compliance regulations, the firewalls protecting the internal network must not have any identity information about external partners. Conversely, firewalls in the partner-facing DMZ should only be aware of partner identities. Which CIE feature is designed to solve this data partitioning requirement?",
    "choices": [
      {
        "letter": "A",
        "text": "Panorama templates, which can be used to push different User-ID agent configurations to each firewall group"
      },
      {
        "letter": "B",
        "text": "Segments, which can be configured to create distinct, filter-based views of users and groups that are then redistributed only to the appropriate firewalls"
      },
      {
        "letter": "C",
        "text": "Multiple tenants, where a separate CIE tenant is required for each user directory to maintain isolation"
      },
      {
        "letter": "D",
        "text": "Directory sync filtering, which is used at the source to prevent specific OUs from being imported into CIE"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 94,
    "text": "What are two valid zone types that can be selected from the zone configuration menu, per Palo Alto Networks best practices? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "Layer 3"
      },
      {
        "letter": "B",
        "text": "Layer 2"
      },
      {
        "letter": "C",
        "text": "Management"
      },
      {
        "letter": "D",
        "text": "DMZ"
      }
    ],
    "answer": "AB",
    "type": "multi"
  },
  {
    "num": 95,
    "text": "An administrator is configuring dynamic updates on a Palo Alto Networks firewall that protects a hospital's patient record system. The primary concern is ensuring maximum stability and avoiding any service disruption from a potentially problematic content update. To align with Palo Alto Networks best practices for such environments, which threshold should the administrator set for content updates?",
    "choices": [
      {
        "letter": "A",
        "text": "0 hours"
      },
      {
        "letter": "B",
        "text": "12 hours"
      },
      {
        "letter": "C",
        "text": "24 hours"
      },
      {
        "letter": "D",
        "text": "48 hours"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 96,
    "text": "An engineer is configuring a GlobalProtect portal and wants to enable split tunneling. The requirement is to route DNS queries for \"https://www.google.com/search?q=corp.internal.com\" to the DNS servers assigned by the VPN, while allowing all other DNS queries to be resolved by the client's locally configured DNS. What is the effect of configuring this split DNS policy?",
    "choices": [
      {
        "letter": "A",
        "text": "It provides selective DNS resolution, with specified domains resolved through the tunnel, optimizing performance for other lookups."
      },
      {
        "letter": "B",
        "text": "It blocks access to all domains that are not explicitly listed in the split tunnel configuration."
      },
      {
        "letter": "C",
        "text": "It forces all applications to use the corporate DNS servers, regardless of the split tunnel settings for IP traffic."
      },
      {
        "letter": "D",
        "text": "It creates a DNS proxy on the client endpoint that forwards all queries to the firewall for inspection."
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 97,
    "text": "An automation engineer is developing a Python script to standardize SD-WAN deployments across multiple customer tenants in Panorama. A key requirement is to programmatically create path quality profiles to monitor link performance based on latency, jitter, and packet loss. Which API call is required for this task?",
    "choices": [
      {
        "letter": "A",
        "text": "XML API command with an xpath of config/devices/entry/vsys/entry/path-quality-profiles on Panorama"
      },
      {
        "letter": "B",
        "text": "XML API command with an xpath of sdwan/path-quality-profiles on a managed firewall"
      },
      {
        "letter": "C",
        "text": "POST request to the SDWanPathQualityProfiles object endpoint via the REST API on Panorama"
      },
      {
        "letter": "D",
        "text": "POST request to the pathMonitoringProfiles object endpoint via the REST API on a managed firewall"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 98,
    "text": "A security administrator is creating a new custom report to get a consolidated view of network events and needs to select a database to query for the report data. Which valid set of databases is available for the task?",
    "choices": [
      {
        "letter": "A",
        "text": "Threat, URL Filtering, WildFire Submissions, GlobalProtect"
      },
      {
        "letter": "B",
        "text": "Traffic, User-ID, Application Statistics, HIP Match"
      },
      {
        "letter": "C",
        "text": "Data Filtering, IP-Tag, User-ID, Endpoint Security"
      },
      {
        "letter": "D",
        "text": "System, Config, Authentication, Session Flow"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 99,
    "text": "An organization's Security policy states that for all outbound web traffic, the TCP session to the external web server must be established by the firewall, not the user's workstation. This requires configuring user web browsers to point to the firewall. Authentication is also required. Which solution on a PA-Series firewall meets these specific needs?",
    "choices": [
      {
        "letter": "A",
        "text": "Transparent proxy"
      },
      {
        "letter": "B",
        "text": "Explicit proxy"
      },
      {
        "letter": "C",
        "text": "GlobalProtect with User-ID"
      },
      {
        "letter": "D",
        "text": "Decryption policy with Authentication Portal"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 100,
    "text": "An administrator is troubleshooting a newly configured site-to-site VPN between a PAN-OS firewall and a third-party policy-based VPN gateway. The tunnel allows traffic between the first pair of configured subnets, but traffic to a newly added remote subnet is failing. The administrator has confirmed that routing and Security policies are correct. What is the most likely cause of this issue?",
    "choices": [
      {
        "letter": "A",
        "text": "A static route for the new subnet pointing to the tunnel interface is missing."
      },
      {
        "letter": "B",
        "text": "The Security policy for the new subnet must be placed above the existing VPN policy."
      },
      {
        "letter": "C",
        "text": "The new local and remote subnets are missing from the Proxy ID configuration."
      },
      {
        "letter": "D",
        "text": "The tunnel's maximum transmission unit (MTU) size must be increased to accommodate the new traffic."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 101,
    "text": "An organization needs a GlobalProtect solution that meets two key requirements: • IT administrators must be able to run scripts and push updates to endpoints before a user logs in. • Users must authenticate with their cloud identity provider, which is protected by multi-factor authentication (MFA). Which GlobalProtect authentication configuration should be used to meet both requirements?",
    "choices": [
      {
        "letter": "A",
        "text": "Cookie-based authentication for both pre-logon and user logon."
      },
      {
        "letter": "B",
        "text": "SAML authentication for pre-logon and certificate-based authentication for user logon."
      },
      {
        "letter": "C",
        "text": "Single authentication profile using Kerberos to handle both pre-logon and user logon."
      },
      {
        "letter": "D",
        "text": "Certificate-based authentication for pre-logon and SAML authentication for user logon."
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 102,
    "text": "What is the primary use case for the CN-Series NGFW?",
    "choices": [
      {
        "letter": "A",
        "text": "Protecting mobile users and remote branch offices (east-west)"
      },
      {
        "letter": "B",
        "text": "Providing security for physical data center perimeters (north-south)"
      },
      {
        "letter": "C",
        "text": "Securing traffic in and out of a public cloud VPC or VNet (north-south)"
      },
      {
        "letter": "D",
        "text": "Enforcing Security policies between pods in a Kubernetes environment (east-west)"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 103,
    "text": "After a recent security audit, a company is required to enforce more strict validation for all certificate-based authentication, including for GlobalProtect clients. An engineer observes the firewall accepting certificates from a recently compromised intermediate certificate authority (CA). The engineer needs to update the firewall configuration to use an Online Certificate Status Protocol (OCSP) responder to check for revoked certificates in real time. In which configuration object would the engineer enable OCSP verification for the CAs used in the authentication process?",
    "choices": [
      {
        "letter": "A",
        "text": "Authentication sequence"
      },
      {
        "letter": "B",
        "text": "Decryption profile"
      },
      {
        "letter": "C",
        "text": "SSL/TLS service profile"
      },
      {
        "letter": "D",
        "text": "Certificate profile"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 104,
    "text": "An administrator enables SSL Forward Proxy decryption using a self-signed certificate on a Palo Alto Networks firewall as the forward trust certificate. Shortly after, users report receiving \"Your connection is not private\" browser errors for all external websites. What is the most likely cause of these widespread certificate errors?",
    "choices": [
      {
        "letter": "A",
        "text": "The decryption policy is configured with a \"no-decrypt\" action, which causes browsers to reject the connection."
      },
      {
        "letter": "B",
        "text": "The external websites are using TLS 1.3, which cannot be decrypted by the firewall without a specific license."
      },
      {
        "letter": "C",
        "text": "The firewall's forward untrust certificate has expired, preventing it from identifying untrusted sites."
      },
      {
        "letter": "D",
        "text": "The firewall's self-signed CA certificate is not deployed to the trusted certificate store on client endpoints."
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 105,
    "text": "An engineer is configuring a site-to-site IPSec VPN to a partner network. The IKE Gateway and IPSec tunnel configurations are complete, and the tunnel interface has been assigned to a security zone. However, the tunnel fails to establish, and no application traffic passes through it once it is up. Which two Security policy configurations are required to allow tunnel establishment and data traffic flow in this scenario? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "A security rule is needed to allow IKE and IPSec traffic between the zone where the physical interface resides and the zone of the partner gateway."
      },
      {
        "letter": "B",
        "text": "A single bidirectional security rule must be configured to manage traffic flowing through the tunnel interface."
      },
      {
        "letter": "C",
        "text": "Security rules must be configured to permit application traffic from the local zone to the tunnel zone, and from the tunnel zone to the local zone."
      },
      {
        "letter": "D",
        "text": "An Application Override policy is needed to allow both the IKE negotiation and the encapsulated data traffic."
      }
    ],
    "answer": "AC",
    "type": "multi"
  },
  {
    "num": 106,
    "text": "A network administrator is configuring path monitoring for a primary static route to ensure immediate failback from a backup route. The administrator wants the primary route to become active again without any delay as soon as its path is restored. Which preemptive hold time value should the administrator configure to achieve this immediate failback?",
    "choices": [
      {
        "letter": "A",
        "text": "-1"
      },
      {
        "letter": "B",
        "text": "0"
      },
      {
        "letter": "C",
        "text": "1"
      },
      {
        "letter": "D",
        "text": "2"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 107,
    "text": "A network security engineer is designing a resilient architecture for inspecting traffic in Google Cloud Platform (GCP). The design must ensure that firewall service is maintained even if a single GCP zone becomes unavailable. Which architecture should be used for the VM-Series firewalls in this use case?",
    "choices": [
      {
        "letter": "A",
        "text": "Ansible playbook that monitors the health of the primary firewall and launches a new one in a different zone when a failure is detected"
      },
      {
        "letter": "B",
        "text": "Single, large VM-Series firewall in one zone that is configured for live migration to another zone upon failure"
      },
      {
        "letter": "C",
        "text": "Instance group of VM-Series firewalls spread across multiple zones with traffic routed to them by a GCP Internal Load Balancer"
      },
      {
        "letter": "D",
        "text": "PAN-OS active/active high availability (HA) cluster configured with dedicated HA interfaces in a shared VPC"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 108,
    "text": "An engineer configures a PA-440 firewall to act as a switch by creating several Layer 2 interfaces and assigning them all to VLAN 20. A file server is connected to interface ethernet1/1, and client workstations are connected to interfaces ethernet1/2 and ethemet1/3. All devices are in VLAN 20. The clients are unable to access the file server. Which configuration step to allow this communication by default is missing?",
    "choices": [
      {
        "letter": "A",
        "text": "Create an Aggregate Ethernet (AE) group that includes all three interfaces."
      },
      {
        "letter": "B",
        "text": "Place ethernet1/1, ethernet1/2, and ethernet1/3 into the same Layer 2 zone."
      },
      {
        "letter": "C",
        "text": "Create an \"allow\" Security policy with the source and destination VLAN set to \"VLAN 20\"."
      },
      {
        "letter": "D",
        "text": "Create a Layer 3 subinterface for VLAN 20 to enable routing."
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 109,
    "text": "Which feature can be enabled on a Layer 3 interface but is not available on Layer 2 interfaces?",
    "choices": [
      {
        "letter": "A",
        "text": "NetFlow profile"
      },
      {
        "letter": "B",
        "text": "LLDP profile"
      },
      {
        "letter": "C",
        "text": "QoS profile"
      },
      {
        "letter": "D",
        "text": "DHCP client"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 110,
    "text": "An engineer is required to configure a site-to-site VPN that will automatically fail over to a backup link if the primary tunnel goes down. The engineer also needs to exchange routes dynamically between the sites. Which two features necessitate assigning an IP address to the tunnel interface? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "Tunnel monitoring"
      },
      {
        "letter": "B",
        "text": "Proxy ID configuration"
      },
      {
        "letter": "C",
        "text": "IKEv2 protocol support"
      },
      {
        "letter": "D",
        "text": "Dynamic routing"
      }
    ],
    "answer": "AD",
    "type": "multi"
  },
  {
    "num": 111,
    "text": "An organization is migrating its GlobalProtect user authentication from an existing LDAP directory to a new Kerberos server. To ensure a smooth transition, the network security team needs to allow users from both directories to authenticate for a period of 90 days. The firewall should first attempt authentication against the new Kerberos server and then fall back to the legacy LDAP server if the initial attempt fails. Which two configurations are required to implement this authentication fallback strategy? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "Configure a new RADIUS proxy on the firewall to handle authentication requests for both Kerberos and LDAP."
      },
      {
        "letter": "B",
        "text": "Implement a User-ID Group Mapping policy to link users between the LDAP and Kerberos directories."
      },
      {
        "letter": "C",
        "text": "Configure an authentication sequence that lists the Kerberos authentication profile first, followed by the LDAP authentication profile."
      },
      {
        "letter": "D",
        "text": "Configure a new authentication profile that references the Kerberos server profile."
      }
    ],
    "answer": "CD",
    "type": "multi"
  },
  {
    "num": 112,
    "text": "A network administrator is hardening a new Palo Alto Networks firewall and wants to ensure that all firewall-generated management traffic, such as calls to Strata Logging Service, uses a dedicated in-band data port instead of the out-of-band management port. Which configuration setting should the administrator modify to reroute this type of traffic?",
    "choices": [
      {
        "letter": "A",
        "text": "Service route"
      },
      {
        "letter": "B",
        "text": "Interface Management profile"
      },
      {
        "letter": "C",
        "text": "Virtual router"
      },
      {
        "letter": "D",
        "text": "Static route"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 113,
    "text": "A Managed Security Service Provider (MSSP) is creating a new VSYS for a customer. To prevent this customer’s traffic from overwhelming the firewall’s state table, which resource limit should the MSSP configure for the new VSYS?",
    "choices": [
      {
        "letter": "A",
        "text": "Max security profiles"
      },
      {
        "letter": "B",
        "text": "Max bandwidth"
      },
      {
        "letter": "C",
        "text": "Max sessions"
      },
      {
        "letter": "D",
        "text": "Max Log Forwarding profiles"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 114,
    "text": "Which two Palo Alto Networks firewall services are secured by attaching an SSL/TLS service profile to their configuration? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "Authentication portal"
      },
      {
        "letter": "B",
        "text": "GlobalProtect portal"
      },
      {
        "letter": "C",
        "text": "LDAP server profiles"
      },
      {
        "letter": "D",
        "text": "Prisma Access service connections"
      }
    ],
    "answer": "AB",
    "type": "multi"
  },
  {
    "num": 115,
    "text": "To comply with new directives mandating the use of quantum-resistant cryptography for all data-in-transit a network engineer is tasked with reconfiguring existing IKEv2 VPN tunnels between PA-Series firewalls to meet this requirement. Which two actions should the engineer take to ensure compliance? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "Configure an IKE Crypto profile with one or more post-quantum rounds selected and apply it to an IKE Gateway configured for the post- quantum key exchange mechanism."
      },
      {
        "letter": "B",
        "text": "Establish a shared secret of at least 64 characters and configure it as a post-quantum pre-shared key (PPK) within an IKEv2-only IKE Gateway."
      },
      {
        "letter": "C",
        "text": "Generate a post-quantum pre-shared key (PPK) and apply it within the IPSec tunnel configuration's advanced settings."
      },
      {
        "letter": "D",
        "text": "Enable GlobalProtect with quantum-resistant tunneling and apply the profile to the IKE Gateway."
      }
    ],
    "answer": "AB",
    "type": "multi"
  },
  {
    "num": 116,
    "text": "An organization is securing its cloud workloads using the Palo Alto Networks platform. The goal is to use a fully managed firewall service that integrates with Panorama for consistent policy management. The solution must be scalable and require minimal changes to the existing routing fabric. • The AWS cloud uses a distributed architecture where each application virtual private cloud (VPC) routes internet traffic through its own internet gateway. • The Azure cloud is built around a Virtual WAN (vWAN) hub for centralized connectivity. Which two deployments meet these criteria? (Choose two.)",
    "choices": [
      {
        "letter": "A",
        "text": "Native cloud provider firewalls in both cloud environments and connected to Panorama for management"
      },
      {
        "letter": "B",
        "text": "Cloud NGFW in each spoke VNet with User-Defined Routes (UDRs) to redirect traffic bypassing the vWAN hub"
      },
      {
        "letter": "C",
        "text": "Cloud NGFW endpoints in each application VPC, updating the VPC route tables to direct traffic through the endpoints"
      },
      {
        "letter": "D",
        "text": "Cloud NGFW as a security partner in the vWAN hub with routing configured to send traffic through the NGFW"
      }
    ],
    "answer": "CD",
    "type": "multi"
  },
  {
    "num": 117,
    "text": "A holding company has recently acquired two new businesses, each with its own Okta identity provider. The holding company wants to use a single Cloud Identity Engine (CIE) instance to provide User-ID for all three organizations’ firewalls. However, for legal reasons, the firewalls of Company A must only receive identity data from Company A's Okta instance, and the firewalls of Company B must only receive data from Company B's Okta instance. Which configuration in CIE supports this requirement with highest operational efficiency?",
    "choices": [
      {
        "letter": "A",
        "text": "Configure a CIE tenant, connect Okta, and create segments."
      },
      {
        "letter": "B",
        "text": "Configure the firewalls for each company to query their respective Okta IdPs directly, bypassing CIE for redistribution."
      },
      {
        "letter": "C",
        "text": "Push all identity data to Panorama and use Panorama's group mapping include/exclude lists to control what each firewall learns."
      },
      {
        "letter": "D",
        "text": "Create a master CIE tenant for the holding company and peer it with two subordinate tenants, one for each acquired business."
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 118,
    "text": "A network engineer has configured a PAN-OS firewall for client certificate authentication. The firewall has the corporate root CA certificate loaded. Client certificates are issued by an intermediate certificate authority (CA), which is signed by the root CA. However, when users attempt to connect, the authentication fails, and system logs indicate an \"invalid certificate\" error. What is the most likely cause of this authentication failure?",
    "choices": [
      {
        "letter": "A",
        "text": "Intermediate CA certificate has not been imported onto the firewall and added to the trust chain."
      },
      {
        "letter": "B",
        "text": "Client certificates were generated with an insecure key length (e.g., 1024-bit RSA)."
      },
      {
        "letter": "C",
        "text": "Firewall clock is out of sync with the CA server by more than five minutes."
      },
      {
        "letter": "D",
        "text": "Online Certificate Status Protocol (OCSP) responder is unreachable, and no certificate revocation list (CRL) fallback is configured."
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 119,
    "text": "An administrator is configuring firewalls via a Panorama template to forward logs to a newly provisioned Strata Logging Service instance. The operational requirement is to maintain existing logging to on-premises Panorama log collectors for immediate, low-latency queries while also forwarding logs to Strata Logging Service for long-term archival. The administrator has already configured and enabled cloud logging connectivity. Which additional step is necessary to meet the operational requirement?",
    "choices": [
      {
        "letter": "A",
        "text": "Enable duplicate logging (cloud and on-premises) under Device -> Setup -> Management in the appropriate templates."
      },
      {
        "letter": "B",
        "text": "Enable log syncing and commit the template changes to both the on-premises and cloud collectors."
      },
      {
        "letter": "C",
        "text": "In the collector group settings, add the Strata Logging Service as a secondary destination for the on-premises collector."
      },
      {
        "letter": "D",
        "text": "Add the Panorama log collector and Strata Logging Service IP addresses to the cloud logging service routes to ensure dual-path cloud and on-premises reachability."
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 120,
    "text": "An administrator needs to perform several maintenance tasks on a managed firewall directly from the Panorama console without using the Context Switch feature. Which set of tasks can the administrator fully execute from the Panorama UI?",
    "choices": [
      {
        "letter": "A",
        "text": "Edit a post-rule. Create a new certificate profile. Configure the firewall's hostname."
      },
      {
        "letter": "B",
        "text": "Download and install a new content update. View current firewall session details. Initiate a device reboot."
      },
      {
        "letter": "C",
        "text": "Create a new zone. Configure a new virtual router. View the local ACC on the firewall."
      },
      {
        "letter": "D",
        "text": "Modify the IP address of a Layer 3 interface. Configure a new local administrator account. Edit a pre-rule."
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 121,
    "text": "When deploying a pair of Palo Alto Networks firewalls in an active/active high availability (HA) cluster what is the dedicated role of the HA3 link?",
    "choices": [
      {
        "letter": "A",
        "text": "Control plane synchronization for heartbeats and state information"
      },
      {
        "letter": "B",
        "text": "Packet forwarding for session setup and asymmetric traffic"
      },
      {
        "letter": "C",
        "text": "Management plane synchronization for configurations and policies"
      },
      {
        "letter": "D",
        "text": "Data plane synchronization for session tables and forwarding tables"
      }
    ],
    "answer": "B",
    "type": "single"
  }
];



function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function shuffleChoices(question) {
  const indices = question.choices.map((_, i) => i);
  const shuffledIndices = shuffleArray(indices);
  
  const oldToText = {};
  question.choices.forEach(c => { oldToText[c.letter] = c.text; });
  
  const correctSet = new Set(question.answer.split(''));
  const oldCorrectLetters = question.choices
    .filter(c => correctSet.has(c.letter))
    .map(c => c.letter);
  
  const newChoices = shuffledIndices.map((oldIdx) => ({
    letter: question.choices[oldIdx].letter,
    text: question.choices[oldIdx].text
  }));

  const newCorrect = oldCorrectLetters.map(oldLetter => {
    const text = oldToText[oldLetter];
    return newChoices.find(c => c.text === text).letter;
  });
  newCorrect.sort();

  return {
    ...question,
    choices: newChoices,
    answer: newCorrect.join('')
  };
}

function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function shuffleChoices(question) {
  const indices = question.choices.map((_, i) => i);
  const shuffledIndices = shuffleArray(indices);
  
  const oldToText = {};
  question.choices.forEach(c => { oldToText[c.letter] = c.text; });
  
  const correctSet = new Set(question.answer.split(''));
  const oldCorrectLetters = question.choices
    .filter(c => correctSet.has(c.letter))
    .map(c => c.letter);
  
  const newChoices = shuffledIndices.map((oldIdx) => ({
    letter: question.choices[oldIdx].letter,
    text: question.choices[oldIdx].text
  }));

  const newCorrect = oldCorrectLetters.map(oldLetter => {
    const text = oldToText[oldLetter];
    return newChoices.find(c => c.text === text).letter;
  });
  newCorrect.sort();

  return {
    ...question,
    choices: newChoices,
    answer: newCorrect.join('')
  };
}