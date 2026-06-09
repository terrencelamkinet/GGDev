Feature Checklist -> Test Case Mapping
========================================
Fubon Kong API Gateway PoC
Reference: API_standard_features_checklist.xlsx
====================================================================

1. SECURITY
====================================================================
Checklist Item                          Test Case(s)                  Coverage
─────────────────────────────────────  ────────────────────────────  ────────
OAuth2 / OIDC Support                  Case_5 (JWT validation)       ✅ Partial
JWT Validation                         Case_5                        ✅ Full
Scope Enforcement                      Case_5 (claims check)        ✅ Partial
mTLS Support                           Case_6                        ✅ Full
WAF Integration                        —                             ❌ Not in scope
DDoS Protection                        Case_8 (rate limiting)       ✅ Partial
IP Whitelisting                        Case_7                        ✅ Full

2. AUTHORIZATION & POLICY
====================================================================
Claim-based Routing                    —                             ❌ Not covered
Fine-grained Policy (ABAC/RBAC)        —                             ❌ Not covered
External Policy Engine (OPA/PDP)       —                             ❌ Not covered
Policy Versioning                      Case_19 (decK)               ✅ Partial
Policy Audit Trail                     Case_12 (access log)         ✅ Partial
Context-based Decision                 —                             ❌ Not covered
Deny-by-default                        Case_2 (default route)       ✅ Partial

3. TRAFFIC MANAGEMENT & PROTECTION
====================================================================
Rate Limiting                          Case_8, Case_9               ✅ Full
Throttling                             Case_8 (burst vs sustained)  ✅ Partial
Quota Management                       —                             ❌ Not covered
Spike Arrest                           —                             ❌ Not covered
Backend Retry                          —                             ❌ Not covered
Circuit Breaker                        Case_10                       ✅ Full
Caching                                —                             ❌ Not covered

4. INTEGRATION
====================================================================
REST Support                           Case_2 (basic proxy)          ✅ Full
SOAP Support                           —                             ❌ Not covered
gRPC Support                           —                             ❌ Not covered
Message Queue (Kafka/MQ)               —                             ❌ Not covered
Transformation (JSON/XML)              Case_11 (header transform)   ✅ Partial
Backend Protocol (HTTP/HTTPS/TCP)      Case_2, Case_15              ✅ Partial

5. OBSERVABILITY
====================================================================
Access Logging                         Case_12                       ✅ Full
Audit Trail (config changes)           Case_12, Case_19             ✅ Partial
Correlation ID                         —                             ❌ Not covered
Metrics (Prometheus)                   Case_13                       ✅ Full
SIEM Integration (Splunk/ELK)          Case_12 (log forwarding)     ✅ Partial
Alerting                               —                             ❌ Not covered

6. DEVOPS & API LIFECYCLE
====================================================================
CI/CD Integration (GitOps)             Case_19 (decK)               ✅ Partial
Config as Code (declarative YAML)      Case_19                       ✅ Full
Environment Promotion                  —                             ❌ Not covered
Version Control (API versioning)       —                             ❌ Not covered
Rollback                               Case_20 (validation)         ✅ Partial
Blue/Green Deployment                  Case_21 (zero-downtime)      ✅ Partial

7. DEV PORTAL
====================================================================
API Portal (self-service)              —                             ❌ Not covered
API Documentation (Swagger/OpenAPI)    —                             ❌ Not covered
API Testing Console                    —                             ❌ Not covered
SDK Generation                         —                             ❌ Not covered
Subscription Mgmt (API key request)    —                             ❌ Not covered

8. DEPLOYMENT & ARCHITECTURE
====================================================================
HA Support (active-active)             Case_17 (load balancing)     ✅ Partial
Multi-Region DR                        —                             ❌ Not covered
Container Support (K8s)                Environment (CP/DP on K8s)   ✅ Assumed
Hybrid Deployment (on-prem + cloud)    —                             ❌ Not covered
Latency Performance                    Case_22                       ✅ Full

====================================================================
COVERAGE SUMMARY
====================================================================
Total checklist items: 44
  ✅ Fully covered:  12  (27%)
  ✅ Partial:        12  (27%)
  ❌ Not covered:    20  (46%)

PoC Phase 1 focus (must do):          Security + Traffic Management
Phase 2 (should do):                  Observability + Integration
Phase 3 (future/devops):              Authorization, Dev Portal, HA

Notes:
  - Dev Portal items are typically not in PoC scope
  - Policy engine (OPA) may be assessed separately
  - Recommend flagging gaps during POC Review meeting
