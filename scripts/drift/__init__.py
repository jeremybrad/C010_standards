"""Repo Drift Detector package.

Provides tiered drift detection for documentation consistency.
"""

from .level1 import run_level1
from .level2 import run_level2
from .level3 import run_level3
from .models import (
    Category,
    DriftReport,
    Finding,
    FindingCounter,
    Severity,
)
from .reporters import write_json_report, write_markdown_report

__all__ = [
    "Category",
    "DriftReport",
    "Finding",
    "FindingCounter",
    "Severity",
    "run_level1",
    "run_level2",
    "run_level3",
    "write_json_report",
    "write_markdown_report",
]
