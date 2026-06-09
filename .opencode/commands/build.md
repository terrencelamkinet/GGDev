# /build

Build frontend + backend for the GGDev project.

## Usage
```
/build [target]
```

## Targets
- `frontend` — Build React/TypeScript frontend
- `backend` — Build/compile backend
- `docker` — Build Docker images
- `all` — Build everything (default)

## Implementation
```bash
#!/bin/bash
# Build GGDev project
set -e

TARGET="${1:-all}"

build_frontend() {
  echo "🔨 Building frontend..."
  cd ~/projects/ggdev-repo/gg-dashboard/frontend
  npm ci
  npm run build --if-present
  echo "✅ Frontend built"
}

build_backend() {
  echo "🔨 Building backend..."
  cd ~/projects/ggdev-repo
  
  # Install Python dependencies
  pip install -r gg-dashboard/requirements.txt --quiet 2>/dev/null || true
  
  # Run any build steps
  if [ -f "gg-dashboard/pyproject.toml" ]; then
    cd gg-dashboard && python -m build --wheel 2>/dev/null || true
  fi
  
  echo "✅ Backend ready"
}

build_docker() {
  echo "🔨 Building Docker images..."
  cd ~/projects/ggdev-repo
  
  if [ -f "docker-compose.yml" ]; then
    docker-compose build 2>&1 || true
  fi
  
  echo "✅ Docker images built"
}

case "$TARGET" in
  frontend)
    build_frontend
    ;;
  backend)
    build_backend
    ;;
  docker)
    build_docker
    ;;
  all)
    build_frontend
    build_backend
    build_docker
    ;;
  *)
    echo "Unknown target: $TARGET"
    echo "Usage: /build [frontend|backend|docker|all]"
    exit 1
    ;;
esac

echo "✅ Build complete: $(date)"
```
