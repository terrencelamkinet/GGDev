# /deploy

Deploy the project to Mac Mini via rsync, then restart services.

## Usage
```
/deploy [target]
```

## Targets
- `dashboard` — Deploy gg-dashboard only
- `all` — Deploy entire ggdev-repo (default)
- `frontend` — Deploy frontend assets only

## Implementation
```bash
#!/bin/bash
# Deploy GGDev project to Mac Mini
set -e

TARGET="${1:-all}"
RSYNC_DEST="gg-fighter:~/projects/ggdev-repo/"
EXCLUDES="--exclude='.git/' --exclude='node_modules/' --exclude='__pycache__/'"

deploy_dashboard() {
  echo "🚀 Deploying gg-dashboard..."
  rsync -avz $EXCLUDES \
    ~/projects/ggdev-repo/gg-dashboard/ \
    "${RSYNC_DEST}gg-dashboard/"
  
  echo "🔄 Restarting dashboard services..."
  ssh gg-fighter "sudo systemctl restart gg-dashboard" 2>/dev/null || \
    ssh gg-fighter "pm2 restart gg-dashboard" 2>/dev/null || true
}

deploy_all() {
  echo "🚀 Deploying full ggdev-repo..."
  rsync -avz $EXCLUDES \
    ~/projects/ggdev-repo/ \
    "$RSYNC_DEST"
  
  echo "🔄 Restarting all services..."
  ssh gg-fighter "sudo systemctl restart gg-dashboard gg-hermes" 2>/dev/null || true
}

deploy_frontend() {
  echo "🚀 Building and deploying frontend..."
  cd ~/projects/ggdev-repo/gg-dashboard/frontend
  npm run build
  
  rsync -avz --exclude='node_modules/' \
    dist/ \
    "${RSYNC_DEST}gg-dashboard/frontend/dist/"
}

case "$TARGET" in
  dashboard)
    deploy_dashboard
    ;;
  frontend)
    deploy_frontend
    ;;
  all)
    deploy_all
    ;;
  *)
    echo "Unknown target: $TARGET"
    echo "Usage: /deploy [dashboard|frontend|all]"
    exit 1
    ;;
esac

echo "✅ Deployment complete: $(date)"
```
