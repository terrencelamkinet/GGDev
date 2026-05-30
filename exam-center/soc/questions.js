const ngfwSocQuestions = [
  {
    "num": 1,
    "text": "Where can an administrator begin to grant a new non-SSO user access to o Cortex XDR tenant? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Customer Support Portal"
      },
      {
        "letter": "B",
        "text": "Cortex Gateway"
      },
      {
        "letter": "C",
        "text": "Cortex XDR tenant settinas under Access Management"
      },
      {
        "letter": "D",
        "text": "IT Service Portal"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 2,
    "text": "Which action should an administrator take to create automated response actions when a user account is compromised? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Map the events as a type of Cortex XSOAR incident, then run a playbook."
      },
      {
        "letter": "B",
        "text": "Runa custom script from the Cortex XDR script library."
      },
      {
        "letter": "C",
        "text": "Create a script in Cortex XSOAR that will run a playbook based on the scenario."
      },
      {
        "letter": "D",
        "text": "Create playbook triggers in Cortex XSIAM and run playbooks for each alert."
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 3,
    "text": "Which two types of tasks are supported in Cortex XSIAM playbooks? (Choose two answers)",
    "choices": [
      {
        "letter": "A",
        "text": "Script creation"
      },
      {
        "letter": "B",
        "text": "Conditional"
      },
      {
        "letter": "C",
        "text": "Data collection"
      },
      {
        "letter": "D",
        "text": "Sub-playbook"
      }
    ],
    "answer": "BD",
    "type": "multi"
  },
  {
    "num": 4,
    "text": "Which SOC role investigates a new Low severity alert? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "SOC manager"
      },
      {
        "letter": "B",
        "text": "Threat hunter"
      },
      {
        "letter": "C",
        "text": "Triage specialist"
      },
      {
        "letter": "D",
        "text": "Incident responder"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 5,
    "text": "Which activities are facilitated through the War Room in Cortex XSOAR? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Running security playbooks, scripts, and commands"
      },
      {
        "letter": "B",
        "text": "Creating, editing, and deleting tasks in the workplan"
      },
      {
        "letter": "C",
        "text": "Viewing asummary of case details and alerts"
      },
      {
        "letter": "D",
        "text": "Conducting initial investigation of incident data and threat intelligence"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 6,
    "text": "Which scripting language will allow the use of the Query Builder in Cortex XDR to show the top five accounts with failed Windows Logons in the past 24 hours? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "PowerShell"
      },
      {
        "letter": "B",
        "text": "JavaScript"
      },
      {
        "letter": "C",
        "text": "XQL"
      },
      {
        "letter": "D",
        "text": "Python"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 7,
    "text": "Which statement explains the difference between the Cortex Identity Threat Detection and Response (ITDR) module and identity analytics in Cortex XSIAM? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "ldentity analytics detects suspicious Logins and MFA spamming, whereas the TDR module defends against anomalous insider activity and"
      },
      {
        "letter": "B",
        "text": "The ITDR module |s designed for compliance reporting, while identity analytics focuses on detecting and * responding to brute force attacks and"
      },
      {
        "letter": "C",
        "text": "Identity analytics provides prevention of suspicious logins, whereas the ITDR module focuses on advanced threat vectors."
      },
      {
        "letter": "D",
        "text": "The ITDR module provides basic security event monitoring, while identity analytics focuses on integrating various security tools."
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 8,
    "text": "What ts the WildFire verdict on a sample that does not pose a direct security threat, but is snown to display obtrusive behavior? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Grayware"
      },
      {
        "letter": "B",
        "text": "Unknown"
      },
      {
        "letter": "C",
        "text": "Benign"
      },
      {
        "letter": "D",
        "text": "Malware"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 9,
    "text": "Why would a security engineer be unable to activate Cortex XDR analytics when configuring data sources and alert sensors during a Cortex XSIAM evaluation? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "The engineer needs to install the Analytics engine."
      },
      {
        "letter": "B",
        "text": "Pathfinder must be activated before turning on analytics."
      },
      {
        "letter": "C",
        "text": "Baseline requirements must be met before activating analytics."
      },
      {
        "letter": "D",
        "text": "The engineer still needs to activate the identity Analytics engine."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 10,
    "text": "What can be used to triage and determine if an artifact in Cortex XDR is malicious? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Alert severity"
      },
      {
        "letter": "B",
        "text": "MITRE tactic"
      },
      {
        "letter": "C",
        "text": "SmartScore"
      },
      {
        "letter": "D",
        "text": "WildFire report"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 11,
    "text": "In Cortex XDR, what can be used to notify analysts of atomic behavior related to processes, registry, files, and network activity? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Indicator of compromise (LOC)"
      },
      {
        "letter": "B",
        "text": "Network traffic analysis (NTA)"
      },
      {
        "letter": "C",
        "text": "Behavioral indicator of compromise (BIOC)"
      },
      {
        "letter": "D",
        "text": "Analytics behavioral indicator of compromise (ABIOC)"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 12,
    "text": "How do indicator verdicts in Cortex XSOAR assist analysts in threat detection and response efforts? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "They classify indicators as malicious, suspicious, benign, or unknown, enabling analysts to prioritize ond respond to threats."
      },
      {
        "letter": "B",
        "text": "They classify indicators solely based on their frequency of occurrence in the network, allowing analysts to * identify common patterns."
      },
      {
        "letter": "C",
        "text": "They categorize indicators based on their geographic origin, helping analysts focus on threats from specific countries."
      },
      {
        "letter": "D",
        "text": "They categorize indicators based on the threat actor's tactics, techniques, and procedures."
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 13,
    "text": "A customer is investigating a security incident in which unusual network traffic is observed and a malicious process is identified on an endpoint.\nWhich Cortex XDR capability assists with correlating firewall network logs and endpoint data in this environment? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Analytics"
      },
      {
        "letter": "B",
        "text": "User authentication management"
      },
      {
        "letter": "C",
        "text": "Log stitching"
      },
      {
        "letter": "D",
        "text": "Indicator of compromise (JOC) rules"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 14,
    "text": "Which type of task will help orcanize other tasks and manage the flow of a playbook in Cortex XSIAM? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Conditional"
      },
      {
        "letter": "B",
        "text": "Section header"
      },
      {
        "letter": "C",
        "text": "Standard"
      },
      {
        "letter": "D",
        "text": "Data collection"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 15,
    "text": "With a Windows endpoint, what is required to remove the Cortex XDR agent when the endpoint is no longer online and cannot be managed directly from the management console? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "A Cortex XDR administrator must provide the end user with an offline removal tool created in the management console."
      },
      {
        "letter": "B",
        "text": "An administrator must disable the agent by opening the agent console from the system tray and entering * a password."
      },
      {
        "letter": "C",
        "text": "When running the uninstaller, the administrator must enter an uninstall pessword from the management console."
      },
      {
        "letter": "D",
        "text": "An administrator must use Cytool to disable security protection on the endpoint with an uninstall password."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 16,
    "text": "Anew incident in Cortex XSIAM contains WildFire malware and Behavioral Threat Protection (BTP) alerts about an unsigned process attempting to dump the memory of lsass.exe.\nWhich initial verdict applies to this incident? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "False positive"
      },
      {
        "letter": "B",
        "text": "False negative"
      },
      {
        "letter": "C",
        "text": "True negative"
      },
      {
        "letter": "D",
        "text": "True positive"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 17,
    "text": "Which action is the responsibility of the SOC manager? (Choose one answer) e A, Developing and implementing crisis communication plans @ B. Handling direct end-user support or help desk issues ¢ C, Performing initial triage and classification of incidents",
    "choices": [
      {
        "letter": "A",
        "text": "Developing and implementing crisis communication plans"
      },
      {
        "letter": "B",
        "text": "Handling direct end-user support or help desk issues"
      },
      {
        "letter": "C",
        "text": "Performing initial triage and classification of incidents"
      },
      {
        "letter": "D",
        "text": "Troubleshooting network cabling and physical installation"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 18,
    "text": "What is the role of content packs in Cortex XSOAR? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "To provide prebuilt bundles for supporting security orchestration use cases"
      },
      {
        "letter": "B",
        "text": "To support technical support teams with relevant information required to troubleshoot"
      },
      {
        "letter": "C",
        "text": "To serve as a central location for installing, exchanging, and contributing content"
      },
      {
        "letter": "D",
        "text": "To serve as a major software versioning update"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 19,
    "text": "Which sensor is used by Cortex XSIAM to identify and collect DNS queries, HTTP headers, and DHCP information? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Enhanced Application Logs"
      },
      {
        "letter": "B",
        "text": "Directory Sync logs"
      },
      {
        "letter": "C",
        "text": "Windows Event Collector logs"
      },
      {
        "letter": "D",
        "text": "Pathfinder data collector"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 20,
    "text": "What are two ways a security team assigns priority to security incidents in Cortex XDR? (Choose two answers)",
    "choices": [
      {
        "letter": "A",
        "text": "By highest SmartScore"
      },
      {
        "letter": "B",
        "text": "By most recently generated"
      },
      {
        "letter": "C",
        "text": "By most incident artifacts"
      },
      {
        "letter": "D",
        "text": "By highest severity"
      }
    ],
    "answer": "AD",
    "type": "multi"
  },
  {
    "num": 21,
    "text": "What is the purpose of incident types in Cortex XSOAR? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "They manually create incidents, configure universal playbooks, and enforce strict adherence to preset service-level agreement (SLA) reminders."
      },
      {
        "letter": "B",
        "text": "They classify events ingested through integrations or the REST API, con trigger specific playbooks, and include customizable layouts and service-"
      },
      {
        "letter": "C",
        "text": "They assist in mapping manual incidents, assign default playbooks, and require inline auto-extraction of indicators."
      },
      {
        "letter": "D",
        "text": "They categorize manval and automated incidents, trigger playbooks automatically, and require predefined fields and integrations."
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 22,
    "text": "How is internal proprietary source code classified? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Restpcted"
      },
      {
        "letter": "B",
        "text": "Confidential"
      },
      {
        "letter": "C",
        "text": "Internal Use Only"
      },
      {
        "letter": "D",
        "text": "Private"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 23,
    "text": "A security auditor must ensure adherence to which two regulatory compliance frameworks when reviewing a financial institution's data protection policies? (Choose two answers)",
    "choices": [
      {
        "letter": "A",
        "text": "NERC CIP"
      },
      {
        "letter": "B",
        "text": "FERPA"
      },
      {
        "letter": "C",
        "text": "GDPR"
      },
      {
        "letter": "D",
        "text": "PCI OSS"
      }
    ],
    "answer": "CD",
    "type": "multi"
  },
  {
    "num": 24,
    "text": "Which two roles can access data model rules in Cortex XSIAM? (Choose two answers)",
    "choices": [
      {
        "letter": "A",
        "text": "IT administrator"
      },
      {
        "letter": "B",
        "text": "Account admin"
      },
      {
        "letter": "C",
        "text": "Deployment admin"
      },
      {
        "letter": "D",
        "text": "Instance administrator"
      }
    ],
    "answer": "BD",
    "type": "multi"
  },
  {
    "num": 25,
    "text": "Which tool enables a company to discover and understand the risk and exposure of company assets? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Security Information and Event Management (SIEM)"
      },
      {
        "letter": "B",
        "text": "Vulnerability management solution"
      },
      {
        "letter": "C",
        "text": "Endpoint detection and response (EDR)"
      },
      {
        "letter": "D",
        "text": "Security orchestration, automation, and response (SOAR)"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 26,
    "text": "What is the most operationally efficient way in Cortex XDR to prevent unauthorized USB access to a phone or mobile device on a Windows machine? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Create a \"disk drive restrictions” device configuration profile."
      },
      {
        "letter": "B",
        "text": "Create a “Windows portable devices” device configuration profile."
      },
      {
        "letter": "C",
        "text": "Create a new \"device identifier exceptions\" profile."
      },
      {
        "letter": "D",
        "text": "Create a behavioral indicator of compromise (BIOC) for device plugin detection."
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 27,
    "text": "What is a primary responsibility of an incident responder in o securily operations center (SOC)? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Supervising vulnerability assessments and penetration tests"
      },
      {
        "letter": "B",
        "text": "Mitigating incidents thal have been escalated"
      },
      {
        "letter": "C",
        "text": "Determining or adjusting criticality of clerts"
      },
      {
        "letter": "D",
        "text": "Developing incident recovery crisis communications plans"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 28,
    "text": "Which component of Cortex XDR is designed to detect insider threats? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Forensics"
      },
      {
        "letter": "B",
        "text": "Cloud Identity Engine"
      },
      {
        "letter": "C",
        "text": "ldentity Analytics"
      },
      {
        "letter": "D",
        "text": "Host Insights"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 29,
    "text": "What is the main difference between artificial intelligence (Al) and machine learning (ML) in cybersecurity? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "MLis a broader discipline that includes Al, which focuses solely on natural language processing."
      },
      {
        "letter": "B",
        "text": "Al is used for automating responses, while ML manages hardware and network infrastructure."
      },
      {
        "letter": "C",
        "text": "ML enables machines to learn fram data, while Al enables machines to mimic human cognitive functions."
      },
      {
        "letter": "D",
        "text": "Al and ML are interchangeable terms that refer to preprogrammed rules which can detect threats."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 30,
    "text": "During a sophisticated cyber attack, a company experiences a mulfivector intrusion that evades detection by traditional security tools.\nThe company requires a solution that will correlate and analyze the disparate attack indicators across its network, endpoints, and cloud environments to uncover the full scope of the breach and take immediate automated response actions.\nWhich solution should be recommended? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "SIEM"
      },
      {
        "letter": "B",
        "text": "XDR"
      },
      {
        "letter": "C",
        "text": "EDR"
      },
      {
        "letter": "D",
        "text": "XSOAR"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 31,
    "text": "How can an administrator run a Cortex XSOAR playbook regularly at a specific time and day of the week? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "By creating o script that will run the playbook"
      },
      {
        "letter": "B",
        "text": "By configuring the playbook to run ona specific date and time"
      },
      {
        "letter": "C",
        "text": "By creating a scheduled reportethet will run the playbook"
      },
      {
        "letter": "D",
        "text": "By creating a job that will run the playbook"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 32,
    "text": "Which artifacts should be collected and analyzed during a forensic investigation following a security operations center (SOC) breach due toa phishing attack? (Choose one answer) e A Proxy logs, URL Logs, cloud audit Logs",
    "choices": [
      {
        "letter": "B",
        "text": "IOC logs, BIOC logs, behavior analytics"
      },
      {
        "letter": "C",
        "text": "Network traffic logs. event logs, email artifacts"
      },
      {
        "letter": "D",
        "text": "SQL injection Logs, orute force attack logs, Mimikatz artifacts"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 33,
    "text": "Which predefined dashboard will provide information regarding the status of deployed endpoints? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Agent Management"
      },
      {
        "letter": "B",
        "text": "Security Administration"
      },
      {
        "letter": "C",
        "text": "Data Ingestion"
      },
      {
        "letter": "D",
        "text": "Incident Management"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 34,
    "text": "Which function eliminates the need for manual analysis in an organization with multiple data sensors? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Eventlog query"
      },
      {
        "letter": "B",
        "text": "Log stitching"
      },
      {
        "letter": "C",
        "text": "Log correlation"
      },
      {
        "letter": "D",
        "text": "Log forwarding"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 35,
    "text": "What is involved in the day-to-day role of a triage specialist? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Managing procurement of IT hardware and software"
      },
      {
        "letter": "B",
        "text": "Managing and configuring the monitoring tools"
      },
      {
        "letter": "C",
        "text": "Deploying and configuring security technologies"
      },
      {
        "letter": "D",
        "text": "Conducting vulnerability assessment and penetration testing"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 36,
    "text": "Which component of Cortex XDR would allow an analyst to determine if suspicious user activity deviates from normal user activity? (Choose one answer) @ A.\\dentity Analytics",
    "choices": [
      {
        "letter": "A",
        "text": "\\dentity Analytics"
      },
      {
        "letter": "B",
        "text": "Behavioral Threat Protection (BTP)"
      },
      {
        "letter": "C",
        "text": "Network troffic analysis"
      },
      {
        "letter": "D",
        "text": "Host Insights"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 37,
    "text": "Which two functions are available when stitching logs in Cortex XDR? (Choose two answers)",
    "choices": [
      {
        "letter": "A",
        "text": "Providing real-time threat prevention or remediation of threats"
      },
      {
        "letter": "B",
        "text": "Creating granular BIOC and correlation rules"
      },
      {
        "letter": "C",
        "text": "Running investigation queries based on combined network and endpoint events"
      },
      {
        "letter": "D",
        "text": "Enabling creation of custom scripts for remediation of security incidents"
      }
    ],
    "answer": "BC",
    "type": "multi"
  },
  {
    "num": 38,
    "text": "What are two outcomes of threat intelligence in a SOC? (Choose two answers)",
    "choices": [
      {
        "letter": "A",
        "text": "Identification and detection of known threat verdicts to improve company security posture"
      },
      {
        "letter": "B",
        "text": "Enablement of security operations teams to reduce workload through automation"
      },
      {
        "letter": "C",
        "text": "Reduction of the number of alerts observed in an incident"
      },
      {
        "letter": "D",
        "text": "Mitigation of potential risks to systems and data"
      }
    ],
    "answer": "AD",
    "type": "multi"
  },
  {
    "num": 39,
    "text": "Which Cortex XDR component raises an alert when suspicious activity composed of multiple events is detected and deviates from established baseline behavior? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Causality Analysis Engine"
      },
      {
        "letter": "B",
        "text": "Analytics Engine"
      },
      {
        "letter": "C",
        "text": "Cloud Identity Engine"
      },
      {
        "letter": "D",
        "text": "XOL Query Engine"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 40,
    "text": "Which incident should a responder prioritize based on overall functional and informational impact to the company? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "A public-facing web server has multiple failed login attempts over a short period of time."
      },
      {
        "letter": "B",
        "text": "A user in the accounting department receives a pop-up message after visiting a website."
      },
      {
        "letter": "C",
        "text": "4 large upload of user dota from an internal file server to a public website occurs."
      },
      {
        "letter": "D",
        "text": "An external-facing company weossite is currently unavailable."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 41,
    "text": "An incident responder is accessing a workstation through the Live Terminal feature in Cortex XSIAM. The responder wants to download a file for analysis, but notices the text on the download option is greyed out.\nWhat would cause this? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "The file exceeds the maximum download size limit."
      },
      {
        "letter": "B",
        "text": "There are insufficient privileges to download the file."
      },
      {
        "letter": "C",
        "text": "The file extension type is not allowable for download"
      },
      {
        "letter": "D",
        "text": "The file has been deleted and is no longer available."
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 42,
    "text": "What will enable ingestion of on-premises firewall logs into Cortex XDR? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "PAN-OS content pack"
      },
      {
        "letter": "B",
        "text": "API"
      },
      {
        "letter": "C",
        "text": "Cloud Identity Engine"
      },
      {
        "letter": "D",
        "text": "Broker VM"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 43,
    "text": "Which built-in report template is used to schedule a report showing the average mean time to resolution (MTTR) for the week? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "\\Incident Management Report"
      },
      {
        "letter": "B",
        "text": "Incident Response Report"
      },
      {
        "letter": "C",
        "text": "Security Manager Report"
      },
      {
        "letter": "D",
        "text": "Security Admin Report"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 44,
    "text": "Which two steps belong in the Cortex XSOAR incident lifecycle? (Choose two answers)",
    "choices": [
      {
        "letter": "A",
        "text": "Preparation"
      },
      {
        "letter": "B",
        "text": "Planning"
      },
      {
        "letter": "C",
        "text": "Incident notification"
      },
      {
        "letter": "D",
        "text": "Incident creation"
      }
    ],
    "answer": "AD",
    "type": "multi"
  },
  {
    "num": 45,
    "text": "Which predefined role in the Cortex XDR tenant can view and triage incidents? (Choose one answer) @ A.IT administrator",
    "choices": [
      {
        "letter": "A",
        "text": "IT administrator"
      },
      {
        "letter": "B",
        "text": "Investigator"
      },
      {
        "letter": "C",
        "text": "Responder"
      },
      {
        "letter": "D",
        "text": "Viewer"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 46,
    "text": "Which task should a threat hunter include in the investigation when a Cortex XDR incident contains alerts about a malicious process? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Disable the account of the user responsible for initiating the process."
      },
      {
        "letter": "B",
        "text": "Immediately isolate the endpoint and delete the identified file."
      },
      {
        "letter": "C",
        "text": "Search for the SHA256 file hash on other endpoints in the environment."
      },
      {
        "letter": "D",
        "text": "Add the SHA256 file hash to the Cortex XDR global block List."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 47,
    "text": "Which response action in Cortex XSIAM would be unavailable to a SOC analyst investigating an incident involving a Linux server? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Live Terminal session initiation"
      },
      {
        "letter": "B",
        "text": "Running a script"
      },
      {
        "letter": "C",
        "text": "File search and destroy"
      },
      {
        "letter": "D",
        "text": "Halting network access"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 48,
    "text": "What is the Cortex XSOAR Marketplace? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Searchable collection of third-party playbooks and data models"
      },
      {
        "letter": "B",
        "text": "Digital storefront where Cortex XSOAR training credits can be purchased and used"
      },
      {
        "letter": "C",
        "text": "Built-in repository of installable content, including integrations and automations"
      },
      {
        "letter": "D",
        "text": "Development environment for creating and sharing third-party integrations"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 49,
    "text": "Which types of indicators are supported out-of-the-box by Cortex XSOAR? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "MAC addresses, URLs, file paths, and extended validation certificates"
      },
      {
        "letter": "B",
        "text": "IP addresses, domain names, URLs, and file hashes"
      },
      {
        "letter": "C",
        "text": "Registry keys, file paths, file hashes, and wild card certificates"
      },
      {
        "letter": "D",
        "text": "Email addresses, domain names, SSL certificates, and natural language indicators"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 50,
    "text": "A custom PowerShell command is detected by Cortex XDR as a behavioral threat, and the administrator has confirmed it as a false positive.\nWhich action will allow this command to run and not be detected by Cortex XDR? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Create an alert exclusion based on CGO hash, signer, and process path."
      },
      {
        "letter": "B",
        "text": "Add the SHA256 hash to the allow list."
      },
      {
        "letter": "C",
        "text": "Create an alert exception based on CGO process path and command arguments."
      },
      {
        "letter": "D",
        "text": "Right click on the alert and create an alert exclusion rule."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 51,
    "text": "Which action is performed as the final step of the NIST incident response plan? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Updating incident response procedures"
      },
      {
        "letter": "B",
        "text": "Gathering evidence"
      },
      {
        "letter": "C",
        "text": "Restoring from backups"
      },
      {
        "letter": "D",
        "text": "Conducting incident response training exercises"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 52,
    "text": "What is a benefit of using Unit 42 threat intelligence during a ransomware attack? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "lt provides detailed research on the ransomware, including its behavior and attack methods, to enhance the response strategy."
      },
      {
        "letter": "B",
        "text": "It creates compliance reports to confirm that the company meets regulatory requirements following the ransomware attack."
      },
      {
        "letter": "C",
        "text": "It offers real-time network traffic analysis to detect and block ransomware spread in the company network,"
      },
      {
        "letter": "D",
        "text": "It manually configures security agents across all company endpoints to ensure the ransomware has been * effectively contained."
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 53,
    "text": "A file hash is evaluated in Cortex XSOAR by using two unique threat feeds:\n* VirusTotal feed (rating of B - usually reliable) and the file verdict is malicious * AlienVault feed (rating of B - usually reliable) and the file verdict is benign What is the overall file verdict? {Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Benign"
      },
      {
        "letter": "B",
        "text": "Malicious"
      },
      {
        "letter": "C",
        "text": "Suspicious"
      },
      {
        "letter": "D",
        "text": "Unknown"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 54,
    "text": "Which MITRE enterprise tactic will provide more information on the technique used by a threat actor who has successfully used PsExec to upload files to an internal server from a compromised workstation? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Lateral movement"
      },
      {
        "letter": "B",
        "text": "Persistence"
      },
      {
        "letter": "C",
        "text": "Execution"
      },
      {
        "letter": "D",
        "text": "Privilege escalation"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 55,
    "text": "In which scenario would an organization benefit from Cortex KDR compared to an EDR solution? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "A business wants fo intecrote data from network traffic, cloud environments, and identity systems for a unified threat landscape."
      },
      {
        "letter": "B",
        "text": "A corporation wants to monitor endpaint activities for advanced threats and gain visibility into endpoint behaviors."
      },
      {
        "letter": "D",
        "text": "A company requires endpoint security that focuses on isolating and responding to threats at the endpoint «» level."
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 56,
    "text": "Which solution will minimize mean time to resolution (MTTR) when, as c result of previous malware infection. a company's Windows endpoint is suffering a small amount of file corruption and modified registry keys? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Use remediation suggestions to restore the affected files and registry modifications."
      },
      {
        "letter": "B",
        "text": "Use Live Terminal fo connect to the machine and upload files to replace the corrupted files."
      },
      {
        "letter": "C",
        "text": "Issue a new laptop from the help desk to expedite a clean system."
      },
      {
        "letter": "D",
        "text": "Configure group policy objects to push new files and registry key changes to the endpoint."
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 57,
    "text": "Which two types of content can be installed or upgraded through a Cortex XSIAM content pack? (Choose two answers)",
    "choices": [
      {
        "letter": "A",
        "text": "Playbook triggers"
      },
      {
        "letter": "B",
        "text": "Behavioral Threat Protection (BTP)"
      },
      {
        "letter": "C",
        "text": "Data Model rules"
      },
      {
        "letter": "D",
        "text": "Analytics alerts"
      }
    ],
    "answer": "CD",
    "type": "multi"
  },
  {
    "num": 58,
    "text": "What is the most operationally efficient tool for detection of events related to abuse of authorized access and malicious insider activity across endpoints, network, identity, and the cloud? (Choose one answer) @ A.User and Entity Behavior Analytics (UEBA) @ B.Honeypots or decoy servers",
    "choices": [
      {
        "letter": "A",
        "text": "User and Entity Behavior Analytics (UEBA)"
      },
      {
        "letter": "B",
        "text": "Honeypots or decoy servers"
      },
      {
        "letter": "C",
        "text": "Correlation rules"
      },
      {
        "letter": "D",
        "text": "Network traffic analysis"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 59,
    "text": "What are the primary functions of the Causality Analysis Engine in Cortex XDR? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "To determine only the root cause of an attack and automatically remediate threats"
      },
      {
        "letter": "B",
        "text": "To prioritize critical alerts and reduce the overall number of alerts generated"
      },
      {
        "letter": "C",
        "text": "To identify the root cause of alerts and provide a complete forensic timeline of events"
      },
      {
        "letter": "D",
        "text": "To perform regular system backups and restore operations in case of failure"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 60,
    "text": "How do sensors function in Cortex XSIAM? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "They assist with log stitching."
      },
      {
        "letter": "B",
        "text": "They monitor endpoint agent health."
      },
      {
        "letter": "C",
        "text": "They collect logs and telemetry data."
      },
      {
        "letter": "D",
        "text": "They monitor data ingestion health."
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 61,
    "text": "The same IP address was fetched from two different threat intelligence feeds in Cortex KSOAR. The first integration returns o verdict of Suspicious with an A (very reliable) confidence rating. while the second integration returns a verdict of Benign also with an A (very reliable) confidence rating.\nWhat is the final indicator verdict assigned to the !P address? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Unknown"
      },
      {
        "letter": "B",
        "text": "Bonign"
      },
      {
        "letter": "C",
        "text": "Suspicious"
      },
      {
        "letter": "D",
        "text": "Malicious"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 62,
    "text": "An administrator has configured Cortex XDR to ingest logs from third party firewalls and is using Cortex XDR agents on endpoints. The goal is to see network connections from the firewalls correlated with the endpoint processes that initiated them.\nWhich feature handles this correlation ta form network stories? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Identity Analytics"
      },
      {
        "letter": "B",
        "text": "Pathfinder"
      },
      {
        "letter": "C",
        "text": "Log stitching"
      },
      {
        "letter": "D",
        "text": "Correlation rules"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 63,
    "text": "Which Cortex XSOAR feature will execute a specific integration command to enrich an IP address without leaving the incident view, while also ensuring this action is recorded in the incident's history? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "War Room"
      },
      {
        "letter": "B",
        "text": "Work plan"
      },
      {
        "letter": "C",
        "text": "Playground"
      },
      {
        "letter": "D",
        "text": "Evidence board"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 64,
    "text": "An automation engineer is using Cortex XSIAM playbooks to create modular. readable, and structured security workflows. The engineer requires a methad to clearly delineate the Engagement, Triage, and Containment phases by introducing visual grouping mechanisms into the playbook canves.\nWhich playbook element is designed to organize the workflow in this scenario? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Task from the artifacts library"
      },
      {
        "letter": "B",
        "text": "Script with a “Print” command"
      },
      {
        "letter": "C",
        "text": "Standard task with a “Manual” input"
      },
      {
        "letter": "D",
        "text": "Section header"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 65,
    "text": "Which action is the responsibility of the security operations center (SOC) manager? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Developing and implementing crisis communication plans"
      },
      {
        "letter": "B",
        "text": "Handling direct end-user support or help desk issues"
      },
      {
        "letter": "C",
        "text": "Troubleshooting network cabling and physical installation"
      },
      {
        "letter": "D",
        "text": "Performing initial triage and classification of incidents"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 66,
    "text": "A security architect is designing a new incident response workflow that requires a specific playbook to be executed every Saturday at 1:00 AM to perform weekly archival and cleanup tasks. This process must be reliably scheduled within Cortex XSOAR.\nWhat should the architect use to ensure the playbook runs automatically per the specifications? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Playbook pre-execution hook that is set with a time-based trigger"
      },
      {
        "letter": "B",
        "text": "External cron job that uses the Cortex XSOAR API to start the playbook"
      },
      {
        "letter": "C",
        "text": "Scheduled report configured to invoke a command for the playbook"
      },
      {
        "letter": "D",
        "text": "Job that initiates the playbook at the designated time"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 67,
    "text": "An organization requires o security solution that offers comprehensive threat visibility across their entire digital ecosystem, including firewalls, cloud environments, and user authentication logs, not just endpoint data.\nWhich Palo Alto Networks solution is best suited to meet this extended requirement? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Cortex endpaint protection platform (EPP)"
      },
      {
        "letter": "B",
        "text": "Cortex XDR"
      },
      {
        "letter": "C",
        "text": "Cortex Cloud Identity Engine"
      },
      {
        "letter": "D",
        "text": "Cortex XSIAM"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 68,
    "text": "What is the primary goal of the Post-Incident Activity phase in the NIST Incident Response Plan? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Initiating automated or manual remediation actions on all affected hosts"
      },
      {
        "letter": "B",
        "text": "Categorizing and prioritizing the incident severity using the scoring system"
      },
      {
        "letter": "C",
        "text": "Conducting o Lessons learned meeting with all involved parties"
      },
      {
        "letter": "D",
        "text": "Determining the roct cause of the breach and patch the vulnerability"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 69,
    "text": "An analyst observes a threat actor using the remote desktop protocol (RDP) to interactively log on to a domain controller using credentials stolen from a compromised workstation.\nWhich MITRE enterprise tactic includes this technique? (Choose one onswer)",
    "choices": [
      {
        "letter": "A",
        "text": "Lateral Movement"
      },
      {
        "letter": "B",
        "text": "Collection"
      },
      {
        "letter": "C",
        "text": "Command and Control"
      },
      {
        "letter": "D",
        "text": "Defense Evasion"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 70,
    "text": "What is a key benefit of data protection? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Improving accessibility to data"
      },
      {
        "letter": "B",
        "text": "Streamlining data onboarding process"
      },
      {
        "letter": "C",
        "text": "Streamlining business processes"
      },
      {
        "letter": "D",
        "text": "Abiding by compliance regulations"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 71,
    "text": "Acustom script activity, previously categorized as non-malicious, suddenly begins executing a series of unusual file operations and network connections. Cortex XDR detects this change, aggregates the sequence of abnormal events, and immediately raises a high-severity alert.\nWhich Cortex XDR capability uses statistical baselining and machine learning to specifically identify this type of activity? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Causolity View"
      },
      {
        "letter": "B",
        "text": "Incident Management Engine"
      },
      {
        "letter": "C",
        "text": "Threat Hunting Engine"
      },
      {
        "letter": "D",
        "text": "Analytics Engine"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 72,
    "text": "An analyst ts investigating a critical incident on a Windows server in which a malware execution led to numerous file deletions and registry key changes. The offected files and registry keys need to be restored efficiently and quickly.\nWhich Cortex XDR response action should the analyst select? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Execute the Isolate Endpoint action, which automatically reverses all known malwoare-related changes upon successful isolation."
      },
      {
        "letter": "B",
        "text": "Run the Search and Destroy action on all affected endpoints to automatically replace all files with a \"good\" hash from the content update package."
      },
      {
        "letter": "C",
        "text": "Initiate a Live Terminal session and use operating system commands to manvally copy original files from a network share and import a clean"
      },
      {
        "letter": "D",
        "text": "Use the Remediation Suggestions action to reviow and apply the recommended actions for restoring the files and registry values."
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 73,
    "text": "What would an account administrator configure when allowing Cortex XDR user access to only a specific endpoint group? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Identity provider (IdP) account placed In the appropriate group"
      },
      {
        "letter": "B",
        "text": "Role-Based Access Control (RBAC) with a predefined role"
      },
      {
        "letter": "C",
        "text": "Custom Support Portal account with the appropriate role"
      },
      {
        "letter": "D",
        "text": "Scope-Based Access Control (SBAC) with specific tags"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 74,
    "text": "An analyst is investigating a complex sequence of malicious activities in Cortex XDR and needs a single, consolidated view of all related processes, network connections, and file changes that resulted in a security alert.\nWhich component of Cortex KDR performs the required data correlation to generate the view? {Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Analytics Engine for anomaly detection"
      },
      {
        "letter": "B",
        "text": "Behavioral Threat Protection (BIP) module"
      },
      {
        "letter": "C",
        "text": "Strata Logging Service Gata aggregation layer"
      },
      {
        "letter": "D",
        "text": "Causality Analysis Engine"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 75,
    "text": "In Cortex XSOAR, which key function is fulfilled by content packs, distinguishing them from individual content items like scripts or playbooks?\n(Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Executing integration commands in a remote network seqment"
      },
      {
        "letter": "B",
        "text": "Bundling related security content for versioning, distribution, and installation of specific use cases"
      },
      {
        "letter": "C",
        "text": "Serving as the core Logging and auditing mechanism for all incident activities"
      },
      {
        "letter": "D",
        "text": "Being a requirement for enabling high availability (HA) and disaster recovery across multiple servers"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 76,
    "text": "Which statement accurately describes the relationship and primary difference between Al and machine Learning (ML) in cybersecurity? (Choose one answer) e 4.Alisa subfield of ML that specifically handles data Labeling and feature engineering for deep learning algorithms.",
    "choices": [
      {
        "letter": "A",
        "text": "Alisa subfield of ML that specifically handles data Labeling and feature engineering for deep learning algorithms."
      },
      {
        "letter": "B",
        "text": "ML focuses on structured, high-volume data processing, whereas Al is dedicated to unstructured data, such as security Logs and threat intelligence"
      },
      {
        "letter": "C",
        "text": "Al refers to the historical approach of using predefined, signature-based rules, while ML represents the mocern shift toward unsupervised anomaly"
      },
      {
        "letter": "D",
        "text": "Alis the science of simuloting human intelligence, whereas ML allows a system to learn and improve from experience without programming."
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 77,
    "text": "An incident in Cortex XSIAM displays alerts for \"Lsass Memory Dump\" originating from a process named proc_dump.exe.\nThe process is unsigned, has an unknown reputation. and was launched from a temporary directory.\nWhich initial verdict applies to this incident? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "True positive"
      },
      {
        "letter": "B",
        "text": "False negative"
      },
      {
        "letter": "C",
        "text": "True negative"
      },
      {
        "letter": "D",
        "text": "False positive"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 78,
    "text": "Asecurity analyst is reviewing o comprehensive list of newly ingested indicators of compromise (IOCs) from various threat intelligence feeds in Cortex XSOAR. The analyst needs to quickly filter and sort the |OCs to determine which ones pose the grectest immediate risk to the organization, regardless of their source.\nWhich indicator attribute in Cortex KSOAR is the most direct and efficient mechanism for this prioritization task? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Indicator Verdict"
      },
      {
        "letter": "B",
        "text": "Source Reliabiliry Score"
      },
      {
        "letter": "C",
        "text": "Traffic Light Protocol (TLP) Label"
      },
      {
        "letter": "D",
        "text": "Indicator Expiration Status"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 79,
    "text": "An organization requires o specific user to have the ability to investigate alerts and perform remediation tasks, such as terminating molicious processes and isolating compromised hosts, without having full administrative control over the tenant settings.\nWhich predefined role should be assigned to this user in Cortex XDR? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Viewer"
      },
      {
        "letter": "B",
        "text": "Investigator"
      },
      {
        "letter": "C",
        "text": "Deployment Admin"
      },
      {
        "letter": "D",
        "text": "Responder"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 80,
    "text": "A security operations center (SOC) anolyst is reviewing the current queve of incidents in the Cortex XDR console. The goal is to prioritize a new threat that signifies a confirmed, deep-seated persistent compromise and represents the greatest risk of immediate, irreparable damage to core network assets.\nWhich incident should the analyst prioritize for immediate containment and remediation? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "The nightly data integrity check failed for the main customer billing database, reporting corrupt indices due to an unknown database process."
      },
      {
        "letter": "B",
        "text": "A third-party security scanner reports an unpatched critical vuinerability with a Common Vulnerability Scoring System (CVSS) score of 9.8 ona"
      },
      {
        "letter": "C",
        "text": "An unknown internal host is communicating with a known command-and-control (c2) server over o non-standard port after a successful Lateral"
      },
      {
        "letter": "D",
        "text": "Aspike of 1500 blocked email messages containing commen phishing URLs was recorded in the last hour, and no users can be detected as having"
      }
    ],
    "answer": "C",
    "type": "single"
  },
  {
    "num": 81,
    "text": "An organization ingests security data from dozens of different sensors. including endpoint agents and network firewalls. These low-fidelity events from all the sources need to become part of a cohesive narrative for a security incident.\nWhich specific automated function performs this task? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Log correlation"
      },
      {
        "letter": "B",
        "text": "Event forwarding"
      },
      {
        "letter": "C",
        "text": "Incident management"
      },
      {
        "letter": "D",
        "text": "Log stitching"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 82,
    "text": "Which security operations center (SOC) role investigates a new low severity alert? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "SOC manager"
      },
      {
        "letter": "B",
        "text": "Threct hunter"
      },
      {
        "letter": "C",
        "text": "Incident responder"
      },
      {
        "letter": "D",
        "text": "Triage specialist"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 83,
    "text": "What will consolidate the final verdict and o detailed trace of the file's behavior when an artifact's hash is automatically submitted to Palo Alto Networks cloud-based service for static and dynamic onalysis? (Choose one answer) @ A. SmartScore incident page e 6. External threat feed indicator",
    "choices": [
      {
        "letter": "A",
        "text": "SmartScore incident page"
      },
      {
        "letter": "B",
        "text": "External threat feed indicator"
      },
      {
        "letter": "C",
        "text": "Cortex XDR artifact summary"
      },
      {
        "letter": "D",
        "text": "WildFire analysis report"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 84,
    "text": "Asecurity analyst is tuning Cortex XDR after a custom application, which uses the mshtc.exe utility with a legitimate internal script, triggers a behavioral threat alert. The administrator must ensure the legitimate script runs without detection.\nWhich set of criteria must be included in the new exception rule to prevent future false positives while maintaining protection against similar malicious activity? (Choose one answer) @ A. Exception based on the process path and script command-line crguments @ B. File name hash (SHA256) of the mshta.exe file",
    "choices": [
      {
        "letter": "A",
        "text": "Exception based on the process path and script command-line crguments"
      },
      {
        "letter": "B",
        "text": "File name hash (SHA256) of the mshta.exe file"
      },
      {
        "letter": "C",
        "text": "Signature signer of the mshta.exe binary"
      },
      {
        "letter": "D",
        "text": "Alert exclusion that is based on the name of the threat"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 85,
    "text": "Which identity security component is best suited to detect lateral movement within a compromised service account? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Identity Analytics"
      },
      {
        "letter": "B",
        "text": "Analytics behavioral indicator of compromise {ABIOC) feature"
      },
      {
        "letter": "C",
        "text": "Cortex XSOAR"
      },
      {
        "letter": "D",
        "text": "Cortex Identity Threat Detection and Response (ITDR) madule"
      }
    ],
    "answer": "D",
    "type": "single"
  },
  {
    "num": 86,
    "text": "Which query Language will perform a deep investigation into a series of potential endpoint attacks by searching across all collected event data using Cortex XDR Query Builder? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "XQL"
      },
      {
        "letter": "B",
        "text": "SOL"
      },
      {
        "letter": "C",
        "text": "KQL"
      },
      {
        "letter": "D",
        "text": "SPL"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 87,
    "text": "Which Cortex XSOAR capability provides sourcing, download, and management of curated collections of security orchestration content? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Deployment Wizard"
      },
      {
        "letter": "B",
        "text": "Cortex Marketplace"
      },
      {
        "letter": "C",
        "text": "Content contribution interface"
      },
      {
        "letter": "D",
        "text": "Content version control"
      }
    ],
    "answer": "B",
    "type": "single"
  },
  {
    "num": 88,
    "text": "Which attribute applies to script creation in Cortex XSOAR? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Can be scheduled to run at a later time and day"
      },
      {
        "letter": "B",
        "text": "Can be executed only with Limited permissions"
      },
      {
        "letter": "C",
        "text": "Can be written using XQL"
      },
      {
        "letter": "D",
        "text": "Can be protected with a password"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 89,
    "text": "Which component of Cortex XSIAM maps events ingested from third-party sources to a standardized format? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Data model"
      },
      {
        "letter": "B",
        "text": "Broker VM"
      },
      {
        "letter": "C",
        "text": "Parsing rules"
      },
      {
        "letter": "D",
        "text": "XDR Collector"
      }
    ],
    "answer": "A",
    "type": "single"
  },
  {
    "num": 90,
    "text": "Where can an analyst look to determine the root cause of a causality chain? (Choose one answer)",
    "choices": [
      {
        "letter": "A",
        "text": "Root cause analysis"
      },
      {
        "letter": "B",
        "text": "Causality Group Owner (CGO)"
      },
      {
        "letter": "C",
        "text": "Behavioral indicators of compromise (BIOCs)"
      },
      {
        "letter": "D",
        "text": "Indicators of compromise [10Cs)"
      }
    ],
    "answer": "B",
    "type": "single"
  }
];
