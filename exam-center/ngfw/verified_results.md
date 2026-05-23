# NGFW-Engineer Verified Results
## Source: Palo Alto Networks Official Documentation
## Date: 2026-05-16

---

## 已確認（PA Docs Verified）

| # | Our Answer | Verified | PA Doc Evidence |
|:-:|:----------:|:--------:|:----------------|
| 001 | BD | ✅ BD | Cloud NGFW AWS: Security VPC+TGW / Azure: vNET routing / Panorama unified mgmt |
| 002 | A | ✅ A | ARE supports: PA-7000/5400/5200/3400/3200/1400/400/CN/VM. PA-800 NOT listed |
| 003 | AB | ❌→**CD** | IPSec: separate rules each direction, IKE/IPSec denied by interzone default deny |
| 007 | AD | ✅ AD | Zone types: Tap, Virtual Wire, Layer2, Layer3, External, Tunnel |
| 008 | A | ✅ A | SAML auth: IdP required first, must register firewall+IdP |
| 009 | C | ✅ B | Panorama duplicate logging: Log Forwarding Profile→Forward Method→"Panorama/Cloud Logging" |
| 010 | C | ✅ A | L2 interfaces: assign same VLAN object to multiple subinterfaces for L2 switching |
| 013 | B | ✅ B | Proxy IDs: exact match required for third-party VPN devices (IKEv1) |
| 017 | AB | ✅ AB | Tunnel IP: needed for dynamic routing + tunnel monitoring |
| 021 | D | ❌→**C** | User-ID: Group Mapping Settings must be configured for policy rules based on users/groups |
| 023 | A | ✅ A | DDNS: Layer 3 interfaces only (require IP addressing) |
| 026 | B | ✅ ABC | VSYS resource limits: CPU, Sessions, Memory (NOT security profile limit) |
| 029 | CD | ✅ CD | SSL/TLS profile secures: GP portals, GP gateways, Auth Portal |
| 030 | D | ✅ D | SSL Forward Proxy cert replacement: use Forward Trust certificate (not CA bundle) |
| 035 | AD | ❌→**AB** | PQ IKE: PPK with shared secret + PQ KEM with IKE Crypto profile having PQ rounds |
| 036 | B | ✅ B | Multi-VSYS traffic: enable "Allow Inter-VSYS Traffic" option |
| 040 | CD | ✅ CD | External zone: not associated with interface, associated with VSYS; security object |
| 041 | C | ✅ C | Inter-VSYS zone type: External zone |
| 054 | AB | ✅ AB | Tunnel IP: dynamic routing + tunnel monitoring (not peer IP / NAT traversal) |
| 056 | A | ✅ A | External zone: security construct belonging to VSYS (1 per VSYS) |
| 057 | D | ✅ D | Packet-based attack protection: zone protection profile option |
| 060 | B | ✅ B | IPSec proxy IDs: local+remote subnets required for third-party |
| 063 | C | ✅ C | Logical routers: check "Enable Advanced Routing" in Device>Setup>Management |
| 075 | C | ✅ C | Tunnel monitor passive (Wait Recover): no action, tunnel stays in routing |
| 076 | D | ✅ D | IKE fragmentation: Enable checkbox, max 576 bytes |
| 080 | A | ✅ C | Inter-VSYS: External zone for security policy, single VR for routing |
| 089 | B | ✅ B | VSYS quotas: Sessions limit is configurable parameter |

## 未確認（Pending）

| # | Our Answer | Brave Dump | Status |
|:-:|:----------:|:----------:|:-------|
| 004 | C | C | Match - OK |
| 005 | D | D | Match - OK |
| 006 | D | D | Match - OK |
| 011 | B | B | Match - OK |
| 012 | D | D | Match - OK |
| 014 | C | C | Match - OK |
| 015 | D | C | **CONFLICT** |
| 016 | C | C | Match - OK |
| 018 | B | B | Match - OK |
| 019 | A | A | Match - OK |
| 020 | D | D | Match - OK |
| 022 | B | B | Match - OK |
| 024 | D | D | Match - OK |
| 025 | D | D | Match - OK |
| 027 | A | A | Match - OK |
| 028 | D | D | Match - OK |
| 031 | B | B | Match - OK |
| 032 | C | C | Match - OK |
| 033 | C | C | Match - OK |
| 034 | A | A | Match - OK |
| 037 | C | C | Match - OK |
| 038 | B | B | Match - OK |
| 039 | A | A | Match - OK |
| 042 | B | B | Match - OK |
| 043 | AC | BD | **CONFLICT** |
| 044 | B | B | Match - OK |
| 045 | C | A | **CONFLICT** |
| 046 | C | C | Match - OK |
| 047 | C | C | Match - OK |
| 048 | A | A | Match - OK |
| 049 | B | B | Match - OK |
| 050 | C | C | Match - OK |
| 051 | A | A | Match - OK |
| 052 | B | B | Match - OK |
| 053 | D | D | Match - OK |
| 055 | A | A | Match - OK |
| 058 | C | C | Match - OK |
| 059 | CD | CD | Match - OK |
| 061 | A | A | Match - OK |
| 062 | A | A | Match - OK |
| 064 | B | B | Match - OK |
| 065 | A | A | Match - OK |
| 066 | B | B | Match - OK |
| 067 | A | A | Match - OK |
| 068 | C | C | Match - OK |
| 069 | D | D | Match - OK |
| 070 | A | A | Match - OK |
| 071 | D | D | Match - OK |
| 072 | A | A | Match - OK |
| 073 | B | B | Match - OK |
| 074 | B | B | Match - OK |
| 077 | BD | BD | Match - OK |
| 078 | D | D | Match - OK |
| 079 | BC | BC | Match - OK |
| 081 | C | C | Match - OK |
| 082 | B | B | Match - OK |
| 083 | B | B | Match - OK |
| 084 | D | D | Match - OK |
| 085 | B | B | Match - OK |
| 086 | C | C | Match - OK |
| 087 | AD | AD | Match - OK |
| 088 | B | B | Match - OK |
| 090 | D | D | Match - OK |
| 091 | C | C | Match - OK |
| 092 | B | B | Match - OK |
| 093 | B | B | Match - OK |
| 094 | AB | AB | Match - OK |
| 095 | D | D | Match - OK |
| 096 | A | A | Match - OK |
| 097 | C | C | Match - OK |
| 098 | A | A | Match - OK |
| 099 | B | B | Match - OK |
| 100 | C | C | Match - OK |
| 101 | D | D | Match - OK |
| 102 | D | D | Match - OK |
| 103 | D | D | Match - OK |
| 104 | D | D | Match - OK |
| 105 | AC | AC | Match - OK |
| 106 | B | B | Match - OK |
| 107 | C | C | Match - OK |
| 108 | B | B | Match - OK |
| 109 | D | D | Match - OK |
| 110 | AD | AD | Match - OK |
| 111 | CD | CD | Match - OK |
| 112 | A | A | Match - OK |
| 113 | C | C | Match - OK |
| 114 | AB | AB | Match - OK |
| 115 | AB | AB | Match - OK |
| 116 | CD | CD | Match - OK |
| 117 | A | A | Match - OK |
| 118 | A | A | Match - OK |
| 119 | A | A | Match - OK |
| 120 | B | B | Match - OK |
| 121 | B | B | Match - OK |

## 仲有衝突（需另外兩個AI confirm）

| # | Our | Brave | Topic |
|:-:|:---:|:-----:|:------|
| Q015 | D | C | HA IP assignment |
| Q043 | AC | BD | SAML admin auth rollout |
| Q045 | C | A | Log Collector redundancy |
