#!/usr/bin/env bash
set -euo pipefail

KONG_IMAGE="${KONG_IMAGE:-kong/kong-gateway:3.14}"
SMOKE_IMAGE="${SMOKE_IMAGE:-hashicorp/http-echo:1.0}"
NETSHOOT_IMAGE="${NETSHOOT_IMAGE:-nicolaka/netshoot:v0.13}"

docker pull "${KONG_IMAGE}"
docker pull "${SMOKE_IMAGE}"
docker pull "${NETSHOOT_IMAGE}"

cat <<EOF
Pulled:
- ${KONG_IMAGE}
- ${SMOKE_IMAGE}
- ${NETSHOOT_IMAGE}

If Fubon uses an internal registry, tag and push these images to the approved registry:
  docker tag ${KONG_IMAGE} <internal-registry>/kong/kong-gateway:3.14
  docker push <internal-registry>/kong/kong-gateway:3.14
  docker tag ${NETSHOOT_IMAGE} <internal-registry>/nicolaka/netshoot:v0.13
  docker push <internal-registry>/nicolaka/netshoot:v0.13
EOF
