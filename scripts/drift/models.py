"""Data models for the Repo Drift Detector.

Defines Finding, Severity, and Category classes for structured drift reporting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class Severity(Enum):
    """Severity levels for drift findings.

    CRITICAL: Canonical docs reference nonexistent paths/commands;
              validator inventory contradicts AVAILABLE_VALIDATORS;
              broken links in canonical docs.
    MAJOR:    Contradictions across canonical docs but not directly executable.
    MINOR:    Low-risk inconsistencies; stale path references that still work.
    INFO:     Observations only; style suggestions.
    """
    CRITICAL = "CRITICAL"
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    INFO = "INFO"

    def __lt__(self, other: Severity) -> bool:
        order = [Severity.INFO, Severity.MINOR, Severity.MAJOR, Severity.CRITICAL]
        return order.index(self) < order.index(other)


class Category(Enum):
    """Categories of drift findings."""
    INVENTORY_MISMATCH = "inventory_mismatch"
    BROKEN_LINK = "broken_link"
    STALE_PATH = "stale_path"
    ORPHAN_CANDIDATE = "orphan_candidate"
    MISPLACED_ARTIFACT = "misplaced_artifact"
    META_MISMATCH = "meta_mismatch"
    GENERATOR_DRIFT = "generator_drift"
    DOC_CONTRADICTION = "doc_contradiction"
    CONFIG_WARNING = "config_warning"


# Default severity for each category
DEFAULT_SEVERITY: dict[Category, Severity] = {
    Category.BROKEN_LINK: Severity.CRITICAL,
    Category.INVENTORY_MISMATCH: Severity.CRITICAL,
    Category.DOC_CONTRADICTION: Severity.MAJOR,
    Category.GENERATOR_DRIFT: Severity.MAJOR,
    Category.STALE_PATH: Severity.MINOR,
    Category.META_MISMATCH: Severity.MINOR,
    Category.ORPHAN_CANDIDATE: Severity.INFO,
    Category.MISPLACED_ARTIFACT: Severity.MINOR,
    Category.CONFIG_WARNING: Severity.INFO,
}


@dataclass
class Finding:
    """A single drift finding.

    Attributes:
        id: Stable identifier (e.g., "DRIFT-L1-001")
        level_detected: Detection level (1, 2, or 3)
        severity: Severity level
        category: Category of the finding
        message: Human-readable description
        file: File path if applicable
        line: Line number if applicable
        suggested_fix: List of remediation steps
        confidence: Confidence level (high, medium, low)
        requires_review: Whether manual review is required
        context: Additional context data
    """
    id: str
    level_detected: int
    severity: Severity
    category: Category
    message: str
    file: str | None = None
    line: int | None = None
    suggested_fix: list[str] = field(default_factory=list)
    confidence: str = "high"
    requires_review: bool = False
    context: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert finding to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "level": self.level_detected,
            "severity": self.severity.value,
            "category": self.category.value,
            "message": self.message,
            "file": self.file,
            "line": self.line,
            "suggested_fix": self.suggested_fix,
            "confidence": self.confidence,
            "requires_review": self.requires_review,
            "context": self.context,
        }


class FindingCounter:
    """Counter for generating unique finding IDs."""

    def __init__(self) -> None:
        self._counts: dict[int, int] = {1: 0, 2: 0, 3: 0}

    def next_id(self, level: int) -> str:
        """Generate the next finding ID for the given level."""
        self._counts[level] += 1
        return f"DRIFT-L{level}-{self._counts[level]:03d}"


@dataclass
class DriftReport:
    """Complete drift detection report.

    Attributes:
        repo_name: Name of the repository
        repo_sha: Short git SHA
        repo_branch: Current branch name
        level: Detection level (1, 2, or 3)
        generated_at: ISO timestamp
        findings: List of all findings
        inventories: Inventory comparison data
    """
    repo_name: str
    repo_sha: str
    repo_branch: str
    level: int
    generated_at: str
    findings: list[Finding] = field(default_factory=list)
    inventories: dict[str, Any] = field(default_factory=dict)

    def counts_by_severity(self) -> dict[Severity, int]:
        """Count findings by severity."""
        counts = {s: 0 for s in Severity}
        for f in self.findings:
            counts[f.severity] += 1
        return counts

    def has_critical(self) -> bool:
        """Check if any CRITICAL findings exist."""
        return any(f.severity == Severity.CRITICAL for f in self.findings)

    def to_dict(self) -> dict[str, Any]:
        """Convert report to dictionary for JSON serialization."""
        counts = self.counts_by_severity()
        return {
            "metadata": {
                "repo": self.repo_name,
                "repo_sha": self.repo_sha,
                "repo_branch": self.repo_branch,
                "level": self.level,
                "generated_at": self.generated_at,
                "detector_version": "1.0.0",
            },
            "summary": {
                "critical": counts[Severity.CRITICAL],
                "major": counts[Severity.MAJOR],
                "minor": counts[Severity.MINOR],
                "info": counts[Severity.INFO],
                "total": len(self.findings),
            },
            "findings": [f.to_dict() for f in self.findings],
            "inventories": self.inventories,
        }


@dataclass
class RepoProfile:
    """Profile of a repository's structure for gating drift checks.

    Flags indicate which C10-specific directories/files exist so the detector
    can skip checks that would produce false positives on non-C10 repos.
    """
    repo_root: Path
    has_validators: bool = False
    has_schemas: bool = False
    has_taxonomies: bool = False
    has_meta_yaml: bool = False
    has_project_primer: bool = False
    has_drift_rules: bool = False

    @classmethod
    def detect(cls, repo_root: Path) -> RepoProfile:
        """Auto-detect repository profile from filesystem."""
        validators_dir = repo_root / "validators"
        return cls(
            repo_root=repo_root,
            has_validators=(
                validators_dir.is_dir()
                and (validators_dir / "__init__.py").exists()
            ),
            has_schemas=(repo_root / "schemas").is_dir(),
            has_taxonomies=(repo_root / "taxonomies").is_dir(),
            has_meta_yaml=(repo_root / "META.yaml").is_file(),
            has_project_primer=(repo_root / "PROJECT_PRIMER.md").is_file(),
            has_drift_rules=(repo_root / "30_config" / "drift_rules.yaml").is_file(),
        )
