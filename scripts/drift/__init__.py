"""Repo Drift Detector package.

Provides tiered drift detection for documentation consistency.
"""

from .defaults import resolve_rules, universal_rules
from .level1 import run_level1
from .level2 import run_level2
from .level3 import run_level3
from .models import (
    Category,
    DriftReport,
    Finding,
    FindingCounter,
    RepoProfile,
    Severity,
)
from .reporters import write_json_report, write_markdown_report

__all__ = [
    "Category",
    "DriftReport",
    "Finding",
    "FindingCounter",
    "RepoProfile",
    "Severity",
    "resolve_rules",
    "run_level1",
    "run_level2",
    "run_level3",
    "universal_rules",
    "write_json_report",
    "write_markdown_report",
]
