# Fubon HK Kong API Gateway PoC Environment Setup Guide

This guide builds the `Kong-PoC-UAT` environment from the PoC summary workbook.

The target platform is Red Hat OpenShift UAT. Kong runs in self-managed hybrid mode: the Control Plane manages configuration and connects to the external PostgreSQL database, while the Data Plane handles API traffic. PostgreSQL is outside OpenShift on a dedicated RHEL VM.

## Confirmed PoC Values

| Item | Value |
| --- | --- |
| PoC environment | `Kong-PoC-UAT` |
| Platform | Existing Fubon UAT OpenShift cluster |
| Deployment mode | Kong Gateway hybrid mode, separate CP and DP |
| Helm chart | `kong/kong`, pinned to chart `3.2.0` |
| Kong image | `kong/kong-gateway:3.14` |
| CP namespace | `kong-cp-uat` |
| DP namespace | `kong-dp-uat` |
| CP replicas | `2` |
| DP replicas | `3` |
| CP pod sizing | `2 vCPU / 4 GiB RAM` per pod |
| DP pod sizing | `2 vCPU / 4 GiB RAM` per pod |
| PostgreSQL | PostgreSQL 14+ on dedicated RHEL VM, `4 vCPU / 8 GiB / 100 GB` |
| API DNS | `api-poc.uat.fubonhk.internal` |
| Kong Manager DNS | `kong-manager.uat.fubonhk.internal` |
| Kong Admin DNS | `kong-admin.uat.fubonhk.internal` |
| CP cluster service | `kong-cp-cluster.kong-cp-uat.svc.cluster.local:8005` |
| CP telemetry service | `kong-cp-clustertelemetry.kong-cp-uat.svc.cluster.local:8006` |

The workbook listed `kong-cp-cluster.fubon-uat.svc.cluster.local`; the generated values use the Helm service names and the confirmed CP namespace, which is the Kubernetes-correct DNS form for this installation.

## Repository Layout

```text
.
├── README.md
├── deck/
│   └── smoke-test.yaml
├── helm/
│   ├── kong-cp-values.yaml
│   └── kong-dp-values.yaml
├── manifests/
│   ├── 00-namespaces-rbac.yaml
│   ├── 01-openshift-routes.yaml
│   ├── 02-networkpolicy.yaml
│   ├── 03-smoke-test-backend.yaml
│   └── 04-netshoot.yaml
├── postgres/
│   ├── postgresql-setup.sql
│   └── postgresql-systemd-limits.conf
└── scripts/
    ├── check-and-apply-network-policy.sh
    ├── create-secrets.sh
    ├── pull-images.sh
    └── validate-render.sh
```

## Prerequisites

Install these on the operator workstation or jump host:

| Tool | Required for |
| --- | --- |
| `oc` CLI | OpenShift login, namespace setup, secrets, validation |
| Helm 3.x | Kong chart installation |
| Docker or Podman | Pulling and mirroring images |
| `openssl` | CP/DP cluster certificate generation |
| `deck` v1.38+ | Kong configuration as code |
| `curl` | Smoke validation |
| `jq` | JSON status output checks |

Access requirements:

- OpenShift access to create resources in `kong-cp-uat` and `kong-dp-uat`.
- Fubon DBA-provided PostgreSQL VM hostname or IP.
- SSH access to the PostgreSQL VM, or access through the approved Fubon jump host.
- Fubon DBA-created database `kong`, user `kong`, and runtime password.
- F5 VIP and internal DNS records for the three hostnames.
- Kong Enterprise license JSON.
- Fubon-approved image registry path if direct Docker Hub pulls are not allowed.

## Network and DNS

Create or confirm these DNS records:

| DNS | Purpose | Target |
| --- | --- | --- |
| `api-poc.uat.fubonhk.internal` | API Gateway proxy | F5 VIP, then OpenShift router, then Kong DP |
| `kong-manager.uat.fubonhk.internal` | Kong Manager UI | Internal management network only |
| `kong-admin.uat.fubonhk.internal` | Kong Admin API | Internal operator or CI/CD network only |

Required firewall flows:

| Source | Destination | Port |
| --- | --- | --- |
| F5 or OpenShift router | Kong DP proxy service | TCP `8443`, optional PoC HTTP `8000` |
| Kong DP namespace | Kong CP cluster service | TCP `8005` |
| Kong DP namespace | Kong CP telemetry service | TCP `8006` |
| Kong CP namespace | External PostgreSQL VM | TCP `5432` |
| Kong DP namespace | Backend API | TCP `443` or confirmed backend port |
| Monitoring collector | Kong status endpoint | TCP `8100` |

Use passthrough TLS on the API route so Kong receives the client TLS handshake and can enforce mTLS at the Data Plane.

## Step 1 - Pull and Mirror Images

Pull the images locally:

```bash
chmod +x scripts/pull-images.sh
./scripts/pull-images.sh
```

If Fubon requires an internal registry, mirror the image and update `image.repository` in both Helm values files:

```bash
docker tag kong/kong-gateway:3.14 <internal-registry>/kong/kong-gateway:3.14
docker push <internal-registry>/kong/kong-gateway:3.14
docker tag nicolaka/netshoot:v0.13 <internal-registry>/nicolaka/netshoot:v0.13
docker push <internal-registry>/nicolaka/netshoot:v0.13
```

Also mirror `hashicorp/http-echo:1.0` only if the optional smoke-test backend will be deployed.

If Fubon mirrors `nicolaka/netshoot:v0.13`, update `manifests/04-netshoot.yaml` to use the internal registry image.

## Step 2 - Prepare PostgreSQL

On the external RHEL PostgreSQL VM, install PostgreSQL 14+ using Fubon DBA standards. The PoC sizing is:

- `4 vCPU`
- `8 GiB RAM`
- `100 GB disk`
- TCP `5432`, unless Fubon DBA assigns a different port

Before connecting, confirm these values with Fubon:

| Input | Example | Notes |
| --- | --- | --- |
| DB VM hostname or IP | `<postgres-host-or-ip>` | Required by Kong CP and validation scripts |
| SSH username | `<ssh-user>` | Usually a named Linux account, not `root` |
| SSH method | key, password, or bastion | Follow Fubon access policy |
| Jump host | `<jump-host>` | Required if DB VM is not directly reachable |
| PostgreSQL service name | `postgresql`, `postgresql-14`, or `postgresql@14-main` | Confirm with DBA |
| PostgreSQL port | `5432` | Use customer port if different |
| Kong DB password | `<kong-db-password>` | Store later in OpenShift Secret only |

### Step 2.1 - SSH to the DB VM

Direct SSH:

```bash
ssh <ssh-user>@<postgres-host-or-ip>
```

SSH through a Fubon jump host:

```bash
ssh -J <jump-user>@<jump-host> <ssh-user>@<postgres-host-or-ip>
```

SSH with a private key:

```bash
chmod 600 /path/to/private-key.pem
ssh -i /path/to/private-key.pem <ssh-user>@<postgres-host-or-ip>
```

SSH with a private key and jump host:

```bash
chmod 600 /path/to/private-key.pem
ssh -i /path/to/private-key.pem \
  -J <jump-user>@<jump-host> \
  <ssh-user>@<postgres-host-or-ip>
```

Expected:

- Login succeeds.
- The shell prompt is on the PostgreSQL VM.
- You can run `sudo -l` or have DBA assistance for privileged commands.

If SSH fails:

| Symptom | Check |
| --- | --- |
| `Connection timed out` | Network route, VPN, jump host, firewall TCP `22` |
| `Permission denied publickey` | Correct SSH key, Linux username, key registered on VM |
| `Could not resolve hostname` | DNS or use direct VM IP |
| MFA prompt never appears | Check VPN/jump host session |
| `sudo: user is not in sudoers` | Ask DBA/Unix team to run privileged setup commands |

### Step 2.2 - Confirm the VM is RHEL and Sized Correctly

Run on the DB VM:

```bash
cat /etc/redhat-release
hostname -f || hostname
nproc
free -h
lsblk
df -h
ulimit -n
ulimit -u
```

Expected:

- OS shows Red Hat Enterprise Linux or a Fubon-approved RHEL-compatible image.
- CPU count is at least `4`.
- Memory is around `8 GiB` or higher.
- Data disk has at least `100 GB`.
- `ulimit -n` should be `65535` after limits are applied.
- `ulimit -u` should be `4096` or higher after limits are applied.

### Step 2.3 - Confirm PostgreSQL 14+ is Installed

Run on the DB VM:

```bash
psql --version
sudo systemctl list-units --type=service | grep -i postgres
```

Expected:

- `psql` reports PostgreSQL `14` or later.
- A PostgreSQL service is installed.

If PostgreSQL is not installed, ask the Fubon DBA team to install PostgreSQL 14+ using Fubon standards before continuing.

Apply OS limits if required:

```bash
sudo mkdir -p /etc/systemd/system/postgresql.service.d
sudo cp postgres/postgresql-systemd-limits.conf /etc/systemd/system/postgresql.service.d/limits.conf
sudo systemctl daemon-reload
sudo systemctl restart <postgresql-service-name>
sudo systemctl status <postgresql-service-name> --no-pager
```

Expected:

- PostgreSQL service is `active (running)`.
- No startup errors appear in `systemctl status`.

### Step 2.4 - Confirm PostgreSQL is Listening on TCP 5432

Run on the DB VM:

```bash
sudo ss -lntp | grep 5432
sudo firewall-cmd --list-ports 2>/dev/null || true
sudo firewall-cmd --list-services 2>/dev/null || true
```

Expected:

- PostgreSQL listens on `0.0.0.0:5432`, `<db-vm-ip>:5432`, or an approved interface reachable from OpenShift.
- If the RHEL host firewall is enabled, TCP `5432` is allowed from the OpenShift worker/egress network.

If PostgreSQL is only listening on `127.0.0.1:5432`, ask the DBA team to update `postgresql.conf` and `pg_hba.conf` according to Fubon standards.

Create the Kong database and runtime user:

```bash
sudo -iu postgres psql -f postgres/postgresql-setup.sql
```

If the file is not on the DB VM, copy it first from the operator workstation:

```bash
scp postgres/postgresql-setup.sql <ssh-user>@<postgres-host-or-ip>:/tmp/postgresql-setup.sql
ssh <ssh-user>@<postgres-host-or-ip>
sudo -iu postgres psql -f /tmp/postgresql-setup.sql
```

With a jump host:

```bash
scp -o ProxyJump=<jump-user>@<jump-host> \
  postgres/postgresql-setup.sql \
  <ssh-user>@<postgres-host-or-ip>:/tmp/postgresql-setup.sql
```

Validate the database locally on the DB VM:

```bash
sudo -iu postgres psql -d kong -c '\du kong'
sudo -iu postgres psql -d kong -c 'select current_database(), current_user;'
```

Expected:

- Database `kong` exists.
- User `kong` exists.
- Runtime user owns or has privileges on database `kong`.

Validate database connectivity from the operator workstation or a network location equivalent to OpenShift egress:

```bash
PGPASSWORD='<kong-db-password>' \
  psql "host=<postgres-host-or-ip> port=5432 dbname=kong user=kong sslmode=prefer" \
  -c 'select version();'
```

Expected:

- Login as user `kong` succeeds.
- `select version();` returns PostgreSQL `14` or later.

Keep the DB VM terminal open until Kong CP installation is complete so DBA/Unix teams can inspect logs if the CP cannot connect.

## Step 3 - Create Namespaces and RBAC

Login to OpenShift:

```bash
oc login <fubon-uat-openshift-api-url>
```

Create namespaces, ServiceAccounts, Roles, and RoleBindings:

```bash
oc apply -f manifests/00-namespaces-rbac.yaml
```

Validate namespace and ServiceAccount creation:

```bash
oc get ns kong-cp-uat kong-dp-uat
oc get sa kong-sa -n kong-cp-uat
oc get sa kong-sa -n kong-dp-uat
oc auth can-i create deployments -n kong-cp-uat
oc auth can-i create jobs -n kong-cp-uat
oc auth can-i create routes.route.openshift.io -n kong-cp-uat
oc auth can-i create deployments -n kong-dp-uat
oc auth can-i create routes.route.openshift.io -n kong-dp-uat
```

Expected:

- Both namespaces exist.
- `kong-sa` exists in both namespaces.
- The current installer user can create Deployments, Jobs, Services, Secrets, and Routes in the PoC namespaces.

Deploy the netshoot diagnostic pods:

```bash
oc apply -f manifests/04-netshoot.yaml
oc rollout status deployment/netshoot -n kong-cp-uat
oc rollout status deployment/netshoot -n kong-dp-uat
```

Validate PostgreSQL connectivity from inside the CP namespace:

```bash
oc exec -n kong-cp-uat deploy/netshoot -- \
  nc -vz <postgres-host-or-ip> 5432

oc exec -n kong-cp-uat deploy/netshoot -- \
  dig +short <postgres-hostname>
```

Expected:

- TCP `5432` is reachable from OpenShift to the PostgreSQL VM.
- PostgreSQL hostname resolves correctly if a DNS name is used.

If the cluster enforces SCC assignment, use the Fubon-approved SCC. Kong does not require privileged containers. The preferred SCC is `restricted` or `nonroot`.

```bash
oc adm policy add-scc-to-user restricted -z kong-sa -n kong-cp-uat
oc adm policy add-scc-to-user restricted -z kong-sa -n kong-dp-uat
```

## Step 4 - Generate CP/DP Cluster Certificate

Create a shared CP/DP cluster certificate for PoC hybrid sync:

```bash
mkdir -p certs/kong-cluster
openssl req -new -x509 -nodes \
  -newkey ec:<(openssl ecparam -name secp384r1) \
  -keyout certs/kong-cluster/tls.key \
  -out certs/kong-cluster/tls.crt \
  -days 1095 \
  -subj "/CN=kong_clustering"
```

For production, replace this with a Fubon CA-issued cluster certificate.

## Step 5 - Create OpenShift Secrets

Set the secret inputs locally:

```bash
export KONG_ADMIN_PASSWORD='<strong-admin-password>'
export KONG_PG_PASSWORD='<kong-db-password-from-dba>'
export KONG_LICENSE_FILE='/path/to/kong-license.json'
```

Create secrets:

```bash
chmod +x scripts/create-secrets.sh
./scripts/create-secrets.sh
```

Validate secret creation:

```bash
oc get secret kong-enterprise-license kong-db-secret kong-admin-secret kong-session-config kong-cluster-cert -n kong-cp-uat
oc get secret kong-enterprise-license kong-cluster-cert -n kong-dp-uat
oc get secret kong-db-secret -n kong-cp-uat -o jsonpath='{.data.password}' | wc -c
oc get secret kong-cluster-cert -n kong-cp-uat -o jsonpath='{.data.tls\.crt}' | wc -c
oc get secret kong-cluster-cert -n kong-dp-uat -o jsonpath='{.data.tls\.crt}' | wc -c
```

Expected:

- All listed secrets exist.
- Secret data length is greater than zero.
- The same `kong-cluster-cert` certificate and key are present in both CP and DP namespaces.

The script generates a random `kong-session-config` secret automatically. To rotate or set a customer-approved session secret explicitly:

```bash
SESSION_SECRET="<fubon-approved-random-session-secret>"
SESSION_CONF="{\"cookie_name\":\"kong_admin_session\",\"secret\":\"${SESSION_SECRET}\",\"cookie_secure\":true,\"cookie_samesite\":\"Strict\"}"

oc create secret generic kong-session-config \
  -n kong-cp-uat \
  --from-literal=admin_gui_session_conf="${SESSION_CONF}" \
  --dry-run=client -o yaml | oc apply -f -
```

## Step 6 - Update Environment-Specific Values

Edit `helm/kong-cp-values.yaml`:

- Replace `__POSTGRES_HOST_OR_IP__` with the PostgreSQL VM hostname or IP.
- Change `pg_port` if Fubon DBA does not use `5432`.
- If images are mirrored, update `image.repository`.

Edit `manifests/02-networkpolicy.yaml`, but do not apply it yet unless Fubon security policy requires NetworkPolicy before application deployment:

- Replace `__POSTGRES_VM_CIDR__/32`.
- Replace `__BACKEND_API_CIDR__/32`.

For the PoC, the recommended sequence is:

1. Deploy CP and DP without NetworkPolicy.
2. Validate PostgreSQL, CP/DP sync, routes, Admin API, and proxy traffic.
3. Apply NetworkPolicy.
4. Re-run the same validation checks to confirm no required traffic was blocked.

This is acceptable only if the OpenShift cluster has the default namespace network behavior and Fubon security approves delayed enforcement for PoC setup. If the cluster enforces default-deny NetworkPolicy globally, apply the policy before installing Kong.

If the actual OpenShift route base domain differs from the workbook examples, routes still use the customer-facing hostnames from the summary:

- `api-poc.uat.fubonhk.internal`
- `kong-manager.uat.fubonhk.internal`
- `kong-admin.uat.fubonhk.internal`

## Step 7 - Validate Helm Rendering

Run a local render and lint:

```bash
chmod +x scripts/validate-render.sh
./scripts/validate-render.sh
```

Inspect the rendered service names:

```bash
rg 'name: kong-cp-cluster|name: kong-cp-clustertelemetry|name: kong-dp-proxy' /tmp/fubon-kong-*-render.yaml
```

## Step 8 - Install Kong Control Plane

Add and update the Kong Helm repo:

```bash
helm repo add kong https://charts.konghq.com
helm repo update kong
```

Install the Control Plane:

```bash
helm upgrade --install kong-cp kong/kong \
  --version 3.2.0 \
  -n kong-cp-uat \
  -f helm/kong-cp-values.yaml \
  --wait \
  --timeout 10m
```

Validate CP pods and services:

```bash
oc get pods,svc -n kong-cp-uat
oc rollout status deployment/kong-cp -n kong-cp-uat
oc get svc kong-cp-cluster kong-cp-clustertelemetry kong-cp-admin kong-cp-manager -n kong-cp-uat
oc get endpoints kong-cp-cluster kong-cp-clustertelemetry kong-cp-admin kong-cp-manager -n kong-cp-uat
oc logs -n kong-cp-uat deploy/kong-cp -c proxy --tail=100
```

Expected:

- `2/2` CP pods ready.
- `kong-cp-cluster` exposes `8005`.
- `kong-cp-clustertelemetry` exposes `8006`.
- `kong-cp-admin` exposes `8001` and `8444`.
- `kong-cp-manager` exposes `8002` and `8445`.
- Service endpoints contain CP pod IPs.
- Logs do not show PostgreSQL connection errors, migration errors, or license errors.

Validate CP status locally through port-forward:

```bash
oc port-forward -n kong-cp-uat deploy/kong-cp 8100:8100
curl -s http://127.0.0.1:8100/status | jq .
```

Expected:

- Status endpoint returns JSON.
- `database.reachable` is `true`.
- `server.connections_active` is present.

## Step 9 - Install Kong Data Plane

Install the Data Plane:

```bash
helm upgrade --install kong-dp kong/kong \
  --version 3.2.0 \
  -n kong-dp-uat \
  -f helm/kong-dp-values.yaml \
  --wait \
  --timeout 10m
```

Validate DP pods and services:

```bash
oc get pods,svc -n kong-dp-uat
oc rollout status deployment/kong-dp -n kong-dp-uat
oc get svc kong-dp-proxy -n kong-dp-uat
oc get endpoints kong-dp-proxy -n kong-dp-uat
```

Expected:

- `3/3` DP pods ready.
- `kong-dp-proxy` exposes `8000` and `8443`.
- Service endpoints contain DP pod IPs.
- DP logs show successful connection to the CP on `8005` and telemetry on `8006`.

Check DP logs:

```bash
oc logs -n kong-dp-uat deploy/kong-dp -c proxy --tail=100
```

Validate DP status locally through port-forward:

```bash
oc port-forward -n kong-dp-uat deploy/kong-dp 8100:8100
curl -s http://127.0.0.1:8100/status | jq .
```

Expected:

- Status endpoint returns JSON.
- DP reports healthy status.
- Logs do not show repeated CP connection failures.

Validate DP-to-CP service connectivity from the DP netshoot pod:

```bash
oc exec -n kong-dp-uat deploy/netshoot -- \
  nc -vz kong-cp-cluster.kong-cp-uat.svc.cluster.local 8005

oc exec -n kong-dp-uat deploy/netshoot -- \
  nc -vz kong-cp-clustertelemetry.kong-cp-uat.svc.cluster.local 8006

oc exec -n kong-dp-uat deploy/netshoot -- \
  dig +short kong-cp-cluster.kong-cp-uat.svc.cluster.local
```

Expected:

- TCP `8005` and `8006` are reachable from `kong-dp-uat` to `kong-cp-uat`.
- CP service DNS resolves from the DP namespace.

## Step 10 - Apply Routes

Apply OpenShift Routes:

```bash
oc apply -f manifests/01-openshift-routes.yaml
oc get routes -n kong-cp-uat
oc get routes -n kong-dp-uat
```

Validate route targets:

```bash
oc describe route kong-proxy-https -n kong-dp-uat
oc describe route kong-manager -n kong-cp-uat
oc describe route kong-admin -n kong-cp-uat
oc get route kong-proxy-https -n kong-dp-uat -o jsonpath='{.spec.to.name}{"\n"}'
oc get route kong-manager -n kong-cp-uat -o jsonpath='{.spec.to.name}{"\n"}'
oc get route kong-admin -n kong-cp-uat -o jsonpath='{.spec.to.name}{"\n"}'
```

Validate internal DNS and service reachability with netshoot:

```bash
oc exec -n kong-dp-uat deploy/netshoot -- \
  dig +short kong-dp-proxy.kong-dp-uat.svc.cluster.local

oc exec -n kong-dp-uat deploy/netshoot -- \
  nc -vz kong-dp-proxy.kong-dp-uat.svc.cluster.local 8443

oc exec -n kong-cp-uat deploy/netshoot -- \
  nc -vz kong-cp-admin.kong-cp-uat.svc.cluster.local 8444
```

Expected:

- `kong-proxy-https` targets `kong-dp-proxy`.
- `kong-manager` targets `kong-cp-manager`.
- `kong-admin` targets `kong-cp-admin`.
- Route admission status is accepted by the OpenShift router.
- Kong DP proxy service DNS resolves.
- Kong DP proxy TLS port `8443` is reachable inside the DP namespace.
- Kong CP Admin API TLS port `8444` is reachable inside the CP namespace.

## Step 11 - Optional Smoke Test Backend

Deploy the simple backend:

```bash
oc apply -f manifests/03-smoke-test-backend.yaml
oc rollout status deployment/smoke-test-backend -n kong-dp-uat
```

Apply the smoke Kong configuration through the CP Admin API:

```bash
deck gateway sync deck/smoke-test.yaml \
  --kong-addr https://kong-admin.uat.fubonhk.internal \
  --headers "Kong-Admin-Token:${KONG_ADMIN_PASSWORD}" \
  --tls-skip-verify
```

Validate via the Data Plane:

```bash
curl -k https://api-poc.uat.fubonhk.internal/api/v1/health
```

Expected response contains:

```json
{"status":"ok","service":"fubon-kong-poc","path":"/api/v1/health"}
```

Validate route, service, and plugin state from the Admin API:

```bash
curl -k \
  -H "Kong-Admin-Token:${KONG_ADMIN_PASSWORD}" \
  https://kong-admin.uat.fubonhk.internal/services/smoke-test-backend

curl -k \
  -H "Kong-Admin-Token:${KONG_ADMIN_PASSWORD}" \
  https://kong-admin.uat.fubonhk.internal/routes/smoke-test-health
```

Expected:

- Service `smoke-test-backend` exists.
- Route `smoke-test-health` exists.
- Proxy request returns HTTP `200`.

## Step 12 - Apply Network Policies

Apply NetworkPolicies only after replacing the placeholder CIDRs and after the pre-policy connectivity checks pass.

To automate the decision, run the helper script. It checks default connectivity first using netshoot. If any required check fails, it applies `manifests/02-networkpolicy.yaml` and validates Kong component status again:

```bash
chmod +x scripts/check-and-apply-network-policy.sh

POSTGRES_HOST=<postgres-host-or-ip> \
BACKEND_HOST=<backend-host-or-ip> \
API_URL=https://api-poc.uat.fubonhk.internal/api/v1/health \
ADMIN_URL=https://kong-admin.uat.fubonhk.internal/ \
KONG_ADMIN_PASSWORD="${KONG_ADMIN_PASSWORD}" \
./scripts/check-and-apply-network-policy.sh
```

If the default connectivity checks pass, the script does not apply NetworkPolicy. To test without applying on failure:

```bash
POSTGRES_HOST=<postgres-host-or-ip> \
APPLY_ON_FAILURE=false \
./scripts/check-and-apply-network-policy.sh
```

Manual apply:

```bash
oc apply -f manifests/02-networkpolicy.yaml
oc get networkpolicy -n kong-cp-uat
oc get networkpolicy -n kong-dp-uat
```

Re-run the critical checks:

```bash
oc rollout status deployment/kong-cp -n kong-cp-uat
oc rollout status deployment/kong-dp -n kong-dp-uat
oc logs -n kong-dp-uat deploy/kong-dp -c proxy --tail=100
oc exec -n kong-cp-uat deploy/netshoot -- nc -vz <postgres-host-or-ip> 5432
oc exec -n kong-dp-uat deploy/netshoot -- nc -vz kong-cp-cluster.kong-cp-uat.svc.cluster.local 8005
oc exec -n kong-dp-uat deploy/netshoot -- nc -vz kong-cp-clustertelemetry.kong-cp-uat.svc.cluster.local 8006
curl -k https://api-poc.uat.fubonhk.internal/api/v1/health
curl -k \
  -H "Kong-Admin-Token:${KONG_ADMIN_PASSWORD}" \
  https://kong-admin.uat.fubonhk.internal/
```

Expected:

- CP and DP remain ready.
- DP still connects to CP on `8005` and `8006`.
- CP still connects to PostgreSQL on `5432`.
- Proxy smoke test still returns HTTP `200`.
- Admin API remains reachable from the internal operator network.

If any check fails immediately after applying NetworkPolicy, remove the policy and review the blocked source, destination, and port:

```bash
oc delete -f manifests/02-networkpolicy.yaml
```

## Step 13 - mTLS Validation

After Fubon provides the test CA and two client certificates:

- Valid client certificate: expect `200`.
- Invalid or missing client certificate: expect `401` after the mTLS plugin is enabled.

Recommended test commands:

```bash
curl -k \
  --cert ./certs/client-valid/tls.crt \
  --key ./certs/client-valid/tls.key \
  https://api-poc.uat.fubonhk.internal/api/v1/health

curl -k https://api-poc.uat.fubonhk.internal/api/v1/health
```

Do not mark mTLS complete until Kong rejects requests without a trusted client certificate.

## Step 14 - Management UI Validation

Open Kong Manager from the internal operator network:

```text
https://kong-manager.uat.fubonhk.internal
```

Login:

- Username: `kong_admin`
- Password: value stored in `kong-admin-secret`

Validate Admin API access:

```bash
curl -k \
  -H "Kong-Admin-Token:${KONG_ADMIN_PASSWORD}" \
  https://kong-admin.uat.fubonhk.internal/
```

Expected:

- Kong Gateway version is returned.
- `configuration_hash` is present.
- Admin API is reachable only from the internal operator or CI/CD network.

## Step 15 - Monitoring Validation

Kong exposes Prometheus metrics on the status listener, port `8100`.

Port-forward for a quick check:

```bash
oc port-forward -n kong-dp-uat deploy/kong-dp 8100:8100
curl http://127.0.0.1:8100/metrics | head
```

Minimum metrics to confirm for PoC sign-off:

- TPS or request count.
- P95 latency.
- HTTP `4xx` and `5xx` rate.
- DP pod CPU and memory.
- DP health and CP/DP connectivity.

## Rollback

Uninstall DP first, then CP:

```bash
helm uninstall kong-dp -n kong-dp-uat
helm uninstall kong-cp -n kong-cp-uat
```

Keep PostgreSQL until Fubon confirms no further config export is required.

## Customer Inputs Still Required

The workbook marks these as TBC and they must be confirmed before the actual install:

| Input | Required by |
| --- | --- |
| OpenShift API URL and cluster name | `oc login`, customer records |
| PostgreSQL VM hostname or IP | `helm/kong-cp-values.yaml` |
| PostgreSQL password | `kong-db-secret` |
| F5 VIP IP | DNS and firewall setup |
| Backend API URL and CIDR | routing and NetworkPolicy |
| Fubon internal registry path | Helm image repository override |
| Fubon test CA and client certificates | mTLS validation |
| Monitoring/Helix scrape method | metrics collection |
| Fubon Git repo URL | decK configuration management |
