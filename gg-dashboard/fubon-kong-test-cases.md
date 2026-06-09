Fubon Kong API Gateway PoC — Functional Test Cases v1
========================================================
Environment:
  CP (Control Plane): K8s
  DP (Data Plane):    K8s
  Database:           PostgreSQL on VM
  Workstation:        Postman/curl → DP
  Demo Server:        Backend API for test routing

Traffic Flow:  Workstation → Kong DP → Demo Server
====================================================================

====================================================================
POC-1: ARCHITECTURE & CONNECTIVITY
====================================================================

Case_1 | CP Admin API Access
────────────────────────────────────────────────────────────────────
Description:  Verify Kong CP Admin API is accessible and secured
Test steps:   1. From workstation, hit CP Admin API endpoint
              2. Verify authentication is required
              3. Verify only internal network can reach CP
Expected:     Admin API requires authentication
              CP not exposed externally
Status:       [  ]
Remark:       Admin access via K8s internal service

Case_2 | DP Proxy traffic flow
────────────────────────────────────────────────────────────────────
Description:  Verify DP proxies traffic from workstation to demo server
Test steps:   1. Deploy a service+route on Kong pointing to demo server
              2. From workstation, send request via DP proxy port
              3. Confirm request reaches demo server
Expected:     Traffic flows: Workstation → Kong DP → Demo Server
              Response returned to workstation
Status:       [  ]
Remark:       Core POC smoke test

Case_3 | PostgreSQL connectivity
────────────────────────────────────────────────────────────────────
Description:  Verify CP connects to PostgreSQL and persists config
Test steps:   1. Check Kong CP logs for DB connection
              2. Create a route via Admin API
              3. Restart Kong CP pod
              4. Verify route still exists after restart
Expected:     Config persists in PostgreSQL across restarts
Status:       [  ]
Remark:       DB on separate VM

====================================================================
POC-2: SECURITY & AUTHENTICATION
====================================================================

Case_4 | API Key authentication
────────────────────────────────────────────────────────────────────
Description:  Verify Kong enforces API key on configured routes
Test steps:   1. Enable key-auth plugin on a test route
              2. Create a consumer with API key
              3. Send request with:
                 a) Valid key in header
                 b) Invalid key
                 c) No key
Expected:     Valid key → 200
              Invalid key → 401
              No key → 401
Status:       [  ]
Remark:       Core auth mechanism

Case_5 | JWT token validation
────────────────────────────────────────────────────────────────────
Description:  Verify Kong validates JWT for Open Banking use case
Test steps:   1. Enable jwt plugin on a test route
              2. Generate a valid JWT (RS256)
              3. Send requests with:
                 a) Valid JWT
                 b) Expired JWT
                 c) Tampered signature
                 d) Wrong issuer
Expected:     Valid JWT → 200
              All invalid variants → 401/403
Status:       [  ]
Remark:       Match Fubon's IdP requirements

Case_6 | mTLS client certificate
────────────────────────────────────────────────────────────────────
Description:  Verify mTLS for partner/client certificate auth
Test steps:   1. Enable mTLS on a route
              2. Generate test client cert (CA-signed)
              3. Send request with:
                 a) Valid client cert
                 b) Expired cert
                 c) No cert
Expected:     Valid cert → 200
              Invalid/no cert → 401
Status:       [  ]
Remark:       Required for fintech partner integration

Case_7 | IP whitelist/blacklist
────────────────────────────────────────────────────────────────────
Description:  Verify IP restriction on routes
Test steps:   1. Configure IP restriction plugin (allow specific CIDR)
              2. Send from allowed IP → should pass
              3. Send from blocked IP → should reject
Expected:     Allowed IP → 200
              Blocked IP → 403
Status:       [  ]
Remark:       DMZ security control

====================================================================
POC-3: TRAFFIC MANAGEMENT
====================================================================

Case_8 | Rate limiting (per client)
────────────────────────────────────────────────────────────────────
Description:  Verify per-client rate limiting
Test steps:   1. Enable rate-limiting plugin (e.g. 5 req/min)
              2. Send 7 requests as same consumer in 1 min
              3. Wait 1 min, send again
Expected:     First 5 → 200
              6th & 7th → 429
              After cooldown → 200 again
Status:       [  ]
Remark:       Protect against API abuse

Case_9 | Rate limiting (per route)
────────────────────────────────────────────────────────────────────
Description:  Verify per-route rate limit independent of client
Test steps:   1. Set route-level rate limit: 100 req/min
              2. Multiple consumers hit same route
              3. Verify total across all consumers capped at 100
Expected:     Aggregate requests > 100 → 429
Status:       [  ]
Remark:       Route-level vs consumer-level

Case_10 | Circuit breaker
────────────────────────────────────────────────────────────────────
Description:  Verify Kong protects backend from cascading failure
Test steps:   1. Configure circuit breaker on upstream
              2. Make demo server slow/unresponsive
              3. Send multiple requests
              4. Verify circuit opens after threshold
Expected:     After N failures → circuit opens
              Subsequent requests → fast-fail 503
              After cooldown → circuit half-opens → retries
Status:       [  ]
Remark:       Critical for backend stability

Case_11 | Request/response transformation
────────────────────────────────────────────────────────────────────
Description:  Verify Kong transforms request/response headers
Test steps:   1. Configure a route with header transformation plugin
              2. Add/remove/modify headers via plugin
              3. Verify demo server receives modified headers
Expected:     Headers added/removed/changed as configured
Status:       [  ]
Remark:       Useful for legacy backend compatibility

====================================================================
POC-4: OBSERVABILITY
====================================================================

Case_12 | Access logging
────────────────────────────────────────────────────────────────────
Description:  Verify Kong logs all proxy requests
Test steps:   1. Enable http-log or file-log plugin
              2. Send several test requests with different methods
              3. Check log output contains:
                 - Timestamp, client IP, method, path
                 - Status code, latency
                 - Consumer ID (if auth enabled)
Expected:     Complete request log for every request
Status:       [  ]
Remark:       Audit trail requirement

Case_13 | Prometheus metrics
────────────────────────────────────────────────────────────────────
Description:  Verify Kong exposes metrics for monitoring
Test steps:   1. Enable prometheus plugin
              2. Hit /metrics endpoint on CP or DP
              3. Verify metrics include:
                 - kong_http_requests_total
                 - kong_latency_ms (p50, p95, p99)
                 - kong_nginx_connections_total
Expected:     Metrics endpoint returns Prometheus-format data
Status:       [  ]
Remark:       For integration with Fubon monitoring stack

Case_14 | Health check
────────────────────────────────────────────────────────────────────
Description:  Verify Kong health check detects backend failure
Test steps:   1. Configure active health check on upstream
              2. Verify demo server is marked "healthy"
              3. Stop demo server
              4. Wait for health check interval
Expected:     Kong marks backend "unhealthy"
              Kong stops routing to unhealthy target
Status:       [  ]
Remark:       HA requirement

====================================================================
POC-5: ROUTING & INTEGRATION
====================================================================

Case_15 | Path-based routing
────────────────────────────────────────────────────────────────────
Description:  Verify Kong routes based on request path
Test steps:   1. Configure two services behind different paths:
                 /api/demo1 → demo server endpoint A
                 /api/demo2 → demo server endpoint B
              2. Send requests to each path
Expected:     Each path routes to correct backend endpoint
Status:       [  ]
Remark:       Basic routing test

Case_16 | Host-based routing
────────────────────────────────────────────────────────────────────
Description:  Verify Kong routes based on Host header
Test steps:   1. Configure two services with different hostnames:
                 api.fubon-test.com → demo server A
                 portal.fubon-test.com → demo server B
              2. Send requests with different Host headers
Expected:     Each hostname routes to correct backend
Status:       [  ]
Remark:       Multi-tenant scenario

Case_17 | Service health and load balancing
────────────────────────────────────────────────────────────────────
Description:  Verify Kong load balances across multiple targets
Test steps:   1. Configure upstream with 2 demo server instances
              2. Send 10 requests
              3. Check distribution across targets
Expected:     Requests distributed (round-robin or least-connections)
              If one target down → all traffic to remaining
Status:       [  ]
Remark:       Scale-out scenario

Case_18 | CORS handling
────────────────────────────────────────────────────────────────────
Description:  Verify Kong handles CORS preflight for web clients
Test steps:   1. Enable CORS plugin on a route
              2. Send OPTIONS request from browser origin
              3. Verify Access-Control-* headers in response
Expected:     Correct CORS headers for allowed origins
              No CORS headers for disallowed origins
Status:       [  ]
Remark:       Required for web portal integration

====================================================================
POC-6: DEVOPS & CONFIGURATION
====================================================================

Case_19 | Declarative config (DB-less mode)
────────────────────────────────────────────────────────────────────
Description:  Verify Kong works with declarative YAML config
Test steps:   1. Export Kong config to YAML via decK
              2. Modify config (add route)
              3. Import config back via decK
              4. Verify new route works
Expected:     Config export → modify → import cycle works
              Routes functional after each step
Status:       [  ]
Remark:       GitOps / CI-CD pipeline

Case_20 | Kong config validation
────────────────────────────────────────────────────────────────────
Description:  Verify Kong validates config before applying
Test steps:   1. Use deck validate or kong check on a valid config
              2. Intentionally break config (bad plugin syntax)
              3. Run validation again
Expected:     Valid config → passes
              Broken config → rejected with error details
Status:       [  ]
Remark:       Prevent bad config from breaking gateway

Case_21 | Zero-downtime reload
────────────────────────────────────────────────────────────────────
Description:  Verify Kong reload without dropping requests
Test steps:   1. Start continuous requests to DP
              2. Apply config change (add new route)
              3. Check if any requests dropped during reload
Expected:     Config changes applied without connection drops
Status:       [  ]
Remark:       Production requirement

====================================================================
POC-7: PERFORMANCE (BONUS IF TIME)
====================================================================

Case_22 | Kong latency overhead
────────────────────────────────────────────────────────────────────
Description:  Measure Kong's added latency
Test steps:   1. Ping demo server directly (no Kong) — record baseline
              2. Send same request via Kong DP
              3. Calculate difference
Expected:     Kong overhead < 5ms (p99)
Status:       [  ]
Remark:       SLA requirement

Case_23 | Throughput test
────────────────────────────────────────────────────────────────────
Description:  Verify Kong handles expected TPS
Test steps:   1. Use Postman/script to send requests in parallel
              2. Start with low TPS, ramp up to target (e.g. 500 TPS)
              3. Monitor Kong CPU/memory on K8s
Expected:     No errors at expected TPS
              CPU < 70%, memory stable
Status:       [  ]
Remark:       Scale test for production reference

====================================================================
SUMMARY
====================================================================

  POC-1 Architecture & Connectivity:    ___ / 3
  POC-2 Security & Authentication:      ___ / 4
  POC-3 Traffic Management:             ___ / 4
  POC-4 Observability:                  ___ / 3
  POC-5 Routing & Integration:          ___ / 4
  POC-6 DevOps & Configuration:         ___ / 3
  POC-7 Performance (bonus):            ___ / 2
  ─────────────────────────────────────────────
  TOTAL:                                 ___ / 23

Recommended priority for Thu 4 Jun:
  Must do:  POC-1, POC-2, POC-3 (core gateway functions)
  Should do: POC-4, POC-5 (observability + routing)
  If time:  POC-6, POC-7 (devops + perf)
