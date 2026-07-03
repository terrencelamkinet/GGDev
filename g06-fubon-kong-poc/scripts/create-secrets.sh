#!/usr/bin/env bash
set -euo pipefail

: "${KONG_ADMIN_PASSWORD:?Set KONG_ADMIN_PASSWORD}"
: "${KONG_PG_PASSWORD:?Set KONG_PG_PASSWORD}"
: "${KONG_LICENSE_FILE:?Set KONG_LICENSE_FILE to the Kong license JSON file path}"

CLUSTER_CERT="${CLUSTER_CERT:-./certs/kong-cluster/tls.crt}"
CLUSTER_KEY="${CLUSTER_KEY:-./certs/kong-cluster/tls.key}"

if ! command -v oc >/dev/null 2>&1; then
  echo "oc CLI is required but was not found in PATH" >&2
  exit 1
fi

for ns in kong-cp-uat kong-dp-uat; do
  oc create secret generic kong-enterprise-license \
    -n "${ns}" \
    --from-file=license="${KONG_LICENSE_FILE}" \
    --dry-run=client -o yaml | oc apply -f -

  oc create secret tls kong-cluster-cert \
    -n "${ns}" \
    --cert="${CLUSTER_CERT}" \
    --key="${CLUSTER_KEY}" \
    --dry-run=client -o yaml | oc apply -f -
done

oc create secret generic kong-db-secret \
  -n kong-cp-uat \
  --from-literal=password="${KONG_PG_PASSWORD}" \
  --dry-run=client -o yaml | oc apply -f -

oc create secret generic kong-admin-secret \
  -n kong-cp-uat \
  --from-literal=password="${KONG_ADMIN_PASSWORD}" \
  --dry-run=client -o yaml | oc apply -f -

SESSION_SECRET="${KONG_SESSION_SECRET:-$(openssl rand -hex 32)}"
SESSION_CONF="{\"cookie_name\":\"kong_admin_session\",\"secret\":\"${SESSION_SECRET}\",\"cookie_secure\":true,\"cookie_samesite\":\"Strict\"}"
oc create secret generic kong-session-config \
  -n kong-cp-uat \
  --from-literal=admin_gui_session_conf="${SESSION_CONF}" \
  --dry-run=client -o yaml | oc apply -f -

echo "Secrets created or updated."
