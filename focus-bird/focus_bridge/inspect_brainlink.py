#!/usr/bin/env python3
"""
BrainLinkParser.pyd 參數偵測器
Run this to find the exact parameter names.
"""
import inspect, sys

# Force load from current directory
import importlib.util
spec = importlib.util.spec_from_file_location("BrainLinkParser", "BrainLinkParser.pyd")
if spec is None:
    spec = importlib.util.spec_from_file_location("BrainLinkParser", "./BrainLinkParser.pyd")
if spec is None:
    print("Error: BrainLinkParser.pyd not found in current folder")
    sys.exit(1)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Show __init__ signature
try:
    sig = inspect.signature(module.BrainLinkParser.__init__)
    print("BrainLinkParser.__init__ parameters:")
    for name, param in sig.parameters.items():
        if name == 'self':
            continue
        default = param.default
        if default is inspect.Parameter.empty:
            print(f"  {name} (required)")
        else:
            print(f"  {name} = {default}")
except Exception as e:
    print(f"inspect failed: {e}")
    # Fallback: try to show __text_signature__
    try:
        print(f"__text_signature__: {module.BrainLinkParser.__init__.__text_signature__}")
    except:
        pass

# Also show all callable methods
print("\nAll callable methods:")
for name in dir(module.BrainLinkParser):
    if not name.startswith('_'):
        print(f"  {name}")
