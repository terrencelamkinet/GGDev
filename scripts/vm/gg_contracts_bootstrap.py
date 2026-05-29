# ── Contracts DB check ──
_last_contracts_check = 0
_last_contracts_update = 0
CONTRACTS_CHECK_INTERVAL = 300  # every 5 min
CONTRACTS_UPDATE_INTERVAL = 604800  # weekly (7 days)

# ── Contracts check imported module ──
_contracts_module = None
def _ensure_contracts_module():
    global _contracts_module
    if _contracts_module is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "gg_contracts_check",
            os.path.join(os.path.dirname(__file__), "gg_contracts_check.py")
        )
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            _contracts_module = mod
    return _contracts_module
