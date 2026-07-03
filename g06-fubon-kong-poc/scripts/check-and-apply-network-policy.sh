#!/usr/bin/env bash
set -euo pipefail

CP_NAMESPACE="${CP_NAMESPACE:-kong-cp-uat}"
DP_NAMESPACE="${DP_NAMESPACE:-kong-dp-uat}"
POSTGRES_HOST="${POSTGRES_HOST:-}"
POSTGRES_PORT="${POSTGRES_PORT:-5432}"
BACKEND_HOST="${BACKEND_HOST:-}"
BACKEND_PORT="${BACKEND_PORT:-443}"
POLICY_FILE="${POLICY_FILE:-manifests/02-networkpolicy.yaml}"
APPLY_ON_FAILURE="${APPLY_ON_FAILURE:-true}"

failed_checks=()

usage() {
  cat <<EOF
Usage:
  POSTGRES_HOST=<postgres-host-or-ip> [BACKEND_HOST=<backend-host-or-ip>] ./scripts/check-and-apply-network-policy.sh

Optional environment variables:
  CP_NAMESPACE=${CP_NAMESPACE}
  DP_NAMESPACE=${DP_NAMESPACE}
  POSTGRES_PORT=${POSTGRES_PORT}
  BACKEND_PORT=${BACKEND_PORT}
  POLICY_FILE=${POLICY_FILE}
  APPLY_ON_FAILURE=${APPLY_ON_FAILURE}
  KONG_ADMIN_PASSWORD=<admin-password>      # enables Admin API post-check
  API_URL=https://api-poc.uat.fubonhk.internal/api/v1/health
  ADMIN_URL=https://kong-admin.uat.fubonhk.internal/

Behavior:
  1. Checks default connectivity using netshoot.
  2. If any required check fails, applies manifests/02-networkpolicy.yaml.
  3. Re-checks Kong component health after applying the policy.
EOF
}

log() {
  printf '\n==> %s\n' "$*"
}

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

check_cmd() {
  local name="$1"
  shift
  echo "-- ${name}"
  if "$@"; then
    echo "   PASS"
  else
    echo "   FAIL"
    failed_checks+=("${name}")
  fi
}

need_binary() {
  command -v "$1" >/dev/null 2>&1 || fail "$1 is required but was not found in PATH"
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

need_binary oc

[[ -n "${POSTGRES_HOST}" ]] || {
  usage
  fail "POSTGRES_HOST is required"
}

[[ -f "${POLICY_FILE}" ]] || fail "NetworkPolicy file not found: ${POLICY_FILE}"

if grep -qE '__POSTGRES_VM_CIDR__|__BACKEND_API_CIDR__' "${POLICY_FILE}"; then
  fail "${POLICY_FILE} still contains placeholder CIDRs. Replace them before this script can apply it."
fi

log "Checking required namespaces and netshoot deployments"
oc get namespace "${CP_NAMESPACE}" >/dev/null
oc get namespace "${DP_NAMESPACE}" >/dev/null
oc rollout status "deployment/netshoot" -n "${CP_NAMESPACE}" --timeout=120s
oc rollout status "deployment/netshoot" -n "${DP_NAMESPACE}" --timeout=120s

log "Checking default network connectivity before NetworkPolicy"
check_cmd "CP netshoot to PostgreSQL ${POSTGRES_HOST}:${POSTGRES_PORT}" \
  oc exec -n "${CP_NAMESPACE}" deploy/netshoot -- nc -vz -w 5 "${POSTGRES_HOST}" "${POSTGRES_PORT}"

check_cmd "DP netshoot DNS for CP cluster service" \
  oc exec -n "${DP_NAMESPACE}" deploy/netshoot -- dig +short "kong-cp-cluster.${CP_NAMESPACE}.svc.cluster.local"

check_cmd "DP netshoot to CP cluster port 8005" \
  oc exec -n "${DP_NAMESPACE}" deploy/netshoot -- nc -vz -w 5 "kong-cp-cluster.${CP_NAMESPACE}.svc.cluster.local" 8005

check_cmd "DP netshoot to CP telemetry port 8006" \
  oc exec -n "${DP_NAMESPACE}" deploy/netshoot -- nc -vz -w 5 "kong-cp-clustertelemetry.${CP_NAMESPACE}.svc.cluster.local" 8006

if [[ -n "${BACKEND_HOST}" ]]; then
  check_cmd "DP netshoot to backend ${BACKEND_HOST}:${BACKEND_PORT}" \
    oc exec -n "${DP_NAMESPACE}" deploy/netshoot -- nc -vz -w 5 "${BACKEND_HOST}" "${BACKEND_PORT}"
fi

if [[ "${#failed_checks[@]}" -eq 0 ]]; then
  log "Default connectivity checks passed"
  echo "NetworkPolicy is not required for basic connectivity at this point."
  echo "You can still apply ${POLICY_FILE} later as the planned hardening step."
  exit 0
fi

log "Default connectivity checks failed"
printf 'Failed checks:\n'
printf '- %s\n' "${failed_checks[@]}"

if [[ "${APPLY_ON_FAILURE}" != "true" ]]; then
  fail "APPLY_ON_FAILURE is not true, so ${POLICY_FILE} was not applied"
fi

log "Applying NetworkPolicy"
oc apply -f "${POLICY_FILE}"
oc get networkpolicy -n "${CP_NAMESPACE}"
oc get networkpolicy -n "${DP_NAMESPACE}"

log "Validating Kong components after NetworkPolicy"
oc rollout status deployment/kong-cp -n "${CP_NAMESPACE}" --timeout=180s
oc rollout status deployment/kong-dp -n "${DP_NAMESPACE}" --timeout=180s

echo "-- Recent DP log lines mentioning cluster connectivity"
oc logs -n "${DP_NAMESPACE}" deploy/kong-dp -c proxy --tail=200 | grep -Ei 'cluster|telemetry|control.?plane|error|fail' || true

if [[ -n "${API_URL:-}" ]]; then
  log "Checking proxy URL"
  curl -kfsS "${API_URL}" >/dev/null
  echo "Proxy URL reachable: ${API_URL}"
fi

if [[ -n "${ADMIN_URL:-}" && -n "${KONG_ADMIN_PASSWORD:-}" ]]; then
  log "Checking Admin API URL"
  curl -kfsS -H "Kong-Admin-Token:${KONG_ADMIN_PASSWORD}" "${ADMIN_URL}" >/dev/null
  echo "Admin API reachable: ${ADMIN_URL}"
fi

log "Completed"
echo "NetworkPolicy was applied because at least one default connectivity check failed."
