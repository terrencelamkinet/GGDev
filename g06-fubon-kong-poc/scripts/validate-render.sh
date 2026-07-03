#!/usr/bin/env bash
set -euo pipefail

CHART_VERSION="${CHART_VERSION:-3.2.0}"

helm repo add kong https://charts.konghq.com >/dev/null 2>&1 || true
helm repo update kong >/dev/null

WORKDIR="/tmp/fubon-kong-chart-${CHART_VERSION}"
rm -rf "${WORKDIR}"
mkdir -p "${WORKDIR}"
helm pull kong/kong --version "${CHART_VERSION}" --untar --untardir "${WORKDIR}" >/dev/null

helm template kong-cp kong/kong \
  --version "${CHART_VERSION}" \
  -n kong-cp-uat \
  -f helm/kong-cp-values.yaml \
  >/tmp/fubon-kong-cp-render.yaml

helm template kong-dp kong/kong \
  --version "${CHART_VERSION}" \
  -n kong-dp-uat \
  -f helm/kong-dp-values.yaml \
  >/tmp/fubon-kong-dp-render.yaml

helm lint "${WORKDIR}/kong" \
  -f helm/kong-cp-values.yaml

helm lint "${WORKDIR}/kong" \
  -f helm/kong-dp-values.yaml

echo "Rendered manifests:"
echo "- /tmp/fubon-kong-cp-render.yaml"
echo "- /tmp/fubon-kong-dp-render.yaml"
