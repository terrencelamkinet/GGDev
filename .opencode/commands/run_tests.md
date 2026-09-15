# /run_tests

Run all test suites for the project.

## Usage
```
/run_tests [target]
```

## Targets
- `backend` — Run Python tests: `cd gg-dashboard && python -m pytest tests/ -v`
- `frontend` — Run frontend tests: `cd gg-dashboard/frontend && npm test`
- `all` — Run all tests (default)

## Implementation
```bash
#!/bin/bash
# Run tests for GGDev project
set -e

TARGET="${1:-all}"

run_backend_tests() {
  echo "🧪 Running backend tests..."
  cd ~/projects/ggdev-repo/gg-dashboard
  python -m pytest tests/ -v --tb=short 2>&1 || true
}

run_frontend_tests() {
  echo "🧪 Running frontend tests..."
  cd ~/projects/ggdev-repo/gg-dashboard/frontend
  npm test 2>&1 || true
}

case "$TARGET" in
  backend)
    run_backend_tests
    ;;
  frontend)
    run_frontend_tests
    ;;
  all)
    run_backend_tests
    run_frontend_tests
    ;;
  *)
    echo "Unknown target: $TARGET"
    echo "Usage: /run_tests [backend|frontend|all]"
    exit 1
    ;;
esac

echo "✅ Tests complete"
```
