#!/usr/bin/env python3
"""Canonical quality-review entry point for the batch summary aggregator.

The implementation is shared with the daily skill scripts directory so the
aggregator can be used alongside ``daily_kpi.py`` without importing or
changing KPI code.  This shim keeps the quality-review package self-contained
for callers that discover tools from this directory.
"""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


_IMPLEMENTATION = Path(__file__).parents[1] / "scripts" / "quality_summary.py"
_SPEC = spec_from_file_location("_training_cw5_quality_summary", _IMPLEMENTATION)
if _SPEC is None or _SPEC.loader is None:  # pragma: no cover - installation error
    raise ImportError(f"cannot load quality summary implementation: {_IMPLEMENTATION}")
_MODULE = module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
for _name in dir(_MODULE):
    if not _name.startswith("__"):
        globals()[_name] = getattr(_MODULE, _name)


if __name__ == "__main__":
    raise SystemExit(main())
