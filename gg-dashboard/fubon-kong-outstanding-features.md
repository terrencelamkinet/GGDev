# Outstanding Features — Not in PoC Scope

These 13 features require additional environment, third-party software, or enterprise license.
Not included in the 33 PoC test flows. Recommended for Phase 2.

## Infrastructure-dependent (needs external component)

| # | Feature | What's Needed |
|---|---|---|
| 1 | WAF Integration | ModSecurity, AWS WAF, or AI WAF solution |
| 2 | SIEM Integration (Splunk/ELK) | Splunk, ELK stack, or any syslog endpoint |
| 3 | gRPC Support | gRPC backend server on demo server |
| 4 | SOAP Support | SOAP/XML web service on demo server |
| 5 | External Policy Engine (OPA/PDP) | Open Policy Agent sidecar or PDP service |
| 6 | Message Queue (Kafka/MQ) | Kafka, RabbitMQ, or any MQ broker |

## Environment-dependent (needs additional deployment)

| # | Feature | What's Needed |
|---|---|---|
| 7 | Environment Promotion | UAT + Production Kong instances |
| 8 | Hybrid Deployment | Cloud Kong instance (AWS / DO / Konnect) |
| 9 | Multi-Region DR | Second region or data center |

## Enterprise-dependent (needs Kong Enterprise / Konnect)

| # | Feature | What's Needed |
|---|---|---|
| 10 | API Portal (Dev Portal) | Kong Enterprise or Konnect |
| 11 | API Documentation (auto-generated) | Part of Dev Portal |
| 12 | API Testing Console | Part of Dev Portal |
| 13 | SDK Generation | Part of Dev Portal |

## Summary

| Category | Count | Effort |
|---|---|---|
| Infrastructure-dependent | 6 | Medium (add backend/service) |
| Environment-dependent | 3 | High (new infra/environment) |
| Enterprise-dependent | 4 | License decision required |
| **Total** | **13** | |

## Covered in PoC (33 test flows, 38 features)

| Phase | Flows | Features Covered |
|---|---|---|
| POC-1 Architecture & Connectivity | 3 | HA Support, Container Support (K8s), REST Support, Backend Protocol |
| POC-2 Security & Authentication | 7 | API Key, JWT, OAuth2/OIDC, Scope, mTLS, IP Whitelist, Deny, CORS, Claim-based Routing |
| POC-3 Traffic Management | 7 | Rate Limit, Quota, Throttling, Spike Arrest, Circuit Breaker, Backend Retry, Caching, DDoS Protection |
| POC-4 Observability | 4 | Access Logging, Correlation ID, Prometheus Metrics, Alerting, Policy Audit Trail |
| POC-5 Routing & Integration | 5 | Path Routing, Host Routing, Transformation, Backend Protocol (HTTPS/TCP), API Versioning |
| POC-6 DevOps & Configuration | 2 | Config as Code, CI/CD, Policy Versioning, Rollback, Blue/Green Deployment |
| POC-7 Advanced Features | 3 | Claim-based Routing, ABAC/RBAC, Context-based Decision |
| POC-9 Performance | 2 | Latency Benchmark, Throughput Test |
